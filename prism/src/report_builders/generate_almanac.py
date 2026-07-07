#!/usr/bin/env python3
"""
generate_almanac.py

Auto-fills the R3 Almanac Agent markdown report from the Almanac Collector's
JSON output, and writes it to weekNN/r3/almanac.md.

Usage:
    python generate_almanac.py <collector_json_path> <week_number> [--out-root OUTPUT_ROOT]

Example:
    python generate_almanac.py almanac_collector_output.json 8
    -> creates ./week08/r3/almanac.md

Notes:
    - "week_number" is your internal sprint week number (the collector JSON
      does not contain it), so pass it explicitly each run.
    - The narrative sentences (bias, confidence, thesis) are generated with
      simple rule-based logic from the sector spread and active calendar
      flags -- same judgment calls that were made manually in W05. Tune the
      thresholds in the CONFIG section below if the "house style" changes,
      and always sanity-check the auto-generated thesis before presenting.
"""

import json
import re
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG -- tune these thresholds if the analytical house style changes
# ---------------------------------------------------------------------------
BULLISH_SPREAD_THRESHOLD = 3.0   # |leader_avg - laggard_avg| above this => mild directional lean
STRONG_SPREAD_THRESHOLD = 6.0    # above this => confident directional call
MAX_LOW_CONF_FLAGS = 1           # more active caution flags than this caps confidence at Medium

# Maps calendar_flags boolean keys -> human label used in the caution narrative.
# The *_seasonal_weakness_flag key is handled separately since its name changes by month.
CAUTION_FLAG_LABELS = {
    "midterm_year_flag": "midterm-year caution",
    "options_expiry_week_flag": "options-expiry-week volatility risk",
    "market_holiday_in_window_flag": "market-holiday disruption",
    "compressed_trading_week_flag": "compressed trading week",
}


def fmt_date(d: str) -> str:
    return datetime.strptime(d, "%Y-%m-%d").strftime("%-d %B %Y")


def find_seasonal_weakness_flag(calendar_flags: dict):
    """Collector currently encodes a *_seasonal_weakness_flag keyed to a
    specific month (e.g. june_seasonal_weakness_flag). Find it dynamically."""
    for key, value in calendar_flags.items():
        if key.endswith("_seasonal_weakness_flag"):
            month_word = key.replace("_seasonal_weakness_flag", "").capitalize()
            return key, month_word, value
    return None, None, False


def active_caution_flags(calendar_flags: dict):
    active = []
    for key, label in CAUTION_FLAG_LABELS.items():
        if calendar_flags.get(key):
            active.append(label)
    _, month_word, sw_value = find_seasonal_weakness_flag(calendar_flags)
    if sw_value:
        active.append(f"{month_word} seasonal weakness")
    return active


def compute_bias_and_confidence(leading, lagging, calendar_flags):
    top_avg = sum(s["weekly_change_pct"] for s in leading) / len(leading)
    bottom_avg = sum(s["weekly_change_pct"] for s in lagging) / len(lagging)
    spread = top_avg - bottom_avg
    caution = active_caution_flags(calendar_flags)

    if spread >= STRONG_SPREAD_THRESHOLD:
        bias = "Risk-on / bullish"
    elif spread >= BULLISH_SPREAD_THRESHOLD:
        bias = "Mildly risk-on"
    elif spread <= -STRONG_SPREAD_THRESHOLD:
        bias = "Risk-off / bearish"
    elif spread <= -BULLISH_SPREAD_THRESHOLD:
        bias = "Mildly risk-off"
    else:
        bias = "Neutral-cautious"

    if len(caution) >= 3:
        confidence = "Low"
    elif len(caution) > MAX_LOW_CONF_FLAGS or abs(spread) < BULLISH_SPREAD_THRESHOLD:
        confidence = "Medium"
    else:
        confidence = "High"

    return bias, confidence, top_avg, bottom_avg, spread, caution


def sector_list_str(sectors):
    return ", ".join(f"{s['sector']} / {s['ticker']}" for s in sectors)


def sector_bullets(sectors):
    return [f"{s['sector']} / {s['ticker']} at {s['weekly_change_pct']:+.2f}%" for s in sectors]


def cycle_phase_from_year(year: int) -> str:
    """Same anchoring as almanac_collector.py's is_midterm_year (2024 = election year)."""
    r = (year - 2024) % 4
    return {
        0: "election_year",
        1: "post_election_year",
        2: "midterm_year",
        3: "pre_election_year",
    }[r]


