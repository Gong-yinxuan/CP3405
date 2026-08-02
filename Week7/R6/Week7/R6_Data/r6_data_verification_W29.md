# R6 Data Engineer — Final Automation Verification (Sprint 7)

**Role:** R6 Data Engineer  
**Verification date:** 19 July 2026  
**Scheduled run checked:** Update Market Data #69

## 1. Eleven-Sector Coverage

The repository collector contains all 11 required S&P 500 sector ETFs:

| Sector | ETF | Present in collector | Present in 17 July output |
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

**Coverage result:** 11/11 sector ETFs.

## 2. Automation Verification

The workflow schedule is:

```yaml
- cron: "0 22 * * 5"
```

This represents Friday 22:00 UTC, or Saturday 06:00 Singapore time, after the normal US Friday market close.

The scheduled run has now occurred:

- **Workflow:** Update Market Data #69
- **Trigger:** Schedule
- **Triggered:** 17 July 2026 at 22:42 UTC
- **Branch:** `main`
- **Status:** **Success**
- **Duration:** 46 seconds
- **Run URL:** https://github.com/Gong-yinxuan/CP3405/actions/runs/29618672719

The resulting `prism/data/output.json` is dated **2026-07-17**.

## 3. Schema Validation

The output contains:

- one `date` field in `YYYY-MM-DD` format;
- three core index assets: SPX, NDX and IWM;
- all 11 sector ETFs;
- six supporting assets: GOLD, WTI, US10Y, TLT, VIX and BTC;
- a numeric `close` and `weekly_change_pct` for every asset.

**Schema result:** Complete and suitable for downstream calibration.

## 4. Important Defect Found

The collector and scheduled workflow succeeded, but the calibration runner reused the existing `vW28_actuals.json` dated 2026-07-10. It did not replace that stale snapshot with the new 2026-07-17 output.

Therefore:

- R6 collection was successful;
- R10's automatically regenerated 85.0% score used the wrong actuals week;
- the calibration runner requires an actuals-date integrity check.

The corrected runner included in this package validates the snapshot date against the prediction's forecast end date and refreshes the latest release snapshot only when the output date matches.

## 5. R6 Final Status

| Requirement | Result |
|---|---|
| Collector covers all 11 sector ETFs | Complete |
| Friday post-close cron configured | Complete |
| Scheduled run occurred | Complete |
| Scheduled run successful | Complete |
| JSON contains all required assets | Complete |
| Numeric schema valid | Complete |
| Downstream date integrity | Fixed in supplied runner |

**R6 conclusion:** The data collection task is complete. The remaining issue was not Yahoo Finance connectivity or sector coverage; it was stale actuals reuse inside the downstream calibration step.
