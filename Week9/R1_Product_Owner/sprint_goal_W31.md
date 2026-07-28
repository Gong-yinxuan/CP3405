# Sprint 9 Goal & Definition of Done (vW31)
**Date:** Monday 27 July 2026  
**Product Owner:** R1 — Ho Yuet Hei

## 🎯 Sprint Goal
Deliver an audit-ready, structurally flawless vW31 market-intelligence prediction package before Sunday 2 August 2026, 23:59 SGT. Building on Sprint 8's repository structural cleanup, this sprint focuses on expanding the LLM prompt matrix to ingest next-week market catalysts, hardening our pipeline against model disruptions, and executing strict manual human quality validation over all automated nodes.

### ❓ Context & Rationale for Lecturer Alignment
Following our Sprint 8 presentation review, we are adding three explicit engineering layers:
*   **Human-in-the-Loop Integrity:** Automated data collections are great, but they are not infallible. Upstream agents must manually sign off on their datasets to ensure zero corrupted or skewed snapshots pass the gate.
*   **Forward-Looking Catalyst Prompting:** Markets move on upcoming expectations, not just historical data. We are upgrading our LLM synthesis prompts to analyze specific high-impact calendar events scheduled for the upcoming week.
*   **Pipeline Hotfixing:** Any lingering data-integrity bugs from last week (such as stale date overrides or historical accumulation errors) must be permanently hotfixed in our scripts.

---

## ⏳ Pipeline Gates & Deadlines

### 🛠️ Upstream Research Agents (The Wednesday Gate — Due Wednesday 29 July @ 23:59 SGT)
*   **R3 (Almanac Analyst):** Run the automated `generate_almanac.py` script. **Human Quality Gate:** R3 must manually inspect the output markdown report against historical baselines to verify structural completeness before the gate closes.
*   **R4 (Macro Analyst):** Commit qualitative macro analysis reports and archive matching asset charts under the designated folder. **Human Quality Gate:** R4 must manually verify that external web scraping feeds did not encounter hidden data errors or access blocks.
*   **R5 (Technical Analyst):** Push trend indicators, snapshot markers (SPX, NDX, IWM), and core index support/resistance asset charts. **Human Quality Gate:** R5 must manually audit all automated moving average numbers to ensure data precision.

### ⚙️ Downstream Synthesis & Logistics (The Weekend Pipeline — Due Sunday 2 August @ 23:59 SGT)
*   **R6 (Data Engineer):** Maintain full script coverage for all 11 mandatory S&P sector ETFs (XLK through XLU). **Hotfix Requirement:** Ensure the pipeline script's date-validation modules automatically drop stale snapshots.
*   **R8 (AI/ML Engineer):** Trigger the GitHub Actions manual synthesis workflow on Thursday 30 July. **Prompt Upgrade:** Redesign the core prompt template to feed specific upcoming macro catalysts directly into the models. Maintain the regex string cleaner to scrub leaking internal reasoning tokens.
*   **R7 (Senior Analyst):** Finalize directional forecasts across all 11 sector ETFs and apply the Human Score Wild Card override with clear documented rationales by Saturday night 1 August.
*   **R10 (Calibration Analyst):** Process actual market close parameters from Saturday 1 August to rebuild the historical performance baseline and finalize performance error tables. **Hotfix Requirement:** Ensure any mismatched historical records are cleanly reconciled inside `accuracy_history.json`.
*   **R9 (DevOps Lead):** Enforce strict file-case checks, handle repository branch protections, merge verified PRs, and seal the definitive release tag on Sunday night 2 August.

---

## 🗂️ Strict Repository Directory Blueprint

All roles must place files exactly according to the structure below. Use chronological agent suffix (**`_W09`**) for research files, and calendar week sprint suffix (**`_W31`**) for tracking logs.

*   📂 **`Week9/`**
    *   📂 **`R1_Product_Owner/`**
        *   📄 `sprint_goal_W31.md` *(This file)*
    *   📂 **`R2_Scrum_Master/`**
        *   📄 `standup_midweek_W31.md`
        *   📄 `retrospective_W31.md`
    *   📂 **`R3_almanac/`**
        *   📁 `almanac_assets/`
        *   📄 `almanac_agent_W09.md`
    *   📂 **`R4_macro/`**
        *   📁 `macro_assets/`
        *   📄 `macro_agent_W09.md`
    *   📂 **`R5_technical/`**
        *   📁 `technical_assets/`
        *   📄 `technical_agent_W09.md`
    *   📂 **`R6_Data/`**
        *   📄 `r6_data_verification_W31.md`
    *   📂 **`R7_Human_Score/`**
        *   📄 `human_score_W09.md`
        *   📄 `prediction.md`
    *   📂 **`R8_llm/`**
        *   📄 `ai_prompt_W09.md`
        *   📄 `llm_synthesis_W31.md`
        *   📄 `synthesis_chatgpt_W09.json`
        *   📄 `synthesis_deepseek_W09.json`
        *   📄 `synthesis_gemini_W09.json`
        *   📄 `synthesis_claude_W09.json`
    *   📂 **`R10_Calibration/`**
        *   📄 `delta_W30.md` *(Tracks week 30 calibration performance)*
        *   📄 `r10_calibration_W31.md`
        *   📄 `accuracy_history.md`
        *   📄 `accuracy_history.json`

---

## ✅ Role-Specific Definition of Done (DoD)

*   **Mandatory Human Quality Check Sign-off:** Every raw data file submitted by R3, R4, and R5 must include a dedicated header section titled `### 🛑 Human Quality Gate Verification` containing a manual confirmation note from the owner to verify that the automated data is completely error-free.
*   **Forward-Looking Catalyst Prompting:** R8's upgraded prompt architecture (`ai_prompt_W09.md`) must feature an explicit context block detailing upcoming next-week calendar catalysts (such as upcoming corporate earnings reports and central bank interest rate decisions) so the AI models can factor them into their directional outputs.
*   **Case-Sensitivity Constraint:** Directory and file names must match the case patterns shown in the blueprint exactly to avoid cross-OS git tracking stalls.
*   **Asset Insulation:** All generated `.png` plots or charts must reside inside their respective role's nested `_assets/` subfolders rather than cluttering base role directories.
*   **Sealed Release Rule:** The DevOps Lead (R9) will only cut the final repository tag (`vW31`) after receiving a verbal sign-off from the Scrum Master on Sunday evening confirming all deliverables are merged and verified.