# DEC-20260507-002: Cycle 022 launch — Path C reattempt + paper Section 3+6 v0.2 rewrite

decision_id:    DEC-20260507-002
date:           2026-05-07
cycle:          022
status:         accepted
authorized_by:  user ("022—A吧" 2026-05-07; following cycle 021 summary + 022-A/B/C candidate menu)
decision_type:  combined cycle launch (S2 Path C reattempt + S3 paper Section 3+6 v0.2 rewrite)
parent_decision: DEC-20260507-001 (cycle 021; defined post-021 trajectory including 022-A as default)
supersedes:     nothing (new combined cycle; does not modify any prior DEC)

---

## Context

Cycle 021 closed `done-with-S2-blocked-by-infrastructure`:

- S1 done: DEC-20260507-001 (cycle 021 launch + Path C + comparator map v0.2)
- S2 BLOCKED: Path C review activation — 4 sub-agent attempts × ~3 min each; all API 500
  nil-pointer panic on Calcium-Ion/new-api gateway (persistent gateway-side bug, not prompt
  content). Deferred to cycle 022 per Honesty Override Option β.
- S3 done: SPEC-20260507-001 (v0.2 comparator map addendum; closes v0.2 markdown trio)
- S4 done: CYCLE-20260507-001.md (full Path C incident documented)
- S5 done: Full sync chain complete

Post-021 trajectory candidates 022-A/B/C were presented to the user. User selected:

  **022-A** (default recommendation) = combined Path C reattempt + paper Section 3+6 v0.2 rewrite

User authorization: "022—A吧" (2026-05-07).

---

## Scope — cycle 022-A

### S1: This decision (DEC-20260507-002)

Scope lock and protocol definition for cycle 022-A.

### S2: Path C reattempt

Spawn 2 sub-agents (general-purpose; READ-ONLY by instruction) to review cycle 020 planning
artifacts using their per-file/per-task review checklists:

  Agent A: E:\kykt\Dream\planning\DREAM3R_V02_CODE_STRUCTURE.md
  Agent B: E:\kykt\Dream\planning\DREAM3R_V02_IMPLEMENTATION_ROADMAP.md

Each agent produces a ≤500-word structured 5-section review (sections A–E; see §Path C protocol).

These agents run in **background** to allow parallel S3 paper rewrite execution.

### S3: Paper Section 3+6 v0.2 rewrite

In-place edit of `literature/PAPER_DRAFT_V1.md`. Scope: Sections 3 (Architecture) and 6
(Comparator positioning) only. Method: add `[v0.2 delta — cycle 022]` annotation blocks;
preserve v0.1 prose per Discipline rule 5 (no silent supersede). Source anchors:
SPEC-20260506-004 (v0.2 architecture deltas 1–6) + SPEC-20260507-001 (v0.2 comparator map).

### S4: cycles/CYCLE-20260507-002.md NEW

Cycle 022 log: records execution, Path C outcome (SUCCESS or BLOCKED), paper rewrite details,
any honest accounting of surprises or limitations. Written after S2+S3 complete.

### S5: Full sync chain

decision_registry → WORKFLOW_STATUS → RESEARCH_STATE → INDEX → TASK_SNAPSHOT (final flip
to `idle`). Rule: TASK_SNAPSHOT is written FIRST as mid-pass anchor before S2+S3 execution,
then flipped to `idle` at S5.

---

## Why this matters

### Path C (S2) — highest-value experiment deferred from 021

Path C is the first exercise of the review-checklist pattern introduced in DEC-20260507-001.
Once it succeeds:
- Agent A findings become revision candidates for DREAM3R_V02_CODE_STRUCTURE.md
- Agent B findings become revision candidates for DREAM3R_V02_IMPLEMENTATION_ROADMAP.md
- Review-action items are captured as v0.3 addendum inputs (B-roadmap-F rule: no in-place
  modification of cycle 020 artifacts; supersede via fresh DEC + v0.3 addendum)

Path C is genuinely HIGH-VALUE: the two reviewed artifacts are the implementation backbone
of the entire Dream3R v0.2 code structure and roadmap. Unreviewed, they carry unknown blind
spots. Reviewed, they produce a prioritized punch list.

