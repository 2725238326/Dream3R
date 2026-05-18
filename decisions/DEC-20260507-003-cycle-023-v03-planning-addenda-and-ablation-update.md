# DEC-20260507-003: Cycle 023 launch — v0.3 planning addenda (3 HIGH RA items) + ablation plan addendum update (ABL-v02-10 + Pillar A coverage)

decision_id:    DEC-20260507-003
date:           2026-05-07
cycle:          023
status:         accepted
authorized_by:  user ("行开始全面推进" 2026-05-07; following agent recommendation to merge 023 + 023.5 into single cycle)
decision_type:  combined cycle launch (S2 v0.3 planning addenda + S3 ablation plan addendum update)
parent_decision: DEC-20260507-002 (cycle 022; defined post-022 trajectory; 023 + 023.5 as separate cycles)
supersedes:     nothing (merges 023 + 023.5 into single cycle per agent recommendation + user approval)

---

## Context

Cycle 022 closed DONE with two key outputs:

1. Path C SUCCEEDED — 7 review-action items (RA-01..07) captured:
   - RA-01 [HIGH]: bench_frame_budget.py lacks per-component latency pass/fail thresholds
   - RA-02 [HIGH]: ExpertAdapter base class interface unresolved (Q-cs-2)
   - RA-03 [MEDIUM]: NSA three-branch output combination underspecified
   - RA-04 [LOW]: losses.py MODIFIED/STABLE labeling contradiction
   - RA-05 [HIGH]: CUT3R / MoGe-2 / DepthAnything-V2 checkpoint inventory missing
   - RA-06 [MEDIUM]: T-v02-F oversized (gates all 9 ablations)
   - RA-07 [MEDIUM]: Pillar A lacks dedicated task in IMPLEMENTATION_ROADMAP

2. Paper v1.2 — §3.8 + §6.0–6.3 added for v0.2 A+D framing.

Agent recommended merging cycles 023 (ablation addendum) + 023.5 (v0.3 planning addenda)
into a single cycle because RA-02 (ExpertAdapter interface) and RA-05 (checkpoint inventory)
are prerequisites for writing a sound ablation plan. User approved: "行开始全面推进".

---

## Scope — cycle 023

### S1: This decision (DEC-20260507-003)

Scope lock and protocol definition for cycle 023.

### S2: v0.3 planning addenda — 3 HIGH RA items

Produce NEW addendum files for the 3 HIGH-priority review-action items from Path C.
Per B-roadmap-F rule: no in-place modification of cycle 020 planning artifacts;
supersede via NEW addendum files under `planning/`.

```text
RA-01 [HIGH] → PLANNING_ADDENDUM_V03_LATENCY_THRESHOLDS.md (NEW)
  Add per-component latency pass/fail thresholds to bench_frame_budget.py
  specification. Source: SPEC-004 Delta 1 per-frame component budget table.
  Produces explicit C1/C2/C3/C4/C5/C6 ms targets with pass/fail criteria
  for T-v02-A implementers.

RA-02 [HIGH] → PLANNING_ADDENDUM_V03_EXPERT_ADAPTER_ABC.md (NEW)
  Resolve Q-cs-2: specify ExpertAdapter abstract base class. Define:
  - Required method signatures (forward, get_capability_match, get_latency_estimate)
  - Required return-dict keys
  - Missing-checkpoint error protocol (fail-loud, not silent skip)
  - attention_regime slot
  Source: Q-cs-2 in CODE_STRUCTURE + COMPOSER_CAPABILITY_DESCRIPTORS.

RA-05 [HIGH] → PLANNING_ADDENDUM_V03_CHECKPOINT_INVENTORY.md (NEW)
  Checkpoint inventory for the 3 uninventoried experts (CUT3R EXPERT-04,
  MoGe-2 EXPERT-05, DepthAnything-V2 EXPERT-06). Per expert:
  - Checkpoint source (official repo / HuggingFace / other)
  - Model size (params + disk + VRAM fp16)
  - License
  - Availability status (confirmed / unverified / unavailable)
  - G_download gate requirement
  Source: COMPOSER_CAPABILITY_DESCRIPTORS + web search for checkpoint metadata.
```

