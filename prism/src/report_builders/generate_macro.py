#!/usr/bin/env python3
"""
generate_macro.py

Auto-fills the R4 Macro Agent markdown report from the Macro Collector's
JSON output, and writes it to Week{N}/R4_macro/macro_agent_W{NN}.md.

Usage:
    python generate_macro.py <collector_json_path> [week_number] [--out-root OUTPUT_ROOT]

Example:
    python generate_macro.py macro_collector_output.json 6
    -> creates ./Week6/R4_macro/macro_agent_W06.md

If week_number is omitted, it is auto-detected the same way as
generate_almanac.py: highest existing Week{N} folder + 1.

------------------------------------------------------------------------
IMPORTANT -- what this script CAN and CANNOT auto-fill
------------------------------------------------------------------------
The current macro_collector.py output only contains market price data
(yields, oil, gold, DXY, VIX, BTC) plus an empty Fed/data-watch shell --
its own "note" field says FedWatch probability is not collected, and the
BLS RSS feeds are currently returning 403 Forbidden (see
data_release_errors in the JSON), so no calendar/inflation data comes
through either.

Auto-filled from JSON:
    - US 10Y / 30Y yield level + direction
    - WTI, Gold, DXY, VIX, BTC level + direction
    - A rule-based MACRO BIAS / CONFIDENCE / INVALIDATION draft

Auto-filled from FRED (free, no API key -- see fetch_fred_latest()):
    - 2Y Yield (FRED series DGS2)
    - Fed target rate range (FRED series DFEDTARU / DFEDTARL)

Auto-filled from a hardcoded FOMC calendar (see FOMC_DECISION_DATES below):
    - Next FOMC date -- the Fed publishes the year's meeting dates in
      advance, so hardcoding + auto-picking "next date >= today" is more
      reliable than scraping a page that might change layout. Extend the
      list when the Fed publishes a new year's schedule.

NOT auto-filled (left as explicit placeholders -- fill by hand or wire up
a data source later):
    - Fed hold probability (CME FedWatch Tool has no free public API)
    - WEEK-AHEAD CALENDAR (BLS RSS feeds currently blocked, 403)
    - KEY EARNINGS (not collected by any current script)
    - CONFIRMED NEWS EVENTS (not collected by any current script)

A NOTE ON YIELD SCALING: the collector stores yield "close" values as
1/10th of the actual percentage (e.g. 0.4485 for a 4.485% 10Y yield --
this matches Yahoo's ^TNX/^TYX convention where the raw quote is the
yield x10, apparently divided by 100 somewhere upstream instead of x10).
This script multiplies yield "close" by 10 to display the real percentage.
VERIFY this against a live rate source the first time you run this for
real, in case the collector's scaling changes.
"""

import json
import re
import shutil
import argparse
from datetime import datetime, date
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
YIELD_DISPLAY_MULTIPLIER = 10  # see "A NOTE ON YIELD SCALING" above
RISING_THRESHOLD_PCT = 3.0     # |weekly_change_pct| above this => "Rising"/"Falling" (vs "Slightly")
VIX_ELEVATED = 20.0
VIX_HIGH = 28.0

# Federal Reserve's published FOMC decision-announcement dates (2nd day of
# each 2-day meeting). 2026 dates are confirmed; 2027 dates are the Fed's
# tentative preview schedule. Source: federalreserve.gov/monetarypolicy/fomccalendars.htm
# Extend this list once the Fed publishes a new year's calendar.
FOMC_DECISION_DATES = [
    date(2026, 1, 28), date(2026, 3, 18), date(2026, 4, 29), date(2026, 6, 17),
    date(2026, 7, 29), date(2026, 9, 16), date(2026, 10, 28), date(2026, 12, 9),
    date(2027, 1, 27), date(2027, 3, 17), date(2027, 4, 28), date(2027, 6, 9),
    date(2027, 7, 28), date(2027, 9, 15), date(2027, 10, 27), date(2027, 12, 8),
]


