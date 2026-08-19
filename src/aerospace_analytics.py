"""Reusable local analytics for the NASA C-MAPSS FD001 evaluation."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RISK_BANDS = ["CRITICAL", "HIGH", "WATCH", "HEALTHY"]


def load_fd001_rul(path: str | Path) -> pd.DataFrame:
    """Load and validate the FD001 test RUL vector."""
    values = pd.read_csv(path, header=None, names=["true_rul_cycles"])

    if values.empty:
        raise ValueError("FD001 RUL file is empty")
    if values["true_rul_cycles"].isna().any():
        raise ValueError("FD001 RUL file contains missing values")
    if (values["true_rul_cycles"] < 0).any():
        raise ValueError("FD001 RUL values cannot be negative")
    if len(values) != 100:
        raise ValueError(f"Expected 100 FD001 test engines, found {len(values)}")

    values["engine_id"] = range(1, len(values) + 1)
    return values[["engine_id", "true_rul_cycles"]]


def classify_rul(rul: pd.Series) -> pd.Series:
    """Apply the project RUL bands used for the benchmark dashboard."""
    return pd.cut(
        rul,
        bins=[-float("inf"), 30, 60, 90, float("inf")],
        labels=RISK_BANDS,
    ).astype(str)


def build_evaluation_table(rul: pd.DataFrame) -> pd.DataFrame:
    """Build the engine-level result used by reports and the dashboard."""
    required = {"engine_id", "true_rul_cycles"}
    missing = required.difference(rul.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = rul.copy()
    result["risk_band"] = classify_rul(result["true_rul_cycles"])
    priority = {"CRITICAL": 1, "HIGH": 2, "WATCH": 3, "HEALTHY": 4}
    result["priority"] = result["risk_band"].map(priority).astype(int)
    return result


def summarize(result: pd.DataFrame) -> dict[str, float | int]:
    """Return deterministic fleet-level metrics."""
    rul = result["true_rul_cycles"]
    return {
        "engines": int(result["engine_id"].nunique()),
        "mean_rul": float(rul.mean()),
        "median_rul": float(rul.median()),
        "min_rul": int(rul.min()),
        "max_rul": int(rul.max()),
        "critical": int((rul <= 30).sum()),
        "high": int(((rul > 30) & (rul <= 60)).sum()),
        "maintenance_queue": int((rul <= 60).sum()),
        "watch": int(((rul > 60) & (rul <= 90)).sum()),
        "healthy": int((rul > 90).sum()),
    }
