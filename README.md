# ✈️ Aerospace Fleet Intelligence

> **Azure Data Engineering portfolio project** for aerospace predictive-maintenance analytics using NASA C-MAPSS turbofan-engine degradation data.

**ADF → ADLS Gen2 → Databricks / PySpark → dbt → Synapse Analytics → Dashboard**

<div align="center">
<img src="reports/fd001_execution_results.svg" alt="Executed FD001 analytical results" width="100%" />
</div>

## 🎯 What this project is

This project demonstrates how an aerospace telemetry platform can move from **raw engine-cycle data → governed transformations → analytical models → warehouse views → maintenance decision support**.

The benchmark is **NASA C-MAPSS FD001**, a simulated turbofan-engine degradation dataset. FD001 contains 100 training trajectories and 100 test trajectories, with 3 operating settings and 21 sensor measurements. NASA describes the training trajectories as run-to-failure and the test trajectories as truncated before failure, with a separate true-RUL vector for evaluation.

### ⚠️ Credibility boundary

This repository intentionally distinguishes between **what has been executed and measured** and **what is an Azure deployment design**.

| Layer | Repository status |
|---|---|
| NASA FD001 analysis | ✅ Executed evidence committed |
| Python analytics | ✅ Implemented |
| Streamlit dashboard | ✅ Runs locally from committed evidence |
| PySpark Bronze → Silver | ✅ Implemented as transformation code |
| PySpark Gold | ✅ Implemented as a clearly labeled baseline heuristic |
| ADF | 🧩 Deployment artifact / design; Azure run not claimed |
| ADLS Gen2 | 🧩 Target storage architecture; live account not claimed |
| dbt | 🧩 Models + contracts + Synapse profile template; live run not claimed |
| Synapse | 🧩 DDL/views; live workspace not claimed |
| GitHub Actions | ✅ CI configuration |

**No live Azure execution, production telemetry, airline fleet data, or aviation certification is claimed.** That distinction is deliberate.

## 🧰 Engineering stack

| Layer | Technology | Purpose |
|---|---|---|
| Source | NASA C-MAPSS | Turbofan degradation benchmark |
| Orchestration | Azure Data Factory | Parameterized ingestion design |
| Storage | ADLS Gen2 | Bronze / Silver / Gold lake architecture |
| Processing | Databricks + PySpark | Schema enforcement, deduplication, feature engineering |
| Modeling | dbt | SQL models, contracts and tests |
| Warehouse | Azure Synapse | Business-facing SQL views |
| Analytics | Python / Pandas | Benchmark analysis and evidence generation |
| Dashboard | Streamlit + Plotly | Interactive maintenance analytics |
| CI | GitHub Actions | Automated Python tests |

## 🔬 Executed FD001 results

The evidence layer is based on the **100-engine FD001 test RUL vector**, not fabricated dashboard values.

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
| 🔴 Critical ≤30 cycles | **25 engines / 25%** |
| 🟠 High 31–60 cycles | **14 engines / 14%** |
| 🔧 Queue ≤60 cycles | **39 engines / 39%** |
| 🟡 Watch 61–90 cycles | **15 engines / 15%** |
| 🟢 Healthy >90 cycles | **46 engines / 46%** |

These dataset-size figures are consistent with published FD001 descriptions: 100 training engines, 100 test engines, 20,631 training records and 13,096 test records.

### 📸 Evidence artifact

The visual above is generated from the committed machine-readable result artifact:

- [`reports/fd001_engine_rul.csv`](reports/fd001_engine_rul.csv)
- [`reports/fd001_execution_results.svg`](reports/fd001_execution_results.svg)
- [`reports/README.md`](reports/README.md)

### 💡 Technical findings

**1. 39% of the benchmark test engines fall into the ≤60-cycle planning queue.**

**2. 25% are in the ≤30-cycle critical band.** The fleet average of 75.52 cycles therefore cannot be used as the only planning KPI.

**3. RUL spans 7–145 cycles.** The distribution is heterogeneous, with a substantial low-RUL tail.

**4. The ten lowest-RUL engines are:**

`E034 (7), E031 (8), E081 (8), E068 (8), E082 (9), E076 (10), E042 (10), E035 (11), E066 (14), E056 (15)`

**5. The benchmark ground truth is evaluation-only.** NASA explicitly provides the true RUL vector for test evaluation; a real prospective system cannot use those future labels at decision time.

## 📊 Dashboard

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The dashboard reads `reports/fd001_engine_rul.csv`, so the committed dashboard is **reproducible without pretending that a live Synapse workspace is connected**.

It provides:

- 📌 benchmark KPI snapshot
- ⏱️ RUL distribution
- 🚦 risk-band distribution
- 🔧 lowest-RUL maintenance queue
- 📈 technical findings
- 💡 business interpretation

## 🏗️ Target architecture

<div align="center">
<img src="assets/architecture.svg" alt="Aerospace Data Engineering target architecture" width="100%" />
</div>

```text
NASA C-MAPSS
     │
     ▼
Azure Data Factory
     │
     ▼
ADLS Gen2 — Bronze
     │
     ▼
Databricks / PySpark
     │
     ├── Silver: engine × cycle telemetry
     │
     └── Gold: latest-engine analytical contract
                │
                ▼
              dbt
                │
                ▼
        Azure Synapse
                │
                ▼
          BI / Dashboard
```

## 🔄 Engineering flow

### 1. 🛬 ADF — ingestion boundary

`adf/` contains parameterized dataset/pipeline metadata for moving a source file into the Bronze boundary. It is a **deployable design artifact**, not evidence of a live Azure run.

### 2. 🗄️ ADLS — storage contract

The intended lake layout is:

```text
bronze/   source-preserving files
silver/   typed engine × cycle telemetry
gold/     latest-engine analytical records
```

