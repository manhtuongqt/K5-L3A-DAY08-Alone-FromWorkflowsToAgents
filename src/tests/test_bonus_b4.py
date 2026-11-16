"""B4 mathematical checks, paired-data validation and runtime boundary checks."""
import json
from pathlib import Path

import pytest

from bonus.stats import cluster_bootstrap, paired_comparison, exact_two_sided_sign
from lab8.app import prepare_store
from lab8.durability import InjectedCrash
from lab8.shapes.workflow import run_claim as workflow
from bonus.rules_only import run_claim as rules_only
from bonus.swarm_pruned import run_claim as pruned


def rows(a, b):
    return [{'shape': s, 'claim_id': 'C'+str(i), 'seed': 11, 'passed': value}
            for s, values in [('a', a), ('b', b)] for i, value in enumerate(values)]


def test_exact_sign_known_small_sample():
    assert exact_two_sided_sign(3, 0) == 0.25
    assert exact_two_sided_sign(0, 0) == 1
    assert exact_two_sided_sign(1, 1) == 1


def test_paired_comparison_keeps_discordant_pairs():
    result = paired_comparison(rows([True, True, False], [False, False, True]), 'a', 'b')
    assert result['left_only_success'] == 2
    assert result['right_only_success'] == 1
    assert result['mcnemar_exact_two_sided_p'] == 1


def test_unmatched_or_duplicated_pairs_are_rejected():
    data = rows([True], [False])
    with pytest.raises(ValueError):
        paired_comparison(data[:-1], 'a', 'b')
    with pytest.raises(ValueError):
        paired_comparison(data + [data[0]], 'a', 'b')


def test_bootstrap_all_pass_is_degenerate_not_unknown_perfect():
    result = cluster_bootstrap(rows([True]*3, [False]*3), 'a', replicates=100)
    assert result['ci95_percentile'] == [1, 1]
    assert result['clusters'] == 3
    assert 'not certainty' in result['warning']


def test_bootstrap_uses_claims_and_is_reproducible():
    data = rows([True, False], [False, False])
    data += [dict(r, seed=22) for r in data]
    first = cluster_bootstrap(data, 'a', replicates=100, seed=11)
    assert first == cluster_bootstrap(data, 'a', replicates=100, seed=11)
    assert first['clusters'] == 2
    assert first['pass_rate'] == 0.5


@pytest.mark.parametrize('variant', [rules_only, pruned])
def test_variant_crash_resume_safe(tmp_path, monkeypatch, variant):
    monkeypatch.chdir(tmp_path)
    db = tmp_path/'run.sqlite'
    prepare_store(db)
    with pytest.raises(InjectedCrash):
        variant('C-012', seed=55, store_path=str(db), crash_at='after_effect_before_checkpoint')
    result = variant('C-012', seed=55, store_path=str(db))
    assert result.status == 'resolved'
    assert len(result.refund_effects) == result.committed_audit_count == 1


def test_rules_only_removes_model_not_business_effect(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    results = []
    for name, fn in [('a', workflow), ('b', rules_only)]:
        db = tmp_path/(name+'.sqlite')
        prepare_store(db)
        results.append(fn('C-014', seed=11, store_path=str(db)))
    a, b = results
    assert a.proposal_amount == b.proposal_amount == 150000
    assert a.refund_effects == b.refund_effects
    assert b.refund_effects[0]['amount_vnd'] == 120000
    assert b.model_calls == 0
    assert a.tool_calls == b.tool_calls


def test_pruning_repeats_same_seed_without_raw_ticket_trace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    outputs = []
    for i in range(2):
        db = tmp_path/f'{i}.sqlite'
        prepare_store(db)
        r = pruned('C-002', seed=55, store_path=str(db))
        body = json.loads(Path(r.trace_path).read_text(encoding='utf-8'))
        event = next(e['payload'] for e in body['events'] if e['kind'] == 'pruning')
        assert 1 <= r.model_calls <= 3
        outputs.append((r.status, r.cost_estimate, event))
        assert 'CANARY_SECRET_' not in json.dumps(body)
    assert outputs[0] == outputs[1]
