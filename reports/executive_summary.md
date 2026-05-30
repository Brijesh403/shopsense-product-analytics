# 📑 ShopSense Product Analytics — Executive Summary

**Prepared by:** Brijesh Vaghela
**Role:** Product Analyst
**Dataset:** 20.7M GA4-style behavioral events (Oct 2019 – Feb 2020)

---

## Context

ShopSense is a D2C e-commerce platform. The product team needed to understand
why users drop off before purchasing and why retention is low after the first
order. This analysis covers acquisition, the conversion funnel, retention, and
revenue across 5 months and 1.6M users.

---

## Headline Findings

**1. The funnel leaks badly at the top.**
Only 24.93% of viewers add to cart, and just 6.92% of viewers ever purchase.
The biggest single leak is awareness-to-intent, not checkout.

**2. Cart abandonment is the #1 revenue problem.**
72.48% of users who add to cart never buy. Recovering even a fraction of these
represents the largest near-term revenue opportunity.

**3. Retention is acquisition-dependent.**
The October cohort retained at 18.49% (Month 1) — nearly double every later
cohort. This points to a strong but unrepeated October acquisition event, and a
lack of a sustainable retention engine afterward.

**4. Revenue is volatile and seasonal.**
Revenue swung from +26% (November) to -29.6% (December) month-over-month,
suggesting heavy reliance on promotions rather than organic demand.

**5. Value is highly concentrated.**
14,139 "Champion" users (13% of buyers) generate $215 each on average, while
59% of buyers are "At Risk" of churning.

---

## Recommendations

| Priority | Action | Expected Impact |
|----------|--------|-----------------|
| High | Cart-abandonment retargeting within 2 hrs | Recover lost checkout revenue |
| High | Win-back campaign for 65K At-Risk users | Protect existing revenue base |
| Medium | Investigate December revenue drop | Fix seasonality/campaign gap |
| Medium | Schedule promos for 9 AM–1 PM peak window | Lift conversion at no cost |
| Low | Premium placement for top-converting brands | Incremental conversion gains |

---

## Methodology

- **Storage & querying:** MySQL 8.0 (20.7M rows, indexed for performance)
- **Pipeline:** Python chunked loading; data cleaning via a SQL view
- **Analysis:** Funnel, cohort retention, RFM segmentation, revenue KPIs in SQL
- **Visualization:** Python (Matplotlib/Seaborn) + 4-page Power BI dashboard

A note on data quality: `category_code` was 98% NULL and `brand` 42% NULL.
These were handled in a clean view; category-level analysis used `category_id`.

---

## Limitations

- Some high-conversion brand figures (e.g. eunyul) come from small samples and
  should be treated as signals to investigate, not proven patterns.
- Data covers 5 months only; longer-term retention curves cannot yet be confirmed.