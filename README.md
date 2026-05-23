# 🛍️ ShopSense Product Analytics

## 📌 Business Context

ShopSense is a D2C e-commerce app serving Indian consumers.
As a Product Analyst, I was tasked with investigating why users
drop off between signup and first purchase, and why retention
is low after the first order.

## ❓ Business Questions Answered

1. Where exactly are users dropping off in the purchase funnel?
2. What is our Day 1, Day 7, and Day 30 retention rate?
3. Which monthly user cohorts generate the most revenue?
4. What is the Monthly Active User (MAU) trend over 5 months?
5. What is the Average Revenue Per User (ARPU)?
6. Which product categories drive the most conversions?

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| MySQL 8.0 | Data storage and SQL analysis |
| Python 3.11 | Data cleaning and EDA |
| Pandas / Seaborn / Matplotlib | Analysis and visualization |
| Power BI | Executive dashboard |
| Git + GitHub | Version control and portfolio |

## 📁 Project Structure

```
shopsense-product-analytics/
│
├── data/
│   ├── raw/                ← Original datasets (not uploaded)
│   └── cleaned/            ← Processed datasets (not uploaded)
│
├── sql/
│   ├── schema/             ← Table creation scripts
│   ├── analysis/           ← Funnel, retention, cohort queries
│   └── kpis/               ← KPI metric queries
│
├── notebooks/              ← Python EDA notebooks
│
├── dashboards/
│   └── screenshots/        ← Power BI dashboard exports
│
├── reports/                ← Final summary reports
│
└── docs/
    ├── kpi_definitions.md  ← All KPI definitions
    └── business_questions.md ← Business questions tracker
```

## 📊 Key KPIs Tracked

| KPI | Definition |
|-----|-----------|
| DAU / WAU / MAU | Daily / Weekly / Monthly Active Users |
| Retention Rate | % of users returning on Day 1, 7, 30 |
| Churn Rate | % of users who never returned |
| Conversion Rate | % of viewers who completed a purchase |
| ARPU | Average Revenue Per User |
| Funnel Drop-off Rate | % lost at each funnel stage |

## 📈 Dataset

- **Source:** GA4-style ecommerce behavioral event data
- **Size:** ~20 million rows across 5 months
- **Events:** `view` → `cart` → `remove_from_cart` → `purchase`

## 🚧 Project Status

| Phase | Status |
|-------|--------|
| Setup & Structure | ✅ Complete |
| Database Schema | 🔄 In Progress |
| SQL Analysis | ⏳ Upcoming |
| Python EDA | ⏳ Upcoming |
| Power BI Dashboard | ⏳ Upcoming |