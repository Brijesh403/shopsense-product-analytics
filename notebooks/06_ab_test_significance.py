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

print(f"Control conversion  : {control_rate:.2%}")
print(f"Treatment conversion: {treat_rate:.2%}")
print(f"Observed lift       : +{lift_pp:.2f} pp")
print(f"Z-statistic         : {z_stat:.2f}")
print(f"P-value             : {p_value:.6f}")
print(f"Significant at 5%?  : {'YES' if p_value < 0.05 else 'NO'}")