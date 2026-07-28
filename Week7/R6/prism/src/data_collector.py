"""
PRISM R6 market actuals collector.

Fetches the three core index exposures, supporting macro assets, and all
11 S&P 500 sector ETFs from Yahoo Finance. The output schema intentionally
remains compatible with the existing R10 calibration runner:

{
  "date": "YYYY-MM-DD",
  "SPX": {"close": 0.0, "weekly_change_pct": 0.0},
  ...
}

The collector fails fast if a required asset is missing and writes output.json
atomically so downstream tools never read a partially written file.
"""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yfinance as yf


CORE_INDICES = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "IWM": "IWM",
}

MACRO_ASSETS = {
    "GOLD": "GC=F",
    "WTI": "CL=F",
    "US10Y": "^TNX",
    "TLT": "TLT",
    "VIX": "^VIX",
    "BTC": "BTC-USD",
}

# Complete Sprint 7 S&P 500 sector coverage.
SECTOR_ETFS = {
    "XLK": "XLK",    # Technology
    "XLV": "XLV",    # Health Care
    "XLF": "XLF",    # Financials
    "XLY": "XLY",    # Consumer Discretionary
    "XLC": "XLC",    # Communication Services
    "XLI": "XLI",    # Industrials
    "XLP": "XLP",    # Consumer Staples
    "XLE": "XLE",    # Energy
    "XLB": "XLB",    # Materials
    "XLRE": "XLRE",  # Real Estate
    "XLU": "XLU",    # Utilities
}

TICKERS = {**CORE_INDICES, **MACRO_ASSETS, **SECTOR_ETFS}
EXPECTED_SECTORS = {
    "XLK", "XLV", "XLF", "XLY", "XLC", "XLI",
    "XLP", "XLE", "XLB", "XLRE", "XLU",
}


def validate_ticker_configuration() -> None:
    """Fail before network access if the 11-sector universe is incomplete."""
    configured = set(SECTOR_ETFS)
    missing = EXPECTED_SECTORS - configured
    unexpected = configured - EXPECTED_SECTORS

    if missing or unexpected or len(configured) != 11:
        raise ValueError(
            "Invalid sector ETF configuration. "
            f"missing={sorted(missing)}, unexpected={sorted(unexpected)}"
        )


def _normalise_close(symbol: str, value: float) -> float:
    # Yahoo Finance reports ^TNX at ten times the percentage yield.
    if symbol == "US10Y":
        value /= 10
    return round(float(value), 2)


def fetch_prices(max_attempts: int = 4) -> dict[str, dict[str, float]]:
    """Fetch latest close and five-trading-day change with retry/backoff."""
    prices: dict[str, dict[str, float]] = {}

    for symbol, yahoo_symbol in TICKERS.items():
        last_error: Exception | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                history = yf.Ticker(yahoo_symbol).history(
                    period="15d",
                    auto_adjust=False,
                )

                if "Close" not in history or history["Close"].dropna().shape[0] < 6:
                    raise ValueError(
                        f"Not enough valid close data for {symbol} ({yahoo_symbol})"
                    )

                closes = history["Close"].dropna()
                latest_close = _normalise_close(symbol, closes.iloc[-1])
                previous_close = _normalise_close(symbol, closes.iloc[-6])

                if previous_close == 0:
                    raise ValueError(f"Previous close is zero for {symbol}")

                weekly_change = round(
                    ((latest_close - previous_close) / previous_close) * 100,
                    1,
                )

                prices[symbol] = {
                    "close": latest_close,
                    "weekly_change_pct": weekly_change,
                }
                print(
                    f"{symbol}: close={latest_close} "
                    f"weekly_change={weekly_change:+.1f}%"
                )
                time.sleep(0.5)
                break

            except Exception as exc:
                last_error = exc
                if attempt == max_attempts:
                    raise RuntimeError(
                        f"Yahoo Finance failed for {symbol} after "
                        f"{max_attempts} attempts: {last_error}"
                    ) from exc

                wait_seconds = (2 ** (attempt - 1)) * 10 + random.randint(1, 5)
                print(
                    f"[WARN] {symbol} attempt {attempt} failed: {exc}. "
                    f"Retrying in {wait_seconds}s."
                )
                time.sleep(wait_seconds)

    return prices

def build_output(prices: dict[str, dict[str, float]]) -> dict[str, Any]:
    """Build the backwards-compatible JSON object used by downstream tools."""
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        **prices,
    }


def validate_output(data: dict[str, Any]) -> None:
    """Validate required keys and numeric fields before writing the file."""
    if not isinstance(data.get("date"), str):
        raise ValueError("Output must contain a string 'date' field")

    datetime.strptime(data["date"], "%Y-%m-%d")

    missing_assets = set(TICKERS) - set(data)
    if missing_assets:
        raise ValueError(f"Output is missing required assets: {sorted(missing_assets)}")

    for symbol in TICKERS:
        record = data[symbol]
        if not isinstance(record, dict):
            raise TypeError(f"{symbol} must map to an object")

        for field in ("close", "weekly_change_pct"):
            value = record.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(f"{symbol}.{field} must be numeric")


def save_output(data: dict[str, Any], filepath: str | Path | None = None) -> Path:
    """Atomically write validated data to prism/data/output.json."""
    validate_output(data)

    if filepath is None:
        prism_root = Path(__file__).resolve().parent.parent
        filepath = prism_root / "data" / "output.json"

    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")

    with temporary_path.open("w", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")

    temporary_path.replace(output_path)
    print(f"Output written to '{output_path}'")
    return output_path


def main() -> None:
    validate_ticker_configuration()
    prices = fetch_prices()
    output = build_output(prices)
    save_output(output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
