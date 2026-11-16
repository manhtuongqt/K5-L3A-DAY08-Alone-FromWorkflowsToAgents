"""Reproduce B4 and write actual test, byte-replay and unchanged-host evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    before = {p: sha(p) for p in ['reports/bonus_ablation.json', 'reports/bonus_benchmark.json']}
    steps = []
    for args in [['-m', 'pytest', '-q', 'tests/test_bonus_b4.py'], ['-m', 'bonus.run_b4']]:
        result = subprocess.run([sys.executable, '-X', 'utf8', *args], capture_output=True,
                                text=True, encoding='utf-8')
        steps.append({'command': 'python ' + ' '.join(args), 'returncode': result.returncode,
                      'stdout': result.stdout, 'stderr': result.stderr})
    after = {p: sha(p) for p in before}
    report = json.loads(Path('reports/bonus_ablation.json').read_text(encoding='utf-8'))
    public = json.loads(Path('reports/verification.json').read_text(encoding='utf-8'))
    safety_ok = all(v == 0 for counters in report['safety']['by_shape'].values()
                    for k, v in counters.items() if k != 'trials')
    checks = {'bonus_commands_pass': all(s['returncode'] == 0 for s in steps),
              'whole_bonus_json_replays_byte_identically': before == after,
              'basic_public_verification_passes': public['passed'],
              'public_safety_counts_zero': safety_ok,
              'basic_baselines_match': all(report['basic_baseline_matches'].values())}
    record = {'topic': 'B4', 'steps': steps, 'checks': checks, 'passed': all(checks.values()),
              'artifact_sha256': after,
              'hidden_gate': 'Not evaluated; instructor must confirm >=0.80 and must-pass gates.'}
    Path('reports/bonus_verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(checks))
    return 0 if record['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
