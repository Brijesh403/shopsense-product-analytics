-- ============================================
-- ShopSense Product Analytics
-- Script: Data Quality Checks + Cleaning
-- Author: Brijesh Vaghela
-- ============================================

USE shopsense;

-- ============================================
-- SECTION 1: DATA PROFILING
-- Understand what we are working with
-- ============================================

-- 1.1 Total row count
SELECT COUNT(*) AS total_rows 
FROM raw_events;

-- 1.2 Date range of data
SELECT 
    MIN(event_time) AS earliest_event,
    MAX(event_time) AS latest_event,
    DATEDIFF(MAX(event_time), MIN(event_time)) AS days_covered
FROM raw_events;

-- 1.3 Unique counts
SELECT
    COUNT(DISTINCT user_id)      AS unique_users,
    COUNT(DISTINCT product_id)   AS unique_products,
    COUNT(DISTINCT user_session) AS unique_sessions,
    COUNT(DISTINCT brand)        AS unique_brands,
    COUNT(DISTINCT category_code) AS unique_categories
FROM raw_events;

-- ============================================
-- SECTION 2: NULL VALUE ANALYSIS
-- Find where data is missing
-- ============================================

-- 2.1 Count NULLs in every column
SELECT
    SUM(CASE WHEN event_time    IS NULL THEN 1 ELSE 0 END) AS null_event_time,
    SUM(CASE WHEN event_type    IS NULL THEN 1 ELSE 0 END) AS null_event_type,
    SUM(CASE WHEN product_id    IS NULL THEN 1 ELSE 0 END) AS null_product_id,
    SUM(CASE WHEN category_id   IS NULL THEN 1 ELSE 0 END) AS null_category_id,
    SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) AS null_category_code,
    SUM(CASE WHEN brand         IS NULL THEN 1 ELSE 0 END) AS null_brand,
    SUM(CASE WHEN price         IS NULL THEN 1 ELSE 0 END) AS null_price,
    SUM(CASE WHEN user_id       IS NULL THEN 1 ELSE 0 END) AS null_user_id,
    SUM(CASE WHEN user_session  IS NULL THEN 1 ELSE 0 END) AS null_user_session
FROM raw_events;

-- 2.2 NULL percentage per column
SELECT
    ROUND(SUM(CASE WHEN category_code IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_category,
    ROUND(SUM(CASE WHEN brand         IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_null_brand,
    ROUND(SUM(CASE WHEN price = 0     THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)         AS pct_zero_price
FROM raw_events;

-- ============================================
-- SECTION 3: DATA QUALITY CHECKS
-- Look for suspicious values
-- ============================================

-- 3.1 Check event_type values
-- Should only be: view, cart, remove_from_cart, purchase
SELECT 
    event_type,
    COUNT(*) AS total
FROM raw_events
GROUP BY event_type
ORDER BY total DESC;

-- 3.2 Check for zero or negative prices
SELECT
    COUNT(*) AS zero_price_rows
FROM raw_events
WHERE price = 0 OR price < 0;

-- 3.3 Price distribution
SELECT
    MIN(price)                    AS min_price,
    MAX(price)                    AS max_price,
    ROUND(AVG(price), 2)          AS avg_price,
    ROUND(STDDEV(price), 2)       AS std_price
FROM raw_events
WHERE event_type = 'purchase';

-- 3.4 Check for duplicate rows
SELECT
    event_time,
    user_id,
    product_id,
    event_type,
    COUNT(*) AS duplicate_count
FROM raw_events
GROUP BY event_time, user_id, product_id, event_type
HAVING COUNT(*) > 1
LIMIT 10;

-- ============================================
-- SECTION 4: CREATE CLEAN VIEW
-- A clean version of the data for all analysis
-- ============================================

CREATE OR REPLACE VIEW clean_events AS
SELECT
    id,
    event_time,
    DATE(event_time)                           AS event_date,
    YEAR(event_time)                           AS event_year,
    MONTH(event_time)                          AS event_month,
    DATE_FORMAT(event_time, '%Y-%m')           AS event_month_str,
    DAYOFWEEK(event_time)                      AS day_of_week,
    HOUR(event_time)                           AS hour_of_day,
    event_type,
    product_id,
    category_id,
    COALESCE(category_code, 'unknown')         AS category_code,
    COALESCE(brand, 'unknown')                 AS brand,
    CASE 
        WHEN price <= 0 THEN NULL 
        ELSE price 
    END                                        AS price,
    user_id,
    user_session
FROM raw_events
WHERE event_time IS NOT NULL
  AND user_id    IS NOT NULL
  AND event_type IN ('view','cart','remove_from_cart','purchase');

-- Verify the view
SELECT COUNT(*) AS clean_row_count FROM clean_events;