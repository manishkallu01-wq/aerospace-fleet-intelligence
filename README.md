# ✈️ Aerospace Fleet Intelligence

> **Clean, production-style Data Engineering portfolio project** for turning NASA C-MAPSS turbofan engine telemetry into governed fleet-health and maintenance analytics.

**Azure Data Factory → ADLS Gen2 → Databricks / PySpark → dbt → Synapse Analytics → Dashboard**

<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="250" viewBox="0 0 1100 250" role="img" aria-label="Aerospace Fleet Intelligence architecture overview">
<rect width="1100" height="250" rx="20" fill="#07111f"/>
<text x="40" y="42" fill="#ffffff" font-family="Arial" font-size="24" font-weight="700">Aerospace Fleet Intelligence</text>
<text x="40" y="66" fill="#94a3b8" font-family="Arial" font-size="12">Telemetry → governed lake → distributed processing → warehouse → decisions</text>
<g font-family="Arial" text-anchor="middle">
<g fill="#102039" stroke="#38bdf8"><rect x="35" y="100" width="135" height="70" rx="12"/><rect x="190" y="100" width="135" height="70" rx="12"/><rect x="345" y="100" width="135" height="70" rx="12"/><rect x="500" y="100" width="135" height="70" rx="12"/><rect x="655" y="100" width="135" height="70" rx="12"/><rect x="810" y="100" width="135" height="70" rx="12"/><rect x="965" y="100" width="100" height="70" rx="12"/></g>
<g fill="#38bdf8" font-size="10" font-weight="700"><text x="102" y="125">SOURCE</text><text x="257" y="125">INGEST</text><text x="412" y="125">LAKE</text><text x="567" y="125">PROCESS</text><text x="722" y="125">MODEL</text><text x="877" y="125">SERVE</text><text x="1015" y="125">BI</text></g>
<g fill="#fff" font-size="12"><text x="102" y="147">NASA C-MAPSS</text><text x="257" y="147">ADF</text><text x="412" y="147">ADLS Gen2</text><text x="567" y="147">Databricks</text><text x="722" y="147">dbt</text><text x="877" y="147">Synapse</text><text x="1015" y="147">Dashboard</text></g>
</g>
<g stroke="#8b5cf6" stroke-width="3"><path d="M170 135h20M325 135h20M480 135h20M635 135h20M790 135h20M945 135h20"/></g>
<text x="40" y="215" fill="#a5b4fc" font-family="Arial" font-size="12">Fleet health • RUL • degradation • maintenance priority • scenario economics • data quality</text>
</svg>
</div>

> **Portfolio note:** C-MAPSS is simulated engine-degradation data. This project demonstrates data-engineering architecture and analytics patterns; it is not a certified aircraft safety or maintenance system.

## 1. What this project demonstrates

This project is intentionally structured like a real Data Engineering repository rather than a single notebook. It covers:

- **Ingestion:** parameterized Azure Data Factory pipeline
- **Storage:** ADLS Gen2 Bronze / Silver / Gold lake design
- **Distributed processing:** Databricks + PySpark transformations
- **Lakehouse:** Delta-ready analytical outputs
- **Transformation:** dbt staging, marts and data-quality tests
- **Warehouse:** Synapse serving layer and business views
- **Analytics:** fleet-health, RUL, risk and maintenance prioritization
- **Dashboard:** Streamlit business-facing operational view
- **Quality:** schema contracts, validation, tests and CI
- **Documentation:** architecture, runbook and interview walkthrough

## 2. Business problem

Maintenance teams need a repeatable way to turn high-volume engine telemetry into a prioritized view of fleet condition. The analytical layer answers:

1. Which engines deserve attention first?
2. How much remaining useful life is visible across the fleet?
3. Which engines exhibit stronger degradation or instability?
4. How should maintenance opportunities be prioritized?
5. How do intervention assumptions change the maintenance queue and scenario economics?

## 3. Repository structure

```text
.
├── adf/                         # Azure Data Factory metadata
│   ├── datasets/                # Dataset definitions
│   └── pipelines/               # Parameterized ingestion pipelines
├── assets/                      # Standalone SVG design artifacts / fallback previews
├── dashboard/                   # Streamlit + Plotly application
├── data/
│   ├── raw/                     # Source-data policy + optional local downloads
│   ├── reference/               # Schema and metadata contracts
│   └── processed/               # Gold output contract
├── databricks/                  # PySpark Bronze → Silver → Gold jobs
├── dbt/
│   ├── models/staging/          # Source-standardization models
│   ├── models/marts/            # Business-facing marts
│   └── tests/                   # Data-quality assertions
├── docs/                        # Runbook, architecture and portfolio walkthrough
├── notebooks/                   # Reproducible exploratory analytics
├── scripts/                     # Data acquisition / utility scripts
├── src/                         # Reusable Python analytics functions
├── synapse/                     # Warehouse DDL and business views
├── tests/                       # Python tests
├── .github/workflows/           # CI
├── .gitignore
├── requirements.txt
└── README.md
```

## 4. Technology stack

