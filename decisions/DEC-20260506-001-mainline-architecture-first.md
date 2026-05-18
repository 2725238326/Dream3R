# DEC-20260506-001 mainline redefined: architecture-first

decision_id: DEC-20260506-001

date: 2026-05-06

status: locked

cycle: closes cycle 015 strategic-pause framing; seeds cycle 016 scope

parents:
- DEC-20260501-004 (Dream3R = candidate, not final thesis)
- DEC-20260504-002 (no all-in any single finalist)
- DEC-20260505-005 (cycle 015 launch + Critic L3 pilot scope)

linked_artifacts:
- TASK_SNAPSHOT.md (resume pointer)
- C:\Users\27252\.claude\projects\e--kykt\memory\feedback_dream_mainline_architecture_first.md (cross-session feedback memory)
- specs/SPEC-20260503-001-geometry-critic.md
- specs/SPEC-20260503-002-executive-memory.md
- specs/SPEC-20260503-003-dynamic-object-permanence.md
- specs/SPEC-20260504-001-3r-composer.md
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1)
- planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md (A1-A8)
- planning/ARCHITECTURE_MECHANISM_INTAKE.md
- literature/PAPER_PHASE2_BLUEPRINT.md (now demoted to support artifact)

## One line summary

User redefined Dream's mainline as **architecture-first**: design a new 3R architecture (transformer / SSM / state-space / hybrid) as a markdown spec + ablation plan + comparator map. NOT framework-first paper writing. Cycle 015 L3 measurement work stays paused at S9 done. Cycle 016 = draft Dream3R-the-architecture.

## What user authorized in this session

User message at 2026-05-06: "所以现在我们做的和新模型有啥关系？或者说什么时候能开始推进主线了？"

After agent surfaced a 3-option strategic question (A framework-first / B architecture-first / C train-first) with explicit tradeoffs, user selected:

```text
"B. Architecture-first"
```

Evidence label for this DEC: `user-decided`. The redirect itself is recorded; no architectural claims yet.

## Why this matters (interpretation)

Prior project state had implied framework-first by default — paper Phase 2 blueprint, demo storyboards, L3 pilot for Critic, all framed as the path to a teacher-demo + paper. That framing is consistent with `DEC-20260501-004` (Dream3R candidate not final) but did not actually have user signoff as the mainline. 14 cycles of work happened under this implicit framing without it being explicit.

User's 2026-05-06 redirect makes the strategic choice explicit: the **primary output of Dream is a new 3R architecture proposal**, not a paper about a control-graph framework over existing 3R models. The control-graph framework remains useful as the THEORY behind the architecture; the architecture itself is the artifact.

This is consistent with user-stated preferences captured earlier:
- `RESEARCH_STATE.md` "Research-Mainline Correction": "我们的主线还是研究新的内容" (mainline is researching new content)
- `paradigm/TEACHER_AUDIENCE_PROFILE.md`: research taste = 科研的训练 / 写作技巧 / 创新范式 / 讲好故事 (innovation paradigm + good storytelling)

A new architecture spec IS an innovation paradigm and IS a story (control-graph-as-architecture). The framework-first reading was a sub-interpretation; architecture-first is the parent interpretation.

## Allowed by this DEC

Cycle 016 (and onward) may:

```text
1. Draft Dream3R architecture spec as a NEW markdown artifact:
   what tokens / what state / what attention or SSM cores / what
   read-write protocol / how A1..A8 actions land in concrete layers /
   how the v2.1 cross-spec contract becomes an internal API.

2. Synthesize the 4 finalist specs (Critic / Memory / Permanence /
   Composer) into modules of the architecture, NOT pick one as THE
   architecture. Per DEC-20260504-002 no-all-in still in force.

3. Draft an ablation plan distinguishing load-bearing components
   from optional ones; specify which experiments would falsify the
   architecture if it were trained.

4. Draft a comparator map vs existing 3R architectures: DUSt3R /
   MASt3R / Spann3R / Fast3R / VGGT / MapAnything / CUT3R /
   Mamba-3R / SSM-3R variants. Show what Dream3R does
   architecturally that none of these do.

5. Cite + reuse existing artifacts as INPUTS to the architecture
   spec: the 4 finalist specs, v2.1 cross-spec contract, A1-A8
   action taxonomy, mechanism intake map, frontier source map,
   paper Phase 2 blueprint (now demoted to support artifact).

6. Carry honesty labels: architecture spec sections marked
   `inferred` / `paper-derived` / `speculative` per
   `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5.