### Paper rewrite (S3) — closes the v0.1/v0.2 paper gap

PAPER_DRAFT_V1.md was written in cycle 017 against the v0.1 architecture specification.
Six v0.2 architecture deltas (SPEC-20260506-004) and the v0.2 comparator map
(SPEC-20260507-001) have since been locked. The paper currently:
  - Describes ViT-L backbone (v0.1); v0.2 uses DINOv3-S (Delta 2)
  - Has no per-frame latency budget (v0.2: 30–50 ms/frame; Delta 1)
  - Describes C2 Memory as SSM/Mamba without storage/retrieval spec; v0.2 adds bounded
    anchor bank + NSA three-branch retrieval (Delta 3)
  - Lists 5 Composer backbones at coarse granularity; v0.2 admits exactly 7 lightweight
    experts with capability descriptors (Delta 5)
  - Uses HIGH/MEDIUM/LOW threat table against full v0.1 architecture; v0.2 narrows to
    A+D pillars with 5-tier pool structure (Delta 6 + SPEC-20260507-001)
  - Does not reflect main-claim narrowing to A+D (Delta 6)

Updating sections 3 and 6 closes the paper-architecture gap for the two sections most
directly affected by v0.2. Sections 1, 2, 4, 5, 7, 8 are out of cycle 022 scope.

---

## Path C protocol

Carried from DEC-20260507-001 §"Path C review protocol", unchanged:

```text
Agents:         2 general-purpose sub-agents
Mode:           background (allow parallel S3 execution)
Instructions:   READ-ONLY by agent prompt; no file writes; no code execution
Output:         ≤500-word structured 5-section review (A–E) per agent
```

Review sections (A–E):

```text
A. File-level integrity
   Is the file well-structured? Does it cover all major components?
   Are there obvious missing sections or header/footer issues?

B. Key-claim faithfulness
   Does the artifact accurately reflect v0.2 architecture deltas
   (Deltas 1–6 from SPEC-20260506-004)? Note any claims that
   contradict or lag behind v0.2.

C. Internal consistency
   Are cross-references, terminology, module naming, task IDs,
   and dependencies internally consistent? Flag any contradictions.

D. Risk and gap identification
   Top 2–3 gaps or underspecified items that would block a code
   author. What is missing?

E. Recommended actions
   ≤3 bullet points. Concrete, actionable items for the next
   revision cycle.
```

Failure protocol (from DEC-20260507-001 §Q4; Honesty Override Option β):

```text
If agents fail again with the same API 500 nil-pointer panic
signature as cycle 021:
  - Do NOT retry a 3rd time in cycle 022.
  - Close cycle 022 S2 as `blocked-by-infrastructure` (same pattern
    as cycle 021).
  - Document in CYCLE-20260507-002.md with full incident accounting.
  - Defer to cycle 023 (if gateway is fixed by then) or flag as
    a persistent infrastructure blocker requiring user intervention.
```

---

## Paper rewrite protocol (S3)

```text
Target file:    literature/PAPER_DRAFT_V1.md
Scope:          Section 3 (Architecture) + Section 6 (Comparator positioning)
Method:         in-place edit with [v0.2 delta — cycle 022 — 2026-05-07] annotation blocks
                added before each updated subsection; v0.1 prose preserved, NOT deleted;
                v0.2 content added as labeled additions or clearly marked replacements.
Evidence discipline:
                Every v0.2 claim carries an evidence label (paper-proven / paper-derived /
                inferred / speculative / engineering-judgment / user-decided).
Source anchors: SPEC-20260506-004 Deltas 1–6 (architecture v0.2)
                SPEC-20260507-001 (v0.2 comparator map addendum)
```

Section 3 changes (from SPEC-20260506-004):

```text
Delta 1 → add per-frame latency budget (30–50 ms; inferred) in §3.1
Delta 2 → update C1 description: DINOv3-S replaces ViT-L; ~22M frozen backbone; ~10-15 ms
Delta 3 → update C2 description: bounded anchor bank (K=256) + NSA three-branch retrieval
Delta 4 → add per-module attention regime table in §3.3 or §3.4 context
Delta 5 → update C5 description: 7 admitted experts EXPERT-01..07
Delta 6 → add §3.0 or inline note: main-claim narrows to pillars A+D (carried into §3.7
           substrate hypothesis framing)
```

