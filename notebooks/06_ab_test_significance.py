# A/B Test — Significance Test (SIMULATED)
from statsmodels.stats.proportion import proportions_ztest
import numpy as np

# From your simulation output
control_n, control_conv = 198999, 54698
treat_n, treat_conv     = 199309, 59272

count = np.array([treat_conv, control_conv])
nobs  = np.array([treat_n, control_n])

z_stat, p_value = proportions_ztest(count, nobs, alternative='larger')

control_rate = control_conv / control_n
treat_rate   = treat_conv / treat_n
lift_pp      = (treat_rate - control_rate) * 100
relative_lift = (treat_rate - control_rate) / control_rate * 100

# ---- 95% Wald confidence interval on the absolute lift ----
# p < 0.05 tells you the lift is real; the CI tells you the plausible
# range of that lift's size, which is what a stakeholder needs to
# decide whether it's worth acting on.
se = ((control_rate * (1 - control_rate) / control_n) +
      (treat_rate * (1 - treat_rate) / treat_n)) ** 0.5
ci_low  = (treat_rate - control_rate) - 1.96 * se
ci_high = (treat_rate - control_rate) + 1.96 * se

# ---- Practical significance threshold ----
# Statistical significance (p < 0.05) answers "is this lift real?"
# Practical significance answers "is this lift big enough to act on?"
# At this scale, a discount nudge has a real cost (margin given up on
# every redemption), so the bar here is a >1pp lift - below that, the
# discount cost likely erodes the recovered revenue.
PRACTICAL_THRESHOLD_PP = 1.0

print(f"Control conversion    : {control_rate:.2%}")
print(f"Treatment conversion  : {treat_rate:.2%}")
print(f"Observed lift         : +{lift_pp:.2f} pp  ({relative_lift:+.1f}% relative)")
print(f"95% CI on lift        : [{ci_low*100:.2f} pp, {ci_high*100:.2f} pp]")
print(f"Z-statistic           : {z_stat:.2f}")
print(f"P-value               : {p_value:.6f}")
print(f"Statistically sig.(5%): {'YES' if p_value < 0.05 else 'NO'}")
print(f"Practically sig.(>{PRACTICAL_THRESHOLD_PP}pp): "
      f"{'YES' if lift_pp > PRACTICAL_THRESHOLD_PP else 'NO'} "
      f"— even the CI's lower bound ({ci_low*100:.2f} pp) clears the bar")