markdown# Sprint 8 Goal & Definition of Done (vW30)
**Date:** Monday 20 July 2026  
**Product Owner:** R1 — Ho Yuet Hei

## 🎯 Sprint Goal
Deliver an audit-ready, structurally flawless vW30 market-intelligence prediction package before Sunday 26 July 2026, 23:59 SGT. This sprint focuses on eliminating file-path duplication, standardizing naming suffixes, and embedding robust date validation into our multi-agent pipeline.

---

## ⏳ Pipeline Gates & Deadlines

### 🛠️ Upstream Research Agents (The Wednesday Gate — Due 22 July @ 23:59 SGT)
*   **R3 (Almanac Analyst):** Ensure the automated `generate_almanac.py` runs cleanly in the GitHub Actions workflow environment to build the required weekly markdown report.
*   **R4 (Macro Analyst):** Commit qualitative macro analysis reports and archive matching asset charts under the designated folder.
*   **R5 (Technical Analyst):** Push trend indicators and core index support/resistance asset charts.

### ⚙️ Downstream Synthesis & Logistics (The Weekend Pipeline — Due Sunday 26 July @ 23:59 SGT)
*   **R6 (Data Engineer):** Expand script coverage to track all 11 mandatory S&P sector ETFs and push verification logs by Friday night.
*   **R8 (AI/ML Engineer):** Trigger the GitHub Actions manual synthesis workflow on Thursday using valid repository secrets.
*   **R7 (Senior Analyst):** Finalize directional forecasts across all 11 sector ETFs and apply the Human Score Wild Card override by Saturday night.
*   **R10 (Calibration Analyst):** Process actual market close parameters from Saturday July 25 to finalize performance error tables.
*   **R9 (DevOps Lead):** Enforce strict file-case checks, merge verified PRs, and seal the definitive release tag on Sunday night.

---

## 🗂️ Strict Repository Directory Blueprint

All roles must place files exactly according to the structure below. No outer root duplicates or loose subdirectories are permitted.

*   📂 **`Week8/`**
    *   📂 **`R1_Product_Owner/`**
        *   📄 `sprint_goal_W30.md` *(This file)*
    *   📂 **`R2_Scrum_Master/`**
        *   📄 `standup_midweek_W30.md`
        *   📄 `retrospective_W30.md`
    *   📂 **`R3_almanac/`** *(Automated pipeline output)*
        *   📁 `almanac_assets/`
        *   📄 `almanac_agent_W08.md`
    *   📂 **`R4_macro/`**
        *   📁 `macro_assets/`
        *   📄 `macro_agent_W08.md`
    *   📂 **`R5_technical/`**
        *   📁 `technical_assets/`
        *   📄 `technical_agent_W08.md`
    *   📂 **`R6_Data/`**
        *   📄 `r6_data_verification_W30.md`
    *   📂 **`R7_Human_Score/`**
        *   📄 `human_score_W08.md`
        *   📄 `prediction.md`
    *   📂 **`R8_llm/`**
        *   📄 `ai_prompt_W08.md`
        *   📄 `llm_synthesis_W30.md`
        *   📄 `synthesis_chatgpt_W08.json`
        *   📄 `synthesis_claude_W08.json`
        *   📄 `synthesis_deepseek_W08.json`
        *   📄 `synthesis_gemini_W08.json`
    *   📂 **`R10_Calibration/`**
        *   📄 `delta_W29.md` *(Tracks week 29 calibration performance)*
        *   📄 `r10_calibration_W30.md`
        *   📄 `accuracy_history.md`
        *   📄 `accuracy_history.json`

---

## ✅ Role-Specific Definition of Done (DoD)

*   **Case-Sensitivity Constraint:** Directory names must match the case patterns shown in the blueprint exactly (e.g., lowercase `R8_llm`, uppercase `R1_Product_Owner`) to avoid cross-OS git tracking stalls.
*   **Asset Insulation:** All generated `.png` or tracking plots must be organized cleanly inside their nested `_assets/` subfolders rather than cluttering the base role directories.
*   **Uniform Suffix Policy:** Research and prediction modules use the chronological agent suffix (**`_W08`**). Process logs, synthesis outcomes, and calibration analyst write-ups use the calendar week sprint suffix (**`_W30`**).
*   **R8 Multi-Model Integrity:** The AI/ML synthesis step must output individual, un-nested `.json` prediction streams for every single target model (ChatGPT, Claude, DeepSeek, Gemini).
*   **R10 Duplication Ban:** No root duplicates of `delta_W29.md` are permitted. All historical error charts and evaluation summaries must reside cleanly within `Week8/R10_Calibration/`.
*   **Sealed Release Rule:** The DevOps Lead (R9) will only cut the final repository tag (`vW30`) after receiving a verbal sign-off from the Scrum Master on Sunday evening confirming all deliverables are merged.