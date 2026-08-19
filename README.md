# ✈️ Aerospace Fleet Intelligence

A data engineering project built around NASA's C-MAPSS FD001 turbofan dataset. It takes engine-cycle data through an Azure-style data platform and turns it into RUL analysis, maintenance priorities, and a small Streamlit dashboard.

**Stack:** Azure Data Factory · ADLS Gen2 · Databricks/PySpark · dbt · Azure Synapse · Python · Streamlit · Plotly · GitHub Actions

![FD001 analysis results](reports/fd001_execution_results.svg)

## 🔎 What this project does

The project follows a simple path:

**ingest → store → clean → transform → model → report**

The repository contains the code and configuration for each part of that flow. The FD001 analysis and dashboard can be run locally from the repository. The Azure folders contain the corresponding cloud implementation files.

## 🎯 Why we built it

Aircraft-engine telemetry is a good data-engineering problem because the useful result is not the raw sensor stream. Someone needs to move the data reliably, standardize it, calculate useful features, keep the analytical tables consistent, and present the result in a form that can be reviewed.

This project uses the public C-MAPSS benchmark to build that flow without using proprietary airline or manufacturer data.

## 📌 Key takeaways

- **39 of 100 test engines** are at or below **60 cycles** of true RUL under the project's planning threshold.
- **25 engines** are at or below **30 cycles**.
- Fleet mean RUL is **75.52 cycles**, but the range is **7–145 cycles**. The low-RUL tail is therefore more useful for prioritization than the average by itself.
- The ten lowest-RUL engines are **E034, E031, E081, E068, E082, E076, E042, E035, E066, and E056**.
- The result file is used directly by the dashboard, so the displayed numbers can be traced back to a committed CSV.

## 📊 Results

| Metric | Result |
|---|---:|
| Test engines | **100** |
| Test records | **13,096** |
| Training records | **20,631** |
| Sensor measurements | **21** |
| Mean RUL | **75.52 cycles** |
| Median RUL | **86 cycles** |
| Minimum RUL | **7 cycles** |
| Maximum RUL | **145 cycles** |
| Critical (≤30) | **25 engines** |
| High (31–60) | **14 engines** |
| Maintenance queue (≤60) | **39 engines** |
| Watch (61–90) | **15 engines** |
| Healthy (>90) | **46 engines** |

### 🚦 RUL bands used in this project

| RUL | Band | Planning use |
|---:|---|---|
| ≤30 | 🔴 Critical | Review first |
| 31–60 | 🟠 High | Plan intervention |
| 61–90 | 🟡 Watch | Monitor more closely |
| >90 | 🟢 Healthy | Normal monitoring |

These are project analysis thresholds. They are **not aircraft maintenance limits**.

## 🏗️ How we built it

![Data platform architecture](assets/architecture.svg)

```text
NASA C-MAPSS
      ↓
Azure Data Factory
      ↓
ADLS Gen2 / Bronze
      ↓
Databricks + PySpark
      ↓
Silver → Gold
      ↓
dbt
      ↓
Azure Synapse
      ↓
Dashboard / BI
```

### ⚙️ 1. Ingest

ADF is used as the planned ingestion layer. The pipeline accepts a source URL and writes the source file to an ADLS Bronze location. The JSON files under `adf/` define the datasets, linked services, and copy activity.

### 🗄️ 2. Store

The intended lake layout separates source data from transformed data:

```text
bronze/   source-preserving files
silver/   typed and cleaned telemetry
gold/     analytical engine records
```

### ⚡ 3. Transform with PySpark

`databricks/01_bronze_to_silver.py` standardizes the C-MAPSS columns, casts engine/cycle fields, removes duplicate engine-cycle rows, and calculates simple sensor statistics.

`databricks/02_silver_to_gold.py` creates the latest record for each engine and adds a **condition-age proxy**. This proxy is a baseline feature for the data pipeline; it is not a trained RUL model.

### 🧱 4. Model with dbt

The dbt layer turns the Gold contract into staging and reporting models. Tests define basic expectations for engine IDs, cycles, and risk bands.

### 🏢 5. Serve with Synapse

The Synapse SQL creates `dbo.fct_engine_health` and reporting views for fleet KPIs and the maintenance queue.

### 📈 6. Present the result

The Streamlit dashboard reads `reports/fd001_engine_rul.csv`. It shows fleet KPIs, RUL distribution, risk counts, a maintenance-priority table, and the main finding from the benchmark.

## 🧠 What we learned

### The average does not tell the whole story

A mean RUL of 75.52 cycles sounds comfortable until the range is shown: **7 to 145 cycles**. An operational view therefore needs both a fleet summary and an engine-level queue.

### Data grain matters