Raw source archives are intentionally excluded from Git history. See [`data/raw/README.md`](data/raw/README.md).

### 3. ⚙️ Databricks / PySpark

`databricks/01_bronze_to_silver.py` implements:

- explicit 26-column source schema
- engine/cycle typing
- duplicate removal
- 21-sensor aggregate statistics
- training RUL derivation from run-to-failure trajectories

`databricks/02_silver_to_gold.py` creates a latest-engine snapshot and an explicitly named **condition-age proxy**.

> The condition-age proxy is a portfolio baseline, **not a trained predictive model**. A production RUL model belongs in a separate evaluated modeling stage.

### 4. 🧪 dbt

`dbt/` contains:

- project configuration
- staging model
- maintenance mart
- fleet KPI mart
- source/model contracts
- Synapse/SQL Server profile template

The repository does not claim a live dbt/Synapse execution unless that environment is actually configured.

### 5. 🏢 Synapse

`synapse/` contains warehouse-oriented DDL and business views for fleet KPIs and the maintenance queue.

### 6. 📊 Dashboard

The local Streamlit dashboard consumes the committed FD001 evidence artifact. This makes the portfolio **inspectable and reproducible** without fabricating a cloud connection.

## 🎯 Business questions

| Question | Evidence / analytical approach |
|---|---|
| 🚨 Which engines need attention first? | Rank the lower-RUL tail and risk bands. |
| ⏱️ How much useful life remains? | Analyze RUL in operating cycles. |
| 🚦 Where is risk concentrated? | Aggregate engines into transparent threshold bands. |
| 🔧 What should planners review? | Produce a sorted maintenance-priority table. |
| 👥 What happens under limited capacity? | Rank candidates before allocating intervention slots. |
| 📈 How would condition change be monitored? | Track Gold-layer snapshots and RUL predictions over time. |

## 🧮 Risk thresholds

For the **benchmark evidence report only**:

| RUL | Band | Action |
|---:|---|---|
| ≤30 | 🔴 CRITICAL | Immediate review |
| 31–60 | 🟠 HIGH | Schedule intervention |
| 61–90 | 🟡 WATCH | Increase monitoring |
| >90 | 🟢 HEALTHY | Routine monitoring |

These are **portfolio planning thresholds**, not aviation maintenance limits.

## 🧪 Data quality & testing

The project includes:

- explicit schema contract
- engine/cycle duplicate control
- cycle validation
- RUL/risk-band contracts
- dbt source/model contracts
- Python unit tests
- GitHub Actions CI
- raw-data exclusion rules
- reproducible machine-readable result artifact

Run:

```bash
pytest -q
```

## 🗂️ Repository structure

```text
.
├── .github/workflows/       CI
├── adf/
│   ├── datasets/            ADF dataset metadata
│   └── pipelines/           ADF pipeline metadata
├── assets/                  Hand-authored engineering SVGs
├── dashboard/               Streamlit application
├── data/
│   ├── raw/                 Source-data instructions
│   └── reference/           Schema contract
├── databricks/              PySpark transformations
├── dbt/
│   ├── models/staging/      Staging SQL
│   ├── models/marts/        Analytical marts
│   ├── dbt_project.yml      dbt configuration
│   └── profiles.example.yml Synapse profile template
├── docs/                    Architecture, runbook, insights
├── notebooks/               Executable analysis notebook + specification
├── reports/                 Executed metrics + CSV + visual evidence
├── scripts/                 Source acquisition
├── src/                     Reusable Python analytics
├── synapse/                 Warehouse SQL
├── tests/                   Automated tests
├── requirements.txt         Dashboard/test environment
└── requirements-data.txt    Optional PySpark/dbt environment
```

## 🎨 Visual provenance

This repository intentionally avoids a common portfolio credibility problem: **beautiful but fabricated imagery presented as evidence**.

- Architecture diagrams are hand-authored SVGs.
- Analytical visuals are generated from committed result artifacts.
- No proprietary aircraft photographs are used.
- No fake airline/aircraft manufacturer UI is presented as a real system.
- No AI-generated image is presented as a photograph, screenshot, sensor output or production dashboard.
- Illustrative concepts, if added later, must be explicitly labeled **DESIGN CONCEPT — NOT SOURCE DATA**.

See [`assets/README.md`](assets/README.md).

## 📚 Documentation

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/runbook.md`](docs/runbook.md)
- [`docs/business_insights.md`](docs/business_insights.md)
- [`docs/portfolio_results.md`](docs/portfolio_results.md)
- [`reports/README.md`](reports/README.md)
- [`data/reference/cmapss_schema.md`](data/reference/cmapss_schema.md)

## 📚 Source

**NASA — C-MAPSS Jet Engine Simulated Data**

https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

NASA describes C-MAPSS as simulated multivariate time-series engine data and explicitly provides true RUL values for test-set evaluation.

## 🚀 Production roadmap

A genuine production deployment would add:

1. Managed Identity + Key Vault
2. Metadata-driven ADF ingestion
3. Delta/ADLS incremental processing
4. Unity Catalog / Purview governance
5. A trained and independently evaluated RUL model
6. Prediction-time feature contracts
7. Synapse environment promotion
8. Azure Monitor / Log Analytics
9. Model/data drift monitoring
10. Capacity-aware maintenance optimization

## 👨‍💻 Author

**Manish Reddy Kallu** · Data Engineering Portfolio

[GitHub](https://github.com/manishkallu01-wq) · [LinkedIn](https://www.linkedin.com/in/manish-reddy-kallu/)

---

**Independent portfolio project using public/simulated data. It does not represent NASA, an airline, an aircraft manufacturer, or a certified aviation maintenance workflow.**
