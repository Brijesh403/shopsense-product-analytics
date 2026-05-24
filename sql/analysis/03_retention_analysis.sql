-- ============================================
-- ShopSense Product Analytics
-- Script: Cohort Retention Analysis
-- Author: Brijesh Vaghela
-- Business Question: How well do we retain users?
-- ============================================

USE shopsense;

-- ============================================
-- STEP 1: FIND EACH USER'S FIRST PURCHASE MONTH
-- This defines which cohort they belong to
-- ============================================

CREATE OR REPLACE VIEW user_cohorts AS
SELECT
    user_id,
    MIN(DATE_FORMAT(event_time, '%Y-%m'))  AS cohort_month,
    MIN(DATE(event_time))                  AS first_purchase_date
FROM clean_events
WHERE event_type = 'purchase'
GROUP BY user_id;

-- Verify cohort sizes
SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
FROM user_cohorts
GROUP BY cohort_month
ORDER BY cohort_month;

-- ============================================
-- STEP 2: FIND ALL PURCHASE ACTIVITY PER USER
-- Every month each user was active (purchased)
-- ============================================

CREATE OR REPLACE VIEW user_activity AS
SELECT
    DISTINCT
    user_id,
    DATE_FORMAT(event_time, '%Y-%m') AS activity_month
FROM clean_events
WHERE event_type = 'purchase';

-- ============================================
-- STEP 3: BUILD THE COHORT RETENTION MATRIX
-- Join cohorts with activity to find Month N retention
-- ============================================

WITH cohort_activity AS (
    SELECT
        uc.user_id,
        uc.cohort_month,
        ua.activity_month,
        PERIOD_DIFF(
            REPLACE(ua.activity_month, '-', ''),
            REPLACE(uc.cohort_month,   '-', '')
        ) AS month_number
    FROM user_cohorts uc
    JOIN user_activity ua
        ON uc.user_id = ua.user_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM user_cohorts
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    cs.cohort_size,
    ca.month_number,
    COUNT(DISTINCT ca.user_id)                              AS retained_users,
    ROUND(COUNT(DISTINCT ca.user_id) * 100.0
          / cs.cohort_size, 2)                             AS retention_rate
FROM cohort_activity ca
JOIN cohort_sizes cs
    ON ca.cohort_month = cs.cohort_month
WHERE ca.month_number >= 0
GROUP BY ca.cohort_month, cs.cohort_size, ca.month_number
ORDER BY ca.cohort_month, ca.month_number;

-- ============================================
-- STEP 4: PIVOT THE RETENTION MATRIX
-- Rows = Cohorts, Columns = Month 0,1,2,3,4
-- ============================================

WITH cohort_activity AS (
    SELECT
        uc.user_id,
        uc.cohort_month,
        ua.activity_month,
        PERIOD_DIFF(
            REPLACE(ua.activity_month, '-', ''),
            REPLACE(uc.cohort_month,   '-', '')
        ) AS month_number
    FROM user_cohorts uc
    JOIN user_activity ua ON uc.user_id = ua.user_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM user_cohorts
    GROUP BY cohort_month
),
retention AS (
    SELECT
        ca.cohort_month,
        cs.cohort_size,
        ca.month_number,
        ROUND(COUNT(DISTINCT ca.user_id) * 100.0
              / cs.cohort_size, 2) AS retention_rate
    FROM cohort_activity ca
    JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    WHERE ca.month_number >= 0
    GROUP BY ca.cohort_month, cs.cohort_size, ca.month_number
)
SELECT
    cohort_month,
    cohort_size,
    MAX(CASE WHEN month_number = 0 THEN retention_rate END) AS month_0,
    MAX(CASE WHEN month_number = 1 THEN retention_rate END) AS month_1,
    MAX(CASE WHEN month_number = 2 THEN retention_rate END) AS month_2,
    MAX(CASE WHEN month_number = 3 THEN retention_rate END) AS month_3,
    MAX(CASE WHEN month_number = 4 THEN retention_rate END) AS month_4
FROM retention
GROUP BY cohort_month, cohort_size
ORDER BY cohort_month;

-- ============================================
-- STEP 5: OVERALL PLATFORM RETENTION SUMMARY
-- Day 1, Day 7, Day 30 retention
-- ============================================

WITH first_purchase AS (
    SELECT
        user_id,
        MIN(DATE(event_time)) AS first_date
    FROM clean_events
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
returning_users AS (
    SELECT
        fp.user_id,
        fp.first_date,
        MIN(DATE(ce.event_time)) AS return_date
    FROM first_purchase fp
    JOIN clean_events ce
        ON fp.user_id    = ce.user_id
        AND ce.event_type = 'purchase'
        AND DATE(ce.event_time) > fp.first_date
    GROUP BY fp.user_id, fp.first_date
)
SELECT
    COUNT(DISTINCT fp.user_id)                              AS total_buyers,
    COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 1
        THEN fp.user_id END)                               AS day1_retained,
    COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 7
        THEN fp.user_id END)                               AS day7_retained,
    COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 30
        THEN fp.user_id END)                               AS day30_retained,
    ROUND(COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 1
        THEN fp.user_id END) * 100.0
        / COUNT(DISTINCT fp.user_id), 2)                  AS day1_retention_pct,
    ROUND(COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 7
        THEN fp.user_id END) * 100.0
        / COUNT(DISTINCT fp.user_id), 2)                  AS day7_retention_pct,
    ROUND(COUNT(DISTINCT CASE
        WHEN DATEDIFF(ru.return_date, fp.first_date) <= 30
        THEN fp.user_id END) * 100.0
        / COUNT(DISTINCT fp.user_id), 2)                  AS day30_retention_pct
FROM first_purchase fp
LEFT JOIN returning_users ru
    ON fp.user_id = ru.user_id;