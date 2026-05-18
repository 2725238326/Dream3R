# DEC-20260506-004 cycle 020 launch + combined code structure planning + implementation roadmap scope lock

decision_id: DEC-20260506-004

date: 2026-05-06

status: locked

cycle: launches cycle 020; primary deliverables are planning/DREAM3R_V02_CODE_STRUCTURE.md (NEW) + planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (NEW); both markdown only

parents:
- DEC-20260501-004 (Dream3R = candidate, not final thesis)
- DEC-20260504-002 (no all-in any single finalist)
- DEC-20260506-001 (mainline architecture-first; v0.1 spec authored)
- DEC-20260506-002 (cycle 018 v0.2 architecture deltas locked)
- DEC-20260506-003 (cycle 019 v0.2 ablation plan addendum scope lock)

linked_artifacts:
- TASK_SNAPSHOT.md (resume pointer; updated FIRST in sync chain)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; INPUT — six numbered deltas mapped to code changes)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2 ablation plan; INPUT — nine ABL-v02 inform task ordering and review surface pattern)
- code/dream3r/ (existing v0.1 code; substrate; NOT modified by cycle 020)
- code/dream3r/PLAN.md (v0.1 implementation roadmap by user 2026-05-06; substrate; NOT modified by cycle 020 — v0.2 roadmap is a separate file)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; INPUT — 7-expert pool informs Composer C5 module redesign)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; INPUT — informs Memory C2 module redesign)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; INPUT — informs Perceiver C1 module redesign)
- planning/DREAM3R_V02_CODE_STRUCTURE.md (NEW; cycle 020 S2 deliverable)
- planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (NEW; cycle 020 S3 deliverable)

## One line summary

Launch cycle 020 to author two combined planning artifacts: planning/DREAM3R_V02_CODE_STRUCTURE.md (maps v0.2 architecture deltas to v0.1 code module changes; per-file change manifest with review surface for other agents) and planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (breaks code structure into per-task scope / inputs / outputs / pre-execution review checklist / post-execution validation checklist for other-agent handoff). Both markdown only; no code touch. Together they constitute the "其他agent审阅修改" load-bearing handoff surface per user request 2026-05-06.

## What user authorized in this session

User dialogue trail (2026-05-06, post cycle 019 closure):

```text
[user] Reviewed cycle 019 closure summary + agent recommendation B
       (skip cycle 020 = SPEC-003 v0.2 comparator map; jump to
       code structure + implementation roadmap as the cycles where
       "其他agent审阅修改" lands).

[user] "行，你帮我吧，我们需要高强度推进"

       Decoded:
       a) Approved option B: skip the post-019 trajectory's
          original cycle 020 (= SPEC-003 v0.2 comparator map
          addendum) for now; jump to code structure +
          implementation roadmap.
       b) "高强度推进" = high-intensity push: combine the
          original cycles 021 + 022 from DEC-20260506-003
          post-019 trajectory into a single cycle 020 with
          two main artifacts (S2 + S3) so that the other-
          agent handoff surface lands faster.
       c) Cycle 021+ is now the renumbering candidate for
          comparator map v0.2 + paper rewrite + cycle 015
          G_run resume + capability_match measurement pass.
```

Evidence label for this DEC: `user-decided` for cycle 020 scope (option B with combined-cycle compression); `user-instructed` for "高强度推进" intensity (justifies combined cycle and forward push); `agent-decided` for the renumbered post-020 trajectory (subject to user revision).

## Why this matters (interpretation; trajectory revision)

DEC-20260506-003 §"Post-019 trajectory" enumerated six queued cycles (020-025) in agent-recommended order, starting with comparator map v0.2 addendum. The user's prior cycle-019-closure dialog and this session's "行" + "高强度推进" jointly revise that trajectory:

