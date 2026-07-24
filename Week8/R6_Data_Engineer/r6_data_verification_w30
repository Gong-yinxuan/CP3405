# R6 Data Engineer — Automation Verification (Sprint 8 / W30)
**Role:** R6 Data Engineer
**Verification date:** 24 July 2026
**Scheduled run checked:** Update Market Data (Friday actuals collector, targeting 2026-07-24 close)

## 1. Eleven-Sector Coverage
The collector (`prism/src/data_collector.py`) still maps all 11 required S&P 500 sector ETFs, unchanged since Week 7:

| Sector | ETF | Present in collector | Present in latest output (2026-07-17) |
|---|---|---|---|
| Technology | XLK | Yes | Yes |
| Health Care | XLV | Yes | Yes |
| Financials | XLF | Yes | Yes |
| Consumer Discretionary | XLY | Yes | Yes |
| Communication Services | XLC | Yes | Yes |
| Industrials | XLI | Yes | Yes |
| Consumer Staples | XLP | Yes | Yes |
| Energy | XLE | Yes | Yes |
| Materials | XLB | Yes | Yes |
| Real Estate | XLRE | Yes | Yes |
| Utilities | XLU | Yes | Yes |

**Coverage result:** 11/11 sector ETFs. No regression from Week 7.

## 2. Automation Verification
The workflow schedule is unchanged:
```yaml
- cron: "0 22 * * 5"
```
Friday 22:00 UTC, i.e. Saturday 06:00 Singapore time, after the US Friday close.

As of this verification (24 July 2026, 11:08 SGT — before the 22:00 UTC trigger), the repository's `prism/data/output.json` is still dated **2026-07-17**, i.e. the artefact produced by last week's run (Update Market Data #69, verified in the Week 7 report). This week's actuals-collection run, which will produce the 2026-07-24 snapshot, had **not yet fired** at the time of writing.

This report therefore verifies collector readiness ahead of tonight's run rather than a completed run. A follow-up check after 06:00 SGT on 25 July is needed to confirm:
- the run triggered on schedule;
- the run completed with **Success**;
- `prism/data/output.json` updates to `"date": "2026-07-24"`.

The separate Monday cron (`0 0 * * 1`, R3/R4/R5 collectors) already executed successfully this sprint — `Week8/R3_almanac`, `Week8/R4_macro`, and `Week8/R5_technical` all contain populated reports for W30, confirming the collector/report-builder chain is healthy on that side of the pipeline.

## 3. Schema Validation
`prism/data/output.json` (still the 2026-07-17 snapshot) continues to validate against the required schema:
- one `date` field in `YYYY-MM-DD` format;
- three core index assets: SPX, NDX and IWM;
- all 11 sector ETFs;
- six supporting assets: GOLD, WTI, US10Y, TLT, VIX and BTC;
- a numeric `close` and `weekly_change_pct` for every asset.

**Schema result:** Complete. No changes needed for tonight's run to produce a valid file, assuming the collector code path is unchanged.

## 4. Important Defect Found — Week 7 Fix Not Yet Deployed
Week 7 flagged that the calibration runner reused a stale `vW28_actuals.json` (dated 2026-07-10) instead of refreshing it with the correct 2026-07-17 output, and reported that a corrected runner with date-integrity validation was supplied to fix this.

Re-checking the live pipeline this sprint:
- The corrected version (`Week7/R10/prism/src/calibration_runner.py`) does contain the forecast-end-date validation and snapshot-refresh logic as described.
- **However, this fix has not been merged into the file the workflow actually runs**, `prism/src/calibration_runner.py`. That file still contains the original logic: *"Only create a new actuals snapshot if it does not exist yet"* — it never overwrites an existing snapshot.
- Consequently, `prism/data/actuals/vW28_actuals.json` is **still dated 2026-07-10**, while `vW28_prediction.json` has a `forecast_week` of `2026-07-13 to 2026-07-17` (expected actuals date 2026-07-17).
- `prism/data/calibration/accuracy_history.json` still records the same **85.0% direction accuracy** for vW28 that Week 7 flagged as computed against the wrong actuals week — it has not been recalculated.

Therefore:
- R6 collection remains healthy (sector coverage and schema are both correct);
- the downstream calibration defect identified in Week 7 is **still live in production**, because the fix was written but never merged into `prism/src/calibration_runner.py`;
- if tonight's 22:00 UTC run proceeds without this merge, the same stale-actuals problem will very likely recur for whichever release is scored next.

**Recommended action before tonight's run:** replace `prism/src/calibration_runner.py` with the corrected version from `Week7/R10/prism/src/calibration_runner.py` (or port its `forecast_end_date()` / date-integrity logic into the production file), then re-run the calibration step once the 2026-07-24 output lands so vW28 (and any newer release) is scored against the correct actuals.

## 5. R6 Final Status
| Requirement | Result |
|---|---|
| Collector covers all 11 sector ETFs | Complete |
| Friday post-close cron configured | Complete |
| Scheduled run for this week occurred | Pending — scheduled for 22:00 UTC tonight, not yet fired as of verification |
| Scheduled run successful | Not yet verifiable |
| JSON contains all required assets | Complete (on last available snapshot, 2026-07-17) |
| Numeric schema valid | Complete |
| Downstream date integrity | **Not fixed** — corrected runner exists but was not merged into production |

**R6 conclusion:** Data collection code is unchanged and remains correct — 11/11 sector coverage and full schema validity hold. The open item carried over from Week 7 is not collector reliability but deployment discipline: the actuals-date integrity fix was written last sprint but never merged into the file the workflow actually executes, so the stale-snapshot defect is still active in production. This should be merged before tonight's scheduled run, and the run's outcome (status, duration, resulting `output.json` date) should be confirmed once it fires.