Section 6 changes (from SPEC-20260507-001):

```text
5-tier pool structure → replace single HIGH/MEDIUM/LOW table with:
  In-pool (7) / Out-of-pool (3) / Out-of-scope (1) / Foundation (1) / Orthogonal (8)
Updated threat ranking → now anchored to pillars A+D (not full architecture)
  Key: Test3R = HIGH threat to pillar A; VGGT = HIGH threat to pillar D offline-batch
  Spann3R reclassified: v0.1 HIGH threat → v0.2 IN-POOL (most significant reclassification)
3 new comparison axes → Axis 9 (NSA), Axis 10 (DINOv3 tier), Axis 11 (Composer pool)
v0.1 threat table → preserved as §6.4 "v0.1 comparator positioning (traceability)"
```

Not authorized in S3:

```text
- Rewriting or deleting Abstract, Section 1, 2, 4, 5, 7, 8
- Changing Working title (separate DEC required)
- Deleting any v0.1 prose from Section 3 or 6
- Claiming measured results (discipline rule: no numbers without benchmark DEC)
- Finalizing Dream3R candidacy (DEC-20260501-004 still in force)
```

---

## Open questions inherited from cycle 021

Carried from DEC-20260507-001 §"Open questions (Q1–Q5)":

```text
Q1 (recommended for cycle 022 consideration):
   ABL-v02-10 Test3R-alone comparator for pillar A robustness gap.
   Status: NOT actioned in cycle 022 (paper rewrite scope is S3+S6;
   ablation plan addendum = SPEC-002 v0.2 addendum, separate cycle).
   Carried to post-022 candidates.

Q2 (recommended for cycle 022 consideration):
   VGGT-on-offline-batch baseline for ABL-v02-4 (pillar D offline-
   batch framing gap). Same status as Q1. Carried.

Q3–Q5: Lower priority; later cycles. Unchanged.
```

Note: Q1+Q2 are explicitly acknowledged but deferred. The S3 paper rewrite ACKNOWLEDGES
the Q2 gap (VGGT offline-batch threat to pillar D) in Section 6 text per Discipline rule 5,
but does NOT manufacture ablation numbers for it.

---

## Post-022 trajectory (updated)

Based on cycles 021–022 execution:

```text
023: SPEC-002 v0.2 ablation plan addendum (adds ABL-v02-1..10 new ablations;
     includes ABL-v02-10 Test3R-alone for Q1; includes ABL-v02-4 VGGT baseline
     for Q2; out of cycle 022 scope)

024: Cycle 015 G_run (long-deferred; paused at S9 per cycle 015 log)

025: Capability_match measurement architecture (server-side measurement
     design for route_regret + capability_match; first step toward measured
     numbers for paper)

026: First T-v02-N code task execution (first actual server-side code task
     in Dream3R v0.2 context)
```

Note: if Path C (S2) yields critical findings that require v0.3 addenda for cycle 020
planning artifacts, a 022.5 / 023-pre sub-cycle is inserted before the 023 ablation
addendum. Depends on Path C success.

---

## Discipline notes

```text
- All v0.2 paper additions carry evidence labels per Discipline rule 5
- v0.1 prose in PAPER_DRAFT_V1.md is NOT deleted (Surgical Edits rule 3 +
  Honesty Override; NEW-file pattern applies to specs; in-place-with-marker
  pattern applies to the evolving paper draft)
- Path C agents are READ-ONLY; any file-write attempt by agent would be
  unauthorized and should not be approved
- Server constraint: F-002 (KYKT 3R model code server-side only); this cycle
  is markdown-only; no server action needed in cycle 022
- Pre-existing lint warnings in PAPER_DRAFT_V1.md are NOT fixed in this sync
  pass (Surgical Edits rule 3)
```

---

## Version history

```text
v1  2026-05-07  cycle 022. Initial launch decision. Combined scope:
                S2 Path C reattempt + S3 paper S3+S6 v0.2 rewrite.
                Authorized: user "022—A吧" 2026-05-07.
```
