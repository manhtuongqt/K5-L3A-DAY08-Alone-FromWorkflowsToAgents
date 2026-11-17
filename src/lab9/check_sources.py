"""Check immutable source boundaries, submission artifacts and common secret patterns."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess

SRC = Path(__file__).resolve().parents[1]
ROOT = SRC.parent
BASE = "cf413f3fff56015b2f16833989e5f1e9726fba26"


def digest(data):
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def main():
    lock = json.loads((SRC / "config/day09_source_lock.json").read_text(encoding="utf-8"))
    errors = []
    for relative, expected in lock["protected_starter_files"].items():
        p = ROOT / relative
        if not p.is_file() or digest(p.read_bytes()) != expected:
            errors.append("changed starter source: " + relative)
    protected = subprocess.run(["git", "diff", "--name-only", BASE, "--", "src/lab8",
                               "README.md", "CHECKPOINTS.md", "RUBRIC.md", "SUBMISSION.md", ".gitignore",
                               ".github/workflows/ci.yml"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    if protected:
        errors.append("changed Day08 protected paths: " + protected)
    names = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    forbidden = [x for x in names if any(s in x.split("/") for s in (".venv", ".env", "traces", "student_drop"))
                 or x.endswith((".sqlite", ".key", ".pem")) or x.startswith("src/eval/instructor/")]
    if forbidden:
        errors.append("tracked private/runtime paths: " + repr(forbidden))
    patterns = [rb"sk-(?:proj-)?[A-Za-z0-9_-]{24,}", rb"gh[pousr]_[A-Za-z0-9]{20,}",
                rb"AIza[0-9A-Za-z_-]{30,}", rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
    introduced = subprocess.run(["git", "diff", "--name-only", BASE], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.splitlines()
    for name in introduced:
        p = ROOT / name
        if p.is_file() and any(re.search(pattern, p.read_bytes()) for pattern in patterns):
            errors.append("possible credential: " + name)
    for version in ("v1", "v2"):
        path = SRC / f"data/eval/eval_set_{version}.jsonl"
        report = SRC / f"reports/baseline_{version}.json"
        if path.is_file() and report.is_file():
            expected = json.loads(report.read_text(encoding="utf-8"))["manifest"]["eval_set_sha"]
            if hashlib.sha256(path.read_bytes()).hexdigest()[:12] != expected:
                errors.append("baseline eval-set SHA mismatch: " + version)
    summary = {"protected_starter_files": len(lock["protected_starter_files"]),
               "day08_base": BASE, "changed_paths_scanned": len(introduced),
               "tracked_paths_scanned": len(names), "errors": errors,
               "scope": "source boundary and common credential patterns; not a proof of no vulnerabilities"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
