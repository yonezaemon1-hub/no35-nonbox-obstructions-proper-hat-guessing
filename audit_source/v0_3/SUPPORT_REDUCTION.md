# Support reduction after the v0.1 audit

Working extension, 2026-10-24. The following lemma and the new search were added **after** the received audit. They have not been independently audited. The upper bounds 42 / 305 / 3439 remain unchanged unless a separately verified new witness is recorded.

## 1. A sharp barrier for the existing relabeling family

Fix k>=3. Any coordinatewise injective relabeling of the existing S_k that makes every tuple proper uses at least k^2 colors. The v0.1 construction attains this number, so color support is already minimal **within this relabeling family**.

Proof. S_k contains the full cube {0,...,k-1}^k. Let A_i be the image of the k symbols in coordinate i of that cube. Injectivity gives |A_i|=k. Every symbol of coordinate i co-occurs in a tuple of the cube with every symbol of coordinate j. Properness therefore requires A_i and A_j to be disjoint for i!=j. Their union has k^2 elements. The explicit v0.1 relabeling uses exactly those k^2 colors. End proof.

This does not bound the support of an arbitrary non-coverable proper point set. A noninjective map, point deletion/addition, or a new incidence structure is outside this family and needs a new Hall-deficiency check. In particular, it does **not** prove C_3=42.

An equivalent finite certificate adds, to the co-occurrence graph of coordinate symbols, edges between different symbols in the same coordinate (the injectivity requirement). The cube symbols form K_{k^2}. For k=3 and 4, the supplied finite certificates give 10 and 17 total symbols, and conflict graphs with 44 and 134 edges, respectively. The existing relabeling colors them with 9 and 16 colors, while the displayed cliques require at least that many.

## 2. Why known projection minimizers are insufficient here

Lev and Rudnev, *Minimizing the sum of projections of a finite set*, arXiv:1610.02504v2, Theorem 1, identify a projection-sum minimizer by the cube order. Their discussion before Theorem 2 explicitly warns that minimizers need not all have the same shape; Theorem 2 is a uniqueness result for specified closed-box cardinalities. This does not classify all 33-point sets with projection deficiency, and their rearrangement is not asserted here to preserve shared color support or properness.

Accordingly, the fixed-cube argument in Section 1 is not used to exclude every smaller-support obstruction.

Primary source: https://arxiv.org/html/1610.02504v2

## 3. Direct search target for C_3<=41

Known results give at least 33 points and at least 6 colors in a non-coverable proper 3-tuple configuration. If an improving obstruction of score at most 41 exists, a Hall-violating subset also has score at most 41. After taking its exact support, only these cases remain:

| Exact support q | Point-count range |
|---:|---|
| 6 | 33..35 |
| 7 | 33..34 |
| 8 | 33 |

The new `search_support.py` models **all ordered proper triples** on each palette, not just coordinatewise relabelings of S_3. For every triple t it has a binary inclusion variable x_t. For each coordinate and visible pair it has a binary projection flag y. It imposes:

- x_t<=y for the three projections of every selected tuple;
- sum x - sum y >= 1;
- 33<=sum x<=41-q and every color occurs;
- harmless normalizations: a chosen point is globally relabeled to (0,1,2); projection counts are ordered by coordinate permutation; the remaining color names 3,...,q-1 are ordered by occurrence count.

For any feasible solution the actual projection sum is no greater than sum y, so the integer-selected tuple set is a Hall obstruction. Conversely, each actual obstruction can be put into one of these normalized models with y equal to its true projection indicators.

An optional `--minimal-core` model uses the following additional necessary conditions for an inclusion-minimal Hall-violating subset: projection deficiency equals one and every occupied visible-input line contains at least two points. For the first condition, removal of any point leaves a coverable set, so |P|-1<=sum_i|pi_i(P)|<|P|. For the second, removal of a point unique on a visible line would preserve a positive deficiency, contradicting minimality. Taking this subset may reduce the exact support; its case is then handled by the corresponding smaller q-model.

These reductions are explanations of the model, not a proof of its solver outcome. HiGHS uses numerical MILP arithmetic. No exact infeasibility certificate, complete independent model audit, or Windows run has been supplied.

Results from the first and strengthened runs are stored separately in `support_search_q*.json` and summarized in `REVISION_NOTES.md`. No time limit is interpreted as nonexistence. A solver's infeasibility report without an exact independent certificate is kept as a search observation.
