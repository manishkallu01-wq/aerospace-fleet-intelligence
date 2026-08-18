{{ config(materialized='table') }}

select
    engine_id,
    cycle,
    condition_age_proxy,
    risk_band,
    case
        when risk_band = 'CRITICAL' then 'Immediate review'
        when risk_band = 'HIGH' then 'Schedule intervention'
        when risk_band = 'WATCH' then 'Increase monitoring'
        else 'Routine monitoring'
    end as recommended_action
from {{ ref('stg_engine_health') }}
