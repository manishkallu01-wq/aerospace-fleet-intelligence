from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Aerospace Fleet Intelligence", page_icon="✈️", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "reports" / "fd001_engine_rul.csv"

st.title("✈️ Aerospace Fleet Intelligence")
st.caption("FD001 benchmark evaluation • RUL distribution • maintenance prioritization")

st.info(
    "Evaluation mode: the dashboard is driven by the committed FD001 ground-truth RUL "
    "artifact. These labels are used to evaluate the engineering/analytics layer; they "
    "must not be treated as future RUL known to an operator in a prospective system."
)

if not RESULTS.exists():
    st.error("Evaluation artifact not found: reports/fd001_engine_rul.csv")
    st.stop()

result = pd.read_csv(RESULTS)
result["risk_band"] = pd.Categorical(
    result["risk_band"], categories=["CRITICAL", "HIGH", "WATCH", "HEALTHY"], ordered=True
)

rul = result["true_rul_cycles"]
critical = int((rul <= 30).sum())
high = int(((rul > 30) & (rul <= 60)).sum())
queue = int((rul <= 60).sum())

st.markdown("### 📊 Evaluation snapshot")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Test engines", len(result))
c2.metric("Mean RUL", f"{rul.mean():.2f} cycles")
c3.metric("Median RUL", f"{rul.median():.0f} cycles")
c4.metric("Critical", f"{critical} / 100")
c5.metric("Maintenance queue", f"{queue} / 100")

left, right = st.columns([1.35, 1])
with left:
    st.markdown("### ⏱️ RUL distribution")
    fig = px.histogram(
        result,
        x="true_rul_cycles",
        nbins=18,
        labels={"true_rul_cycles": "True RUL (cycles)"},
        title="FD001 test-engine remaining useful life",
    )
    fig.add_vline(x=30, line_dash="dash", annotation_text="Critical threshold: 30")
    fig.add_vline(x=60, line_dash="dash", annotation_text="Queue threshold: 60")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### 🚦 Risk distribution")
    risk = result["risk_band"].value_counts().reindex(
        ["CRITICAL", "HIGH", "WATCH", "HEALTHY"], fill_value=0
    ).rename_axis("risk_band").reset_index(name="engines")
    fig = px.bar(risk, x="risk_band", y="engines", text="engines")
    fig.update_layout(height=420, xaxis_title=None, yaxis_title="Engines")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🔧 Maintenance priority queue")
priority = result.sort_values(["priority", "true_rul_cycles"]).head(20).copy()
priority = priority.rename(columns={"true_rul_cycles": "RUL cycles"})
st.dataframe(
    priority[["engine_id", "RUL cycles", "risk_band", "priority"]],
    use_container_width=True,
    hide_index=True,
)

st.markdown("### 💡 Technical findings")
a, b, c = st.columns(3)
a.metric("RUL range", f"{rul.min()}–{rul.max()} cycles")
b.metric("High-risk tail", f"{critical + high} engines")
c.metric("Healthy population", f"{int((rul > 90).sum())} engines")

st.markdown("### 🎯 Business interpretation")
st.success(
    f"{queue}% of the benchmark test fleet falls at or below 60 RUL cycles, including "
    f"{critical} critical engines and {high} high-risk engines. A planner should use "
    "the lower tail—not the fleet average alone—to prioritize intervention."
)
st.caption(
    "Source: NASA C-MAPSS FD001 benchmark. Ground-truth RUL is an evaluation label. "
    "A production deployment would replace it with a prediction/Gold-layer estimate available at decision time."
)
