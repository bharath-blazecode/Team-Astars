"""Run all backend suites in separate processes, using the selected Python environment."""
import os
from pathlib import Path
import subprocess
import sys

BACKEND = Path(__file__).resolve().parents[1] / "backend"
SUITES = [
    ["-m", "prorio.selftest"],
    ["test_api.py"],
    ["test_db.py"],
    ["test_workspace.py"],
    ["test_insights.py"],
    ["test_collaboration.py"],
    ["test_clario_live.py"],
]


def main():
    failed = []
    for suite in SUITES:
        print(f"\nRunning {' '.join(suite)}", flush=True)
        env = {**os.environ, "NRY_DB": ":memory:", "NRY_NOW": "2026-11-15T12:00:00Z",
               "PYTHONIOENCODING": "utf-8"}
        result = subprocess.run([sys.executable, *suite], cwd=BACKEND, env=env)
        if result.returncode:
            failed.append(" ".join(suite))
    if failed:
        print("\nFailed suites: " + ", ".join(failed), file=sys.stderr)
        return 1
    print(f"\nAll {len(SUITES)} backend suites passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
