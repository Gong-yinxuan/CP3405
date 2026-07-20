# Sprint 7 Goal and Definition of Done — R1 Product Owner — vW29

**Team:** Team 5  
**Sprint:** Sprint 7 / Week 7  
**Forecast tag:** `vW29`  
**Due:** Sunday 19 July 2026, 23:59 SGT  
**Presentation:** Monday 20 July 2026  
**Role:** R1 — Product Owner  

---

## Sprint 7 Goal

Deliver an audit-ready `vW29` market-intelligence increment on time, with blockers surfaced early, R3/R4/R5 outputs completed before R8 synthesis, all required data collected automatically, Human Score connected to the final prediction, calibration evidence committed, and the final delivery sealed with the exact `vW29` release tag.

---

## R1 Product Owner Contribution

As the R1 Product Owner, I:

- Defined the Sprint 7 Goal.
- Defined the Definition of Done.
- Set the acceptance criteria for the `vW29` release.
- Included the R2 midweek check-in requirement.
- Set the Wednesday deadline for R3, R4, and R5.
- Defined the required delivery sequence.
- Reviewed the final GitHub evidence against the DoD.
- Recorded the completed deliverables and remaining exceptions.
- Completed the final Product Owner release assessment.

---

## Required Delivery Sequence

**R3 Almanac + R4 Macro + R5 Technical → R8 LLM Synthesis → R7 Human Score and Final Prediction → R9 vW29 Release**

Supporting responsibilities:

- R1 defines the Sprint Goal, DoD, and final release assessment.
- R2 monitors role progress, blockers, deadlines, and team readiness.
- R6 verifies the automated data pipeline and sector coverage.
- R10 verifies the previous prediction against actual results.

---

# Final Definition of Done Review — Sprint 7 / vW29

| Area | Definition of Done item | Final status |
| --- | --- | --- |
| Sprint Setup | `sprint_goal_W29.md` is committed and the Sprint Goal is communicated to the team. | **Complete** |
| Scrum Health | `standup_midweek_W29.md` records the status and blockers of all roles by the Wednesday checkpoint. | **Complete** |
| Code Quality | Feature work passes through Code Review before merging into `main`. | **Complete** |
| Automation | GitHub Actions runs automatically after Friday US market close. | **Complete — scheduled Run #69 succeeded** |
| Automation Evidence | The successful workflow URL is available as final evidence. | **Complete** |
| Data Collection | SPX, NDX, IWM, all 11 sector ETFs, and supporting assets are included in the automated output. | **Complete — R6 verified all required assets** |
| Final Sector Prediction | The final prediction provides an individual direction and confidence for all 11 sector ETFs. | **Documented exception — the collector includes all sectors, but the final prediction does not provide separate predictions for every sector** |
| Agent Sequence | R3 Almanac, R4 Macro, and R5 Technical outputs are committed before R8 synthesis. | **Complete** |
| LLM Synthesis | At least two LLMs are called successfully through API. | **Complete — four valid LLM response files were committed** |
| LLM Evidence | Raw API responses and a completed comparison table are committed. | **Complete** |
| Human Score | R7 Human Score and sourced Wild Card reasoning are connected to the final decision. | **Complete** |
| Prediction File | The final prediction includes the main indices, direction, confidence, evidence, and invalidation conditions. | **Complete with documented sector-coverage exception** |
| Calibration | Corrected `delta_W28.md` records Sprint 6 accuracy and improvement actions. | **Complete** |
| Future Calibration | A calibration framework for W29 post-actuals scoring is prepared. | **Complete** |
| Branch Merge | Active Sprint 7 working branches are merged before the release. | **Complete** |
| Release Tag | The exact `vW29` release tag is created before the deadline. | **Complete** |
| Discord | The Sprint 7 submission is posted using the mandatory template and evidence links. | **Complete** |
| Retrospective | `retrospective_W29.md` is completed and committed by R2. | **Complete** |
| Presentation | R1 contribution and GitHub evidence are ready for presentation. | **Complete — team-wide readiness is monitored by R2** |

---

## Required Sector Coverage

The required sector ETFs are:

`XLK · XLV · XLF · XLY · XLC · XLI · XLP · XLE · XLB · XLRE · XLU`

R6 verified that all 11 sector ETFs are present in the data collector and in the 17 July automated output.

The data-collection requirement is therefore complete.

The remaining exception is that the final prediction does not show a separate direction and confidence value for every sector ETF. This exception is documented and carried forward as an improvement item.

---

## Verified Sprint 7 Evidence

### Sprint Goal and Scrum Health

