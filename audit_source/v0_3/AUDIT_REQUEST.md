> Historical v0.2 material follows. For the current v0.3 output-routing fix and received audit, see FIX_v03.md. Claims of unchanged verifier bytes apply to v0.2 only.

# Differential audit request — No.35 candidate v0.3

The user-supplied v0.1 audit reports conditional PROOF PASS and COMPUTATION
PASS. PROOF.md's mathematical argument is unchanged; its version-specific
citations and status labels are clarified. The original ZIP is frozen under
prior/. Focus the new audit on REFERENCE_VERSION_MAP.md, SUPPORT_REDUCTION.md,
search_support.py, verify_revision.py, and the outcome/claim boundaries in
REVISION_NOTES.md. Do not extend the old PASS to these additions automatically.

New priority questions:

- Is the k^2 lower bound valid exactly for coordinatewise injective proper
  relabelings of the fixed S_k, without excluding other point sets?
- Is the reduction of an improving C_3 obstruction to exact supports 6,7,8
  and the listed point caps sound? Are the symmetry normalizations and
  optional minimal-Hall-core restrictions safe?
- Do the numerical solver statuses remain search observations, with
  C_3=42 and any improved upper bound explicitly unclaimed?
- Is the inherited-source/new-result division sufficiently narrow for a
  short note? Keep novelty and significance distinct from correctness.

The original audit questions are retained below as context:

1. Is S_k the already known Gadouleau/He–Ido–Przybocki construction, with cardinality M_k and projection deficiency one? Confirm attribution, including the minimum-cardinality theorem used in Section 6.
2. For every k>=3, does the special label phi_{k-1}(k)=k-1 always avoid equality with the first coordinate on the appended face? Check why k=2 must be excluded.
3. Does coordinatewise injectivity preserve every projection cardinality despite sharing a color between coordinate alphabets?
4. Does the Q=M_k+k^2+1 palette argument defeat every deterministic, vertex-specific strategy at every n? Check all quantifiers and the difference between an obstruction and a winning strategy.
5. Does every non-coverable complete proper box have score at least M_k+k^2+1? Check the harmonic-sum criterion, the integer support bound, and the use of the inherited minimum-cardinality theorem.
6. Is the elementary lower bound M_k+2k valid using the clique theorem HGP(K_k)=2k-1? Do not mistake it for a claimed original theorem.
7. Most importantly, is this precise proper relabeling, additive k^2 upper bound, or negative answer to box extremality already present under another description? Evaluate whether this is a worthwhile short note or merely an immediate known consequence.

Recompute the supplied finite counts and inspect the negative controls. The author's Windows run, an external review, a complete prior-art audit, exact C_3, and HGP(B_{2,5}) are all unclaimed.

Return PROOF / COMPUTATION / REFERENCES / NOVELTY separately. Preserve RELEASE=HOLD pending author review of the audit and the novelty boundary.
