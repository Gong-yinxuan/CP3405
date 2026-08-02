# R10 Calibration Role — Final Sprint 7 Completion

**Role:** R10 Product Analyst / Calibration  
**Completion date:** 19 July 2026

## Work Completed

- Verified the successful Friday post-close automation run.
- Retrieved the definitive 17 July structured output.
- Detected that the repository calibration reused a stale 10 July snapshot.
- Rebuilt `vW28_actuals.json` using the correct 17 July data.
- Recalculated `delta_W28.md`.
- Updated cumulative metrics through vW28.
- Added a calibration-runner fix that validates actuals dates.

## Corrected vW28 Result

| Metric | Corrected result |
|---|---:|
| Direction accuracy | 50.0% — 10/20 |
| Range accuracy | 40.0% — 8/20 |
| Mean absolute error | 3.72 pp |
| Core-index direction | 33.3% — 1/3 |
| 11-sector direction | 63.6% — 7/11 |
| Largest error | VIX — 26.9 pp |
| Second-largest error | WTI — 13.5 pp |

## Why the Previous Result Was Wrong

The repository's generated `delta_W28.md` showed 85.0% direction accuracy because `calibration_runner.py` followed a “never overwrite actuals” rule. The existing snapshot was dated 10 July, although the prediction metadata stated 13–17 July.

The successful 17 July workflow updated `prism/data/output.json`, but R10 continued scoring against the old snapshot. The corrected result uses the output date that matches the forecast end date.

## Cumulative Accuracy through vW28

- Asset-weighted direction accuracy: **48.6% — 18/37**
- Asset-weighted range accuracy: **35.1% — 13/37**
- Asset-weighted mean absolute error: **4.11 pp**

## Calibration Learning

The largest weakness was a shared bullish exposure across SPX, NDX and XLK. The forecast also expected VIX to fall, but VIX rose 24.9%, and WTI rose much more than predicted. Future predictions should use a volatility-regime gate and reduce duplicated confidence across correlated assets.

## R10 Final Status

| Requirement | Result |
|---|---|
| Gather definitive Week 28 actuals | Complete — 17 July output |
| Compare Sprint 6 prediction with actuals | Complete |
| Calculate directional accuracy | Complete |
| Calculate range accuracy and error | Complete |
| Update cumulative history | Complete |
| Identify calibration improvement | Complete |
| Protect against stale actuals | Fixed in supplied runner |

**R10 conclusion:** Complete, with the corrected vW28 score replacing the stale-snapshot result.
