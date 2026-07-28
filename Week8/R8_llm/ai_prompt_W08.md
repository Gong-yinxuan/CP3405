You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate and synthesize three independent analysis legs into a forward-looking Weekly Prediction Brief.

1. MASTER MARKET DATA (Verified by Data Pipeline)
[TECHNICAL INDICATOR AGENT DATA]: 
{
  "generated_at": "2026-07-23T10:02:17Z",
  "collector": "Technical Collector",
  "agent_input_for": "Technical Agent",
  "data_source": "Yahoo Finance via yfinance",
  "note": "This collector automates EMA, momentum, and support/resistance candidate data. Manual chart trendlines and annotated screenshots are not automated yet.",
  "instruments": {
    "SPX": {
      "symbol": "SPX",
      "yahoo_ticker": "^GSPC",
      "name": "S&P 500 Index",
      "latest_trading_date": "2026-07-22",
      "last_close": 7498.96,
      "weekly_change_pct": -0.97,
      "ema_8": 7500.85,
      "ema_21": 7489.92,
      "price_vs_8ema": "below",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": -1.89,
      "distance_from_21ema": 9.04,
      "ema_gap": 10.93,
      "ema_condition": "Zone 2 Pullback",
      "recent_20d_high": 7581.5,
      "recent_20d_low": 7294.18,
      "resistance_candidate": 7581.5,
      "support_candidate": 7294.18,
      "technical_bias": "Neutral",
      "history_file": "technical/history/SPX.json"
    },
    "NDX": {
      "symbol": "NDX",
      "yahoo_ticker": "^NDX",
      "name": "Nasdaq 100 Index",
      "latest_trading_date": "2026-07-22",
      "last_close": 28998.1,
      "weekly_change_pct": -1.71,
      "ema_8": 29084.56,
      "ema_21": 29304.22,
      "price_vs_8ema": "below",
      "ema_8_vs_21ema": "below",
      "distance_from_8ema": -86.46,
      "distance_from_21ema": -306.12,
      "ema_gap": -219.66,
      "ema_condition": "Zone 3 Bearish",
      "recent_20d_high": 30328.79,
      "recent_20d_low": 28231.32,
      "resistance_candidate": 30328.79,
      "support_candidate": 28231.32,
      "technical_bias": "Bearish",
      "history_file": "technical/history/NDX.json"
    },
    "IWM": {
      "symbol": "IWM",
      "yahoo_ticker": "IWM",
      "name": "Russell 2000 ETF Proxy",
      "latest_trading_date": "2026-07-22",
      "last_close": 293.79,
      "weekly_change_pct": -0.67,
      "ema_8": 294.77,
      "ema_21": 294.63,
      "price_vs_8ema": "below",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": -0.98,
      "distance_from_21ema": -0.84,
      "ema_gap": 0.14,
      "ema_condition": "Zone 2 Pullback",
      "recent_20d_high": 302.72,
      "recent_20d_low": 290.68,
      "resistance_candidate": 302.72,
      "support_candidate": 290.68,
      "technical_bias": "Neutral",
      "history_file": "technical/history/IWM.json"
    }
  }
}

