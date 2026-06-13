# Acceptance Criteria — W04 / vW24

## Product Increment Criteria

| Criterion | Accept / Reject | Evidence |
|---|---|---|
| At least one automated market-data fetch step exists | Accept, with live verification recommended | `w3_delta_report.md` documents Yahoo Finance collection and JSON output. |
| The output is structured | Accept | JSON schema is documented for SPY, QQQ, IWM, XLK, XLU, XLV. |
| The increment supports future automation | Accept | The field names and date format are documented for later agent and delta-engine use. |
| The team can explain why this was automated first | Accept | `DECISION.md` explains the Product Owner rationale. |

## Prediction Criteria

| Criterion | Accept / Reject | Evidence |
|---|---|---|
| SPX prediction included | Accept | Updated `prediction.md`. |
| NDX prediction included | Accept | Updated `prediction.md`. |
| IWM prediction included | Accept | Updated `prediction.md`. |
| At least 3 S&P sectors included | Accept | Updated R1/R3 files cover XLB, XLF, XLV, XLK, XLE, XLU, XLC and more. |
| Leading and lagging sectors identified | Accept | Leading: XLB / XLF. Lagging: XLC / XLK. |
| Evidence folder supports the call | Accept | Midweek and Friday evidence logs and screenshots are referenced. |

## Quality Criteria

| Criterion | Status | Required action |
|---|---|---|
| R1 Product Owner complete | Done | Use `product_owner.md`. |
| R3 Almanac complete | Done | Use `almanac.md`. |
| R4 Macro complete | Not done in current repo view | Fill `R4_macro/macro_agent_W04.md`. |
| R5 Technical complete | Done | Existing `R5_technical/technical_agent_W04.md`. |
| R7 Human Score complete | Not done in current repo view | Fill `human_score_W04.md`. |
| R8 LLM synthesis complete | Not done in current repo view | Fill `llm_synthesis.md` and save raw prompts/responses. |

## Product Owner final acceptance

The W04 package is acceptable for R1/R3 after these changes because it now matches the uploaded evidence. The final call is neutral-bullish with medium confidence, not the earlier bearish-neutral draft.