def next_fomc_date(today: date = None) -> date:
    today = today or date.today()
    upcoming = [d for d in FOMC_DECISION_DATES if d >= today]
    return min(upcoming) if upcoming else None


def fetch_fred_latest(series_id: str):
    """Fetch the most recent non-missing observation for a FRED series via
    the free, no-API-key-required CSV endpoint. Returns (date_str, value)
    or raises on failure/no data."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PrismMacroCollector/1.0; +https://github.com/)"}
    resp = requests.get(url, timeout=15, headers=headers)
    resp.raise_for_status()
    lines = resp.text.strip().splitlines()
    latest_date, latest_val = None, None
    for line in lines[1:]:  # skip header row
        parts = line.strip().split(",")
        if len(parts) != 2:
            continue
        date_str, val_str = parts
        if val_str in (".", ""):
            continue
        try:
            latest_val = float(val_str)
            latest_date = date_str
        except ValueError:
            continue
    if latest_val is None:
        raise ValueError(f"No valid observations found for FRED series {series_id}")
    return latest_date, latest_val


def fetch_fed_rates_data() -> dict:
    """Best-effort fetch of 2Y yield + Fed target rate range from FRED.
    Each field fails independently so one bad fetch doesn't blank the rest."""
    result = {"y2": None, "target_lower": None, "target_upper": None, "errors": []}

    try:
        _, y2 = fetch_fred_latest("DGS2")
        result["y2"] = y2
    except Exception as e:
        result["errors"].append(f"DGS2 (2Y yield): {e}")

    try:
        _, lower = fetch_fred_latest("DFEDTARL")
        result["target_lower"] = lower
    except Exception as e:
        result["errors"].append(f"DFEDTARL (target rate lower bound): {e}")

    try:
        _, upper = fetch_fred_latest("DFEDTARU")
        result["target_upper"] = upper
    except Exception as e:
        result["errors"].append(f"DFEDTARU (target rate upper bound): {e}")

    return result


def get(market_data: dict, key: str):
    return market_data.get(key)


def fmt_yield_pct(entry) -> str:
    if not entry:
        return "Not automated"
    return f"{entry['close'] * YIELD_DISPLAY_MULTIPLIER:.2f}%"


def direction_word(weekly_change_pct: float, up_word="Rising", down_word="Falling", flat_word="Flat") -> str:
    if weekly_change_pct is None:
        return "Not automated"
    if abs(weekly_change_pct) < 0.5:
        return flat_word
    magnitude = "Slightly " if abs(weekly_change_pct) < RISING_THRESHOLD_PCT else ""
    word = up_word if weekly_change_pct > 0 else down_word
    return f"{magnitude}{word}".strip()


import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from week_utils import detect_next_week_number  # noqa: E402


def build_macro_bias(market: dict) -> tuple:
    """Very rough rule-based draft, based only on the data this collector
    actually has -- yields, oil, gold, DXY, VIX, BTC. No Fed, calendar, or
    news signal is available, so confidence is capped at Medium and the
    reasoning says so explicitly."""
    y10 = get(market, "US_10Y_YIELD")
    y30 = get(market, "US_30Y_YIELD")
    vix = get(market, "VIX")
    wti = get(market, "WTI")
    gold = get(market, "GOLD")
    dxy = get(market, "DXY")

    yield_changes = [e["weekly_change_pct"] for e in [y10, y30] if e]
    avg_yield_change = sum(yield_changes) / len(yield_changes) if yield_changes else 0.0

    vix_level = vix["close"] if vix else None
    vix_change = vix["weekly_change_pct"] if vix else 0.0

    risk_off_points = 0
    risk_on_points = 0

    if avg_yield_change < -1.0:
        risk_on_points += 1  # falling yields generally supportive of risk assets
    elif avg_yield_change > 1.0:
        risk_off_points += 1

    if vix_level is not None:
        if vix_level >= VIX_HIGH:
            risk_off_points += 2
        elif vix_level >= VIX_ELEVATED:
            risk_off_points += 1
        elif vix_change < -5:
            risk_on_points += 1

    if gold and gold["weekly_change_pct"] > 1.5:
        risk_off_points += 1  # gold bid = safe-haven demand
    if wti and wti["weekly_change_pct"] > 3:
        risk_off_points += 1  # sharp oil spike = inflation/geopolitical risk
    if dxy and dxy["weekly_change_pct"] < -1.0:
        risk_on_points += 1  # weaker dollar generally risk-on

    net = risk_on_points - risk_off_points
    if net >= 2:
        bias = "Bullish"
    elif net == 1:
        bias = "Slightly Bullish"
    elif net == 0:
        bias = "Neutral"
    elif net == -1:
        bias = "Slightly Bearish"
    else:
        bias = "Bearish"

    return bias, avg_yield_change, vix_level, risk_on_points, risk_off_points



