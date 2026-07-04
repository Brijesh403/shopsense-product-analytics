# ============================================
# ShopSense Product Analytics
# Script: Funnel Drop-off Significance Testing
# Author: Brijesh Vaghela
# Business Question: The monthly funnel numbers move
#                     around every month -- is that real
#                     variation, or noise? Descriptive
#                     rates alone can't answer that.
# ============================================
#
# Input: data/powerbi/monthly_funnel.csv (from 03_export_for_powerbi.py)
#
# Method: chi-square test of independence, treating each month
# as a group and testing whether conversion rate (or view-to-cart,
# or cart-to-purchase) is independent of month. A significant
# result means the rate genuinely differs by month -- it does NOT
# by itself tell you the differences are large enough to act on;
# see the practical-significance note at the bottom.

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest

df = pd.read_csv('data/powerbi/monthly_funnel.csv')
print("Loaded monthly funnel data:")
print(df[['event_month_str', 'viewers', 'carters', 'buyers']])
print()

# ---- Chi-square: is overall conversion rate independent of month? ----
table_conv = df[['buyers']].copy()
table_conv['non_buyers'] = df['viewers'] - df['buyers']
chi2, p, dof, _ = chi2_contingency(table_conv[['buyers', 'non_buyers']].values)
print(f"Overall conversion rate vs. month  : chi2={chi2:,.1f}, dof={dof}, "
      f"p={'<0.001' if p < 0.001 else f'{p:.4f}'}")

# ---- Chi-square: is view-to-cart rate independent of month? ----
table_vc = df[['carters']].copy()
table_vc['non_carters'] = df['viewers'] - df['carters']
chi2b, pb, dofb, _ = chi2_contingency(table_vc[['carters', 'non_carters']].values)
print(f"View-to-cart rate vs. month        : chi2={chi2b:,.1f}, dof={dofb}, "
      f"p={'<0.001' if pb < 0.001 else f'{pb:.4f}'}")

# ---- Chi-square: is cart-to-purchase rate independent of month? ----
table_cp = df[['buyers']].copy()
table_cp['non_converting_carters'] = df['carters'] - df['buyers']
chi2c, pc, dofc, _ = chi2_contingency(table_cp[['buyers', 'non_converting_carters']].values)
print(f"Cart-to-purchase rate vs. month    : chi2={chi2c:,.1f}, dof={dofc}, "
      f"p={'<0.001' if pc < 0.001 else f'{pc:.4f}'}")
print()

# ---- Pairwise: Nov vs Dec conversion rate (the revenue-drop story) ----
nov = df[df['event_month_str'] == '2019-11'].iloc[0]
dec = df[df['event_month_str'] == '2019-12'].iloc[0]
count = np.array([nov['buyers'], dec['buyers']])
nobs = np.array([nov['viewers'], dec['viewers']])
z, p_pair = proportions_ztest(count, nobs)
nov_rate = nov['buyers'] / nov['viewers']
dec_rate = dec['buyers'] / dec['viewers']
print(f"Nov vs Dec conversion rate: {nov_rate:.2%} -> {dec_rate:.2%} "
      f"(Z={z:.2f}, p={'<0.001' if p_pair < 0.001 else f'{p_pair:.4f}'})")
print()

# ---- Practical significance note ----
print("NOTE ON PRACTICAL SIGNIFICANCE:")
print("At this sample size (350K-400K viewers/month), even a 0.1pp")
print("difference in conversion rate will read as 'statistically")
print("significant' -- the chi-square/Z tests above confirm the month-to-")
print("month swings are real, not sampling noise, but they do not by")
print("themselves say whether a given swing is big enough to act on.")
print("For that, look at the effect size in reports/executive_summary.md")
print("(e.g. the -29.6% December revenue drop) alongside these tests.")