```text
Original DEC-003 trajectory:        Revised under DEC-004 (this DEC):

  Cycle 020 = SPEC-003 v0.2          Cycle 020 = code structure
              comparator map                     + implementation roadmap
              addendum                             (combined; 2 artifacts)
  Cycle 021 = code structure         Cycle 021 = SPEC-003 v0.2
              planning                             comparator map addendum
                                                   (deferred from original 020)
  Cycle 022 = implementation         Cycle 022 = paper Phase 2 rewrite
              roadmap                              for v0.2 main-claim A+D
  Cycle 023 = paper rewrite          Cycle 023 = cycle 015 G_run
              for A+D                              resumption
  Cycle 024 = cycle 015 G_run        Cycle 024 = capability_match
              resumption                           measurement pass
  Cycle 025 = capability_match       Cycle 025 = first ablation
              measurement pass                     execution authorization
                                                   (per ABL-v02-N selection)
```

Rationale for the revision (per Honesty Override):

```text
- User-stated motivation: "高强度推进" + the user's earlier note
  that "其他agent审阅修改" load-bearing surface lands at code
  structure + roadmap; comparator map narrowing is a markdown-
  reorganization task with smaller blast radius and can wait.
- Combining code structure + roadmap into one cycle is cheaper
  than two cycles (one DEC + one cycle log + one sync chain
  vs two of each); content-wise they are tightly coupled
  (the roadmap consumes the structure as INPUT).
- Trajectory revision is allowed per DEC-003 §"Post-019
  trajectory": "User may revise priority / insert new cycles /
  drop any item". Documented here to avoid silent supersede;
  decision_registry will carry both the original and revised
  trajectory in successive rows (DEC-003 row preserved
  unchanged; DEC-004 row notes the revision).
```

## Why combined planning artifacts

Code structure planning (S2 deliverable; DREAM3R_V02_CODE_STRUCTURE.md) answers WHAT changes: which v0.1 code files get modified, what NEW modules are needed, what stays stable.

Implementation roadmap (S3 deliverable; DREAM3R_V02_IMPLEMENTATION_ROADMAP.md) answers HOW: breaks the WHAT into reviewable tasks for other agents. Per-task scope / inputs / outputs / estimated effort / pre-execution review checklist / post-execution validation checklist.

The two are tightly coupled but conceptually distinct. Keeping them as two separate files (rather than one merged file) lets other agents review either layer independently:

```text
- An agent reviewing "is the v0.2 code structure correct?" reads
  only DREAM3R_V02_CODE_STRUCTURE.md; doesn't need to wade through
  per-task review checklists.
- An agent reviewing "are the tasks well-scoped for execution?"
  reads only DREAM3R_V02_IMPLEMENTATION_ROADMAP.md; doesn't need
  to re-derive the structural rationale.
- An agent picking up a specific task to execute reads both:
  the structure for the WHAT, the roadmap for the HOW + checklist.
```

This separation also serves cycle 022+ where the original cycle 022 (single combined) would have produced one large file; splitting now establishes the pattern for future v0.3+ revisions.

## Allowed by this DEC

Cycle 020 may produce, in order:

