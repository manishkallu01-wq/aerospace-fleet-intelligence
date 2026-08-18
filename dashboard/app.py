import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Aerospace Fleet Intelligence", page_icon="✈️", layout="wide")
st.title("✈️ Aerospace Fleet Intelligence")
st.caption("Executive fleet health • remaining useful life • maintenance prioritization")

st.info("NASA C-MAPSS FD001 profile: 100 training trajectories, 100 test trajectories, one operating condition and one fault mode. The test trajectories end before failure, making early-warning prioritization the core business problem.")

# Portfolio preview records. These values are explicitly illustrative until Gold data is connected.
preview = pd.DataFrame({
    "engine_id": [101, 102, 103, 104, 105, 106, 107, 108],
    "rul": [18, 42, 71, 96, 27, 58, 34, 83],
    "health_score": [18, 43, 72, 91, 29, 61, 37, 79],
})
preview["risk_band"] = pd.cut(
    preview["health_score"],
    bins=[-1, 24, 49, 74, 100],
    labels=["CRITICAL", "HIGH", "WATCH", "HEALTHY"],
)
preview["recommended_action"] = preview["risk_band"].map({
    "CRITICAL": "Immediate review",
    "HIGH": "Schedule intervention",
    "WATCH": "Increase monitoring",
    "HEALTHY": "Routine monitoring",
})

st.markdown("### 📊 Executive snapshot")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Engines in preview", len(preview))
c2.metric("Elevated-risk engines", int((preview.health_score < 50).sum()))
c3.metric("Average RUL", f"{preview.rul.mean():.0f} cycles")
c4.metric("Average health", f"{preview.health_score.mean():.0f}/100")

left, right = st.columns([1.35, 1])
with left:
    st.markdown("### 🎯 Health vs. remaining life")
    fig = px.scatter(
        preview,
        x="rul",
        y="health_score",
        color="risk_band",
        hover_data=["engine_id", "recommended_action"],
        labels={"rul": "Remaining useful life (cycles)", "health_score": "Health score"},
    )
    fig.update_layout(height=390, legend_title_text="Risk")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### 🚦 Risk distribution")
    risk = preview["risk_band"].value_counts().rename_axis("risk_band").reset_index(name="engines")
    fig = px.bar(risk, x="risk_band", y="engines", text="engines")
    fig.update_layout(height=390, xaxis_title=None, yaxis_title="Engines")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🔧 Maintenance priority queue")
queue = preview.sort_values(["health_score", "rul"]).copy()
st.dataframe(queue[["engine_id", "rul", "health_score", "risk_band", "recommended_action"]], use_container_width=True, hide_index=True)

st.markdown("### 💡 Business questions this dashboard answers")
q1, q2, q3 = st.columns(3)
q1.markdown("**1. Where should planners look first?**\n\nRank engines by health/risk so scarce maintenance capacity is focused on the most urgent cases.")
q2.markdown("**2. How much life remains?**\n\nUse RUL as the common planning measure while keeping the underlying telemetry at engine × cycle grain.")
q3.markdown("**3. What changes operationally?**\n\nConvert analytical risk into review, intervention, monitoring or routine actions instead of stopping at a chart.")

st.markdown("### 🧭 Source-backed portfolio insight")
st.success("Because NASA's FD001 test trajectories stop before system failure, the strongest portfolio story is not 'we detected failures after they happened.' It is 'we built a pipeline that turns pre-failure telemetry into an explainable maintenance-prioritization layer.'")
st.caption("Preview KPI values and engine-level records are illustrative. Replace them with the Gold/Synapse dataset to make the dashboard production-data driven.")
