"""
Prism Macro Data Collector — W5

Collects automatic macro market data and Fed + Data Watch information.

Output:
- prism/data/macro/macro_collector_output.json
- prism/data/macro/macro_data_watch.md
- prism/data/macro/history/*.json

No manual Fed probability.
No FedWatch scraping.
No fake calendar/news data.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta, date
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

BLS_RELEASE_FEEDS = {
    "CPI": "https://www.bls.gov/feed/cpi.rss",
    "PPI": "https://www.bls.gov/feed/ppi.rss",
    "IMPORT_EXPORT_PRICES": "https://www.bls.gov/feed/ximpim.rss",
    "REAL_EARNINGS": "https://www.bls.gov/feed/realer.rss",
    "EMPLOYMENT_SITUATION": "https://www.bls.gov/feed/empsit.rss"
}


REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PrismMacroCollector/1.0; +https://github.com/)",
    "Accept": "application/rss+xml, application/xml, text/xml, text/html;q=0.9,*/*;q=0.8"
}


EARNINGS_WATCHLIST = {
    # Banks / financials
    "JPM": {"company": "JPMorgan Chase", "why_it_matters": "Large U.S. bank; credit quality, loan demand, trading revenue, and economic outlook."},
    "BAC": {"company": "Bank of America", "why_it_matters": "Consumer banking, deposits, net interest income, and credit stress."},
    "C": {"company": "Citigroup", "why_it_matters": "Global banking, credit trends, and risk appetite."},
    "WFC": {"company": "Wells Fargo", "why_it_matters": "Consumer credit, loan demand, and deposit pressure."},
    "GS": {"company": "Goldman Sachs", "why_it_matters": "Investment banking, trading activity, and market-risk appetite."},
    "MS": {"company": "Morgan Stanley", "why_it_matters": "Investment banking, wealth management, and capital markets sentiment."},

    # Mega-cap / macro-sensitive growth
    "AAPL": {"company": "Apple", "why_it_matters": "Mega-cap demand signal and large weight in SPX/NDX."},
    "MSFT": {"company": "Microsoft", "why_it_matters": "Cloud/AI demand and large-cap technology leadership."},
    "NVDA": {"company": "NVIDIA", "why_it_matters": "AI semiconductor demand and high-beta technology leadership."},
    "TSLA": {"company": "Tesla", "why_it_matters": "Consumer discretionary risk appetite and high-beta growth sentiment."}
}


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def save_json(data: dict | list, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)

    print(f"[OK] Saved {path}")


def save_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

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


def get_week_window(today: datetime | None = None) -> dict:
    """
    Calculates the current week commencing Monday.
    Example:
    If today is Wednesday, returns Monday to Sunday of that week.
    """

    if today is None:
        today = datetime.now(timezone.utc)

    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=0)

    return {
        "week_commencing": start_of_week.strftime("%Y-%m-%d"),
        "week_ending": end_of_week.strftime("%Y-%m-%d"),
        "start": start_of_week,
        "end": end_of_week
    }


def parse_rss_date(pub_date_text: str) -> datetime | None:
    if not pub_date_text:
        return None

    try:
        published_at = parsedate_to_datetime(pub_date_text)

        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)

        return published_at

    except Exception:
        return None


def is_relevant_date(
    published_at: datetime | None,
    week_start: datetime,
    week_end: datetime,
    lookback_days: int = 7
) -> bool:
    """
    Includes items from the target week plus a small lookback window.
    This helps catch CPI/inflation data released just before the week.
    """

    if published_at is None:
        return True

    lower_bound = week_start - timedelta(days=lookback_days)
    upper_bound = week_end + timedelta(days=1)

    return lower_bound <= published_at <= upper_bound


def clean_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def extract_speaker_hint(title: str) -> str:
    """
    Fed speech titles often start with the speaker name.
    This is only a simple hint.
    """

    if "," in title:
        return title.split(",")[0].strip()

    return "Unknown speaker"


def classify_fed_speech_tone_hint(title: str, summary: str) -> str:
    """
    Simple keyword-based hint only.
    R4 should still review the actual speech meaning manually or with LLM support.
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