```text
S1  This DEC + TASK_SNAPSHOT mid-pass anchor                   -> done by this commit (DEC) + sync pass
S2  planning/DREAM3R_V02_CODE_STRUCTURE.md (NEW)
    Map v0.2 architecture deltas (Delta 1..6 in SPEC-004) to
    v0.1 code module changes. Section structure:
    - Identity / Approval / Scope of v0.2 code structure
    - Reading order
    - Existing v0.1 code structure (per-file summary; cited
      from code/dream3r/PLAN.md; NOT re-derived)
    - v0.2 delta -> module mapping table (Delta 1..6 ->
      MODIFIED / NEW / STABLE files)
    - Per-file change manifest:
        * MODIFIED files (modules.py / model.py / losses.py /
          smoke_test.py / config.py / train.py / __init__.py)
          with: what changes / which v0.2 delta drives the
          change / interface stability promise / risk +
          review surface
        * NEW files needed (e.g., memory_anchor_bank.py for
          NSA + anchor bank; composer_experts/ subdirectory
          for 7-expert pool)
        * STABLE files (bus.py CR-1..CR-6 gates carry forward;
          existing token taxonomy stable)
    - Interface stability statement (which v0.1 APIs other
      modules depend on must NOT change syntactically; what
      semantic changes are honest to flag)
    - Server-side deployment surface (per F-002; what gets
      uploaded to /hdd3/kykt26/code/dream3r/)
    - Pre-existing v0.1 PLAN.md relationship (NOT replaced;
      coexists; v0.2 roadmap supersedes v0.1 phase 2-6 only)
    - Risks (R-cs-1..R-cs-N for code-structure-specific risks)
    - Boundaries (no code touch; planning only; etc.)
    - Linked artifacts
    - Open questions
    - Discipline notes
    - Version history                                          -> pending

S3  planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (NEW)
    Break S2 code structure into reviewable tasks for other
    agents. Section structure:
    - Identity / Approval / Scope of v0.2 roadmap
    - Reading order (S2 structure is INPUT)
    - Task taxonomy (T-v02-N tasks; per-task structure)
    - Per-task spec (T-v02-1..T-v02-M each with):
        * task_id / depends_on (other T-v02 tasks)
        * scope (which files; what changes)
        * inputs (existing files; spec sections; v0.1 PLAN.md
          checkboxes consumed by this task)
        * outputs (modified files; new files; tests; logs)
        * estimated effort (lines-of-code / engineering-hours
          inferred; honest evidence label)
        * pre-execution review checklist (handed to a reviewer
          BEFORE the agent starts implementation; verifies
          scope is correctly understood)
        * post-execution validation checklist (handed to a
          reviewer AFTER implementation completes; verifies
          changes match scope + tests pass + no regression)
        * execution gate (separate DEC + per-step micro
          gates; F-002 server-side; reviewer authorizes)
    - Task dependency graph (DAG; covers S2 module changes)
    - Recommended execution order (Tier 1 prerequisites
      first; then per-module)
    - Compute / wall-clock budget estimate (inferred)
    - Boundaries (no code touch; reviewer authorization
      required for each task)
    - Linked artifacts
    - Open questions
    - Discipline notes
    - Version history                                          -> pending

S4  Sync chain (TASK_SNAPSHOT first per F-001 rule 6;
    decision_registry append DEC-004; WORKFLOW_STATUS /
    RESEARCH_STATE / INDEX light sync; INDEX adds 2 NEW
    planning rows + latest cycle log pointer to
    CYCLE-20260506-005; cycles/CYCLE-20260506-005.md NEW
    cycle log)                                                 -> pending
```

## Not allowed by this DEC

