"""Exploratory CEGIS for B_{2,5}, q=8. Restricted XOR-translation class.

This is a search tool, not an UNSAT certificate for arbitrary strategies.
Standard library verifier; python-sat required only for synthesis.
"""
import argparse
import itertools
import json
import platform
import threading
import time
from pathlib import Path

EDGES = [(x, y) for x in range(8) for y in range(8) if x != y]
ALL = (1 << len(EDGES)) - 1
LEGAL_MASK = [sum(1 << i for i, (x, y) in enumerate(EDGES)
                  if z not in (x, y)) for z in range(8)]


def mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return c


def bad_component(mask):
    """Return an edge set with |edges|>|incident row/column vertices|."""
    parent = list(range(16))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    es = []
    while mask:
        bit = mask & -mask
        i = bit.bit_length() - 1
        mask ^= bit
        x, y = EDGES[i]
        a, b = find(x), find(8 + y)
        if a != b:
            parent[a] = b
        es.append(i)
    groups = {}
    for i in es:
        groups.setdefault(find(EDGES[i][0]), []).append(i)
    for group in groups.values():
        vertices = {v for i in group for v in (EDGES[i][0], 8 + EDGES[i][1])}
        if len(group) > len(vertices):
            # Strip leaves without changing the excess; yields a smaller clause.
            group = set(group)
            while True:
                degree = {}
                for i in group:
                    x, y = EDGES[i]
                    degree[x] = degree.get(x, 0) + 1
                    degree[8+y] = degree.get(8+y, 0) + 1
                leaves = {v for v, d in degree.items() if d == 1}
                if not leaves:
                    break
                group = {i for i in group if EDGES[i][0] not in leaves
                         and 8+EDGES[i][1] not in leaves}
            return sorted(group)
    return None


def check(h, collect=True):
    n = len(h)
    masks = [[LEGAL_MASK[z] for z in range(8)] for _ in range(n)]
    for j in range(n):
        for i, (x, y) in enumerate(EDGES):
            g = x ^ h[j][x ^ y]
            assert g not in (x, y)
            masks[j][g] &= ~(1 << i)
    bad = []
    # XOR-translation equivariance makes z[0]=0 representatives complete.
    for tail in itertools.product(range(8), repeat=n-1):
        z = (0,) + tail
        mask = ALL
        for j, value in enumerate(z):
            mask &= masks[j][value]
        component = bad_component(mask)
        if component:
            bad.append((z, component))
            if not collect:
                return bad
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=150)
    ap.add_argument('--max-iterations', type=int, default=10000)
    ap.add_argument('--output', default='translation_result.json')
    args = ap.parse_args()
    from pysat.solvers import Solver
    t0 = time.monotonic()
    result = {'scope': 'g_j(x,y)=x XOR h_j(x XOR y), q=8, n=5', 'solver':'glucose4',
              'arbitrary_strategies_decided': False, 'python': platform.python_version()}
    baseline = [[0] + [mul(a, d) for d in range(1, 8)] for a in range(2, 8)]
    controls = [len(check(baseline[:i] + baseline[i+1:])) * 8 for i in range(6)]
    assert controls == [224]*6, controls
    result['known_affine_five_page_failure_counts'] = controls
    print('Known-control check: six affine omissions each fail on 224/32768 vectors.', flush=True)
    variables = {}
    for j in range(5):
        for d in range(1, 8):
            for v in range(1, 8):
                if v != d:
                    variables[j,d,v] = len(variables)+1
    clauses = []
    for j in range(5):
        for d in range(1, 8):
            vs = [variables[j,d,v] for v in range(1,8) if v != d]
            clauses.append(vs)
            clauses.extend([-a,-b] for a,b in itertools.combinations(vs,2))
    # WLOG within this class: page permutation sorts h_j(1).
    for j in range(4):
        for a in range(2,8):
            for b in range(2,a):
                clauses.append([-variables[j,1,a],-variables[j+1,1,b]])
    # A global invertible binary linear relabelling fixing 1 sends the minimum
    # first-page value to 2; then reordering the pages restores the sort.
    # This second normalization is not used: avoid interactions with the order.
    seen = set()
    status = 'UNKNOWN_LIMIT'
    total_bad = 0
    with Solver(name='glucose4', bootstrap_with=clauses) as solver:
        timer = threading.Timer(args.seconds, solver.interrupt)
        timer.daemon = True
        timer.start()
        try:
            for iteration in range(args.max_iterations):
                if time.monotonic()-t0 > args.seconds:
                    break
                sat = solver.solve_limited(expect_interrupt=True)
                if sat is None:
                    break
                if not sat:
                    status = 'UNSAT_RESTRICTED_CLASS_SOLVER_REPORT'
                    break
                positives = {v for v in solver.get_model() if v > 0}
                h = [[0]*8 for _ in range(5)]
                for (j,d,v), number in variables.items():
                    if number in positives:
                        h[j][d] = v
                bad = check(h)
                total_bad += len(bad)
                if not bad:
                    status = 'SAT_CONSTRUCTION_CANDIDATE'
                    result['h'] = h
                    break
                added = 0
                for z, component in bad:
                    clause = tuple(sorted({variables[j, x ^ y, x ^ z[j]]
                                           for i in component for x,y in [EDGES[i]]
                                           for j in range(5)}))
                    if clause not in seen:
                        seen.add(clause)
                        solver.add_clause(list(clause))
                        added += 1
                assert added, 'Counterexample should exclude the current model.'
                if iteration % 10 == 0:
                    print(json.dumps({'iteration':iteration,'bad_orbits':len(bad),
                                      'new_clauses':added,'clauses':len(seen),
                                      'seconds':round(time.monotonic()-t0,3)}), flush=True)
            result.update(status=status, iterations=iteration+1,
                          counterexample_clauses=len(seen), bad_orbits_processed=total_bad,
                          solver_stats=solver.accum_stats())
        finally:
            timer.cancel()
    result['seconds'] = time.monotonic()-t0
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
