from pyspark.sql import functions as F

# Expected C-MAPSS columns after source parsing.
COLUMNS = ["engine_id", "cycle"] + [f"op_setting_{i}" for i in range(1, 4)] + [f"sensor_{i}" for i in range(1, 22)]


def transform_bronze(df):
    """Standardize telemetry and derive cycle-level engineering features."""
    typed = df.toDF(*COLUMNS)
    return (
        typed
        .withColumn("engine_id", F.col("engine_id").cast("int"))
        .withColumn("cycle", F.col("cycle").cast("int"))
        .dropDuplicates(["engine_id", "cycle"])
        .withColumn("sensor_mean", F.expr("aggregate(array(sensor_1,sensor_2,sensor_3,sensor_4,sensor_5), cast(0.0 as double), (acc,x) -> acc + coalesce(x,0.0)) / 5.0"))
        .withColumn("sensor_instability", F.abs(F.col("sensor_3") - F.col("sensor_3").cast("double")))
    )


def add_rul(df):
    max_cycle = df.groupBy("engine_id").agg(F.max("cycle").alias("max_cycle"))
    return df.join(max_cycle, "engine_id").withColumn("rul", F.col("max_cycle") - F.col("cycle")).drop("max_cycle")