```text
1. No code touch. The 2 planning artifacts document WHAT and HOW
   for v0.2 code changes; they do NOT execute any change.
   code/dream3r/ files are READ for analysis (per F-001 rule 1
   only when necessary; PLAN.md already read; bus.py / modules.py
   / model.py / losses.py / smoke_test.py NOT re-Read in cycle
   020 — content cited from PLAN.md + INDEX summary). Server-side
   /hdd3/kykt26/code/dream3r/ untouched.

2. No supersede of code/dream3r/PLAN.md. The v0.1 PLAN.md (user-
   authored 2026-05-06; phase 1-6 with checkboxes) is preserved
   unchanged. v0.2 roadmap is a SEPARATE file under planning/.
   PLAN.md phase 1 (code polish) checkboxes that align with v0.2
   deltas may be REFERENCED by v0.2 roadmap tasks; PLAN.md is NOT
   edited in cycle 020.

3. No new repo clones / installs / checkpoints. NSA / DINOv3 /
   per-expert-checkpoint downloads remain gated. v0.2 code
   structure documents what would be downloaded; v0.2 roadmap
   tasks document the download authorization surface but do
   NOT trigger downloads.

4. No retroactive rewriting of SPEC-20260506-002 v0.1 / SPEC-
   20260506-003 v0.1 / SPEC-20260506-004 v0.2 / SPEC-20260506-
   005 v0.2 bodies. All four are INPUTS; cycle 020 references
   them by section name + line anchors (Grep -n only when
   necessary).

5. No SPEC-20260506-003 v0.2 comparator map addendum. That is
   deferred to renumbered cycle 021 per the trajectory revision
   in §"Why this matters" above.

6. No paper rewrite. PAPER_DRAFT_V1.md Section 3 + Section 6
   update for v0.2 main-claim A+D framing remains a separate
   later cycle (renumbered cycle 022).

7. No KYKT navigation change. No frontend implementation. No
   demo storyboard promotion past `draft`. No teacher-demo
   readiness claim. No retiring of any non-finalist track. All
   carried unchanged from prior DECs.

8. No promotion of any task in DREAM3R_V02_IMPLEMENTATION_ROADMAP
   to "approved-for-execution". Each task carries an explicit
   execution gate ("requires separate DEC + per-step micro gates
   + reviewer authorization"); tasks are reviewable but not
   self-authorizing.

9. No silent revision of the v0.2 main-claim narrowing
   (A + D pillars per DEC-002). Code structure + roadmap may
   NOT introduce new pillars or re-promote demoted pillars
   (B / C) or reduce E to absent.

10. No silent supersede of cycle 019 ABL-v02 review checklist
    pattern. Per-task review checklist in cycle 020 roadmap
    follows the same structural pattern (pre + post execution
    checklists; explicit modification path = fresh DEC + v0.3
    addendum; no in-place edits to checklists).
```

## v0.2 code structure scope summary (S2 preview)

```text
Existing v0.1 code (per code/dream3r/PLAN.md + INDEX):
  __init__.py                package entry
  bus.py        ~130 lines   C6 Memory Bus + CR-1..CR-6 gates
  modules.py    ~280 lines   C1-C5 five computational cores
  model.py      ~150 lines   Dream3R main + bus tick orchestration
  losses.py     ~90  lines   multi-loss L_total
  smoke_test.py ~100 lines   end-to-end validation
  config.py                  YAML config (planned per PLAN 1.2)
  data_dtu.py                DTU DataLoader (planned per PLAN 2)
  train.py                   training driver (planned per PLAN 1.2)

v0.2 delta -> module mapping (preview; full table in S2):

  Delta 1 (frame budget)       -> NEW per-module latency
                                  instrumentation; modifies
                                  smoke_test.py + new bench script
  Delta 2 (DINOv3-S backbone)  -> modifies modules.py C1
                                  Perceiver; new heads from
                                  scratch (cannot transfer ViT-L)
  Delta 3 (NSA + anchor bank)  -> modifies modules.py C2 Memory;
                                  NEW memory_anchor_bank.py;
                                  NEW nsa_attention.py
  Delta 4 (sparse attention as -> shared with Delta 3 NSA layer;
   optimization)                  no separate file
  Delta 5 (7-expert Composer)  -> modifies modules.py C5 Composer;
                                  NEW composer_experts/ subdir
                                  with adapters per expert (one
                                  Python module per admitted
                                  expert: mast3r_adapter.py /
                                  fast3r_adapter.py / spann3r_
                                  adapter.py / cut3r_adapter.py /
                                  moge2_adapter.py / depth_anything
                                  _v2_adapter.py / test3r_adapter.py)
  Delta 6 (main-claim A + D)   -> documentation-only at code level;
                                  no module change required (the
                                  narrowing is paper-level, not
                                  code-level)

Stable / unchanged in v0.2:
  bus.py CR-1..CR-6 gates      (carries forward; only signal-
                                space additions if any)
  losses.py L_total structure  (multi-loss carries; loss weights
                                per ABL-v02-7 head schedule may
                                vary but L_total stays multi-loss)
  Token taxonomy T1..T6        (additive at most; no token
                                deletion)
```