```

## Not allowed by this DEC

```text
1. No training. No GPU runs to "test" the architecture. Architecture-
   first authorizes DESIGN + ABLATION PLANNING, not execution. Train-
   first (option C) remains deferred / blocked.

2. No final thesis selection. Dream3R-the-architecture is a candidate
   per DEC-20260501-004; it can still be revised, replaced, or
   merged with another candidate.

3. No retiring of any of the 4 finalist mechanisms. Per
   DEC-20260504-002, the architecture must preserve them as
   composable modules.

4. No new repo clones / installs / checkpoints beyond cycle 015's
   already-done work. The architecture spec is markdown; if any
   reference run is needed, surface a separate gate (probably via
   resuming cycle 015 G_run).

5. No KYKT navigation change. No frontend implementation. No demo
   storyboard promotion past `draft`. No reusable Codex skill
   packaging. No teacher-demo readiness claim.

6. No silent supersede of `DEC-20260501-004` (Dream3R = candidate)
   or `DEC-20260504-002` (no-all-in). Both still apply to the
   architecture work.

7. No retroactive rewriting of the 4 finalist specs, v2.1 contract,
   or any past case card / storyboard / cycle log. Architecture
   spec is a NEW artifact that REFERENCES them; it does not edit
   them in place. (Surgical Edits rule 3.)
```

## Implications for cycle 015

```text
- Cycle 015 stays paused at S9 done. NOT closed. NOT abandoned.
- The L3 infrastructure (test3r conda env on server; launch.py:103
  patch with .cycle015.bak; F-002 server-topology memory; 4 local
  shallow clones) is reusable as evidence anchor for the
  architecture spec's Critic-module section. Not wasted.
- G_run can still be surfaced later if the architecture spec needs
  measured Critic-style verification evidence to anchor a section.
  Until then, no G_run.
- TASK_SNAPSHOT.md "If interrupted, resume from" should now point
  primarily at cycle 016 (architecture spec drafting) rather than
  at cycle 015 G_run.
```

## Cycle 016 launch scope (this DEC seeds it)

```text
S1  This DEC + feedback memory persistence              -> done by this commit
S2  Write Dream3R architecture spec draft (NEW artifact;
    proposed location: specs/SPEC-20260506-001-dream3r-architecture.md
    OR planning/DREAM3R_ARCHITECTURE_DRAFT.md; user-pickable
    location at S2 launch time)                         -> pending
S3  Write Dream3R ablation plan (NEW artifact)          -> pending
S4  Write Dream3R comparator map (NEW artifact OR
    section appended to existing planning/RESEARCH_GRAPH_AND_PAPER_
    START.md; user-pickable)                            -> pending
S5  Sync chain (TASK_SNAPSHOT first; then WORKFLOW_STATUS,
    RESEARCH_STATE, INDEX, decision_registry,
    AGENT_MASTER_PROMPT, README)                        -> pending
```

S2..S5 are deferred to a later session per user "今日进度到此为止". This DEC + feedback memory + TASK_SNAPSHOT.md stamp + Open user decisions block are the only S1 artifacts today. Cycle 016 launch DEC (a separate DEC if needed, OR cycle 016 may launch directly under this DEC depending on user direction at next session) will formalize S2..S5 scope.

## Discipline notes

```text
- Surgical Edits: this DEC + the feedback memory + TASK_SNAPSHOT.md
  stamp are the only NEW artifacts today. No existing spec / case
  card / contract / storyboard / cycle log is rewritten.
- Honesty Override: the redirect itself is `user-decided`; no
  architectural claims yet. Architecture spec drafting (cycle 016
  S2) will carry per-section evidence labels.
- F-001 anti-32MB: TASK_SNAPSHOT.md is updated FIRST in the minimal
  sync; large files in active context capped at <=2; no full-file
  Reads of already-cited content.
- Hard rules (carried from AGENT_MASTER_PROMPT.md): no
  reproduction / no checkpoint download / no training / no KYKT
  navigation change / no frontend implementation / no thesis
  finalization / no retiring of any non-finalist track. All still
  in force; this DEC adds none.
```