The telemetry is naturally organized at **engine × operating cycle** grain. Keeping that grain clear makes the Silver transformation, feature calculations, and later aggregation easier to reason about.

### Benchmark labels must not be confused with predictions

FD001 provides true RUL values for the test set so that predictive models can be evaluated. Those values would not be known to an operator before failure. The current dashboard is therefore a benchmark-results view, not a live predictive-maintenance system.

### Simple thresholds can be useful, but they are not a maintenance policy

The 30/60/90-cycle bands make the benchmark easier to interpret. They are project thresholds, not certified aircraft maintenance limits.

### Business numbers need business inputs

There is no dollar savings estimate here because the dataset does not contain real maintenance costs, labor rates, downtime costs, or intervention decisions. Adding a savings number without those inputs would be misleading.

## 🔬 How the results were produced

The reproducible local path is:

```text
RUL_FD001.txt
      ↓
scripts/build_fd001_results.py
      ↓
src/aerospace_analytics.py
      ↓
reports/fd001_engine_rul.csv
      ↓
dashboard/app.py
```

The same result file is also used by the dashboard and the reports, which keeps the displayed numbers tied to one machine-readable source.

## ▶️ Reproduce the project locally

### 1. Clone

```bash
git clone https://github.com/manishkallu01-wq/aerospace-fleet-intelligence.git
cd aerospace-fleet-intelligence
```

### 2. Create the Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Get the source data

Download the public **NASA C-MAPSS Jet Engine Simulated Data** and extract the FD001 files under:

```text
data/raw/
```

The local result build specifically needs:

```text
data/raw/RUL_FD001.txt
```

The full source archive is intentionally not committed to Git.

### 4. Build the result table

```bash
python scripts/build_fd001_results.py
```

Expected output:

```text
reports/fd001_engine_rul.csv
```

The file contains:

```text
engine_id,true_rul_cycles,risk_band,priority
```

### 5. Run the tests

```bash
pytest -q
```

The tests cover the RUL thresholds, summary reconciliation, input size, missing values, negative values, and required columns.

### 6. Run the dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard reads the CSV generated in Step 4, so no database connection is required for the local benchmark view.

### 7. Run the notebook

Open:

```text
notebooks/01_fd001_analysis.ipynb
```

The reusable functions are in:

```text
src/aerospace_analytics.py
```

For the short project explanation, findings, and reproduction checklist, see [`docs/project_story.md`](docs/project_story.md).

## ☁️ Azure deployment path

The cloud implementation is organized as:

```text
ADF → ADLS Bronze → Databricks/PySpark → Gold → dbt → Synapse → BI
```

The repository contains the implementation/configuration files for this flow, but it does not include an Azure subscription or credentials. The project therefore does not claim a live cloud run.

For an Azure deployment:

1. Create an ADLS Gen2 account and Bronze/Silver/Gold locations.
2. Configure the ADF linked services and datasets under `adf/`.
3. Import/configure `adf/pipelines/pl_aerospace_ingestion.json`.
4. Run the PySpark transformations in a Databricks workspace.
5. Publish the Gold table using the schema in `synapse/01_tables.sql`.
6. Configure the dbt profile from `dbt/profiles.example.yml`.
7. Run the dbt staging and mart models.
8. Create the Synapse views from `synapse/02_business_views.sql`.
9. Point BI/reporting to the resulting Synapse views.

`docs/runbook.md` contains the post-load checks to perform.

## 🧪 Testing and CI

Run locally:

```bash
pytest -q
```

GitHub Actions runs the test suite on pushes and pull requests.

## 📚 Documentation

- [`docs/project_story.md`](docs/project_story.md) — what we did, why, how, lessons, and reproduction
- [`docs/architecture.md`](docs/architecture.md) — platform layout and data grain
- [`docs/data_dictionary.md`](docs/data_dictionary.md) — dataset fields and definitions
- [`docs/runbook.md`](docs/runbook.md) — local and Azure setup
- [`docs/business_insights.md`](docs/business_insights.md) — interpretation of results
- [`docs/portfolio_results.md`](docs/portfolio_results.md) — result summary and visual
- [`reports/README.md`](reports/README.md) — generated result files

## 🔗 Data source

NASA C-MAPSS Jet Engine Simulated Data:  
https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

## 🚀 Possible next steps

- Train and evaluate an actual RUL prediction model
- Add incremental Delta Lake processing
- Add data-quality checks in the cloud pipeline
- Add model/data drift monitoring
- Add Azure Monitor and operational logging
- Add environment-based CI/CD deployment
- Add maintenance-capacity optimization

## 👤 Author

**Manish Reddy Kallu**  
Data Engineering Portfolio

GitHub: https://github.com/manishkallu01-wq

> Independent portfolio project using public/simulated data. It is not a NASA, airline, aircraft manufacturer, or certified aviation maintenance system.
