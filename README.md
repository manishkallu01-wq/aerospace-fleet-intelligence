# Aerospace Fleet Intelligence

A data engineering project built around NASA's C-MAPSS FD001 turbofan dataset. The project takes engine-cycle data through an Azure-oriented data platform and turns it into RUL analysis, maintenance priorities, and a small Streamlit dashboard.

**Stack:** Azure Data Factory · ADLS Gen2 · Databricks/PySpark · dbt · Azure Synapse · Python · Streamlit · Plotly · GitHub Actions

## Project overview

The main idea is straightforward: start with engine telemetry, clean and organize it, build an analytical layer, and make the results useful to someone looking at fleet health.

The repository has two parts:

1. **Working local analysis** using the NASA FD001 data and the supplied test RUL values.
2. **Azure implementation files** showing how the same flow would be deployed with ADF, ADLS, Databricks, dbt, and Synapse.

The local analysis and dashboard are runnable from the files committed to this repository. The Azure pieces are deployment/configuration files; they are not presented as a live Azure environment.

## What is in the repository

| Area | What it does |
|---|---|
| `adf/` | ADF dataset and pipeline definitions |
| `databricks/` | PySpark Bronze-to-Silver and Silver-to-Gold transformations |
| `dbt/` | Staging models, marts, contracts, and Synapse profile template |
| `synapse/` | Warehouse tables and business views |
| `src/` | Reusable Python analysis functions |
| `dashboard/` | Streamlit dashboard |
| `reports/` | CSV results and generated analysis graphic |
| `tests/` | Python tests |
| `docs/` | Architecture, data definitions, run instructions, and findings |
| `notebooks/` | Analysis notebook and specification |
| `scripts/` | NASA source-data download helper |

## Data

The project uses **NASA C-MAPSS FD001**, a simulated turbofan-engine degradation dataset.

FD001 contains:

- 100 training engine trajectories
- 100 test engine trajectories
- 3 operating settings
- 21 sensor measurements
- 20,631 training records
- 13,096 test records

The training trajectories run to simulated failure. The test trajectories stop before failure, and NASA provides a separate true-RUL vector for evaluating predictions.

## Results from the FD001 analysis

The committed result file contains one row for each of the 100 test engines.

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

The ten lowest-RUL engines in the test set are:

`E034 (7), E031 (8), E081 (8), E068 (8), E082 (9), E076 (10), E042 (10), E035 (11), E066 (14), E056 (15)`

These numbers come from `reports/fd001_engine_rul.csv` and are used to drive the dashboard.

## Risk bands

The project uses simple RUL ranges to make the benchmark results easier to read:

| RUL | Band | Suggested planning action |
|---:|---|---|
| ≤30 | Critical | Review first |
| 31–60 | High | Plan intervention |
| 61–90 | Watch | Monitor more closely |
| >90 | Healthy | Normal monitoring |

These ranges are project thresholds for the benchmark analysis. They are **not aircraft maintenance limits**.

## Architecture

```text
NASA C-MAPSS
      |
      v
Azure Data Factory
      |
      v
ADLS Gen2 - Bronze
      |
      v
Databricks / PySpark
      |
      +---- Silver: typed engine-cycle data
      |
      +---- Gold: latest engine state
                    |
                    v
                   dbt
                    |
                    v
              Azure Synapse
                    |
                    v
              Dashboard / BI
```

### ADF

`adf/` contains parameterized dataset and pipeline metadata for the ingestion step. The files are ready to be imported/configured in an Azure environment, but no live ADF run is claimed in this repository.

### ADLS

The intended lake layout is:

```text
bronze/   source-preserving files
silver/   typed and cleaned telemetry
gold/     analytical engine records
```

The raw NASA files are not stored in Git. See `data/raw/README.md` for the download instructions.

### Databricks / PySpark

`databricks/01_bronze_to_silver.py` handles the source schema, engine/cycle typing, duplicate removal, and sensor-level feature calculations.

`databricks/02_silver_to_gold.py` builds the latest engine snapshot and a simple condition-age proxy. The proxy is a baseline feature for the portfolio; it is not presented as a trained RUL model.

### dbt

The `dbt/` directory contains staging SQL, analytical marts, source/model contracts, and a profile template for Synapse/SQL Server.

### Synapse

The `synapse/` directory contains warehouse DDL and views for fleet KPIs and the maintenance queue.

### Dashboard

The Streamlit app reads the committed `reports/fd001_engine_rul.csv` file. It does not require a live Synapse connection to show the benchmark results.

It includes:

- fleet-level RUL statistics
- RUL distribution
- risk-band counts
- maintenance priority queue
- a few simple findings for the benchmark

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
streamlit run dashboard/app.py
```

The dashboard expects `reports/fd001_engine_rul.csv` to be present.

## Testing

The Python tests cover the risk-band boundaries and reconciliation of the summary counts.

Run:

```bash
pytest -q
```

GitHub Actions runs the same test command on pushes and pull requests.

## Current Azure status

The repository includes the Azure implementation files, but the Azure resources themselves are not part of this GitHub project.

| Component | Current status |
|---|---|
| NASA FD001 analysis | Completed locally |
| Python analytics | Implemented and tested |
| Streamlit dashboard | Runs from committed results |
| PySpark transformations | Implemented |
| ADF | Pipeline/dataset files included; live run not claimed |
| ADLS Gen2 | Target lake design; live account not included |
| dbt | Models and contracts included; live run not claimed |
| Synapse | DDL/views included; live workspace not included |
| GitHub Actions | CI workflow included |

This keeps the repository clear about what can be reproduced directly from GitHub and what still needs an Azure subscription.

## Business questions

The analysis is aimed at a few practical questions:

- Which engines have the lowest remaining useful life?
- How large is the maintenance queue under a given RUL threshold?
- How does the lower-RUL tail compare with the fleet average?
- How could a warehouse expose the data to planners or BI tools?
- What would need to change before replacing benchmark labels with a real RUL model?

## Important note about RUL

The true RUL values supplied with FD001 are test labels. They are useful for measuring a model, but they would not be known to an operator before an engine reaches failure.

For that reason, the current dashboard is a **benchmark analysis dashboard**, not a live predictive-maintenance system. A production version would feed the same downstream layers with model predictions generated from data available at decision time.

## Documentation

- `docs/architecture.md` - platform layout and data grain
- `docs/data_dictionary.md` - FD001 fields and RUL definitions
- `docs/runbook.md` - local and Azure setup steps
- `docs/business_insights.md` - findings and planning interpretation
- `docs/portfolio_results.md` - results and engineering evidence
- `reports/README.md` - generated results and how they were produced

## Source

NASA - C-MAPSS Jet Engine Simulated Data:
https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

## Next steps

A fuller deployment could add:

1. Managed Identity and Key Vault
2. Metadata-driven ADF ingestion
3. Incremental Delta/ADLS processing
4. Data governance with Purview or Unity Catalog
5. A trained and independently evaluated RUL model
6. Model and data drift monitoring
7. Azure Monitor / Log Analytics
8. Environment-specific CI/CD deployment
9. Maintenance-capacity optimization

## Author

**Manish Reddy Kallu**  
Data Engineering Portfolio

GitHub: https://github.com/manishkallu01-wq  
LinkedIn: https://www.linkedin.com/in/manish-reddy-kallu/

> Independent portfolio project using public/simulated data. It is not a NASA, airline, aircraft manufacturer, or certified aviation maintenance system.