def fetch_fed_speeches(week_window: dict, max_items: int = 10) -> list[dict]:
    """
    Fetch Fed speaker metadata from the Federal Reserve speeches RSS feed.
    """

    response = requests.get(FED_SPEECHES_RSS_URL, timeout=30, headers=REQUEST_HEADERS)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    speeches = []

    for item in root.findall("./channel/item"):
        title = clean_text(item.findtext("title", default=""))
        link = clean_text(item.findtext("link", default=""))
        summary = clean_text(item.findtext("description", default=""))
        pub_date_text = clean_text(item.findtext("pubDate", default=""))

        if not title:
            continue

        published_at = parse_rss_date(pub_date_text)

        if not is_relevant_date(
            published_at,
            week_window["start"],
            week_window["end"],
            lookback_days=7
        ):
            continue

        speeches.append({
            "speaker_hint": extract_speaker_hint(title),
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


def fetch_bls_feed(feed_name: str, feed_url: str, week_window: dict, max_items: int = 5) -> list[dict]:
    """
    Fetch BLS release metadata from one BLS RSS feed.
    """

    response = requests.get(feed_url, timeout=30, headers=REQUEST_HEADERS)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    releases = []

    for item in root.findall("./channel/item"):
        title = clean_text(item.findtext("title", default=""))
        link = clean_text(item.findtext("link", default=""))
        summary = clean_text(item.findtext("description", default=""))
        pub_date_text = clean_text(item.findtext("pubDate", default=""))

        if not title:
            continue

        published_at = parse_rss_date(pub_date_text)

        if not is_relevant_date(
            published_at,
            week_window["start"],
            week_window["end"],
            lookback_days=7
        ):
            continue

        releases.append({
            "feed": feed_name,
            "title": title,
            "published_at": published_at.isoformat() if published_at else pub_date_text,
            "source_url": link,
            "summary": summary
        })

        if len(releases) >= max_items:
            break

    return releases


def fetch_bls_releases(week_window: dict) -> dict:
    """
    Fetch CPI/inflation-related and major data-release metadata from BLS RSS feeds.
    """

    output = {
        "inflation_data": [],
        "major_data_releases": [],
        "errors": {}
    }

    inflation_feeds = [
        "CPI",
        "PPI",
        "IMPORT_EXPORT_PRICES",
        "REAL_EARNINGS"
    ]

    major_data_feeds = [
        "EMPLOYMENT_SITUATION"
    ]

    for feed_name in inflation_feeds:
        try:
            items = fetch_bls_feed(
                feed_name,
                BLS_RELEASE_FEEDS[feed_name],
                week_window,
                max_items=3
            )

            output["inflation_data"].extend(items)

        except Exception as error:
            output["errors"][feed_name] = str(error)

    for feed_name in major_data_feeds:
        try:
            items = fetch_bls_feed(
                feed_name,
                BLS_RELEASE_FEEDS[feed_name],
                week_window,
                max_items=3
            )

            output["major_data_releases"].extend(items)

        except Exception as error:
            output["errors"][feed_name] = str(error)

    return output




def normalise_earnings_date(value) -> date | None:
    """
    yfinance calendar formats can change. This function accepts strings,
    datetime/date objects, pandas timestamps, or list-like values and returns a date.
    """

    if value is None:
        return None

    if isinstance(value, (list, tuple)):
        if not value:
            return None
        value = value[0]

    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        # Keep only the date part if yfinance returns a timestamp string.
        text = text.replace("Z", "").split("T")[0].split(" ")[0]
        try:
            return datetime.fromisoformat(text).date()
        except Exception:
            return None

    return None


def extract_earnings_date_from_calendar(calendar_data) -> date | None:
    """
    Best-effort extraction for yfinance calendar output.
    Handles dict-like and DataFrame-like structures.
    """

    if calendar_data is None:
        return None

    # Newer yfinance often returns a dict.
    if isinstance(calendar_data, dict):
        for key in ["Earnings Date", "Earnings High", "Earnings Low"]:
            if key in calendar_data:
                parsed = normalise_earnings_date(calendar_data.get(key))
                if parsed:
                    return parsed

    # Older yfinance sometimes returns a DataFrame with index labels.
    try:
        if hasattr(calendar_data, "loc"):
            for key in ["Earnings Date", "Earnings High", "Earnings Low"]:
                try:
                    value = calendar_data.loc[key].iloc[0]
                    parsed = normalise_earnings_date(value)
                    if parsed:
                        return parsed
                except Exception:
                    pass
    except Exception:
        pass

    # Last fallback: scan values looking for a date.
    try:
        values = calendar_data.values.flatten() if hasattr(calendar_data, "values") else []
        for value in values:
            parsed = normalise_earnings_date(value)
            if parsed:
                return parsed
    except Exception:
        pass

    return None


def fetch_earnings_calendar(week_window: dict) -> dict:
    """
    Fetch upcoming earnings dates for a small macro-relevant watchlist using yfinance.
    This is best-effort. If yfinance does not return a date, the item is skipped and
    the error is recorded instead of inventing an earnings event.
    """

    start_date = week_window["start"].date()
    end_date = week_window["end"].date()

    output = {
        "earnings_calendar": [],
        "errors": {}
    }

    for ticker, info in EARNINGS_WATCHLIST.items():
        try:
            yf_ticker = yf.Ticker(ticker)
            calendar_data = yf_ticker.calendar
            earnings_date = extract_earnings_date_from_calendar(calendar_data)

            if earnings_date is None:
                output["errors"][ticker] = "No earnings date returned by yfinance calendar."
                continue

            if start_date <= earnings_date <= end_date:
                output["earnings_calendar"].append({
                    "ticker": ticker,
                    "company": info["company"],
                    "date": earnings_date.isoformat(),
                    "why_it_matters": info["why_it_matters"],
                    "source": "yfinance calendar"
                })

        except Exception as error:
            output["errors"][ticker] = str(error)

    return output


def build_confirmed_prism_events(output: dict) -> list[str]:
    """
    Build a confirmed-events list using only things Prism actually collected.
    This is not a general news scraper. It summarizes Fed RSS items, BLS release
    metadata, earnings calendar hits, and large macro-market moves.
    """

    events = []
    watch = output.get("fed_and_data_watch", {})
    market = output.get("macro_market_data", {})

    for speech in watch.get("fed_speakers", []):
        speaker = speech.get("speaker_hint", "Fed speaker")
        title = speech.get("title", "Fed speech")
        tone = speech.get("tone_hint", "unknown tone")
        events.append(f"Fed speech captured: {speaker} — {title} ({tone}).")

    for item in watch.get("inflation_data", []) + watch.get("major_data_releases", []):
        feed = item.get("feed", "BLS")
        title = item.get("title", "BLS release")
        published = item.get("published_at", "date unavailable")
        events.append(f"BLS release metadata captured: {feed} — {title} ({published}).")

    for earning in watch.get("earnings_calendar", []):
        company = earning.get("company", earning.get("ticker", "Company"))
        date_text = earning.get("date", "date unavailable")
        events.append(f"Earnings calendar item captured: {company} on {date_text}.")

    y10 = market.get("US_10Y_YIELD", {})
    y30 = market.get("US_30Y_YIELD", {})
    wti = market.get("WTI", {})
    vix = market.get("VIX", {})
    gold = market.get("GOLD", {})

    yield_changes = [item.get("weekly_change_pct") for item in [y10, y30] if isinstance(item.get("weekly_change_pct"), (int, float))]
    if yield_changes:
        avg_yield_change = sum(yield_changes) / len(yield_changes)
        if avg_yield_change > 1.0:
            events.append(f"Treasury yield pressure confirmed: average 10Y/30Y weekly change is +{avg_yield_change:.2f}%.")
        elif avg_yield_change < -1.0:
            events.append(f"Treasury yield relief confirmed: average 10Y/30Y weekly change is {avg_yield_change:.2f}%.")

    if isinstance(wti.get("weekly_change_pct"), (int, float)) and wti["weekly_change_pct"] > 3:
        events.append(f"Oil inflation-risk signal confirmed: WTI weekly change is +{wti['weekly_change_pct']:.2f}%.")

    if isinstance(vix.get("weekly_change_pct"), (int, float)) and vix["weekly_change_pct"] < -5:
        events.append(f"Volatility compression confirmed: VIX weekly change is {vix['weekly_change_pct']:.2f}%.")

    if isinstance(gold.get("weekly_change_pct"), (int, float)) and gold["weekly_change_pct"] < -1.5:
        events.append(f"Gold weakness confirmed: gold weekly change is {gold['weekly_change_pct']:.2f}%.")

    if not events:
        events.append("No confirmed macro events were collected by Prism automation in this run.")

    return events

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


def build_markdown_output(output: dict) -> str:
    watch = output.get("fed_and_data_watch", {})
    week_commencing = watch.get("week_commencing", "Unknown")
    week_ending = watch.get("week_ending", "Unknown")

    fed_speakers = watch.get("fed_speakers", [])
    inflation_data = watch.get("inflation_data", [])
    major_data_releases = watch.get("major_data_releases", [])

    lines = []

    lines.append("# R4 Macro Agent — Fed + Data Watch")
    lines.append("")
    lines.append(f"**Week commencing:** {week_commencing}")
    lines.append(f"**Week ending:** {week_ending}")
    lines.append("")
    lines.append("## Fed Speakers")
    lines.append("")

    if fed_speakers:
        for speech in fed_speakers:
            lines.append(f"- **Speaker hint:** {speech.get('speaker_hint', 'Unknown')}")
            lines.append(f"  - Title: {speech.get('title', '')}")
            lines.append(f"  - Published: {speech.get('published_at', '')}")
            lines.append(f"  - Tone hint: {speech.get('tone_hint', '')}")
            lines.append(f"  - Source: {speech.get('source_url', '')}")
            lines.append("")
    else:
        lines.append("- No recent Fed speeches found in the collector window.")
        lines.append("")

    lines.append("## CPI / Inflation-Related Releases")
    lines.append("")

    if inflation_data:
        for item in inflation_data:
            lines.append(f"- **{item.get('feed', '')}:** {item.get('title', '')}")
            lines.append(f"  - Published: {item.get('published_at', '')}")
            lines.append(f"  - Source: {item.get('source_url', '')}")
            lines.append("")
    else:
        lines.append("- No recent CPI/inflation-related BLS releases found in the collector window.")
        lines.append("")

    lines.append("## Major Data Releases")
    lines.append("")

    if major_data_releases:
        for item in major_data_releases:
            lines.append(f"- **{item.get('feed', '')}:** {item.get('title', '')}")
            lines.append(f"  - Published: {item.get('published_at', '')}")
            lines.append(f"  - Source: {item.get('source_url', '')}")
            lines.append("")
    else:
        lines.append("- No major BLS data releases found in the collector window.")
        lines.append("")

    lines.append("## R4 Interpretation Placeholder")
    lines.append("")
    lines.append("- Fed speaker tone: To be reviewed by R4.")
    lines.append("- Inflation/data impact: To be reviewed by R4.")
    lines.append("- Macro risk level: To be reviewed by R4.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    project_root = get_project_root()
    week_window = get_week_window()

    output = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collector": "Macro Collector",
        "agent_input_for": "Macro Agent",
        "data_source": {
            "market_data": "Yahoo Finance via yfinance",
            "fed_speakers": "Federal Reserve speeches RSS feed",
            "economic_data_releases": "BLS RSS feeds"
        },
        "note": (
            "This collector gathers automatic macro market data and Fed + Data Watch metadata. "
            "FedWatch probability is not collected here."
        ),
        "macro_market_data": {},
        "fed_and_data_watch": {
            "week_commencing": week_window["week_commencing"],
            "week_ending": week_window["week_ending"],
            "fed_speakers": [],
            "fed_speaker_count": 0,
            "inflation_data": [],
            "major_data_releases": [],
            "data_release_errors": {},
            "earnings_calendar": [],
            "earnings_errors": {},
            "confirmed_news_events": []
        }
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

    print("Fetching Fed speakers...")

    try:
        fed_speakers = fetch_fed_speeches(
            week_window=week_window,
            max_items=10
        )

        output["fed_and_data_watch"]["fed_speakers"] = fed_speakers
        output["fed_and_data_watch"]["fed_speaker_count"] = len(fed_speakers)

        print(f"[OK] Fed speeches collected: {len(fed_speakers)}")

    except Exception as error:
        output["fed_and_data_watch"]["fed_speaker_error"] = str(error)
        print(f"[ERROR] Failed to collect Fed speakers: {error}")

    print("Fetching BLS data releases...")

    bls_releases = fetch_bls_releases(week_window)

    output["fed_and_data_watch"]["inflation_data"] = bls_releases["inflation_data"]
    output["fed_and_data_watch"]["major_data_releases"] = bls_releases["major_data_releases"]
    output["fed_and_data_watch"]["data_release_errors"] = bls_releases["errors"]

    print(f"[OK] Inflation releases collected: {len(bls_releases['inflation_data'])}")
    print(f"[OK] Major data releases collected: {len(bls_releases['major_data_releases'])}")

    print("Fetching earnings calendar from yfinance watchlist...")
    earnings_output = fetch_earnings_calendar(week_window)
    output["fed_and_data_watch"]["earnings_calendar"] = earnings_output["earnings_calendar"]
    output["fed_and_data_watch"]["earnings_errors"] = earnings_output["errors"]
    print(f"[OK] Earnings calendar items collected: {len(earnings_output['earnings_calendar'])}")

    output["fed_and_data_watch"]["confirmed_news_events"] = build_confirmed_prism_events(output)

    output_path = project_root / "data" / "macro" / "macro_collector_output.json"
    save_json(output, output_path)

    markdown_path = project_root / "data" / "macro" / "macro_data_watch.md"
    markdown_output = build_markdown_output(output)
    save_text(markdown_output, markdown_path)

    print("Macro collection complete.")


if __name__ == "__main__":
    main()