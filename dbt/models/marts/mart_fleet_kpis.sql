{{ config(materialized='table') }}

select
    count(*) as engine_count,
    avg(health_score) as avg_health_score,
    avg(rul) as avg_rul,
    sum(case when risk_band in ('CRITICAL','HIGH') then 1 else 0 end) as elevated_risk_engines,
    sum(case when risk_band = 'CRITICAL' then 1 else 0 end) as critical_engines
from {{ ref('stg_engine_health') }}
