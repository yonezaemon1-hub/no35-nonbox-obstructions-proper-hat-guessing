# Received external audit of v0.1 — faithful summary

Received through the user's message on 2026-10-24 (Asia/Tokyo). The complete text is in that conversation message. Reviewer identity, independent source code and raw execution logs were not supplied. The following records the **reported** checks, rather than representing them as executions by this assistant.

| Item | Received judgment |
|---|---|
| PROOF | PASS, conditional on the cited theorems |
| COMPUTATION | PASS |
| REFERENCES | PARTIAL |
| NOVELTY | INCONCLUSIVE, leaning toward a small contribution |
| RELEASE | HOLD |

The report confirmed the proper relabeling for k>=3 and the k=2 failure, preservation of projections, all quantifiers in the direct game argument, the complete-box comparison, and the inherited lower bound M_k+2k.

The reviewer reported separate recursion/relabeling code and Hopcroft–Karp checks for k=3,4,5: cardinalities 33/289/3414, support k^2, projection sums 32/288/3413, maximum matchings 32/288/3413. At k=6, only counts (50070 points, projection sum 50069) were reported, with no matching run. They also reported a k=3, 43-color, four-page game check, clique controls at K_3/K_4, the box optima 46/317/3526, success of the bundled verifier, and all archive hashes matching. Windows reproduction was unconfirmed.

For references the reviewer checked Zhai Table 4, Section 9.2 and Theorem 1.1, and the He–Ido–Przybocki arXiv text. They flagged the mismatch between arXiv numbering and the numbers used in the candidate, without verifying the EJC numbering. They did not check Adriaensen full text, Kakatelis, Alon/Tian, or `search_translation.py`.

On novelty, the report identified only the k^2-color proper relabeling as candidate-new, emphasized that the point-set recursion and the covering framework are known, and regarded the result as close to a short consequence of existing theorems. It saw possible short-note value in the negative answer to box extremality, but noted the unresolved 39..42 interval and lack of a smaller-support construction.

The report suggested investigating support reduction, or proceeding to final prior-art review while retaining HOLD. This revision chose a bounded support investigation after fixing the version labels. Its new barrier lemma and new MILP search are **outside** the received audit's scope.
