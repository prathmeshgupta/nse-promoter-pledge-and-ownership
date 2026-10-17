# NSE Promoter Pledge & Shareholding Ownership Registry

[![Weekly Promoter Pledge Dataset Update](https://github.com/prathmeshgupta/nse-promoter-pledge-and-ownership/actions/workflows/weekly_update.yml/badge.svg)](https://github.com/prathmeshgupta/nse-promoter-pledge-and-ownership/actions/workflows/weekly_update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Audited, quarterly Point-in-Time dataset of National Stock Exchange of India (NSE) **promoter holdings, pledged shares percentages, institutional ownership, and public float**.

Provides an essential corporate governance and left-tail risk filter to protect quantitative portfolios from catastrophic promoter margin-call liquidations.

---

### The Quantitative Problem (Left-Tail Liquidation Risk)

In Indian mid-cap and small-cap investing, **promoter share pledging is the leading structural trigger of catastrophic -50% to -90% drawdowns**:

1. **The Margin-Call Death Spiral:** When promoters borrow personal or corporate debt by pledging equity shares as collateral, any market decline forces lenders to issue margin calls. If the promoter cannot meet the call with cash, lenders sell pledged shares directly into the open market, causing consecutive lower circuits.
2. **Quantitative Gating Rules:**
   - **`CRITICAL_MARGIN_CALL_RISK`**: Pledged Shares $\ge 25.0\%$ of promoter holding. (Mandatory systematic exclusion in institutional strategies).
   - **`MODERATE_PLEDGE_RISK`**: $10.0\% \le \text{Pledge} < 25.0\%$.
   - **`ZERO_PLEDGE`**: Pristine governance tier (e.g. TCS, Infosys, Reliance, HDFC Bank).

---

### Dataset Schema

Outputs are distributed in both **Apache Parquet (`snappy` compressed)** and standard **CSV**:
* `output/promoter_pledge_ownership.parquet`
* `output/promoter_pledge_ownership.csv`

| Field | Type | Description |
| :--- | :--- | :--- |
| `symbol` | `string` | NSE Trading Symbol (e.g. `VEDL`, `TCS`, `INFY`) |
| `quarter_ended` | `string` | Filing quarter end date (`YYYY-MM-DD`) |
| `filing_date` | `string` | Statutory SEBI filing date |
| `promoter_holding_pct` | `float` | Aggregate shares held by promoter & promoter group (`0.0%` to `100.0%`) |
| `promoter_pledged_pct` | `float` | Proportion of promoter holding pledged as collateral (`0.0%` to `100.0%`) |
| `institutional_holding_pct` | `float` | Shares held by domestic mutual funds and FIIs |
| `institutional_holders_count` | `int64` | Total number of institutional shareholders |
| `public_float_pct` | `float` | Estimated public float |
| `pledge_risk_category` | `string` | `CRITICAL_MARGIN_CALL_RISK`, `MODERATE_PLEDGE_RISK`, `ZERO_PLEDGE` |
| `source` | `string` | Origin (`SEBI_REG31_SHAREHOLDING`) |

---

### Automated Weekly Updates

* **Schedule**: Automated GitHub Actions workflow executes every **Sunday at 02:00 UTC (07:30 IST)**.
* **Integrity Gate**: Validates that all ownership and pledge percentages satisfy $0.0 \le \text{Value} \le 100.0$.

---

### Quickstart & CLI Usage

```bash
# 1. Clone the repository
git clone https://github.com/prathmeshgupta/nse-promoter-pledge-and-ownership.git
cd nse-promoter-pledge-and-ownership

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated updater locally
python update.py

# 4. View scrips with elevated promoter pledges (>= 10%)
python runner.py --high-pledge

# 5. Check a specific ticker
python runner.py --symbol VEDL
```
