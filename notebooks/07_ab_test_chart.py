# ============================================
# ShopSense — A/B Test Result Chart
# Author: Brijesh Vaghela
# Visualizes the control vs. treatment conversion
# rates from the simulated cart-abandonment test.
# Uses the same style as the EDA charts in 02_eda_analysis.ipynb
# ============================================

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style('whitegrid')
sns.set_palette('husl')

# Results from notebooks/06_ab_test_significance.py
control_n, control_conv = 198999, 54698
treat_n, treat_conv = 199309, 59272

control_rate = control_conv / control_n * 100
treat_rate = treat_conv / treat_n * 100

groups = ['Control\n(no nudge)', 'Treatment\n(discount nudge)']
rates = [control_rate, treat_rate]
colors = ['#4C72B0', '#DD8452']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(groups, rates, color=colors, alpha=0.85, width=0.5)

for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f'{rate:.2f}%', ha='center', fontsize=13, fontweight='bold')

ax.annotate(
    f'+{treat_rate - control_rate:.2f}pp lift\np < 0.001 (Z = 15.72)',
    xy=(1, treat_rate), xytext=(1.15, treat_rate - 4),
    fontsize=11, fontweight='bold', color='#2ecc71',
    arrowprops=dict(arrowstyle='->', color='#2ecc71')
)

ax.set_ylabel('Conversion Rate (%)', fontsize=12)
ax.set_title(
    'Simulated A/B Test — Cart Abandonment Discount Nudge\n'
    f'Control (n={control_n:,}) vs. Treatment (n={treat_n:,})',
    fontsize=13, fontweight='bold'
)
ax.set_ylim(0, max(rates) + 6)
sns.despine()
plt.tight_layout()

plt.savefig('dashboards/screenshots/11_ab_test_results.png', dpi=150)
print("Saved dashboards/screenshots/11_ab_test_results.png")
