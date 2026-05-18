# FUTURE_DS_02
# 📉 Telco Customer Churn Analysis

A complete **retention analytics pipeline** for subscription and SaaS businesses — built on a real-world telecom dataset of 7,043 customers. This project identifies why customers leave, which segments are most at risk, and what actions can meaningfully reduce churn.

> Built for product managers, startup founders, and business stakeholders who need clear, actionable retention intelligence — not just charts.

---

## 📊 Key Findings

| Metric | Value |
|---|---|
| Overall Churn Rate | **26.5%** |
| Monthly Revenue at Risk | **$139,131** |
| Avg CLV — Churned Customer | **$1,532** |
| Avg CLV — Retained Customer | **$2,550** |
| Highest-Risk Segment Churn | **60.4%** (M2M + Fibre + E-check) |

**The three biggest levers:**
- 🔴 Month-to-month customers churn at **42.7%** vs **2.8%** on two-year contracts
- 🔴 New customers (0–6 months) churn at **53.3%** — the critical drop-off window
- 🟢 Online Security & Tech Support users churn at only **~15%** vs **42%** without add-ons

---

## 📁 Project Structure

```
telco-churn-analysis/
│
├── Telco-Customer-Churn.csv          # Source dataset (7,043 customers, 21 features)
├── telco_churn_analysis.py           # Main analysis script — cleans data, runs analysis, saves charts
├── Telco_Retention_Analysis_Report.docx  # Executive Word report with embedded charts
├── README.md
│
└── churn_charts/                     # Auto-generated on script run
    ├── 01_churn_by_contract.png
    ├── 02_churn_by_tenure.png
    ├── 03_churn_by_internet.png
    ├── 04_churn_by_payment.png
    ├── 05_retention_drivers.png
    ├── 06_monthly_charges_dist.png
    └── 07_heatmap_contract_internet.png
```

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-username/telco-churn-analysis.git
cd telco-churn-analysis
```

### 2. Install dependencies

```bash
pip install pandas matplotlib seaborn scikit-learn
```

### 3. Run the analysis

```bash
python telco_churn_analysis.py
```

The script will:
- Load and clean the dataset
- Print a full summary and high-risk segment breakdown to the terminal
- Save 7 charts to `./churn_charts/`

---

## 📦 Dataset

**Source:** [IBM Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

7,043 customers × 21 features including:

| Feature | Description |
|---|---|
| `tenure` | Months the customer has been active |
| `Contract` | Month-to-month, One year, Two year |
| `InternetService` | DSL, Fiber optic, None |
| `PaymentMethod` | Electronic check, Mailed check, Bank transfer, Credit card |
| `MonthlyCharges` | Current monthly bill |
| `TotalCharges` | Total spend to date |
| `OnlineSecurity` / `TechSupport` | Value-added service flags |
| `Churn` | Target variable — Yes / No |

---

## 📈 Charts Generated

| # | Chart | What It Shows |
|---|---|---|
| 01 | Churn by Contract Type | Month-to-month vs annual vs two-year |
| 02 | Churn by Tenure | Drop-off curve across customer lifecycle |
| 03 | Churn by Internet Service | Fibre vs DSL vs no internet |
| 04 | Churn by Payment Method | E-cheque vs automatic methods |
| 05 | Retention Drivers | Impact of add-ons on churn rate |
| 06 | Monthly Charges Distribution | Churned vs retained customers |
| 07 | Contract × Internet Heatmap | Highest-risk segment intersections |

---

## 🧠 Analysis Breakdown

### Data Cleaning
- `TotalCharges` coerced from string to numeric (11 blank rows filled with `MonthlyCharges`)
- Binary churn flag (`Churned`) added for aggregation
- Tenure bucketed into five cohort bands
- Customer Lifetime Value (CLV) estimated as `MonthlyCharges × tenure`

### Segments Analysed
- Contract type
- Tenure cohort (0–6m, 7–12m, 13–24m, 25–36m, 37–72m)
- Internet service type
- Payment method
- Value-added services (Online Security, Tech Support, Online Backup)
- Demographics (Senior citizen, Partner, Dependents)
- Price sensitivity (Monthly charges distribution)

### High-Risk Segments Identified

| Segment | Customers | Churn Rate |
|---|---|---|
| Month-to-month + Fibre + Electronic check | 1,307 | 60.4% |
| Month-to-month + No security add-on | 2,631 | 51.0% |
| Senior citizens on month-to-month | 807 | 54.6% |
| Tenure under 6 months | 1,481 | 52.9% |

---

## 📋 Strategic Recommendations Summary

| Priority | Initiative | Expected Impact |
|---|---|---|
| P0 | Contract conversion campaign (M2M → annual) | ~5 pp churn reduction |
| P0 | 90-day onboarding journey for new customers | 0–6mo churn from 53% → ~40% |
| P1 | Add-on upsell to unprotected internet customers | Segment churn from 51% → ~28% |
| P1 | Payment method migration (e-cheque → auto-pay) | Segment churn from 45% → ~16% |
| P2 | Fibre loyalty programme & quality initiative | Fibre churn from 42% → <25% |

Full analysis with data tables, charts, and implementation roadmap available in [`Telco_Retention_Analysis_Report.docx`](./Telco_Retention_Analysis_Report.docx).

---

## 🛠️ Requirements

```
python >= 3.8
pandas
matplotlib
seaborn
scikit-learn
numpy
```

---

## 📄 License

MIT License. Dataset sourced from IBM Sample Data via Kaggle — free for educational and analytical use.

---

## 🙋 Use Cases

This project is a practical template for:
- **SaaS companies** analysing subscription churn
- **Telcos and utilities** tracking customer attrition
- **Data analysts** building a portfolio retention project
- **Product and growth teams** identifying where to intervene in the customer lifecycle

Swap in your own dataset with the same column structure and the pipeline runs end-to-end.
