# 🏗️ Architecture

## 🔄 Data flow

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
      +---- Silver: engine x cycle telemetry
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

The project keeps ingestion, storage, transformation, modeling, and reporting in separate layers. That makes it easier to test each part and replace one component without rewriting the rest of the flow.

## 📐 Data grain

The Silver telemetry data is stored at **engine x operating cycle** grain.

The main Gold record represents the latest available state for each engine.

## 🧩 What is implemented

The repository contains:

- ADF dataset and pipeline metadata
- PySpark transformations for Bronze-to-Silver and Silver-to-Gold processing
- dbt staging and mart SQL
- Synapse DDL and reporting views
- Python analysis and tests
- a Streamlit dashboard driven by the committed FD001 result file

The Azure files are intended to be configured and run in an Azure environment. The repository does not claim that those cloud resources are currently running.

## 🚀 Moving toward production

A production deployment would add managed identities, Key Vault, incremental loads, monitoring, data governance, environment-specific configuration, and CI/CD deployment into Azure.
