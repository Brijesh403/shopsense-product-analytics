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

## Caveat
Simulated lift, not causal evidence. A real rollout with proper
randomization would be needed before acting on this in production.