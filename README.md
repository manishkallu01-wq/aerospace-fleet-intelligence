# ✈️ Aerospace Fleet Intelligence

> **Executive-grade Azure Data Engineering portfolio project** turning NASA C-MAPSS turbofan telemetry into fleet-health, predictive-maintenance and operational decision analytics.

**Azure Data Factory → ADLS Gen2 → Databricks / PySpark → dbt → Synapse Analytics → Dashboard**

<div align="center"><img src="assets/executive-fleet-operations-dashboard.svg" alt="Executive Aerospace Fleet Operations Dashboard" width="100%" /></div>

## 🎯 What this project delivers

A complete data product — **ingest → store → transform → test → model → serve → analyze** — built around a concrete business decision:

> **Which engines should maintenance planners review first, how much useful life remains, and where should scarce maintenance capacity be allocated?**

### 🧰 Engineering stack

`Azure Data Factory` · `ADLS Gen2` · `Azure Databricks` · `PySpark` · `Delta Lake` · `dbt` · `Azure Synapse` · `SQL` · `Python` · `Streamlit` · `Plotly` · `GitHub Actions`

### 📌 Business outputs

- 🚨 Fleet risk ranking
- ⏱️ Remaining Useful Life (RUL)
- 🔧 Maintenance priority queue
- 📈 Health vs. RUL analysis
- 📊 Risk by engine type
- 🧭 Capacity-aware intervention planning
- 💰 Assumption-driven maintenance scenarios
- ✅ Tested, warehouse-ready Gold layer

> **Portfolio note:** C-MAPSS is simulated engine-degradation data. The project demonstrates engineering and analytics patterns; it is not a certified aviation safety or maintenance system.

## 📊 Executive dashboard

The dashboard is intentionally designed like an operations product rather than a notebook screenshot. It provides:

| View | Business decision |
|---|---|
| 🚦 Fleet risk distribution | Where is risk concentrated? |
| ⏱️ RUL vs. health | Which engines have less remaining life? |
| 🔧 Maintenance priorities | What should planners review first? |
| 📈 RUL trend | Is fleet condition changing? |
| 🚨 Alerts | What requires immediate attention? |
| 💡 Key insights | What action should management take? |

## 🔬 Executed analysis — actual FD001 results

This section is the **evidence layer** of the portfolio. These values are derived from the 100-engine FD001 test RUL labels rather than invented dashboard KPIs.

| Metric | Result |
|---|---:|
| ✈️ Test engines | **100** |
| 🧾 Test records | **13,096** |
| 🏭 Training records | **20,631** |
| 📡 Sensor channels | **21** |
| ⏱️ Mean true RUL | **75.52 cycles** |
| 📍 Median true RUL | **86 cycles** |
| 🔻 Minimum true RUL | **7 cycles** |
| 🔺 Maximum true RUL | **145 cycles** |
| 🔴 Critical ≤30 cycles | **25 engines (25%)** |
| 🟠 High 31–60 cycles | **14 engines (14%)** |
| 🔧 Maintenance queue ≤60 | **39 engines (39%)** |
| 🟡 Watch 61–90 cycles | **15 engines (15%)** |
| 🟢 Healthy >90 cycles | **46 engines (46%)** |

### 📸 Executed-results screenshot

<div align="center"><img src="reports/fd001_execution_results.svg" alt="Executed NASA C-MAPSS FD001 results with actual RUL metrics and maintenance priorities" width="100%" /></div>

### 💡 What the numbers tell us

1. **39% of the test fleet falls into the maintenance queue** using the project threshold of ≤60 RUL cycles.
2. **25% is critical** at ≤30 cycles — the lower tail needs attention even though the fleet-wide mean is 75.52 cycles.
3. The RUL range is wide: **7 to 145 cycles**, showing substantial heterogeneity across engines.
4. The ten lowest-RUL engines are **E034 (7), E031 (8), E081 (8), E068 (8), E082 (9), E076 (10), E042 (10), E035 (11), E066 (14), E056 (15)**.
5. The median of **86 cycles** is substantially above the minimum, demonstrating why a single fleet-average KPI is insufficient for maintenance prioritization.

> ⚠️ **Important analytical distinction:** these are benchmark **ground-truth RUL labels used for evaluation**. A prospective operational system would use model predictions/Gold-layer estimates available at decision time; it must not expose future true RUL as if it were known to an operator.

➡️ **Full machine-readable output:** [`reports/fd001_engine_rul.csv`](reports/fd001_engine_rul.csv)  
➡️ **Full execution report:** [`reports/README.md`](reports/README.md)

## 💡 Key portfolio insights

### 🚨 1. Prioritize before failure
C-MAPSS provides run-to-failure training trajectories and test trajectories that stop before failure. The strongest business story is therefore **early-warning maintenance prioritization**, not post-failure detection.

### ⏱️ 2. RUL becomes the planning language
Remaining Useful Life expressed in operating cycles gives planners a consistent comparison measure while the Silver layer preserves detailed engine × cycle telemetry.

### 🔧 3. Analytics must become an action
The Gold layer converts risk into a recommended action — immediate review, scheduled intervention, increased monitoring or routine monitoring — so the output is a **maintenance queue**, not just a model score.