- `Week7/R1_Product_Owner/sprint_goal_W29.md`
- `Week7/R2_Scrum_Master/standup_midweek_W29.md`
- `Week7/R2_Scrum_Master/retrospective_W29.md`

The Sprint Goal was defined at the beginning of the sprint. R2 created the midweek check-in and recorded team progress and blockers.

### Agent Outputs

The required agent outputs were committed before the final LLM synthesis:

- `Week7/R3_almanac/almanac_agent_W07.md`
- `Week7/R4_macro/macro_agent_W07.md`
- `Week7/R5_technical/technical_agent_W07.md`

R3 provided seasonal and calendar evidence. R4 provided macroeconomic and market-condition evidence. R5 provided the technical market analysis.

### Automation and Data Coverage

R6 verified:

- SPX, NDX, and IWM coverage.
- All 11 required sector ETFs.
- Six supporting market assets.
- Valid numeric output schema.
- Friday post-close automation.
- A successful scheduled workflow run.

The successful workflow evidence is:

- Workflow: `Update Market Data #69`
- Trigger: Schedule
- Status: Success
- Duration: 46 seconds
- Output date: 17 July 2026
- Run URL: https://github.com/Gong-yinxuan/CP3405/actions/runs/29618672719

### LLM Synthesis

Four valid LLM response files were committed:

- `Week7/R8_llm/synthesis_chatgpt_W07.json`
- `Week7/R8_llm/synthesis_claude_W07.json`
- `Week7/R8_llm/synthesis_deepseek_W07.json`
- `Week7/R8_llm/synthesis_gemini_W07.json`

The comparison and synthesis evidence is:

- `Week7/R8_llm/llm_synthesis_W07.md`

The four models provided a generally bullish or cautious-bullish weekly outlook with Medium confidence.

### Human Score and Final Prediction

R7 completed:

- `Week7/ R7_Human_Score/human_score_W07.md`
- `Week7/ R7_Human_Score/prediction.md`

The Human Score produced a total of `+6`, resulting in a **Bullish Override**.

The final index calls were:

- SPX: Up
- NDX: Flat/Up
- IWM: Up

The final prediction includes percentage ranges, confidence levels, supporting evidence, contradiction evidence, and invalidation conditions.

### Calibration

R10 completed the corrected Sprint 6 calibration using the correct 17 July actuals.

The corrected results were:

- Direction accuracy: **50.0%**
- Range accuracy: **40.0%**
- Mean absolute error: **3.72 percentage points**

Calibration evidence:

- `Week7/R10/delta_W28.md`
- `Week7/R10/Week7/R10_Calibration/r10_calibration_W29.md`
- `Week7/R10/Week7/R10_Calibration/accuracy_dashboard_W23_W28.md`
- `Week7/R10/Week7/R10_Calibration/accuracy_history_W23_W28.csv`

### Release

The final release was created with the exact required tag:

- Release tag: `vW29`
- Release URL: https://github.com/Gong-yinxuan/CP3405/releases/tag/vW29

---

## Documented DoD Exceptions

Two exceptions were identified during the Product Owner review:

### 1. Complete Code Review Evidence

Some work was merged through pull requests, but GitHub did not provide enough evidence to confirm that every change passed through the Trello Code Review column.

### 2. Individual Predictions for All 11 Sectors

The automated data output includes all 11 sector ETFs. However, the final prediction does not provide a separate direction and confidence value for every sector.

These exceptions do not prevent the `vW29` release from being delivered, but they prevent the Sprint from being described as having perfect DoD compliance.

---

## Final R1 Product Owner Assessment

**Release delivery status:** Complete  
**Definition of Done compliance:** Complete with two documented exceptions

The main Sprint 7 delivery chain was completed:

**Sprint Goal → Midweek Check-in → Agent Outputs → LLM Synthesis → Human Score → Final Prediction → Automated Fetch → Calibration → vW29 Release**

The following major deliverables were completed:

- Sprint Goal and Definition of Done.
- R2 midweek check-in and retrospective.
- R3, R4, and R5 agent outputs.
- Four valid LLM API response files.
- LLM comparison and synthesis.
- R7 Human Score and Wild Card reasoning.
- Final index prediction with confidence and invalidation conditions.
- Successful scheduled automation.
- All 11 sector ETFs in the automated data output.
- Corrected calibration evidence.
- Branch merging.
- Exact `vW29` release tag.


The `vW29` release was successfully delivered. Two DoD exceptions were documented for future improvement: complete Code Review evidence and individual predictions for all 11 sector ETFs.

**Product Owner decision:** The `vW29` release is accepted as delivered, with two documented DoD exceptions carried forward for improvement.

---
