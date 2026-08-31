You are acting as an advanced Multi-LLM Consensus Synthesis Engine for CP3405 DT3 Market Intelligence.
Your task is to evaluate three independent retrospective analysis legs, cross-reference them with live internet research, and deliver a forward-looking Weekly Prediction Brief.

1. LOCAL SOURCE DATA PAYLOADS (Retrospective Pipeline Ingestion)
[TECHNICAL INDICATOR AGENT DATA]:
{
  "generated_at": "2026-08-31T04:06:23Z",
  "collector": "Technical Collector",
  "agent_input_for": "Technical Agent",
  "data_source": "Yahoo Finance via yfinance",
  "note": "This collector automates EMA, momentum, and support/resistance candidate data. Manual chart trendlines and annotated screenshots are not automated yet.",
  "instruments": {
    "SPX": {
      "symbol": "SPX",
      "yahoo_ticker": "^GSPC",
      "name": "S&P 500 Index",
      "latest_trading_date": "2026-08-28",
      "last_close": 7711.76,
      "weekly_change_pct": 0.49,
      "ema_8": 7697.72,
      "ema_21": 7668.78,
      "price_vs_8ema": "above",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": 14.04,
      "distance_from_21ema": 42.98,
      "ema_gap": 28.94,
      "ema_condition": "Zone 1 Bullish",
      "recent_20d_high": 7816.7,
      "recent_20d_low": 7504.78,
      "resistance_candidate": 7816.7,
      "support_candidate": 7504.78,
      "technical_bias": "Bullish",
      "history_file": "technical/history/SPX.json"
    },
    "NDX": {
      "symbol": "NDX",
      "yahoo_ticker": "^NDX",
      "name": "Nasdaq 100 Index",
      "latest_trading_date": "2026-08-28",
      "last_close": 29433.43,
      "weekly_change_pct": 0.43,
      "ema_8": 29398.36,
      "ema_21": 29343.81,
      "price_vs_8ema": "above",
      "ema_8_vs_21ema": "above",
      "distance_from_8ema": 35.07,
      "distance_from_21ema": 89.62,
      "ema_gap": 54.55,
      "ema_condition": "Zone 1 Bullish",
      "recent_20d_high": 30195.72,
      "recent_20d_low": 28196.88,
      "resistance_candidate": 30195.72,
      "support_candidate": 28196.88,
      "technical_bias": "Bullish",
      "history_file": "technical/history/NDX.json"
    },
    "IWM": {
      "symbol": "IWM",
      "yahoo_ticker": "IWM",
      "name": "Russell 2000 ETF Proxy",
      "latest_trading_date": "2026-08-28",
      "last_close": 295.75,
      "weekly_change_pct": -1.4,
      "ema_8": 298.81,
      "ema_21": 298.81,
      "price_vs_8ema": "below",
      "ema_8_vs_21ema": "equal",
      "distance_from_8ema": -3.06,
      "distance_from_21ema": -3.06,
      "ema_gap": 0.0,
      "ema_condition": "Mixed / Neutral",
      "recent_20d_high": 305.18,
      "recent_20d_low": 292.4,
      "resistance_candidate": 305.18,
      "support_candidate": 292.4,
      "technical_bias": "Neutral",
      "history_file": "technical/history/IWM.json"
    }
  }
}