def load_seasonality(seasonality_json_path):
    if not seasonality_json_path:
        return None
    p = Path(seasonality_json_path)
    if not p.exists():
        print(f"[warn] seasonality file not found, skipping monthly stats fill: {p}")
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def monthly_stats_row(seasonality: dict, index_label: str, month: int, year: int):
    """Return (seasonal_rank, seasonal_avg, cycle_rank, cycle_avg) as display
    strings, falling back to 'Not automated' for anything missing."""
    fallback = ("Not automated", "Not automated", "Not automated", "Not automated")
    if not seasonality:
        return fallback

    idx_data = seasonality.get("indices", {}).get(index_label)
    if not idx_data or "error" in idx_data:
        return fallback

    seasonal_rank = idx_data.get("monthly_rank", {}).get(str(month)) or idx_data.get("monthly_rank", {}).get(month)
    seasonal_avg = idx_data.get("monthly_avg_return_pct", {}).get(str(month)) or idx_data.get("monthly_avg_return_pct", {}).get(month)

    phase = cycle_phase_from_year(year)
    phase_data = idx_data.get("by_cycle_phase", {}).get(phase, {})
    cycle_rank = phase_data.get("rank_by_month", {}).get(str(month)) or phase_data.get("rank_by_month", {}).get(month)
    cycle_avg = phase_data.get("avg_return_pct_by_month", {}).get(str(month)) or phase_data.get("avg_return_pct_by_month", {}).get(month)

    return (
        str(seasonal_rank) if seasonal_rank is not None else "Not automated",
        f"{seasonal_avg:+.2f}%" if seasonal_avg is not None else "Not automated",
        str(cycle_rank) if cycle_rank is not None else "Not automated",
        f"{cycle_avg:+.2f}%" if cycle_avg is not None else "Not automated",
    )


