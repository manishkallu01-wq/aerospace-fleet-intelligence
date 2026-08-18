"""Reusable local analytics for the NASA C-MAPSS FD001 evaluation."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

RISK_BANDS = ["CRITICAL", "HIGH", "WATCH", "HEALTHY"]


def load_fd001_rul(path: str | Path) -> pd.DataFrame:
    """Load the official FD001 test RUL vector in engine-id order."""
    values = pd.read_csv(path, header=None, names=["true_rul_cycles"])
    values["engine_id"] = range(1, len(values) + 1)
    return values[["engine_id", "true_rul_cycles"]]


def classify_rul(rul: pd.Series) -> pd.Series:
    """Apply transparent planning thresholds to ground-truth/evaluation RUL."""
    return pd.cut(
        rul,
        bins=[-float("inf"), 30, 60, 90, float("inf")],
        labels=RISK_BANDS,
    ).astype(str)


def build_evaluation_table(rul: pd.DataFrame) -> pd.DataFrame:
    """Build the machine-readable evaluation result used by reports/dashboard."""
    result = rul.copy()
    result["risk_band"] = classify_rul(result["true_rul_cycles"])
    priority = {"CRITICAL": 1, "HIGH": 2, "WATCH": 3, "HEALTHY": 4}
    result["priority"] = result["risk_band"].map(priority).astype(int)
    return result


def summarize(result: pd.DataFrame) -> dict[str, float | int]:
    """Return deterministic portfolio-level metrics."""
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
