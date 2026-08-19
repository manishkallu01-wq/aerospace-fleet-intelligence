# FD001 Data Dictionary

NASA C-MAPSS FD001 rows contain **26 numeric columns**: engine identifier, cycle, three operating settings, and 21 sensor measurements.

| Field | Meaning | Engineering interpretation |
|---|---|---|
| `engine_id` | Unit number | Engine trajectory identifier |
| `cycle` | Time in cycles | Operating age of the simulated engine |
| `op_setting_1` | Operational setting 1 | Flight/operating-condition variable |
| `op_setting_2` | Operational setting 2 | Flight/operating-condition variable |
| `op_setting_3` | Operational setting 3 | Flight/operating-condition variable |
| `sensor_1` | T2 | Total temperature at fan inlet |
| `sensor_2` | T24 | Total temperature at LPC outlet |
| `sensor_3` | T30 | Total temperature at HPC outlet |
| `sensor_4` | T50 | Total temperature at LPT outlet |
| `sensor_5` | P2 | Pressure at fan inlet |
| `sensor_6` | P15 | Total pressure in bypass duct |
| `sensor_7` | P30 | Total pressure at HPC outlet |
| `sensor_8` | Nf | Physical fan speed |
| `sensor_9` | Nc | Physical core speed |
| `sensor_10` | EPR | Engine pressure ratio |
| `sensor_11` | Ps30 | Static pressure at HPC outlet |
| `sensor_12` | Phi | Fuel-flow-to-Ps30 ratio |
| `sensor_13` | NRf | Corrected fan speed |
| `sensor_14` | NRc | Corrected core speed |
| `sensor_15` | BPR | Bypass ratio |
| `sensor_16` | farB | Burner fuel-air ratio |
| `sensor_17` | htBleed | Bleed enthalpy |
| `sensor_18` | Nf_dmd | Demanded fan speed |
| `sensor_19` | PCNfR_dmd | Demanded corrected fan speed |
| `sensor_20` | W31 | HPT coolant bleed |
| `sensor_21` | W32 | LPT coolant bleed |

## RUL semantics

- **Training:** RUL can be derived as `failure_cycle - current_cycle` because training trajectories reach simulated failure.
- **Test:** the supplied true-RUL vector is held out for evaluation. It must not be joined into a prospective prediction feature set.

## Source

NASA C-MAPSS Jet Engine Simulated Data: https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data
