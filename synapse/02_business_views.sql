CREATE OR ALTER VIEW dbo.vw_fleet_kpis AS
SELECT
    COUNT(*) AS engine_count,
    AVG(CAST(health_score AS decimal(10,2))) AS avg_health_score,
    AVG(CAST(rul AS decimal(10,2))) AS avg_rul,
    SUM(CASE WHEN risk_band IN ('CRITICAL','HIGH') THEN 1 ELSE 0 END) AS elevated_risk_engines,
    SUM(CASE WHEN risk_band = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_engines
FROM dbo.fct_engine_health;

CREATE OR ALTER VIEW dbo.vw_maintenance_queue AS
SELECT
    engine_id,
    cycle,
    rul,
    health_score,
    risk_band,
    CASE
        WHEN risk_band = 'CRITICAL' THEN 'Immediate review'
        WHEN risk_band = 'HIGH' THEN 'Schedule intervention'
        WHEN risk_band = 'WATCH' THEN 'Increase monitoring'
        ELSE 'Routine monitoring'
    END AS recommended_action
FROM dbo.fct_engine_health;