[ALMANAC & HISTORICAL SEASONALITY AGENT DATA]:
{
  "generated_at": "2026-08-31T04:06:30Z",
  "collector": "Almanac Collector",
  "agent_input_for": "Almanac Agent",
  "data_source": "Yahoo Finance via yfinance + automatic date rules",
  "note": "This collector automates calendar flags and sector ranking. It does not manually interpret seasonal patterns or news.",
  "forecast_window": {
    "generated_from_date_utc": "2026-08-31",
    "start": "2026-09-07",
    "end": "2026-09-11"
  },
  "calendar_flags": {
    "month": "September",
    "june_seasonal_weakness_flag": false,
    "midterm_year_flag": true,
    "options_expiry_date": "2026-09-18",
    "options_expiry_week_flag": false,
    "market_holiday_in_window_flag": false,
    "compressed_trading_week_flag": false,
    "holidays_in_window": []
  },
  "sector_weekly_performance": {
    "XLK": {
      "ticker": "XLK",
      "sector": "Technology",
      "latest_trading_date": "2026-08-28",
      "close": 185.69,
      "weekly_change_pct": 1.3,
      "history_file": "almanac/sector_history/XLK.json"
    },
    "XLF": {
      "ticker": "XLF",
      "sector": "Financials",
      "latest_trading_date": "2026-08-28",
      "close": 58.1,
      "weekly_change_pct": 1.08,
      "history_file": "almanac/sector_history/XLF.json"
    },
    "XLV": {
      "ticker": "XLV",
      "sector": "Healthcare",
      "latest_trading_date": "2026-08-28",
      "close": 171.16,
      "weekly_change_pct": -1.98,
      "history_file": "almanac/sector_history/XLV.json"
    },
    "XLE": {
      "ticker": "XLE",
      "sector": "Energy",
      "latest_trading_date": "2026-08-28",
      "close": 62.68,
      "weekly_change_pct": -1.51,
      "history_file": "almanac/sector_history/XLE.json"
    },
    "XLB": {
      "ticker": "XLB",
      "sector": "Materials",
      "latest_trading_date": "2026-08-28",
      "close": 53.18,
      "weekly_change_pct": -0.67,
      "history_file": "almanac/sector_history/XLB.json"
    },
    "XLI": {
      "ticker": "XLI",
      "sector": "Industrials",
      "latest_trading_date": "2026-08-28",
      "close": 177.14,
      "weekly_change_pct": -1.73,
      "history_file": "almanac/sector_history/XLI.json"
    },
    "XLY": {
      "ticker": "XLY",
      "sector": "Consumer Discretionary",
      "latest_trading_date": "2026-08-28",
      "close": 117.21,
      "weekly_change_pct": -0.69,
      "history_file": "almanac/sector_history/XLY.json"
    },
    "XLP": {
      "ticker": "XLP",
      "sector": "Consumer Staples",
      "latest_trading_date": "2026-08-28",
      "close": 85.45,
      "weekly_change_pct": -0.63,
      "history_file": "almanac/sector_history/XLP.json"
    },
    "XLU": {
      "ticker": "XLU",
      "sector": "Utilities",
      "latest_trading_date": "2026-08-28",
      "close": 42.73,
      "weekly_change_pct": -0.09,
      "history_file": "almanac/sector_history/XLU.json"
    },
    "XLC": {
      "ticker": "XLC",
      "sector": "Communication Services",
      "latest_trading_date": "2026-08-28",
      "close": 112.99,
      "weekly_change_pct": 1.43,
      "history_file": "almanac/sector_history/XLC.json"
    },
    "XLRE": {
      "ticker": "XLRE",
      "sector": "Real Estate",
      "latest_trading_date": "2026-08-28",
      "close": 44.48,
      "weekly_change_pct": -1.33,
      "history_file": "almanac/sector_history/XLRE.json"
    }
  },
  "sector_ranking": {
    "leading_sectors": [
      {
        "ticker": "XLC",
        "sector": "Communication Services",
        "weekly_change_pct": 1.43
      },
      {
        "ticker": "XLK",
        "sector": "Technology",
        "weekly_change_pct": 1.3
      },
      {
        "ticker": "XLF",
        "sector": "Financials",
        "weekly_change_pct": 1.08
      }
    ],
    "lagging_sectors": [
      {
        "ticker": "XLV",
        "sector": "Healthcare",
        "weekly_change_pct": -1.98
      },
      {
        "ticker": "XLI",
        "sector": "Industrials",
        "weekly_change_pct": -1.73
      },
      {
        "ticker": "XLE",
        "sector": "Energy",
        "weekly_change_pct": -1.51
      }
    ]
  }
}
{
  "generated_at": "2026-08-01T03:19:10Z",
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
            "7": 0.56,
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
        "7": 1.61,
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
            "7": 1.69,
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
        "7": 1.22,
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
            "7": -0.74,
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
            "4": 7,
            "5": 5,
            "6": 11,
            "7": 8,
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
        "7": 0.45,
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
            "7": -2.0,
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

[PIPELINE ECONOMIC CALENDAR CAPTURE]:
{
  "week_commencing": "2026-08-31",
  "week_ending": "2026-09-06",
  "fed_speakers": [
    {
      "speaker_hint": "Warsh",
      "title": "Warsh, In Our Time",
      "published_at": "2026-08-28T14:00:00+00:00",
      "source_url": "https://www.federalreserve.gov/newsevents/speech/warsh20260828a.htm",
      "summary": "Speech At \u201cFinancial Innovation: Implications for Payments and Policy,\u201d an economic policy symposium sponsored by the Federal Reserve Bank of Kansas City, Jackson Hole, Wyoming",
      "tone_hint": "neutral_or_unclear_keyword_hint",
      "r4_note": "Keyword hint only. R4 should verify the actual Fed speaker message."
    }
  ],
  "fed_speaker_count": 1,
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

2. MANDATORY INDEPENDENT REAL-TIME RESEARCH INSTRUCTIONS
Our local economic macro data collectors may have missed critical market events, unscheduled central bank updates, or breaking macroeconomic catalysts. 
YOU ARE EXPLICITLY ORDERED TO USE YOUR WEB-SEARCH, LIVE-RETRIEVAL, AND PARAMETRIC KNOWLEDGE INFRASTRUCTURE TO PERFORM AN INDEPENDENT AUDIT OF CURRENT LIVE SECTORS AND EVENTS:
- Research current breaking macroeconomic catalysts, geopolitical shifts, or sudden volatility vectors affecting broad market indices (SPX, NDX, IWM) for the upcoming tracking week.
- Cross-reference the 'PIPELINE ECONOMIC CALENDAR CAPTURE' against actual public economic calendars to identify high-importance missing events (e.g., unscheduled central bank speeches, flash PMI data, emergency updates, or unexpected global inventory revisions).
- Identify current consensus estimates for any major upcoming indicators to evaluate trend acceleration or trend exhaustion conditions.

3. YOUR REQUIRED EVALUATION OUTPUT FORMAT
Provide a punchy, highly structured synthesis detailing your findings. 

Rules for Synthesis Compilation:
- Do not invent past historical price metrics.
- INTEGRATE YOUR INDEPENDENT RESEARCH FINDINGS directly into your index outlooks and regime evaluations to enhance accuracy beyond our local data collectors.
- Explicitly log any discovered data collection gaps, omitted events, or missed macroeconomic parameters inside the dedicated 'pipeline_omissions_discovered' array key so we can update our collectors.

Output strictly as valid, clean JSON matching the target keys below. No markdown wrappers.
{
"weekly_regime": "text description detailing expected market regime, incorporating both pipeline telemetry and your independent live research discoveries",
"confidence_score": "High, Medium, or Low",
"spx_pct_estimate": "Estimated percentage range",
"ndx_pct_estimate": "Estimated percentage range",
"iwm_pct_estimate": "Estimated percentage range",
"top_supporting_reason": "Single strong statement detailing your top core macro/technical catalyst trigger discovered",
"top_contradiction_cited": "The primary scheduled risk or discovered missing calendar anomaly that could break this trend",
"invalidation_condition": "Specific closing level or yield target breaker level",
"tone_caveat_language": "Short description of target exposure alignment based on the complete risk calendar",
"consensus_bias": "BULLISH / BEARISH / NEUTRAL / MIXED",
"consensus_read_summary": "A 2-3 sentence paragraph summarizing model alignment, agreements, and specific missing market developments highlighted via your independent live search...",
"point_of_maximum_divergence": "The single biggest disagreement point between aggressive and defensive views regarding upcoming event impacts...",
"key_supporting_factors": ["Live factor from local data", "Macro driver or missed calendar event surfaced via independent search"],
"main_contradiction_risk": "The top structural risk moving against the consensus trend this week...",
"invalidation_summary": "The exact parameter or support level that breaks this consensus view...",
"pipeline_omissions_discovered": ["List specific high-importance calendar events, indicators, central bank releases, or macro data points missed by our local macro/technical collectors that you discovered via real-time research"],
"r7_human_score_question": "A critical evaluation question helping the human team weigh the conflicting data legs against discovered external elements...",
"r6_slide_bullet_1": "Core slide takeaway bullet 1 incorporating live research context...",
"r6_slide_bullet_2": "Core slide takeaway bullet 2 incorporating live research context...",
"r6_slide_bullet_3": "Core slide takeaway bullet 3 incorporating live research context..."
}