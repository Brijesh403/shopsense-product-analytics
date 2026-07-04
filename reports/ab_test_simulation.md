# A/B Test (Simulated) — Cart Abandonment Discount Nudge

**Note:** ShopSense data is observational (no real experiment was run).
This is a simulated test demonstrating correct A/B testing methodology
on real user data.

## Design
- H0: discount nudge has no effect on abandoner conversion
- H1: discount nudge increases conversion
- Baseline: 27.52% | MDE: +3pp | Alpha: 0.05 | Power: 0.80
- Required sample: 2,828/group | Available: 398,308 abandoners

## Results
| Group | Users | Conversions | Rate |
|---|---|---|---|
| Control | 198,999 | 54,698 | 27.49% |
| Treatment | 199,309 | 59,272 | 29.74% |

Z = 15.72, p < 0.001 → statistically significant.

## Statistical vs. Practical Significance

A p-value only answers "is this lift real?" — it doesn't say whether the
lift is *big enough to act on*. Both numbers matter:

| Question | Answer |
|---|---|
| Is the lift statistically real? | Yes — p < 0.001, Z = 15.72 |
| How big is the lift, with uncertainty? | +2.25pp, 95% CI **[1.97pp, 2.53pp]** |
| How big is that in relative terms? | +8.2% relative lift over baseline |
| Is it practically worth acting on? | Yes, at a >1pp practical-significance bar — even the CI's lower bound (1.97pp) clears it |

The practical bar (>1pp) reflects that a discount nudge has a real cost:
every redemption gives up margin, so a lift that's statistically real but
tiny (e.g. +0.1pp) could still lose money once the discount cost is
netted out. Here the effect is large enough, even at its most
conservative estimate, to be worth a real rollout — subject to the
caveat below.

## Caveat
Simulated lift, not causal evidence. A real rollout with proper
randomization would be needed before acting on this in production.