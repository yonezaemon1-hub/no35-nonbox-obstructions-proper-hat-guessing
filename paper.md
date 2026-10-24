---
title: "Non-Box Obstructions for Proper Hat Guessing on Book Graphs"
author: "Ryutaro Yonezu - Yonezu Research Lab"
date: "24 October 2026 - Unrefereed preprint v1.0 (Research Note No.35)"
---

## Abstract and publication scope

We give a proper relabeling of an established non-coverable point-set recursion. For k>=3, it yields a support-sensitive obstruction of score M_k+k^2, where M_k=1+sum_{r=1}^k r^r, and consequently a uniform upper bound on proper hat guessing on book graphs. The color-sharing step saves exactly one color over the immediate disjoint-coordinate-color version of the known construction. Complete proper Cartesian boxes have strictly larger obstruction score. The recursive geometry, minimum-cardinality theorem, and supporting game invariants are prior work. Exact optimal values, scholarly novelty, and priority are not claimed. This public note retains the mathematics of the reviewed v0.3 candidate; formatting, current audit status, and the baseline comparison have been clarified.

The external AI reviewer reported proof/computation/references PASS, novelty INCONCLUSIVE, and RELEASE HOLD. The author's subsequent explicit instruction on 24 October 2026 authorizes this qualified public preprint. Reviewer recommendations remain preserved in the audit archive. All rights reserved.

Research contact: yonezaemon1+research@gmail.com

## 1. Model and claim boundary

Let B_{k,n}=K_k join an independent set of n pages. Each vertex sees its open neighborhood, makes one deterministic guess, and the adversary must provide a proper coloring. Strategies may differ at every vertex. HGP denotes the largest palette admitting a guaranteed win.

For a finite set P of ordered proper k-tuples, pi_i deletes coordinate i, supp(P) is the union of the colors occurring in P, and P is coverable when it can be partitioned into k parts on each of which the corresponding pi_i is injective. Write

    C_k = min {|P| + |supp(P)| : P is a non-coverable finite set of proper k-tuples}.

Zhai [Z, Theorem 1.1 and Theorem 3.8] identifies this invariant with sup_n HGP(B_{k,n}). We also give a direct game proof of our upper bound, so that part does not require importing the full stabilization result.

Put M_k=1+sum_{r=1}^k r^r. The candidate claims are:

1. For every k>=3 and n>=1, HGP(B_{k,n}) <= M_k+k^2. More specifically, C_k <= M_k+k^2.
2. Every complete Cartesian box consisting of proper tuples gives a strictly larger obstruction score than this bound, for every k>=3. This addresses the box-extremality question in [Z, Section 9.2] in the negative, subject to the received audit boundary and the unresolved scholarly-novelty review.
3. Combining existing theorems gives M_k+2k <= C_k <= M_k+k^2 for k>=3. The lower bound is an elementary deduction from prior results, not an independent new lower-bound method.

No claim of C_3=42 is made. No finite page threshold, winning strategy at 42 colors, or resolution of HGP(B_{2,5}) is claimed.

## 2. A completely explicit three-spine obstruction

Set A={0,1,2}, B={3,4,5}, D={6,7,8}, and

    P = (A x B x D) union ({0,1} x B x {2}).

There are 27+6=33 distinct tuples. Every tuple has three different entries and the support has size nine. The three projection sizes, in deletion order, are 12, 11, and 9. Thus

    |P|=33 > 12+11+9=32.

Each spine can correctly cover at most the number of its distinct visible-input slots. Therefore P is not coverable, and C_3 <= 33+9=42.

This is a nine-color obstruction used in a palette of at least 43 colors to defeat strategies; it is not a nine-color winning strategy or a 42-color winning strategy.

## 3. The inherited uncolored recursion

The recursive geometry here is known: the construction of Gadouleau, presented explicitly in He–Ido–Przybocki [HIP-EJC, Lemma 11 and Figure 1; HIP-arXiv, Lemma 2.6 and Figure 1]. We do not claim the recursion, its cardinality, or the uncolored minimum-cardinality theorem as new.

Use zero-based coordinate values and define

    S_1 = {(0),(1)},
    S_k = {0,...,k-1}^k union { (s,k) : s in S_{k-1} }  (k>=2).

