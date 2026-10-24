"""No.35 candidate: count proper obstructions; Python standard library only.

The recursion of uncoloured point sets is the known construction of
He, Ido and Przybocki (2022), not a new claim of this candidate.
The candidate step is the support-preserving proper recolouring for k>=3.
"""
import itertools
import json
import platform
from fractions import Fraction
from pathlib import Path


def uncoloured(k):
    if k == 1:
        return {(0,), (1,)}
    return set(itertools.product(range(k), repeat=k)) | {
        p + (k,) for p in uncoloured(k-1)}


def colour(k, point, safe=True):
    return tuple((k-1 if safe else 1) if i == k-1 and value == k
                 else i*k+value for i,value in enumerate(point))


def projections(points, k):
    return [{p[:i]+p[i+1:] for p in points} for i in range(k)]


def maximum_matching(points, k):
    """Independent check: assign each tuple to one distinct visible-input slot."""
    points = sorted(points)
    adjacent = [[(i,p[:i]+p[i+1:]) for i in range(k)] for p in points]
    matched = {}
    def augment(row, seen):
        for slot in adjacent[row]:
            if slot in seen:
                continue
            seen.add(slot)
            if slot not in matched or augment(matched[slot], seen):
                matched[slot] = row
                return True
        return False
    return sum(augment(row,set()) for row in range(len(points)))


def best_box(k):
    """Exact finite search of integer sides, using a current objective cap."""
    best = (k+1)**k + k*(k+1)
    best_sides = (k+1,)*k
    visited = 0
    def visit(sides, prod, total, reciprocal, first):
        nonlocal best,best_sides,visited
        remaining = k-len(sides)
        if remaining == 1:
            if reciprocal >= 1:
                return
            threshold = 1/(1-reciprocal)
            last = max(first,threshold.numerator//threshold.denominator+1)
            value = prod*last+total+last
            visited += 1
            if value < best:
                best,best_sides = value,sides+(last,)
            return
        side = first
        while prod*side**remaining + total + remaining*side < best:
            r = reciprocal+Fraction(1,side)
            if r < 1:
                visit(sides+(side,),prod*side,total+side,r,side)
            side += 1
    visit((),1,0,Fraction(0),2)
    assert sum(Fraction(1,x) for x in best_sides) < 1
    return {'k':k,'sides':best_sides,'bound':best,'last_coordinate_trials':visited}


def main():
    out = Path(__file__).resolve().parent / "run_outputs"
    out.mkdir(exist_ok=True)
    results = {'python':platform.python_version(), 'platform':platform.platform(),
               'scope':'finite checks supplement the all-k induction in PROOF.md',
               'rows':[],'matching':[],'negative_controls':{}}
    for k in range(2,7):
        raw = uncoloured(k)
        expected = 1+sum(i**i for i in range(1,k+1))
        assert len(raw) == expected
        raw_sizes = list(map(len,projections(raw,k)))
        assert sum(raw_sizes) == expected-1
        if k == 2:
            results['known_uncoloured_base'] = {
                'size':len(raw),'projection_sizes':raw_sizes,
                'claimed_new':False}
            continue
        points = {colour(k,p) for p in raw}
        assert len(points) == len(raw)
        assert all(len(set(p)) == k for p in points)
        support = set().union(*(set(p) for p in points))
        assert support == set(range(k*k))
        sizes = list(map(len,projections(points,k)))
        assert sizes == raw_sizes
        assert len(points)-sum(sizes) == 1
        results['rows'].append({'k':k,'points':len(points),'support':len(support),
                                'projection_sizes':sizes,'projection_sum':sum(sizes),
                                'hall_deficiency':1,'upper_bound':len(points)+len(support)})
        if k <= 4:
            matching = maximum_matching(points,k)
            assert matching == len(points)-1
            results['matching'].append({'k':k,'points':len(points),'maximum_matching':matching})
            (out/f'witness_k{k}.json').write_text(json.dumps({
                'k':k,'tuples':sorted(points),'projection_sizes':sizes,
                'support_size':len(support),'upper_bound':len(points)+len(support)
            },indent=2)+'\n',encoding='utf-8')
        print(json.dumps(results['rows'][-1]), flush=True)
    p3 = {colour(3,p) for p in uncoloured(3)}
    deletion_checks = [maximum_matching(p3-{p},3)==len(p3)-1 for p in p3]
    assert all(deletion_checks)
    unsafe = {colour(3,p,safe=False) for p in uncoloured(3)}
    improper = sum(len(set(p)) != 3 for p in unsafe)
    assert improper == 3
    results['negative_controls'] = {
        'all_33_single_point_deletions_become_coverable':all(deletion_checks),
        'unsafe_colour_merge_improper_tuple_count':improper}
    results['box_optima'] = [best_box(k) for k in range(2,7)]
    expected_boxes = {2:11,3:46,4:317,5:3526}
    for entry in results['box_optima']:
        if entry['k'] in expected_boxes:
            assert entry['bound'] == expected_boxes[entry['k']]
    results['status'] = 'PASS_FINITE_CHECKS_NOT_NOVELTY_OR_EXTERNAL_AUDIT'
    (out/'verification_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results['negative_controls']), flush=True)
    print('PASS: construction counts, properness, support, matching and negative controls.')


if __name__ == '__main__':
    main()
