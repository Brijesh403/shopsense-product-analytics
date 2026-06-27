# 🛍️ ShopSense Product Analytics
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![SQL](https://img.shields.io/badge/SQL-MySQL-blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-orange)
![Rows](https://img.shields.io/badge/Data-20.7M%20Rows-red)

## 📌 Business Context

ShopSense is a D2C cosmetics e-commerce store — a portfolio case built on a
**public GA4-style ecommerce events dataset (~20.7M rows)**. As a Product Analyst,
I investigated why users drop off between **product view and first purchase**, and
why retention is low after the first order. *(All revenue figures are in USD, as
per the source dataset.)*

## ❓ Business Questions Answered

1. Where exactly are users dropping off in the purchase funnel?
2. What is our Day 1, Day 7, and Day 30 retention rate?
3. Which monthly user cohorts generate the most revenue?
4. What is the Monthly Active User (MAU) trend over 5 months?
5. What is the Average Revenue Per User (ARPU)?
6. Which product categories drive the most conversions?

## 🔑 Key Findings (TL;DR)

> Full write-up in [`reports/executive_summary.md`](reports/executive_summary.md).

- **The funnel leaks at the top, not at checkout.** Only **24.9%** of viewers add to cart and just **6.9%** ever purchase — the biggest loss is awareness→intent.
- **Cart abandonment is the #1 revenue leak.** **72.5%** of users who add to cart never buy.
- **Retention is acquisition-dependent.** The Oct-2019 cohort retained at **18.5%** in Month 1 — nearly 2× every later cohort, pointing to a one-off acquisition spike and no durable retention engine.
- **Revenue is promotion-driven and volatile.** Month-over-month swing from **+26%** (Nov) to **−29.6%** (Dec).
- **Value is highly concentrated.** **14,139 "Champion" users (13% of buyers)** average **$215** each, while **59% of buyers are "At Risk."**
- **Best conversion window is 9 AM–1 PM** (~6% vs ~3.5% overnight) — a free lever for promo timing.

**Scale:** 20.7M events · 1.6M users · 110,518 buyers · $6.35M revenue · ARPU $57.47.

| Recommendation | Expected Impact |
|----------------|-----------------|
| Cart-abandonment retargeting within 2 hrs | Recover the largest near-term revenue pool |
| Win-back campaign for 65K At-Risk users | Protect existing revenue base |
| Investigate December revenue drop | Fix seasonality / campaign gap |
| Schedule promos for the 9 AM–1 PM peak | Lift conversion at zero cost |

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

- **Source:** Public GA4-style ecommerce behavioral events (cosmetics retailer), framed here as the "ShopSense" D2C case
- **Size:** ~20.7 million events across 5 months (Oct 2019 – Feb 2020)
- **Events:** `view` → `cart` → `remove_from_cart` → `purchase`
- **Currency:** USD (as per source data)

## 📸 Key Visualizations

### Monthly Revenue Trend
![Revenue](dashboards/screenshots/01_monthly_revenue.png)

### Conversion Funnel
![Funnel](dashboards/screenshots/02_funnel_chart.png)

### Cohort Retention Heatmap
![Cohort](dashboards/screenshots/03_cohort_heatmap.png)

### User Segmentation
![Segments](dashboards/screenshots/04_user_segments.png)

### Hourly Conversion Rate
![Hourly](dashboards/screenshots/05_hourly_conversion.png)

### Top Brands by Revenue
![Brands](dashboards/screenshots/06_top_brands.png)
---

**Brijesh Vaghela** · [LinkedIn](https://www.linkedin.com/in/brijesh-vaghela) · [GitHub](https://github.com/Brijesh403)