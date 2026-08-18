import pandas as pd
import streamlit as st

st.set_page_config(page_title="Aerospace Fleet Intelligence", page_icon="✈️", layout="wide")
st.title("✈️ Aerospace Fleet Intelligence")
st.caption("Fleet health • RUL • maintenance prioritization")

sample = pd.DataFrame({
    "engine_id": [101, 102, 103, 104, 105, 106],
    "rul": [18, 42, 71, 96, 27, 58],
    "health_score": [18, 43, 72, 91, 29, 61],
    "risk_band": ["CRITICAL", "HIGH", "WATCH", "HEALTHY", "HIGH", "WATCH"],
})

c1, c2, c3, c4 = st.columns(4)
c1.metric("Engines monitored", len(sample))
c2.metric("Elevated risk", int((sample.health_score < 50).sum()))
c3.metric("Average RUL", f"{sample.rul.mean():.0f} cycles")
c4.metric("Average health", f"{sample.health_score.mean():.0f}/100")

st.subheader("Fleet risk")
st.bar_chart(sample.set_index("engine_id")["health_score"])

st.subheader("Maintenance queue")
st.dataframe(sample.sort_values("health_score"), use_container_width=True, hide_index=True)
st.info("Demo values are illustrative. Connect the Synapse business view to replace the sample dataset with Gold-layer outputs.")
