"""
Market Data Collector - Level 2 → 3 Pipeline
Fetches closing prices for SPY, QQQ, IWM from Yahoo Finance
and saves the result as output.json
"""

import json
import yfinance as yf
from datetime import datetime


def fetch_market_data(tickers: list[str]) -> dict:
    """
    Fetch the latest available closing price for each ticker.

    Args:
        tickers: List of ticker symbols to retrieve.

    Returns:
        Dictionary mapping each ticker to its latest closing price.
    """
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            # 'history' with period='1d' returns today's bar (or latest available)
            hist = data.history(period="1d")
            if hist.empty:
                # Fall back to the most recent available session
                hist = data.history(period="5d")
            if hist.empty:
                raise ValueError(f"No price data returned for {ticker}")
            closing_price = round(float(hist["Close"].iloc[-1]), 2)
            prices[ticker] = closing_price
        except Exception as exc:
            print(f"[ERROR] Could not retrieve data for {ticker}: {exc}")
            raise

    return prices


def build_output(prices: dict) -> dict:
    """
    Combine today's date with the retrieved prices into the output schema.

    Args:
        prices: Mapping of ticker → closing price.

    Returns:
        Structured output dictionary matching the JSON specification.
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    return {
        "date": today,
        **prices,
    }


def save_output(data: dict, filepath: str = "output.json") -> None:
    """
    Write the output dictionary to a JSON file.

    Args:
        data:     Data to serialise.
        filepath: Destination file path (overwritten on each run).
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] output written to '{filepath}'")


def main() -> None:
    tickers = ["SPY", "QQQ", "IWM"]

    print("Fetching market data …")
    prices = fetch_market_data(tickers)

    output = build_output(prices)
    print(f"Data collected: {output}")

    save_output(output)


if __name__ == "__main__":
    main()
