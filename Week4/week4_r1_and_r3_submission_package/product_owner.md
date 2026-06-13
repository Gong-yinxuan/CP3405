# Week 4 — R1 Product Owner Output

**Role:** R1 — Product Owner  
**Sprint week:** W4 / vW24  
**Submission due:** Sunday 14 June 2026, 23:59 SGT  
**Presentation:** Monday 15 June 2026  
**Purpose:** Confirm the sprint goal, validate Definition of Done, and deliver the final W4 prediction narrative.

---

## 1. Required R1 responsibility

R1 is responsible for guarding sprint value, confirming the Definition of Done, and owning the prediction-call narrative. For Week 4, R1 must make sure the team submits both:

1. A real W4 market prediction: **SPX + NDX + IWM + at least 3 S&P 500 sectors**.
2. A real software increment: **at least one automated data-fetch or pipeline step committed to GitHub with clear instructions**.

R1 does not replace R3/R4/R5/R7. R1 turns their evidence into one coherent sprint goal, DoD status, and final call.

---

## 2. Sprint goal

**Sprint Goal — Week 4 / vW24**

> Build the first inspectable software increment for the market-intelligence pipeline and use it to support a W4 prediction covering SPX, NDX, IWM, and at least three S&P 500 sectors.

This sprint is successful only if the team can show both market reasoning and a working system increment. A prediction without software is incomplete. A software demo without a locked prediction is also incomplete.

---

## 3. Definition of Done checklist

| Requirement | Owner | DoD status | Evidence required |
|---|---|---|---|
| W4 prediction covers SPX, NDX, IWM | Full team / R1 signs off | To verify | `prediction_2026-W24.md` |
| At least 3 S&P sector signals included | R3/R4/R5 + R1 sign-off | To verify | Sector table inside prediction file |
| R3 Almanac output completed before LLMs | R3 | Ready | `almanac.md` |
| Software increment committed | Dev Team | To verify | Script file + output JSON/CSV |
| README explains how to run the script | Dev Team / R1 verifies | To verify | `README.md` |
| DECISION.md explains what was automated first and why | R1 | Ready | `DECISION.md` |
| W3 delta report included | R6/R10 | To verify | Delta report/table |
| LLM API call logged if Level 3 target chosen | R8 | Optional / Level 3 | Prompt + raw response file |
| Release tag created | R9 | To verify | GitHub release tag `vW24` |
| Monday demo can run live | R9 + Dev Team | To verify | Live run, not screenshot |

**R1 DoD statement for Monday:**  
Our Week 4 DoD is met only if the prediction file, sector coverage, R3 Almanac evidence, DECISION.md, software increment, README, delta report, and release tag are visible in GitHub before the deadline.

---

## 4. Architecture decision paragraph for `DECISION.md`

**Decision:**  
For Sprint 4, the team chose to automate the first data-collection step instead of building a polished dashboard. The most painful manual task in the earlier sprint was collecting repeatable market evidence from the same sources, then converting it into a format the agents and LLMs could use. Automating the data fetch first gives the team a reliable input layer for future agents, reduces manual copy-paste error, and makes the weekly prediction process inspectable in GitHub. This matches the course architecture direction: move from manual evidence collection to a structured and then automated intelligence pipeline. The first software increment does not need to be large, but it must run, save a structured output file, and be explainable by the team.

---

## 5. Market snapshot used by R1

Latest available ETF snapshot from the data pull before writing this draft:

| Proxy | Market meaning | Latest level | R1 reading |
|---|---|---:|---|
| SPY | S&P 500 proxy | 741.75 | Broad market still firm, but R3 seasonality says do not chase with high confidence. |
| QQQ | Nasdaq 100 proxy | 721.34 | Stronger relative setup because Technology remains the best seasonal sector. |
| IWM | Russell 2000 proxy | 292.95 | Vulnerable to FOMC and rate-path uncertainty. |
| XLK | Technology | 184.80 | Best seasonal sector candidate. |
| XLE | Energy | 57.55 | Seasonal short risk; volatile if oil/geopolitics move. |
| XLF | Financials | 53.34 | FOMC/rate-path risk plus seasonal banking headwind. |
| XLB | Materials | 52.18 | Weak seasonal window; cyclical demand risk. |

---

## 6. R1 final W4 prediction draft

**Important:** This is the R1/R3 version. The team should merge it with R4 Macro, R5 Technical, R7 Human Score, and R8 LLM comparison before locking the GitHub release.

