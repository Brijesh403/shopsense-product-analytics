# Statistical Tests

Deeper statistical rigor layered on top of the core funnel/segment analysis --
testing whether descriptive differences are real, not just eyeballing them.

## Contents

| File | Question it answers |
|------|---------------------|
| `01_funnel_significance_test.py` | Are the month-to-month funnel swings statistically real, or noise? |
| `02_segment_lift_analysis.py` | Does cart-abandonment behavior differ by RFM segment, and where's the recovery opportunity concentrated? |

## Method

Both scripts use a chi-square test of independence for the "is this
difference real across groups" question, then a two-proportion Z-test
(with a 95% CI) for the specific headline pairwise comparison. This
mirrors the same statistical toolkit used in `04-06_ab_test_*.py`, applied
to observational data instead of a designed experiment.

## Key findings

- Every funnel rate (overall conversion, view-to-cart, cart-to-purchase)
  differs significantly by month (p < 0.001) -- expected at this sample
  size (350K+ viewers/month). The scripts print an explicit note that
  statistical significance here is close to guaranteed; the real question
  is effect size, covered in `reports/executive_summary.md`.
- Cart abandonment rate differs significantly by segment (p < 0.001), but
  the gap between the highest and lowest segments (Champion 62.0% vs
  At-Risk 64.5%) is small in absolute terms -- segment alone isn't a
  strong lever on abandonment *rate*. Full write-up in
  [`reports/segment_lift_analysis.md`](../../reports/segment_lift_analysis.md).

## Data dependency

- `01_funnel_significance_test.py` reads `data/powerbi/monthly_funnel.csv`
  (already produced by `03_export_for_powerbi.py`).
- `02_segment_lift_analysis.py` runs `sql/analysis/04_segment_cart_abandonment.sql`
  live against MySQL if `DB_PASSWORD` is set; otherwise it falls back to the
  verified output from running that query against the full dataset, so the
  script still produces real numbers with no DB connection.
