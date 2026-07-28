# R10 Cumulative Accuracy Dashboard — Corrected through vW28

## Weekly History

| Release | Forecast week | Direction accuracy | Correct / Total | Range accuracy | Range hits | Mean absolute error |
|---|---|---:|---:|---:|---:|---:|
| vW23 | Week 3 | 25.0% | 2/8 | 12.5% | 1/8 | 6.34 pp |
| vW25 | 2026-06-22 to 2026-06-26 | 66.7% | 6/9 | 44.4% | 4/9 | 3.01 pp |
| vW28 | 2026-07-13 to 2026-07-17 | 50.0% | 10/20 | 40.0% | 8/20 | 3.72 pp |

## Cumulative Metrics

### Equal-release average

- Average direction accuracy: **47.2%**
- Average range accuracy: **32.3%**
- Average error: **4.36 percentage points**

### Asset-weighted cumulative result

- Direction accuracy: **48.6%** — 18/37
- Range accuracy: **35.1%** — 13/37
- Mean absolute error: **4.11 percentage points**

## Trend Assessment

- Direction accuracy improved sharply from vW23 to vW25, then fell to 50.0% in vW28.
- vW28 exposed concentration risk: the bullish SPX/NDX/XLK view failed together.
- Range accuracy remains weaker than directional accuracy.
- The largest calibration error came from VIX, followed by WTI and XLK.
- Historical metrics must only be updated after actuals-date validation passes.

## Dashboard Decision

Use the **asset-weighted metric** as the primary cumulative measure because each release scored a different number of assets. Keep the equal-release average as a secondary continuity measure.
