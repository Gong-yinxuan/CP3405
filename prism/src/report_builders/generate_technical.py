#!/usr/bin/env python3
"""
generate_technical.py

Auto-fills the R5 Technical Agent markdown report from the Technical
Collector's JSON output, and writes it to Week{N}/R5_technical/technical_agent_W{NN}.md.

Usage:
    python generate_technical.py <collector_json_path> [week_number] [--out-root OUTPUT_ROOT]

Example:
    python generate_technical.py technical_collector_output.json 6
    -> creates ./Week6/R5_technical/technical_agent_W06.md

If week_number is omitted, it is auto-detected the same way as the other
report builders: highest existing Week{N} folder + 1.

------------------------------------------------------------------------
IMPORTANT -- what this script CAN and CANNOT auto-fill
------------------------------------------------------------------------
The technical_collector.py output is fairly rich -- EMA levels/conditions,
price position vs EMAs, and one resistance/support candidate per
instrument are all computed automatically. But per the collector's own
"note" field, manual chart trendlines and annotated screenshots are
NOT automated.

Auto-filled from JSON:
    - LAST CLOSE + weekly change
    - 8 EMA vs PRICE, 8 EMA vs 21 EMA, EMA condition zone
    - Resistance 1 / Support 1 (from the 20-day high/low candidates)
    - TECHNICAL BIAS (collector already classifies this)
    - A rule-based CONFIDENCE + INVALIDATION + WATCH THIS WEEK draft

NOT auto-filled (left as explicit placeholders):
    - TRENDLINE section (needs a human to draw trendlines off a chart)
    - Resistance 2 / Support 2 (collector only gives one candidate level
      each; a second level needs a longer lookback / manual chart read)
    - BREADTH NOTE (% of S&P 500 above 200-day MA, Russell vs SPX/NDX
      leadership commentary -- not collected by any current script)
    - Annotated chart screenshots (chart_builder.py produces plain price
      history charts, not annotated trendline/level screenshots)
"""

import json
import re
import argparse
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INSTRUMENT_ORDER = ["SPX", "NDX", "IWM"]
INSTRUMENT_LABELS = {
    "SPX": "S&P 500 (SPX)",
    "NDX": "NASDAQ 100 (NDX)",
    "IWM": "Russell 2000 (IWM)",
}


import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from week_utils import detect_next_week_number  # noqa: E402


def fmt_price(v: float) -> str:
    return f"{v:,.2f}"


def confidence_from_alignment(inst: dict) -> tuple:
    """Rough rule: bias is stronger/higher-confidence when price is above
    both EMAs and the EMAs themselves are stacked in the same direction as
    the bias. Disagreement between price/EMA position and the stated bias
    lowers confidence."""
    bias = inst["technical_bias"]
    price_above_8 = inst["price_vs_8ema"] == "above"
    ema8_above_21 = inst["ema_8_vs_21ema"] == "above"

    if bias == "Bullish":
        aligned = price_above_8 and ema8_above_21
    elif bias == "Bearish":
        aligned = (not price_above_8) and (not ema8_above_21)
    else:
        aligned = price_above_8 == ema8_above_21  # both agree, even if bias is neutral

    if aligned:
        confidence = "Medium-High"
        reason = "Price position and EMA stack both agree with the stated bias."
    else:
        confidence = "Medium-Low"
        reason = "Price position and/or EMA stack diverge from the stated bias, so treat this as a lower-conviction read."
    return confidence, reason


