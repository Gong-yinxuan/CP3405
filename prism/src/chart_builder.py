"""
Prism Chart Builder — W5

Reads collector JSON outputs and generates PNG charts for each agent.

Outputs:
- prism/data/technical/charts/
- prism/data/macro/charts/
- prism/data/almanac/charts/
"""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


# -----------------------------
# Common helpers
# -----------------------------

def get_project_root() -> Path:
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if parent.name == "prism":
            return parent

    raise FileNotFoundError("Could not find prism folder.")


def load_json(path: Path):
    if not path.exists():
        print(f"[WARN] Missing file, skipping: {path}")
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_valid_number(value) -> bool:
    try:
        number = float(value)
        return math.isfinite(number)
    except Exception:
        return False


def save_chart(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[OK] Saved chart: {path}")


def hide_extra_x_labels(dates: list[str]) -> None:
    ax = plt.gca()
    every_nth = max(1, len(dates) // 8)

    for index, label in enumerate(ax.get_xticklabels()):
        if index % every_nth != 0:
            label.set_visible(False)


# -----------------------------
# Technical charts
# -----------------------------

def build_technical_weekly_change_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "technical" / "technical_collector_output.json"
    output_path = project_root / "data" / "technical" / "charts" / "technical_weekly_change.png"

    data = load_json(input_path)
    if data is None:
        return

    instruments = data.get("instruments", {})

    rows = []

    for symbol, item in instruments.items():
        change = item.get("weekly_change_pct")

        if is_valid_number(change):
            rows.append({
                "symbol": symbol,
                "weekly_change_pct": float(change)
            })

    if not rows:
        print("[WARN] No technical weekly change data found.")
        return

    labels = [row["symbol"] for row in rows]
    values = [row["weekly_change_pct"] for row in rows]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.axhline(0, linewidth=1)
    plt.title("Technical Agent: Weekly Change")
    plt.xlabel("Instrument")
    plt.ylabel("Weekly change (%)")

    for index, value in enumerate(values):
        plt.text(index, value, f"{value:+.1f}%", ha="center", va="bottom")

    save_chart(output_path)


def build_technical_history_chart(project_root: Path, symbol: str) -> None:
    history_path = project_root / "data" / "technical" / "history" / f"{symbol}.json"
    technical_path = project_root / "data" / "technical" / "technical_collector_output.json"
    output_path = project_root / "data" / "technical" / "charts" / f"technical_{symbol}_history.png"

    history_data = load_json(history_path)
    technical_data = load_json(technical_path)

    if history_data is None or technical_data is None:
        return

    if isinstance(history_data, dict):
        history_rows = history_data.get("history", [])
    else:
        history_rows = history_data

    history_rows = history_rows[-60:]

    dates = []
    closes = []

    for row in history_rows:
        close = row.get("close")

        if is_valid_number(close):
            dates.append(row.get("date"))
            closes.append(float(close))

    if not closes:
        print(f"[WARN] No valid close data for {symbol}.")
        return

    instrument_data = technical_data.get("instruments", {}).get(symbol, {})

    plt.figure(figsize=(11, 5))
    plt.plot(dates, closes, label="Close")

    ema_8 = instrument_data.get("ema_8")
    ema_21 = instrument_data.get("ema_21")

    if is_valid_number(ema_8):
        plt.axhline(float(ema_8), linestyle="--", label="8 EMA")

    if is_valid_number(ema_21):
        plt.axhline(float(ema_21), linestyle="--", label="21 EMA")

    support = (
        instrument_data.get("support_candidate")
        or instrument_data.get("support")
        or instrument_data.get("recent_low")
    )

    resistance = (
        instrument_data.get("resistance_candidate")
        or instrument_data.get("resistance")
        or instrument_data.get("recent_high")
    )

    if is_valid_number(support):
        plt.axhline(float(support), linestyle=":", label="Support candidate")

    if is_valid_number(resistance):
        plt.axhline(float(resistance), linestyle=":", label="Resistance candidate")

    plt.title(f"Technical Agent: {symbol} Price Evidence")
    plt.xlabel("Date")
    plt.ylabel("Close")
    plt.xticks(rotation=45)
    plt.legend()

    hide_extra_x_labels(dates)
    save_chart(output_path)


# -----------------------------
# Macro charts
# -----------------------------

def build_macro_weekly_change_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "macro" / "macro_collector_output.json"
    output_path = project_root / "data" / "macro" / "charts" / "macro_weekly_change.png"

    data = load_json(input_path)
    if data is None:
        return

    macro_data = data.get("macro_market_data", {})

    rows = []

    for symbol, item in macro_data.items():
        change = item.get("weekly_change_pct")

        if is_valid_number(change):
            rows.append({
                "symbol": symbol,
                "weekly_change_pct": float(change)
            })

    if not rows:
        print("[WARN] No macro weekly change data found.")
        return

    rows.sort(key=lambda row: row["weekly_change_pct"])

    labels = [row["symbol"] for row in rows]
    values = [row["weekly_change_pct"] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values)
    plt.axvline(0, linewidth=1)
    plt.title("Macro Agent: Weekly Change")
    plt.xlabel("Weekly change (%)")
    plt.ylabel("Macro asset")

    for index, value in enumerate(values):
        plt.text(value, index, f"{value:+.1f}%", va="center")

    save_chart(output_path)


def build_macro_5d_change_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "macro" / "macro_collector_output.json"
    output_path = project_root / "data" / "macro" / "charts" / "macro_5d_change.png"

    data = load_json(input_path)
    if data is None:
        return

    macro_data = data.get("macro_market_data", {})

    rows = []

    for symbol, item in macro_data.items():
        change = item.get("change_5d")

        if is_valid_number(change):
            rows.append({
                "symbol": symbol,
                "change_5d": float(change)
            })

    if not rows:
        print("[WARN] No macro 5D change data found.")
        return

    rows.sort(key=lambda row: row["change_5d"])

    labels = [row["symbol"] for row in rows]
    values = [row["change_5d"] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values)
    plt.axvline(0, linewidth=1)
    plt.title("Macro Agent: 5-Day Absolute Change")
    plt.xlabel("5-day change")
    plt.ylabel("Macro asset")

    for index, value in enumerate(values):
        plt.text(value, index, f"{value:+.2f}", va="center")

    save_chart(output_path)


def build_macro_yield_chart(project_root: Path) -> None:
    output_path = project_root / "data" / "macro" / "charts" / "macro_yields_history.png"

    yield_symbols = [
        "US_10Y_YIELD",
        "US_30Y_YIELD"
    ]

    plt.figure(figsize=(11, 5))

    plotted = False
    dates_for_labels = []

    for symbol in yield_symbols:
        history_path = project_root / "data" / "macro" / "history" / f"{symbol}.json"
        history = load_json(history_path)

        if history is None:
            continue

        dates = []
        values = []

        for row in history[-60:]:
            close = row.get("close")

            if is_valid_number(close):
                dates.append(row.get("date"))
                values.append(float(close))

        if values:
            plt.plot(dates, values, label=symbol)
            dates_for_labels = dates
            plotted = True

    if not plotted:
        print("[WARN] No yield history data found.")
        plt.close()
        return

    plt.title("Macro Agent: Treasury Yield History")
    plt.xlabel("Date")
    plt.ylabel("Yield (%)")
    plt.xticks(rotation=45)
    plt.legend()

    hide_extra_x_labels(dates_for_labels)
    save_chart(output_path)


def build_macro_fed_data_watch_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "macro" / "macro_collector_output.json"
    output_path = project_root / "data" / "macro" / "charts" / "macro_fed_data_watch.png"

    data = load_json(input_path)
    if data is None:
        return

    watch = data.get("fed_and_data_watch", {})

    rows = [
        {
            "label": "Fed Events",
            "count": len(watch.get("fed_events", []))
        },
        {
            "label": "Fed Speakers",
            "count": len(watch.get("fed_speakers", []))
        },
        {
            "label": "Inflation Data",
            "count": len(watch.get("inflation_data", []))
        },
        {
            "label": "Major Releases",
            "count": len(watch.get("major_data_releases", []))
        }
    ]

    labels = [row["label"] for row in rows]
    values = [row["count"] for row in rows]

    plt.figure(figsize=(9, 5))
    plt.bar(labels, values)
    plt.title("Macro Agent: Fed + Data Watch")
    plt.xlabel("Event type")
    plt.ylabel("Number of events")

    for index, value in enumerate(values):
        plt.text(index, value + 0.05, str(value), ha="center")

    plt.xticks(rotation=20, ha="right")
    save_chart(output_path)


def build_macro_relevance_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "macro" / "macro_collector_output.json"
    output_path = project_root / "data" / "macro" / "charts" / "macro_relevance_summary.png"

    data = load_json(input_path)
    if data is None:
        return

    watch = data.get("fed_and_data_watch", {})

    relevance_counts = {
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Unknown": 0
    }

    event_groups = [
        watch.get("fed_events", []),
        watch.get("fed_speakers", []),
        watch.get("inflation_data", []),
        watch.get("major_data_releases", [])
    ]

    for group in event_groups:
        for item in group:
            relevance = item.get("macro_relevance", "Unknown")

            if relevance not in relevance_counts:
                relevance = "Unknown"

            relevance_counts[relevance] += 1

    labels = list(relevance_counts.keys())
    values = list(relevance_counts.values())

    if sum(values) == 0:
        print("[WARN] No macro relevance data found.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title("Macro Agent: Event Macro Relevance")
    plt.xlabel("Macro relevance")
    plt.ylabel("Number of events")

    for index, value in enumerate(values):
        plt.text(index, value + 0.05, str(value), ha="center")

    save_chart(output_path)


# -----------------------------
# Almanac charts
# -----------------------------

def build_almanac_sector_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "almanac" / "almanac_collector_output.json"
    output_path = project_root / "data" / "almanac" / "charts" / "almanac_sector_ranking.png"

    data = load_json(input_path)
    if data is None:
        return

    sectors = (
        data.get("sector_weekly_performance")
        or data.get("sectors")
        or {}
    )

    rows = []

    for ticker, item in sectors.items():
        change = item.get("weekly_change_pct")

        if is_valid_number(change):
            sector_name = item.get("sector") or item.get("name") or ""
            label = ticker

            if sector_name:
                label = f"{ticker} ({sector_name})"

            rows.append({
                "label": label,
                "weekly_change_pct": float(change)
            })

    if not rows:
        print("[WARN] No almanac sector data found.")
        return

    rows.sort(key=lambda row: row["weekly_change_pct"])

    labels = [row["label"] for row in rows]
    values = [row["weekly_change_pct"] for row in rows]

    plt.figure(figsize=(11, 7))
    plt.barh(labels, values)
    plt.axvline(0, linewidth=1)
    plt.title("Almanac Agent: Sector Weekly Ranking")
    plt.xlabel("Weekly change (%)")
    plt.ylabel("Sector ETF")

    for index, value in enumerate(values):
        plt.text(value, index, f"{value:+.1f}%", va="center")

    save_chart(output_path)


def build_almanac_calendar_flags_chart(project_root: Path) -> None:
    input_path = project_root / "data" / "almanac" / "almanac_collector_output.json"
    output_path = project_root / "data" / "almanac" / "charts" / "almanac_calendar_flags.png"

    data = load_json(input_path)
    if data is None:
        return

    flags = (
        data.get("seasonal_calendar_flags")
        or data.get("calendar_flags")
        or {}
    )

    rows = []

    for flag_name, flag_value in flags.items():
        if isinstance(flag_value, bool):
            rows.append({
                "flag": flag_name.replace("_", " ").title(),
                "active": 1 if flag_value else 0
            })

    if not rows:
        print("[WARN] No calendar flags found.")
        return

    labels = [row["flag"] for row in rows]
    values = [row["active"] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.ylim(0, 1.2)
    plt.title("Almanac Agent: Seasonal Calendar Flags")
    plt.xlabel("Calendar flag")
    plt.ylabel("Active")

    for index, value in enumerate(values):
        label = "Yes" if value == 1 else "No"
        plt.text(index, value + 0.05, label, ha="center")

    plt.xticks(rotation=30, ha="right")
    save_chart(output_path)


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    project_root = get_project_root()

    print("Building Prism agent charts...")

    # Technical Agent
    build_technical_weekly_change_chart(project_root)

    for symbol in ["SPX", "NDX", "IWM"]:
        build_technical_history_chart(project_root, symbol)

    # Macro Agent
    build_macro_weekly_change_chart(project_root)
    build_macro_5d_change_chart(project_root)
    build_macro_yield_chart(project_root)
    build_macro_fed_data_watch_chart(project_root)
    build_macro_relevance_chart(project_root)

    # Almanac Agent
    build_almanac_sector_chart(project_root)
    build_almanac_calendar_flags_chart(project_root)

    print("Chart generation complete.")


if __name__ == "__main__":
    main()