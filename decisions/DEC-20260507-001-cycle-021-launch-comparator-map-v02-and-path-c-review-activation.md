# DEC-20260507-001 cycle 021 launch + comparator map v0.2 addendum + Path C review activation

decision_id: DEC-20260507-001

date: 2026-05-07

status: locked

cycle: launches cycle 021; primary deliverables are specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (NEW) + Path C review of cycle 020 planning artifacts (other-agent review activation); both markdown only

parents:

- DEC-20260501-004 (Dream3R = candidate, not final thesis)
- DEC-20260504-002 (no all-in any single finalist)
- DEC-20260506-001 (mainline architecture-first)
- DEC-20260506-002 (cycle 018 v0.2 architecture deltas locked)
- DEC-20260506-003 (cycle 019 v0.2 ablation plan addendum scope lock; original cycle 020 = SPEC-003 v0.2 comparator map addendum)
- DEC-20260506-004 (cycle 020 launch + combined code structure planning + implementation roadmap; trajectory revision deferring SPEC-003 v0.2 comparator map to renumbered cycle 021)

linked_artifacts:

- TASK_SNAPSHOT.md (resume pointer; updated FIRST in sync chain per F-001 rule 6)
- specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1 comparator map; INPUT — substrate that v0.2 addendum modifies via NEW file; v0.1 body preserved unchanged)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; INPUT — Delta 5 Composer pool reorganization is the load-bearing reason for the comparator map addendum)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2 ablation plan; INPUT — ABL-v02-4 Composer best-of-N + ABL-v02-5 capability_match measurement inform threat ranking)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; 7 admitted experts inform in-pool tier)
- planning/DREAM3R_V02_CODE_STRUCTURE.md (cycle 020 S2; INPUT for Path C review; 1086 lines)
- planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (cycle 020 S3; INPUT for Path C review; 1226 lines)
- specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (NEW; cycle 021 S3 deliverable)

## One line summary

Launch cycle 021 to (a) author specs/SPEC-20260507-001-dream3r-comparator-map-v02.md as the v0.2 comparator map addendum that closes the v0.2 markdown trio (architecture / ablation plan / comparator map), and (b) activate Path C — spawn other-agent reviewers to actually exercise the per-file/per-task review checklists in cycle 020 deliverables (DREAM3R_V02_CODE_STRUCTURE.md + DREAM3R_V02_IMPLEMENTATION_ROADMAP.md), so the load-bearing handoff surface designed in cycle 020 gets real validation rather than remaining theoretical.

## What user authorized in this session

User dialogue trail (2026-05-07, post cycle 020 closure):

```text
[agent] Summary of state after cycle 020 closure:
        - v0.2 markdown architecture (SPEC-004) + ablation plan
          (SPEC-005) + code structure + implementation roadmap
          all done
        - v0.2 comparator map addendum still open (renumbered
          cycle 021 candidate per DEC-004)
        - 5 next-cycle candidates surfaced (021..025)
        - Path C ("activate other-agent review of cycle 020
          planning artifacts") flagged as orthogonal option
        - Default agent recommendation: cycle 021 = SPEC-003
          v0.2 comparator map addendum + Path C in parallel

[user] "请你推进吧，我们也该开始全面落实了"

       Decoded:
       a) "请你推进吧" = direct authorization to proceed; agent
          decides scope.
       b) "我们也该开始全面落实了" = phase signal: time to start
          comprehensive 落实 (implementation/realization). The
          word 落实 is stronger than 继续 (continue) or 推进
          (push forward) alone — it implies actually USING what
          we've built, not just writing more. Combined with
          "全面" (comprehensive), this signals multi-track push.
       c) Most aligned interpretation given prior agent
          recommendation: launch cycle 021 with combined scope
          = (S3) v0.2 comparator map addendum (markdown trio
          closer) + (S2) Path C review activation (actually
          exercise the cycle 020 review surface). Paper Section
          3+6 rewrite for A+D framing deferred to cycle 022 to
          keep cycle 021 scope cohesive.
```

Evidence label for this DEC: `user-instructed` for "全面落实" intensity (justifies multi-track push); `agent-decided` for combined-scope choice (comparator map + Path C in parallel; subject to user revision); `user-implicit-endorsement` for following agent's prior cycle 020 closure recommendation ("021 + 同步启动路径 C").