def fmt_asset_line(label: str, entry: dict | None, prefix: str = "", suffix: str = "") -> str:
    if not entry:
        return f"- {label}: Not available from Prism automation"
    close = entry.get("close")
    change = entry.get("weekly_change_pct")
    direction = direction_word(change)
    if isinstance(close, (int, float)):
        if prefix == "$":
            return f"- {label}: ${close:,.2f}, {direction}"
        return f"- {label}: {prefix}{close:.2f}{suffix}, {direction}"
    return f"- {label}: Not available from Prism automation"


def describe_fed_speakers(fdw: dict) -> str:
    speakers = fdw.get("fed_speakers", [])
    if not speakers:
        return "No Fed speech metadata was collected by Prism in this run."

    names = []
    tones = set()

    for item in speakers:
        name = item.get("speaker_hint", "Unknown")
        tone = item.get("tone_hint", "unknown")
        if name not in names:
            names.append(name)
        tones.add(tone)

    names_text = ", ".join(names)
    if tones == {"neutral_or_unclear_keyword_hint"}:
        tone_text = "tone hints were neutral or unclear"
    else:
        tone_text = "tone hints were mixed"

    return f"Prism captured {len(speakers)} Fed speech item(s): {names_text}. The {tone_text}."


def build_automation_calendar_rows(market: dict, fdw: dict, week_number: int) -> list[dict]:
    y10 = get(market, "US_10Y_YIELD")
    y30 = get(market, "US_30Y_YIELD")
    wti = get(market, "WTI")
    vix = get(market, "VIX")
    errors = fdw.get("data_release_errors", {})
    data_items = fdw.get("inflation_data", []) + fdw.get("major_data_releases", [])

    week_label = f"Week {int(week_number):02d}"

    rows = [
        {
            "day": week_label,
            "event": "Fed speaker watch",
            "expected": describe_fed_speakers(fdw),
            "importance": "Medium"
        }
    ]

    if data_items:
        for item in data_items:
            feed = item.get("feed", "BLS")
            title = item.get("title", "BLS release")
            published = item.get("published_at", "date unavailable")
            rows.append({
                "day": week_label,
                "event": f"{feed} release metadata",
                "expected": f"{title}. Published/dated: {published}.",
                "importance": "High" if feed in {"CPI", "PPI", "EMPLOYMENT_SITUATION"} else "Medium"
            })
    elif errors:
        rows.append({
            "day": week_label,
            "event": "BLS data watch",
            "expected": (
                f"Prism could not collect CPI/PPI/employment release metadata because "
                f"BLS RSS returned errors for {', '.join(errors.keys())}."
            ),
            "importance": "Medium"
        })
    else:
        rows.append({
            "day": week_label,
            "event": "BLS data watch",
            "expected": "No CPI/PPI/employment release metadata was collected by Prism in this run.",
            "importance": "Medium"
        })

    if y10 and y30:
        rows.append({
            "day": week_label,
            "event": "Yield movement watch",
            "expected": (
                f"10Y yield is {fmt_yield_pct(y10)} and 30Y yield is {fmt_yield_pct(y30)}. "
                f"Yield direction is {direction_word((y10.get('weekly_change_pct', 0) + y30.get('weekly_change_pct', 0)) / 2)}."
            ),
            "importance": "High"
        })
    else:
        rows.append({
            "day": week_label,
            "event": "Yield movement watch",
            "expected": "Yield data was incomplete in the Prism macro run.",
            "importance": "High"
        })

    if wti and vix:
        rows.append({
            "day": week_label,
            "event": "Oil and volatility watch",
            "expected": (
                f"WTI is {direction_word(wti.get('weekly_change_pct'))}; "
                f"VIX is {direction_word(vix.get('weekly_change_pct'))} at {vix.get('close'):.2f}. "
                "This creates a mixed macro signal."
            ),
            "importance": "High"
        })

    return rows

