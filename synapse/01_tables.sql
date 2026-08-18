CREATE TABLE dbo.fct_engine_health (
    engine_id INT NOT NULL,
    cycle INT NOT NULL,
    sensor_mean FLOAT NULL,
    sensor_stddev FLOAT NULL,
    condition_age_proxy FLOAT NULL,
    risk_band VARCHAR(20) NOT NULL,
    CONSTRAINT CK_fct_engine_health_risk_band
        CHECK (risk_band IN ('CRITICAL', 'HIGH', 'WATCH', 'HEALTHY'))
);

-- The PySpark Gold layer is responsible for publishing this contract.
-- This DDL defines the Synapse serving boundary; it does not imply a live workspace.
