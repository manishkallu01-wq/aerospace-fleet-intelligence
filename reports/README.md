# 📊 Executed Analytics & Evidence

This folder contains **outputs generated from the project analysis**, not just source code.

## NASA C-MAPSS FD001 results

| Metric | Result |
|---|---:|
| Test engines | **100** |
| Test records | **13,096** |
| Training records | **20,631** |
| Sensor channels | **21** |
| Mean true RUL | **75.52 cycles** |
| Median true RUL | **86 cycles** |
| Minimum true RUL | **7 cycles** |
| Maximum true RUL | **145 cycles** |
| Critical engines (≤30) | **25 (25%)** |
| High engines (31–60) | **14 (14%)** |
| Maintenance queue (≤60) | **39 (39%)** |
| Watch engines (61–90) | **15 (15%)** |
| Healthy engines (>90) | **46 (46%)** |

## 🔎 What the execution tells us

### 1. 39% of the test fleet belongs in a maintenance planning queue
Using the project threshold of **RUL ≤ 60 cycles**, 39 of 100 engines qualify. That is a materially different operational signal from simply reporting average fleet health.

### 2. One quarter of the fleet is in the critical band
**25 engines (25%) have ≤30 cycles of true RUL.** The lowest observed RUL is only **7 cycles**, so a maintenance planner would need to prioritize the lower tail rather than rely on the mean of 75.52 cycles.

### 3. The distribution is highly heterogeneous
The median RUL is **86 cycles**, while the minimum is **7** and maximum is **145**. The fleet therefore contains a substantial long-life population alongside a concentrated low-RUL tail.

### 4. The first priority candidates are concrete
The ten lowest-RUL engines are E034 (7), E031 (8), E081 (8), E068 (8), E082 (9), E076 (10), E042 (10), E035 (11), E066 (14), and E056 (15).

### 5. This is a decision-support result, not a certified prediction
These are **ground-truth RUL labels from the benchmark test set** used for evaluation and portfolio analysis. The production dashboard should use model predictions or Gold-layer estimates when deployed prospectively. It should not expose future true RUL as if it were available to an operator before failure.

## 🖼️ Evidence screenshot

![FD001 execution results](fd001_execution_results.svg)

## 📁 Machine-readable output

`fd001_engine_rul.csv` contains the 100-engine result table with RUL, risk band and priority.

## 🔬 Reproduction

The analytical pipeline is designed as:

`NASA C-MAPSS → ADF → ADLS → PySpark → Gold → dbt → Synapse → dashboard`

The benchmark result shown here is a **ground-truth evaluation artifact**. It is intentionally kept separate from prospective production predictions so the portfolio does not leak future labels into the operational dashboard.
