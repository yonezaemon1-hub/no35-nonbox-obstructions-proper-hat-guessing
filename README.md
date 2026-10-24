# No.35 - Non-Box Obstructions for Proper Hat Guessing on Book Graphs

Ryutaro Yonezu / Yonezu Research Lab / public preprint v1.0 / 24 October 2026.

**Unrefereed. Novelty INCONCLUSIVE. No priority claim. All rights reserved.**

For k>=3, the note proves C_k <= M_k+k^2 and HGP(B_{k,n}) <= M_k+k^2 for every n>=1, with M_k=1+sum(r^r,r=1..k). The construction uses a known Gadouleau-type recursion. The immediate disjoint-color baseline is M_k+k^2+1; color sharing improves it by exactly one. The respective k=3,4,5 upper bounds are 42,305,3439. No exact C_3=42 or winning strategy at 42 colors is claimed.

- `No35_Preprint_v1_0.pdf`: public English note.
- `paper.md`: editable public paper source.
- `audit_source/v0_3/`: preserved candidate proof, offline verification scripts, finite evidence, exploratory data and historical audit statuses.
- `RELEASE_NOTES.md`: author release decision and received external AI audit.
- `SHA256SUMS.txt`: integrity of this public repository payload.

Offline verification (Python 3.12, standard library):

```powershell
python .\audit_source\v0_3\verify_obstructions.py
python .\audit_source\v0_3\verify_revision.py
python .\audit_source\v0_3\regression_check.py
```

The optional exploratory solver programs have additional dependencies and are not needed for these checks. Linux/Python 3.12.14 release checks passed; Windows execution is not claimed. Reviewer-supplied Python 3.13.17 results are distinguished from author-side runs.

Historical files inside `audit_source` retain their original HOLD labels. The author explicitly instructed public release on 24 October 2026 after receiving the additional audit. This release does not turn an AI audit into journal/conference peer review and does not certify historical novelty. The TU Delft thesis full-text comparison remains incomplete.

Research inquiries: yonezaemon1+research@gmail.com