## Why this matters

Cycle 020 wrote DREAM3R_V02_CODE_STRUCTURE.md and DREAM3R_V02_IMPLEMENTATION_ROADMAP.md with explicit per-file review surface subsections + per-task pre/post execution checklists, designed for "其他agent审阅修改" (other-agent review/modification). But until another agent actually reads those documents and produces structured review feedback, the review surface is theoretical. Path C activation in this cycle converts theory into measurement: do the checklists work as designed when given to a fresh agent?

Two distinct branches of cycle 021:

```text
S3 (markdown trio closer):
  - SPEC-20260507-001 NEW v0.2 comparator map addendum
  - Reorganizes comparator pool per SPEC-004 Delta 5 (7 admitted
    experts in-pool; VGGT / MapAnything / Kimi-KDA out-of-pool
    with reason; ViT-L backbone out-of-scope; new axes covering
    NSA / DINOv3 / 7-expert pool dimensions)
  - Threat ranking against main-claim A (Verification-as-
    architecture) + D (Heterogeneous best-of-N Composer)
  - Architecture-novel elements with no comparator
  - v0.1 SPEC-003 body preserved unchanged per Discipline rule 5
    (NEW file pattern; v0.1 referenced but not modified)
  - Closes v0.2 markdown trio: architecture (SPEC-004) +
    ablation plan (SPEC-005) + comparator map (SPEC-007 candidate
    ID; this DEC reserves SPEC-20260507-001 as the artifact ID)

S2 (Path C review activation):
  - Spawn 2 sub-agents IN PARALLEL via Agent tool
    Agent A: review DREAM3R_V02_CODE_STRUCTURE.md
            (1086 lines)
            against SPEC-004 v0.2 architecture (six deltas) and
            existing v0.1 code/dream3r/ structure
    Agent B: review DREAM3R_V02_IMPLEMENTATION_ROADMAP.md
            (1226 lines)
            against sibling CODE_STRUCTURE + SPEC-005 v0.2
            ablation plan (9 ABL-v02 for Tier 4 tasks)
  - Each agent produces ≤500-word structured review
  - Findings consolidated in cycle log
  - Review-action items captured (no in-place edits to cycle 020
    artifacts in this cycle; revisions go to cycle 022+ via
    fresh DEC + v0.3 addendum per B-roadmap-F rule)
```

The two branches are independent. S3 markdown writing happens in main agent context; S2 sub-agents run in their own contexts. No cross-contamination. Combined cycle compresses what would otherwise be cycles 021 + (path-C activation cycle) into a single push under user "全面落实" intensity.

## Allowed by this DEC

Cycle 021 may produce, in order (S2 + S3 in parallel):

