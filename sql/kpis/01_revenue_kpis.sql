-- ============================================
-- ShopSense Product Analytics
-- Script: Revenue and KPI Analysis
-- Author: Brijesh Vaghela
-- Business Question: What is our revenue health?
-- ============================================

USE shopsense;

-- ============================================
-- QUERY 1: MONTHLY REVENUE TREND
-- How is revenue growing month over month?
-- ============================================

SELECT
    event_month_str                         AS month,
    COUNT(DISTINCT user_id)                 AS unique_buyers,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(price), 2)                    AS total_revenue,
    ROUND(AVG(price), 2)                    AS avg_order_value,
    ROUND(SUM(price) /
          COUNT(DISTINCT user_id), 2)       AS arpu
FROM clean_events
WHERE event_type = 'purchase'
GROUP BY event_month_str
ORDER BY event_month_str;

-- ============================================
-- QUERY 2: OVERALL PLATFORM KPIs
-- Single number summary for executive report
-- ============================================

SELECT
    COUNT(DISTINCT user_id)                 AS total_buyers,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(price), 2)                    AS total_revenue,
    ROUND(AVG(price), 2)                    AS avg_order_value,
    ROUND(SUM(price) /
          COUNT(DISTINCT user_id), 2)       AS overall_arpu,
    ROUND(COUNT(*) /
          COUNT(DISTINCT user_id), 2)       AS avg_orders_per_user
FROM clean_events
WHERE event_type = 'purchase';

-- ============================================
-- QUERY 3: REVENUE BY COHORT
-- Which acquisition cohort generates most revenue?
-- ============================================

SELECT
    uc.cohort_month,
    COUNT(DISTINCT ce.user_id)              AS buyers,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(ce.price), 2)                 AS total_revenue,
    ROUND(SUM(ce.price) /
          COUNT(DISTINCT ce.user_id), 2)    AS arpu,
    ROUND(AVG(ce.price), 2)                 AS avg_order_value
FROM clean_events ce
JOIN user_cohorts uc
    ON ce.user_id = uc.user_id
WHERE ce.event_type = 'purchase'
GROUP BY uc.cohort_month
ORDER BY uc.cohort_month;

-- ============================================
-- QUERY 4: TOP 10 HIGHEST VALUE USERS
-- Who are our best customers?
-- ============================================

SELECT
    user_id,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(price), 2)                    AS total_spent,
    ROUND(AVG(price), 2)                    AS avg_order_value,
    MIN(DATE(event_time))                   AS first_purchase,
    MAX(DATE(event_time))                   AS last_purchase,
    DATEDIFF(
        MAX(DATE(event_time)),
        MIN(DATE(event_time)))              AS customer_lifespan_days
FROM clean_events
WHERE event_type = 'purchase'
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT 10;

-- ============================================
-- QUERY 5: REVENUE BY BRAND
-- Which brands drive the most revenue?
-- ============================================

SELECT
    brand,
    COUNT(DISTINCT user_id)                 AS unique_buyers,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(price), 2)                    AS total_revenue,
    ROUND(AVG(price), 2)                    AS avg_price
FROM clean_events
WHERE event_type = 'purchase'
  AND brand != 'unknown'
GROUP BY brand
ORDER BY total_revenue DESC
LIMIT 10;

-- ============================================
-- QUERY 6: REVENUE BY HOUR OF DAY
-- When does most revenue happen?
-- ============================================

SELECT
    hour_of_day,
    COUNT(*)                                AS total_orders,
    ROUND(SUM(price), 2)                    AS total_revenue,
    ROUND(AVG(price), 2)                    AS avg_order_value
FROM clean_events
WHERE event_type = 'purchase'
GROUP BY hour_of_day
ORDER BY total_revenue DESC
LIMIT 10;

-- ============================================
-- QUERY 7: MONTH OVER MONTH REVENUE GROWTH
-- Is revenue growing or shrinking?
-- ============================================

WITH monthly_revenue AS (
    SELECT
        event_month_str                     AS month,
        ROUND(SUM(price), 2)                AS revenue
    FROM clean_events
    WHERE event_type = 'purchase'
    GROUP BY event_month_str
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER
        (ORDER BY month)                    AS prev_month_revenue,
    ROUND((revenue - LAG(revenue)
        OVER (ORDER BY month)) * 100.0 /
        LAG(revenue)
        OVER (ORDER BY month), 2)           AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;

-- ============================================
-- QUERY 8: USER SEGMENTATION BY VALUE
-- RFM-style segmentation
-- ============================================

WITH user_stats AS (
    SELECT
        user_id,
        COUNT(*)                            AS frequency,
        ROUND(SUM(price), 2)               AS monetary,
        MAX(DATE(event_time))              AS last_purchase
    FROM clean_events
    WHERE event_type = 'purchase'
    GROUP BY user_id
)
SELECT
    CASE
        WHEN monetary >= 100
         AND frequency >= 3  THEN 'Champion'
        WHEN monetary >= 50
         AND frequency >= 2  THEN 'Loyal'
        WHEN frequency = 1
         AND monetary >= 20  THEN 'Promising'
        WHEN frequency = 1   THEN 'New Customer'
        ELSE 'At Risk'
    END                                     AS segment,
    COUNT(*)                                AS user_count,
    ROUND(AVG(monetary), 2)                 AS avg_revenue,
    ROUND(AVG(frequency), 2)                AS avg_orders
FROM user_stats
GROUP BY segment
ORDER BY avg_revenue DESC;