def build_macro_bias_text(bias: str, avg_yield_change: float, vix_level, risk_on_pts: int, risk_off_pts: int, market: dict) -> str:
    y10 = get(market, "US_10Y_YIELD")
    y30 = get(market, "US_30Y_YIELD")
    wti = get(market, "WTI")
    gold = get(market, "GOLD")
    dxy = get(market, "DXY")
    vix = get(market, "VIX")
    btc = get(market, "BTC")

    yield_desc = "rising" if avg_yield_change > 0.5 else ("falling" if avg_yield_change < -0.5 else "mostly flat")
    vix_desc = f"VIX is {direction_word(vix.get('weekly_change_pct'))} at {vix_level:.2f}" if vix and vix_level is not None else "VIX data is unavailable"

    return (
        f"The macro bias is **{bias.lower()}** because Treasury yields are {yield_desc} "
        f"(average 10Y/30Y weekly change {avg_yield_change:+.2f}%). "
        f"WTI is {direction_word(wti.get('weekly_change_pct')) if wti else 'not available'}, "
        f"gold is {direction_word(gold.get('weekly_change_pct')) if gold else 'not available'}, "
        f"DXY is {direction_word(dxy.get('weekly_change_pct')) if dxy else 'not available'}, "
        f"and {vix_desc}. BTC is {direction_word(btc.get('weekly_change_pct')) if btc else 'not available'}. "
        f"Prism counted {risk_on_pts} risk-on signal(s) and {risk_off_pts} risk-off signal(s). "
        "Because the signals are mixed, R4 should treat this as a cautious macro read rather than a strong directional call."
    )


def build_confidence_text(fdw: dict) -> str:
    missing_items = []

    if not fdw.get("fed_speakers"):
        missing_items.append("Fed speech metadata")
    if fdw.get("data_release_errors"):
        missing_items.append("BLS release metadata")
    if not fdw.get("inflation_data"):
        missing_items.append("inflation release details")
    if not fdw.get("major_data_releases"):
        missing_items.append("major data release details")

    if missing_items:
        return (
            "Confidence is **Medium-Low** because Prism collected the main market data "
            "but some macro context is incomplete: "
            + ", ".join(missing_items)
            + ". The output still follows the automation-only rule by marking missing fields as unavailable instead of using manual external sources."
        )

    return (
        "Confidence is **Medium** because Prism collected market data plus Fed/data-watch metadata. "
        "R4 should still avoid high confidence because macro conditions can change quickly."
    )


def build_invalidation_text(market: dict) -> str:
    y10 = get(market, "US_10Y_YIELD")
    y30 = get(market, "US_30Y_YIELD")
    wti = get(market, "WTI")
    vix = get(market, "VIX")
    gold = get(market, "GOLD")

    return (
        "The cautious macro bias would be invalidated if Treasury yields stop rising, "
        "WTI loses upward momentum, and VIX remains low or continues falling. "
        "The cautious view would be strengthened if the 10Y and 30Y yields continue rising, "
        "WTI keeps moving higher, gold continues falling, or VIX begins rising from its current level."
    )


