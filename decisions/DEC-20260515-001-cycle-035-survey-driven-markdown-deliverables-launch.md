# DEC-20260515-001: Cycle 035 survey-driven markdown deliverables launch

Status: accepted

Date: 2026-05-15

Cycle: 035

Decision type: bounded markdown deliverable execution

Authorized trigger: user approved proceeding with the cycle 035 scope of
`planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` (created 2026-05-15) by
replying "推进吧" after the proposal was presented in active conversation.

## Decision

Proceed with cycle 035 to execute the P0 short-term items from
`planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` Section 6:

1. Write `planning/SOTA_MATRIX_V2.md` — re-label SPEC-20260507-001 v0.2
   Tier 1-5 comparator pool entries against the survey's four-axis
   classification (failure modes / long-seq memory four types / test-time
   three subtypes / output asset three types).
2. Write `planning/CRITIC_CALIBRATION_PLAN_V1.md` — calibration plan for
   per-failure-mode threshold standardization on the C4 Critic geometric
   conflict signal, anchored to the survey's six failure mode list.
3. Write `planning/LONG_SEQ_REAL_TABLE_PLAN.md` — extension plan for the
   four existing `ablate_recurrence` variants on KITTI long windows
   (>=10 windows). Plan only; no run authorized by this DEC.
4. Append 4 new cross-spec risk rows to `planning/WORK_RISK_REGISTER.md`
   (OOD detection gap / external prior conflict / 4DGS license chain /
   input extension axis gap) as identified in proposal P0-4.

This DEC also authorizes the sync chain to update:

- `INDEX.md` — new entries for SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md
  and the three new planning files
- `WORKFLOW_STATUS.md` — Last updated stamp + cycle 035 row + Recommended
  Next User Decision block refresh
- `TASK_SNAPSHOT.md` — Last updated stamp + status flip (idle → cycle 035
  in_progress → idle on close) + cycle 035 subtask board
- `cycles/CYCLE-20260515-001.md` — new cycle 035 log

## Scope

Allowed in cycle 035:

- create the three new markdown files under `Dream/planning/`:
  - `SOTA_MATRIX_V2.md`
  - `CRITIC_CALIBRATION_PLAN_V1.md`
  - `LONG_SEQ_REAL_TABLE_PLAN.md`
- append 4 new rows to the Cross-SPEC Risk Table in
  `Dream/planning/WORK_RISK_REGISTER.md` (and bump its Last updated stamp)
- update `Dream/INDEX.md`, `Dream/WORKFLOW_STATUS.md`,
  `Dream/TASK_SNAPSHOT.md` per Guidance File Sync Rule (TASK_SNAPSHOT
  first)
- create `Dream/cycles/CYCLE-20260515-001.md` to log the cycle 035 close
  pass
- reference SPEC-20260506-004 / SPEC-20260506-005 / SPEC-20260507-001 /
  SPEC-20260507-002 / SPEC-20260508-001 / SPEC-20260508-002 by section /
  line anchor when needed; do NOT modify any SPEC file

Not authorized in cycle 035:

- editing any file under `Dream/specs/` (including drafting any v0.4
  spec delta; B1 / B2 / B3 from proposal §5 remain proposal-status only)
- editing any file under `Dream/code/`
- editing any file under `/hdd3/kykt26/code/dream3r/`
- importing CUT3R / Spann3R / Dream3R / server model runtime code
- checkpoint download or checkpoint use
- training or fine-tuning
- real model inference
- running ABL-v02-1..9 / ABL-memory-1..11 / ablate_recurrence on KITTI
  long windows / any other ablation run
- running `evaluate_real_sequence.py` or any server smoke test
- frontend or navigation work
- promoting any demo storyboard past `draft`
- paper claim promotion
- launching any v0.4 spec delta drafting cycle (separate DEC required)
- retiring any non-finalist track
- declaring teacher-demo readiness
- editing Track B 3R-mix files (Track B wound down 2026-05-14; manuscript
  surface remains decoupled from Dream/KYKT vocabulary)
- modifying `code/dream3r/RECENT_PROGRESS.md` or
  `code/dream3r/NEXT_PHASE_ROADMAP.md` (the proposal's W19-W30 reorder
  is a recommendation; actual roadmap updates need their own DEC)

## Required Boundary

The three new planning files (SOTA_MATRIX_V2 / CRITIC_CALIBRATION_PLAN_V1 /
LONG_SEQ_REAL_TABLE_PLAN) are **planning artifacts only**, not execution
authorizations. None of them by itself authorizes:

- launching a calibration run
- running ablate_recurrence on KITTI long windows
- modifying C4 Critic thresholds in `code/dream3r/config.py`
- modifying the v0.2 comparator-map spec

