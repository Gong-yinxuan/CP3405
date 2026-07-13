# Definition of Done — Sprint 7 / vW29

**Role owner:** R1 Product Owner  
**Purpose:** Make “done” unambiguous before the `vW29` tag is cut.

## vW29 Definition of Done Checklist

| Area | DoD item | Status before final tag |
|---|---|---|
| Sprint Setup | `sprint_goal_W29.md` committed to repo and posted to Discord on Monday 13 July. | |
| Scrum Health | `standup_midweek_W29.md` committed by R2 before Wednesday 23:59 SGT, detailing status/blockers for all 10 roles. | |
| Code Quality | All feature branches passed through the Trello "Code Review" column. No direct commits to main by developers. | |
| Automation | GitHub Actions workflow ran automatically after Friday US close / Saturday morning SGT. | |
| Automation evidence | Workflow run URL is saved in the final submission / Discord post. | |
| Data coverage | SPX, NDX, IWM and all 11 sector ETFs are included in the prediction scope. | |
| Agent sequence | R3 Almanac, R4 Macro, and R5 Technical outputs are committed before LLM synthesis (Wednesday noon gate). | |
| LLM synthesis | At least two LLMs are called via API, not only chat window. | |
| LLM evidence | Raw API responses and comparison table are committed as files. | |
| Human Score | R7 Wild Card / Human Score is written and connected to final decision. | |
| Prediction file | `prediction_W29.md` includes SPX, NDX, IWM, all 11 sectors, direction, confidence, invalidation, and evidence summary. | |
| Calibration | `delta_W28.md` exists and is committed to confirm Sprint 6 accuracy learning before the W29 decision. | |
| Future calibration | `delta_W29.md` path is prepared for post-actuals scoring. | |
| Branch Merge | All active working branches merged into main before Saturday 18 July ends. | |
| Tag | Correct release tag `vW29` is created before Sunday 19 July 23:59 SGT. | |
| Discord | Sprint 7 Discord submission posted using the mandatory template. | |
| Retrospective | `retrospective_W29.md` completed and committed to the repo by R2. | |

## Product Owner sign-off rule
R1 should sign off only when the final artefacts are inspectable in GitHub. A file that exists locally but is not committed does not count. A workflow that only “works on my machine” does not count. A prediction that omits all-11-sector coverage does not meet Sprint 7 scope.