# Notebooks & Pipeline Scripts

Python scripts and notebooks for data ingestion, exploration, and dashboard prep.

## Contents

| File | Purpose |
|------|---------|
| `01_load_data.py` | Chunked pipeline loading 20.7M rows of CSV into MySQL with cleaning applied per chunk |
| `02_eda_analysis.ipynb` | Exploratory analysis producing 6 publication-quality charts |
| `03_export_for_powerbi.py` | Exports aggregated query results to CSV for the Power BI layer |

## Stack
Python 3.11 · pandas · SQLAlchemy · Matplotlib · Seaborn

> Chunked loading keeps memory stable while processing ~2.4 GB of source data.