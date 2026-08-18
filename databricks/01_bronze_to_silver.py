from pyspark.sql import functions as F

COLUMNS = ["engine_id", "cycle"] + [f"op_setting_{i}" for i in range(1, 4)] + [f"sensor_{i}" for i in range(1, 22)]


def transform_bronze(df):
    """Standardize C-MAPSS telemetry at engine × cycle grain."""
    typed = df.toDF(*COLUMNS)
    sensor_cols = [F.col(f"sensor_{i}").cast("double") for i in range(1, 22)]
    return (
        typed
        .withColumn("engine_id", F.col("engine_id").cast("int"))
        .withColumn("cycle", F.col("cycle").cast("int"))
        .dropDuplicates(["engine_id", "cycle"])
        .withColumn("sensor_mean", sum(sensor_cols) / F.lit(len(sensor_cols)))
        .withColumn(
            "sensor_stddev",
            F.sqrt(
                sum((c - F.col("sensor_mean")) ** 2 for c in sensor_cols) / F.lit(len(sensor_cols))
            ),
        )
    )


def add_training_rul(df):
    """Derive run-to-failure RUL for training trajectories only."""
    max_cycle = df.groupBy("engine_id").agg(F.max("cycle").alias("failure_cycle"))
    return (
        df.join(max_cycle, "engine_id")
        .withColumn("rul", F.col("failure_cycle") - F.col("cycle"))
        .drop("failure_cycle")
    )
