# C-MAPSS schema contract

Each telemetry row represents one engine at one operating cycle.

| Field | Type | Meaning |
|---|---|---|
| engine_id | integer | Engine identifier |
| cycle | integer | Operating cycle |
| op_setting_1..3 | double | Operating settings |
| sensor_1..21 | double | Sensor measurements |
| rul | integer | Derived remaining useful life |

The source files are space-delimited and do not contain a header. Parsing should be parameterized by dataset (`FD001`–`FD004`).
