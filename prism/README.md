# Market Data Collector — Level 2 → 3 Pipeline

## Project Overview

This project implements a minimal automated data pipeline as part of the **Level 2 → 3** stage of the Almanac Agent system.

The pipeline:
1. Fetches the latest closing prices for **SPY**, **QQQ**,**IWM**， **XLK**，**XUL**， and **XLV** from Yahoo Finance.
2. Structures the data into a JSON file (`output.json`).
3. Commits the file to this GitHub repository automatically via GitHub Actions.

> **Scope note:** This stage is a *data collection pipeline only*. No machine learning, prediction, or financial analysis is performed here. Those features are introduced in Level 3 and Level 4.

---
，
## Data Sources

| Ticker | Index Represented          | Source        |
|--------|---------------------------|---------------|
| SPY    | S&P 500 (large-cap)       | Yahoo Finance |
| QQQ    | Nasdaq 100 (tech-heavy)   | Yahoo Finance |
| IWM    | Russell 2000 (small-cap)  | Yahoo Finance |
| XLK    | Techonology Sector ETF    | Yahoo Finance |
| XLU    | Utilities Sector ETF      | Yahoo Finance |
| XLV    | Health Care Sector ETF    | Yahoo Finance |

---

## Output Format

Each execution generates (or overwrites) `output.json` with the following structure:

```json
{
  "date": "YYYY-MM-DD",
  "SPY": 000.00,
  "QQQ": 000.00,
  "IWM": 000.00,
  "XLK": { "close": 000.00, "weekly_change_pct": 0.0 },
  "XLU": { "close": 000.00, "weekly_change_pct": 0.0 },
  "XLV": { "close": 000.00, "weekly_change_pct": 0.0 }
}
```

- **One record per run** — the file is overwritten on each execution.
- **Closing price** (or latest available price if the market is still open) is used.
- **weekly change pct** — percentage change over the past 5 trading days.
- **No comments or extra fields** — the format is intentionally machine-readable to support future AI/agent modules.

---

## Running Locally

### Prerequisites

- Python 3.9 or higher
- `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-org>/<your-repo>.git

# Install the only dependency
pip install yfinance
```

### Execution

```bash
python collect_market_data.py
```

After the script completes you will see:

```
Fetching market data …
Data collected: {
  "date": "2026-06-12",
  "SPY": {
    "close": 737.76,
    "weekly_change_pct": -2.6
  },
  "QQQ": {
    "close": 717.12,
    "weekly_change_pct": -3.2
  },
  "IWM": {
    "close": 290.41,
    "weekly_change_pct": -0.5
  },
  "XLK": {
    "close": 183.21,
    "weekly_change_pct": -5.2
  },
  "XLU": {
    "close": 44.05,
    "weekly_change_pct": 0.3
  },
  "XLV": {
    "close": 154.09,
    "weekly_change_pct": 1.3
  }
}
[OK] output written to 'output.json'
```

### Success Criteria

- [ ] Script runs without errors
- [ ] `output.json` is generated in the project root
- [ ] All three values (`SPY`, `QQQ`, `IWM`, `XLK`, `XLU`, `XLV`) are valid numbers
- [ ] The JSON structure matches the specification above

---

## GitHub Actions Automation

The workflow file is located at `.github/workflows/market_data.yml`.

### Triggers

| Trigger            | When it runs                                  |
|--------------------|-----------------------------------------------|
| `workflow_dispatch` | Manually via the **Actions** tab on GitHub   |
| `schedule` (cron)  | Every Monday at 09:00 UTC automatically      |

### What the workflow does

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs `yfinance`.
4. Runs `collect_market_data.py`.
5. Commits and pushes the updated `output.json` (only if the file changed).

### How to trigger manually

1. Go to the **Actions** tab in this repository.
2. Select **Market Data Collector**.
3. Click **Run workflow** → **Run workflow**.

---

## Future Compatibility

Although the system is intentionally simple, the JSON schema is designed to support future upgrades:

| Level | Feature |
|-------|---------|
| Level 3 | LLM-based market prediction agent |
| Level 3+ | Delta comparison engine (prediction vs actual) |
| Level 4 | Full intelligent dashboard system |

Keeping field names (`SPY`, `QQQ`, `IWM`) and date format (`YYYY-MM-DD`) consistent is critical for these future modules to work without modification.

---

## Team Roles (Task Allocation)

| Role | Person | Responsibility |
|------|--------|---------------|
| Data Source Research | Person 1 | Selected Yahoo Finance; defined tickers |
| Data Collection Script | Person 2 | Developed `collect_market_data.py` |
| Data Structure Design | Person 3 | Defined JSON schema and field naming |
| GitHub Automation | Person 4 | Configured `market_data.yml` workflow |
| Documentation | Person 5 | Wrote this README |
| Testing & Validation | Person 6 | Verified script output and Actions run |
| Integration & Submission | Person 7 | Prepared submission materials |

---

## License

This project is for educational purposes as part of a Design Thinking course assignment.
