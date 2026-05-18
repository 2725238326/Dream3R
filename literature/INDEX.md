# Literature Guidance Board

Last updated: 2026-05-05 (cycle 013 refresh pass: SPINE_MEMORY / SPINE_CRITIC / SPINE_COMPOSER / SPINE_PERMANENCE / CRITICAL_NOTES all folded in cycle-013-mined sources per the closeout deferred queue; PAPER_RELATED_WORK_SKELETON.md was upgraded to prose draft in cycle 013 S3; v1 structure unchanged)

Status: literature **guidance**, not literature **inventory**.

## Purpose

Existing source files are inventories: every paper Dream has touched, plus URL / track / evidence label rows. They answer "what do we know?".

This directory answers a different question: "if I were starting work on a Dream finalist tomorrow, what should I read first, what should I read second, what should I skip with reason, and where do papers contradict each other?"

The two are deliberately separate. Inventories grow monotonically; guidance is curated, opinionated, and revised when the spine of a finalist changes.

## Pointers To Inventories (Do Not Duplicate)

When a paper is added or its evidence label changes, edit the inventory, not this guidance board:

- full source map: `sources/FRONTIER_SOURCE_MAP.md`
- lightweight registry: `registry/source_registry.md`

If the new paper is commonly confused with an existing comparator or changes how a finalist is positioned, also add a line to `literature/CRITICAL_NOTES.md` and (if relevant) update the affected `literature/SPINE_*.md` file.

## Files

| File | Role |
|---|---|
| `INDEX.md` | this file; entry point and usage rules |
| `SPINE_CRITIC.md` | required + advanced + skip-with-reason reading for the Critic finalist (SPEC-20260503-001); cross-paper disagreements; interface to the spec |
| `SPINE_MEMORY.md` | same structure for the Executive Memory finalist (SPEC-20260503-002) |
| `SPINE_PERMANENCE.md` | same structure for the Dynamic Object Permanence finalist (SPEC-20260503-003) |
| `SPINE_COMPOSER.md` | same structure for the Composer finalist (SPEC-20260504-001); cross-domain analog (MoE routing) included |
| `CRITICAL_NOTES.md` | running log of "looks like X is X' but actually" insights; deconfusion of commonly-confused mechanisms |
| `PAPER_RELATED_WORK_SKELETON.md` | section list mapped to F1-F6 failure modes; populated from SPINE files; updates as case cards land |

## Usage Rules

When adding a new spine entry to a SPINE file:

1. Cite the source by its registry ID (e.g. `SRC-2025-007 Test3R`) and link to its inventory row, do not re-state URL or arXiv id.
2. Carry the inventory's evidence label forward unchanged. If you disagree with the label, change it in the inventory first via a cycle log, not silently here.
3. Add at most two lines per entry: "what this paper actually claims" and "what people often misread it as". The misread line is the lever; without it the entry duplicates the inventory.

When adding a CRITICAL_NOTES.md entry:

1. Title is the confusion (e.g. "Mem3R memory != Point3R memory").
2. Body is one paragraph, max five sentences. If you need more, the entry is probably about claim verification rather than deconfusion; route it to a cycle log instead.
3. Linked sources by registry ID.
4. Last-updated stamp.

When the SPINE files change in a way that affects the paper structure, update `PAPER_RELATED_WORK_SKELETON.md`. Do not let the skeleton drift silently.

## Evidence Discipline

Every claim about a paper carries an evidence label drawn from the standard ladder: `paper-proven`, `code-observed`, `demo-observed`, `inferred`, `unknown`. Speculative claims about a paper's positioning belong in CRITICAL_NOTES.md with `inferred` or `speculative`, not in the SPINE required-reading lines.

This is enforced by `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5 (Honesty Override). The literature board is a high-density target for tone drift because it explains rather than reports; a stricter label discipline is appropriate.

## Versioning

This is v1. The board itself may be revised, but:

- spine ordering changes that demote / promote a paper produce a cycle-log entry
- evidence-label changes happen in inventories, not here
- new finalist spec -> new SPINE file in this directory, plus an entry here in the file table

## Companion Files

- `paradigm/RESEARCH_CODE_DISCIPLINE.md` — rule 5 (Honesty Override) and rule 1 (Think Before Synthesizing) governing this board
- `sources/FRONTIER_SOURCE_MAP.md` — full inventory; cited from SPINE files
- `registry/source_registry.md` — lightweight ID -> URL map
- finalist specs in `specs/` — each SPINE file has a section interfacing to its spec
