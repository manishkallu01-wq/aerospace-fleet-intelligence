# Runbook

## Run locally

Create a virtual environment, install the project requirements, run the tests, and start the dashboard:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
streamlit run dashboard/app.py
```

The dashboard reads the committed FD001 result file at `reports/fd001_engine_rul.csv`.

## Download the source data

Set `CMAPSS_URL` to the current NASA C-MAPSS download URL and run:

```bash
python scripts/download_cmapss.py
```

The full source dataset is kept outside Git history.

## Azure setup

For an Azure deployment, provision ADLS Gen2, ADF, Databricks, and Synapse. Import the files under `adf/`, configure the linked services and paths for the target environment, then run the PySpark jobs and publish the Gold data to Synapse. The dbt models can then be configured against the warehouse.

The repository contains the deployment files, but the Azure resources and credentials are not included here.

## Checks to run after a cloud load

- Check that the ADF copy completed.
- Confirm the Bronze file count.
- Check for duplicate engine/cycle rows.
- Compare Silver and Gold row counts.
- Check null rates in the main fields.
- Run the dbt tests before publishing views.
- Confirm the dashboard data timestamp before using it for reporting.
