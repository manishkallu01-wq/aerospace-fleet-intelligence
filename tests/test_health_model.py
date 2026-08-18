import pandas as pd


def test_risk_bands_are_valid():
    df = pd.DataFrame({"risk_band": ["CRITICAL", "HIGH", "WATCH", "HEALTHY"]})
    assert set(df.risk_band).issubset({"CRITICAL", "HIGH", "WATCH", "HEALTHY"})


def test_health_score_contract():
    scores = pd.Series([0.0, 25.0, 50.0, 75.0, 100.0])
    assert scores.between(0, 100).all()
