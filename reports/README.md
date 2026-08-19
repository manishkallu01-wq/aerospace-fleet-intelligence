# ✈️ FD001 Results

This folder contains the result files produced from the NASA C-MAPSS FD001 analysis.

![FD001 execution results](fd001_execution_results.svg)

## 📊 Results

| Metric | Result |
|---|---:|
| Test engines | **100** |
| Test records | **13,096** |
| Training records | **20,631** |
| Sensor channels | **21** |
| Mean RUL | **75.52 cycles** |
| Median RUL | **86 cycles** |
| Minimum RUL | **7 cycles** |
| Maximum RUL | **145 cycles** |
| Critical (≤30) | **25 engines** |
| High (31–60) | **14 engines** |
| Maintenance queue (≤60) | **39 engines** |
| Watch (61–90) | **15 engines** |
| Healthy (>90) | **46 engines** |

## 🚦 Main finding

Thirty-nine of the 100 test engines are at or below 60 cycles of true RUL. Twenty-five are at or below 30 cycles.

The ten lowest-RUL engines are:

`E034 (7), E031 (8), E081 (8), E068 (8), E082 (9), E076 (10), E042 (10), E035 (11), E066 (14), E056 (15)`

## 📁 Files

- `fd001_engine_rul.csv` - one result row for each test engine
- `fd001_execution_results.svg` - chart generated from the result file

## 🔬 Reproducing the analysis

The result file is the input used by the Streamlit dashboard. The surrounding repository contains the PySpark, Python, dbt, Synapse, and ADF files used to build the wider project.

The RUL values in this report are the true test labels supplied with FD001. They are used here to check and explain the benchmark results; they are not model predictions.
