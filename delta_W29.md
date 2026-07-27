# Delta Report — vW29 (Team 05, manually reconstructed)
**Week:** W29
**Forecast week:** 2026-07-20 to 2026-07-24 (submission stated "2026-07-21 to 2026-07-25")
**Generated at:** 2026-07-27 (reconstructed — no automated delta was ever produced for this release)
**Prediction source:** Team 05 Weekly Prediction Submission, submitted 2026-07-19 14:48 SGT
**Actuals source:** `prism/data/output.json` (2026-07-24 snapshot) — same underlying data used as `vW30_actuals.json`

> **Note:** Unlike vW23/vW25/vW28/vW30, this release has no `delta_W29.json`/`.md` in `prism/data/calibration/` — it was never scored. Team 05's submission also gives direction + range only, not a single point forecast, so "Expected %" below is the **midpoint of their stated range**, and "Direction correct?" treats compound labels (e.g. "Flat/Up") as correct if the actual value is either positive or within ±1%. This is a reconstruction, not an output of `calibration_runner.py` — flagging so it isn't mistaken for an official run.

## Summary
- Direction accuracy: 55.6% (5 out of 9)
- Range accuracy: 33.3% (3 out of 9)
- Average error size: 2.19%
- No sector ETFs were individually forecast by the team (only qualitative leading/lagging sector calls — see below)

## Asset Results
| Asset | Prediction | Expected % (range midpoint) | Range % | Actual direction | Actual % | Direction correct? | Range hit? | Error % | Bias |
|---|---|---:|---:|---|---:|---|---|---:|---|
| SPX | Up | 1.4 | 0.8 to 2.0 | Down | -0.6 | No | No | 2.0 | Too bullish |
| NDX | Flat/Up | 0.3 | -0.2 to 0.8 | Down | -1.6 | No | No | 1.9 | Too bullish |
| IWM | Up | 0.75 | 0.3 to 1.2 | Down | -1.0 | No | No | 1.75 | Too bullish |
| GOLD | Down | -0.75 | -2.0 to 0.5 | Up | 1.1 | No | No | 1.85 | Too bearish |
| WTI | Up | 3.5 | 2.0 to 5.0 | Up | 9.7 | Yes | No | 6.2 | Too bearish (magnitude) |
| US10Y | Up | 2.0 | 1.0 to 3.0 | Up | 4.4 | Yes | No | 2.4 | Too bearish (magnitude) |
| TLT | Down | -1.25 | -2.5 to 0.0 | Down | -1.5 | Yes | Yes | 0.25 | Well calibrated |
| VIX | Flat/Up | 1.5 | -2.0 to 5.0 | Down (flat) | -1.0 | Yes (borderline) | Yes | 2.5 | Too bullish |
| BTC | Flat | 0.0 | -4.0 to 4.0 | Down (flat) | -0.9 | Yes | Yes | 0.9 | Too bearish (slight) |

## Sector Calls (qualitative — not part of the numeric table above)
| Call | Team 05 pick | Actual weekly change | Actual rank (of 11) | Verdict |
|---|---|---:|---|---|
| Leading sector | XLF, XLC | XLF +0.1%, XLC **-3.9%** | XLF 8th, XLC **10th** (2nd worst) | **Miss** — both picks were among the weakest sectors, not the strongest. XLE (+3.4%) was the actual leader. |
| Lagging sector | XLV, XLP | XLV +0.9%, XLP -1.2% | XLV 6th (mid-pack, positive), XLP 9th | **Mixed** — XLP was reasonably close (weak performer). XLV was wrong; it finished positive, not lagging. |

## R6/R10 Notes
- **Largest error:** WTI (6.2 percentage points) — direction was right, but the range badly underestimated the move (oil rose nearly 2x the top of the predicted range).
- **Main bias:** Too bullish (4 of 9) vs too bearish (4 of 9), roughly balanced — but the two biggest misses (SPX, sector leadership call) were both on the bullish side.
- **Process gap, not just accuracy gap:** this release was never run through `calibration_runner.py` at all. Combined with the vW28 stale-actuals bug already reported, that's two consecutive releases (vW28 and vW29) whose scores are either wrong or missing — vW30 is the first release this sprint with a clean, timely delta report.
- **Improvement:** same recommendation as before — merge the date-integrity fix into `prism/src/calibration_runner.py`, and additionally make sure every submitted release (including human/Team submissions, not just automated `vW*_prediction.json` releases) gets a delta report generated, so gaps like vW29 don't go unnoticed until someone manually reconstructs them.
