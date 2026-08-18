# Runbook

## Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
streamlit run dashboard/app.py
```

## Source data

Set `CMAPSS_URL` to the current NASA source download URL and run `python scripts/download_cmapss.py`. Full source data stays outside Git history.

## Azure

Provision ADLS Gen2, ADF, Databricks and Synapse. Import the JSON metadata under `adf/`, run the Databricks jobs, publish the Gold output to Synapse, then execute the dbt models/tests.

## Operational checks

- Verify the ADF copy activity completed.
- Confirm Bronze file count and source partition.
- Check duplicate engine/cycle records.
- Check Silver/Gold row counts and null rates.
- Run dbt tests before publishing warehouse views.
- Confirm dashboard freshness timestamp before business use.
