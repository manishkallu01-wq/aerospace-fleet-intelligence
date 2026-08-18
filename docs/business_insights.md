# 📊 Business Insights & Decision Framework

## Why this project matters

Aerospace telemetry has value only when it can be converted into a repeatable decision workflow. This project demonstrates the engineering path from engine-cycle observations to an analytical maintenance-prioritization layer.

## 🔎 Insight 1 — prioritize before failure

NASA C-MAPSS FD001 contains run-to-failure training trajectories and truncated test trajectories. The benchmark's true RUL vector exists for **evaluation**, not as information available to an operator before failure.

**Decision framing:** evaluate a prospective RUL model against the ground truth, then use the model's prediction—not the future label—to rank engines operationally.

## ⏱️ Insight 2 — RUL is a planning measure

RUL is expressed in operating cycles. In the committed FD001 evidence, the mean is **75.52 cycles**, the median is **86**, and the observed range is **7–145 cycles**.

**Decision:** do not use the mean alone. The lower tail contains the engines that would require the earliest attention.

## 🚦 Insight 3 — transparent evaluation bands

For the benchmark report, the project uses simple thresholds to turn the ground-truth evaluation vector into an explainable planning view:

| RUL | Band | Decision framing |
|---:|---|---|
| ≤30 | 🔴 CRITICAL | Immediate review |
| 31–60 | 🟠 HIGH | Schedule intervention |
| 61–90 | 🟡 WATCH | Increase monitoring |
| >90 | 🟢 HEALTHY | Routine monitoring |

These thresholds are **portfolio analysis conventions**, not aviation maintenance limits.

## 🔧 Insight 4 — analytics must become an action

A useful engineering product should expose a ranked maintenance queue, not just a model score. The dbt and Synapse layers therefore provide a queue-shaped analytical contract.

For the executed FD001 evidence, **39 of 100 engines (39%)** are at or below 60 cycles and **25 (25%)** are at or below 30 cycles.

## 📈 Insight 5 — separate benchmark truth from prospective prediction

The repository intentionally has two analytical states:

1. **Evaluation:** true RUL labels are used to measure and inspect benchmark behavior.
2. **Prospective production design:** a separately trained/evaluated RUL model supplies predictions from data available at decision time.

Keeping those states separate prevents target leakage and makes the portfolio more credible.

## 💰 Insight 6 — keep economics explicit

Maintenance cost, downtime cost and intervention capacity are scenario inputs. The repository does **not** claim fabricated dollar savings from simulated data.

## 🎯 Interview takeaway

> **I built the data-platform design and executed the benchmark evidence layer end-to-end, then separated evaluation truth from the prospective production architecture so future RUL labels are never presented as operationally available information.**

That distinction demonstrates data engineering maturity as well as analytics awareness.
