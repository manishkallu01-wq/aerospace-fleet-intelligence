"""Build the engine-level FD001 result file used by the dashboard."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.aerospace_analytics import build_evaluation_table, load_fd001_rul

INPUT = ROOT / "data" / "reference" / "RUL_FD001.txt"
OUTPUT = ROOT / "reports" / "fd001_engine_rul.csv"


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(
            "Missing data/reference/RUL_FD001.txt."
        )

    rul = load_fd001_rul(INPUT)
    result = build_evaluation_table(rul)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)

    print(f"Wrote {len(result)} engine results to {OUTPUT}")
    print(f"Mean RUL: {result['true_rul_cycles'].mean():.2f} cycles")
    print(f"Maintenance queue (<=60): {(result['true_rul_cycles'] <= 60).sum()} engines")


if __name__ == "__main__":
    main()