### 👥 4. Capacity matters
When maintenance capacity is limited, the queue can be ranked by risk and RUL so the highest-priority engines consume scarce intervention slots first.

### 💰 5. Economics stay credible
Maintenance cost, downtime cost and capacity are explicit scenario assumptions. The project does **not** fabricate savings from simulated aerospace data.

## 📊 Business questions answered

| Question | Answer from the analytical layer |
|---|---|
| 🚨 **Which engines need attention first?** | Rank latest engine states by health, RUL and risk. |
| ⏱️ **How much life remains?** | Compare engines using RUL cycles. |
| 🚦 **Where is risk concentrated?** | Aggregate engine snapshots into CRITICAL / HIGH / WATCH / HEALTHY bands. |
| 🔧 **What should happen next?** | Translate each risk band into a maintenance action. |
| 👥 **What if capacity is constrained?** | Prioritize the highest-risk candidates within available maintenance capacity. |
| 📈 **Is fleet condition changing?** | Track RUL and health trends over time. |

Detailed analysis: [`docs/business_insights.md`](docs/business_insights.md) · [`docs/portfolio_results.md`](docs/portfolio_results.md)

## 🏗️ Architecture

<div align="center"><img src="assets/architecture.svg" alt="Aerospace Data Engineering architecture" width="100%" /></div>

**NASA C-MAPSS → ADF → ADLS Bronze → Databricks/PySpark → ADLS Silver/Gold → dbt → Synapse → Dashboard**

## 🔄 Data engineering flow

### 1. 🛬 Ingest — Azure Data Factory
Parameterized ingestion accepts the dataset/source and Bronze destination, keeping source capture separate from transformation for replayability.

### 2. 🗄️ Store — ADLS Gen2
A clean Bronze / Silver / Gold lake pattern provides durable boundaries between raw telemetry, standardized data and business-ready outputs.

### 3. ⚙️ Transform — Databricks + PySpark
Explicit schema enforcement, duplicate detection, cycle validation, RUL derivation, sensor features, health scoring and risk classification.

### 4. 🧪 Model — dbt
Reusable staging and marts with uniqueness, relationship, accepted-value and health-score tests.

### 5. 🏢 Serve — Synapse
Curated warehouse objects and business views expose the analytical contract to BI consumers.

### 6. 📊 Decide — Dashboard
Executive KPIs, fleet risk, RUL, maintenance priorities, alerts and trends turn the data into an operational decision layer.

## 📁 Repository structure

```text
adf/                 Azure Data Factory datasets + pipelines
assets/              Executive dashboard + architecture SVGs
dashboard/           Streamlit + Plotly dashboard
data/raw/            Raw-data policy / local source downloads
data/reference/      Schema contracts and source metadata
databricks/          PySpark Bronze → Silver → Gold jobs
dbt/                 Staging models, marts and tests
docs/                Architecture, runbook, insights, results
notebooks/           Reproducible exploratory analytics
reports/             Executed metrics, CSV output, evidence visuals
scripts/             Source-data acquisition
src/                 Reusable Python analytics logic
synapse/             Warehouse DDL + business views
tests/               Automated Python validation
.github/workflows/   CI
```

## 🚦 Risk framework

| Band | Action |
|---|---|
| 🔴 **CRITICAL** | Immediate review |
| 🟠 **HIGH** | Schedule intervention |
| 🟡 **WATCH** | Increase monitoring |
| 🟢 **HEALTHY** | Routine monitoring |

The health score is an **interpretable portfolio prioritization heuristic**, not an aviation-certified prediction model.

## 🧪 Data quality & reliability

- explicit source schema
- engine/cycle duplicate checks
- cycle validation
- required-field checks
- health-score `[0,100]` contract
- dbt uniqueness and relationship tests
- accepted risk values
- GitHub Actions CI
- replayable Bronze boundary
- full raw archive excluded from Git history

## 🗃️ Data source

**NASA — C-MAPSS Jet Engine Simulated Data**

https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

The full archive is deliberately not committed to GitHub. Run `scripts/download_cmapss.py` when required. The schema contract is maintained in `data/reference/cmapss_schema.md`.

## 🚀 Production evolution

Managed Identity + Key Vault, Purview/Unity Catalog governance, metadata-driven ADF ingestion, incremental Delta processing, Azure Monitor/Log Analytics, environment promotion, data contracts, model registry and platform cost monitoring are natural production extensions.

## 📚 Documentation

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/runbook.md`](docs/runbook.md)
- [`docs/business_insights.md`](docs/business_insights.md)
- [`docs/portfolio_results.md`](docs/portfolio_results.md)
- [`docs/portfolio_walkthrough.md`](docs/portfolio_walkthrough.md)
- [`reports/README.md`](reports/README.md)

## 👨‍💻 Author

**Manish Reddy Kallu** · Data Engineering Portfolio

[GitHub](https://github.com/manishkallu01-wq) · [LinkedIn](https://www.linkedin.com/in/manish-reddy-kallu/)

---

**Independent portfolio project using public/simulated data. It does not represent NASA, an airline, an aircraft manufacturer, or a certified aviation maintenance workflow.**
