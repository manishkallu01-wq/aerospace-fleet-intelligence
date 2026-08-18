{{ config(materialized='view') }}

select
    cast(engine_id as integer) as engine_id,
    cast(cycle as integer) as cycle,
    cast(sensor_mean as double) as sensor_mean,
    cast(sensor_stddev as double) as sensor_stddev,
    cast(condition_age_proxy as double) as condition_age_proxy,
    cast(risk_band as varchar) as risk_band
from {{ source('aerospace', 'fct_engine_health') }}
