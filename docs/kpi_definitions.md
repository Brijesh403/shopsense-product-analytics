# KPI Definitions — ShopSense Product Analytics

## 📌 Purpose
This document defines every KPI used in this project.
All definitions follow industry-standard product analytics practices.

---

## 👥 User Metrics

| KPI | Definition | Formula |
|-----|-----------|---------|
| DAU | Daily Active Users — unique users who performed any event in a day | COUNT(DISTINCT user_id) per day |
| WAU | Weekly Active Users — unique users active in a 7-day window | COUNT(DISTINCT user_id) per week |
| MAU | Monthly Active Users — unique users active in a 30-day window | COUNT(DISTINCT user_id) per month |
| New Users | Users whose first event falls within the period | MIN(event_time) within period |
| Returning Users | Users who were active in a previous period and returned | user_id present in both periods |

---

## 🔻 Funnel Metrics

| KPI | Definition | Formula |
|-----|-----------|---------|
| View-to-Cart Rate | % of viewers who added to cart | cart_users / view_users × 100 |
| Cart-to-Purchase Rate | % of cart users who completed purchase | buyers / cart_users × 100 |
| Overall Conversion Rate | % of viewers who completed purchase | buyers / view_users × 100 |
| Cart Abandonment Rate | % of cart users who never purchased | (cart_users - buyers) / cart_users × 100 |
| Funnel Drop-off Rate | % of users lost between two consecutive stages | (stage_n - stage_n+1) / stage_n × 100 |

---

## 💰 Revenue Metrics

| KPI | Definition | Formula |
|-----|-----------|---------|
| Total Revenue | Sum of all purchase event prices | SUM(price) WHERE event_type = 'purchase' |
| ARPU | Average Revenue Per User | Total Revenue / Unique Buyers |
| ARPPU | Average Revenue Per Paying User | Total Revenue / Unique Purchasers |
| AOV | Average Order Value | Total Revenue / Total Orders |
| Revenue per Session | Average revenue generated per session | Total Revenue / Unique Sessions |

---

## 🔁 Retention Metrics

| KPI | Definition | Formula |
|-----|-----------|---------|
| Day 1 Retention | % of new users who return next day | Users active on Day 1 / New Users × 100 |
| Day 7 Retention | % of new users who return within 7 days | Users active on Day 7 / New Users × 100 |
| Day 30 Retention | % of new users who return within 30 days | Users active on Day 30 / New Users × 100 |
| Churn Rate | % of users who never returned after first visit | Lost Users / Total Users × 100 |
| Cohort Retention | Retention tracked by acquisition month group | Active users in month N / Cohort size × 100 |

---

## 📊 Engagement Metrics

| KPI | Definition | Formula |
|-----|-----------|---------|
| Sessions per User | Average number of sessions per user | Unique Sessions / Unique Users |
| Events per Session | Average events triggered per session | Total Events / Unique Sessions |
| DAU/MAU Ratio | Stickiness — how often monthly users return daily | DAU / MAU × 100 |

---

## 🏆 Our Project Findings

| KPI | Value Found |
|-----|------------|
| Total Users | 1,639,358 |
| Total Sessions | 4,535,941 |
| Sessions per User | 2.77 |
| Overall Conversion Rate | 6.92% |
| View-to-Cart Rate | 24.93% |
| Cart-to-Purchase Rate | 27.75% |
| Cart Abandonment Rate | 72.48% |
| Peak Conversion Hour | 11 AM (6.04%) |
| Best Converting Brand | eunyul (51.32%) |
| Data Coverage | 151 days (Oct 2019 — Feb 2020) |

---

## 📝 Data Quality Notes

| Column | Issue | Resolution |
|--------|-------|-----------|
| category_code | 98.29% NULL | Use category_id instead |
| brand | 42.32% NULL | Replaced with 'unknown' in clean view |
| price | 0.50% zero/negative | Excluded in clean view |
| user_session | 0.02% NULL | Excluded in clean view |
| remove_from_cart | Duplicate events | Deduplicated via GROUP BY |