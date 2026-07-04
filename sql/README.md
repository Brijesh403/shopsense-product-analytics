# SQL Layer

All analytical logic for the ShopSense project, written for MySQL 8.0 and executed
against 20.7M+ behavioral events. Scripts are numbered in execution order.

## Structure

| Folder | Script | Purpose |
|--------|--------|---------|
| `schema/` | `01_create_tables.sql` | Table definitions, data types, and performance indexes |
| `analysis/` | `01_data_cleaning.sql` | Profiling, NULL/quality checks, and the `clean_events` view |
| `analysis/` | `02_funnel_analysis.sql` | View → cart → purchase conversion and drop-off rates |
| `analysis/` | `03_retention_analysis.sql` | Cohort retention matrix and Day 1/7/30 retention |
| `analysis/` | `04_segment_cart_abandonment.sql` | Cart abandonment rate by RFM segment, feeding the significance test in `notebooks/statistical_tests/` |
| `kpis/` | `01_revenue_kpis.sql` | ARPU, AOV, revenue trends, MoM growth, RFM segmentation |

## Techniques Demonstrated
CTEs · window functions (`LAG`, `OVER`) · `PERIOD_DIFF` cohort logic ·
conditional aggregation · views · index-based performance tuning.

> All downstream analysis reads from the `clean_events` view, never the raw table.