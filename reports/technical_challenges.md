# Technical Challenges Solved

## Loading 20.7M rows without exhausting memory

A naive `pd.read_csv()` load of the full dataset would load all 5
monthly files into RAM at once. `01_load_data.py` reads each file in
100K-row chunks and appends to MySQL incrementally, keeping peak memory
usage flat regardless of total file size — the same pattern used in
production ETL pipelines that can't assume the dataset fits in memory.

## Two columns were mostly unusable as-is

`category_code` was 98.3% NULL and `brand` was 42.3% NULL in the raw
data. Rather than drop these columns (losing all category/brand
analysis) or leave the NULLs in place (breaking every downstream GROUP
BY), both were handled in the `clean_events` SQL view: category
analysis falls back to the numeric `category_id` (always populated),
and NULL brands are recoded to an explicit `'unknown'` label so they
group correctly instead of silently vanishing from aggregates.

## Querying 20.7M rows fast enough for interactive dashboards

`raw_events` is indexed on `event_type`, `user_id`, and `event_time` —
the three columns every funnel, cohort, and time-window query filters
or joins on. Without these indexes, the funnel and cohort queries in
`sql/analysis/` (which scan the full clean view) would fall back to
full table scans on every Power BI refresh.