def build_markdown(data: dict, week_number: int, seasonality: dict = None) -> str:
    cf = data["calendar_flags"]
    fw = data["forecast_window"]
    leading = data["sector_ranking"]["leading_sectors"]
    lagging = data["sector_ranking"]["lagging_sectors"]

    week_label = f"W{int(week_number):02d}"
    start_fmt = fmt_date(fw["start"])
    end_fmt = fmt_date(fw["end"])
    month_name = cf.get("month", datetime.strptime(fw["start"], "%Y-%m-%d").strftime("%B"))
    year = datetime.strptime(fw["start"], "%Y-%m-%d").year

    sw_key, sw_month, sw_value = find_seasonal_weakness_flag(cf)
    sw_month = sw_month or month_name
    midterm = cf.get("midterm_year_flag", False)
    expiry_flag = cf.get("options_expiry_week_flag", False)
    expiry_date = cf.get("options_expiry_date")
    holiday_flag = cf.get("market_holiday_in_window_flag", False)
    compressed_flag = cf.get("compressed_trading_week_flag", False)

    bias, confidence, top_avg, bottom_avg, spread, caution = compute_bias_and_confidence(
        leading, lagging, cf
    )

    leaders_str = sector_list_str(leading)
    laggers_str = sector_list_str(lagging)
    leader_bullets = sector_bullets(leading)
    lagger_bullets = sector_bullets(lagging)

    caution_str = ", ".join(caution) if caution else "no active seasonal or cycle-year caution flags"
    breadth_word = "mixed" if abs(spread) < STRONG_SPREAD_THRESHOLD else ("bullish" if spread > 0 else "bearish")

    # --- Cycle context table rows ---
    cycle_rows = []
    cycle_rows.append(
        f"| {week_label}: {start_fmt} - {end_fmt} | "
        f"{(sw_month + ' seasonal weakness flag is active' if sw_value else sw_month + ' seasonal weakness flag is not active')}"
        f"{' and midterm-year flag is active.' if midterm else '; midterm-year flag is not active.'} | "
        f"{'Use as a confidence reducer, not as a hard directional signal.' if caution else 'No calendar-based confidence reduction required.'} |"
    )
    if expiry_flag and expiry_date:
        cycle_rows.append(
            f"| Options-expiry week | Options-expiry date is {fmt_date(expiry_date)}, inside this forecast window. | "
            f"Apply an options-expiry-week volatility caveat for {week_label}. |"
        )
    else:
        cycle_rows.append(
            f"| Post-options-expiry period | No options-expiry date falls inside this forecast window. | "
            f"Do not apply a direct options-expiry-week penalty for {week_label}. |"
        )
    cycle_rows.append(
        f"| {month_name} seasonal context | The collector does not provide exact historical average returns for {month_name}. | "
        f"Keep the almanac signal data-driven and avoid unsupported statistics. |"
    )

    lines = []
    lines.append(f"# Almanac Agent Output — R3 — Week {week_label}")
    lines.append("")
    lines.append(f"**Sprint:** Week {week_label}")
    lines.append(f"**Market week:** {start_fmt} – {end_fmt}")
    lines.append("**Role:** R3 — Almanac Agent Lead")
    lines.append("**File:** `almanac.md`")
    lines.append("**Purpose:** Provide the seasonal / calendar-pattern evidence leg before LLM synthesis. This is a probability-context document, not a standalone trading call.")
    lines.append("")
    lines.append("> **Commit note:** If this file is uploaded to GitHub, also upload the folder `almanac_assets/` so the charts render correctly.")
    lines.append(f"> **Auto-generated:** Generated from `{data.get('collector', 'Almanac Collector')}` output dated {data.get('generated_at', 'unknown')}. Review narrative sections before presenting.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. R3 Presentation Bullets — Max 3 Points")
    lines.append("")
    lines.append(f"* **Month rank / cycle context:** {month_name} {year} carries {caution_str}. Historically, the S&P 500 and NASDAQ monthly return statistics were not automatically collected by the current Almanac Collector, so exact average return values should not be invented.")
    lines.append("")
    expiry_bit = f"contains an options-expiry date ({fmt_date(expiry_date)})" if (expiry_flag and expiry_date) else "does not contain an options-expiry week"
    holiday_bit = "a market holiday" if holiday_flag else "no market holiday"
    compressed_bit = "is a compressed trading week" if compressed_flag else "is not a compressed trading week"
    lines.append(f"* **Most relevant week pattern:** Week {week_label} {expiry_bit}, has {holiday_bit}, and {compressed_bit}.")
    lines.append("")
    lines.append(f"* **Sector seasonality / confidence:** **{bias}, {confidence} confidence.** The strongest current sector evidence comes from {leaders_str}. However, {laggers_str} are lagging, so broad sector breadth leans {breadth_word}.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Visual Evidence Summary")
    lines.append("")
    lines.append(f"### 2.1 {week_label} Calendar Risk Flags")
    lines.append("")
    lines.append(f"**Interpretation:** The collector identifies {caution_str} as active. R3 should {'reduce confidence accordingly' if (caution or expiry_flag) else 'not apply a calendar-based confidence reduction'}.")
    lines.append("")
    lines.append(f"### 2.2 {week_label} Sector Leadership Ranking")
    lines.append("")
    lines.append(f"**Interpretation:** Sector leadership is led by {', '.join(leader_bullets)}. This suggests market leadership is {'broad-based' if top_avg > 0 else 'weak even among relative leaders'}.")
    lines.append("")
    lines.append(f"### 2.3 {week_label} Sector Lagging Ranking")
    lines.append("")
    lines.append(f"**Interpretation:** The weakest sectors are {', '.join(lagger_bullets)}. The sector picture is {breadth_word}.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Structured Almanac Agent Output for LLM Synthesis")
    lines.append("")
    lines.append("### MONTH")
    lines.append("")
    lines.append(f"**{month_name} {year}** — {caution_str if caution else 'no active structural seasonal caution block'}.")
    lines.append("")
    lines.append("### CYCLE CONTEXT")
    lines.append("")
    lines.append(f"{year} is {'a **midterm year**' if midterm else 'not flagged as a midterm year'}. The Almanac framework treats **{month_name} in this cycle-year setting** based on the active flags below.")
    lines.append("")
    lines.append("| Cycle Window | Historical Context | R3 Use |")
    lines.append("| --- | --- | --- |")
    lines.extend(cycle_rows)
    lines.append("")
    interp1 = f"The cycle context matters because {caution_str} warn that the week may carry elevated risk." if caution else "No active cycle-context flags reduce confidence this week."
    interp2 = "The options-expiry date inside this window adds a volatility caveat." if expiry_flag else "The absence of options-expiry, holiday, and compressed-week flags keeps calendar pressure low."
    lines.append(f"**Interpretation:** {interp1} {interp2}")
    lines.append("")
    lines.append("### MONTHLY STATS")
    lines.append("")
    lines.append(f"| Index / Asset | {month_name} Seasonal Rank | {month_name} Avg % Return | Cycle-Year Rank | Cycle-Year Avg % Return | R3 Interpretation |")
    lines.append("| --- | :---: | :---: | :---: | :---: | --- |")
    for index_label, note_if_automated, note_if_not in [
        ("S&P 500", "Historical seasonal rank and average return computed from full price history.", "No collector-based monthly statistic available."),
        ("DJIA / Dow", "Historical seasonal rank and average return computed from full price history.", "No collector-based monthly statistic available."),
        ("NASDAQ", "Historical seasonal rank and average return computed from full price history.", "Use sector leadership as the stronger evidence source instead of unsupported monthly stats."),
        ("Russell 2000 / IWM", "Historical seasonal rank and average return computed from full price history.", "No collector-based monthly statistic available."),
    ]:
        s_rank, s_avg, c_rank, c_avg = monthly_stats_row(seasonality, index_label, datetime.strptime(fw["start"], "%Y-%m-%d").month, year)
        note = note_if_automated if s_rank != "Not automated" else note_if_not
        lines.append(f"| **{index_label}** | {s_rank} | {s_avg} | {c_rank} | {c_avg} | {note} |")
    lines.append("")
    lines.append(f"**Net monthly signal:** **{bias}.**")
    lines.append("")
    lines.append("### SPECIFIC WEEK / DAY PATTERN")
    lines.append("")
    lines.append("| Pattern | Direction | Strength | R3 Treatment |")
    lines.append("| --- | --- | --- | --- |")
    if sw_value:
        lines.append(f"| {sw_month} seasonal weakness flag | Bearish / cautious | Medium | Use as a confidence reducer. |")
    else:
        lines.append(f"| {sw_month} seasonal weakness flag | Neutral | Low | No seasonal weakness flag active this window. |")
    if midterm:
        lines.append("| Midterm-year flag | Bearish / cautious | Medium | Adds caution to the forecast, especially if other agents disagree. |")
    else:
        lines.append("| Midterm-year flag | Neutral | Low | Midterm-year flag not active. |")
    if expiry_flag:
        lines.append("| Options-expiry-week flag is true | Bearish / cautious | Medium | Apply an options-expiry-week volatility caveat. |")
    else:
        lines.append("| Options-expiry-week flag is false | Neutral | Low | No direct options-expiry-week penalty. |")
    if holiday_flag or compressed_flag:
        lines.append("| Market-holiday / compressed-week flag is true | Bearish / cautious | Low-Medium | Reduce liquidity expectations and widen error bars. |")
    else:
        lines.append("| Market-holiday and compressed-week flags are false | Neutral | Low | Calendar structure is clean this week. |")
    lines.append("")
    week_implication = (
        "Seasonality and calendar risk argue for a cautious stance; sector evidence can only partially offset this."
        if len(caution) >= 2
        else "Seasonality does not provide a strong directional signal by itself; sector evidence should carry more weight this week."
    )
    lines.append(f"**Week {week_label} implication:** {week_implication}")
    lines.append("")
    lines.append("### SECTOR SEASONALITY SIGNALS")
    lines.append("")
    lines.append("| Sector / ETF Proxy | Almanac Seasonal Window | Signal | R3 Use in Prediction |")
    lines.append("| --- | --- | --- | --- |")
    for s in leading:
        lines.append(f"| **{s['sector']} / {s['ticker']}** | {week_label} current collector window | Bullish / positive current evidence | {s['sector']} is a leading sector at {s['weekly_change_pct']:+.2f}%, supporting a risk-on interpretation. |")
    for s in lagging:
        lines.append(f"| **{s['sector']} / {s['ticker']}** | {week_label} current collector window | Bearish / weak current evidence | {s['sector']} is a lagging sector at {s['weekly_change_pct']:+.2f}%, so it should not be used as a leader. |")
    lines.append("")
    breadth_desc = "Sector breadth is constructive at the leadership level" if top_avg > 0 else "Sector breadth is weak even at the leadership level"
    lines.append(f"**Net sector signal:** {breadth_desc}, while {laggers_str} weigh on the picture. The net sector signal is **{bias}**.")
    lines.append("")
    lines.append("### ALMANAC SEASONAL BIAS")
    lines.append("")
    lines.append(f"**{bias}.**")
    lines.append("")
    lines.append("### CONFIDENCE")
    lines.append("")
    lines.append(f"**{confidence}.**")
    reasoning_flags = caution_str.capitalize() if caution else "No active caution flags"
    reasoning_expiry = "and an options-expiry date falls inside this window" if expiry_flag else "with no options-expiry, holiday, or compressed-week flag active"
    reasoning_spread = "a strong signal" if abs(spread) >= STRONG_SPREAD_THRESHOLD else "a moderate signal"
    lines.append(f"Reasoning: {reasoning_flags} {reasoning_expiry}. Sector spread between leaders and laggards is {spread:+.2f} percentage points, which is {reasoning_spread}.")
    lines.append("")
    lines.append("### ALMANAC THESIS")
    lines.append("")
    thesis_filter = "a caution filter" if (caution or expiry_flag) else "a data point"
    thesis_caution = (caution_str.capitalize() + " conditions warn that volatility and false breaks are possible.") if caution else "No structural calendar warnings are active this week."
    thesis_action = "reduce confidence but not override bullish or bearish evidence from Technical or Macro agents" if caution else "let sector evidence lead, since no calendar caution flags are active"
    lines.append(f"The {week_label} Almanac signal should be treated as {thesis_filter} rather than a standalone forecast. {thesis_caution} Current sector ranking shows leadership in {leaders_str}, while {laggers_str} lag. R3 should {thesis_action} if those agents also support the same direction.")
    lines.append("")
    lines.append("### KEY OUTPUT SENTENCE")
    lines.append("")
    offset_word = "offsets" if spread > 0 else "reinforces"
    lines.append(f"**Seasonality suggests {bias.lower()}, with {confidence.lower()} confidence, because {caution_str}, while sector leadership in {leaders_str} {offset_word} the calendar risk.**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. R3 Handoff to R6 / R7")
    lines.append("")
    lines.append("### What R6 should paste into the multi-LLM prompt")
    lines.append("")
    lines.append("Use the full **Structured Almanac Agent Output** section from the previous block.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Final R3 Slide Text")
    lines.append("")
    lines.append(f"**R3 Almanac Agent — Week {week_label}**")
    lines.append("")
    bullet1 = (caution_str.capitalize() + " remain active, so Almanac reduces confidence.") if caution else "No active seasonal or cycle-year caution flags this week."
    bullet2 = f"An options-expiry date falls inside this window ({fmt_date(expiry_date)}), adding volatility risk." if (expiry_flag and expiry_date) else f"Week {week_label} has no options-expiry-week, market-holiday, or compressed trading-week flag."
    lines.append(f"* {bullet1}")
    lines.append(f"* {bullet2}")
    lines.append(f"* Sector evidence: {leaders_str} lead, while {laggers_str} lag.")

    return "\n".join(lines) + "\n"


