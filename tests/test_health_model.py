import pandas as pd

from src.aerospace_analytics import build_evaluation_table, summarize


def test_risk_bands_are_valid():
    df = pd.DataFrame({"risk_band": ["CRITICAL", "HIGH", "WATCH", "HEALTHY"]})
    assert set(df.risk_band).issubset({"CRITICAL", "HIGH", "WATCH", "HEALTHY"})


def test_fd001_threshold_boundaries():
    source = pd.DataFrame({"engine_id": [1, 2, 3, 4], "true_rul_cycles": [30, 31, 60, 61]})
    result = build_evaluation_table(source)
    assert result["risk_band"].tolist() == ["CRITICAL", "HIGH", "HIGH", "WATCH"]


def test_summary_counts_are_reconciled():
    source = pd.DataFrame({"engine_id": [1, 2, 3, 4], "true_rul_cycles": [10, 40, 80, 100]})
    metrics = summarize(build_evaluation_table(source))
    assert metrics["engines"] == 4
    assert metrics["maintenance_queue"] == 2
    assert metrics["critical"] == 1
    assert metrics["high"] == 1
    assert metrics["watch"] == 1
    assert metrics["healthy"] == 1
