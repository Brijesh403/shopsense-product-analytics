# A/B Test — SIMULATED Assignment + Results
# ShopSense: cart-abandonment discount nudge
# NOTE: ShopSense data is observational. No real experiment was run.
# This script simulates random assignment on real abandoners to
# demonstrate correct A/B testing methodology end-to-end.

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

np.random.seed(42)  # reproducible

engine = create_engine(
    'mysql+mysqlconnector://root:1998@127.0.0.1/shopsense?charset=utf8mb4'
)

# Pull real cart-abandoners with their actual purchase outcome
df = pd.read_sql("""
    WITH cart_users AS (
        SELECT DISTINCT user_id FROM clean_events WHERE event_type = 'cart'
    ),
    purchasers AS (
        SELECT DISTINCT user_id FROM clean_events WHERE event_type = 'purchase'
    )
    SELECT
        c.user_id,
        CASE WHEN p.user_id IS NOT NULL THEN 1 ELSE 0 END AS actually_purchased
    FROM cart_users c
    LEFT JOIN purchasers p ON c.user_id = p.user_id
""", engine)

# Random 50/50 assignment
df['group'] = np.random.choice(['control', 'treatment'], size=len(df), p=[0.5, 0.5])

# Simulate the discount lift: treatment gets +3pp boost applied
# to users who did NOT actually purchase (simulating "nudge recovers some")
def simulate_outcome(row):
    if row['actually_purchased'] == 1:
        return 1  # already converted, unaffected
    if row['group'] == 'treatment':
        return np.random.binomial(1, 0.03)  # +3pp recovery chance
    return 0

df['converted'] = df.apply(simulate_outcome, axis=1)

# Results
summary = df.groupby('group')['converted'].agg(['count', 'sum', 'mean'])
summary.columns = ['users', 'conversions', 'conversion_rate']
print(summary)

df.to_csv('data/powerbi/ab_test_simulated_results.csv', index=False)
print("\n✅ Saved to data/powerbi/ab_test_simulated_results.csv")