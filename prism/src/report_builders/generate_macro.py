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
    lines.append(f"> **Auto-generated:** Generated from `{data.get('collector', 'Macro Collector')}` output dated {data.get('generated_at', 'unknown')}. "
                 f"Fields marked *Not automated* need to be filled in by hand -- see the script docstring for why.")
    if fed_data["errors"]:
        lines.append(f"> **FRED fetch warnings:** {'; '.join(fed_data['errors'])}")
    lines.append("")
    lines.append("## FED & RATES")
    if fed_data["target_lower"] is not None and fed_data["target_upper"] is not None:
        lines.append(f"- Fed target rate: {fed_data['target_lower']:.2f}%–{fed_data['target_upper']:.2f}% (source: FRED DFEDTARL/DFEDTARU)")
    else:
        lines.append("- Fed target rate: Not automated (FRED fetch failed this run — see warning above)")
    lines.append("- Fed hold probability: Not automated (CME FedWatch has no free public API)")
    if fomc_date:
        lines.append(f"- Next FOMC: {fomc_date.strftime('%d %B %Y')}")
    else:
        lines.append("- Next FOMC: Not automated (hardcoded calendar has no more upcoming dates — extend FOMC_DECISION_DATES)")
    if fed_data["y2"] is not None:
        lines.append(f"- 2Y Yield: {fed_data['y2']:.2f}% (source: FRED DGS2)")
    else:
        lines.append("- 2Y Yield: Not automated (FRED fetch failed this run — see warning above)")
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
        curve_note = "10Y < 30Y" if y10_pct < y30_pct else "10Y >= 30Y (inverted vs 30Y)"
        lines.append(f"- Yield curve: 2Y unavailable this run — {curve_note}")
    else:
        lines.append("- Yield curve: Not automated")
    lines.append(f"- Yield direction: {direction_word(avg_yield_change)}")
    lines.append("")
    lines.append("## COMMODITIES & DOLLAR")
    if wti:
        lines.append(f"- Crude Oil WTI: ${wti['close']:.2f}, {direction_word(wti['weekly_change_pct'])}")
    else:
        lines.append("- Crude Oil WTI: Not automated")
    if gold:
        lines.append(f"- Gold: ${gold['close']:,.2f}, {direction_word(gold['weekly_change_pct'])}")
    else:
        lines.append("- Gold: Not automated")
    if dxy:
        lines.append(f"- DXY: {dxy['close']:.2f}, {direction_word(dxy['weekly_change_pct'])}")
    else:
        lines.append("- DXY: Not automated")
    if vix:
        lines.append(f"- VIX: {vix['close']:.2f}, {direction_word(vix['weekly_change_pct'])}")
    if btc:
        lines.append(f"- BTC: ${btc['close']:,.2f}, {direction_word(btc['weekly_change_pct'])}")
    lines.append("")
    lines.append("## WEEK-AHEAD CALENDAR")
    errors = fdw.get("data_release_errors", {})
    if errors:
        lines.append(f"*Not automated — BLS RSS feeds returned errors this run ({', '.join(errors.keys())}). Fill in manually from a calendar source (e.g. Investing.com, ForexFactory).*")
    else:
        lines.append("*Not automated — no calendar data collected this run. Fill in manually.*")
    lines.append("")
    lines.append("| Day | Event | Expected | Importance |")
    lines.append("|---|---|---|---|")
    lines.append("| _fill manually_ | | | |")
    lines.append("")
    lines.append("## KEY EARNINGS")
    lines.append("*Not automated — no earnings calendar collected. Fill in manually.*")
    lines.append("")
    lines.append("| Company | Date | Why It Matters |")
    lines.append("|---|---|---|")
    lines.append("| _fill manually_ | | |")
    lines.append("")
    lines.append("## CONFIRMED NEWS EVENTS")
    lines.append("*Not automated — no news collection wired up yet. Fill in manually.*")
    lines.append("")
    lines.append("## MACRO BIAS")
    lines.append(f"**{bias}** _(auto-drafted from yields/VIX/oil/gold/DXY only -- no Fed, calendar, or news signal was available; review and rewrite once those sections are filled in)_")
    lines.append("")
    yield_desc = "falling" if avg_yield_change < -0.5 else ("rising" if avg_yield_change > 0.5 else "roughly flat")
    vix_desc = f"VIX at {vix_level:.1f}" if vix_level is not None else "VIX data unavailable"
    lines.append(f"Yields are {yield_desc} on the week (avg {avg_yield_change:+.2f}%), with {vix_desc}. "
                 f"Oil, gold, and dollar moves were weighed alongside these to produce a rough {bias.lower()} lean "
                 f"({risk_on_pts} risk-on signal(s) vs {risk_off_pts} risk-off signal(s)). "
                 f"This draft does NOT reflect any Fed policy stance, scheduled data releases, earnings, or news events, "
                 f"since none of those are currently automated -- update this paragraph once those sections are filled in.")
    lines.append("")
    lines.append("## CONFIDENCE")
    lines.append("**Low** _(auto-drafted)_")
    lines.append("This confidence is capped at Low because Fed hold probability, the Week-Ahead Calendar, Key Earnings, and Confirmed News "
                 "Events sections are still not automated (Fed target rate, 2Y yield, and next FOMC date now are). "
                 "Once the remaining sections are completed by hand, confidence should be reassessed.")
    lines.append("")
    lines.append("## INVALIDATION")
    lines.append("_Not automated — write this once the Fed/Rates, calendar, and news sections above are filled in by hand, "
                 "since invalidation conditions depend on those events._")

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


if __name__ == "__main__":
    main()