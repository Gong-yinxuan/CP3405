# Accuracy History — W23 to W28

| Release | Week | Forecast week | Direction accuracy | Correct / Total | Range accuracy | Range hits | Average error % |
|---|---|---|---:|---:|---:|---:|---:|
| vW23 | W23 | Week 3 | 25.0% | 2/8 | 12.5% | 1/8 | 6.34% |
| vW25 | W25 | 2026-06-22 to 2026-06-26 | 66.7% | 6/9 | 44.4% | 4/9 | 3.01% |
| vW28 | W28 | 2026-07-13 to 2026-07-17 | 85.0% | 17/20 | 55.0% | 11/20 | 1.17% |

## Cumulative Summary

- Average direction accuracy: 58.9%
- Average range accuracy: 37.3%
- Average error size: 3.51%
- Calibration bias: R10 observed a slight large-cap bullish bias in the team’s forecast. The forecast was better at identifying direction than estimating the exact weekly percentage change.
- Improvement: For the next sprint, the team should create and commit `vWxx_prediction.json` before the forecast week begins. This will give R10 a clean sealed prediction to score after Friday close and avoid needing to reconstruct predictions later.
