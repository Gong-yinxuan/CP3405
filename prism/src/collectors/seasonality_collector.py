"""
Prism Monthly Seasonality Collector

Fills the gap the Almanac Collector explicitly does not cover: exact
historical average % return and seasonal rank per calendar month, for major
US indices, plus the same broken out by US presidential-cycle-year phase
(election / post-election / midterm / pre-election).

Uses full available yfinance monthly-close history. This is a slow-changing
dataset (only shifts as new months of data arrive), so it does not need to
run on the same weekly cadence as the other collectors -- monthly is enough.

Output:
- prism/data/almanac/monthly_seasonality.json
"""

import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf


INDEX_TICKERS = {
    "S&P 500": "^GSPC",
    "DJIA / Dow": "^DJI",
    "NASDAQ": "^IXIC",
    "Russell 2000 / IWM": "^RUT",
}


def get_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "prism":
            return parent
    raise FileNotFoundError("Could not find prism folder.")


def cycle_phase(year: int) -> str:
    """US presidential cycle, anchored the same way as almanac_collector.py's
    is_midterm_year (election years are 2024, 2028, ...)."""
    r = (year - 2024) % 4
    return {
        0: "election_year",
        1: "post_election_year",
        2: "midterm_year",
        3: "pre_election_year",
    }[r]


def fetch_monthly_returns(ticker: str) -> pd.DataFrame:
    hist = yf.Ticker(ticker).history(period="max", interval="1mo")
    if hist.empty:
        raise ValueError(f"No data returned for {ticker}")

    df = hist[["Close"]].dropna().copy()
    df["pct_return"] = df["Close"].pct_change() * 100
    df = df.dropna()
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["cycle_phase"] = df["year"].apply(cycle_phase)
    return df


def build_seasonality_for_index(ticker: str) -> dict:
    df = fetch_monthly_returns(ticker)

    # --- Plain calendar-month seasonality (all years pooled) ---
    monthly_avg = df.groupby("month")["pct_return"].mean()
    monthly_rank = monthly_avg.rank(ascending=False, method="min").astype(int)

    # --- Same, but split by cycle-year phase ---
    cycle_stats = {}
    for phase in ["election_year", "post_election_year", "midterm_year", "pre_election_year"]:
        subset = df[df["cycle_phase"] == phase]
        if subset.empty:
            continue
        phase_avg = subset.groupby("month")["pct_return"].mean()
        phase_rank = phase_avg.rank(ascending=False, method="min").astype(int)
        cycle_stats[phase] = {
            "avg_return_pct_by_month": {int(m): round(float(v), 2) for m, v in phase_avg.items()},
            "rank_by_month": {int(m): int(r) for m, r in phase_rank.items()},
            "num_years_sampled": int(subset["year"].nunique()),
        }

    return {
        "monthly_avg_return_pct": {int(m): round(float(v), 2) for m, v in monthly_avg.items()},
        "monthly_rank": {int(m): int(r) for m, r in monthly_rank.items()},
        "by_cycle_phase": cycle_stats,
        "data_start": str(df.index.min().date()),
        "data_end": str(df.index.max().date()),
        "num_years_total": int(df["year"].nunique()),
    }


def main() -> None:
    project_root = get_project_root()

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collector": "Monthly Seasonality Collector",
        "data_source": "Yahoo Finance via yfinance (full available monthly history)",
        "note": (
            "Historical average % return and seasonal rank per calendar month, "
            "and the same broken out by US presidential-cycle-year phase. "
            "Rank 1 = highest average return for that grouping."
        ),
        "indices": {},
    }

    for label, ticker in INDEX_TICKERS.items():
        print(f"Computing seasonality for {label} ({ticker})...")
        try:
            output["indices"][label] = build_seasonality_for_index(ticker)
        except Exception as error:
            output["indices"][label] = {"error": str(error)}
            print(f"[ERROR] {label}: {error}")

    out_path = project_root / "data" / "almanac" / "monthly_seasonality.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"[OK] Saved {out_path}")


if __name__ == "__main__":
    main()