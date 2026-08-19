"""Validate structural, syntax, configuration, and documentation contracts."""
from pathlib import Path
import ast, json, sys

ROOT=Path(__file__).resolve().parents[1]
required=["README.md","src/aerospace_analytics.py","scripts/build_fd001_results.py","tests/test_health_model.py","reports/fd001_engine_rul.csv","adf/pipelines/pl_aerospace_ingestion.json","dbt/dbt_project.yml","synapse/01_tables.sql"]
errors=[f"missing: {p}" for p in required if not (ROOT/p).is_file()]
for path in list((ROOT/"src").glob("*.py"))+list((ROOT/"scripts").glob("*.py"))+list((ROOT/"dashboard").glob("*.py")):
    try: ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
    except SyntaxError as exc: errors.append(f"{path.relative_to(ROOT)}: {exc}")
for path in (ROOT/"adf").rglob("*.json"):
    try: json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"{path.relative_to(ROOT)}: {exc}")
readme=(ROOT/"README.md").read_text(encoding="utf-8")
for link in ["assets/architecture.svg","docs/project_story.md","docs/runbook.md","reports/fd001_engine_rul.csv"]:
    if link not in readme: errors.append(f"README missing link: {link}")
if errors:
    print("\n".join(f"ERROR {e}" for e in errors)); sys.exit(1)
print("PASS aerospace project structure, syntax, JSON, and evidence links")
