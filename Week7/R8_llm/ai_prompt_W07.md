You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate and synthesize three independent analysis legs into a forward-looking Weekly Prediction Brief.

1. MASTER MARKET DATA (Verified by Data Pipeline)
[TECHNICAL INDICATOR AGENT DATA]: 
{
  "generated_at": "2026-07-13T02:50:50Z",
  "collector": "Technical Collector",
  "agent_input_for": "Technical Agent",
  "data_source": "Yahoo Finance via yfinance",
  "note": "This collector automates EMA, momentum, and support/resistance candidate data. Manual chart trendlines and annotated screenshots are not automated yet.",
  "instruments": {
    "SPX": {
      "symbol": "SPX",
      "yahoo_ticker": "^GSPC",
      "name": "S&P 500 Index",
      "latest_trading_date": "2026-07-10",
      "last_close": 7575.39,
      "weekly_change_pct": 1.23,
      "ema_8": 7511.06,
      "ema_21": 7472.72,
      "price_vs_8ema": "above",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": 64.33,
      "distance_from_21ema": 102.67,
      "ema_gap": 38.34,
      "ema_condition": "Zone 1 Bullish",
      "recent_20d_high": 7579.93,
      "recent_20d_low": 7257.33,
      "resistance_candidate": 7579.93,
      "support_candidate": 7257.33,
      "technical_bias": "Bullish",
      "history_file": "technical/history/SPX.json"
    },
    "NDX": {
      "symbol": "NDX",
      "yahoo_ticker": "^NDX",
      "name": "Nasdaq 100 Index",
      "latest_trading_date": "2026-07-10",
      "last_close": 29825.11,
      "weekly_change_pct": 1.69,
      "ema_8": 29605.75,
      "ema_21": 29593.23,
      "price_vs_8ema": "above",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": 219.36,
      "distance_from_21ema": 231.88,
      "ema_gap": 12.52,
      "ema_condition": "Zone 1 Bullish",
      "recent_20d_high": 30642.57,
      "recent_20d_low": 28548.5,
      "resistance_candidate": 30642.57,
      "support_candidate": 28548.5,
      "technical_bias": "Bullish",
      "history_file": "technical/history/NDX.json"
    },
    "IWM": {
      "symbol": "IWM",
      "yahoo_ticker": "IWM",
      "name": "Russell 2000 ETF Proxy",
      "latest_trading_date": "2026-07-10",
      "last_close": 295.99,
      "weekly_change_pct": -0.53,
      "ema_8": 296.66,
      "ema_21": 294.77,
      "price_vs_8ema": "below",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": -0.67,
      "distance_from_21ema": 1.22,
      "ema_gap": 1.89,
      "ema_condition": "Zone 2 Pullback",
      "recent_20d_high": 302.72,
      "recent_20d_low": 283.4,
      "resistance_candidate": 302.72,
      "support_candidate": 283.4,
      "technical_bias": "Neutral",
      "history_file": "technical/history/IWM.json"
    }
  }
}