By induction S_{k-1} is contained in {0,...,k-1}^{k-1}; hence the appended face lies next to the cube. The two pieces are disjoint, so |S_k|=k^k+|S_{k-1}|=M_k.

For a finite k-dimensional set X define its projection deficiency by

    d(X)=|X|-sum_i |pi_i(X)|.

We have d(S_1)=2-1=1 (the projection is the single empty tuple). The cube contributes k^k points and k projections of size k^(k-1), so has deficiency zero. Appending the face adds |S_{k-1}| points. Its projection in the last direction is already contained in the cube's projection. In each other direction it adds a disjoint copy, at last-coordinate value k, of the corresponding projection of S_{k-1}. Consequently d(S_k)=d(S_{k-1})=1.

## 4. Proper relabeling using exactly k^2 colors

Fix k>=3, and initially give coordinate i (zero-based) the disjoint block of colors

    phi_i(a)=ik+a, 0<=a<k.

The final coordinate also takes the extra value k. Assign it the existing color

    phi_{k-1}(k)=k-1.

Each coordinate map is injective on its own alphabet. In the cube, all tuple entries belong to disjoint blocks, hence are different. In the appended face, the first coordinate is at most k-2: S_{k-1} has dimension at least two and its first coordinate ranges from 0 to k-2. Thus its first-coordinate color is never k-1 on this face. No other coordinate block contains the extra color k-1. All tuples therefore remain proper.

Let P_k be the resulting set. Coordinatewise injectivity preserves |P_k| and each projection cardinality. The cube already uses all k^2 colors, and the extra face introduces none. Hence

    |P_k|=M_k,  |supp(P_k)|=k^2,  d(P_k)=1.

It follows that C_k<=M_k+k^2. The exclusion k>=3 is essential: for k=2, the analogous merge creates an improper tuple; the known value remains C_2=11.

## 5. Direct upper bound in the game

Take a palette of Q=M_k+k^2+1 colors and any strategy on any B_{k,n}. Embed P_k in that palette. For each page j, the set of guesses {g_j(p):p in P_k} contains at most M_k colors. Together with supp(P_k) it occupies at most M_k+k^2<Q colors. Choose a page color z_j outside that union.

These choices are independent, since pages are nonadjacent. For every spine tuple p in P_k, the combined assignment (p,z_1,...,z_n) is proper and every page is wrong.

Hold these page colors fixed. Spine i sees pi_i(p) and the fixed page vector; it can be right on at most |pi_i(P_k)| of these distinct assignments, since a visible input determines a single guess. The union of all spine successes therefore has size at most

    sum_i |pi_i(P_k)|=M_k-1<|P_k|.

Some assignment defeats every player. There is no winning Q-color strategy. Palette monotonicity gives HGP(B_{k,n})<=Q-1=M_k+k^2, for every n. This argument allows arbitrary deterministic local strategies and makes no symmetry restriction.

## 6. Why complete proper boxes cannot attain the minimum

A complete box T=A_1 x ... x A_k made entirely of proper tuples must have pairwise disjoint A_i. Write a_i=|A_i|. Such a box is non-coverable precisely when sum_i 1/a_i<1. The sufficiency follows by counting projections of the whole box. Conversely, if sum_i 1/a_i>=1, every subset Q of the box satisfies |pi_i(Q)|>=|Q|/a_i and therefore sum_i |pi_i(Q)|>=|Q|. Hall's matching criterion then makes the box coverable.

For a non-coverable box, Cauchy–Schwarz yields

    (sum_i a_i)(sum_i 1/a_i)>=k^2,

and hence sum_i a_i>k^2, or sum_i a_i>=k^2+1 by integrality. The established minimum-cardinality theorem [HIP-EJC, Theorem 2 and Lemmas 8–11; HIP-arXiv, Theorem 1.2 and Lemmas 2.3–2.6] says that every non-coverable k-dimensional point set has at least M_k points. Therefore every such box has score

    |T|+|supp(T)| >= M_k+k^2+1 > M_k+k^2 >= C_k.

The strict comparison uses a known theorem for cardinality. Its new candidate content is the proper relabeling in Section 4 and its consequence for the support-sensitive objective.

## 7. An inherited lower bound and current intervals

