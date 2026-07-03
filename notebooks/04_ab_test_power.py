# A/B Test — Sample Size / Power Analysis
# ShopSense: cart-abandonment discount nudge (SIMULATED)

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Inputs
baseline = 0.2752      # current abandoner conversion (from SQL baseline)
mde      = 0.03        # minimum detectable effect (+3pp)
treatment = baseline + mde
alpha    = 0.05
power    = 0.80

# Effect size (Cohen's h) for two proportions
effect = proportion_effectsize(treatment, baseline)

# Required sample size PER GROUP
analysis = NormalIndPower()
n = analysis.solve_power(
    effect_size=effect,
    alpha=alpha,
    power=power,
    ratio=1.0,
    alternative='larger'
)

print(f"Baseline conversion : {baseline:.2%}")
print(f"Target conversion   : {treatment:.2%}")
print(f"MDE                 : +{mde:.0%} pts")
print(f"Alpha               : {alpha}")
print(f"Power               : {power}")
print(f"\nRequired per group  : {round(n):,} users")
print(f"Total required      : {round(n)*2:,} users")
print(f"Available abandoners: 398,308")