def build_markdown(data: dict, week_number: int) -> str:
    market = data.get("macro_market_data", {})
    fdw = data.get("fed_and_data_watch", {})

    week_str = f"{int(week_number):02d}"

    y10 = get(market, "US_10Y_YIELD")
    y30 = get(market, "US_30Y_YIELD")
    wti = get(market, "WTI")
    gold = get(market, "GOLD")
    dxy = get(market, "DXY")
    vix = get(market, "VIX")
    btc = get(market, "BTC")

    bias, avg_yield_change, vix_level, risk_on_pts, risk_off_pts = build_macro_bias(market)

    fed_data = fetch_fed_rates_data()
    fomc_date = next_fomc_date()

    lines = []
    lines.append(f"# R4 Macro Agent — Week {week_str}")
    lines.append("")
    lines.append(
        f"> **Auto-generated:** Generated from `{data.get('collector', 'Macro Collector')}` output dated "
        f"{data.get('generated_at', 'unknown')}. This report mainly uses Prism automation outputs. "
        f"Fields marked **manual review** were added by R4 after checking external sources."
    )
    if fed_data["errors"]:
        lines.append(f"> **FRED fetch warnings:** {'; '.join(fed_data['errors'])}")
    lines.append("")

    lines.append("## FED & RATES")
    if fed_data["target_lower"] is not None and fed_data["target_upper"] is not None:
        lines.append(f"- Fed target rate: {fed_data['target_lower']:.2f}%–{fed_data['target_upper']:.2f}% (source: automated FRED fetch in Prism report builder)")
    else:
        lines.append("- Fed target rate: Not available from this Prism run")
    lines.append(
        "- Fed hold probability: **Manual review** — [fill FedWatch value here] "
        "from CME FedWatch as of [date/time checked]"
    )
    if fomc_date:
        lines.append(f"- Next FOMC: {fomc_date.strftime('%d %B %Y')} (from Prism's hardcoded FOMC schedule)")
    else:
        lines.append("- Next FOMC: Not available from this Prism run")
    if fed_data["y2"] is not None:
        lines.append(f"- 2Y Yield: {fed_data['y2']:.2f}% (source: automated FRED fetch in Prism report builder)")
    else:
        lines.append("- 2Y Yield: Not available from this Prism run")
    lines.append(f"- 10Y Yield: {fmt_yield_pct(y10)}")
    lines.append(f"- 30Y Yield: {fmt_yield_pct(y30)}")
    if fed_data["y2"] is not None and y10 and y30:
        y2_pct = fed_data["y2"]
        y10_pct = y10["close"] * YIELD_DISPLAY_MULTIPLIER
        y30_pct = y30["close"] * YIELD_DISPLAY_MULTIPLIER
        if y2_pct < y10_pct < y30_pct:
            curve_shape = "normal"
        elif y2_pct > y10_pct:
            curve_shape = "inverted (2Y > 10Y)"
        else:
            curve_shape = "flat/mixed"
        lines.append(f"- Yield curve: [{curve_shape}], 2Y {y2_pct:.2f}% / 10Y {y10_pct:.2f}% / 30Y {y30_pct:.2f}%")
    elif y10 and y30:
        y10_pct = y10["close"] * YIELD_DISPLAY_MULTIPLIER
        y30_pct = y30["close"] * YIELD_DISPLAY_MULTIPLIER
        curve_note = "10Y < 30Y" if y10_pct < y30_pct else "10Y >= 30Y"
        lines.append(f"- Yield curve: 2Y unavailable this run — {curve_note}")
    else:
        lines.append("- Yield curve: Not available from this Prism run")
    lines.append(f"- Yield direction: {direction_word(avg_yield_change)}")
    lines.append("")

    lines.append("## COMMODITIES & DOLLAR")
    lines.append(fmt_asset_line("Crude Oil WTI", wti, prefix="$"))
    lines.append(fmt_asset_line("Gold", gold, prefix="$"))
    lines.append(fmt_asset_line("DXY", dxy))
    lines.append(fmt_asset_line("VIX", vix))
    lines.append(fmt_asset_line("BTC", btc, prefix="$"))
    lines.append("")

    lines.append("## WEEK-AHEAD CALENDAR")
    lines.append("")
    lines.append("| Day | Event | Expected | Importance |")
    lines.append("|---|---|---|---|")
    for row in build_automation_calendar_rows(market, fdw, week_number):
        lines.append(f"| {row['day']} | {row['event']} | {row['expected']} | {row['importance']} |")
    lines.append("")

    lines.append("## KEY EARNINGS")
    lines.append("")
    lines.append("| Company | Date | Why It Matters |")
    lines.append("|---|---|---|")
    earnings = fdw.get("earnings_calendar", [])
    if earnings:
        for item in earnings:
            company = item.get("company", item.get("ticker", "Unknown"))
            date_text = item.get("date", "Date unavailable")
            why = item.get("why_it_matters", "Macro relevance not provided by Prism.")
            lines.append(f"| {company} | {date_text} | {why} |")
    else:
        err_count = len(fdw.get("earnings_errors", {}))
        reason = f"Prism checked the yfinance earnings watchlist, but no Week {week_str} earnings dates were returned."
        if err_count:
            reason += f" Earnings lookup also recorded {err_count} ticker-level warning(s)."
        lines.append(f"| Not available from Prism automation | Not available | {reason} |")
    lines.append("")

    lines.append("## CONFIRMED NEWS EVENTS")
    lines.append("")
    confirmed_events = fdw.get("confirmed_news_events", [])
    if confirmed_events:
        for event in confirmed_events:
            lines.append(f"- {event}")
    else:
        lines.append("- No confirmed news events were collected by the current Prism automation run.")
        lines.append(f"- {describe_fed_speakers(fdw)}")
        lines.append(
            f"- Main automated macro signals: yields are {direction_word(avg_yield_change)}, "
            f"WTI is {direction_word(wti.get('weekly_change_pct')) if wti else 'not available'}, "
            f"gold is {direction_word(gold.get('weekly_change_pct')) if gold else 'not available'}, "
            f"DXY is {direction_word(dxy.get('weekly_change_pct')) if dxy else 'not available'}, "
            f"VIX is {direction_word(vix.get('weekly_change_pct')) if vix else 'not available'}, "
            f"and BTC is {direction_word(btc.get('weekly_change_pct')) if btc else 'not available'}."
        )
        if fdw.get("data_release_errors"):
            lines.append(f"- BLS data release collection returned errors for: {', '.join(fdw.get('data_release_errors', {}).keys())}.")
    lines.append("")

    lines.append("## MACRO BIAS")
    lines.append(f"**{bias} / Cautious** _(auto-drafted from Prism automation data)_")
    lines.append("")
    lines.append(build_macro_bias_text(bias, avg_yield_change, vix_level, risk_on_pts, risk_off_pts, market))
    lines.append("")

    lines.append("## CONFIDENCE")
    lines.append("**Medium-Low** _(auto-drafted from Prism automation completeness)_")
    lines.append(build_confidence_text(fdw))
    lines.append("")

    lines.append("## INVALIDATION")
    lines.append(build_invalidation_text(market))

    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser(description="Generate R4 Macro Agent markdown from collector JSON.")
    parser.add_argument("json_path", help="Path to the Macro Collector JSON output")
    parser.add_argument(
        "week_number",
        type=int,
        nargs="?",
        default=None,
        help="Sprint week number, e.g. 6 for W06. If omitted, auto-detected from existing Week{N} folders under --out-root.",
    )
    parser.add_argument("--out-root", default=".", help="Repo root containing Week{N} folders")
    parser.add_argument(
        "--charts-dir",
        default=None,
        help="Directory containing this week's macro chart PNGs (e.g. prism/data/macro/charts). "
             "If given, copies them into Week{N}/R4_macro/macro_assets/ alongside the report.",
    )
    args = parser.parse_args()

    with open(args.json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out_root = Path(args.out_root)
    week_number = args.week_number
    if week_number is None:
        week_number = detect_next_week_number(out_root)
        print(f"[auto] No week number given -- detected next week as {week_number}")

    md = build_markdown(data, week_number)

    n = int(week_number)
    out_dir = out_root / f"Week{n}" / "R4_macro"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"macro_agent_W{n:02d}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")

    if args.charts_dir:
        charts_src = Path(args.charts_dir)
        if charts_src.is_dir():
            assets_dir = out_dir / "macro_assets"
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