The minimum-cardinality theorem gives |P|>=M_k for any non-coverable P. Adriaensen et al. [A] prove HGP(K_k)=2k-1. A winning strategy on that clique partitions every set of proper k-tuples supported on at most 2k-1 colors into coverable parts (assign a tuple to one of its correct clique players). Thus a non-coverable proper P must use at least 2k colors. Adding the two inequalities gives C_k>=M_k+2k.

| k | Known optimized box bound in Zhai v3 | Candidate upper bound | Inherited lower bound |
|---:|---:|---:|---:|
| 3 | 46 | 42 | 39 |
| 4 | 317 | 305 | 297 |
| 5 | 3526 | 3439 | 3424 |

The exact C_k within these intervals is unresolved here. The k=6 finite check gives 50106 as our upper bound; the bundled finite integer-box optimizer gives 51487 for that restricted box problem. This k=6 box optimum is an internal computational result, not a number quoted from [Z].

## 8. Verification and limits

The standard-library verifier checks counts, properness, support, and projection deficiency at k=3,4,5,6 (33,289,3414,50070 tuples). It separately computes maximum bipartite matchings at k=3 and k=4, obtaining 32 and 288, respectively. Each of the 33 single-point deletions of P_3 becomes coverable. An unsafe color merge produces three improper tuples. These are controls for the finite verifier; the all-k theorem is the induction and direct proof above.

The supplied standard-library checks were rerun for this release on Linux/Python 3.12.14 and passed, including the documented execution order and regression controls. Windows-machine execution is not claimed. The user-supplied external AI review reports PROOF, COMPUTATION and REFERENCES PASS, NOVELTY INCONCLUSIVE and a reviewer RELEASE HOLD recommendation. The author explicitly approved public release on 24 October 2026. This is an unrefereed note, not a journal- or conference-peer-reviewed publication. No Lean/Coq formalization or comprehensive novelty certification is claimed.

## Comparison with the immediate disjoint-color baseline

The inherited recursion already gives an obstruction with M_k points and k^2+1 colors by assigning disjoint colors to each coordinate alphabet. Thus C_k <= M_k+k^2+1 follows immediately from prior constructions. The color-sharing operation in Section 4 improves that direct baseline by exactly one: 43 to 42 for k=3, 306 to 305 for k=4, and 3440 to 3439 for k=5. The larger differences from optimized box bounds must not be attributed entirely to color sharing. At k=3, the disjoint-color value 43 already beats the box value 46. Historical novelty and priority remain unestablished; this note is positioned as a short consequence of an established recursion.

## References

[HIP-EJC] Xiaoyu He, Yuzu Ido, Benjamin Przybocki. *Hat Guessing on Books and Windmills*. Electronic Journal of Combinatorics 29(1), P1.12 (2022). DOI: https://doi.org/10.37236/10098. Publisher full text: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i1p12/pdf/ . The recursive construction is attributed there to Gadouleau [its reference 8].

[HIP-arXiv] Same authors and title. arXiv:2010.13249, October 2020, 18-page PDF inspected on 2026-10-24. https://arxiv.org/pdf/2010.13249 . See REFERENCE_VERSION_MAP.md for the correspondence with the 19-page EJC publication; EJC numbering is not arXiv numbering.

[Z] Yulin Zhai. *Proper Hat-Guessing on Two-Spine Book Graphs*. arXiv:2607.25274v3, 18 August 2026. https://arxiv.org/html/2607.25274v3 . Sections 3, 7 and 9.2 define the support-sensitive invariant, give the box bounds, and ask about box extremality.

[A] Sam Adriaensen et al. *Hat guessing with proper colorings*. arXiv:2603.04909v4, 24 August 2026. https://arxiv.org/html/2603.04909v4 . The archived final literature check reports successful examination of Theorem 1.1, Proposition 2.3 and Section 5 of v4; earlier access failures in historical files refer to an earlier search.

[K] Ioannis Kakatelis. *An upper bound on the proper hat guessing number of graphs*. arXiv:2610.04124v2, 6 October 2026. https://arxiv.org/html/2610.04124v2 . Its order/maximum-degree bound was inspected as related work; it does not provide a competing uniform-in-page-count bound for this claim in the inspected text.


Copyright (c) 2026 Ryutaro Yonezu. All rights reserved.
