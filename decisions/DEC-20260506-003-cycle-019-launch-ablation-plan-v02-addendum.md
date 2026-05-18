# DEC-20260506-003 cycle 019 launch + ablation plan v0.2 addendum scope lock

decision_id: DEC-20260506-003

date: 2026-05-06

status: locked

cycle: launches cycle 019; primary deliverable is SPEC-20260506-005 v0.2 ablation plan addendum (delta-only on SPEC-20260506-002 v0.1)

parents:
- DEC-20260501-004 (Dream3R = candidate, not final thesis)
- DEC-20260504-002 (no all-in any single finalist)
- DEC-20260506-001 (mainline architecture-first; v0.1 spec authored)
- DEC-20260506-002 (cycle 018 v0.2 architecture deltas locked)

linked_artifacts:
- TASK_SNAPSHOT.md (resume pointer; updated FIRST in sync chain)
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1 substrate; preserved per Honesty Override; receives only Version history tail pointer)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (cycle 018 v0.2 architecture; INPUT to v0.2 ablation deltas)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; INPUT — defines 7-expert pool + capability_match measurement gap)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; INPUT — defines NSA-removal ablation surface)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; INPUT — defines DINOv3-S vs -B vs -L + frozen vs partial-unfreeze ablation surface)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (NEW; cycle 019 S2 deliverable; v0.2 ablation plan addendum)

## One line summary

Launch cycle 019 to author SPEC-20260506-005 (v0.2 ablation plan addendum, NEW file, delta-only) covering ablation surfaces opened by the six v0.2 architecture deltas: NSA-removal, DINOv3-S vs -B vs -L, frozen vs partial-unfreeze, route_regret per-regime, capability_match measurement, Composer best-of-N vs single-expert, selection-gate signal subsetting, frame-budget benchmark, head training schedule. v0.1 ablation plan body is NOT rewritten; v0.2 addendum carries inline evidence labels per ablation. Each new ablation includes an explicit review checklist subsection so other agents can pick up the work for review / modification / execution gating.

## What user authorized in this session

User dialogue trail (2026-05-06, post cycle 018 closure):

```text
[user] Reviewed cycle 018 closure summary + agent recommendation of
       5 next-cycle candidates with priority order:
         (1) SPEC-002 v0.2 ablation plan addendum [agent recommended]
         (2) SPEC-003 v0.2 comparator map addendum
         (3) PAPER_DRAFT_V1 Section 3 + 6 rewrite for A+D
         (4) Cycle 015 G_run resumption (Critic A4 measured anchor)
         (5) Capability_match measurement pass

[user] "嗯嗯好的按你的来，不要忘记我们的工作规范，而且在你后续建立
       代码结构和任务安排后我还需要其他agent审阅修改，你文档更新清楚哈"

       Decoded:
       a) Approved option (1) SPEC-002 v0.2 ablation plan addendum
          as cycle 019 primary deliverable.
       b) Reminded agent to honor working discipline (F-001 anti-32MB
          / F-002 server topology / Surgical Edits / Honesty Override
          / hard rules in AGENT_MASTER_PROMPT.md section 6).
       c) Flagged that future code structure + task arrangement work
          (post-019; likely cycle 021+) will be reviewed and modified
          by other agents — set things up so other agents can pick up.
       d) Reinforced clear documentation.
```