def detect_next_week_number(root: Path) -> int:
    """Scan the repo root for existing Week{N} / Week{N}_Evidence folders and
    return the next sequential week number. Falls back to 1 if none found."""
    pattern = re.compile(r"^Week(\d+)", re.IGNORECASE)
    max_week = 0
    for child in root.iterdir():
        if not child.is_dir():
            continue
        m = pattern.match(child.name)
        if m:
            max_week = max(max_week, int(m.group(1)))
    return max_week + 1 if max_week > 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Generate R3 Almanac Agent markdown from collector JSON.")
    parser.add_argument("json_path", help="Path to the Almanac Collector JSON output")
    parser.add_argument(
        "week_number",
        type=int,
        nargs="?",
        default=None,
        help="Sprint week number, e.g. 8 for W08. If omitted, auto-detected from existing Week{N} folders under --out-root.",
    )
    parser.add_argument("--out-root", default=".", help="Repo root containing Week{N} folders")
    parser.add_argument(
        "--seasonality-json",
        default=None,
        help="Path to monthly_seasonality.json (from seasonality_collector.py). "
             "If given, fills real numbers into the MONTHLY STATS table instead of 'Not automated'.",
    )
    parser.add_argument(
        "--charts-dir",
        default=None,
        help="Directory containing this week's almanac chart PNGs (e.g. prism/data/almanac/charts). "
             "If given, copies them into Week{N}/R3_almanac/almanac_assets/ alongside the report.",
    )
    args = parser.parse_args()

    with open(args.json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    seasonality = load_seasonality(args.seasonality_json)

    out_root = Path(args.out_root)
    week_number = args.week_number
    if week_number is None:
        week_number = detect_next_week_number(out_root)
        print(f"[auto] No week number given -- detected next week as {week_number}")

    md = build_markdown(data, week_number, seasonality)

    n = int(week_number)
    out_dir = out_root / f"Week{n}" / "R3_almanac"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"almanac_agent_W{n:02d}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")

    if args.charts_dir:
        charts_src = Path(args.charts_dir)
        if charts_src.is_dir():
            assets_dir = out_dir / "almanac_assets"
            assets_dir.mkdir(parents=True, exist_ok=True)
            copied = 0
            for png in charts_src.glob("*.png"):
                shutil.copy2(png, assets_dir / png.name)
                copied += 1
            print(f"[OK] Archived {copied} chart(s) into {assets_dir}")
        else:
            print(f"[warn] charts-dir not found, skipping chart archiving: {charts_src}")


if __name__ == "__main__":
    main()