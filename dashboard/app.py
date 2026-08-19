from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Aerospace Fleet Intelligence", page_icon="✈️", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "reports" / "fd001_engine_rul.csv"

st.title("✈️ Aerospace Fleet Intelligence")
st.caption("NASA FD001 results • RUL distribution • maintenance priorities")

st.info(
    "This dashboard uses the true RUL values supplied with the FD001 test set. "
    "They are used here to show and check the benchmark results, not as live predictions."
)

if not RESULTS.exists():
    st.error("Result file not found: reports/fd001_engine_rul.csv")
    st.stop()

result = pd.read_csv(RESULTS)
required = {"engine_id", "true_rul_cycles", "risk_band", "priority"}
missing = required.difference(result.columns)
if missing:
    st.error(f"Result file is missing required columns: {sorted(missing)}")
    st.stop()

result["risk_band"] = pd.Categorical(
    result["risk_band"], categories=["CRITICAL", "HIGH", "WATCH", "HEALTHY"], ordered=True
)

rul = result["true_rul_cycles"]
engine_count = len(result)
critical = int((rul <= 30).sum())
high = int(((rul > 30) & (rul <= 60)).sum())
queue = int((rul <= 60).sum())
queue_pct = queue / engine_count * 100

st.markdown("### 📊 Fleet summary")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Test engines", engine_count)
c2.metric("Mean RUL", f"{rul.mean():.2f} cycles")
c3.metric("Median RUL", f"{rul.median():.0f} cycles")
c4.metric("Critical", f"{critical} / {engine_count}")
c5.metric("Maintenance queue", f"{queue} / {engine_count}")

left, right = st.columns([1.35, 1])
with left:
    st.markdown("### ⏱️ RUL distribution")
    fig = px.histogram(
        result,
        x="true_rul_cycles",
        nbins=18,
        labels={"true_rul_cycles": "True RUL (cycles)"},
        title="FD001 test-engine RUL",
    )
    fig.add_vline(x=30, line_dash="dash", annotation_text="Critical: 30")
    fig.add_vline(x=60, line_dash="dash", annotation_text="Queue: 60")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### 🚦 Risk distribution")
    risk = (
        result["risk_band"]
        .value_counts()
        .reindex(["CRITICAL", "HIGH", "WATCH", "HEALTHY"], fill_value=0)
        .rename_axis("risk_band")
        .reset_index(name="engines")
    )
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

st.markdown("### 💡 Findings")
a, b, c = st.columns(3)
a.metric("RUL range", f"{rul.min()}–{rul.max()} cycles")
b.metric("Critical + high", f"{critical + high} engines")
c.metric("Healthy population", f"{int((rul > 90).sum())} engines")

st.markdown("### 🎯 Takeaway")
st.success(
    f"{queue_pct:.0f}% of the test engines ({queue} of {engine_count}) are at or below 60 RUL cycles. "
    f"That includes {critical} engines at or below 30 cycles and {high} engines from 31–60 cycles. "
    "For this benchmark, the lower end of the RUL distribution is more useful for prioritization than the fleet average alone."
)
st.caption(
    "Source: NASA C-MAPSS FD001. The RUL values shown here are test-set ground truth used for benchmark analysis. "
    "A predictive version of the dashboard would use model estimates instead."
)
