# Sprint 7 Retrospective Report (vW29)
**Date:** Sunday 19 July 2026  
**Scrum Master:** R2 - Ho Yuet Hei

## 🎯 Sprint Goal Evaluation
* **Goal Status:** Achieved
* **Summary:** Successfully delivered an audit-ready vW29 market-intelligence increment before the 23:59 SGT deadline. All 11 S&P sector ETFs were integrated into the pipeline, and the final prediction has been successfully sealed under the `vW29` release tag.

---

## 📈 Metric & Process Performance

### 🔄 1. The Role Rotation & Blocker Resolution
* **What Happened:** At the start of Sprint 7, a major mid-sprint role rotation was executed. This created a board-level blocker: *"Possible Confusion from Role Swap (Mentally prepared everyone to fulfil their roles)"*. Downstream roles (R6, R8, and R10) initially faced ambiguity regarding their updated technical scopes and execution steps.
* **Scrum Master Intervention:** Conducted 1-on-1 alignment huddles during mid-week check-ins. Clarified the mandatory 11-sector ETF expansion for R6, walked R8 through the GitHub Actions manual execution path, and pre-staged R10 for the weekend calibration requirements. 
* **Outcome:** The blocker was successfully cleared. All team members executed their newly assigned tasks without missing pipeline gate deadlines.

### ⚙️ 2. Workflow & Automation Highlights
* **What Went Well:** The automation of R3's Almanac agent via `generate_almanac.py` directly inside GitHub Actions worked flawlessly. This completely removed manual file injection friction from the Wednesday gate, allowing R4 and R5 to merge their research smoothly.
* **Downstream Execution:** R8 successfully triggered the synthesis pipeline on Thursday morning using the stored repository API secrets, feeding pristine data into the LLM engine on schedule.

---

## 🛑 Engineering Pitfalls & Course Corrections

### ⚠️ Premature Release Tagging
* **Problem Encountered:** On Sunday morning, a pipeline sequence conflict occurred where the `vW29` final release tag was cut prematurely while critical deliverables (`delta_W28.md` and Human Score wild card overrides) were still actively *In Development*.
* **Immediate Correction:** The Scrum Master coordinated with R9 (DevOps Lead) to delete the premature tag. The final repository release was strictly held back until R7 and R10 verified their final text files were completely merged into `main`.

---

## 🚀 Key Takeaways for Sprint 8
1. **Freeze System Tags:** Establish a hard rule that the DevOps Lead (R9) will only cut the final release tag after a final verbal or written sign-off from the Scrum Master on Sunday evening.
2. **Enhance Backlog Clarity:** Improve backlog grooming prior to the next sprint by embedding strict Definitions of Done (DoD) and explicit fulfillment conditions for each role to prevent role-swap confusion.
