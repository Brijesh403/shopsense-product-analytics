-- ============================================
-- ShopSense Product Analytics
-- Script: Funnel Analysis
-- Author: Brijesh Vaghela
-- Business Question: Where are users dropping off?
-- ============================================

USE shopsense;

-- ============================================
-- QUERY 1: OVERALL FUNNEL
-- How many unique users reach each stage?
-- ============================================

SELECT
    'Step 1 - View'             AS funnel_stage,
    COUNT(DISTINCT user_id)     AS unique_users
FROM clean_events
WHERE event_type = 'view'

UNION ALL

SELECT
    'Step 2 - Cart'             AS funnel_stage,
    COUNT(DISTINCT user_id)     AS unique_users
FROM clean_events
WHERE event_type = 'cart'

UNION ALL

SELECT
    'Step 3 - Purchase'         AS funnel_stage,
    COUNT(DISTINCT user_id)     AS unique_users
FROM clean_events
WHERE event_type = 'purchase';

-- ============================================
-- QUERY 2: FUNNEL WITH DROP-OFF RATES
-- The metric to determine where users are dropping off the most
-- ============================================

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'view'     THEN user_id END) AS viewers,
        COUNT(DISTINCT CASE WHEN event_type = 'cart'     THEN user_id END) AS carters,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS buyers
    FROM clean_events
)
SELECT
    viewers                                                    AS total_viewers,
    carters                                                    AS total_carters,
    buyers                                                     AS total_buyers,
    ROUND(carters  * 100.0 / viewers, 2)                      AS view_to_cart_rate,
    ROUND(buyers   * 100.0 / carters, 2)                      AS cart_to_purchase_rate,
    ROUND(buyers   * 100.0 / viewers, 2)                      AS overall_conversion_rate
FROM funnel;

-- ============================================
-- QUERY 3: MONTHLY FUNNEL TREND
-- Is conversion improving or declining?
-- ============================================

WITH monthly_funnel AS (
    SELECT
        event_month_str,
        COUNT(DISTINCT CASE WHEN event_type = 'view'     THEN user_id END) AS viewers,
        COUNT(DISTINCT CASE WHEN event_type = 'cart'     THEN user_id END) AS carters,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS buyers
    FROM clean_events
    GROUP BY event_month_str
)
SELECT
    event_month_str,
    viewers,
    carters,
    buyers,
    ROUND(carters * 100.0 / viewers, 2)  AS view_to_cart_pct,
    ROUND(buyers  * 100.0 / carters, 2)  AS cart_to_purchase_pct,
    ROUND(buyers  * 100.0 / viewers, 2)  AS overall_conversion_pct
FROM monthly_funnel
ORDER BY event_month_str;

-- ============================================
-- QUERY 4: CART ABANDONMENT RATE
-- Users who added to cart but never purchased
-- ============================================

WITH cart_users AS (
    SELECT DISTINCT user_id
    FROM clean_events
    WHERE event_type = 'cart'
),
purchase_users AS (
    SELECT DISTINCT user_id
    FROM clean_events
    WHERE event_type = 'purchase'
),
abandoned AS (
    SELECT COUNT(*) AS abandoned_users
    FROM cart_users
    WHERE user_id NOT IN (SELECT user_id FROM purchase_users)
)
SELECT
    (SELECT COUNT(*) FROM cart_users)    AS total_cart_users,
    (SELECT abandoned_users FROM abandoned) AS abandoned_users,
    (SELECT COUNT(*) FROM purchase_users)  AS purchase_users,
    ROUND(
        (SELECT abandoned_users FROM abandoned) * 100.0 /
        (SELECT COUNT(*) FROM cart_users), 2
    )                                    AS cart_abandonment_rate
;

-- ============================================
-- QUERY 5: FUNNEL BY HOUR OF DAY
-- When are users most likely to convert?
-- ============================================

WITH hourly AS (
    SELECT
        hour_of_day,
        COUNT(DISTINCT CASE WHEN event_type = 'view'     THEN user_id END) AS viewers,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS buyers
    FROM clean_events
    GROUP BY hour_of_day
)
SELECT
    hour_of_day,
    viewers,
    buyers,
    ROUND(buyers * 100.0 / viewers, 2) AS conversion_rate
FROM hourly
ORDER BY conversion_rate DESC
LIMIT 10;

-- ============================================
-- QUERY 6: TOP CONVERTING BRANDS
-- Which brands convert viewers to buyers best?
-- ============================================

WITH brand_funnel AS (
    SELECT
        brand,
        COUNT(DISTINCT CASE WHEN event_type = 'view'     THEN user_id END) AS viewers,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS buyers
    FROM clean_events
    WHERE brand != 'unknown'
    GROUP BY brand
    HAVING viewers > 1000
)
SELECT
    brand,
    viewers,
    buyers,
    ROUND(buyers * 100.0 / viewers, 2) AS conversion_rate
FROM brand_funnel
ORDER BY conversion_rate DESC
LIMIT 10;