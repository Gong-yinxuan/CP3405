"""
Prism Technical Data Collector — W5

Collects historical price data and calculates technical inputs for:
- SPX
- NDX
- IWM

Output:
- prism/data/technical/technical_input.json
- prism/data/technical/history/SPX.json
- prism/data/technical/history/NDX.json
- prism/data/technical/history/IWM.json
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf


TECHNICAL_TICKERS = {
    "SPX": {
        "ticker": "^GSPC",
        "name": "S&P 500 Index"
    },
    "NDX": {
        "ticker": "^NDX",
        "name": "Nasdaq 100 Index"
    },
    "IWM": {
        "ticker": "IWM",
        "name": "Russell 2000 ETF Proxy"
    }
}


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_json(data: dict | list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"[OK] Saved {path}")


def fetch_history(ticker: str, period: str = "6mo") -> list[dict]:
    asset = yf.Ticker(ticker)
    hist = asset.history(period=period, interval="1d")

    if hist.empty:
        raise ValueError(f"No data returned for {ticker}")

    records = []

    for date_index, row in hist.iterrows():
        volume = row.get("Volume", 0)

        try:
            volume = int(volume)
        except Exception:
            volume = 0

        records.append({
            "date": date_index.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": volume
        })

    return records


def calculate_ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)
    ema = sum(values[:period]) / period

    for price in values[period:]:
        ema = (price - ema) * multiplier + ema

    return round(ema, 2)


def calculate_weekly_change(history: list[dict]) -> float | None:
    if len(history) < 6:
        return None

    latest_close = history[-1]["close"]
    previous_close = history[-6]["close"]

    if previous_close == 0:
        return None

    return round(((latest_close - previous_close) / previous_close) * 100, 2)


def compare(first: float, second: float) -> str:
    if first > second:
        return "above"
    if first < second:
        return "below"
    return "equal"


def classify_ema_condition(close: float, ema_8: float, ema_21: float) -> str:
    if close > ema_8 and ema_8 > ema_21:
        return "Zone 1 Bullish"

    if close < ema_8 and ema_8 > ema_21:
        return "Zone 2 Pullback"

    if close < ema_8 and ema_8 < ema_21:
        return "Zone 3 Bearish"

    return "Mixed / Neutral"


def classify_bias(ema_condition: str, weekly_change: float | None) -> str:
    if ema_condition == "Zone 1 Bullish" and weekly_change is not None and weekly_change > 0:
        return "Bullish"

    if ema_condition == "Zone 3 Bearish" and weekly_change is not None and weekly_change < 0:
        return "Bearish"

    return "Neutral"


def build_record(symbol: str, info: dict, history: list[dict]) -> dict:
    closes = [day["close"] for day in history]

    latest = history[-1]
    close = latest["close"]

    ema_8 = calculate_ema(closes, 8)
    ema_21 = calculate_ema(closes, 21)
    weekly_change = calculate_weekly_change(history)

    recent_20_days = history[-20:]
    recent_high = max(day["high"] for day in recent_20_days)
    recent_low = min(day["low"] for day in recent_20_days)

    if ema_8 is not None and ema_21 is not None:
        ema_condition = classify_ema_condition(close, ema_8, ema_21)
        price_vs_8ema = compare(close, ema_8)
        ema_8_vs_21ema = compare(ema_8, ema_21)
        distance_from_8ema = round(close - ema_8, 2)
        distance_from_21ema = round(close - ema_21, 2)
        ema_gap = round(ema_8 - ema_21, 2)
        bias = classify_bias(ema_condition, weekly_change)
    else:
        ema_condition = "Insufficient data"
        price_vs_8ema = "unknown"
        ema_8_vs_21ema = "unknown"
        distance_from_8ema = None
        distance_from_21ema = None
        ema_gap = None
        bias = "Unknown"

    return {
        "symbol": symbol,
        "yahoo_ticker": info["ticker"],
        "name": info["name"],
        "latest_trading_date": latest["date"],
        "last_close": close,
        "weekly_change_pct": weekly_change,
        "ema_8": ema_8,
        "ema_21": ema_21,
        "price_vs_8ema": price_vs_8ema,
        "ema_8_vs_21ema": ema_8_vs_21ema,
        "distance_from_8ema": distance_from_8ema,
        "distance_from_21ema": distance_from_21ema,
        "ema_gap": ema_gap,
        "ema_condition": ema_condition,
        "recent_20d_high": round(recent_high, 2),
        "recent_20d_low": round(recent_low, 2),
        "resistance_candidate": round(recent_high, 2),
        "support_candidate": round(recent_low, 2),
        "technical_bias": bias,
        "history_file": f"technical/history/{symbol}.json"
    }


def main() -> None:
    project_root = get_project_root()

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collector": "Technical Collector",
        "agent_input_for": "Technical Agent",
        "data_source": "Yahoo Finance via yfinance",
        "note": (
            "This collector automates EMA, momentum, and support/resistance candidate data. "
            "Manual chart trendlines and annotated screenshots are not automated yet."
        ),
        "instruments": {}
    }

    print("Fetching technical data...")

    for symbol, info in TECHNICAL_TICKERS.items():
        try:
            history = fetch_history(info["ticker"], period="6mo")

            history_path = (
                project_root
                / "data"
                / "technical"
                / "history"
                / f"{symbol}.json"
            )

            save_json(history, history_path)

            output["instruments"][symbol] = build_record(symbol, info, history)

            print(f"[OK] Technical data collected for {symbol}")

        except Exception as error:
            output["instruments"][symbol] = {
                "symbol": symbol,
                "yahoo_ticker": info["ticker"],
                "name": info["name"],
                "error": str(error)
            }

            print(f"[ERROR] Failed to collect {symbol}: {error}")

    output_path = project_root / "data" / "technical" / "technical_collector_output.json"
    save_json(output, output_path)

    print("Technical collection complete.")


if __name__ == "__main__":
    main()