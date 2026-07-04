# Funnel Drop-off — Statistical Significance

The executive summary reports the funnel drop-off rates descriptively
(24.9% view-to-cart, 27.75% cart-to-purchase). This report tests whether
the *month-to-month movement* in those rates is statistically real,
using `notebooks/statistical_tests/01_funnel_significance_test.py`.

## Method

Chi-square test of independence: is each rate (overall conversion,
view-to-cart, cart-to-purchase) independent of month, across the 5
months in the dataset? Followed by a two-proportion Z-test on the one
pairwise comparison the business cares about most: November (revenue
peak) vs. December (revenue drop).

## Results

| Rate | Chi-square | df | p-value |
|---|---|---|---|
| Overall conversion vs. month | 1,724.0 | 4 | < 0.001 |
| View-to-cart vs. month | 18,412.1 | 4 | < 0.001 |
| Cart-to-purchase vs. month | 6,835.5 | 4 | < 0.001 |

| Comparison | Nov | Dec | Z | p-value |
|---|---|---|---|---|
| Conversion rate | 8.86% | 7.15% | 26.68 | < 0.001 |

All three funnel stages show statistically significant variation across
months, and the November-to-December conversion drop specifically is
not sampling noise.

## The caveat that matters more than the p-value

With 350,000-400,000 viewers per month, this test has enormous
statistical power — at this scale, even a 0.1 percentage-point
difference would read as "significant." The chi-square/Z-test results
above confirm the swings are *real*, but they do not by themselves say
a swing is *big enough to act on*. That's a separate, effect-size
question, already covered in
[`executive_summary.md`](executive_summary.md): the December drop is
-29.6% month-over-month, which is large by any practical standard,
not just a statistically detectable one.

The general lesson (relevant in any interview): at large sample sizes,
statistical significance stops being the interesting question — almost
everything is significant. Practical significance (the size of the
effect, and whether it's worth acting on) becomes the real filter. This
project applies that same distinction to the A/B test in
[`ab_test_simulation.md`](ab_test_simulation.md).
