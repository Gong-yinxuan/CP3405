# Sprint 9 Final Retrospective — vW31

**Retrospective date:** Sunday 2 August 2026  
**Scrum Master:** R2 — Jinsong Jiang  
**Demo Day:** Monday 3 August 2026

## 1. Sprint Goal Evaluation

**Goal:** Deliver a reliable, clear and audit-ready vW31 increment, prepare each role's Demo Day segment and seal the project with the final tag.

**Status at repository audit:** **Partial — sign-off withheld**

R1, R3, R4, R5 and R8 evidence is substantially present. However, the repository still shows DoD risks: R2 evidence was missing, R6/R7/R9 Week9 evidence was not visible, R8 used a W30 filename, required Human Quality Gate sections were absent, R10 structure/history was unclear and the final `vW31` tag was not visible.

R2 should change the status to **Achieved** only after every final check is supported by visible evidence.

## 2. What Went Well

- **Real upstream evidence:** R3, R4 and R5 produced substantial reports for the final synthesis.
- **Four-model synthesis:** R8 saved ChatGPT, Gemini, DeepSeek and Claude-stream JSON outputs.
- **Fallback resilience:** the synthesis records that the Claude connection dropped and the workflow automatically switched to an OpenRouter free fallback.
- **Hardening knowledge:** Sprint 8's date-integrity and two-stage calibration learning was retained.
- **Automation history:** recent scheduled `Update Market Data` runs provide evidence that the pipeline is no longer purely manual.

## 3. What Did Not Go Well

- The mandatory R2 mid-week artefact was not visible early enough.
- R3/R4/R5 reports existed without the required Human Quality Gate heading.
- R8's synthesis content is Week 31 but the filename says W30.
- R6, R7 and R9 final Week9 evidence was not inspectable during the audit.
- R10 content used an incorrect nested path and an outdated Week 8 README.
- Demo Day role/evidence readiness was not visibly locked early enough.

## 4. Blocker Timeline

| Time | Blocker | Required R2 action |
|---|---|---|
| Wednesday | Human Quality Gate sections missing | Return files to R3/R4/R5 before accepting the synthesis gate |
| Thursday | R8 W30/W31 filename mismatch | Rename before R7 handoff |
| Friday–Saturday | R6/R7 evidence not visible | Escalate and define a final evidence deadline |
| Saturday | R10 path and cumulative history incomplete | Require corrected structure and W22–W31 table |
| Sunday | Final tag not visible | Withhold R2 approval |

## 5. Comparison with Sprint 8

Sprint 8's major issues were provider failure and prediction-versus-actuals date mismatch. The team responded with fallback behaviour and safer calibration logic.

Sprint 9's major risks shifted toward **release discipline**: naming, folder structure, quality-gate evidence, segment readiness and final sign-off. The system became more resilient, but release governance still needed improvement.

## 6. One Specific Process Change

### Automated pre-tag release audit

Before R9 creates a tag, one script should verify:

- every role folder and W31 file exists;
- R3/R4/R5 contain the Human Quality Gate heading;
- four R8 outputs and the W31 synthesis exist;
- R7 final prediction exists;
- R10 cumulative W22–W31 table exists;
- latest scheduled Actions proof is recorded;
- no W30 filename remains in Week9;
- R2 retrospective and role assignment exist.

Any failed check should stop the release and print a clear error.

## 7. Final Learning

PRISM evolved from manually assembled market notes into a structured multi-agent pipeline with automation, LLM comparison, fallback handling, Human Score and calibration.

The final lesson is that system quality is not only whether code runs. A professional increment must be traceable, consistently named, manually validated where required and inspectable by someone outside the team.

## 8. R2 Sign-Off

**Current decision:** **NOT YET APPROVED**

R2 approves `vW31` only when all mandatory files are merged, the final Actions run is verified, every role's Demo Day evidence is confirmed, the cumulative table is present and all DoD defects are closed.
