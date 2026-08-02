# Sprint 8 Retrospective Report (vW30)

**Date:** Sunday 26 July 2026  
**Scrum Master:** R2 - Hoang To

---

## 🎯 Sprint Goal Evaluation

* **Goal Status:** Achieved
* **Summary:** The team successfully continued the Prism market-intelligence automation work for `vW30`. The team delievered everything before deadline.

---

## 📈 Metric & Process Performance

### 🔄 1. Workflow

* **What Happened:** The team found that the normal calibration runner could fail when the matching prediction file was not ready yet.
* **Scrum Master Intervention:** Coordinated the testing of a separate `save_actuals.py` workflow so actuals could be saved first without depending on `vW30_prediction.json`.
* **Outcome:** Actuals saving became clearer and safer. The team can now run the workflow in two stages: first save actuals, then run calibration only after the matching prediction file exists.

### ⚙️ 2. API Key Invalidation

* **What Happened:** When team running for LLM-synthesis the tencent/Hy3 one of the model ran into errors.

* **What Went Well:** Team figured out the model we used last week jsut announced no longer free so we went looking for new model

* **Outcome:** Team found a new free model and moved on with it.

### 🧪 3. Calibration Validation

* **What Happened:** When calibration was run for `vW30`, the script detected a date mismatch between the actuals date and the prediction forecast week.
* **Result:** The calibration runner correctly stopped instead of producing an inaccurate score. This showed that the date-integrity logic is working as intended.
* **Learning:** The issue was not caused by the actuals file. The problem was that the prediction file had the wrong `forecast_week`, ending on `2026-08-01` instead of matching the actuals date `2026-07-24`.

---

## 🛑 Engineering Pitfalls & Course Corrections

### ⚠️ Prediction and Actuals Date Mismatch

* **Problem Encountered:** The `vW30_prediction.json` file had a forecast week that did not match the actuals data date. The actuals snapshot was dated `2026-07-24`, but the prediction expected an end date of `2026-08-01`.
* **Immediate Correction:** The team identified that the correct forecast week should be `2026-07-20 to 2026-07-24`. Calibration should only be run after the prediction file and actuals file are confirmed to refer to the same forecast period.
* **Outcome:** The team avoided generating an incorrect calibration score.

### ⚠️ GitHub Actions Workflow Reliability

* **Problem Encountered:** The GitHub Actions update workflow still needed refinement because the automated process could save actuals but should not blindly run calibration when the matching prediction file is missing or incorrectly dated.
* **Immediate Correction:** The workflow was updated so that `save_actuals.py` saves the actuals snapshot first, and calibration only runs if the matching prediction file exists.
* **Outcome:** The workflow is safer because missing prediction files no longer break the entire actuals collection process.

---

## 🚀 Key Takeaways for Sprint 9

1. **Separate Actuals Saving from Calibration:** Keep `save_actuals.py` as a separate R6 step so actuals can be saved even before prediction scoring is ready.

2. **Validate Forecast Week Before Calibration:** Before running `calibration_runner.py`, confirm that the prediction `forecast_week` end date matches the actuals `date`.

3. **Avoid Hardcoded Release Mistakes:** The workflow should avoid permanently hardcoding releases such as `vW30`. Each sprint should either auto-detect the release safely or allow a manual release input.