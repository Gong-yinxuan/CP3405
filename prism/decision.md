# Week 6 Automation Decision

## Objective

The objective for Week 6 was to improve Prism from a partial automation tool into a more complete market intelligence pipeline. The team needed the system to support the vW28 prediction by collecting market data, covering all 11 S&P sectors, running automated LLM synthesis, and producing delta score / calibration outputs with less manual work.

## What We Chose to Automate

The team chose to automate two main parts of the workflow:

1. **LLM synthesis**
   - Instead of manually asking multiple LLMs and copying their answers into a table, Prism will call at least two LLMs through API.
   - The responses will be saved automatically.
   - The system will compare the responses so the team can review agreement, disagreement, and confidence.

2. **Delta score and calibration**
   - Instead of manually comparing the previous prediction against actual market results, Prism will read the prediction JSON and actual market data.
   - The system will calculate direction accuracy, range accuracy, average error size, and calibration bias.
   - The result will be saved as a delta report and added to cumulative accuracy history.

## Why We Chose These Steps

We chose these steps because they are repeated every sprint and are easy to make mistakes on when done manually. LLM comparison requires consistent prompts and saved responses, while delta scoring requires accurate comparison between predicted direction and actual weekly movement. Automating these parts makes the pipeline more reliable, easier to demonstrate, and easier to audit in GitHub.

## Automated Market Data Coverage

The automated collector currently gathers data for the main prediction assets:

```python
# Prediction assets
"SPX": "^GSPC",
"NDX": "^NDX",
"IWM": "IWM",
"GOLD": "GC=F",
"WTI": "CL=F",
"US10Y": "^TNX",
"TLT": "TLT",
"VIX": "^VIX",
"BTC": "BTC-USD",