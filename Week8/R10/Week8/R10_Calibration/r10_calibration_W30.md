# R10 Calibration — Week 8 Completion

**Role:** R10 Product Analyst / Calibration  
**Release scored:** vW29  
**Forecast week:** 21–25 July 2026  
**Final market close:** 24 July 2026

## Required Work Completed

- Retrieved the final available market closes for the forecast week.
- Compared the vW29 prediction against actual outcomes.
- Scored direction, range and midpoint error for all nine explicitly predicted assets.
- Ranked all 11 S&P sector ETFs.
- Updated cumulative accuracy through vW29.
- Documented the key calibration improvement for the next sprint.

## Final vW29 Result

- Direction accuracy: **55.6% — 5/9**
- Range accuracy: **33.3% — 3/9**
- Mean absolute error: **2.02 pp**
- Predicted sector leaders matched actual top three: **0/2**
- Predicted sector laggards matched actual bottom three: **1/2**

## Data Integrity Status

The GitHub repository's `prism/data/output.json` remained dated 17 July rather than 24 July. R10 therefore used externally verified final closes and marked the actuals file accordingly. The score should be rerun automatically if a valid 24 July repository output is later committed.

## Main Learning

The team overestimated broad equity strength and underestimated event-driven dispersion. The next calibration should reduce correlated bullish confidence and require explicit predictions for every sector so all 11 sectors can be scored consistently.
