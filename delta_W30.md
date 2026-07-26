# Delta Report — vW30

**Week:** W30
**Forecast week:** 2026-07-20 to 2026-07-24
**Generated at:** 2026-07-26 08:47:11
**Actuals source:** `prism/data/actuals/vW30_actuals.json`

## Summary

- Direction accuracy: 60.0%
- Correct directions: 12 out of 20
- Range accuracy: 40.0%
- Range hits: 8 out of 20
- Average error size: 2.09%

## Asset Results

| Asset | Prediction | Expected % | Range % | Actual direction | Actual % | Direction correct? | Range hit? | Error % | Bias |
|---|---|---:|---:|---|---:|---|---|---:|---|
| SPX | Neutral | -0.3 | -1.0 to 0.5 | Down | -0.6 | Yes | Yes | 0.3 | Well calibrated |
| NDX | Down | -1.5 | -2.5 to -0.5 | Down | -1.6 | Yes | Yes | 0.1 | Well calibrated |
| IWM | Neutral | 0.0 | -1.0 to 1.0 | Down | -1.0 | Yes | Yes | 1.0 | Too bullish |
| XLK | Down | -1.2 | -2.5 to 0.0 | Up | 0.2 | No | No | 1.4 | Too bearish |
| XLE | Up | 2.5 | 0.5 to 4.0 | Up | 3.4 | Yes | Yes | 0.9 | Too bearish |
| XLV | Neutral | 0.0 | -1.0 to 0.8 | Up | 0.9 | No | No | 0.9 | Too bearish |
| XLF | Neutral | 0.2 | -0.8 to 1.2 | Up | 0.1 | Yes | Yes | 0.1 | Well calibrated |
| XLC | Down | -1.0 | -2.0 to 0.2 | Down | -3.9 | Yes | No | 2.9 | Too bullish |
| XLP | Neutral | 0.2 | -0.5 to 0.8 | Down | -1.2 | No | No | 1.4 | Too bullish |
| XLU | Down | -0.5 | -1.2 to 0.3 | Up | 2.5 | No | No | 3.0 | Too bearish |
| XLRE | Down | -1.0 | -2.0 to 0.0 | Up | 1.2 | No | No | 2.2 | Too bearish |
| XLB | Down | -0.8 | -1.8 to 0.2 | Up | 1.4 | No | No | 2.2 | Too bearish |
| XLI | Down | -0.7 | -1.5 to 0.2 | Up | 1.8 | No | No | 2.5 | Too bearish |
| XLY | Down | -0.8 | -1.8 to 0.2 | Down | -5.2 | Yes | No | 4.4 | Too bullish |
| WTI | Up | 2.5 | 0.5 to 4.5 | Up | 9.7 | Yes | No | 7.2 | Too bearish |
| GOLD | Neutral | 0.5 | -0.5 to 2.0 | Up | 1.1 | Yes | Yes | 0.6 | Too bearish |
| US10Y | Up | 1.0 | 0.5 to 2.0 | Up | 4.4 | Yes | No | 3.4 | Too bearish |
| TLT | Down | -1.2 | -2.0 to 0.0 | Down | -1.5 | Yes | Yes | 0.3 | Well calibrated |
| VIX | Up | 5.0 | 2.0 to 8.0 | Down | -1.0 | No | No | 6.0 | Too bullish |
| BTC | Neutral | 0.0 | -4.0 to 4.0 | Down | -0.9 | Yes | Yes | 0.9 | Too bullish |

## R6/R10 Notes

- Largest error: WTI (7.2 percentage points)
- Main bias: Too bearish (6 too bullish vs 10 too bearish)
- Improvement: validate actuals date, reduce correlated confidence, and widen ranges for high-volatility assets.
