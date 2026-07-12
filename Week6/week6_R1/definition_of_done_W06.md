# Definition of Done — Sprint 6 / vW28

**Role owner:** R1 Product Owner  
**Purpose:** Make “done” unambiguous before the `vW28` tag is cut.

## vW28 Definition of Done Checklist

| Area | DoD item | Status before final tag                   |
|---|---|-------------------------------------------|
| Automation | GitHub Actions workflow ran automatically after Friday US close / Saturday morning SGT. | To verify from Actions log                |
| Automation evidence | Workflow run URL is saved in the final submission / Discord post. | To complete                               |
| Data coverage | SPX, NDX, IWM and all 11 sector ETFs are included in the prediction scope. | To complete                               |
| Agent sequence | R3 Almanac, R4 Macro, and R5 Technical outputs are committed before LLM synthesis. | Partially met: R3/R4/R5 files exist       |
| LLM synthesis | At least two LLMs are called via API, not only chat window. | Partially met: Only Gemini called via API |
| LLM evidence | Raw API responses and comparison table are committed as files. | Met: Can be found in R8 Files             |
| Human Score | R7 Wild Card / Human Score is written and connected to final decision. | To complete by R7                         |
| Prediction file | `prediction_W28.md` or `prediction_W28.json` includes SPX, NDX, IWM, all 11 sectors, direction, confidence, invalidation, and evidence summary. | R1 draft prepared                         |
| Calibration | `delta_W25.md` exists or is added to confirm Sprint 5 accuracy learning before W28 decision. | Sprint 6 fix item                         |
| Future calibration | `delta_W28.md` path is prepared for post-actuals scoring. | To complete after actuals                 |
| Tag | Correct release tag `vW28` is created before Sunday 12 July 23:59 SGT. | To complete by R9                         |
| Discord | Sprint 6 Discord submission posted with repo, tag, prediction, automation, agent, LLM, calibration, and Scrum health details. | Draft prepared                            |
| Retrospective | One concrete Sprint 7 improvement is recorded in repo. | To complete by R2/R10                     |

## Product Owner sign-off rule

R1 should sign off only when the final artefacts are inspectable in GitHub. A file that exists locally but is not committed does not count. A workflow that only “works on my machine” does not count. A prediction that omits all-11-sector coverage does not meet Sprint 6 scope.
