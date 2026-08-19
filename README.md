# ✈️ Aerospace Fleet Intelligence

A reproducible analysis of NASA C-MAPSS FD001 remaining-useful-life labels, paired with an Azure-oriented data-platform design.

> This is an engineering study using simulated benchmark data. It is not an aircraft maintenance system and its thresholds are not maintenance limits.

![Architecture](assets/architecture.svg)

## Business question

How can a fleet team turn engine-level health data into a consistent maintenance-priority view while keeping the source, transformations, quality rules, and published metrics traceable?

## What runs locally

```text
data/reference/RUL_FD001.txt
          ↓
validated pandas transformation
          ↓
risk-band classification
          ↓
reports/fd001_engine_rul.csv
          ↓
Streamlit dashboard
```

The committed 100-row RUL input is the compact FD001 label vector required to rebuild the report. Full training and test telemetry is not committed.

## Results

| Metric | Value |
|---|---:|
| Engines | 100 |
| Mean RUL | 75.52 cycles |
| Median RUL | 86 cycles |
| Minimum / maximum | 7 / 145 cycles |
| Critical, ≤30 | 25 |
| High, 31–60 | 14 |
| Watch, 61–90 | 15 |
| Healthy, >90 | 46 |

The 39 engines at or below 60 cycles form the project’s review queue. The average alone hides this low-RUL tail, so the dashboard keeps both fleet-level statistics and engine-level priorities visible. These are benchmark labels and project-defined bands, not model predictions or aviation policy.

![Execution results](assets/fd001-execution-results.svg)

## Reproduce the report

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_project.py
pytest -q
python scripts/build_fd001_results.py
git diff --exit-code -- reports/fd001_engine_rul.csv
streamlit run dashboard/app.py
```

The final `git diff` command confirms that rebuilding the report produces the committed artifact exactly. CI runs the same validation, tests, result build, and diff check.

## Risk bands

| RUL | Band | Project use |
|---:|---|---|
| ≤30 | 🔴 Critical | Review first |
| 31–60 | 🟠 High | Plan intervention |
| 61–90 | 🟡 Watch | Monitor |
| >90 | 🟢 Healthy | Normal review |

## Cloud design

The repository also contains deployable configuration examples for:

```text
ADF ingestion → ADLS Bronze → Databricks/PySpark Silver and Gold
             → dbt models → Synapse views → BI
```

Files under `adf/`, `databricks/`, `dbt/`, and `synapse/` are scaffolding for that design. No live Azure deployment is claimed. Subscription resources, credentials, environment parameters, deployment automation, and cloud integration evidence are outside this repository.

## Full C-MAPSS data

To work with the complete training and test telemetry, set `CMAPSS_URL` to the current official archive URL and run:

```bash
CMAPSS_URL="..." python scripts/download_cmapss.py
```

The archive is written under `data/raw/` and remains outside Git.

## Repository guide

- [Architecture](docs/architecture.md)
- [Data dictionary](docs/data_dictionary.md)
- [Business interpretation](docs/business_insights.md)
- [Runbook](docs/runbook.md)
- [Project walkthrough](docs/project_story.md)
- [Report artifacts](reports/README.md)

## Limitations

The local result uses true FD001 RUL labels; it does not train or evaluate a predictive model. The cloud files have not been executed against a live Azure environment. Cost savings cannot be calculated from C-MAPSS because it contains no labor, downtime, parts, or intervention-cost data.
