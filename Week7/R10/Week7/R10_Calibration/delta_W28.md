# Delta Report — vW28 (Corrected with 17 July Actuals)

**Forecast week:** 2026-07-13 to 2026-07-17  
**Actuals date:** 2026-07-17  
**Actuals source:** `prism/data/output.json` from scheduled GitHub Actions run #69, copied to `prism/data/actuals/vW28_actuals.json`  
**Automation run:** https://github.com/Gong-yinxuan/CP3405/actions/runs/29618672719  
**Run result:** Success — triggered 17 July 2026 at 22:42 UTC, duration 46 seconds

> **Integrity correction:** The repository's previous `vW28_actuals.json` was dated 2026-07-10. The calibration runner preserved that stale snapshot and therefore produced an 85.0% result against the wrong week. This corrected report uses the 2026-07-17 output that matches the prediction's stated forecast end date.

> **Prediction caveat:** `vW28_prediction.json` is marked as reconstructed from Sprint 6 evidence rather than an originally sealed prediction. The arithmetic below is correct for the stated week, but the result should still be described as reconstructed calibration evidence.

## Summary

- **Direction accuracy:** 50.0% — 10/20
- **Range accuracy:** 40.0% — 8/20
- **Mean absolute error:** 3.72 percentage points
- **Core indices:** 1/3 direction correct; 1/3 range hits; 2.8 pp mean error
- **11 sectors:** 7/11 direction correct (63.6%); 6/11 range hits (54.5%); 1.67 pp mean error
- **Macro/supporting assets:** 2/6 direction correct; 1/6 range hits; 7.92 pp mean error

## Asset Results

| Asset | Prediction | Expected % | Range % | Actual direction | Actual % | Direction correct? | Range hit? | Error % | Bias |
|---|---|---:|---:|---|---:|---|---|---:|---|
| SPX | Up | 1.0 | 0.5 to 1.5 | Down | -1.6 | No | No | 2.6 | Too bullish |
| NDX | Up | 1.2 | 0.5 to 1.8 | Down | -4.1 | No | No | 5.3 | Too bullish |
| IWM | Neutral | -0.2 | -0.8 to 0.5 | Down | -0.7 | Yes | Yes | 0.5 | Well calibrated |
| XLK | Up | 1.3 | 0.5 to 2.2 | Down | -5.5 | No | No | 6.8 | Too bullish |
| XLE | Up | 1.5 | 0.5 to 2.5 | Up | 4.7 | Yes | No | 3.2 | Too bearish |
| XLV | Up | 0.8 | 0.0 to 1.6 | Up | 0.2 | Yes | Yes | 0.6 | Too bullish |
| XLF | Up | 0.7 | 0.0 to 1.4 | Up | 1.0 | Yes | Yes | 0.3 | Well calibrated |
| XLC | Up | 0.6 | -0.2 to 1.4 | Down | -0.9 | No | No | 1.5 | Too bullish |
| XLP | Neutral | 0.1 | -0.5 to 0.7 | Up | 1.3 | No | No | 1.2 | Too bearish |
| XLU | Neutral | -0.2 | -0.9 to 0.4 | Down | -0.5 | Yes | Yes | 0.3 | Well calibrated |
| XLRE | Down | -0.6 | -1.4 to 0.1 | Up | 2.2 | No | No | 2.8 | Too bearish |
| XLB | Down | -0.7 | -1.6 to 0.1 | Down | -0.7 | Yes | Yes | 0.0 | Well calibrated |
| XLI | Down | -0.6 | -1.4 to 0.2 | Down | -1.4 | Yes | Yes | 0.8 | Too bullish |
| XLY | Down | -0.6 | -1.5 to 0.2 | Down | -1.5 | Yes | Yes | 0.9 | Too bullish |
| WTI | Up | 1.0 | 0.0 to 2.2 | Up | 14.5 | Yes | No | 13.5 | Too bearish |
| GOLD | Neutral | 0.0 | -0.8 to 0.8 | Down | -2.0 | No | No | 2.0 | Too bullish |
| US10Y | Up | 1.0 | 0.3 to 2.0 | Down | -2.2 | No | No | 3.2 | Too bullish |
| TLT | Down | -1.0 | -2.0 to 0.0 | Up | 0.1 | No | No | 1.1 | Too bearish |
| VIX | Down | -2.0 | -6.0 to 2.0 | Up | 24.9 | No | No | 26.9 | Too bearish |
| BTC | Up | 1.0 | -0.5 to 2.5 | Up | 0.2 | Yes | Yes | 0.8 | Too bullish |

## R10 Calibration Findings

- **Largest error:** VIX at 26.9 percentage points. The forecast expected Down but the actual weekly move was 24.9%.
- **Second-largest error:** WTI at 13.5 percentage points.
- **Bias counts:** 10 too bullish, 6 too bearish, and 4 well calibrated.
- **Main failure mode:** The forecast was too optimistic for large-cap growth and volatility. SPX, NDX and XLK fell, while VIX rose sharply. The model also severely underestimated WTI's move.
- **Best-calibrated calls:** IWM, XLF, XLU, XLB and BTC were close to the submitted ranges; XLE had the correct direction but an underestimated magnitude.

## Calibration Action for vW29

1. Seal the prediction JSON before any Friday actuals are available.
2. Require the actuals snapshot date to equal the forecast end date; fail the run on a mismatch.
3. Add a volatility-regime check using VIX and WTI before finalising directional confidence.
4. Reduce confidence when SPX/NDX/XLK are all exposed to the same growth-factor risk.
5. Keep direction accuracy, range accuracy and magnitude error as separate metrics.

## R10 Conclusion

Using the correct 17 July actuals, vW28 achieved **50.0% direction accuracy**, **40.0% range accuracy**, and **3.72 percentage points mean absolute error**. The earlier 85.0% figure was produced from a stale 10 July snapshot and should not be used as the final vW28 score.
