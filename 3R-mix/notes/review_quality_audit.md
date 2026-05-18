# Review quality audit

Status: quality pass guided by local copies of:

- `guidance_skills/research-superpower`
- `guidance_skills/academic-research-skills`

These third-party guidance repositories are local references only and are ignored by Git.

## Adopted rules

1. Systematic question framing: state research questions, corpus source, inclusion/exclusion criteria, and screening rubric.
2. Precision over breadth: classify papers by role and evidence relevance, not by name-dropping.
3. Integrity gates: claims about performance, SOTA, code availability, deployment, and application quality require direct source support or a caution label.
4. Reviewer stance: test the paper against multiple lenses: domain coverage, method taxonomy, evidence sufficiency, writing quality, and strongest counter-argument.
5. Anti-sycophancy: do not upgrade a claim because it sounds useful; preserve uncertainty where the local corpus has not been fully read.

## Screening rubric used for this survey

Score is qualitative rather than numeric in the final paper, but the decision rules follow the research-superpower pattern:

- Tier A: direct 3R / pointmap / feed-forward geometry methods. Must be discussed in core sections.
- Tier B: adjacent 3R extensions: dynamic, long-sequence, test-time adaptation, prior-guided reconstruction. Discussed in mechanism-specific sections.
- Tier C: output representation / visualization methods: 3DGS, 4DGS, pose-free Gaussian methods. Discussed as application-output path.
- Tier D: supporting priors: depth, features, tracking, segmentation. Discussed only as auxiliary evidence, not as main-line 3R methods.
- Excluded from core claims: active perception, cross-domain memory, generic MoE/routing, and non-3R reasoning methods unless explicitly marked as analogy.

## Manuscript changes made in this pass

- Added a research questions and methodology section.
- Added corpus and screening table.
- Added direct/adjacent/supporting source boundaries.
- Added reviewer-style limitation section before conclusion.
- Tightened application claims and code/demo claims.
- Preserved “尚需确认” where code, license, or full experimental comparison was not verified.

## Residual risks

- Many PDFs are downloaded but not fully read; paper-level details beyond abstracts/local inventories still need targeted reading before final publication.
- Bibliography metadata is sufficient for drafting but should be DOI/venue-checked before formal submission.
- Current figures are Typst conceptual tables, not paper-derived diagrams.
- The review is a narrative survey, not a formal PRISMA systematic review.
