# FD001 Analysis

This analysis uses the NASA C-MAPSS FD001 test RUL file to summarize the test fleet and build a simple maintenance-priority view.

## Source

`data/raw/RUL_FD001.txt`

The file contains the true RUL value for each of the 100 FD001 test engines. These values are benchmark labels used to check an RUL model; they are not live sensor predictions.

## Results

| Metric | Result |
|---|---:|
| Engines | **100** |
| Mean RUL | **75.52 cycles** |
| Median RUL | **86 cycles** |
| Minimum RUL | **7 cycles** |
| Maximum RUL | **145 cycles** |
| Critical (≤30) | **25 / 100** |
| High (31–60) | **14 / 100** |
| Queue (≤60) | **39 / 100** |
| Watch (61–90) | **15 / 100** |
| Healthy (>90) | **46 / 100** |

## Run the analysis

```python
from src.aerospace_analytics import load_fd001_rul, build_evaluation_table, summarize

rul = load_fd001_rul("data/raw/RUL_FD001.txt")
result = build_evaluation_table(rul)
metrics = summarize(result)
print(metrics)
```

The resulting table can be written to `reports/fd001_engine_rul.csv` and used by the dashboard.

## What the result means

The average RUL is 75.52 cycles, but the test set spans 7 to 145 cycles. Using 60 cycles as the project planning cutoff puts 39 engines in the maintenance queue. Twenty-five of those are at or below 30 cycles.

The lowest-RUL engine is E034 at 7 cycles. The next lowest values are 8, 8, 8, 9, 10, 10, 11, 14, and 15 cycles.

The important point is that the average alone is not enough to prioritize individual engines. The engine-level table is what makes the result useful for review.