## v0.2 implementation roadmap scope summary (S3 preview)

```text
Task taxonomy (T-v02-N tasks; full per-task spec in S3):

Tier 1 prerequisites (must run first; unblock other tasks):
  T-v02-A   Frame-budget benchmark scaffolding (smoke_test.py
            extension + new bench script). Unblocks Delta 1.
  T-v02-B   YAML config system (config.py expansion;
            preset: small_v01 / small_v02 / base_v02). Unblocks
            multi-variant ablation runs.

Tier 2 per-module v0.2 changes (parallelizable across modules):
  T-v02-C1  Perceiver C1 backbone swap to DINOv3-S; head re-init;
            frozen-backbone default (per Delta 2 + DINOV3_C1 memo).
  T-v02-C2-mem-bank  Memory C2 anchor bank (new file
            memory_anchor_bank.py; bounded K=256; LRU eviction;
            permanence-link protection).
  T-v02-C2-nsa       NSA selection gate (new file nsa_attention.py;
            three-branch compressed/selected/sliding; gate input
            mix critic_confidence + permanence_link).
  T-v02-C5  Composer C5 expansion to 7-expert pool (new
            composer_experts/ subdir with one adapter per
            admitted expert; routing policy per
            COMPOSER_CAPABILITY_DESCRIPTORS).

Tier 3 integration + validation:
  T-v02-D   model.py bus tick reorchestration (incorporates
            Tier 2 module changes; respects v0.1 bus tick
            order).
  T-v02-E   smoke_test.py v0.2 update (validates new modules
            in isolation + end-to-end forward + backward +
            loss + gates).
  T-v02-F   data_dtu.py + train.py for first v0.2 training
            (per PLAN.md phase 2 + 4; consumes T-v02-A..E).

Tier 4 ablation execution scaffolding (one task per ABL-v02
that needs special harness; reviewer authorization per task):
  T-v02-ABL-1   NSA-removal harness (allows variant routing
                between NSA and cosine top-k via config flag)
  T-v02-ABL-2   DINOv3 backbone tier harness
  T-v02-ABL-3   Frozen vs unfreeze harness
  T-v02-ABL-4   Composer best-of-N vs single-expert harness
  T-v02-ABL-5   Capability_match measurement micro-benchmark
                harness
  T-v02-ABL-6   Selection-gate signal subsetting harness
  T-v02-ABL-7   Head training schedule harness
  T-v02-ABL-8   Frame-budget benchmark harness (overlaps with
                T-v02-A; promotes T-v02-A scaffolding to
                production benchmark)
  T-v02-ABL-9   NSA kernel benefit decomposition harness

Each T-v02 task carries:
  pre-execution review checklist  (5-10 items; reviewer verifies
                                   scope before execution starts)
  post-execution validation       (5-10 items; reviewer verifies
   checklist                       changes match scope + tests
                                   pass + no regression)
  execution gate                   (separate DEC + per-step micro
                                   gates per F-002)
```

Total estimated effort (inferred): 22 tasks; total lines-of-code estimate ~2500-3500 (NEW) + ~800-1200 (MODIFIED); engineering-hour estimate per task ~2-12 hours; total ~80-150 engineering-hours for v0.2 code work (pre-training).

## Post-020 trajectory (revised; agent-recommended; user-revisable)

