# 📈 Portfolio Results & Analytics

> **Evidence layer:** this page separates reproducible FD001 benchmark findings from the target Azure architecture.

## ✈️ Dataset profile

NASA C-MAPSS FD001 is a simulated turbofan-engine degradation benchmark. It contains 100 training trajectories and 100 test trajectories under one operating condition and one fault mode. Each cycle contains three operating settings and 21 sensor measurements.

The test trajectories are truncated before failure and the separate RUL vector is supplied for benchmark evaluation.

## 🔢 Executed benchmark metrics

| Metric | Result |
|---|---:|
| Test engines | **100** |
| Test records | **13,096** |
| Training records | **20,631** |
| Mean true RUL | **75.52 cycles** |
| Median true RUL | **86 cycles** |
| Minimum true RUL | **7 cycles** |
| Maximum true RUL | **145 cycles** |
| Critical ≤30 | **25 engines** |
| High 31–60 | **14 engines** |
| Maintenance queue ≤60 | **39 engines** |
| Watch 61–90 | **15 engines** |
| Healthy >90 | **46 engines** |

## 🎯 Business questions

### 1. Which engines should receive attention first?

**Benchmark answer:** start with the lower-RUL tail. The ten lowest-RUL engines in the committed evidence range from **7 to 15 cycles**.

**Production answer:** replace true RUL with an independently evaluated model prediction available at decision time.

### 2. How much useful life remains?

The benchmark evaluation spans **7–145 cycles**, with a median of **86 cycles**. That spread is why fleet averages should be paired with distribution and tail metrics.

### 3. Where is risk concentrated?

Using the portfolio's transparent evaluation thresholds, **25%** of test engines are critical and **39%** fall into the ≤60-cycle maintenance queue.

### 4. What happens when maintenance capacity is constrained?

The queue-shaped dbt/Synapse contract provides the structure for sorting candidates by urgency. Capacity itself should remain an explicit planning parameter rather than an invented operational fact.

### 5. What should an analyst avoid claiming?

The benchmark's true RUL labels are **evaluation ground truth**. They are not available to an operator before failure. The portfolio therefore does not present the benchmark labels as a live predictive-maintenance system.

## 🧱 Engineering evidence

The repository contains:

- ADF parameterized ingestion metadata
- ADLS Bronze/Silver/Gold architecture
- PySpark transformations
- dbt project + source/model contracts
- Synapse business views
- Streamlit dashboard
- executable analysis notebook
- machine-readable CSV results
- rendered SVG evidence
- Python tests + GitHub Actions CI

The Azure components are **deployment-ready portfolio artifacts**, not claims of a currently running Azure subscription/workspace.

## 🖼️ Evidence

![Executed FD001 results](../reports/fd001_execution_results.svg)

## 💼 Portfolio outcome

The strongest result is a traceable chain:

`public source → schema contract → transformation code → tests → result artifact → dashboard → cloud deployment design`

That is materially more defensible than presenting an attractive dashboard with invented KPIs.
