# PRISM — Week 4 First Software Increment

## Project Overview

PRISM is a market prediction system developed for **CP3405**.

The goal of the project is to gradually transition from a **manual market prediction workflow** into a **partially automated pipeline** using structured agents, automation, and LLM synthesis.

The system focuses on predicting:

* **S&P 500 (SPX)**
* **Nasdaq 100 (NDX)**
* **Russell 2000 (IWM)**
* **S&P 500 sector performance**

Week 4 introduces the team's **first software increment**, automating market data collection and integrating structured AI synthesis.

---

## Week 4 Deliverables

### Implemented Features

Automated market data collection

GitHub Actions workflow

JSON structured output

W3 Delta Report (prediction vs actual)

3 Agents Output

4 LLM Model

Prediction file


## Week 4 Automation

### Automated Market Data Pipeline

The Week 4 automation uses **Yahoo Finance (`yfinance`)** to retrieve market data automatically.

Currently collected assets include:

### Index Proxies

* **SPY** → S&P 500
* **QQQ** → Nasdaq 100
* **IWM** → Russell 2000

---

## Running the Pipeline Locally

### Install dependencies

```bash
pip install -r prism/requirements.txt
```

### Run the market data collector

```bash
python prism/src/data_collector.py
```

---

## GitHub Actions Automation

The repository includes an automated workflow:

```txt
.github/workflows/update.yml
```

The workflow:

1. Sets up Python
2. Installs dependencies
3. Runs the market data collector
4. Updates structured market outputs

The workflow can be triggered:

* **Manually**
* **Scheduled execution**

---

## Team Goal

The long-term goal is to transform PRISM from a manual workflow into a reproducible and partially autonomous prediction system using structured agents, automation, and AI-assisted reasoning.
