# ✈️ FD001 Results

This folder contains the main analytical output from the NASA C-MAPSS FD001 analysis.

![FD001 execution results](../assets/fd001-execution-results.svg)

## 📌 Key takeaways

- **100** test engines are included.
- **39 engines (39%)** are at or below 60 cycles of true RUL.
- **25 engines (25%)** are at or below 30 cycles.
- The fleet mean is **75.52 cycles**, while the range is **7–145 cycles**.
- The lowest-RUL engine is **E034 at 7 cycles**.

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

## 🔧 Priority list

The ten lowest-RUL engines are:

| Engine | True RUL | Band |
|---|---:|---|
| E034 | 7 | 🔴 Critical |
| E031 | 8 | 🔴 Critical |
| E081 | 8 | 🔴 Critical |
| E068 | 8 | 🔴 Critical |
| E082 | 9 | 🔴 Critical |
| E076 | 10 | 🔴 Critical |
| E042 | 10 | 🔴 Critical |
| E035 | 11 | 🔴 Critical |
| E066 | 14 | 🔴 Critical |
| E056 | 15 | 🔴 Critical |

## 📁 Files

- `fd001_engine_rul.csv` — one result row for each test engine
- `../assets/fd001-execution-results.svg` — visual summary built from the result CSV

## ▶️ Reproduce

From the repository root, after placing `RUL_FD001.txt` under `data/raw/`:

```bash
python scripts/build_fd001_results.py
pytest -q
streamlit run dashboard/app.py
```

The build script reads the NASA test RUL vector, applies the project's four RUL bands, and writes the CSV consumed by the dashboard.

## ⚠️ Note on the RUL values

The RUL values in this folder are the true test labels supplied with FD001. They are used to evaluate and explain the benchmark. They are not model predictions.