| Layer | Technology | Responsibility |
|---|---|---|
| Source | NASA C-MAPSS | Open simulated aerospace telemetry |
| Ingestion | **Azure Data Factory** | Parameterized ingestion and orchestration |
| Storage | **ADLS Gen2** | Durable Bronze/Silver/Gold zones |
| Processing | **Azure Databricks + PySpark** | Distributed cleansing and feature engineering |
| Table format | **Delta Lake** | Reliable lakehouse outputs |
| Modeling | **dbt** | Modular SQL, tests and marts |
| Warehouse | **Azure Synapse Analytics** | Analytical serving layer |
| Dashboard | **Streamlit + Plotly** | Business analytics |
| Quality | **pytest + dbt tests** | Automated validation |
| CI/CD | **GitHub Actions** | Pull-request and push validation |

## 5. End-to-end data flow

### Bronze — preserve the source

ADF copies the selected C-MAPSS dataset into ADLS without applying business transformations. This creates a replayable ingestion boundary.

### Silver — clean and enrich

Databricks/PySpark:

- applies an explicit schema
- removes duplicate engine/cycle records
- validates cycle values
- derives remaining useful life
- calculates sensor summaries and instability indicators
- produces a standardized analytical dataset

### Gold — create a decision layer

The Gold output contains the latest engine-health snapshot with RUL, health score and actionable risk band.

### dbt — model and test

The dbt layer creates reusable analytical models:

- `stg_engine_health`
- `mart_fleet_kpis`
- `fct_maintenance_opportunity`

Tests cover uniqueness, accepted risk values, relationships and health-score boundaries.

### Synapse — serve the business

Synapse exposes curated warehouse objects and views for dashboard consumption.

## 6. Business analytics

### Fleet health score

The project uses an interpretable prioritization heuristic:

```text
Health Score =
    0.40 × RUL Risk
  + 0.25 × Degradation Trend
  + 0.20 × Sensor Instability
  + 0.15 × Cycle Age Risk
```

Risk bands translate the analytical score into operational actions:

| Risk | Recommended action |
|---|---|
| **CRITICAL** | Immediate review |
| **HIGH** | Schedule intervention |
| **WATCH** | Increase monitoring |
| **HEALTHY** | Routine monitoring |

### Maintenance scenario analysis

The dashboard supports editable assumptions for:

- planned maintenance cost
- unplanned failure cost
- downtime cost
- maintenance capacity
- intervention RUL threshold

Outputs are clearly presented as **scenario estimates**, not real financial results.

## 7. Dashboard

The dashboard is designed around business questions rather than engineering logs:

- fleet KPI cards
- risk distribution
- engine RUL ranking
- health vs. RUL relationship
- maintenance opportunity queue
- scenario economics
- filters for engine/risk status

The visual preview is maintained as SVG in `assets/dashboard.svg`; the README architecture above is also embedded directly as SVG markup.

## 8. Data source

**NASA — C-MAPSS Jet Engine Simulated Data**

https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data

The source contains multivariate engine time-series data with operational settings, sensor measurements and degradation trajectories. The full archive is deliberately **not committed** to GitHub. Use `scripts/download_cmapss.py` when the full dataset is required.

## 9. Run locally

```bash
git clone https://github.com/manishkallu01-wq/aerospace-fleet-intelligence.git
cd aerospace-fleet-intelligence
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
streamlit run dashboard/app.py
```

Download source data:

```bash
python scripts/download_cmapss.py
```

## 10. Azure deployment path

1. Provision ADLS Gen2 and create an `aerospace` filesystem.
2. Configure ADF HTTP and ADLS linked services using managed identity where possible.
3. Import the ADF datasets and pipeline under `adf/`.
4. Parameterize the pipeline with `dataset_id`, `source_url` and `bronze_path`.
5. Import/run the Databricks Bronze → Silver → Gold jobs.
6. Publish Gold data to the Synapse serving layer.
7. Configure dbt against the warehouse and run `dbt debug`, `dbt run`, `dbt test`.
8. Point the dashboard/BI layer at the Synapse business views.

## 11. Data quality and reliability

- explicit source schema
- engine/cycle duplicate checks
- cycle-range validation
- null and required-field checks
- health score contract `[0,100]`
- dbt uniqueness and relationship tests
- accepted-value tests for risk bands
- CI on every push and pull request
- raw-zone replay boundary
- source-data download excluded from Git history

## 12. Production hardening

A production implementation could add Managed Identity + Key Vault, Microsoft Purview governance, Unity Catalog, metadata-driven ADF ingestion, incremental Delta processing, Azure Monitor/Log Analytics, environment promotion, data contracts, model registry and platform cost monitoring.

## 13. Documentation

- [`docs/architecture.md`](docs/architecture.md) — design and data contracts
- [`docs/runbook.md`](docs/runbook.md) — setup and operations
- [`docs/portfolio_walkthrough.md`](docs/portfolio_walkthrough.md) — interview-ready explanation
- [`dbt/README.md`](dbt/README.md) — transformation layer
- [`data/raw/README.md`](data/raw/README.md) — source-data policy

## 14. Author

**Manish Reddy Kallu** · Data Engineering Portfolio

[GitHub](https://github.com/manishkallu01-wq) · [LinkedIn](https://www.linkedin.com/in/manish-reddy-kallu/)

---

**Independent portfolio project. Public/simulated data only. No real aircraft, airline, OEM, safety or maintenance decisions are represented.**
