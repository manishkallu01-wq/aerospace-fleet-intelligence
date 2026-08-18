# Architecture

## Logical flow

`NASA C-MAPSS → ADF → ADLS Bronze → Databricks/PySpark → ADLS Silver/Gold → dbt → Synapse → Dashboard`

## Design principles

1. **Replayability:** raw ingestion remains separate from transformations.
2. **Separation of concerns:** orchestration, storage, processing, modeling and serving are distinct layers.
3. **Testability:** data contracts and automated checks sit close to transformation logic.
4. **Business-first Gold layer:** downstream consumers receive engine-health and maintenance-ready data rather than raw telemetry.
5. **Security-ready:** managed identity and secret management are preferred over credentials in code.

## Grain

The Silver telemetry table is at **engine × operating cycle** grain. The primary Gold analytical record is the latest observed state for each engine.

## Production evolution

The portfolio implementation can be promoted with metadata-driven ADF pipelines, incremental Delta loads, Unity Catalog/Purview governance, Azure Monitor, environment-specific configuration, CI/CD promotion and managed identities.
