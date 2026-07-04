# ============================================
# ShopSense — Export Data for Power BI
# Author: Brijesh Vaghela
# ============================================

import pandas as pd
from sqlalchemy import create_engine
import os

# ============================================
# CONFIGURATION
# Set DB_PASSWORD as an environment variable:
#   Windows: $env:DB_PASSWORD = "your_password"
#   Linux/Mac: export DB_PASSWORD="your_password"
# ============================================

DB_CONFIG = {
    'host'    : os.getenv('DB_HOST', '127.0.0.1'),
    'user'    : os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'shopsense')
}

if not DB_CONFIG['password']:
    raise ValueError("DB_PASSWORD environment variable is not set.")

engine = create_engine(
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}?charset=utf8mb4"
)

os.makedirs('data/powerbi', exist_ok=True)

print("Exporting monthly funnel...")
pd.read_sql("""
    WITH monthly AS (
        SELECT
            event_month_str,
            COUNT(DISTINCT CASE WHEN event_type='view'
                THEN user_id END)     AS viewers,
            COUNT(DISTINCT CASE WHEN event_type='cart'
                THEN user_id END)     AS carters,
            COUNT(DISTINCT CASE WHEN event_type='purchase'
                THEN user_id END)     AS buyers
        FROM clean_events
        GROUP BY event_month_str
    )
    SELECT *,
        ROUND(buyers*100.0/viewers,2) AS conversion_rate,
        ROUND((viewers-carters)*100.0/viewers,2) AS view_to_cart_dropoff,
        ROUND((carters-buyers)*100.0/carters,2)  AS cart_to_purchase_dropoff
    FROM monthly
    ORDER BY event_month_str
""", engine).to_csv('data/powerbi/monthly_funnel.csv', index=False)
print("✅ monthly_funnel.csv exported")

print("Exporting monthly revenue...")
pd.read_sql("""
    SELECT
        event_month_str                               AS month,
        COUNT(DISTINCT user_id)                       AS unique_buyers,
        COUNT(*)                                      AS total_orders,
        ROUND(SUM(price),2)                           AS total_revenue,
        ROUND(AVG(price),2)                           AS avg_order_value,
        ROUND(SUM(price)/COUNT(DISTINCT user_id),2)   AS arpu
    FROM clean_events
    WHERE event_type = 'purchase'
    GROUP BY event_month_str
    ORDER BY event_month_str
""", engine).to_csv('data/powerbi/monthly_revenue.csv', index=False)
print("✅ monthly_revenue.csv exported")

print("Exporting cohort retention...")
pd.read_sql("""
    WITH cohort_activity AS (
        SELECT
            uc.user_id,
            uc.cohort_month,
            ua.activity_month,
            PERIOD_DIFF(
                REPLACE(ua.activity_month,'-',''),
                REPLACE(uc.cohort_month,'-','')
            ) AS month_number
        FROM user_cohorts uc
        JOIN (
            SELECT DISTINCT user_id,
                DATE_FORMAT(event_time,'%Y-%m') AS activity_month
            FROM clean_events
            WHERE event_type='purchase'
        ) ua ON uc.user_id = ua.user_id
    ),
    cohort_sizes AS (
        SELECT cohort_month,
               COUNT(DISTINCT user_id) AS cohort_size
        FROM user_cohorts
        GROUP BY cohort_month
    )
    SELECT
        ca.cohort_month,
        cs.cohort_size,
        ca.month_number,
        COUNT(DISTINCT ca.user_id) AS retained_users,
        ROUND(COUNT(DISTINCT ca.user_id)*100.0/cs.cohort_size,2) AS retention_rate
    FROM cohort_activity ca
    JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    WHERE ca.month_number >= 0
    GROUP BY ca.cohort_month, cs.cohort_size, ca.month_number
    ORDER BY ca.cohort_month, ca.month_number
""", engine).to_csv('data/powerbi/cohort_retention.csv', index=False)
print("✅ cohort_retention.csv exported")

print("Exporting user segments...")
pd.read_sql("""
    WITH user_stats AS (
        SELECT
            user_id,
            COUNT(*)            AS frequency,
            ROUND(SUM(price),2) AS monetary
        FROM clean_events
        WHERE event_type = 'purchase'
        GROUP BY user_id
    )
    SELECT
        CASE
            WHEN monetary >= 100 AND frequency >= 3 THEN 'Champion'
            WHEN monetary >= 50  AND frequency >= 2 THEN 'Loyal'
            WHEN frequency = 1   AND monetary >= 20 THEN 'Promising'
            WHEN frequency = 1                      THEN 'New Customer'
            ELSE 'At Risk'
        END AS segment,
        COUNT(*)               AS user_count,
        ROUND(AVG(monetary),2) AS avg_revenue,
        ROUND(AVG(frequency),2) AS avg_orders
    FROM user_stats
    GROUP BY segment
    ORDER BY avg_revenue DESC
""", engine).to_csv('data/powerbi/user_segments.csv', index=False)
print("✅ user_segments.csv exported")

print("Exporting hourly conversion...")
pd.read_sql("""
    WITH h AS (
        SELECT
            hour_of_day,
            COUNT(DISTINCT CASE WHEN event_type='view'
                THEN user_id END) AS viewers,
            COUNT(DISTINCT CASE WHEN event_type='purchase'
                THEN user_id END) AS buyers
        FROM clean_events
        GROUP BY hour_of_day
    )
    SELECT
        hour_of_day,
        viewers, buyers,
        ROUND(buyers*100.0/viewers,2) AS conversion_rate,
        ROUND(buyers*100.0/SUM(buyers) OVER(),2) AS pct_of_total_buyers
    FROM h
    ORDER BY hour_of_day
""", engine).to_csv('data/powerbi/hourly_conversion.csv', index=False)
print("✅ hourly_conversion.csv exported")

print("Exporting top brands...")
pd.read_sql("""
    SELECT
        brand,
        COUNT(DISTINCT user_id)  AS unique_buyers,
        COUNT(*)                 AS total_orders,
        ROUND(SUM(price),2)      AS total_revenue,
        ROUND(AVG(price),2)      AS avg_order_value
    FROM clean_events
    WHERE event_type='purchase'
      AND brand != 'unknown'
    GROUP BY brand
    ORDER BY total_revenue DESC
    LIMIT 15
""", engine).to_csv('data/powerbi/top_brands.csv', index=False)
print("✅ top_brands.csv exported")

print("Exporting KPI summary...")
pd.read_sql("""
    SELECT
        COUNT(DISTINCT user_id)                      AS total_buyers,
        COUNT(*)                                     AS total_orders,
        ROUND(SUM(price),2)                          AS total_revenue,
        ROUND(AVG(price),2)                          AS avg_order_value,
        ROUND(SUM(price)/COUNT(DISTINCT user_id),2)  AS arpu,
        ROUND(COUNT(*)/COUNT(DISTINCT user_id),2)    AS avg_orders_per_user
    FROM clean_events
    WHERE event_type = 'purchase'
""", engine).to_csv('data/powerbi/kpi_summary.csv', index=False)
print("✅ kpi_summary.csv exported")

print("\n✅ ALL FILES EXPORTED SUCCESSFULLY")
print("Location: data/powerbi/")