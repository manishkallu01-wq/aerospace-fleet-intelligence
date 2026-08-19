# Project Story

This page is the short version of the project for someone who wants to understand it before opening the code.

## 1. What did we do?

We built a small end-to-end data engineering workflow around NASA's C-MAPSS FD001 turbofan benchmark.

The project:

1. takes engine-cycle telemetry as the source data,
2. defines a Bronze → Silver → Gold data flow,
3. uses PySpark for cleaning and feature calculations,
4. defines dbt models for analytical reporting,
5. defines Synapse tables and views for the serving layer,
6. produces an engine-level RUL result table,
7. and presents those results in a Streamlit dashboard.

The repository also includes ADF and ADLS configuration files for the planned Azure ingestion path.

## 2. Why did we do it?

Raw telemetry is difficult to use directly. A useful engineering workflow needs consistent schemas, a clear data grain, repeatable transformations, quality checks, and a reporting layer.

The C-MAPSS benchmark gives us a public way to demonstrate those ideas without using proprietary aircraft or airline data.

The practical question used for the benchmark is:

> **Which test engines have the least remaining useful life, and how large is the review queue under a simple RUL threshold?**

## 3. How did we do it?

### Data

NASA C-MAPSS FD001 provides 100 training trajectories and 100 test trajectories, with three operating settings and 21 sensor measurements.

### Engineering flow

```text
NASA C-MAPSS
      ↓
ADF ingestion definition
      ↓
ADLS Bronze
      ↓
PySpark Silver
      ↓
PySpark Gold
      ↓
dbt models
      ↓
Synapse tables/views
      ↓
Dashboard / BI
```

### Local result flow

The benchmark result shown in the dashboard follows a simpler reproducible path:

```text
RUL_FD001.txt
      ↓
scripts/build_fd001_results.py
      ↓
src/aerospace_analytics.py
      ↓
reports/fd001_engine_rul.csv
      ↓
Streamlit dashboard
```

The result CSV is therefore the single machine-readable source for the dashboard's benchmark KPIs.

## 4. What did we learn?

### The average is not enough

The FD001 test set has a mean RUL of **75.52 cycles**, but the range is **7–145 cycles**. Looking only at the mean would hide the engines at the lower end of the distribution.

### The lower tail is the useful operational view

Using **60 cycles** as a project planning threshold puts **39 of 100 engines** into the review queue. **25 engines** are at or below 30 cycles.

### Data grain affects the whole design

The telemetry naturally sits at **engine × cycle** grain. Keeping that grain explicit makes the Silver transformation and later aggregation easier to understand and test.

### Ground truth is not a prediction

The RUL values used for the benchmark come from NASA's supplied test labels. They are useful for evaluating a model, but they would not be known to an operator before failure. A production system would replace them with predictions generated from information available at prediction time.

### Financial impact needs real business inputs

The benchmark has no maintenance labor rates, downtime cost, parts cost, or intervention history. We therefore do not attach a made-up dollar-savings number to the results.

## 5. How can someone reproduce it?

### Local benchmark analysis

```bash
git clone https://github.com/manishkallu01-wq/aerospace-fleet-intelligence.git
cd aerospace-fleet-intelligence
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place the FD001 `RUL_FD001.txt` file under `data/raw/`, then run:

```bash
python scripts/build_fd001_results.py
pytest -q
streamlit run dashboard/app.py
```

The generated result is:

```text
reports/fd001_engine_rul.csv
```

### Azure implementation

The Azure files under `adf/`, `databricks/`, `dbt/`, and `synapse/` provide the implementation starting point. A real deployment requires an Azure subscription and environment-specific configuration.

Follow `docs/runbook.md` for the deployment sequence and post-load checks.

## Final result

The project is intentionally small enough to understand but covers the main stages expected in a data engineering workflow:

**source → ingestion → storage → transformation → modeling → serving → reporting → validation**

The benchmark result is reproducible locally, while the Azure layer provides the path for turning the local workflow into a cloud deployment.
