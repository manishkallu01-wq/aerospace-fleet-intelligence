from pyspark.sql import functions as F


def build_gold(df):
    """Create a latest-engine snapshot with an explicit, non-predictive age proxy.

    This is a portfolio baseline, not a trained RUL model. Prospective RUL must be
    supplied by a separately evaluated model before operational use.
    """
    latest = df.groupBy("engine_id").agg(F.max("cycle").alias("latest_cycle"))
    current = (
        df.join(
            latest,
            (df.engine_id == latest.engine_id) & (df.cycle == latest.latest_cycle),
        )
        .drop(latest.engine_id, "latest_cycle")
    )

    max_cycle = current.agg(F.max("cycle").alias("fleet_max_cycle")).collect()[0]["fleet_max_cycle"]
    age_proxy = F.greatest(
        F.lit(0.0),
        F.least(F.lit(100.0), 100.0 * (1.0 - F.col("cycle") / F.lit(float(max_cycle))),),
    )

    return (
        current
        .withColumn("condition_age_proxy", age_proxy)
        .withColumn(
            "risk_band",
            F.when(F.col("condition_age_proxy") < 25, "CRITICAL")
            .when(F.col("condition_age_proxy") < 50, "HIGH")
            .when(F.col("condition_age_proxy") < 75, "WATCH")
            .otherwise("HEALTHY"),
        )
        .select(
            "engine_id",
            "cycle",
            "sensor_mean",
            "sensor_stddev",
            "condition_age_proxy",
            "risk_band",
        )
    )