NOT actioned in S2: RA-03 (MEDIUM), RA-04 (LOW), RA-06 (MEDIUM), RA-07 (MEDIUM; handled in S3).

### S3: Ablation plan addendum update

Produce NEW addendum file: `specs/SPEC-20260507-002-dream3r-ablation-plan-v03-addendum.md`

This file extends SPEC-005 (v0.2 ablation plan) with:

```text
ABL-v02-10: Test3R-alone comparator (Q1 from SPEC-20260507-001)
  Tests whether Test3R's built-in verifier alone matches Dream3R's
  Critic-gate-driven verification on pillar A metrics. If Test3R-alone
  passes, pillar A's novelty claim weakens. Tier 1 (load-bearing for
  pillar A robustness).

RA-07 Pillar A coverage patch:
  Add explicit Pillar A falsification task mapping — which ABLs
  (v0.1 ABL-4 Critic removal + v0.2 ABL-v02-6 selection-gate +
  ABL-v02-10 Test3R-alone) collectively cover Pillar A claims.
  This closes the gap Agent B found (Pillar A had no dedicated
  task in IMPLEMENTATION_ROADMAP).

VGGT offline-batch baseline note (Q2 from SPEC-20260507-001):
  Add explicit acknowledgment that ABL-v02-4 (Composer best-of-N)
  should include a VGGT offline-batch baseline for pillar D
  offline-batch framing. Not a new ABL; annotation on ABL-v02-4's
  variant list.
```

### S4: Cycle log + sync chain

- cycles/CYCLE-20260507-003.md NEW
- decision_registry → WORKFLOW_STATUS → RESEARCH_STATE → INDEX → TASK_SNAPSHOT final flip

---

## Why merging 023 + 023.5 is the right call

1. **RA-02 (ExpertAdapter ABC) is a prerequisite for ABL-v02-10**: the Test3R-alone
   comparator ablation needs to know how Test3R's adapter interface works to define the
   comparison protocol. Writing ABL-v02-10 without the adapter spec would produce a
   spec that references an undefined interface.

2. **RA-05 (checkpoint inventory) is a prerequisite for ABL-v02-4 variant definition**:
   the best-of-N vs single-expert ablation needs confirmed checkpoint availability for
   each expert. If 3 of 7 checkpoints are unavailable, the ablation variant matrix
   changes.

3. **RA-01 (latency thresholds) feeds ABL-v02-8**: the frame-budget benchmark ABL needs
   explicit pass/fail thresholds per component, not just "30-50 ms total".

Doing both in one cycle ensures the ablation plan can reference concrete interface specs
and confirmed checkpoint states instead of TBD placeholders.

---

## Not authorized in cycle 023

```text
- Training, GPU runs, checkpoint download, code execution
- In-place modification of CODE_STRUCTURE or IMPLEMENTATION_ROADMAP
  (B-roadmap-F: NEW addendum files only)
- In-place modification of SPEC-005 v0.2 body (NEW addendum file only)
- RA-03 / RA-04 / RA-06 (deferred; MEDIUM/LOW; not blocking)
- Abstract, Section 1/2/4/5/7/8 changes to PAPER_DRAFT_V1.md
- Finalizing Dream3R candidacy (DEC-20260501-004 still in force)
- Server-side action (markdown only; F-002)
```

---

## Discipline notes

```text
- B-roadmap-F: no in-place modification of cycle 020 artifacts;
  supersede via NEW addendum files under planning/
- SPEC-005 v0.2 body NOT modified; v0.3 addendum is a NEW file
  under specs/ (same NEW-file pattern as SPEC-004 on SPEC-001,
  SPEC-005 on SPEC-002, SPEC-20260507-001 on SPEC-003)
- All v0.3 content carries evidence labels per Discipline rule 5
- Pre-existing lint not fixed per Surgical Edits rule 3
- DEC-20260501-004 + DEC-20260504-002 still in force
```

---

## Version history

```text
v1  2026-05-07  cycle 023. Combined v0.3 planning addenda (3 HIGH
                RA items: latency thresholds + ExpertAdapter ABC +
                checkpoint inventory) + ablation plan v0.3 addendum
                (ABL-v02-10 Test3R-alone + Pillar A coverage + Q2
                VGGT baseline annotation). Authorized: user "行开始
                全面推进" 2026-05-07.
```
