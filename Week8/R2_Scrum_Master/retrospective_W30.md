# Sprint 8 Retrospective Report (vW29)
**Date:** 
**Scrum Master:** R2 - To Hoang Gia

## 🎯 Sprint Goal Evaluation
* **Goal Status:** In Progress
* **Summary:** Successfully delivered an audit-ready vW30 market-intelligence increment before the 23:59 SGT deadline. All 11 S&P sector ETFs were integrated into the pipeline, and the final prediction has been successfully sealed under the `vW29` release tag.

---

## 📈 Metric & Process Performance

### 🔄 1. The Role Rotation & Blocker Resolution
**Blocker:** Both `tencent/hy3` on OpenRouter and Claude on Anthropic required paid account credits that the team did not have institutional or personal-payment access to fund for coursework. OpenRouter's promotional free tier for Hy3 ended July 21, one day before this sprint's synthesis run, and the newly created Anthropic Console account did not carry usable trial credits. This is a policy/access constraint, not a technical one.

**Response:** Separated the Claude and Hy3 call paths in `llm_synthesis.py`, added strict hyperparameter bounds and a reasoning-tag cleanup pass for Hy3's output, and built a three-layer fallback chain: Hy3 → Claude → OpenRouter's free-tier auto-router (`openrouter/free`), with an automatic retry on the free tier since it routes to a different model each call. Every substitution is logged and surfaced as a visible warning in the generated report, so no fallback is silent.

**Outcome:** Verified via a live manual run on July 23 — with both Hy3 and Claude unavailable, the pipeline still completed successfully with zero crashes, produced all required output files (`synthesis_claude_hy3_W08.json`, `llm_synthesis_W30.md`, plus the four other per-model JSON files), and clearly flagged every fallback substitution in both the raw JSON (`_fallback_warning` field) and the human-readable report ("⚠️ Fallback Notices" section). This demonstrates the resilience the Sprint Goal required, independent of any single vendor's payment status.

### ⚙️ 2. Workflow & Automation Highlights


---

## 🛑 Engineering Pitfalls & Course Corrections

### ⚠️ Premature Release Tagging

---

## 🚀 Key Takeaways for Sprint 8
