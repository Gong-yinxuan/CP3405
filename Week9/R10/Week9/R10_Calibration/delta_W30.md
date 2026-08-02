# Delta Report — vW29

**Forecast week:** 2026-07-21 to 2026-07-25  
**Final market close used:** Friday 24 July 2026  
**Prepared by:** R10 Calibration / Product Analyst

> The repository's `prism/data/output.json` was still dated 17 July when this report was prepared. Therefore, this report uses externally verified 24 July closes. It should be replaced by the automated repository snapshot if R6/R9 later commit a valid 24 July output.

## Calibration Summary

- **Direction accuracy:** 55.6% — 5/9
- **Range accuracy:** 33.3% — 3/9
- **Mean absolute midpoint error:** 2.02 percentage points
- **Sector leader match:** 0/2
- **Sector laggard match:** 1/2

## Asset Results

| Asset | Prediction | Predicted range | Actual % | Direction correct? | Range hit? | Error (pp) |
|---|---|---:|---:|---|---|---:|
| SPX | Up | +0.8% to +2.0% | -0.6% | No | No | 2.00 |
| NDX | Flat/Up | -0.2% to +0.8% | -0.8% | No | No | 1.10 |
| IWM | Up | +0.3% to +1.2% | -1.0% | No | No | 1.75 |
| GOLD | Down | -2.0% to +0.5% | +1.2% | No | No | 1.95 |
| WTI | Up | +2.0% to +5.0% | +9.2% | Yes | No | 5.70 |
| US10Y | Up | +1.0% to +3.0% | +4.2% | Yes | No | 2.20 |
| TLT | Down | -2.5% to +0.0% | -1.5% | Yes | Yes | 0.25 |
| VIX | Flat/Up | -2.0% to +5.0% | -1.0% | Yes | Yes | 2.50 |
| BTC | Flat | -4.0% to +4.0% | +0.7% | Yes | Yes | 0.70 |

## Sector Outcome

| Rank | Sector ETF | Actual weekly change | Assessment |
|---:|---|---:|---|
| 1 | XLE | +3.4% | Not explicitly ranked |
| 2 | XLU | +2.5% | Not explicitly ranked |
| 3 | XLI | +1.8% | Not explicitly ranked |
| 4 | XLB | +1.4% | Not explicitly ranked |
| 5 | XLRE | +1.2% | Not explicitly ranked |
| 6 | XLV | +0.9% | Predicted laggard |
| 7 | XLK | +0.2% | Not explicitly ranked |
| 8 | XLF | +0.1% | Predicted leader |
| 9 | XLP | -1.2% | Predicted laggard |
| 10 | XLC | -3.9% | Predicted leader |
| 11 | XLY | -5.2% | Not explicitly ranked |

**Actual leaders:** XLE (+3.4%), XLU (+2.5%), XLI (+1.8%).  
**Actual laggards:** XLY (-5.2%), XLC (-3.9%), XLP (-1.2%).

## R10 Findings

1. The bullish broad-market call failed: SPX, NDX and IWM all declined.
2. The strongest correct call was WTI direction, but its +9.2% move was far above the predicted range.
3. TLT, VIX and BTC were the only three complete range hits.
4. XLC was forecast as a leader but became the second-worst sector.
5. XLP was correctly identified as a laggard; XLV was not.

## Calibration Action

- Reduce confidence when a forecast depends on pre-event positioning rather than confirmed price action.
- Add a correlated-risk penalty when SPX, NDX and IWM all share the same bullish thesis.
- Use a wider volatility-adjusted range for WTI and VIX.
- Require a valid actuals date before calibration is added to cumulative history.
- Store all 11 sector predictions explicitly; leader/laggard labels alone are insufficient for full sector accuracy scoring.

## R10 Conclusion

The vW29 forecast achieved **55.6% directional accuracy**, **33.3% range accuracy**, and **2.02 percentage points mean absolute error** across nine explicitly predicted assets. The main weakness was excessive bullish confidence in equities and an underestimation of oil volatility.
