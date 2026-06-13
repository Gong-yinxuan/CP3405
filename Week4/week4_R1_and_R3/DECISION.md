# DECISION.md — Week 4 Architecture Decision (Repo-Aligned)

## What did we choose to automate first?

For W04, the team chose to automate the **market data collection step** first.

The documented pipeline fetches market data from Yahoo Finance for:

- SPY — S&P 500 proxy
- QQQ — Nasdaq 100 proxy
- IWM — Russell 2000 proxy
- XLK — Technology sector ETF
- XLU — Utilities sector ETF
- XLV — Healthcare sector ETF

The output is structured as `output.json`, with latest close and weekly-change fields where applicable.

---

## Why this was the right first automation

The most repetitive part of the manual pipeline is collecting market levels and sector evidence before agents can reason about them. Automating this first creates a stable input layer for later agents.

This is better than building a dashboard first because a dashboard without reliable input data is only presentation. A small collector that runs and writes structured JSON is a real system increment.

---

## How this matches the W04 roadmap

The W04 roadmap asks for:

- First software increment.
- At least one automated data fetch script committed to GitHub.
- Prediction expansion to SPX, NDX, IWM, and at least three S&P sectors.
- `DECISION.md` explaining what was automated first and why.

The chosen automation directly satisfies the minimum software-increment requirement and supports the sector-expansion requirement because it includes three sector ETFs: **XLK, XLU, and XLV**.

---

## Decision scope

This W04 automation is **not yet** a complete prediction engine.

It does not automatically make the final forecast, calculate Human Score, run LLM calls, or produce a full Delta Engine. It only collects structured market data. That is acceptable for W04 because the roadmap expects the team to move gradually from manual work toward a structured and automated pipeline.

---

## Definition of Done for this decision

| Check | Status | Note |
|---|---|---|
| Data source selected | Done | Yahoo Finance. |
| Index proxies defined | Done | SPY, QQQ, IWM. |
| Minimum sector ETFs defined | Done | XLK, XLU, XLV. |
| Structured output format | Done | JSON schema documented in `w3_delta_report.md`. |
| Script runs locally | Needs live verification | Show `collect_market_data.py` running if teacher asks. |
| Output file exists | Needs live verification | Show `output.json` in repo or generated locally. |
| GitHub Actions workflow | Needs live verification | Show `.github/workflows/market_data.yml` if available. |

---

## Product Owner note

This decision protects sprint value because it reduces manual copying, standardises input data, and gives later agents a machine-readable evidence base. For W05, the correct next step is to connect this collector to an automatic delta comparison file so the team can compare W04 prediction versus W04 actuals without manual calculation.

---

## Repo evidence sources checked

- Week4 folder: https://github.com/Gong-yinxuan/CP3405/tree/main/Week4
- W04 Wednesday Midsprint Check: https://github.com/Gong-yinxuan/CP3405/tree/main/Week4/Evidence/W04%20Wednesday%20Midsprint%20Check
- W04 Friday Closing: https://github.com/Gong-yinxuan/CP3405/tree/main/Week4/Evidence/W04%20Friday%20Closing
- Midweek actuals: https://raw.githubusercontent.com/Gong-yinxuan/CP3405/main/Week4/Evidence/actuals_2026-W04-midweek-log.md
- Closing actuals: https://raw.githubusercontent.com/Gong-yinxuan/CP3405/main/Week4/Evidence/actuals_2026-W04-closing.md
- Technical Agent W04: https://raw.githubusercontent.com/Gong-yinxuan/CP3405/main/Week4/R5_technical/technical_agent_W04.md
- Market Data Collector report: https://raw.githubusercontent.com/Gong-yinxuan/CP3405/main/Week4/w3_delta_report.md
- Course roadmap: https://dt3-tr2-26-market-intelligence.pages.dev/roadmap/
- Roles page: https://dt3-tr2-26-market-intelligence.pages.dev/roles/
- Federal Reserve 2026 FOMC calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- NYSE holiday calendar: https://www.nyse.com/trade/hours-calendars