```text
Cycle 021   SPEC-20260506-003 v0.2 comparator map addendum
            (deferred from original cycle 020). NEW file under
            specs/. Reorganize comparators per in-pool / out-
            of-pool / out-of-scope tiers per SPEC-004 Delta 5.
            Markdown only. Lower priority than code structure
            but completes the v0.2 markdown trio.

Cycle 022   PAPER_DRAFT_V1.md Section 3 + Section 6 update for
            v0.2 main-claim A+D framing. Markdown only. Cycle
            launch DEC required.

Cycle 023   Cycle 015 G_run resumption (Critic A4 measured
            anchor; paused at S9 done). Server-side execution
            per F-002. Cycle launch DEC + per-step micro gates
            required.

Cycle 024   Capability_match measurement pass per ABL-v02-5
            (promotes inferred -> measured for 7-expert pool).
            Server-side execution per F-002. Cycle launch DEC
            + per-ablation DEC required.

Cycle 025   First task execution authorization from
            DREAM3R_V02_IMPLEMENTATION_ROADMAP (likely T-v02-A
            frame-budget benchmark scaffolding or T-v02-B YAML
            config; both are Tier 1 prerequisites). Server-side
            per F-002. Cycle launch DEC + per-task pre-execution
            review checklist sign-off + per-step micro gates.
```

This trajectory replaces the DEC-003 §"Post-019 trajectory" enumeration. Both are agent-recommended; both are user-revisable. Documented here to avoid silent supersede.

## Review surface for other agents (handoff checklist)

This DEC includes an explicit review surface so any agent picking up cycle 020 work for audit can verify:

```text
[ ] DEC scope is consistent with DEC-20260506-002 main-claim narrowing
    (A+D pillars; B/C demoted; E supporting; no re-promotion in code
    structure or roadmap).
[ ] Trajectory revision (skip DEC-003 cycle 020 = comparator map;
    combine cycles 021+022 into this cycle 020 = code structure +
    roadmap) is documented in §"Why this matters" + §"Post-020
    trajectory".
[ ] Code structure file maps each of v0.2 Delta 1..6 to specific v0.1
    code module changes (verify in DREAM3R_V02_CODE_STRUCTURE.md
    delta -> module mapping table).
[ ] Roadmap file has per-task pre-execution review checklist + post-
    execution validation checklist (the load-bearing other-agent
    handoff hook per user request 2026-05-06).
[ ] No task in roadmap is implicitly authorized by SPEC alone; each
    has an explicit execution gate.
[ ] No task in roadmap re-introduces dropped candidates (Kimi-KDA,
    VGGT, MapAnything).
[ ] code/dream3r/PLAN.md (v0.1 user-authored) is preserved unchanged;
    v0.2 roadmap coexists as a separate file.
[ ] code/dream3r/ source files are NOT modified by cycle 020 itself
    (planning-only).
[ ] F-001 + F-002 + Surgical Edits + Honesty Override followed.
[ ] Per-task review checklist subsections in roadmap are explicitly
    not modifiable in-place (B-roadmap-N forbids; supersede via
    fresh DEC + v0.3 addendum).
```

## Implications for prior cycles

```text
- Cycle 015 (Critic L3 pilot) remains paused at S9 done. v0.2 code
  structure does NOT resume G_run; cycle 015 G_run resumption is
  post-020 trajectory item 3 (renumbered cycle 023).

- Cycle 016 (architecture v0.1 + ablation plan + comparator map)
  closed cleanly. v0.2 code structure builds on its outputs.

- Cycle 017 (paper draft v1) carries forward unchanged. Its Section 3
  + Section 6 update is post-020 trajectory item 2 (renumbered cycle
  022).

- Cycle 018 (v0.2 architecture deltas) closed cleanly. SPEC-20260506-
  004 is the primary INPUT to cycle 020 code structure (Delta 1..6
  mapped to module changes).

- Cycle 019 (v0.2 ablation plan addendum) closed cleanly. SPEC-
  20260506-005 ABL-v02-1..9 inform cycle 020 roadmap task ordering
  (Tier 4 ablation execution scaffolding tasks T-v02-ABL-1..9 are
  one task per ABL where harness work is needed).

- DEC-20260506-003 §"Post-019 trajectory" is REVISED by this DEC.
  Original cycle 020 (= comparator map) is deferred to renumbered
  cycle 021. Combined original cycles 021+022 (= code structure +
  roadmap) become the new cycle 020. The DEC-003 row in
  decision_registry is preserved unchanged; this DEC documents the
  revision.

- code/dream3r/PLAN.md (v0.1 implementation roadmap; user-authored
  2026-05-06) remains unchanged. v0.2 roadmap coexists at planning/
  DREAM3R_V02_IMPLEMENTATION_ROADMAP.md. PLAN.md phase 1 checkbox
  items that align with v0.2 deltas (e.g., "Memory C2 GRU -> Mamba")
  are SUPERSEDED by v0.2 roadmap (which uses NSA + anchor bank
  per Delta 3); PLAN.md text is NOT edited; the supersede is
  documented in DREAM3R_V02_CODE_STRUCTURE.md §"Pre-existing v0.1
  PLAN.md relationship".
```

