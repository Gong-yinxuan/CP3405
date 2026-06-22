"""
Prism Macro Data Collector — W5

Collects automatic macro market data and Fed speaker metadata.

Output:
- prism/data/macro/macro_collector_output.json
- prism/data/macro/history/*.json

No config file.
No manual Fed probability.
No fake calendar/news data.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
import yfinance as yf


MACRO_ASSETS = {
    "US_10Y_YIELD": {
        "ticker": "^TNX",
        "name": "US 10-Year Treasury Yield",
        "category": "yield",
        "divide_by_10": True
    },
    "US_30Y_YIELD": {
        "ticker": "^TYX",
        "name": "US 30-Year Treasury Yield",
        "category": "yield",
        "divide_by_10": True
    },
    "WTI": {
        "ticker": "CL=F",
        "name": "Crude Oil WTI Futures",
        "category": "commodity",
        "divide_by_10": False
    },
    "GOLD": {
        "ticker": "GC=F",
        "name": "Gold Futures",
        "category": "commodity",
        "divide_by_10": False
    },
    "DXY": {
        "ticker": "DX-Y.NYB",
        "name": "US Dollar Index",
        "category": "currency_index",
        "divide_by_10": False
    },
    "VIX": {
        "ticker": "^VIX",
        "name": "CBOE Volatility Index",
        "category": "volatility",
        "divide_by_10": False
    },
    "BTC": {
        "ticker": "BTC-USD",
        "name": "Bitcoin USD",
        "category": "crypto",
        "divide_by_10": False
    }
}


FED_SPEECHES_RSS_URL = "https://www.federalreserve.gov/feeds/speeches.xml"


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_json(data: dict | list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)

    print(f"[OK] Saved {path}")


def scale_value(value: float, divide_by_10: bool) -> float:
    if divide_by_10:
        return round(value / 10, 4)

    return round(value, 4)


def fetch_history(ticker: str, divide_by_10: bool, period: str = "1mo") -> list[dict]:
    asset = yf.Ticker(ticker)
    hist = asset.history(period=period, interval="1d")

    if hist.empty:
        raise ValueError(f"No data returned for {ticker}")

    records = []

    for date_index, row in hist.iterrows():
        close = scale_value(float(row["Close"]), divide_by_10)

        records.append({
            "date": date_index.strftime("%Y-%m-%d"),
            "close": close
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


def calculate_5d_change(history: list[dict]) -> float | None:
    if len(history) < 6:
        return None

    latest_close = history[-1]["close"]
    previous_close = history[-6]["close"]

    return round(latest_close - previous_close, 4)


def classify_direction(change: float | None) -> str:
    if change is None:
        return "Unknown"

    if change > 0:
        return "Up"

    if change < 0:
        return "Down"

    return "Flat"


def classify_fed_speech_tone_hint(title: str, summary: str) -> str:
    """
    Simple keyword-based hint only.
    R4 should still review the real speech meaning manually or with LLM support.
    """

    text = f"{title} {summary}".lower()

    hawkish_keywords = [
        "inflation",
        "price stability",
        "restrictive",
        "tightening",
        "higher rates",
        "labor market"
    ]

    dovish_keywords = [
        "slowdown",
        "softening",
        "unemployment",
        "easing",
        "rate cut",
        "downside risks"
    ]

    hawkish_score = sum(1 for word in hawkish_keywords if word in text)
    dovish_score = sum(1 for word in dovish_keywords if word in text)

    if hawkish_score > dovish_score:
        return "hawkish_keyword_hint"

    if dovish_score > hawkish_score:
        return "dovish_keyword_hint"

    return "neutral_or_unclear_keyword_hint"


def fetch_fed_speeches(days_back: int = 14, max_items: int = 10) -> list[dict]:
    """
    Fetch recent Fed speeches from the Federal Reserve speeches RSS feed.
    This collects metadata only: title, date, link, summary, and keyword tone hint.
    """

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

    response = requests.get(FED_SPEECHES_RSS_URL, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    speeches = []

    for item in root.findall("./channel/item"):
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        summary = item.findtext("description", default="").strip()
        pub_date_text = item.findtext("pubDate", default="").strip()

        if not title:
            continue

        try:
            published_at = parsedate_to_datetime(pub_date_text)

            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)

        except Exception:
            published_at = None

        if published_at and published_at < cutoff_date:
            continue

        speeches.append({
            "title": title,
            "published_at": published_at.isoformat() if published_at else pub_date_text,
            "source_url": link,
            "summary": summary,
            "tone_hint": classify_fed_speech_tone_hint(title, summary),
            "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
        })

        if len(speeches) >= max_items:
            break

    return speeches


def build_macro_record(symbol: str, info: dict, history: list[dict]) -> dict:
    latest = history[-1]
    weekly_change = calculate_weekly_change(history)
    change_5d = calculate_5d_change(history)

    return {
        "symbol": symbol,
        "yahoo_ticker": info["ticker"],
        "name": info["name"],
        "category": info["category"],
        "latest_trading_date": latest["date"],
        "close": latest["close"],
        "weekly_change_pct": weekly_change,
        "change_5d": change_5d,
        "direction_5d": classify_direction(change_5d),
        "history_file": f"macro/history/{symbol}.json"
    }


def main() -> None:
    project_root = get_project_root()

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collector": "Macro Collector",
        "agent_input_for": "Macro Agent",
        "data_source": {
            "market_data": "Yahoo Finance via yfinance",
            "fed_speakers": "Federal Reserve speeches RSS feed"
        },
        "note": (
            "This collector gathers automatic macro market data and recent Fed speaker metadata. "
            "FedWatch probability, earnings, economic calendar, and news are not collected here."
        ),
        "macro_market_data": {},
        "fed_speakers": [],
        "fed_speaker_count": 0
    }

    print("Fetching macro data...")

    for symbol, info in MACRO_ASSETS.items():
        try:
            history = fetch_history(
                info["ticker"],
                divide_by_10=info["divide_by_10"],
                period="1mo"
            )

            history_path = (
                project_root
                / "data"
                / "macro"
                / "history"
                / f"{symbol}.json"
            )

            save_json(history, history_path)

            output["macro_market_data"][symbol] = build_macro_record(
                symbol,
                info,
                history
            )

            print(f"[OK] Macro data collected for {symbol}")

        except Exception as error:
            output["macro_market_data"][symbol] = {
                "symbol": symbol,
                "yahoo_ticker": info["ticker"],
                "name": info["name"],
                "category": info["category"],
                "error": str(error)
            }

            print(f"[ERROR] Failed to collect {symbol}: {error}")

    try:
        print("Fetching recent Fed speeches...")

        output["fed_speakers"] = fetch_fed_speeches(
            days_back=14,
            max_items=10
        )

        output["fed_speaker_count"] = len(output["fed_speakers"])

        print(f"[OK] Fed speeches collected: {output['fed_speaker_count']}")

    except Exception as error:
        output["fed_speakers_error"] = str(error)
        output["fed_speaker_count"] = 0

        print(f"[ERROR] Failed to collect Fed speeches: {error}")

    output_path = project_root / "data" / "macro" / "macro_collector_output.json"
    save_json(output, output_path)

    print("Macro collection complete.")


if __name__ == "__main__":
    main()