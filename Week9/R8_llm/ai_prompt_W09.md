You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate and synthesize three independent analysis legs into a forward-looking Weekly Prediction Brief.

1. MASTER MARKET DATA (Verified by Data Pipeline)
[TECHNICAL INDICATOR AGENT DATA]: 
{
  "generated_at": "2026-07-12T12:08:17Z",
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
  "generated_at": "2026-07-12T12:08:18Z",
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
      "latest_trading_date": "2026-07-10",
      "close": 71.41,
      "weekly_change_pct": 3.96,
      "change_5d": 2.72,
      "direction_5d": "Up",
      "history_file": "macro/history/WTI.json"
    },
    "GOLD": {
      "symbol": "GOLD",
      "yahoo_ticker": "GC=F",
      "name": "Gold Futures",
      "category": "commodity",
      "latest_trading_date": "2026-07-10",
      "close": 4113.7002,
      "weekly_change_pct": 0.02,
      "change_5d": 1.0,
      "direction_5d": "Up",
      "history_file": "macro/history/GOLD.json"
    },
    "DXY": {
      "symbol": "DXY",
      "yahoo_ticker": "DX-Y.NYB",
      "name": "US Dollar Index",
      "category": "currency_index",
      "latest_trading_date": "2026-07-10",
      "close": 100.97,
      "weekly_change_pct": 0.11,
      "change_5d": 0.11,
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
      "latest_trading_date": "2026-07-12",
      "close": 63931.0703,
      "weekly_change_pct": 1.0,
      "change_5d": 633.6758,
      "direction_5d": "Up",
      "history_file": "macro/history/BTC.json"
    }
  },
  "fed_and_data_watch": {
    "week_commencing": "2026-07-06",
    "week_ending": "2026-07-12",
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
  "generated_at": "2026-07-12T12:08:20Z",
  "collector": "Almanac Collector",
  "agent_input_for": "Almanac Agent",
  "data_source": "Yahoo Finance via yfinance + automatic date rules",
  "note": "This collector automates calendar flags and sector ranking. It does not manually interpret seasonal patterns or news.",
  "forecast_window": {
    "generated_from_date_utc": "2026-07-12",
    "start": "2026-07-13",
    "end": "2026-07-17"
  },
  "calendar_flags": {
    "month": "July",
    "june_seasonal_weakness_flag": false,
    "midterm_year_flag": true,
    "options_expiry_date": "2026-07-17",
    "options_expiry_week_flag": true,
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
{
  "generated_at": "2026-07-12T12:08:16Z",
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
        "7": 1.44,
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
            "7": 0.66,
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
        "7": 1.62,
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
            "7": 1.72,
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
        "7": 1.31,
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
            "7": -0.42,
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
        "7": 0.49,
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
            "7": -1.85,
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