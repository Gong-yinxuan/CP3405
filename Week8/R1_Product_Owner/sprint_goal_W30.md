# Sprint 8 Goal and Definition of Done — R1 Product Owner — vW30
**Team:** Team 5
**Sprint:** Sprint 8 / Week 8
**Forecast tag:** `vW30`
**Due:** Sunday 26 July 2026, 23:59 SGT
**Role:** R1 — Product Owner

## Sprint 8 Goal
Deliver an audit-ready `vW30` market-intelligence increment on time. This sprint requires complete resolution of past sector-coverage gaps, programmatic token regex cleanup for Hy3 model reasoning leaks, and active API failovers configured before the July 21 OpenRouter promotional cutoff.

## Required Delivery Sequence
R3 Almanac + R4 Macro + R5 Technical → R8 LLM Synthesis → R7 Human Score & Full Sector Prediction → R9 vW30 Release

## ✅ Mandatory Acceptance Criteria (DoD)
*   **Sector Coverage Resolution:** The final prediction file MUST provide individual direction and confidence intervals for all 11 sector ETFs (XLK through XLU), completely resolving the Sprint 7 exception.
*   **Hy3 Streaming Token Filter:** R8 must implement code architecture to scrub raw internal reasoning blocks leaking into visible markdown generation streams.
*   **API Promotional Failover:** R9 must configure repository secrets for alternative endpoints (e.g., DeepSeek/Claude) to prevent pipeline failures when free access tier closes on July 21.
*   **Case Casing Rules:** All file deliverables must use strictly lowercase nomenclature to ensure cross-OS git rename safety.
*   **Wednesday Gate Compliance:** R3, R4, and R5 must clear their automated data inputs before the Wednesday 23:59 SGT checkpoint.
