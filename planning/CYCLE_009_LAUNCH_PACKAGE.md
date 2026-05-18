# Cycle 009 Launch Package

Last updated: 2026-05-04 (pre-launch prep sub-pass; cycle 009 itself NOT started)

Status: **prep-only**. This document is a launch checklist. Cycle 009 has NOT started. Starting requires user `go` on D4' (cycle 009 launch authorization). Do not flip TASK_SNAPSHOT.md to `in_progress` until that signal is recorded.

## Why this file exists

This file exists so that the moment user authorizes cycle 009 (D4' = `go`), forward motion can start without another round of "what do we have, what do we need". It captures:

1. The pre-launch audit findings (what was checked, what's clean, what to know)
2. The subtask board skeleton for cycle 009 under default D1' / D2' values (parallel Composer + Critic; paper-derived only)
3. The activation procedure when `go` arrives

Cross-references for the actual cycle-009 work itself live in:

- `WORKFLOW_STATUS.md` "Recommended Next User Decision" (canonical decision wording)
- `TASK_SNAPSHOT.md` "Open user decisions" (concise restatement)
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` (signal contract every case card must respect, see CR-6)
- `specs/` (the four finalist L1 specs)

## Pre-launch audit findings (2026-05-04)

Audit scope: `Dream/specs/`, `Dream/paradigm/`, `Dream/planning/`, `Dream/registry/`, cross-spec contract v1.

Method: `Grep` scan for `TODO` / `TBD` / `FIXME` / `XXX` / `???`; `Grep` cross-reference scan for `CROSS_SPEC_SIGNAL_CONTRACT`; structural sanity grep for headings.

Results:

| Item | Status | Note |
|---|---|---|
| Open `TODO` / `TBD` / `FIXME` markers in specs/ | clean | 0 hits |
| Open markers in paradigm/ | clean | 0 hits |
| All 4 finalist L1 spec files present | clean | SPEC-20260503-001 / -002 / -003 + SPEC-20260504-001 |
| Cross-spec contract v1 structure | clean | Has Purpose / Scope / Signal Owner Table / Per-SPEC Published Signals (all 4) / 6 Conflict Resolution Rules including CR-6 mandating cycle 009 case cards record contract usage / Versioning / Change Log |
| Spec → contract back-reference (`CROSS_SPEC_SIGNAL_CONTRACT` in spec body) | partial | Only `SPEC-20260504-001-3r-composer.md` references the contract by name; Critic / Memory / Permanence specs do not. See note CR-A1 below |
| TEACHER_AUDIENCE_PROFILE.md fill-in structure | ready | 7 user-input sections present with example option menus; agent must not invent content (D3' input gate) |

### Cosmetic note CR-A1: spec → contract back-references

Three specs (Critic, Memory, Permanence) were drafted 2026-05-03, before the cross-spec contract was published 2026-05-04. The contract has full Per-SPEC Published Signals coverage for all four specs (so the forward link contract → spec is intact). The reverse link spec → contract exists only on the 2026-05-04 Composer spec.

This is cosmetic, not a blocker. Cycle 009 case cards must record contract usage per CR-6 anyway, so the contract will be consulted regardless. If the user wants the back-reference added, this is a one-line edit per spec at the top of each "Companion Files" or near the spec status line.

Recommendation: hold. Add back-references only if they help readability for the human reviewer; otherwise leave the asymmetry in place and note its origin in spec change logs at the next versioning event.

## Cycle 009 subtask board skeleton (under default D1' = parallel, D2' = paper-derived)

NOT YET ACTIVE. This skeleton is ONLY what cycle 009 would look like under default decision values. Decision values may change cells below.

```text
G1 (gate)  Wait for user `go` on D4' (cycle 009 launch authorization).
           Record the `go` in decisions/DEC-YYYYMMDD-NNN-cycle-009-launch.md
           with stamped D1' / D2' / D3' values at time of launch.

S1         Open cycles/CYCLE-20260505-001.md cycle log; flip
           TASK_SNAPSHOT.md status to in_progress; copy this subtask
           board into the snapshot board with statuses pending.

S2         Draft CASE-20260504-CRITIC-01: first Critic case card; cite
           SPEC-20260503-001 + cross-spec contract CR-1 / CR-3 / CR-5 /
           CR-6; capture cross-spec signals consumed and published.

S3         Draft CASE-20260504-CRITIC-02: second Critic case card;
           independent of CASE-20260504-CRITIC-01; same contract anchors.

S4         Draft CASE-20260504-CRITIC-03: third Critic case card;
           independent of S2 / S3 to test contract under multiple
           instances.

S5  (D1')  IF D1' = parallel: in parallel with S2-S4, draft
           CASE-20260505-COMPOSER-01..03 from paper-derived capability
           cards (default D2'); reference SPEC-20260504-001 + CR-1 /
           CR-4. SKIP if D1' = sequential.

S6         Cross-spec contract usage audit: verify CR-1..CR-6 instances
           recorded across the 6 (or 3) drafted case cards. Note any
           contract field that proved hard to populate; capture as a
           v1 -> v2 candidate.

S7         Cycle 009 closeout: write cycles/CYCLE-20260505-001.md
           closeout section; sync RESEARCH_STATE.md / WORKFLOW_STATUS.md;
           run Guidance File Sync Rule chain starting from
           TASK_SNAPSHOT.md (per anti-F-001 rule 6).

S8         Surface cycle-009 outputs to user: brief 3-section report
           (case cards drafted / contract gaps found / D-decisions
           surfaced for cycle 010); ask for cycle-010 launch decisions.
```

If D1' = sequential, S5 deletes; cycle 010 picks up Composer case cards instead.

If D2' = paper + KYKT-job-derived, S5 expands: each Composer case card needs both a paper anchor AND a KYKT-job anchor; estimate +50% time.

If D3' (TEACHER_AUDIENCE_PROFILE.md) is unpopulated at launch, S2-S5 still proceed (case cards are independent of demo storyboard per the file's own "Agent Behavior While This File Is Empty" rule); only D-decision packet at S8 will repeat the D3' ask.

## Activation procedure when user `go` arrives

When user replies with `D1' = ... D2' = ... D3' = ... D4' = go`:

1. Create `Dream/decisions/DEC-YYYYMMDD-NNN-cycle-009-launch.md` recording the four values verbatim and the user-message timestamp.
2. Create `Dream/cycles/CYCLE-20260505-001.md` with header `# CYCLE-20260505-001 Cycle 009 (Critic case-card filling [+ Composer if parallel])` + initial subtask board copied from this file.
3. Update `TASK_SNAPSHOT.md`:
   - Status: `in_progress`
   - Current task: `cycle-009-case-card-filling`
   - Phase: still `Phase 1.5` (cycle 009 stays inside Phase 1.5)
   - Subtask board: copy the active rows from this skeleton, adjusting for D1' / D2'
   - If interrupted, resume from: `cycles/CYCLE-20260505-001.md` last incomplete subtask
4. Begin S2 immediately.

If D3' content is included in the same `go` message, also:

5. Edit `paradigm/TEACHER_AUDIENCE_PROFILE.md` to fill the 7 user-input sections from D3' content, change Status from `placeholder` to `populated`, add a Change Log entry, bump Last updated.
6. Surface in S8 that D3' resolved and demo planning can begin (still gated on case-card data per `decisions/DEC-20260504-002`).

## Companion files

- `WORKFLOW_STATUS.md` "Recommended Next User Decision" (canonical D1'..D4' wording)
- `TASK_SNAPSHOT.md` "Open user decisions" (concise restatement)
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` (every case card respects this contract per CR-6)
- `specs/SPEC-20260503-001-geometry-critic.md` (anchor for S2-S4)
- `specs/SPEC-20260504-001-3r-composer.md` (anchor for S5 if D1' = parallel)
- `paradigm/TEACHER_AUDIENCE_PROFILE.md` (D3' input target)
- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` (D3 deferral memo)

## Change log

- 2026-05-04: file created during pre-launch prep sub-pass following the `TASK_SNAPSHOT.md` introduction; no cycle 009 work has started.