```text
S1  This DEC + TASK_SNAPSHOT mid-pass anchor                   -> done by this commit (DEC) + sync pass

S2  Path C review activation (TWO sub-agents in parallel)
    Agent A scope:
      - Read planning/DREAM3R_V02_CODE_STRUCTURE.md (1086 lines;
        artifact under review)
      - Read specs/SPEC-20260506-004-dream3r-architecture-v02.md
        (882 lines; v0.2 architecture; six deltas the structure
        must serve)
      - Spot-check 2-3 files in code/dream3r/ to verify v0.1
        module structure assumptions
      - Reference code/dream3r/PLAN.md if needed (substrate)
      - Produce <=500-word structured critical review covering:
        A. Delta-to-file mapping accuracy
        B. Review surface clarity per MODIFIED + NEW file
        C. Missing pieces / dependencies
        D. Honesty calibration of evidence labels
        E. Top 3 actionable issues
    Agent B scope:
      - Read planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md
        (1226 lines; artifact under review)
      - Read planning/DREAM3R_V02_CODE_STRUCTURE.md (1086 lines;
        sibling INPUT)
      - Read specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md
        (991 lines; nine ABL-v02 inform Tier 4 ABL harness tasks)
      - Produce <=500-word structured critical review covering:
        A. Task scoping (size; cohesion; missing/redundant tasks)
        B. Pre/post execution checklist actionability
        C. Dependency DAG correctness
        D. Effort calibration (~250-380 engineering-hours
           inferred — credible?)
        E. Top 3 actionable issues
    Agent type: general-purpose (Agent tool with subagent_type=
    general-purpose; both agents have read-only scope by
    instruction; they produce text findings, no edits)
    Background mode: NO. Reviews need to complete in this session
    so findings can be consolidated in cycle log. Run agents in
    parallel via single message with two Agent tool calls.       -> pending

S3  specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (NEW)
    Section structure:
    - Identity / Approval / Scope of v0.2 comparator map addendum
    - Reading order
    - v0.1 comparator map relationship (citation only;
      v0.1 body NOT modified)
    - v0.2 architecture deltas reference (Delta 1..6 from
      SPEC-004; especially Delta 5 Composer pool)
    - Reorganized comparator pool per Delta 5
        * In-pool tier (7 admitted experts): MASt3R / Fast3R /
          Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R;
          per-expert role in v0.2 main-claim D
        * Out-of-pool tier (deprecated from v0.1): VGGT (too
          heavy) / MapAnything (too heavy) / Kimi Linear / KDA
          (LM-to-3R transfer not pursued); each with explicit
          reason
        * Out-of-scope tier: ViT-L backbone (replaced by
          DINOv3-S per Delta 2)
    - New comparator dimensions introduced by v0.2:
        * NSA-style sparse attention dimension (compare against
          dense attention baselines + alternative sparse
          attention schemes)
        * DINOv3 backbone tier dimension (compare DINOv3-S vs
          DINOv3-B vs alternative ViT-L-class backbones)
        * Composer 7-expert pool dimension (compare against
          single-expert specialists + heterogeneous multi-expert
          systems in adjacent domains)
    - Threat ranking against main-claim A + D
    - Architecture-novel elements with no comparator (carry
      forward from SPEC-003 v0.1 + add v0.2-introduced novelty)
    - Boundaries (markdown only; v0.1 body NOT modified)
    - Linked artifacts
    - Open questions
    - Discipline notes
    - Version history
    Target length: 500-800 lines (Honesty Override permits
    overshoot if needed; will be acknowledged in cycle log)     -> pending

S4  Cycle log + Path C findings consolidation
    cycles/CYCLE-20260507-001.md NEW
    Sections:
    - Cycle 021 subtask board
    - Cycle 021 artifacts produced (DEC-001 + SPEC-001 v0.2
      comparator map + Path C agent reviews)
    - Path C review consolidation:
        * Agent A findings on CODE_STRUCTURE
        * Agent B findings on IMPLEMENTATION_ROADMAP
        * Cross-agent themes (if any)
        * Review-action items for cycle 022+ (NOT acted on in
          cycle 021 per B-roadmap-F)
    - Cycle 021 outcome (closed) + renumbered post-021 trajectory
    - Hard rules carried
    - F-001 / F-002 honoring
    - Honesty Override consummated
    - Resume action when user returns
    - Linked artifacts
    - Version history                                            -> pending

S5  Sync chain (TASK_SNAPSHOT first per F-001 rule 6;
    decision_registry append DEC-20260507-001; WORKFLOW_STATUS
    / RESEARCH_STATE / INDEX line-3 sync + INDEX SPEC-20260507-
    001 row added under specs/ + INDEX latest cycle log pointer
    to CYCLE-20260507-001; final TASK_SNAPSHOT flip to idle)    -> pending
```

## Not allowed by this DEC

