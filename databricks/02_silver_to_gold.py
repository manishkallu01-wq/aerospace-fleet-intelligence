from pyspark.sql import functions as F


def build_gold(df):
    """Create an engine-health snapshot for downstream warehouse analytics."""
    latest = df.groupBy("engine_id").agg(F.max("cycle").alias("latest_cycle"))
    current = df.join(latest, (df.engine_id == latest.engine_id) & (df.cycle == latest.latest_cycle)).drop(latest.engine_id, "latest_cycle")
    return (
        current
        .withColumn("health_score", F.greatest(F.lit(0.0), F.least(F.lit(100.0), 100.0 - F.col("cycle") * 0.25)))
        .withColumn("risk_band", F.when(F.col("health_score") < 25, "CRITICAL").when(F.col("health_score") < 50, "HIGH").when(F.col("health_score") < 75, "WATCH").otherwise("HEALTHY"))
        .select("engine_id", "cycle", "rul", "sensor_mean", "sensor_instability", "health_score", "risk_band")
    )