## Discipline notes

```text
- Surgical Edits (rule 3): cycle 020 produces 2 NEW planning files;
  no source code touch; no v0.1 spec / planning / PLAN.md body
  rewriting. decision_registry receives one new row.
  Other sync files (TASK_SNAPSHOT / WORKFLOW_STATUS / RESEARCH_STATE
  / INDEX) get line-3 timestamp + minimal cycle 020 callouts; INDEX
  also gets 2 new rows under planning/ + latest-cycle-log pointer
  update. Pre-existing markdown lint warnings NOT fixed in cycle 020.

- Honesty Override (rule 5): every per-file change in
  DREAM3R_V02_CODE_STRUCTURE.md carries an evidence label (paper-
  derived for Delta 2 backbone swap; speculative for Delta 3 NSA
  transfer; engineering-judgment for Delta 5 expert pool composition;
  inferred for line-of-code estimates). Every per-task entry in
  DREAM3R_V02_IMPLEMENTATION_ROADMAP.md carries an estimated effort
  + evidence label. Trajectory revision in §"Why this matters"
  preserves DEC-003 original trajectory as historical reason; does
  NOT delete or rewrite DEC-003 row in decision_registry.

- F-001 anti-32MB: cycle 020 references existing artifacts by name +
  line anchor; SPEC-001 v0.1 / SPEC-002 v0.1 / SPEC-004 v0.2 / SPEC-
  005 v0.2 / 3 cycle 018 planning files / code/dream3r/PLAN.md
  already in context or summarized in INDEX; no full re-Read.
  Source code files (bus.py / modules.py / model.py / losses.py /
  smoke_test.py) NOT Read in cycle 020 (PLAN.md summary + INDEX
  summary suffice for planning-level mapping). Each new artifact
  bounded under ~1000 lines.

- F-002 server topology: cycle 020 is markdown only. /hdd3/kykt26/
  untouched. The 2 new planning files document the server-side
  deployment surface (which v0.1 PLAN.md already established) but
  do NOT execute any deployment.

- Hard rules from AGENT_MASTER_PROMPT.md section 6 (carried): no
  reproduction; no checkpoint download; no training; no KYKT
  navigation change; no frontend implementation; no thesis
  finalization; no retiring of any non-finalist track; no demo
  storyboard promotion past `draft`. All in force; this DEC adds
  none and modifies none.

- DEC-20260501-004 candidate-not-final + DEC-20260504-002 no-all-in
  carried unchanged. v0.2 code structure + roadmap plan v0.2
  candidate code; they do NOT commit to v0.2 as final thesis.
  Tasks in roadmap are reviewable scaffolding; no task carries
  authorization.

- Review surface for other agents: per user instruction
  "其他agent审阅修改 + 文档更新清楚" + "高强度推进", every per-file
  change in code structure has a review surface; every per-task
  entry in roadmap has pre + post execution review checklists.
  These checklists are the primary handoff hook for review agents.
  Modifications go via fresh DEC + v0.3 addendum; no in-place edits.
```
