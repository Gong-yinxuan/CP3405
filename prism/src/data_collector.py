"""
Market Data Pipeline - Level 2 → 3
Fetches closing prices + weekly change % from Yahoo Finance
for SPY, QQQ, IWM, XLK, XLU, XLV and saves to data/output.json
"""

import json
from pathlib import Path
from datetime import datetime

import yfinance as yf


TICKERS = {
    # Prediction assets
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "IWM": "IWM",
    "GOLD": "GC=F",
    "WTI": "CL=F",
    "US10Y": "^TNX",
    "TLT": "TLT",
    "VIX": "^VIX",
    "BTC": "BTC-USD",

    # All 11 S&P sector ETFs
    "XLK": "XLK",    # Technology
    "XLF": "XLF",    # Financials
    "XLV": "XLV",    # Healthcare
    "XLE": "XLE",    # Energy
    "XLY": "XLY",    # Consumer Discretionary
    "XLP": "XLP",    # Consumer Staples
    "XLI": "XLI",    # Industrials
    "XLU": "XLU",    # Utilities
    "XLB": "XLB",    # Materials
    "XLRE": "XLRE",  # Real Estate
    "XLC": "XLC"     # Communication Services
}

def fetch_prices() -> dict:
    """
    Fetch close price and weekly change % for all tickers.
    Uses 10 days of history so there are always enough points
    to calculate a 5-trading-day (≈ 1 week) return.
    """
    prices = {}

    for ticker, yahoo_ticker in TICKERS.items():
        data = yf.Ticker(yahoo_ticker)
        hist = data.history(period="10d")

        if len(hist) < 2:
            raise ValueError(f"Not enough data returned for {ticker}")

        latest_close   = round(float(hist["Close"].iloc[-1]), 2)
        # go back 5 trading days (or as far as available)
        lookback       = min(5, len(hist) - 1)
        prev_close     = round(float(hist["Close"].iloc[-1 - lookback]), 2)
        if ticker == "US10Y":
            latest_close = round(latest_close / 10, 2)
            prev_close = round(prev_close / 10, 2)
        weekly_change  = round(((latest_close - prev_close) / prev_close) * 100, 1)

        prices[ticker] = {
            "close": latest_close,
            "weekly_change_pct": weekly_change,
        }
        print(f"  {ticker}: close={latest_close}  weekly_change={weekly_change:+.1f}%")

    return prices


def build_output(prices: dict) -> dict:
    """Attach today's date and return the final output object."""
    today = datetime.today().strftime("%Y-%m-%d")
    return {"date": today, **prices}


def save_output(data: dict, filepath: str = None) -> None:
    """
    Write the output dictionary to a JSON file.

    Args:
        data:     Data to serialise.
        filepath: Destination file path (overwritten on each run).
                  Defaults to <project_root>/data/output.json
    """
    if filepath is None:
        src_dir  = Path(__file__).resolve().parent   # .../src/
        filepath = src_dir.parent / "data" / "output.json"

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)  # create data/ if needed

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\n Output written to '{filepath}'")


def main():
    print("Fetching market data...")
    prices = fetch_prices()
    output = build_output(prices)
    save_output(output)
    print(f"Output:\n{json.dumps(output, indent=2)}")


if __name__ == "__main__":
    main()

