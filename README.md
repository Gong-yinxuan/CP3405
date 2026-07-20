# PRISM — Sprint 13 (vW29) Final Release

## Project Overview

PRISM is a market prediction system developed for **CP3405**.

The goal of the project is to gradually transition from a **manual market prediction workflow** into a **partially automated pipeline** using structured agents, automation, and LLM synthesis.

The system focuses on predicting:

* **S&P 500 (SPX)**
* **Nasdaq 100 (NDX)**
* **Russell 2000 (IWM)**
* **All 11 S&P 500 sector ETFs** (XLK, XLV, XLF, XLY, XLC, XLI, XLP, XLE, XLB, XLRE, XLU)

---

## Sprint 13 (vW29) Deliverables

**Sprint Goal:** Deliver an audit-ready vW29 market-intelligence increment by Sunday 19 July 2026, 23:59 SGT, with blockers surfaced by Wednesday, R3/R4/R5 outputs finalized before R8 synthesis, all 11 S&P sector ETFs included, at least two valid LLM API responses committed, R7 Human Score connected to the final prediction, a successful automated Friday-close workflow, verified calibration evidence, and the final prediction sealed with the exact `vW29` release tag.

**Sprint status:** Achieved ✅

| Role | This week's output |
|---|---|
| R1 Product Owner | Defined the Sprint Goal and Definition of Done — `Week7/R1_Product_Owner/sprint_goal_W29.md` |
| R2 Scrum Master | Mid-week check-in and blocker tracking, plus the Sprint retrospective — `Week7/R2_Scrum_Master/standup_midweek_W29.md`, `retrospective_W29.md` |
| R3 Almanac | Automated Almanac agent report generated via `generate_almanac.py` — `Week7/R3_almanac/almanac_agent_W07.md` |
| R4 Macro | Macro agent report covering yields, oil, gold, DXY, VIX, and BTC — `Week7/R4_macro/macro_agent_W07.md` |
| R5 Technical | Technical analysis across SPX / NDX / IWM — `Week7/R5_technical/technical_agent_W07.md` |
| R6 Data | Verified and expanded the data collector to cover all 11 S&P sector ETFs; confirmed the scheduled automation run — `Week7/R6/Week7/R6_Data/r6_data_verification_W29.md` |
| R7 Human Score | Five-dimension human override score connected to the final prediction — `Week7/ R7_Human_Score/human_score_W07.md`, `prediction.md` |
| R8 LLM Synthesis | Synthesis across 4 LLMs (Claude, ChatGPT, Gemini, DeepSeek) with a comparison table — `Week7/R8_llm/llm_synthesis_W07.md` |
| R9 GitHub Lead | Merged all working branches into `main` and cut the final `vW29` release tag |
| R10 Calibration | Rebuilt `vW28_actuals.json`, corrected `delta_W28.md`, and verified prior-week accuracy before this week's decision — `Week7/R10/Week7/R10_Calibration/r10_calibration_W29.md` |

---

## Automated Market Data Pipeline

Automated collectors run for the Technical, Macro, and Almanac roles, producing structured JSON output consumed by the LLM synthesis step.

| Collector | Purpose | Output |
| --------- | ------- | ------ |
| `technical_collector.py` | Collects historical index data and calculates technical indicators | `technical_collector_output.json` |
| `macro_collector.py` | Collects automatic macro market data such as yields, oil, gold, DXY, VIX, and BTC | `macro_collector_output.json` |
| `almanac_collector.py` | Collects calendar flags and sector ranking data | `almanac_collector_output.json` |

---

## Running the Pipeline Locally

From the repository root, run:

py prism/src/data_collector.py
py prism/src/collectors/technical_collector.py
py prism/src/collectors/macro_collector.py
py prism/src/collectors/almanac_collector.py

On systems where `python` is used instead of `py`, run:

python prism/src/data_collector.py
python prism/src/collectors/technical_collector.py
python prism/src/collectors/macro_collector.py
python prism/src/collectors/almanac_collector.py

---

## GitHub Actions Automation

The GitHub Actions workflow automatically runs the collectors and commits generated data files.

Workflow file:

`.github/workflows/update.yml`

Current automation schedule: Saturday 5:00 AM Singapore Time

Cron expression:

`- cron: "0 21 * * 5"`

This time was selected because US markets normally close before Saturday morning Singapore time, allowing the workflow to collect updated weekly market data after the trading week ends.

The workflow runs:

* Main market data collector
* Technical collector
* Macro collector
* Almanac collector
* Commit generated data under `prism/data`
