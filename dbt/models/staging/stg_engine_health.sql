{{ config(materialized='view') }}

select
    cast(engine_id as integer) as engine_id,
    cast(cycle as integer) as cycle,
    cast(rul as integer) as rul,
    cast(sensor_mean as double) as sensor_mean,
    cast(sensor_instability as double) as sensor_instability,
    cast(health_score as double) as health_score,
    cast(risk_band as varchar) as risk_band
from {{ source('aerospace', 'engine_health') }}
