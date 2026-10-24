# No.35 v0.3 — reproduction-output fix

2026-10-24 (Asia/Tokyo). Mathematical statements, bounds, and search decisions unchanged. RELEASE HOLD; NOVELTY INCONCLUSIVE.

The user supplied a v0.2 audit reporting PROOF PASS for the restricted-family lemma and reductions, REFERENCES PASS for the number correspondence, and COMPUTATION PARTIAL due to a reproducibility bug. The old documented execution order overwrote verification_results.json with the running environment's Python/OS strings, then required that regenerated file to match the frozen original bytes. This was a real defect in the supplied workflow.

v0.3 sends every generated witness and result of verify_obstructions.py to run_outputs/. verify_revision.py also sends its generated result there. Root certificates and root verification_results.json remain frozen and are still compared byte-for-byte with the original v0.1 ZIP. The archived original verifier is retained inside that ZIP; the current verifier is deliberately modified for output routing and is no longer claimed byte-identical. No mathematical result or environment field is discarded to hide a numerical mismatch.

The regression check executes the documented order, repeats it with changed Python/OS descriptions, compares every mathematical result with the archived baseline (excluding only python/platform), and checks that all root evidence bytes remain unchanged. A deliberately modified root mathematical result must still be rejected. These checks simulate metadata differences; they are not native Windows or Python 3.13 runs.

The received reviewer separately reported CP-SAT: q=6 INFEASIBLE after 340 seconds, q=7 UNKNOWN after 1500 seconds, and q=8 UNKNOWN after 840 seconds. Its q=6 model includes minimal-Hall-core conditions. Reviewer code/logs and exact independently checkable infeasibility certificates were not supplied. Record this as independent solver corroboration reported by the reviewer, not a newly reproduced computation or a decision for q=7/8. C_3 remains in 39..42.

No longer-running q=7/8 search is started by this fix. The next research step remains final prior-art review under HOLD before committing further computation time.