def build_instrument_block(symbol: str, inst: dict, latest_date: str) -> list:
    lines = []
    label = INSTRUMENT_LABELS.get(symbol, symbol)

    lines.append(f"**INSTRUMENT**: {label}, Daily Chart <br>")
    date_fmt = datetime.strptime(latest_date, "%Y-%m-%d").strftime("%d %b %Y")
    lines.append(f"**LAST CLOSE**: {fmt_price(inst['last_close'])} (Fri {date_fmt}), weekly change {inst['weekly_change_pct']:+.2f}%")
    lines.append("")
    lines.append("## 8 EMA vs PRICE:")
    lines.append("")
    price_pos = inst["price_vs_8ema"]
    momentum_word = "intact" if price_pos == "above" else "weakening"
    lines.append(f"* Price is [{price_pos.upper()}] the 8 EMA. Short-term momentum [{momentum_word}].")
    lines.append(f"* 8 EMA estimated at ~{fmt_price(inst['ema_8'])}. Price is ~{abs(inst['distance_from_8ema']):.1f} points [{price_pos}] it.")
    lines.append("")
    lines.append("## 8 EMA vs 21 EMA:")
    lines.append("")
    ema_pos = inst["ema_8_vs_21ema"]
    trend_word = "bullish" if ema_pos == "above" else "bearish"
    lines.append(f"* 8 EMA is [{ema_pos.upper()}] 21 EMA. Trend structure [{trend_word}].")
    compressing = "compressing" if inst["ema_gap"] < abs(inst["distance_from_21ema"]) * 0.5 else "not compressing"
    lines.append(f"* 21 EMA estimated at ~{fmt_price(inst['ema_21'])}. Gap between 8 and 21 EMA = ~{inst['ema_gap']:.1f} pts, [{compressing}].")
    lines.append(f"* EMA condition: [{inst['ema_condition']}]")
    lines.append("")
    lines.append("## TRENDLINE:")
    lines.append("")
    lines.append("* Not automated — collector does not draw chart trendlines. Fill in manually from the chart:")
    lines.append("  * Trendline drawn from [month] lows, connecting lows at ~[level], ~[level], ~[level].")
    lines.append("  * Current trendline support: approximately [range] on the coming week.")
    lines.append("  * Price is [above/below] the trendline. [break status].")
    lines.append("")
    lines.append("## KEY LEVELS:")
    lines.append("")
    lines.append(f"* Resistance 1: {fmt_price(inst['resistance_candidate'])} (20-day high)")
    lines.append("* Resistance 2: Not automated — fill in manually")
    lines.append(f"* Support 1: {fmt_price(inst['support_candidate'])} (20-day low) ← KEY LEVEL")
    lines.append("* Support 2: Not automated — fill in manually")
    lines.append("")
    lines.append("## BREADTH NOTE:")
    lines.append("")
    lines.append("* Not automated — % of S&P 500 above 200-day MA and Russell vs SPX/NDX leadership commentary are not collected. Fill in manually.")
    lines.append("")

    bias = inst["technical_bias"]
    confidence, reason = confidence_from_alignment(inst)
    lines.append(f"**TECHNICAL BIAS**: {bias}<br>")
    lines.append(f"**CONFIDENCE**: {confidence} _(auto-drafted)_. {reason}<br>")
    support = inst["support_candidate"]
    resistance = inst["resistance_candidate"]
    opposite_bias = "Bearish" if bias != "Bearish" else "Bullish"
    lines.append(f"**INVALIDATION**: Close below {fmt_price(support)} = loss of key support. Would shift bias toward {opposite_bias}. "
                 f"(Auto-drafted from the support candidate only — refine once TRENDLINE and Support 2 are filled in.)<br>")
    lines.append(f"**WATCH THIS WEEK**: Whether {symbol} can hold above {fmt_price(support)} and whether it can challenge "
                 f"resistance near {fmt_price(resistance)}. _(auto-drafted)_<br>")
    lines.append("")
    lines.append("---")
    lines.append("")
    return lines


def build_markdown(data: dict, week_number: int) -> str:
    instruments = data.get("instruments", {})

    # Use the latest_trading_date from whichever instrument has it, for the header
    any_inst = next(iter(instruments.values()), {})
    latest_date = any_inst.get("latest_trading_date", datetime.now().strftime("%Y-%m-%d"))
    date_fmt = datetime.strptime(latest_date, "%Y-%m-%d").strftime("%d %b %Y")

    lines = []
    lines.append(f"# Technical Agent Output — Week of {date_fmt}")
    lines.append("")
    lines.append(f"> **Auto-generated:** Generated from `{data.get('collector', 'Technical Collector')}` output dated {data.get('generated_at', 'unknown')}. "
                 f"Sections marked *Not automated* need to be filled in by hand -- see the script docstring for why.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for symbol in INSTRUMENT_ORDER:
        inst = instruments.get(symbol)
        if not inst:
            continue
        lines.extend(build_instrument_block(symbol, inst, inst.get("latest_trading_date", latest_date)))

    lines.append("Charts (not annotated with trendlines/levels — add those manually if needed):")
    for symbol in INSTRUMENT_ORDER:
        if symbol in instruments:
            lines.append(f"`prism/data/technical/charts/technical_{symbol}_history.png`")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate R5 Technical Agent markdown from collector JSON.")
    parser.add_argument("json_path", help="Path to the Technical Collector JSON output")
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
    out_dir = out_root / f"Week{n}" / "R5_technical"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"technical_agent_W{n:02d}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()