# Notebooks & Pipeline Scripts

Python scripts and notebooks for data ingestion, exploration, dashboard prep, and
A/B test analysis.

## Contents

| File | Purpose |
|------|---------|
| `01_load_data.py` | Chunked pipeline loading 20.7M rows of CSV into MySQL with cleaning applied per chunk |
| `02_eda_analysis.ipynb` | Exploratory analysis producing 6 publication-quality charts |
| `03_export_for_powerbi.py` | Exports aggregated query results to CSV for the Power BI layer |
| `04_ab_test_power.py` | Sample-size / power analysis for the simulated cart-abandonment A/B test |
| `05_ab_test_simulation.py` | Random group assignment + simulated treatment effect on real abandoner data |
| `06_ab_test_significance.py` | Two-proportion Z-test on the simulated results |

## Stack
Python 3.11 · pandas · SQLAlchemy · statsmodels · Matplotlib · Seaborn

## Setup
DB credentials are read from environment variables, never hardcoded:
```
DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
```
See the repo root `requirements.txt` for dependencies.

> Chunked loading keeps memory stable while processing ~2.4 GB of source data.