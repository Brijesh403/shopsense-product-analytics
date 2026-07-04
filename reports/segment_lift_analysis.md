# Segment-Level Cart Abandonment — Champions vs. At-Risk

The RFM segmentation in the executive summary splits buyers into five
value tiers. This report asks a follow-up question the segmentation
alone doesn't answer: **does cart-abandonment behavior differ by
segment, and if we ran the cart-abandonment discount nudge again,
where should it be targeted first?**

Produced by `sql/analysis/04_segment_cart_abandonment.sql` and
`notebooks/statistical_tests/02_segment_lift_analysis.py`.

## Method

For every user with at least one purchase (i.e. every user who has an
RFM segment), count their lifetime cart-add events and lifetime
purchase events. `abandoned_instances = cart_count − purchase_count`
(floored at 0) is a lifetime-count proxy for cart abandonment — this
dataset doesn't reliably link one specific cart event to one specific
purchase, so this measures "how many more times did this user add to
cart than they ultimately checked out," not session-level abandonment.

## Results — real, measured data (no simulation)

| Segment | Users | Total Carts | Abandoned Instances | Abandonment Rate |
|---|---|---|---|---|
| Champion | 14,139 | 1,493,513 | 926,553 | 62.04% |
| At Risk | 65,240 | 1,122,022 | 724,117 | 64.54% |
| Loyal | 19,722 | 763,856 | 489,315 | 64.06% |
| New Customer | 7,351 | 32,590 | 25,299 | 77.63% |
| Promising | 4,066 | 15,359 | 11,328 | 73.75% |

**Chi-square test (abandonment rate independent of segment?):**
chi2 = 5,503.5, df = 4, p < 0.001 — abandonment rate does differ by segment.

**Champion vs. At-Risk (the headline comparison):**

| | Rate | 95% CI on the gap |
|---|---|---|
| Champion | 62.04% | |
| At Risk | 64.54% | |
| Gap (At Risk − Champion) | 2.50pp | [2.38pp, 2.62pp] |

Z = 41.44, p < 0.001 — the gap is statistically real.

## The finding that matters more than the p-value

**Champions abandon carts at nearly the same rate as At-Risk users.**
Only a 2.5-point gap separates your highest-value repeat buyers from
your least engaged ones. Past spend and purchase frequency predict
almost nothing about whether *this* cart gets checked out. That's
counter-intuitive, and worth stating plainly: **segment is not a strong
lever on abandonment rate.**

What segment *does* predict is volume. Champions collectively generate
the single largest pool of abandoned-cart instances (926,553) — not
because they abandon more often, but because they simply shop far more
than anyone else (1.49M total cart-adds vs. At-Risk's 1.12M).

## Illustrative opportunity sizing — not a new measured effect

The section above is 100% real, measured data. This part is not: it
applies the *already-validated* recovery rate from the actual
cart-abandonment A/B test (`ab_test_simulation.md`: ~3% recovery on
abandoned instances) to each segment's real abandoned-cart volume, to
show where the addressable opportunity is biggest. No experiment has
tested whether Champions and At-Risk actually respond differently to a
discount nudge — this is sizing, not a discovery.

| Segment | Abandoned Instances | Illustrative Recovered Conversions (at 3%) |
|---|---|---|
| Champion | 926,553 | ~27,797 |
| At Risk | 724,117 | ~21,724 |
| Loyal | 489,315 | ~14,679 |
| New Customer | 25,299 | ~759 |
| Promising | 11,328 | ~340 |

## Recommendation

1. **Don't target the nudge by segment based on abandonment rate** — the
   rate gap between segments is real but too small (2.5pp) to justify
   different messaging by RFM tier.
2. **Do prioritize by volume.** Champions and At-Risk together account
   for ~1.65M of the ~2.18M total abandoned instances across all
   segments — a recovery campaign focused on just these two groups
   covers the large majority of the addressable opportunity.
3. **Before scaling spend on this**, run the actual segmented A/B test
   (not this retrospective sizing) to confirm whether recovery rate
   genuinely varies by segment — the uniform 3% assumption above is a
   placeholder for planning, not a validated per-segment number.