Each of those actions requires a separate DEC and per-step gate per F-002
and DEC-20260503-001 research-code-discipline rule 3 (Surgical Edits) and
rule 5 (Honesty Override).

The proposal upstream (SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md) status
remains `draft, awaiting user review` until and unless the user issues a
separate DEC that formally accepts the proposal as a v0.4 design input.
Cycle 035's purpose is to land the P0 markdown deliverables that the
proposal identified, not to ratify the proposal as a spec.

## Output Interpretation

If cycle 035 closes cleanly, the strongest allowed claim is:

```text
Cycle 035 lands four planning markdown deliverables that translate the
2026-05-15 3R-mix survey's observations (six failure modes, long-seq
memory four types, test-time three subtypes, output asset three types,
input extension axis gap) into (a) a re-labeled SOTA comparator matrix,
(b) a per-failure-mode calibration plan for C4 Critic, (c) a
long-sequence real-data ablate_recurrence extension plan, and (d) four
new cross-spec risks. The deliverables are planning evidence; no
calibration result, ablation result, spec change, or code change has
been validated.
```

The following remain unvalidated by cycle 035:

- whether per-failure-mode threshold calibration on real KITTI
  distributions improves Critic A4 verification quality
- whether the proposed long-sequence ablate_recurrence extension reveals
  scale drift or memory decay on KITTI >=10 windows
- whether the 4 new risks should trigger spec changes (no spec change
  authorized in this cycle)
- whether the survey-driven re-labeling of SPEC-20260507-001 v0.2
  comparator tiers should propagate to a v0.3 comparator spec delta
- whether the proposal's P1 items (B1 / B2 / B3 v0.4 spec deltas) should
  enter drafting

## Stop Gates

- **G0 authorization**: passed by this DEC.
- **G1 path setup**: only `Dream/planning/` (3 new files + 1 existing
  file edit) and `Dream/cycles/` (1 new file) may receive new content.
  Sync chain edits limited to `Dream/INDEX.md`,
  `Dream/WORKFLOW_STATUS.md`, `Dream/TASK_SNAPSHOT.md`.
- **G2 upstream traceability**: each of the 3 new planning files must
  link back to `planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` and to
  the relevant SPEC anchor (e.g., SOTA_MATRIX_V2 → SPEC-20260507-001 v0.2
  Tier 1-5; CRITIC_CALIBRATION_PLAN_V1 → SPEC-20260506-004 v0.2 C4 +
  CROSS_SPEC_SIGNAL_CONTRACT.md; LONG_SEQ_REAL_TABLE_PLAN → ablate_recurrence
  in `code/dream3r/RECENT_PROGRESS.md` and NEXT_PHASE_ROADMAP).
- **G3 evidence label discipline**: every quantitative claim in the new
  planning files must carry an evidence label (paper-derived /
  inferred / engineering-judgment / agent-decided / measured). No
  silent label upgrades.
- **G4 outputs**: all of the following must exist before cycle 035
  closes:
  - `planning/SOTA_MATRIX_V2.md`
  - `planning/CRITIC_CALIBRATION_PLAN_V1.md`
  - `planning/LONG_SEQ_REAL_TABLE_PLAN.md`
  - 4 new rows appended to `planning/WORK_RISK_REGISTER.md`
  - `cycles/CYCLE-20260515-001.md`
  - `INDEX.md` / `WORKFLOW_STATUS.md` / `TASK_SNAPSHOT.md` updated
- **G5 verification**: visual scan of each new file for (a) upstream
  links present per G2, (b) evidence labels present per G3, (c) no
  forbidden-action claims (no "the calibration was run", no "the
  spec was updated").

## Next Direction If Passed

After cycle 035 closes, the next admissible decision is one of:

- A: launch a separate DEC authorizing calibration data collection on
  KITTI (CRITIC_CALIBRATION_PLAN_V1 execution; requires F-002 server
  authorization).
- B: launch a separate DEC authorizing ablate_recurrence on KITTI long
  windows (LONG_SEQ_REAL_TABLE_PLAN execution; requires F-002 server
  authorization).
- C: launch a separate DEC starting v0.4 architecture delta drafting
  (B1 Critic path split / B2 output asset contract / B3 input extension
  axis), each as a markdown-only spec addendum to SPEC-20260506-004 v0.2.
- D: pause and revise the proposal based on cycle 035 deliverable
  quality.
- E: return to architecture-first mainline non-survey work (e.g., W22
  visualization pack, W23 expert adapter loading prerequisites).

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in,
DEC-20260501-011 thesis reframe, and DEC-20260503-001 research-code-
discipline all remain in force unchanged.