[MACROECONOMIC DATA AGENT DATA]: 
{
  "generated_at": "2026-07-23T10:02:18Z",
  "collector": "Macro Collector",
  "agent_input_for": "Macro Agent",
  "data_source": {
    "market_data": "Yahoo Finance via yfinance",
    "fed_speakers": "Federal Reserve speeches RSS feed",
    "economic_data_releases": "BLS RSS feeds with BLS release calendar ICS fallback"
  },
  "note": "This collector gathers automatic macro market data and Fed + Data Watch metadata. FedWatch probability is not collected here.",
  "macro_market_data": {
    "US_10Y_YIELD": {
      "symbol": "US_10Y_YIELD",
      "yahoo_ticker": "^TNX",
      "name": "US 10-Year Treasury Yield",
      "category": "yield",
      "latest_trading_date": "2026-07-22",
      "close": 0.4657,
      "weekly_change_pct": 2.46,
      "change_5d": 0.0112,
      "direction_5d": "Up",
      "history_file": "macro/history/US_10Y_YIELD.json"
    },
    "US_30Y_YIELD": {
      "symbol": "US_30Y_YIELD",
      "yahoo_ticker": "^TYX",
      "name": "US 30-Year Treasury Yield",
      "category": "yield",
      "latest_trading_date": "2026-07-22",
      "close": 0.5147,
      "weekly_change_pct": 1.26,
      "change_5d": 0.0064,
      "direction_5d": "Up",
      "history_file": "macro/history/US_30Y_YIELD.json"
    },
    "WTI": {
      "symbol": "WTI",
      "yahoo_ticker": "CL=F",
      "name": "Crude Oil WTI Futures",
      "category": "commodity",
      "latest_trading_date": "2026-07-23",
      "close": 90.14,
      "weekly_change_pct": 14.17,
      "change_5d": 11.19,
      "direction_5d": "Up",
      "history_file": "macro/history/WTI.json"
    },
    "GOLD": {
      "symbol": "GOLD",
      "yahoo_ticker": "GC=F",
      "name": "Gold Futures",
      "category": "commodity",
      "latest_trading_date": "2026-07-23",
      "close": 4093.5,
      "weekly_change_pct": 2.71,
      "change_5d": 107.8999,
      "direction_5d": "Up",
      "history_file": "macro/history/GOLD.json"
    },
    "DXY": {
      "symbol": "DXY",
      "yahoo_ticker": "DX-Y.NYB",
      "name": "US Dollar Index",
      "category": "currency_index",
      "latest_trading_date": "2026-07-23",
      "close": 101.141,
      "weekly_change_pct": 0.41,
      "change_5d": 0.411,
      "direction_5d": "Up",
      "history_file": "macro/history/DXY.json"
    },
    "VIX": {
      "symbol": "VIX",
      "yahoo_ticker": "^VIX",
      "name": "CBOE Volatility Index",
      "category": "volatility",
      "latest_trading_date": "2026-07-23",
      "close": 17.62,
      "weekly_change_pct": 5.32,
      "change_5d": 0.89,
      "direction_5d": "Up",
      "history_file": "macro/history/VIX.json"
    },
    "BTC": {
      "symbol": "BTC",
      "yahoo_ticker": "BTC-USD",
      "name": "Bitcoin USD",
      "category": "crypto",
      "latest_trading_date": "2026-07-23",
      "close": 65585.5938,
      "weekly_change_pct": 1.22,
      "change_5d": 788.9922,
      "direction_5d": "Up",
      "history_file": "macro/history/BTC.json"
    }
  },
  "fed_and_data_watch": {
    "week_commencing": "2026-07-20",
    "week_ending": "2026-07-26",
    "fed_speakers": [
      {
        "speaker_hint": "Jefferson",
        "title": "Jefferson, Navigating Economic Shocks: A Monetary Policymaker\u2019s Perspective",
        "published_at": "2026-07-16T23:00:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/jefferson20260716a.htm",
        "summary": "Speech At the Stanford Institute for Economic Policy Research, Stanford University, Stanford, California",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Cook",
        "title": "Cook, Economic Outlook",
        "published_at": "2026-07-15T17:00:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/cook20260715a.htm",
        "summary": "Speech At The Exchequer Club of Washington D.C., Washington, D.C.",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Bowman",
        "title": "Bowman, Responsible Innovation and Financial Inclusion",
        "published_at": "2026-07-14T18:55:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/bowman20260714a.htm",
        "summary": "Speech At \u201cNext-Gen Financial Inclusion,\u201d the third annual Financial Inclusion Conference hosted by the Federal Reserve Board, Washington, D.C. (via pre-recorded video)",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Barr",
        "title": "Barr, Will Artificial Intelligence Broadly Raise Living Standards or Drive Income and Wealth Inequality?",
        "published_at": "2026-07-14T16:40:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/barr20260714a.htm",
        "summary": "Speech At \u201cNext-Gen Financial Inclusion,\u201d the third annual Financial Inclusion Conference hosted by the Federal Reserve Board",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Waller",
        "title": "Waller, Monetary Policy at a Crossroads",
        "published_at": "2026-07-13T16:30:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/waller20260713a.htm",
        "summary": "Speech At the New York Association for Business Economics, New York, New York",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      },
      {
        "speaker_hint": "Bowman",
        "title": "Bowman, Modernizing Financial Regulation",
        "published_at": "2026-07-13T09:25:00+00:00",
        "source_url": "https://www.federalreserve.gov/newsevents/speech/bowman20260713a.htm",
        "summary": "Speech At a Bank Policy Institute London Conference, London, United Kingdom",
        "tone_hint": "neutral_or_unclear_keyword_hint",
        "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
      }
    ],
    "fed_speaker_count": 6,
    "inflation_data": [],
    "major_data_releases": [],
    "data_release_errors": {
      "CPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/cpi.rss",
      "PPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ppi.rss",
      "IMPORT_EXPORT_PRICES": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ximpim.rss",
      "REAL_EARNINGS": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/realer.rss",
      "EMPLOYMENT_SITUATION": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/empsit.rss",
      "BLS_CALENDAR_ICS": "403 Client Error: Forbidden for url: https://www.bls.gov/schedule/news_release/bls.ics"
    },
    "rss_errors": {
      "CPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/cpi.rss",
      "PPI": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ppi.rss",
      "IMPORT_EXPORT_PRICES": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/ximpim.rss",
      "REAL_EARNINGS": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/realer.rss",
      "EMPLOYMENT_SITUATION": "403 Client Error: Forbidden for url: https://www.bls.gov/feed/empsit.rss"
    },
    "calendar_source": "BLS RSS feeds + BLS release calendar ICS fallback",
    "calendar_source_url": "https://www.bls.gov/schedule/news_release/bls.ics"
  }
}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]: 
{
  "generated_at": "2026-07-23T10:02:21Z",
  "collector": "Almanac Collector",
  "agent_input_for": "Almanac Agent",
  "data_source": "Yahoo Finance via yfinance + automatic date rules",
  "note": "This collector automates calendar flags and sector ranking. It does not manually interpret seasonal patterns or news.",
  "forecast_window": {
    "generated_from_date_utc": "2026-07-23",
    "start": "2026-07-27",
    "end": "2026-07-31"
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
      "latest_trading_date": "2026-07-22",
      "close": 180.27,
      "weekly_change_pct": -0.72,
      "history_file": "almanac/sector_history/XLK.json"
    },
    "XLF": {
      "ticker": "XLF",
      "sector": "Financials",
      "latest_trading_date": "2026-07-22",
      "close": 56.05,
      "weekly_change_pct": -0.9,
      "history_file": "almanac/sector_history/XLF.json"
    },
    "XLV": {
      "ticker": "XLV",
      "sector": "Healthcare",
      "latest_trading_date": "2026-07-22",
      "close": 159.43,
      "weekly_change_pct": 0.72,
      "history_file": "almanac/sector_history/XLV.json"
    },
    "XLE": {
      "ticker": "XLE",
      "sector": "Energy",
      "latest_trading_date": "2026-07-22",
      "close": 59.2,
      "weekly_change_pct": 4.78,
      "history_file": "almanac/sector_history/XLE.json"
    },
    "XLB": {
      "ticker": "XLB",
      "sector": "Materials",
      "latest_trading_date": "2026-07-22",
      "close": 50.82,
      "weekly_change_pct": 0.63,
      "history_file": "almanac/sector_history/XLB.json"
    },
    "XLI": {
      "ticker": "XLI",
      "sector": "Industrials",
      "latest_trading_date": "2026-07-22",
      "close": 178.85,
      "weekly_change_pct": -0.67,
      "history_file": "almanac/sector_history/XLI.json"
    },
    "XLY": {
      "ticker": "XLY",
      "sector": "Consumer Discretionary",
      "latest_trading_date": "2026-07-22",
      "close": 114.02,
      "weekly_change_pct": -2.55,
      "history_file": "almanac/sector_history/XLY.json"
    },
    "XLP": {
      "ticker": "XLP",
      "sector": "Consumer Staples",
      "latest_trading_date": "2026-07-22",
      "close": 84.38,
      "weekly_change_pct": 1.09,
      "history_file": "almanac/sector_history/XLP.json"
    },
    "XLU": {
      "ticker": "XLU",
      "sector": "Utilities",
      "latest_trading_date": "2026-07-22",
      "close": 45.93,
      "weekly_change_pct": 1.57,
      "history_file": "almanac/sector_history/XLU.json"
    },
    "XLC": {
      "ticker": "XLC",
      "sector": "Communication Services",
      "latest_trading_date": "2026-07-22",
      "close": 109.2,
      "weekly_change_pct": -3.69,
      "history_file": "almanac/sector_history/XLC.json"
    },
    "XLRE": {
      "ticker": "XLRE",
      "sector": "Real Estate",
      "latest_trading_date": "2026-07-22",
      "close": 45.01,
      "weekly_change_pct": 1.01,
      "history_file": "almanac/sector_history/XLRE.json"
    }
  },
  "sector_ranking": {
    "leading_sectors": [
      {
        "ticker": "XLE",
        "sector": "Energy",
        "weekly_change_pct": 4.78
      },
      {
        "ticker": "XLU",
        "sector": "Utilities",
        "weekly_change_pct": 1.57
      },
      {
        "ticker": "XLP",
        "sector": "Consumer Staples",
        "weekly_change_pct": 1.09
      }
    ],
    "lagging_sectors": [
      {
        "ticker": "XLC",
        "sector": "Communication Services",
        "weekly_change_pct": -3.69
      },
      {
        "ticker": "XLY",
        "sector": "Consumer Discretionary",
        "weekly_change_pct": -2.55
      },
      {
        "ticker": "XLF",
        "sector": "Financials",
        "weekly_change_pct": -0.9
      }
    ]
  }
}
{
  "generated_at": "2026-07-23T10:02:16Z",
  "collector": "Monthly Seasonality Collector",
  "data_source": "Yahoo Finance via yfinance (full available monthly history)",
  "note": "Historical average % return and seasonal rank per calendar month, and the same broken out by US presidential-cycle-year phase. Rank 1 = highest average return for that grouping.",
  "indices": {
    "S&P 500": {
      "monthly_avg_return_pct": {
        "1": 0.98,
        "2": 0.35,
        "3": 0.87,
        "4": 1.6,
        "5": 1.46,
        "6": 0.35,
        "7": 1.41,
        "8": -0.26,
        "9": -0.9,
        "10": 0.99,
        "11": 1.91,
        "12": 1.39
      },
      "monthly_rank": {
        "1": 7,
        "2": 10,
        "3": 8,
        "4": 2,
        "5": 3,
        "6": 9,
        "7": 4,
        "8": 11,
        "9": 12,
        "10": 6,
        "11": 1,
        "12": 5
      },
      "by_cycle_phase": {
        "election_year": {
          "avg_return_pct_by_month": {
            "1": -0.35,
            "2": 0.2,
            "3": 0.3,
            "4": 1.31,
            "5": 0.74,
            "6": 0.78,
            "7": 0.42,
            "8": 1.43,
            "9": -0.28,
            "10": -1.83,
            "11": 1.7,
            "12": 0.85
          },
          "rank_by_month": {
            "1": 11,
            "2": 9,
            "3": 8,
            "4": 3,
            "5": 6,
            "6": 5,
            "7": 7,
            "8": 2,
            "9": 10,
            "10": 12,
            "11": 1,
            "12": 4
          },
          "num_years_sampled": 10
        },
        "post_election_year": {
          "avg_return_pct_by_month": {
            "1": 1.47,
            "2": -1.16,
            "3": 0.15,
            "4": 2.74,
            "5": 3.25,
            "6": 0.77,
            "7": 3.35,
            "8": -0.4,
            "9": -0.0,
            "10": 1.29,
            "11": 3.0,
            "12": 1.76
          },
          "rank_by_month": {
            "1": 6,
            "2": 12,
            "3": 9,
            "4": 4,
            "5": 2,
            "6": 8,
            "7": 1,
            "8": 11,
            "9": 10,
            "10": 7,
            "11": 3,
            "12": 5
          },
          "num_years_sampled": 11
        },
        "midterm_year": {
          "avg_return_pct_by_month": {
            "1": -0.63,
            "2": 0.84,
            "3": 1.39,
            "4": -0.27,
            "5": 0.98,
            "6": -1.63,
            "7": 0.57,
            "8": -1.27,
            "9": -2.04,
            "10": 3.38,
            "11": 2.68,
            "12": -0.72
          },
          "rank_by_month": {
            "1": 8,
            "2": 5,
            "3": 3,
            "4": 7,
            "5": 4,
            "6": 11,
            "7": 6,
            "8": 10,
            "9": 12,
            "10": 1,
            "11": 2,
            "12": 9
          },
          "num_years_sampled": 11
        },
        "pre_election_year": {
          "avg_return_pct_by_month": {
            "1": 3.57,
            "2": 1.6,
            "3": 1.68,
            "4": 2.7,
            "5": 0.73,
            "6": 1.64,
            "7": 1.2,
            "8": -0.76,
            "9": -1.38,
            "10": 1.11,
            "11": 0.13,
            "12": 3.66
          },
          "rank_by_month": {
            "1": 2,
            "2": 6,
            "3": 4,
            "4": 3,
            "5": 9,
            "6": 5,
            "7": 7,
            "8": 11,
            "9": 12,
            "10": 8,
            "11": 10,
            "12": 1
          },
          "num_years_sampled": 10
        }
      },
      "data_start": "1985-02-01",
      "data_end": "2026-07-01",
      "num_years_total": 42
    },
    "DJIA / Dow": {
      "monthly_avg_return_pct": {
        "1": 0.28,
        "2": -0.01,
        "3": 0.54,
        "4": 2.17,
        "5": 0.49,
        "6": -0.11,
        "7": 1.59,
        "8": -0.51,
        "9": -0.7,
        "10": 1.75,
        "11": 2.69,
        "12": 0.97
      },
      "monthly_rank": {
        "1": 8,
        "2": 9,
        "3": 6,
        "4": 2,
        "5": 7,
        "6": 10,
        "7": 4,
        "8": 11,
        "9": 12,
        "10": 3,
        "11": 1,
        "12": 5
      },
      "by_cycle_phase": {
        "election_year": {
          "avg_return_pct_by_month": {
            "1": -0.7,
            "2": -1.28,
            "3": 0.44,
            "4": 1.29,
            "5": -0.1,
            "6": -0.34,
            "7": 0.97,
            "8": 1.75,
            "9": -0.56,
            "10": -2.21,
            "11": 3.16,
            "12": 0.79
          },
          "rank_by_month": {
            "1": 10,
            "2": 11,
            "3": 6,
            "4": 3,
            "5": 7,
            "6": 8,
            "7": 4,
            "8": 2,
            "9": 9,
            "10": 12,
            "11": 1,
            "12": 5
          },
          "num_years_sampled": 9
        },
        "post_election_year": {
          "avg_return_pct_by_month": {
            "1": 0.47,
            "2": -0.24,
            "3": 0.28,
            "4": 2.44,
            "5": 2.66,
            "6": 0.29,
            "7": 3.11,
            "8": -0.81,
            "9": -0.51,
            "10": 1.55,
            "11": 3.08,
            "12": 1.74
          },
          "rank_by_month": {
            "1": 7,
            "2": 10,
            "3": 9,
            "4": 4,
            "5": 3,
            "6": 8,
            "7": 1,
            "8": 12,
            "9": 11,
            "10": 6,
            "11": 2,
            "12": 5
          },
          "num_years_sampled": 9
        },
        "midterm_year": {
          "avg_return_pct_by_month": {
            "1": 0.19,
            "2": 0.71,
            "3": 0.12,
            "4": 0.76,
            "5": -0.55,
            "6": -1.97,
            "7": 1.63,
            "8": -1.66,
            "9": -0.88,
            "10": 4.91,
            "11": 2.22,
            "12": -1.08
          },
          "rank_by_month": {
            "1": 6,
            "2": 5,
            "3": 7,
            "4": 4,
            "5": 8,
            "6": 12,
            "7": 3,
            "8": 11,
            "9": 9,
            "10": 1,
            "11": 2,
            "12": 10
          },
          "num_years_sampled": 9
        },
        "pre_election_year": {
          "avg_return_pct_by_month": {
            "1": 1.13,
            "2": 0.86,
            "3": 1.44,
            "4": 4.43,
            "5": -0.15,
            "6": 1.77,
            "7": 0.54,
            "8": -1.55,
            "9": -0.9,
            "10": 3.27,
            "11": 2.18,
            "12": 2.37
          },
          "rank_by_month": {
            "1": 7,
            "2": 8,
            "3": 6,
            "4": 1,
            "5": 10,
            "6": 5,
            "7": 9,
            "8": 12,
            "9": 11,
            "10": 2,
            "11": 4,
            "12": 3
          },
          "num_years_sampled": 8
        }
      },
      "data_start": "1992-02-01",
      "data_end": "2026-07-01",
      "num_years_total": 35
    },
    "NASDAQ": {
      "monthly_avg_return_pct": {
        "1": 2.12,
        "2": 0.62,
        "3": 0.56,
        "4": 1.36,
        "5": 1.89,
        "6": 1.1,
        "7": 1.25,
        "8": 0.27,
        "9": -0.8,
        "10": 0.98,
        "11": 2.18,
        "12": 1.68
      },
      "monthly_rank": {
        "1": 2,
        "2": 9,
        "3": 10,
        "4": 5,
        "5": 3,
        "6": 7,
        "7": 6,
        "8": 11,
        "9": 12,
        "10": 8,
        "11": 1,
        "12": 4
      },
      "by_cycle_phase": {
        "election_year": {
          "avg_return_pct_by_month": {
            "1": 0.4,
            "2": 2.89,
            "3": -0.38,
            "4": -0.06,
            "5": 0.94,
            "6": 2.24,
            "7": -0.62,
            "8": 2.62,
            "9": -0.61,
            "10": -2.95,
            "11": 0.5,
            "12": 1.54
          },
          "rank_by_month": {
            "1": 7,
            "2": 1,
            "3": 9,
            "4": 8,
            "5": 5,
            "6": 3,
            "7": 11,
            "8": 2,
            "9": 10,
            "10": 12,
            "11": 6,
            "12": 4
          },
          "num_years_sampled": 10
        },
        "post_election_year": {
          "avg_return_pct_by_month": {
            "1": 2.7,
            "2": -3.23,
            "3": -1.16,
            "4": 3.51,
            "5": 4.54,
            "6": 1.61,
            "7": 3.57,
            "8": 0.2,
            "9": -0.1,
            "10": 2.23,
            "11": 3.05,
            "12": 1.21
          },
          "rank_by_month": {
            "1": 5,
            "2": 12,
            "3": 11,
            "4": 3,
            "5": 1,
            "6": 7,
            "7": 2,
            "8": 9,
            "9": 10,
            "10": 6,
            "11": 4,
            "12": 8
          },
          "num_years_sampled": 11
        },
        "midterm_year": {
          "avg_return_pct_by_month": {
            "1": -0.28,
            "2": 0.62,
            "3": 1.23,
            "4": -0.67,
            "5": 0.46,
            "6": -1.68,
            "7": -0.63,
            "8": -2.08,
            "9": -1.38,
            "10": 2.68,
            "11": 3.69,
            "12": -0.98
          },
          "rank_by_month": {
            "1": 6,
            "2": 4,
            "3": 3,
            "4": 8,
            "5": 5,
            "6": 11,
            "7": 7,
            "8": 12,
            "9": 10,
            "10": 2,
            "11": 1,
            "12": 9
          },
          "num_years_sampled": 11
        },
        "pre_election_year": {
          "avg_return_pct_by_month": {
            "1": 5.89,
            "2": 2.6,
            "3": 2.67,
            "4": 2.66,
            "5": 1.5,
            "6": 2.45,
            "7": 2.65,
            "8": 0.33,
            "9": -1.18,
            "10": 1.85,
            "11": 1.4,
            "12": 4.99
          },
          "rank_by_month": {
            "1": 1,
            "2": 6,
            "3": 3,
            "4": 4,
            "5": 9,
            "6": 7,
            "7": 5,
            "8": 11,
            "9": 12,
            "10": 8,
            "11": 10,
            "12": 2
          },
          "num_years_sampled": 10
        }
      },
      "data_start": "1985-02-01",
      "data_end": "2026-07-01",
      "num_years_total": 42
    },
    "Russell 2000 / IWM": {
      "monthly_avg_return_pct": {
        "1": 0.74,
        "2": 1.01,
        "3": 0.41,
        "4": 1.24,
        "5": 1.38,
        "6": 0.8,
        "7": 0.47,
        "8": -0.36,
        "9": -0.43,
        "10": -0.54,
        "11": 2.24,
        "12": 2.38
      },
      "monthly_rank": {
        "1": 7,
        "2": 5,
        "3": 9,
        "4": 4,
        "5": 3,
        "6": 6,
        "7": 8,
        "8": 10,
        "9": 11,
        "10": 12,
        "11": 2,
        "12": 1
      },
      "by_cycle_phase": {
        "election_year": {
          "avg_return_pct_by_month": {
            "1": -0.15,
            "2": 2.72,
            "3": -1.13,
            "4": 0.3,
            "5": 0.92,
            "6": 0.96,
            "7": 0.44,
            "8": 1.89,
            "9": 0.28,
            "10": -2.99,
            "11": 3.46,
            "12": 3.24
          },
          "rank_by_month": {
            "1": 10,
            "2": 3,
            "3": 11,
            "4": 8,
            "5": 6,
            "6": 5,
            "7": 7,
            "8": 4,
            "9": 9,
            "10": 12,
            "11": 1,
            "12": 2
          },
          "num_years_sampled": 10
        },
        "post_election_year": {
          "avg_return_pct_by_month": {
            "1": 1.33,
            "2": -1.84,
            "3": -0.07,
            "4": 1.91,
            "5": 3.81,
            "6": 2.02,
            "7": 2.62,
            "8": 1.03,
            "9": 1.44,
            "10": -0.32,
            "11": 1.49,
            "12": 2.09
          },
          "rank_by_month": {
            "1": 8,
            "2": 12,
            "3": 10,
            "4": 5,
            "5": 1,
            "6": 4,
            "7": 2,
            "8": 9,
            "9": 7,
            "10": 11,
            "11": 6,
            "12": 3
          },
          "num_years_sampled": 10
        },
        "midterm_year": {
          "avg_return_pct_by_month": {
            "1": -0.8,
            "2": 1.35,
            "3": 1.92,
            "4": 0.31,
            "5": -0.69,
            "6": -1.48,
            "7": -1.9,
            "8": -2.87,
            "9": -1.65,
            "10": 1.86,
            "11": 2.95,
            "12": -0.16
          },
          "rank_by_month": {
            "1": 8,
            "2": 4,
            "3": 2,
            "4": 5,
            "5": 7,
            "6": 9,
            "7": 11,
            "8": 12,
            "9": 10,
            "10": 3,
            "11": 1,
            "12": 6
          },
          "num_years_sampled": 10
        },
        "pre_election_year": {
          "avg_return_pct_by_month": {
            "1": 2.77,
            "2": 1.91,
            "3": 0.97,
            "4": 2.58,
            "5": 1.47,
            "6": 1.81,
            "7": 0.76,
            "8": -1.89,
            "9": -2.09,
            "10": -0.49,
            "11": 1.15,
            "12": 4.08
          },
          "rank_by_month": {
            "1": 2,
            "2": 4,
            "3": 8,
            "4": 3,
            "5": 6,
            "6": 5,
            "7": 9,
            "8": 11,
            "9": 12,
            "10": 10,
            "11": 7,
            "12": 1
          },
          "num_years_sampled": 10
        }
      },
      "data_start": "1987-10-01",
      "data_end": "2026-07-01",
      "num_years_total": 40
    }
  }
}

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