| Asset | Direction | Expected weekly range | Confidence | Main reason |
|---|---|---:|---|---|
| SPX | **Flat / Down** | **-0.8% to +0.4%** | Low–Medium | June midterm-year weakness plus FOMC/SEP and options-expiry pressure reduce upside conviction. |
| NDX | **Flat / Up** | **-0.3% to +0.8%** | Low–Medium | Technology still has the clearest positive sector seasonality, so NDX can outperform SPX. |
| IWM | **Down / Flat** | **-1.2% to +0.2%** | Low | Small caps are rate-sensitive and vulnerable if the Fed sounds hawkish. |
| XLK | **Flat / Up** | Relative outperformer | Medium | Technology seasonal long window remains the strongest R3 sector signal. |
| XLE | **Down / Volatile** | Relative underperformer | Medium | Energy seasonal short window is active; oil/geopolitical risk can create volatility. |
| XLF | **Flat / Down** | Relative underperformer | Medium | Financials face seasonal short risk and FOMC uncertainty. |
| XLB | **Down** | Relative underperformer | Medium | Materials seasonal weakness and cyclical sensitivity remain headwinds. |

**R1 final call:**  
The team should lock a **cautious Week 4 call** unless R4/R5 provide strong contrary evidence. R1 should avoid describing the market as broadly bullish. The cleaner narrative is that NDX has relative support from Technology, while SPX is capped by June seasonality and event risk, and IWM is the weakest of the three because of FOMC/rate sensitivity.

---

## 7. Invalidation conditions

The W4 call should be considered wrong if:

1. The FOMC statement, SEP, and press conference are clearly dovish.
2. Bond yields fall after the Fed decision and rate-sensitive sectors rally.
3. SPX breaks higher with broad sector participation, not only mega-cap technology.
4. IWM outperforms SPX and NDX after the Fed decision.
5. XLF and XLB both turn positive with strong breadth.

---

## 8. R1 Monday presentation script

Our Sprint 4 goal was to move from a manual prediction workflow toward a working market-intelligence system. For this week, the Definition of Done is not just a prediction file. It also requires evidence in GitHub, at least three sector signals, a software increment that runs, a README, DECISION.md, a W3 delta report, and the vW24 release tag. Based on the R3 Almanac evidence, I would not support a high-confidence bullish call. Week 4 contains FOMC/SEP risk, options-expiry pressure, and a Juneteenth market closure, all inside a weak June midterm-year context. Our provisional call is SPX flat-to-down, NDX relatively stronger because Technology still has seasonal support, and IWM weaker because small caps are rate-sensitive. Final confidence should remain low-to-medium until Macro, Technical, LLM comparison, and Human Score confirm the call.

---

## 9. R1 final 3 bullet points for presentation

- Sprint goal: ship the first real software increment while still locking a W4 prediction for SPX, NDX, IWM, and at least three sectors.
- DoD status: prediction + sector table + R3 output + DECISION.md + working script + README + W3 delta + `vW24` tag must all be visible in GitHub.
- Final call draft: cautious W4 — SPX flat/down, NDX relative outperformer, IWM most vulnerable; confidence low-to-medium until all roles confirm.

---

## Sources used

- CP3405 DT3 Roadmap: https://dt3-tr2-26-market-intelligence.pages.dev/roadmap/
- Sprint 4 Announcement: https://dt3-tr2-26-market-intelligence.pages.dev/sprint4/
- Roles & Responsibilities: https://dt3-tr2-26-market-intelligence.pages.dev/roles/
- System Architecture: https://dt3-tr2-26-market-intelligence.pages.dev/system/
- Exemplary Solution / Almanac example: https://dt3-tr2-26-market-intelligence.pages.dev/exemplary-solution
- Federal Reserve FOMC calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Federal Reserve June 2026 calendar: https://www.federalreserve.gov/newsevents/2026-june.htm
- Nasdaq 2026 U.S. equity/options holiday calendar: https://www.nasdaqtrader.com/trader.aspx?id=Calendar
- NYSE holiday calendar: https://www.nyse.com/trade/hours-calendars
- Cboe 2026 options expiration calendar: https://cdn.cboe.com/resources/options/Cboe2026OPTIONSCalendar.pdf
- Reuters macro context, 9–10 Jun 2026: Fed hold-rate expectation and persistent inflation risk.
