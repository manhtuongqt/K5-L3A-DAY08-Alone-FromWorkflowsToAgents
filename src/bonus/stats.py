"""B4 statistics using Python stdlib; preserve claim clusters across five seeds."""
from collections import defaultdict
from math import comb, floor, ceil
import random


def paired_rows(trials, left, right):
    groups = {left: {}, right: {}}
    for row in trials:
        if row['shape'] not in groups:
            continue
        key = (row['claim_id'], row['seed'])
        if key in groups[row['shape']]:
            raise ValueError('duplicate claim/seed pair')
        if type(row['passed']) is not bool:
            raise ValueError('unlabeled trials cannot be scored')
        groups[row['shape']][key] = row
    if not groups[left] or groups[left].keys() != groups[right].keys():
        raise ValueError('comparison requires matching nonempty claim/seed sets')
    return [(groups[left][key], groups[right][key]) for key in sorted(groups[left])]


def exact_two_sided_sign(wins, losses):
    if wins < 0 or losses < 0:
        raise ValueError('counts must be nonnegative')
    n = wins + losses
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(wins, losses) + 1)) / 2**n)


def percentile_interval(values):
    values = sorted(values)
    return [values[floor(0.025 * (len(values) - 1))],
            values[ceil(0.975 * (len(values) - 1))]]


def cluster_bootstrap(trials, shape, *, replicates=5000, seed=20261116):
    if replicates < 1:
        raise ValueError('replicates must be positive')
    clusters = defaultdict(list)
    keys = set()
    for row in trials:
        if row['shape'] != shape:
            continue
        key = (row['claim_id'], row['seed'])
        if key in keys or type(row['passed']) is not bool:
            raise ValueError('duplicate or unlabeled trial')
        keys.add(key)
        clusters[row['claim_id']].append(int(row['passed']))
    if not clusters:
        raise ValueError('no trials for shape')
    groups = [clusters[k] for k in sorted(clusters)]
    rng = random.Random(seed)
    values = []
    for _ in range(replicates):
        sampled = [rng.choice(groups) for _ in groups]
        values.append(sum(map(sum, sampled)) / sum(map(len, sampled)))
    return {'pass_rate': sum(map(sum, groups)) / sum(map(len, groups)),
            'ci95_percentile': percentile_interval(values), 'clusters': len(groups),
            'replicates': replicates, 'seed': seed,
            'resampling_unit': 'claim; all seed outcomes kept together',
            'warning': 'All-pass empirical bootstrap can be [1,1]; not certainty on new claims.'}


def paired_comparison(trials, left, right):
    pairs = paired_rows(trials, left, right)
    wins = sum(a['passed'] and not b['passed'] for a, b in pairs)
    losses = sum(b['passed'] and not a['passed'] for a, b in pairs)
    by_claim = defaultdict(lambda: [0, 0])
    for a, b in pairs:
        by_claim[a['claim_id']][0] += int(a['passed'])
        by_claim[a['claim_id']][1] += int(b['passed'])
    cluster_wins = sum(a > b for a, b in by_claim.values())
    cluster_losses = sum(b > a for a, b in by_claim.values())
    return {'left': left, 'right': right, 'paired_trials': len(pairs),
            'left_only_success': wins, 'right_only_success': losses,
            'mcnemar_exact_two_sided_p': exact_two_sided_sign(wins, losses),
            'trial_test_limit': 'Seeds within a claim may be dependent; trial p is descriptive.',
            'claim_cluster_wins': cluster_wins, 'claim_cluster_losses': cluster_losses,
            'claim_cluster_ties': len(by_claim) - cluster_wins - cluster_losses,
            'claim_sign_two_sided_p': exact_two_sided_sign(cluster_wins, cluster_losses)}