[MACROECONOMIC DATA AGENT DATA]: 
{
  "generated_at": "2026-07-13T02:50:51Z",
  "collector": "Macro Collector",
  "agent_input_for": "Macro Agent",
  "data_source": {
    "market_data": "Yahoo Finance via yfinance",
    "fed_speakers": "Federal Reserve speeches RSS feed",
    "economic_data_releases": "BLS RSS feeds"
  },
  "note": "This collector gathers automatic macro market data and Fed + Data Watch metadata. FedWatch probability is not collected here.",
  "macro_market_data": {
    "US_10Y_YIELD": {
      "symbol": "US_10Y_YIELD",
      "yahoo_ticker": "^TNX",
      "name": "US 10-Year Treasury Yield",
      "category": "yield",
      "latest_trading_date": "2026-07-10",
      "close": 0.4569,
      "weekly_change_pct": 1.87,
      "change_5d": 0.0084,
      "direction_5d": "Up",
      "history_file": "macro/history/US_10Y_YIELD.json"
    },
    "US_30Y_YIELD": {
      "symbol": "US_30Y_YIELD",
      "yahoo_ticker": "^TYX",
      "name": "US 30-Year Treasury Yield",
      "category": "yield",
      "latest_trading_date": "2026-07-10",
      "close": 0.5071,
      "weekly_change_pct": 1.73,
      "change_5d": 0.0086,
      "direction_5d": "Up",
      "history_file": "macro/history/US_30Y_YIELD.json"
    },
    "WTI": {
      "symbol": "WTI",
      "yahoo_ticker": "CL=F",
      "name": "Crude Oil WTI Futures",
      "category": "commodity",
      "latest_trading_date": "2026-07-12",
      "close": 74.27,
      "weekly_change_pct": 8.34,
      "change_5d": 5.72,
      "direction_5d": "Up",
      "history_file": "macro/history/WTI.json"
    },
    "GOLD": {
      "symbol": "GOLD",
      "yahoo_ticker": "GC=F",
      "name": "Gold Futures",
      "category": "commodity",
      "latest_trading_date": "2026-07-12",
      "close": 4079.6001,
      "weekly_change_pct": -1.82,
      "change_5d": -75.5,
      "direction_5d": "Down",
      "history_file": "macro/history/GOLD.json"
    },
    "DXY": {
      "symbol": "DXY",
      "yahoo_ticker": "DX-Y.NYB",
      "name": "US Dollar Index",
      "category": "currency_index",
      "latest_trading_date": "2026-07-12",
      "close": 101.112,
      "weekly_change_pct": 0.26,
      "change_5d": 0.262,
      "direction_5d": "Up",
      "history_file": "macro/history/DXY.json"
    },
    "VIX": {
      "symbol": "VIX",
      "yahoo_ticker": "^VIX",
      "name": "CBOE Volatility Index",
      "category": "volatility",
      "latest_trading_date": "2026-07-10",
      "close": 15.03,
      "weekly_change_pct": -6.93,
      "change_5d": -1.12,
      "direction_5d": "Down",
      "history_file": "macro/history/VIX.json"
    },
    "BTC": {
      "symbol": "BTC",
      "yahoo_ticker": "BTC-USD",
      "name": "Bitcoin USD",
      "category": "crypto",
      "latest_trading_date": "2026-07-13",
      "close": 63424.0391,
      "weekly_change_pct": 0.2,
      "change_5d": 126.6446,
      "direction_5d": "Up",
      "history_file": "macro/history/BTC.json"
    }
  },
  "fed_and_data_watch": {
    "week_commencing": "2026-07-13",
    "week_ending": "2026-07-19",
    "fed_speakers": [
      {
        "speaker_hint": "Bowman",
        "title": "Bowman, Opening Remarks on Sound Practices for Artificial Intelligence",
        "published_at": "2026-07-07T11:00:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/bowman20260707a.htm",
        "summary": "Speech At the Financial Stability Board Virtual Outreach Event",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Waller",
        "title": "Waller, Two Thoughts on the Transmission of Monetary Policy",
        "published_at": "2026-07-06T15:00:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/waller20260706a.htm",
        "summary": "Speech At &quot;Challenges for Monetary Policy Transmission in a Changing World,&quot; a conference sponsored by the Bank of Italy for the research network initiated by the European System of Central Banks, Rome, Italy",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      }
    ],
    "fed_speaker_count": 2,
    "inflation_data": [],
    "major_data_releases": [],
    "data_release_errors": {
      "CPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/cpi.rss",
      "PPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ppi.rss",
      "IMPORT_EXPORT_PRICES": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ximpim.rss",
      "REAL_EARNINGS": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/realer.rss",
      "EMPLOYMENT_SITUATION": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/empsit.rss"
    }
  }
}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]: 
{
  "generated_at": "2026-07-13T02:50:55Z",
  "collector": "Almanac Collector",
  "agent_input_for": "Almanac Agent",
  "data_source": "Yahoo Finance via yfinance + automatic date rules",
  "note": "This collector automates calendar flags and sector ranking. It does not manually interpret seasonal patterns or news.",
  "forecast_window": {
    "generated_from_date_utc": "2026-07-13",
    "start": "2026-07-20",
    "end": "2026-07-24"
  },
  "calendar_flags": {
    "month": "July",
    "june_seasonal_weakness_flag": false,
    "midterm_year_flag": true,
    "options_expiry_date": "2026-07-17",
    "options_expiry_week_flag": false,
    "market_holiday_in_window_flag": false,
    "compressed_trading_week_flag": false,
    "holidays_in_window": []
  },
  "sector_weekly_performance": {
    "XLK": {
      "ticker": "XLK",
      "sector": "Technology",
      "latest_trading_date": "2026-07-10",
      "close": 185.78,
      "weekly_change_pct": 2.87,
      "history_file": "almanac/sector_history/XLK.json"
    },
    "XLF": {
      "ticker": "XLF",
      "sector": "Financials",
      "latest_trading_date": "2026-07-10",
      "close": 55.71,
      "weekly_change_pct": 0.16,
      "history_file": "almanac/sector_history/XLF.json"
    },
    "XLV": {
      "ticker": "XLV",
      "sector": "Healthcare",
      "latest_trading_date": "2026-07-10",
      "close": 160.84,
      "weekly_change_pct": -1.77,
      "history_file": "almanac/sector_history/XLV.json"
    },
    "XLE": {
      "ticker": "XLE",
      "sector": "Energy",
      "latest_trading_date": "2026-07-10",
      "close": 55.08,
      "weekly_change_pct": 3.49,
      "history_file": "almanac/sector_history/XLE.json"
    },
    "XLB": {
      "ticker": "XLB",
      "sector": "Materials",
      "latest_trading_date": "2026-07-10",
      "close": 50.89,
      "weekly_change_pct": -2.15,
      "history_file": "almanac/sector_history/XLB.json"
    },
    "XLI": {
      "ticker": "XLI",
      "sector": "Industrials",
      "latest_trading_date": "2026-07-10",
      "close": 181.92,
      "weekly_change_pct": -1.08,
      "history_file": "almanac/sector_history/XLI.json"
    },
    "XLY": {
      "ticker": "XLY",
      "sector": "Consumer Discretionary",
      "latest_trading_date": "2026-07-10",
      "close": 117.24,
      "weekly_change_pct": 0.1,
      "history_file": "almanac/sector_history/XLY.json"
    },
    "XLP": {
      "ticker": "XLP",
      "sector": "Consumer Staples",
      "latest_trading_date": "2026-07-10",
      "close": 84.12,
      "weekly_change_pct": -1.02,
      "history_file": "almanac/sector_history/XLP.json"
    },
    "XLU": {
      "ticker": "XLU",
      "sector": "Utilities",
      "latest_trading_date": "2026-07-10",
      "close": 45.41,
      "weekly_change_pct": -0.76,
      "history_file": "almanac/sector_history/XLU.json"
    },
    "XLC": {
      "ticker": "XLC",
      "sector": "Communication Services",
      "latest_trading_date": "2026-07-10",
      "close": 111.64,
      "weekly_change_pct": 1.86,
      "history_file": "almanac/sector_history/XLC.json"
    },
    "XLRE": {
      "ticker": "XLRE",
      "sector": "Real Estate",
      "latest_trading_date": "2026-07-10",
      "close": 44.45,
      "weekly_change_pct": -0.51,
      "history_file": "almanac/sector_history/XLRE.json"
    }
  },
  "sector_ranking": {
    "leading_sectors": [
      {
        "ticker": "XLE",
        "sector": "Energy",
        "weekly_change_pct": 3.49
      },
      {
        "ticker": "XLK",
        "sector": "Technology",
        "weekly_change_pct": 2.87
      },
      {
        "ticker": "XLC",
        "sector": "Communication Services",
        "weekly_change_pct": 1.86
      }
    ],
    "lagging_sectors": [
      {
        "ticker": "XLB",
        "sector": "Materials",
        "weekly_change_pct": -2.15
      },
      {
        "ticker": "XLV",
        "sector": "Healthcare",
        "weekly_change_pct": -1.77
      },
      {
        "ticker": "XLI",
        "sector": "Industrials",
        "weekly_change_pct": -1.08
      }
    ]
  }
}
{}

