# PRISM — Week 5 First Software Increment

## Project Overview

PRISM is a market prediction system developed for **CP3405**.

The goal of the project is to gradually transition from a **manual market prediction workflow** into a **partially automated pipeline** using structured agents, automation, and LLM synthesis.

The system focuses on predicting:

* **S&P 500 (SPX)**
* **Nasdaq 100 (NDX)**
* **Russell 2000 (IWM)**
* **S&P 500 sector performance**

---

## Week 5 Deliverables

### Implemented Features

Automated market data collection for 3 agent

GitHub Actions workflow

JSON structured output

3 Agents Output

4 LLM Model

Prediction file

## Week 5 Automation

### Automated Market Data Pipeline

# Week 5 README — Prism Agent Data Automation

## Project

**Prism Market Intelligence System**
**Sprint:** Week 5 / W05
**Team:** Team 5
**Focus:** Agent data automation for Technical, Macro, and Almanac roles

---

## 2. What Was Automated This Week

This week, the team added three new automated collectors:

| Collector                | Purpose                                                                           | Output                            |
| ------------------------ | --------------------------------------------------------------------------------- | --------------------------------- |
| `technical_collector.py` | Collects historical index data and calculates technical indicators                | `technical_collector_output.json` |
| `macro_collector.py`     | Collects automatic macro market data such as yields, oil, gold, DXY, VIX, and BTC | `macro_collector_output.json`     |
| `almanac_collector.py`   | Collects calendar flags and sector ranking data                                   | `almanac_collector_output.json`   |


---

## Running the Pipeline Locally

From the repository root, run:

py prism/src/data_collector.py
py prism/src/collectors/technical_collector.py
py prism/src/collectors/macro_collector.py
py prism/src/collectors/almanac_collector.py

On systems where python is used instead of py, run:

python prism/src/data_collector.py
python prism/src/collectors/technical_collector.py
python prism/src/collectors/macro_collector.py
python prism/src/collectors/almanac_collector.py

---

## GitHub Actions Automation

The GitHub Actions workflow automatically runs the collectors and commits generated data files.

Workflow file:

.github/workflows/update.yml

Current automation schedule:

Saturday 5:00 AM Singapore Time

Cron expression:

- cron: "0 21 * * 5"

This time was selected because US markets normally close before Saturday morning Singapore time, allowing the workflow to collect updated weekly market data after the trading week ends.

The workflow runs:

Main market data collector
Technical collector
Macro collector
Almanac collector
Commit generated data under prism/data
