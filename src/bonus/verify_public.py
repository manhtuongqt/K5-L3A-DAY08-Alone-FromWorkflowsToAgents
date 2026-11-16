"""Verify public gates without changing host, evaluator, config or fixture data.

Run from src/: python -m bonus.verify_public
This is a technical evidence generator, not the instructor's hidden grader.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone


def main():
    root = Path(__file__).resolve().parents[1]
    repo = root.parent
    checks = []
    commands = [
        ["-m", "lab8.smoke"],
        ["-m", "pytest", "-q"],
        ["-m", "pytest", "-q", "-m", "student", "-o", "addopts="],
        ["-m", "lab8.crash_test", "--count", "20", "--out", "reports/crash.json"],
        ["-m", "lab8.benchmark", "--shapes", "workflow,single,orchestrator,swarm",
         "--cases", "data/public_claims.jsonl", "--seeds", "11,22,33,44,55",
         "--out", "reports/benchmark_reproduced.json"],
    ]
    for args in commands:
        proc = subprocess.run([sys.executable, "-X", "utf8", *args], cwd=root,
                              capture_output=True, text=True, encoding="utf-8")
        entry = {"command": "python " + " ".join(args), "passed": proc.returncode == 0,
                 "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        checks.append(entry)
        print(entry["command"], "PASS" if entry["passed"] else "FAIL", flush=True)
    original = json.loads((root / "reports/benchmark.json").read_text(encoding="utf-8"))
    repeat = json.loads((root / "reports/benchmark_reproduced.json").read_text(encoding="utf-8"))
    checks.append({"name": "whole_public_benchmark_reproduces", "passed": original == repeat,
                   "scope": "controlled variables, all 280 trials, summaries; not just rounded rates"})
    paths = [*sorted((root / "lab8").glob("*.py")), *sorted((root / "config").glob("*")),
             *sorted((root / "data").glob("*")), root / "lab8/shapes/swarm_reference.py",
             root / "lab8/shapes/common.py", root / "lab8/shapes/__init__.py"]
    protected = []
    for path in paths:
        if not path.is_file():
            continue
        rel = path.relative_to(repo).as_posix()
        expected = subprocess.run(["git", "rev-parse", "upstream/main:" + rel], cwd=repo,
                                  capture_output=True, text=True, check=True).stdout.strip()
        actual = subprocess.run(["git", "hash-object", "--path=" + rel, rel], cwd=repo,
                                capture_output=True, text=True, check=True).stdout.strip()
        protected.append({"path": rel, "unchanged": actual == expected, "blob": actual})
    checks.append({"name": "official_host_and_measurement_files_unchanged",
                   "passed": all(p["unchanged"] for p in protected), "files": protected})
    artifacts = {}
    for name in ("benchmark.json", "crash.json", "research_ablation.json"):
        artifacts[name] = hashlib.sha256((root / "reports" / name).read_bytes()).hexdigest()
    record = {"checked_at": datetime.now(timezone.utc).isoformat(),
              "scope": "Basic public gates; B4 verified separately in bonus_verification.json",
              "python": platform.python_version(), "platform": platform.platform(),
              "checks": checks, "passed": all(c["passed"] for c in checks),
              "artifact_sha256": artifacts,
              "hidden_gate": "NOT EVALUATED: official instructor grader and hidden labels unavailable",
              "bonus_points_claimed": False}
    (root / "reports/verification.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Public verification:", record["passed"], flush=True)
    return 0 if record["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
