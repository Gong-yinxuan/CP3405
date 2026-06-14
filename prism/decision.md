# Week 4 Automation Decision
### Objective

For Week 4, the team was required to move from a manual workflow toward an automated software increment. Rather than attempting to automate the entire Almanac Agent system at once, the team selected a single high-value and low-risk automation step to establish a reliable foundation for future development.

### What We Chose to Automate

The team chose to automate the market data collection stage of the pipeline.

A Python script was developed to automatically retrieve market data using Yahoo Finance (yfinance) and generate structured output in JSON format.

### The automated collector currently gathers:

S&P 500 proxy (SPY)
Nasdaq 100 proxy (QQQ)
Russell 2000 proxy (IWM)
Selected S&P 500 sector ETFs

The output is saved into a structured file (output.json) for downstream analysis.