```text
1. No code touch. The 2 cycle 021 deliverables (SPEC-20260507-001
   comparator map addendum + Path C reviews) are pure markdown
   output. code/dream3r/ files are READ for review purposes
   (Agent A spot-check) but NOT modified. Server-side
   /hdd3/kykt26/code/dream3r/ untouched.

2. No supersede of SPEC-20260506-003 v0.1 comparator map. v0.2
   addendum lives in NEW file SPEC-20260507-001 per Surgical
   Edits + Discipline rule 5. v0.1 body preserved unchanged.
   Only SPEC-003 Version history tail may receive a v0.2 pointer
   entry (similar to cycle 019 SPEC-002 v0.1 Version history
   v0.2 pointer pattern).

3. No in-place edits to cycle 020 deliverables. DREAM3R_V02_
   CODE_STRUCTURE.md and DREAM3R_V02_IMPLEMENTATION_ROADMAP.md
   are READ by Path C agents for review purposes; NOT modified
   by this cycle. Per B-roadmap-F (no in-place modification of
   review checklists), any acted-on findings go to cycle 022+
   via fresh DEC + v0.3 addendum.

4. No promotion of any task in IMPLEMENTATION_ROADMAP to
   "approved-for-execution" via Path C reviews. Path C agents
   are reviewers, not executors. Their findings are advisory
   for future revision, not authorization for code execution.

5. No checkpoint download / clone / install / GPU run / training
   / KYKT navigation change / frontend implementation / demo
   storyboard promotion past `draft` / teacher-demo readiness
   claim / thesis finalization / retiring of any non-finalist
   track. All carried unchanged from prior DECs.

6. No paper Section 3+6 rewrite for v0.2 main-claim A+D framing
   in cycle 021. That is deferred to renumbered cycle 022 (per
   DEC-004 trajectory revision; this DEC reaffirms cycle 022 =
   paper rewrite).

7. No silent revision of v0.2 main-claim narrowing (A + D
   pillars per DEC-002). Comparator map v0.2 may NOT introduce
   new pillars or re-promote demoted pillars (B / C) or reduce
   E to absent.

8. No Path C agent authorized to write/edit any project file.
   Both sub-agents are read-only by instruction. They produce
   text findings returned to main agent; main agent quotes
   findings into cycle log. If a Path C finding requires file
   modification, that modification is DEFERRED to cycle 022+
   (separate DEC).

9. No re-Read of large files already in main-agent context per
   F-001 rule 1. SPEC-001 v0.1 (~1821 lines), SPEC-002 v0.1
   (~770 lines), SPEC-003 v0.1 (625 lines), SPEC-004 v0.2 (882
   lines), SPEC-005 v0.2 (991 lines), DREAM3R_V02_CODE_STRUCTURE
   (1086 lines), DREAM3R_V02_IMPLEMENTATION_ROADMAP (1226 lines)
   already in main-agent context from prior cycles or main-cycle-
   021 prep — main agent cites by section + line anchor. Path C
   sub-agents have FRESH contexts; they Read what they need.

10. No silent supersede of post-019/post-020 trajectory. Cycle
    021 acts on the trajectory's renumbered cycle 021 (comparator
    map) as planned; the only revision is +Path C activation
    layered on top. Documented honestly in this DEC.
```

## Cycle 021 inputs and not-inputs

```text
INPUTS for SPEC-20260507-001 (comparator map v0.2 addendum):
  - SPEC-20260506-003 v0.1 comparator map (substrate; cited)
  - SPEC-20260506-004 v0.2 architecture (Delta 5 + Delta 2 +
    Delta 3 + Delta 4 inform new comparator dimensions)
  - SPEC-20260506-005 v0.2 ablation plan (ABL-v02-4 + ABL-v02-5
    inform threat ranking)
  - planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (7 admitted
    experts; per-expert capability descriptor)
  - DEC-20260506-002 (v0.2 architecture deltas locked decision;
    out-of-pool reason for VGGT / MapAnything / Kimi-KDA)

INPUTS for Path C reviews:
  - Agent A: planning/DREAM3R_V02_CODE_STRUCTURE.md +
    SPEC-20260506-004 v0.2 architecture + spot-check 2-3 code/
    dream3r/ files + code/dream3r/PLAN.md as substrate
  - Agent B: planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md +
    planning/DREAM3R_V02_CODE_STRUCTURE.md (sibling) +
    specs/SPEC-20260506-005 v0.2 ablation plan

NOT inputs (do NOT Read):
  - Anything under archive/ unless cited specifically
  - source_registry.md / research_unit_registry.md (no per-row
    update in cycle 021)
  - storyboards/ (no storyboard promotion or revision in cycle
    021)
  - Cases/ L2 case cards (no per-card revision in cycle 021)
```

## Hard rules carried (verbatim from prior cycles + AGENT_MASTER_PROMPT.md section 6)

