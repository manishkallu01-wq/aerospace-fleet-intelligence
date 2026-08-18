# 📊 Business Insights & Decision Framework

## Why this project matters

Aerospace telemetry has value only when it can be converted into a repeatable decision workflow. This project turns engine-cycle observations into an analytical layer that helps a maintenance planner answer **where to look, when to intervene, and how to prioritize limited capacity**.

## 🔎 Insight 1 — prioritize before failure

NASA C-MAPSS FD001 provides run-to-failure training trajectories and test trajectories that stop before failure. That makes **early-warning prioritization** the right business framing for this portfolio project.

**Decision:** rank engines by remaining useful life and health/risk rather than waiting for a failure event.

## ⏱️ Insight 2 — RUL is a planning measure

RUL is represented in operating cycles. It gives the business a common planning scale across engines while the detailed Silver layer retains the underlying engine × cycle telemetry.

**Decision:** use RUL bands to support maintenance scheduling and escalation, while avoiding claims that a portfolio heuristic is a certified maintenance prediction.

## 🚦 Insight 3 — convert scores into actions

A score alone is not a business product. The Gold layer maps risk into an explicit action:

| Risk | Decision |
|---|---|
| CRITICAL | Immediate review |
| HIGH | Schedule intervention |
| WATCH | Increase monitoring |
| HEALTHY | Routine monitoring |

**Decision:** create a maintenance queue that can be handed to a planner instead of presenting an unexplained model output.

## 📈 Insight 4 — measure capacity pressure

Maintenance capacity is finite. The dashboard therefore supports scenario assumptions for intervention thresholds and available capacity.

Example question:

> **If the maintenance team can handle only N engines in the next planning window, which engines enter the queue first?**

The answer should be generated from Gold/Synapse data rather than manually selected records.

## 💰 Insight 5 — keep economics explicit

The project supports scenario variables for planned maintenance cost, unplanned failure cost and downtime cost. These are **user-provided assumptions**, not claimed aerospace financial benchmarks.

This makes the analytics useful for portfolio discussion without fabricating a dollar-saving result.

## 🎯 Interview takeaway

The strongest story is:

> **I built a cloud data platform that ingests aerospace telemetry, processes it at scale with PySpark, models tested business marts with dbt, serves them through Synapse, and converts engine-health data into an actionable maintenance-priority dashboard.**

That demonstrates the complete Data Engineering lifecycle — not just a prediction notebook.
