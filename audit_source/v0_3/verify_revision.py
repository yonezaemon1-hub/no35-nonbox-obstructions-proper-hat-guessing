"""Standard-library checks for new finite relabeling-barrier certificates."""
import hashlib
import itertools
import json
import platform
import zipfile
from pathlib import Path


def main():
    root=Path(__file__).resolve().parent
    original=root/'prior'/'No35_NonBox_Obstructions_Candidate_v0_1_20261024.zip'
    expected='6eb385e1eb1d4d5d7baa467aff8f4a29d2f14e8f78bf036ba84518fe41c4ca05'
    assert hashlib.sha256(original.read_bytes()).hexdigest()==expected
    with zipfile.ZipFile(original) as z:
        for name in ['witness_k3.json','witness_k4.json','verification_results.json']:
            assert z.read(name)==(root/name).read_bytes()
    result={'python':platform.python_version(),'original_zip_sha256':expected,
            'frozen_certificates_and_results_byte_unchanged':True,
            'verifier_output_routing_modified_in_v03':True,'barrier_checks':[]}
    for k in [3,4]:
        cert=json.loads((root/f'witness_k{k}.json').read_text())
        P={tuple(t) for t in cert['tuples']}
        blocks=[range(i*k,i*k+k) for i in range(k)]
        cube=set(itertools.product(*blocks))
        assert cube<=P
        symbols={(i,p[i]) for p in P for i in range(k)}
        edges=set()
        for a,b in itertools.combinations(sorted(symbols),2):
            if a[0]==b[0] or any(p[a[0]]==a[1] and p[b[0]]==b[1] for p in P):
                edges.add((a,b))
        clique={(i,c) for i,block in enumerate(blocks) for c in block}
        assert len(clique)==k*k
        assert all(tuple(sorted(pair)) in edges for pair in itertools.combinations(clique,2))
        assert all(a[1]!=b[1] for a,b in edges)
        assert len(symbols)==k*k+1
        assert len(edges)==(k*k+1)*(k*k)//2-(k-2)
        result['barrier_checks'].append({'k':k,'cube_points':len(cube),
            'symbols':len(symbols),'constraint_edges':len(edges),'clique':len(clique),
            'existing_support':len({c for p in P for c in p})})
    # Independent endpoint control: merging the extra coordinate symbol at k=2.
    raw={(a,b) for a in range(2) for b in range(3)}
    attempt={(a,2+b if b<2 else 1) for a,b in raw}
    improper=sum(a==b for a,b in attempt)
    assert improper==1
    result['unsafe_k2_improper_tuples']=improper
    result['status']='PASS_FINITE_BARRIER_CHECKS_ONLY'
    out=root/'run_outputs'
    out.mkdir(exist_ok=True)
    (out/'revision_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
