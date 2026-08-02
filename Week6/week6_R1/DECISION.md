# DECISION.md — Sprint 6 R1 Product Owner

**Decision owner:** R1 Product Owner  
**Sprint:** Sprint 6 / vW28  
**Date:** Week 6  
**Decision theme:** Close the audit gap between prediction and measurable outcome.

## Context

The Pipeline Audit identified that the repository already contains partial automation and structured role outputs, but the previous sprint lacked a clearly sealed prediction-to-actuals chain. Week 5 had prediction evidence and structured market data, but actuals and delta score were not clearly packaged as a single audit-ready file.

Sprint 6 requires a stronger increment: automated pipeline, all 11 S&P sectors, at least two LLM API calls, calibration, and a sealed `vW28` tag.

## Decision

**Sprint 6 will treat the missing actuals/delta scoring file as the primary automation gap to close.**

The team will create or update a repeatable calibration artefact:

- `delta_W25.md` for previous-sprint accuracy learning.
- `delta_W28.md` or `actuals_W28.json` path prepared for post-Friday actuals.
- Cumulative accuracy table for W3–W6 where possible.

## Why this is the correct Product Owner decision

This gap matters more than cosmetic improvements because Sprint Review must answer whether the system improved. Without a delta file, the team can show prediction text but cannot prove learning. The Product Owner should prioritise evidence that links forecast → outcome → retrospective improvement.

## Accepted trade-off

The team may keep the prediction narrative concise so effort can be spent on automation evidence, data coverage, and calibration. A polished narrative without a measurable outcome chain is not accepted as full Sprint 6 value.

## Success criteria

- R10 or the relevant calibration owner commits `delta_W25.md` before final sign-off, or clearly explains why actuals are unavailable.
- vW28 prediction file includes all required instruments.
- Final Sprint 6 Discord submission includes the automated run URL and tag URL.
- R1 can explain the delivery chain in one sentence during Monday review.

## Product Owner statement

Sprint 6 should be judged by whether the repo proves a working delivery pipeline, not by whether the written prediction sounds confident. The core value is an inspectable, repeatable system.
