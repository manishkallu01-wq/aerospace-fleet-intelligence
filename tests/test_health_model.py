import pandas as pd
import pytest

from src.aerospace_analytics import build_evaluation_table, classify_rul, load_fd001_rul, summarize


def test_risk_band_boundaries():
    source = pd.Series([30, 31, 60, 61, 90, 91])
    assert classify_rul(source).tolist() == [
        "CRITICAL", "HIGH", "HIGH", "WATCH", "WATCH", "HEALTHY"
    ]


def test_summary_counts_reconcile():
    source = pd.DataFrame(
        {"engine_id": [1, 2, 3, 4], "true_rul_cycles": [10, 40, 80, 100]}
    )
    metrics = summarize(build_evaluation_table(source))
    assert metrics == {
        "engines": 4,
        "mean_rul": 57.5,
        "median_rul": 60.0,
        "min_rul": 10,
        "max_rul": 100,
        "critical": 1,
        "high": 1,
        "maintenance_queue": 2,
        "watch": 1,
        "healthy": 1,
    }


def test_loader_requires_100_engines(tmp_path):
    path = tmp_path / "RUL_FD001.txt"
    path.write_text("\n".join(["10"] * 99))
    with pytest.raises(ValueError, match="Expected 100 FD001 test engines"):
        load_fd001_rul(path)


def test_loader_rejects_blank_values(tmp_path):
    path = tmp_path / "RUL_FD001.txt"
    path.write_text("\n".join(["10"] * 99 + [""]))
    with pytest.raises(ValueError, match="missing values"):
        load_fd001_rul(path)


def test_loader_rejects_negative_rul(tmp_path):
    path = tmp_path / "RUL_FD001.txt"
    path.write_text("\n".join(["10"] * 99 + ["-1"]))
    with pytest.raises(ValueError, match="cannot be negative"):
        load_fd001_rul(path)


def test_evaluation_requires_expected_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        build_evaluation_table(pd.DataFrame({"engine_id": [1]}))
