-- ============================================
-- ShopSense Product Analytics
-- Script: Cart Abandonment by RFM Segment
-- Author: Brijesh Vaghela
-- Business Question: Does cart abandonment behavior
--                     differ by customer segment, and
--                     where is the recovery opportunity
--                     concentrated?
-- ============================================

USE shopsense;

-- ============================================
-- Per-user cart activity + purchase activity,
-- joined to the same RFM segment logic used in
-- sql/kpis/01_revenue_kpis.sql (Query 8), so
-- segment definitions stay consistent everywhere.
-- ============================================

WITH user_stats AS (
    SELECT
        user_id,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END)          AS frequency,
        COALESCE(SUM(CASE WHEN event_type = 'purchase'
                          THEN price END), 0)                        AS monetary,
        COUNT(CASE WHEN event_type = 'cart' THEN 1 END)              AS cart_count
    FROM clean_events
    GROUP BY user_id
    HAVING frequency >= 1   -- only users with a purchase history have an RFM segment
),
segmented AS (
    SELECT
        user_id,
        frequency,
        monetary,
        cart_count,
        -- same CASE WHEN as sql/kpis/01_revenue_kpis.sql Query 8
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
        -- a user's cart adds that never became one of their purchases.
        -- Not a session-level abandonment flag (this dataset doesn't
        -- reliably link a specific cart event to a specific purchase
        -- event) -- this is a lifetime-count proxy: how many more times
        -- did this user add to cart than they ultimately checked out.
        GREATEST(cart_count - frequency, 0)     AS abandoned_instances
    FROM user_stats
)
SELECT
    segment,
    COUNT(*)                                     AS users,
    SUM(cart_count)                              AS total_carts,
    SUM(frequency)                                AS total_purchases,
    SUM(abandoned_instances)                     AS abandoned_instances,
    ROUND(SUM(abandoned_instances) * 100.0
          / SUM(cart_count), 2)                  AS abandonment_rate_pct
FROM segmented
GROUP BY segment
ORDER BY abandoned_instances DESC;
