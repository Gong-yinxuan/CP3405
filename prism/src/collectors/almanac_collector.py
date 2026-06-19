"""
Prism Almanac Data Collector — W5

Collects automatic calendar/seasonality flags and sector ranking.

Output:
- prism/data/almanac/almanac_input.json
- prism/data/almanac/sector_history/*.json

No config file.
No manual calendar/news interpretation.
"""

import json
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

import yfinance as yf


SECTOR_TICKERS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLB": "Materials",
    "XLI": "Industrials",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLU": "Utilities",
    "XLC": "Communication Services",
    "XLRE": "Real Estate"
}


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_json(data: dict | list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"[OK] Saved {path}")


def fetch_history(ticker: str, period: str = "1mo") -> list[dict]:
    asset = yf.Ticker(ticker)
    hist = asset.history(period=period, interval="1d")

    if hist.empty:
        raise ValueError(f"No data returned for {ticker}")

    records = []

    for date_index, row in hist.iterrows():
        records.append({
            "date": date_index.strftime("%Y-%m-%d"),
            "close": round(float(row["Close"]), 4)
        })

    return records


def calculate_weekly_change(history: list[dict]) -> float | None:
    if len(history) < 6:
        return None

    latest_close = history[-1]["close"]
    previous_close = history[-6]["close"]

    if previous_close == 0:
        return None

    return round(((latest_close - previous_close) / previous_close) * 100, 2)


def next_monday_after(today: date) -> date:
    days_ahead = (7 - today.weekday()) % 7

    if days_ahead == 0:
        days_ahead = 7

    return today + timedelta(days=days_ahead)


def third_friday(year: int, month: int) -> date:
    current = date(year, month, 1)
    fridays = []

    while current.month == month:
        if current.weekday() == 4:
            fridays.append(current)

        current += timedelta(days=1)

    return fridays[2]


def observed_holiday(holiday: date) -> date:
    if holiday.weekday() == 5:
        return holiday - timedelta(days=1)

    if holiday.weekday() == 6:
        return holiday + timedelta(days=1)

    return holiday


def us_market_holidays_for_year(year: int) -> list[dict]:
    holidays = [
        {
            "name": "New Year's Day",
            "date": observed_holiday(date(year, 1, 1))
        },
        {
            "name": "Juneteenth",
            "date": observed_holiday(date(year, 6, 19))
        },
        {
            "name": "Independence Day",
            "date": observed_holiday(date(year, 7, 4))
        },
        {
            "name": "Christmas Day",
            "date": observed_holiday(date(year, 12, 25))
        }
    ]

    return holidays


def is_in_window(target: date, start: date, end: date) -> bool:
    return start <= target <= end


def is_midterm_year(year: int) -> bool:
    """
    2026 is a US midterm year after the 2024 presidential election.
    """
    return (year - 2024) % 4 == 2


def build_forecast_window() -> dict:
    today = datetime.now(timezone.utc).date()
    start = next_monday_after(today)
    end = start + timedelta(days=4)

    return {
        "generated_from_date_utc": today.strftime("%Y-%m-%d"),
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d")
    }


def fetch_sector_data(project_root: Path) -> dict:
    sectors = {}

    print("Fetching sector data...")

    for ticker, sector_name in SECTOR_TICKERS.items():
        try:
            history = fetch_history(ticker, period="1mo")

            history_path = (
                project_root
                / "data"
                / "almanac"
                / "sector_history"
                / f"{ticker}.json"
            )

            save_json(history, history_path)

            latest = history[-1]
            weekly_change = calculate_weekly_change(history)

            sectors[ticker] = {
                "ticker": ticker,
                "sector": sector_name,
                "latest_trading_date": latest["date"],
                "close": latest["close"],
                "weekly_change_pct": weekly_change,
                "history_file": f"almanac/sector_history/{ticker}.json"
            }

            print(f"[OK] Sector {ticker}: {weekly_change}%")

        except Exception as error:
            sectors[ticker] = {
                "ticker": ticker,
                "sector": sector_name,
                "error": str(error)
            }

            print(f"[ERROR] Failed to collect {ticker}: {error}")

    return sectors


def rank_sectors(sectors: dict) -> dict:
    valid = []

    for ticker, data in sectors.items():
        change = data.get("weekly_change_pct")

        if isinstance(change, (int, float)):
            valid.append({
                "ticker": ticker,
                "sector": data["sector"],
                "weekly_change_pct": change
            })

    sorted_sectors = sorted(
        valid,
        key=lambda item: item["weekly_change_pct"],
        reverse=True
    )

    return {
        "leading_sectors": sorted_sectors[:3],
        "lagging_sectors": sorted_sectors[-3:][::-1]
    }


def build_calendar_flags(forecast_window: dict) -> dict:
    start = datetime.strptime(forecast_window["start"], "%Y-%m-%d").date()
    end = datetime.strptime(forecast_window["end"], "%Y-%m-%d").date()

    expiry = third_friday(start.year, start.month)

    holidays = us_market_holidays_for_year(start.year)

    holidays_in_window = [
        {
            "name": item["name"],
            "date": item["date"].strftime("%Y-%m-%d")
        }
        for item in holidays
        if is_in_window(item["date"], start, end)
    ]

    return {
        "month": start.strftime("%B"),
        "june_seasonal_weakness_flag": start.month == 6 or end.month == 6,
        "midterm_year_flag": is_midterm_year(start.year),
        "options_expiry_date": expiry.strftime("%Y-%m-%d"),
        "options_expiry_week_flag": is_in_window(expiry, start, end),
        "market_holiday_in_window_flag": len(holidays_in_window) > 0,
        "compressed_trading_week_flag": len(holidays_in_window) > 0,
        "holidays_in_window": holidays_in_window
    }


def main() -> None:
    project_root = get_project_root()

    forecast_window = build_forecast_window()
    sectors = fetch_sector_data(project_root)
    sector_ranking = rank_sectors(sectors)
    calendar_flags = build_calendar_flags(forecast_window)

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collector": "Almanac Collector",
        "agent_input_for": "Almanac Agent",
        "data_source": "Yahoo Finance via yfinance + automatic date rules",
        "note": (
            "This collector automates calendar flags and sector ranking. "
            "It does not manually interpret seasonal patterns or news."
        ),
        "forecast_window": forecast_window,
        "calendar_flags": calendar_flags,
        "sector_weekly_performance": sectors,
        "sector_ranking": sector_ranking
    }

    output_path = project_root / "data" / "almanac" / "almanac_collector_output.json"
    save_json(output, output_path)

    print("Almanac collection complete.")


if __name__ == "__main__":
    main()