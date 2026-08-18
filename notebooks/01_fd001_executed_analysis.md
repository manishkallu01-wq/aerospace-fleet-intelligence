# 🔬 FD001 Executed Analysis

> Reproducible evaluation notebook specification. The committed `reports/` artifacts are the rendered evidence from this analysis.

## Objective

Quantify the FD001 test-fleet RUL distribution and convert it into a transparent maintenance-prioritization view.

## Source

NASA C-MAPSS FD001 test RUL labels. The benchmark contains 100 test engines. The labels are **evaluation ground truth** and are not prospective operator information.

## Metrics

- Engines: **100**
- Mean RUL: **75.52 cycles**
- Median RUL: **86 cycles**
- Minimum RUL: **7 cycles**
- Maximum RUL: **145 cycles**
- Critical (≤30): **25 engines / 25%**
- High (31–60): **14 engines / 14%**
- Maintenance queue (≤60): **39 engines / 39%**
- Watch (61–90): **15 engines / 15%**
- Healthy (>90): **46 engines / 46%**

## Reproduction contract

```python
from src.aerospace_analytics import load_fd001_rul, build_evaluation_table, summarize

rul = load_fd001_rul("data/raw/RUL_FD001.txt")
result = build_evaluation_table(rul)
metrics = summarize(result)
print(metrics)
```

## Interpretation

The mean alone hides a significant low-RUL tail. The operational planning threshold of ≤60 cycles identifies **39%** of engines for the maintenance queue, while **25%** are in the critical ≤30-cycle band.

The ten lowest-RUL engines are retained in `reports/fd001_engine_rul.csv` and rendered in `reports/fd001_execution_results.svg`.

## Credibility boundary

This analysis does **not** claim that the benchmark is a live airline fleet, that true RUL is known before failure, or that the heuristic is aviation-certified. It demonstrates how an engineering platform can preserve benchmark truth for evaluation while separating it from prospective operational predictions.