```text
- No reproduction. No checkpoint download. No training. No KYKT
  navigation change. No frontend implementation. No thesis
  finalization. No retiring of any non-finalist track. No demo
  storyboard promotion past `draft`. No teacher-demo readiness
  claim. None of these without explicit user approval in active
  conversation.
- DEC-20260501-004 (Dream3R candidate-not-final) and DEC-
  20260504-002 (no-all-in any single finalist) still in force.
- Cycle 021 is markdown only. Any code touch (whether triggered
  by Path C findings or otherwise) requires a separate DEC +
  per-step micro gates per F-002.
- Surgical Edits (Discipline rule 3): every changed line traces
  to user request, decision memo, or Sync Rule trigger.
  Pre-existing markdown lint warnings on TASK_SNAPSHOT historical
  block + WORKFLOW_STATUS / decision_registry / INDEX table
  separators NOT fixed in this pass per Surgical Edits rule 3.
- Honesty Override (Discipline rule 5): every claim in SPEC-
  20260507-001 carries an evidence label. Path C reviews quoted
  verbatim into cycle log (not paraphrased; not silently
  edited). Trajectory adherence (cycle 021 = comparator map per
  renumbered post-020 trajectory) preserved without silent
  revision.
- F-001 working rules: TASK_SNAPSHOT first in sync chain
  (mid-pass anchor + final flip); no re-Read of in-context
  files; prefer Edit (diff payload) over Write for existing
  files; cap large files in active context at <=2 simultaneously;
  Path C sub-agents have their own contexts and do not consume
  main-agent budget.
- F-002: KYKT 3R model code runs server-side; cycle 021 stays
  local; only Agent A spot-check Reads code/dream3r/ files (these
  are the LOCAL editing copies, not the server execution copies).
```

## Discipline notes

```text
1. Cycle 021 inherits the cycle 019 + cycle 020 NEW-file pattern:
   v0.2 lives in a NEW spec file (SPEC-20260507-001), not as
   in-place edits to v0.1 SPEC-003. Only SPEC-003 Version history
   tail receives a v0.2 pointer entry (cycle 020 declined to
   apply this pattern to PLAN.md because PLAN.md has different
   semantics; SPEC-003 v0.1 is a normal versioned spec, so the
   version-history-tail-pointer pattern applies).

2. Path C review pattern (NEW this cycle): when activating
   another agent to review existing project markdown, the
   protocol is:
   - Sub-agent runs in its own context (no main-agent context
     pollution)
   - Sub-agent has READ-ONLY scope by prompt instruction
     (cannot edit project files)
   - Sub-agent produces structured findings (≤500 words for this
     activation; future activations may revise budget)
   - Main agent quotes findings VERBATIM into cycle log
     (Honesty Override; no silent paraphrase)
   - Findings are advisory; acted-on revisions go to a fresh
     cycle + DEC + v0.3 addendum (per B-roadmap-F rule for
     review-checklist supersede)

3. Combined-cycle compression precedent: cycle 020 combined
   original cycles 021 + 022 from DEC-003 trajectory under user
   "高强度推进". Cycle 021 (this cycle) combines the renumbered
   cycle 021 (comparator map) with a NEW addition (Path C
   activation) under user "全面落实" — same compression precedent,
   different surface. The renumbered post-021 trajectory is
   updated below.

4. Effort estimate honesty: cycle 021 is larger than typical
   markdown cycle. SPEC-20260507-001 target 500-800 lines;
   Path C review consolidation adds ~200-400 lines to cycle log;
   total NEW markdown ~800-1200 lines + sync chain edits.
   Cycle log will record actual line counts honestly per
   Discipline rule 5.

5. Path C agent budget per F-001 rule: each sub-agent's
   context is independent of main agent; main agent's F-001
   budget is for SPEC-20260507-001 writing only. Main agent
   does NOT re-Read inputs already in context (SPEC-003 v0.1 +
   SPEC-004 v0.2 + SPEC-005 v0.2 + COMPOSER_CAPABILITY_
   DESCRIPTORS already cited above).
```

## Renumbered post-021 trajectory

