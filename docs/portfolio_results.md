# 📈 Portfolio Results & Analytics

> **Evidence layer:** this page separates reproducible source-data findings from illustrative dashboard preview values.

## ✈️ Dataset profile

The NASA C-MAPSS FD001 benchmark is a simulated turbofan-engine degradation dataset. It contains multivariate sensor measurements across operating cycles and is designed around degradation/run-to-failure analysis.

The project deliberately does **not** claim that these observations represent a real airline fleet or certified maintenance system.

## 🎯 Business questions

### 1. Which engines should receive attention first?

**Answer:** the Gold layer ranks the latest engine state using an explainable combination of remaining useful life, degradation behavior, sensor instability and cycle-age risk.

**Business value:** maintenance planners receive a prioritized queue rather than a raw telemetry dump.

### 2. How much useful life remains?

**Answer:** RUL is expressed in operating cycles and becomes the common planning measure across engines.

**Business value:** planners can group engines into intervention, monitoring and routine-review windows.

### 3. Where is fleet risk concentrated?

**Answer:** the dashboard groups the latest engine snapshots into CRITICAL, HIGH, WATCH and HEALTHY bands.

**Business value:** management can see whether limited maintenance capacity is being consumed by a small high-risk subset or spread broadly across the fleet.

### 4. What happens when maintenance capacity is constrained?

**Answer:** the maintenance opportunity mart is designed to rank candidates against an intervention threshold and available capacity.

**Business value:** the same analytical output can support different planning scenarios without changing the underlying telemetry pipeline.

### 5. What should an analyst avoid claiming?

The health score is a **portfolio decision heuristic**, not an aviation-certified prediction model. Financial outputs are scenario estimates based on user-provided assumptions. This distinction keeps the project technically credible.

## 🧮 Analytical model

```text
Health Score =
    0.40 × RUL Risk
  + 0.25 × Degradation Trend
  + 0.20 × Sensor Instability
  + 0.15 × Cycle Age Risk
```

The score is transformed into an operational risk band and then into a recommended action.

| Risk band | Planner action |
|---|---|
| 🔴 CRITICAL | Immediate review |
| 🟠 HIGH | Schedule intervention |
| 🟡 WATCH | Increase monitoring |
| 🟢 HEALTHY | Routine monitoring |

## 📊 Dashboard story

The dashboard is intentionally organized in this order:

**Fleet snapshot → risk concentration → RUL/health relationship → maintenance queue → business questions**

That sequence lets a reviewer move from **"What is happening?"** to **"Where is the problem?"** to **"What should we do?"**.

## 🔬 Reproducibility standard

For a portfolio-quality deployment, displayed KPI values should always be generated from:

`NASA source → ADF → ADLS → PySpark → Gold → dbt → Synapse → dashboard`

Illustrative preview records are explicitly labeled in the application and must not be presented as measured NASA benchmark statistics.

## 💼 Portfolio outcome

The important result is not a fabricated savings percentage. The outcome is a complete analytical data product that demonstrates:

- cloud ingestion and orchestration
- lakehouse storage design
- distributed PySpark processing
- governed SQL transformation with dbt
- warehouse serving through Synapse
- business-oriented KPI design
- maintenance prioritization
- data-quality controls
- decision-focused dashboard storytelling
