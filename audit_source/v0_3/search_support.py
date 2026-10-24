"""Exploratory MILP: a proper 3-tuple Hall obstruction with score <= 41.

Requires numpy/scipy; not part of the standard-library proof verifier.
Solver infeasibility is not an independently checkable exact certificate.
"""
import argparse
import itertools
import json
import platform
import time
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--colours',type=int,required=True,choices=[6,7,8])
    ap.add_argument('--seconds',type=float,default=35)
    ap.add_argument('--minimal-core',action='store_true')
    args=ap.parse_args()
    import numpy as np
    import scipy
    from scipy.optimize import Bounds,LinearConstraint,milp
    from scipy.sparse import coo_matrix
    q=args.colours
    points=list(itertools.permutations(range(q),3))
    slots=[(i,pair) for i in range(3) for pair in itertools.permutations(range(q),2)]
    slot_index={s:len(points)+i for i,s in enumerate(slots)}
    nvar=len(points)+len(slots)
    rows=[];cols=[];data=[];lo=[];hi=[]
    def add(coeff,lower=-np.inf,upper=np.inf):
        r=len(lo)
        for c,value in coeff.items():
            rows.append(r);cols.append(c);data.append(value)
        lo.append(lower);hi.append(upper)
    # Projection flags must contain each selected point's three visible pairs.
    for t,p in enumerate(points):
        for i in range(3):
            j=slot_index[i,p[:i]+p[i+1:]]
            add({t:1,j:-1},upper=0)
    add({i:1 for i in range(len(points))},lower=33,upper=41-q)
    add({**{i:1 for i in range(len(points))},
         **{len(points)+i:-1 for i in range(len(slots))}},lower=1,
         upper=1 if args.minimal_core else np.inf)
    if args.minimal_core:
        # A Hall-inclusion-minimal non-coverable subset has deficiency one,
        # and no occupied visible-input line contains only one point.
        # If a counterexample loses colours on taking this subset, its exact
        # support is handled by a different q-model in the same 6..8 sweep.
        for (axis,pair),flag in slot_index.items():
            coeff={i:-1 for i,p in enumerate(points) if p[:axis]+p[axis+1:]==pair}
            coeff[flag]=2
            add(coeff,upper=0)
    # Exact support q. The three q-models cover every possible score <= 41:
    # existing bounds require >=33 points and >=6 colours.
    for colour in range(q):
        add({i:1 for i,p in enumerate(points) if colour in p},lower=1)
    # Any nonempty proper point set can be globally relabelled to contain 012.
    add({points.index((0,1,2)):1},lower=1,upper=1)
    # WLOG sort the true projection sizes via coordinate permutation, then
    # globally relabel a chosen point back to 012.
    for i in range(2):
        coeff={j:1 for (axis,pair),j in slot_index.items() if axis==i}
        coeff.update({j:-1 for (axis,pair),j in slot_index.items() if axis==i+1})
        add(coeff,upper=0)
    # Sort frequencies only among the unfixed colour names 3,...,q-1.
    for a in range(3,q-1):
        add({i:int(a in p)-int(a+1 in p) for i,p in enumerate(points)
             if (a in p)!=(a+1 in p)},lower=0)
    matrix=coo_matrix((np.array(data,dtype=float),(rows,cols)),
                      shape=(len(lo),nvar)).tocsc()
    objective=np.r_[np.ones(len(points)),np.zeros(len(slots))]
    start=time.monotonic()
    res=milp(objective,integrality=np.ones(nvar),bounds=Bounds(0,1),
             constraints=LinearConstraint(matrix,np.array(lo),np.array(hi)),
             options={'time_limit':args.seconds,'mip_rel_gap':0.0})
    result={'colours':q,'point_cap':41-q,'tuple_variables':len(points),
            'minimal_hall_core_conditions':args.minimal_core,
            'projection_flags':len(slots),'constraints':len(lo),
            'python':platform.python_version(),'scipy':scipy.__version__,
            'status_code':int(res.status),'message':str(res.message),
            'seconds':time.monotonic()-start,
            'exact_unsat_certificate':False,'global_C3_decided':False}
    for key in ['mip_node_count','mip_gap','mip_dual_bound','fun']:
        value=getattr(res,key,None)
        if value is not None:
            result[key]=float(value)
    if res.x is not None:
        P={p for i,p in enumerate(points) if res.x[i]>.5}
        projected=[{p[:i]+p[i+1:] for p in P} for i in range(3)]
        support=set().union(*(set(p) for p in P)) if P else set()
        valid=(all(len(set(p))==3 for p in P) and len(support)==q
               and 33<=len(P)<=41-q and len(P)>sum(map(len,projected)))
        result['incumbent_validated_in_exact_integer_arithmetic']=valid
        if valid:
            result['witness']={'tuples':sorted(P),'points':len(P),
                'support':len(support),'projection_sizes':list(map(len,projected)),
                'score':len(P)+len(support)}
    suffix='_core' if args.minimal_core else ''
    path=Path(__file__).resolve().parent/f'support_search_q{q}{suffix}.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