```text
Cycle 021 (in progress; closing this pass):
  v0.2 comparator map addendum (SPEC-20260507-001 NEW) + Path C
  review activation (sub-agent reviews of cycle 020 planning
  artifacts)

Renumbered post-021 trajectory (per this DEC; agent-recommended;
user-revisable):

  022. PAPER_DRAFT_V1.md Section 3 + Section 6 update for v0.2
       main-claim A+D framing (markdown only). PLUS cycle 022
       may absorb Path C review-action items requiring CODE_
       STRUCTURE / IMPLEMENTATION_ROADMAP v0.3 addendum (if
       any surfaced in cycle 021 S2). Cycle launch DEC required.

  023. Cycle 015 G_run resumption (Critic A4 measured anchor;
       paused at S9 done). Server-side execution per F-002.
       Cycle launch DEC + per-step micro gates required.

  024. Capability_match measurement pass per ABL-v02-5 (promotes
       inferred -> measured for 7-expert pool). Server-side
       execution per F-002. Cycle launch DEC + per-ablation
       DEC required.

  025. First T-v02-N task execution authorization (likely
       T-v02-A repo skeleton + config schema scaffold as
       lowest-risk first task; or jump to T-v02-ABL-N if
       measurement is preferred). Cycle launch DEC + per-task
       DEC + per-step micro gates per F-002 required. Reviewer
       authorization protocol must be defined as part of launch
       DEC.

  026. (open) Subsequent T-v02-N task execution OR ABL-v02-N
       execution depending on cycle 025 outcome. Each subsequent
       task / ABL requires its own DEC.
```

Default agent recommendation for cycle 022 launch (revisable):

```text
Option A: cycle 022 = paper Section 3+6 rewrite + Path C v0.3
  addendum acting on cycle 021 review findings (combined cycle).
  Markdown only. Closes post-cycle-020 review loop.

Option B: cycle 022 = paper Section 3+6 rewrite ONLY. Path C
  findings deferred to a later v0.3 addendum cycle if needed.
  Lighter cycle; depends on whether Path C surfaces material
  issues.

Option C: cycle 022 = first code execution authorization
  (jumping to renumbered cycle 025). Higher value if user
  wants to start measuring/implementing; requires DEC + multiple
  per-step gates; server-side; not as clean a starting point.

Surface decision will be informed by Path C review findings
in cycle 021 closure; option A becomes more attractive if
findings surface specific actionable revision items.
```

## Open questions for cycle 021 closure

```text
Q1. Does Path C review surface material issues with cycle 020's
    review-checklist pattern itself (i.e., are pre/post execution
    checklists genuinely actionable or were they aspirational)?
    Answer: emerges from Agent B findings.

Q2. Does Path C review surface miswiring between v0.2 deltas
    and per-file changes (i.e., is CODE_STRUCTURE actually
    correct as a v0.2 implementation map)?
    Answer: emerges from Agent A findings.

Q3. Should comparator map v0.2 addendum extend to a FOURTH
    architecture-novel-elements axis covering "review-pattern
    novelty" (cycle 020's per-file/per-task review checklist
    structure as a contribution beyond architecture)?
    Decision: NOT in cycle 021 scope; review-pattern is
    research workflow contribution, not 3R architecture
    contribution. Re-surface only if user requests in future
    paper-writing cycle.

Q4. If Path C agents surface CRITICAL issues (e.g., a delta
    is wrongly mapped, a task is impossible to execute),
    should cycle 021 close as `done with critical-findings`
    rather than `done`? And should the next cycle be forced
    to address those findings before any other work?
    Decision: Yes for both. If any Path C finding labels itself
    "critical" or "blocking", cycle 021 closes with explicit
    Status: done-with-critical-findings; cycle 022 launch DEC
    must address those findings as S2 before any other scope.
    Honesty Override consummation.
```

## Cycle launch summary (for resume)

```text
date_authorized:    2026-05-07
authorized_by:      user message "请你推进吧，我们也该开始全面
                    落实了"
authorized_scope:   cycle 021 = SPEC-20260507-001 v0.2 comparator
                    map addendum (NEW) + Path C review activation
                    (2 sub-agents in parallel) + cycle log + sync
                    chain. Markdown only.
budget_estimate:    ~800-1200 NEW markdown lines + sync chain
                    edits + 2 sub-agent reviews ≤500 words each
deadline:           single session (2026-05-07)
deferral:           paper Section 3+6 rewrite (cycle 022); v0.3
                    addendum on cycle 020 artifacts (cycle 022 if
                    Path C surfaces actionable items, else later);
                    code execution (cycle 025+); ABL execution
                    (cycle 025+ per-ABL DEC).
```
