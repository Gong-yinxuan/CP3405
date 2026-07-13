# Sprint 7 Goal — R1 Product Owner — vW29

**Team:** Team 5  
**Sprint:** Sprint 7 / Week 7  
**Forecast tag:** `vW29`  
**Due:** Sunday 19 July 2026, 23:59 SGT  
**Presentation:** Monday 20 July 2026  
**Role:** R1 — Product Owner  

## Sprint 7 Goal

**Deliver an audit-ready vW29 market-intelligence increment by Sunday 19 July 2026, 23:59 SGT, with blockers surfaced by Wednesday, R3/R4/R5 outputs finalized before R8 synthesis, all 11 S&P sector ETFs included, at least two valid LLM API responses committed, R7 Human Score connected to the final prediction, a successful automated Friday-close workflow, verified calibration evidence, and the final prediction sealed with the exact `vW29` release tag.**

## Why This Goal Is Measurable

The team can verify the Sprint Goal by checking:

- `standup_midweek_W29.md` is committed by R2 before Wednesday 15 July, 23:59 SGT.
- The R2 check-in records the specific status and blockers of every role.
- R3 Almanac, R4 Macro, and R5 Technical outputs are reviewed and finalized before R8 synthesis.
- At least two valid LLM API responses are saved as repository files.
- A completed LLM comparison table is committed.
- R7 Human Score and sourced Wild Card reasoning are connected to the final decision.
- The final prediction covers SPX, NDX, IWM, and all 11 S&P sector ETFs.
- The automated workflow runs successfully after Friday US market close.
- The successful GitHub Actions run URL is included in the final submission.
- `delta_W28.md` and cumulative accuracy evidence are reviewed.
- All active branches are merged before the final release.
- The exact `vW29` tag is created before the deadline.
- The final Discord submission contains working evidence links.

## Dependency Order

The required delivery order is:

**R3 Almanac + R4 Macro + R5 Technical → R8 LLM Synthesis → R7 Human Score and Final Prediction → R9 vW29 Release**

Supporting responsibilities:

- R1 defines the Sprint Goal and Definition of Done.
- R2 monitors role status, blockers, deadlines, and dependencies.
- R6 confirms the automated data pipeline and all 11 sector ETFs.
- R10 verifies the previous prediction against actual results.

## R1 Acceptance Position

Sprint 7 should not be accepted as Done if the repository contains only partial or auto-generated draft files.

The Sprint is accepted only when the output is inspectable as one complete delivery chain:

**Sprint Goal → mid-week check-in → agent outputs → LLM synthesis → Human Score → final prediction → automated fetch → calibration → vW29 release**

---

# Definition of Done — Sprint 7 / vW29

**Role owner:** R1 Product Owner  
**Purpose:** Make “Done” unambiguous before the `vW29` tag is created.

## vW29 Definition of Done Checklist

| Area | DoD item | Status before final tag |
| --- | --- | --- |
| Sprint Setup | `sprint_goal_W29.md` is committed through Code Review and the Sprint Goal is posted to Discord on Monday 13 July. | In progress |
| Scrum Health | `standup_midweek_W29.md` is committed by R2 before Wednesday 15 July, 23:59 SGT, detailing the status and blockers of all roles. | Pending |
| Code Quality | All feature branches pass through the Trello Code Review column. Developers do not commit directly to main. | In progress |
| Automation | GitHub Actions runs automatically after Friday US close / Saturday morning SGT. | Pending Friday run |
| Automation Evidence | The successful workflow URL is saved in the final submission and Discord post. | Pending |
| Data Coverage | SPX, NDX, IWM, and all 11 sector ETFs are included in the final prediction scope. | Collector configured; final prediction pending |
| Agent Sequence | R3 Almanac, R4 Macro, and R5 Technical outputs are reviewed and committed before final R8 synthesis. | Drafts exist; owner review pending |
| LLM Synthesis | At least two LLMs are called successfully through API, not only through chat windows. | Partially met; final verification pending |
| LLM Evidence | Raw API responses and a completed comparison table are committed as files. | Files exist; errors and pending fields remain |
| Human Score | R7 Wild Card / Human Score is written, sourced, and connected to the final decision. | Pending |
| Prediction File | `prediction_W29.md` or `.json` includes SPX, NDX, IWM, all 11 sectors, direction, confidence, invalidation, and evidence summary. | Pending |
| Calibration | `delta_W28.md` is verified and completed to record Sprint 6 accuracy learning before the W29 decision. | File exists; R10 review pending |
| Future Calibration | A `delta_W29.md` path is prepared for post-actuals scoring. | Pending |
| Branch Merge | All active working branches are merged into main before Saturday 18 July ends. | Pending |
| Tag | The correct release tag `vW29` is created before Sunday 19 July, 23:59 SGT. | Pending |
| Discord | The Sprint 7 Discord submission is posted using the mandatory template and working links. | Pending |
| Retrospective | `retrospective_W29.md` is completed and committed by R2. | Pending |
| Presentation | Every role R1–R10 is ready to present on Monday 20 July. | Pending |

## Required Sector Coverage

The final prediction must include:

`XLK · XLV · XLF · XLY · XLC · XLI · XLP · XLE · XLB · XLRE · XLU`

## Product Owner Sign-Off Rule

R1 should sign off only when the final artefacts are inspectable in GitHub.

A file that exists locally but is not committed does not count. An auto-generated report with incomplete manual sections, unresolved API errors, or pending calculations does not count as final evidence.

A workflow that only works manually does not satisfy the scheduled automation requirement. A prediction that omits any required index or sector does not meet Sprint 7 scope.

**Current Sprint status:** In Progress  

**Definition of Done owner:** R1 Product Owner  
**Final verification:** R2 Scrum Master