Evidence label for this DEC: `user-decided` for cycle 019 scope (option 1 from agent's prioritized list); `user-instructed` for review-surface and clean-handoff requirements; `agent-decided` for the post-019 trajectory enumeration (subject to user revision).

## Why this matters (interpretation)

v0.2 architecture spec (SPEC-20260506-004) introduced six deltas with inline evidence labels but did NOT specify how to falsify them. The ablation plan v0.1 (SPEC-20260506-002) covers v0.1 architecture only; its 10 ABLs (ABL-1..ABL-10) are anchored to v0.1 modules and substrate hypothesis. The v0.2 deltas open new ablation surfaces that SPEC-002 v0.1 does not cover:

```text
1. NSA-to-3R transfer is `speculative` per DEC-20260506-002 §"Discipline
   notes" + planning/NSA_MEMORY_INTEGRATION_MEMO.md §"Risk / honest
   limits". An NSA-removal ablation is the natural falsification: if
   removing NSA selection (fall back to plain anchor bank with cosine
   top-k retrieval) does NOT measurably regress on long-context drift
   + verification recall, then NSA's contribution to v0.2 is zero and
   the speculative label was honest. This ablation MUST be in the v0.2
   ablation plan.

2. DINOv3-S substitution is `paper-derived` per DINOV3_C1 memo, but
   pointmap-quality risk under frozen-backbone + heads-from-scratch
   is unmeasured. v0.2 needs a backbone-tier ablation (-S / -B / -L)
   plus a frozen vs partial-unfreeze ablation. v0.1 ABL-2 (substrate
   hypothesis) does not cover backbone weight class.

3. Frame budget 30-50 ms/frame at 30 FPS is `inferred` per DEC-002 +
   SPEC-004 Delta 1. A frame-budget benchmark ablation (TITAN RTX
   wall-clock vs A100 paper-claim) is needed before any "streaming-
   first compliance" claim is published. v0.1 had no per-frame budget
   to benchmark.

4. Composer pool best-of-7 vs single-expert is the v0.2 main-claim D
   primary demonstration (per SPEC-004 Delta 6). v0.1 ABL-7 (Composer
   removal) tests "with vs without Composer" but not "best-of-N vs
   any single expert per regime" — that is the v0.2 D-claim
   falsification surface.

5. Capability_match values per Composer expert are `inferred` per
   COMPOSER_CAPABILITY_DESCRIPTORS §"Open items". A measurement pass
   is needed to promote those values from inferred to measured. The
   measurement plan belongs in the ablation plan even if execution
   is gated.

6. Selection-gate signal mix (Critic confidence + Permanence link
   co-driving NSA selection) is `speculative` per NSA_MEMORY memo.
   A signal-subsetting ablation (critic-only / permanence-only /
   both / neither) tests whether the cross-module signal mix is
   load-bearing.

7. Heads-from-scratch training schedule is unspecified — v0.2 says
   "frozen-backbone default; optional top-N unfreezing". A training
   schedule ablation (head-only vs head+top-N vs full) determines
   whether DINOv3-S can match DUSt3R-quality pointmaps under realistic
   training cost.

8. NSA hardware-aware kernel benefit on TITAN RTX (vs H100 published)
   is uncertain per NSA_MEMORY memo. Algorithmic vs wall-clock
   benefit needs to be measured separately.
```

These eight surfaces (S1..S8 above; orthogonal to subtask IDs) define the v0.2 ablation addendum scope.

## Allowed by this DEC

Cycle 019 may produce, in order:

```text
S1  This DEC + TASK_SNAPSHOT mid-pass anchor                    -> done by this commit (DEC) + sync pass
S2  specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (NEW)
    Delta-only addendum to SPEC-20260506-002 v0.1.
    Section structure (target ~500-700 lines):
    - Identity / Approval / Scope of v0.2 addendum
    - Reading order
    - Why v0.2 addendum exists (surfaces S1..S8 above)
    - v0.1 ABL traceability matrix (which v0.1 ABLs each v0.2 ABL
      extends, supersedes, or is independent of)
    - ABL-v02-1..ABL-v02-N (each with: ID / v0.2 delta link /
      v0.1 ABL link / baseline / variant / test setup / expected
      outcome + evidence label / falsification interpretation /
      execution gate / REVIEW CHECKLIST for other agents)
    - Falsification mapping table (v0.2 main-claim A + D pillars
      mapped to ABL-v02 IDs that falsify each)
    - Benchmark input mapping (v0.1 B1-B6 reused; new categories
      proposed if needed for v0.2 specifically)
    - Dependency graph (v0.2 ABLs only; cross-references to v0.1
      ABLs)
    - Compute budget estimate addendum (v0.2-specific cost)
    - Boundaries (delta + carry from v0.1)
    - Linked artifacts
    - Open questions
    - Discipline notes
    - Version history                                            -> pending
S3  Sync chain (TASK_SNAPSHOT first per F-001 rule 6;
    SPEC-002 v0.1 Version history tail v0.2 pointer;
    decision_registry append DEC-003 + backfill DEC-002 status
    [bundled honesty correction; cycle 018 closed status flip];
    WORKFLOW_STATUS / RESEARCH_STATE / INDEX light sync;
    INDEX adds SPEC-005 row + latest cycle log pointer to
    CYCLE-20260506-004; cycles/CYCLE-20260506-004.md NEW
    cycle log)                                                   -> pending
```

## Not allowed by this DEC

```text
1. No training. No GPU runs. No checkpoint download. v0.2 ablation
   addendum is markdown spec; execution remains gated. Any subsequent
   ablation execution requires a separate per-ablation DEC + per-step
   micro gates similar to cycle 015's G_clone / G_install / G_download
   / G_run / G_log_use chain. Ablation-execution authorization is
   explicitly OUT of cycle 019 scope.

2. No retroactive rewriting of SPEC-20260506-002 v0.1 body. v0.2 is
   a NEW file (SPEC-005). v0.1 receives only a Version history tail
   pointer, not in-place edits to its 10 ABL sections, falsification
   table, dependency graph, or boundaries. (Surgical Edits rule 3 +
   Honesty Override rule 5; same pattern as cycle 018's SPEC-001 ->
   SPEC-004 v0.2 architecture handling.)

3. No paper rewrite. PAPER_DRAFT_V1.md Section 3 + Section 6 update
   for v0.2 main-claim A+D framing remains a separate later cycle
   (post-019 trajectory item 3). Cycle 019 ablation addendum may
   cite paper sections as future consumers but does NOT modify them.

4. No comparator map addendum. SPEC-20260506-003 v0.2 narrowing per
   in-pool / out-of-pool / out-of-scope tiers (per SPEC-004 Delta 5)
   is post-019 trajectory item 2; explicitly OUT of cycle 019 scope.

5. No code touch. No Dream3R PyTorch implementation changes
   (E:\kykt\Dream\code\dream3r\ + server-side /hdd3/kykt26/code/dream3r/
   are both untouched). Code structure planning is post-019 trajectory
   item 4; not in this DEC. Per F-002 server-topology rules, any
   code touch goes server-side and requires a fresh DEC.

6. No KYKT navigation change. No frontend implementation. No demo
   storyboard promotion past `draft`. No teacher-demo readiness
   claim. No retiring of any non-finalist track. All carried unchanged.

7. No silent supersede of DEC-20260506-002 main-claim narrowing.
   Cycle 019 falsification mapping must be consistent with A+D
   pillar framing; B/C remain demoted to discipline / future;
   E remains supporting. v0.2 ablation addendum may NOT introduce
   new pillars or re-promote B/C/E.

8. No promotion of inferred capability_match values to measured
   without execution. Cycle 019 documents the measurement plan;
   it does NOT execute it.
```

## v0.2 ablation addendum scope summary

```text
ABL-v02-1  NSA-removal (selected branch ablation; falls back to
           plain anchor bank with cosine top-k retrieval)
           tests:   v0.2 Delta 3 + Delta 4 (NSA Memory + sparse
                    attention as architectural optimization)
           ev_lbl:  speculative -> falsifies if NSA contributes 0

ABL-v02-2  DINOv3 backbone tier (-S / -B / -L)
           tests:   v0.2 Delta 2 (DINOv3-S replaces ViT-L)
           ev_lbl:  paper-derived -> -S vs -B Pareto frontier
                    measurement; -L is escape hatch baseline

ABL-v02-3  Frozen vs partial-unfreeze (top-N blocks)
           tests:   v0.2 Delta 2 (frozen-backbone default)
           ev_lbl:  inferred -> measures pointmap quality cost
                    of frozen-backbone simplification

ABL-v02-4  Composer best-of-N vs single-expert per regime
           tests:   v0.2 Delta 5 + Delta 6 main-claim D
           ev_lbl:  paper-derived -> direct D-pillar falsification

ABL-v02-5  Capability_match measurement pass
           tests:   v0.2 Delta 5 (capability_match values are
                    currently inferred)
           ev_lbl:  inferred -> measurement plan only;
                    promotes inferred -> measured if executed

ABL-v02-6  Selection-gate signal subsetting (Critic-only /
           Permanence-only / both / neither driving NSA top-k gate)
           tests:   v0.2 Delta 3 + Delta 6 main-claim A
           ev_lbl:  speculative -> tests whether cross-module
                    signal mix is load-bearing for verification

ABL-v02-7  Head training schedule (head-only / head+top-N
           unfreeze / full-unfreeze; fixed budget)
           tests:   v0.2 Delta 2 (heads from scratch; ViT-L head
                    weights cannot transfer)
           ev_lbl:  inferred -> measures DINOv3-S quality ceiling

ABL-v02-8  Frame-budget benchmark (TITAN RTX wall-clock vs
           paper-claim A100 for full v0.2 streaming pass)
           tests:   v0.2 Delta 1 (30-50 ms/frame at 30 FPS)
           ev_lbl:  inferred -> compliance check before any
                    streaming-first claim is published

ABL-v02-9  NSA kernel benefit decomposition (algorithmic
           sparsity gain vs hardware-aware kernel gain on
           TITAN RTX)
           tests:   v0.2 Delta 4 (NSA as engineering optimization)
           ev_lbl:  inferred -> separates algorithmic vs kernel
                    contributions for honest reporting
```

Each ABL-v02-N row in SPEC-005 will carry: baseline / variant configuration / test setup / expected outcome / falsification interpretation / execution gate / **review checklist for other agents** (the explicit handoff surface per user request).

## Post-019 trajectory (agent-recommended; user-revisable)

Other agents picking up this work will see the following queued cycles. None is launched without separate user direction.

```text
Cycle 020   SPEC-20260506-003 v0.2 comparator map addendum
            (NEW file; SPEC-20260506-006? — pending ID confirmation
            at cycle launch). Reorganize comparators per in-pool /
            out-of-pool / out-of-scope tiers. Markdown only.

Cycle 021   Code structure planning artifact (NEW; markdown only;
            file location TBD at cycle launch — likely
            planning/DREAM3R_V02_CODE_STRUCTURE.md). Documents how
            v0.2 deltas map to v0.1 code module changes (existing
            v0.1 code at E:\kykt\Dream\code\dream3r\ + server-side
            /hdd3/kykt26/code/dream3r/). Specifies what code files
            change, what new modules are added, what interfaces
            remain stable. THIS IS PLANNING ONLY; no code touch.
            Per F-002, eventual code execution goes server-side
            and requires a fresh DEC.

Cycle 022   Implementation roadmap + task arrangement (NEW; markdown
            only; file location TBD — likely
            planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md). Breaks
            cycle 021's code structure into reviewable tasks for
            other agents. Each task gets: scope / inputs / outputs /
            estimated effort / pre-execution review checklist /
            post-execution validation checklist. THIS IS PLANNING
            ONLY; no code touch. Authorization for any task
            requires a separate DEC per task.

Cycle 023   Paper Phase 2 rewrite for v0.2 main-claim A+D (PAPER_
            DRAFT_V1.md Section 3 + Section 6 update; possibly
            Section 4 claim narrative reanchoring). Markdown only.
            Cycle launch DEC required.

Cycle 024   Cycle 015 G_run resumption (Critic A4 measured anchor;
            paused at S9 done). Server-side execution per F-002.
            Cycle launch DEC + per-step micro gates required.

Cycle 025   Capability_match measurement pass per ABL-v02-5
            (promotes inferred -> measured for 7-expert pool).
            Server-side execution per F-002. Cycle launch DEC +
            per-ablation DEC required.
```

This trajectory is agent-recommended; user may revise priority / insert new cycles / drop any item. Documenting it here lets other agents (per user request "其他agent审阅修改") see the full forward picture without having to re-derive it.

## Review surface for other agents (handoff checklist)

This DEC includes an explicit review surface so any agent picking up cycle 019 work for audit can verify:

```text
[ ] DEC scope is consistent with DEC-20260506-002 main-claim narrowing
    (A+D pillars; B/C demoted; E supporting; no re-promotion).
[ ] Each v0.2 ablation maps to at least one v0.2 architecture delta
    (ABL-v02-1..9 -> Delta 1..6 traceability; verify in SPEC-005).
[ ] No ABL-v02-N reintroduces a dropped candidate (no Kimi-KDA, no
    VGGT in-pool, no MapAnything in-pool).
[ ] Each v0.2 ablation carries an evidence label (paper-known /
    paper-derived / inferred / speculative / engineering-judgment).
[ ] Each v0.2 ablation has an execution gate ("requires separate
    DEC + per-step micro gates"); no ablation is implicitly
    authorized by SPEC-005 alone.
[ ] SPEC-002 v0.1 body is NOT modified; only Version history tail
    receives v0.2 pointer.
[ ] F-001 + F-002 + Surgical Edits + Honesty Override followed.
[ ] Per-ABL review checklist subsection present in SPEC-005 (the
    handoff hook per user request).
[ ] Post-019 trajectory enumeration (cycles 020..025) consistent
    with hard rules in AGENT_MASTER_PROMPT.md section 6.
```

## Implications for prior cycles

```text
- Cycle 015 (Critic L3 pilot) remains paused at S9 done. v0.2 ablation
  plan addendum does NOT resume G_run; cycle 015 G_run resumption is
  post-019 trajectory item 4 (cycle 024).

- Cycle 016 (architecture v0.1 + ablation plan + comparator map) closed
  cleanly. v0.2 addendum builds on its outputs; does NOT invalidate
  any v0.1 ABL-1..ABL-10. v0.1 ABLs remain canonical for v0.1
  architecture testing.

- Cycle 017 (paper draft v1) carries forward unchanged. Its Section 3
  + Section 6 update is post-019 trajectory item 3 (cycle 023).

- Cycle 018 (v0.2 architecture deltas) closed cleanly per
  CYCLE-20260506-003. SPEC-004 v0.2 architecture is the primary input
  to cycle 019 SPEC-005. DEC-20260506-002 status note in
  decision_registry currently reads "accepted (S1-S3 done; S4-S5
  partial)" — that note was accurate in first session but became
  stale on cycle 018 closure. Cycle 019 sync chain bundles a backfill
  to update this note to "accepted (S1-S5 closed)" as an honesty
  correction.

- RU-007 (Attention-Residual / KDA 3R) status remains "rejected for
  v0.2 scope; LM-to-3R transfer not pursued in active branch" per
  cycle 018 S5 update. Cycle 019 does NOT reopen RU-007.
```

## Discipline notes

```text
- Surgical Edits: SPEC-005 is a NEW file; SPEC-002 v0.1 body NOT
  rewritten. v0.1 receives only Version history tail pointer.
  decision_registry receives one new row + one stale-note backfill.
  Other sync files (TASK_SNAPSHOT / WORKFLOW_STATUS / RESEARCH_STATE
  / INDEX) get line-3 timestamp + minimal cycle 019 callouts; INDEX
  also gets one new row under specs/ + latest-cycle-log pointer
  update. Pre-existing markdown lint warnings (SPEC-001 line 593
  table; TASK_SNAPSHOT historical block; cycle log tables) NOT
  fixed in cycle 019 per Surgical Edits rule 3.

- Honesty Override: every v0.2 ablation in SPEC-005 carries an inline
  evidence label. NSA-removal expected outcome is `speculative` (no
  3R prior art); DINOv3 tier ablation is `paper-derived`; frame
  budget is `inferred`; capability_match measurement plan is
  `inferred -> measured-if-executed`. Stale-note backfill on
  DEC-20260506-002 row in decision_registry is itself an Honesty
  Override action: do not delete the prior status string; supersede
  with reason ("S1-S5 all closed per cycle 018 closure 2026-05-06").

- F-001 anti-32MB: SPEC-005 target ~500-700 lines (delta-only).
  SPEC-002 v0.1 (~770 lines, ~30 KB) is NOT re-Read in cycle 019;
  cited via existing TOC + Grep -n for specific section anchors
  (B1-B6 line 537 + Falsification summary line 630 + Version
  history line 761). SPEC-001 v0.1 + SPEC-004 v0.2 already in
  context from cycle 018; no re-Read needed.

- F-002 server topology: cycle 019 is markdown only. No server-side
  execution. /hdd3/kykt26/ untouched. Any subsequent ablation
  execution goes server-side per F-002 rules and requires a fresh
  DEC + per-step micro gates.

- Hard rules carried from AGENT_MASTER_PROMPT.md section 6: no
  reproduction / no checkpoint download / no training / no KYKT
  navigation change / no frontend implementation / no thesis
  finalization / no retiring of any non-finalist track / no demo
  storyboard promotion past `draft`. All in force; this DEC adds
  none and modifies none.

- DEC-20260501-004 candidate-not-final and DEC-20260504-002 no-all-in
  carried unchanged. v0.2 ablation addendum tests v0.2 architecture;
  it does NOT commit to v0.2 as the final thesis. v0.2 main-claim
  narrowing to A+D from DEC-20260506-002 is the load-bearing pillar
  ordering; v0.2 ablations do NOT re-promote demoted pillars.
```