2. YOUR REQUIRED EVALUATION OUTPUT FORMAT
Provide a punchy, highly structured synthesis detailing the following dimensions:
WEEKLY REGIME: Dominant expected market regime.
INDEX OUTLOOK: Direction, Estimated % move, and Key reason for SPX, NDX, and IWM.
SECTOR LEADERSHIP: Leading sector, Lagging sector, and why leadership matters this week.
CORE SYNTHESIS MATRIX: Alignment/conflict points between Technical, Macro, and Almanac legs.

Rules:
- Use only provided evidence. Do not invent external data points or trends.
- Output strictly as valid, clean JSON matching the target keys below. No markdown wrappers.

{
  "weekly_regime": "text description here",
  "confidence_score": "High, Medium, or Low",
  "spx_pct_estimate": "Estimated percentage range",
  "ndx_pct_estimate": "Estimated percentage range",
  "iwm_pct_estimate": "Estimated percentage range",
  "top_supporting_reason": "Single strong statement summary",
  "top_contradiction_cited": "Single core threat summary",
  "invalidation_condition": "Specific closing level or yield target breaker",
  "tone_caveat_language": "Short description of target exposure alignment",

  "consensus_bias": "BULLISH / BEARISH / NEUTRAL / MIXED",
  "consensus_read_summary": "A 2-3 sentence paragraph summarizing model alignment and core agreements based on data...",
  "point_of_maximum_divergence": "The single biggest disagreement point between aggressive and defensive views...",
  "key_supporting_factors": ["Live factor 1 from data", "Live factor 2 from data"],
  "main_contradiction_risk": "The top structural risk moving against the consensus trend this week...",
  "invalidation_summary": "The exact parameter or support level that breaks this consensus view...",
  "r7_human_score_question": "A critical evaluation question helping the human team weigh the conflicting data legs...",
  "r6_slide_bullet_1": "Core slide takeaway bullet 1...",
  "r6_slide_bullet_2": "Core slide takeaway bullet 2...",
  "r6_slide_bullet_3": "Core slide takeaway bullet 3..."
}