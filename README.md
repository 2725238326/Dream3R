# Dream Research Workspace

Last updated: 2026-05-22 (v0.4 architecture closure round: `code/dream3r/contracts.py` + `repair.py` + `orchestrator.py` + 3 new test files + `ARCHITECTURE_V04_STATUS.md` added; 24 new + 130 existing tests pass; v0.3 code byte-identical. See `ARCHITECTURE_V04_STATUS.md` for the per-axis checklist and explicit stub/fallback/proxy list.)

Earlier last updated: 2026-05-08 (cycle 031: C2 Memory v0.3 local P0 scaffold created; ABL-memory-0 passed as fixture/logging validity gate; cycle 024 scaffold remains engineering baseline only)

## Purpose

`Dream` is the research workspace for the next-stage KYKT 3R / visual-geometry agenda.

The goal is to build an **architecture-first 3R research engine** that can continuously absorb:

- new 3R papers and model families
- new neural architectures such as SSM/Mamba, memory models, residual attention, test-time compute, continual learning, and RL
- useful GitHub projects that have not yet been applied to 3R
- demo ideas that can be integrated into the KYKT app

The workspace should eventually produce:

1. a large master research prompt
2. research skill/rules for repeated research-agent use
3. a teacher-facing demo and proposal blueprint
4. candidate model/app integration plans for KYKT

Mainline priority:

```text
new 3R / spatial-intelligence research content first;
backend, KYKT app, and frontend are supporting layers.
```

Highest-authority resume pointer (read FIRST on every session start; if status is `in_progress` or `blocked`, do not start new work):

```text
E:\kykt\Dream\TASK_SNAPSHOT.md
```

Canonical agent entry prompt (read after `TASK_SNAPSHOT.md`; lists `TASK_SNAPSHOT.md` as mandatory-load item 1):

```text
E:\kykt\Dream\AGENT_MASTER_PROMPT.md
```

Canonical frontend design handoff prompt:

```text
E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md
```

Quick navigation index:

```text
E:\kykt\Dream\INDEX.md
```

## Current Direction

Primary direction:

```text
Architecture-first 3R research, with demo and KYKT app integration as required output surfaces.
```

Current mechanism focus:

```text
C2 Memory v0.3: replace GRU/vector AnchorBank/NSA-label as the research
center with state-token recurrence + explicit spatial memory + bus-gated
write policy. The current planning chain is:
planning/MEMORY_V03_DESIGN_STUDY.md ->
specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md ->
planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md ->
specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md ->
planning/MEMORY_V03_ABLATION_REVIEW.md ->
planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md ->
experiments/prototypes/memory_v03_p0/README.md.
```

The current strategy is **not** to prematurely choose one method such as Mamba-3R, Event-DUSt3R, or SplatBridge-4D.

Instead, Dream should first build a systematic research engine that can compare and synthesize:

- Memory / State models
- 3R model composition
- Test-time reasoning and self-correction
- Continual / lifelong spatial learning
- Cross-modal and new sensor extensions
- System demo paths that can surprise a teacher while staying feasible

## Directory Map

Root-level files (entry points):

- `TASK_SNAPSHOT.md`: **read first.** Highest-authority resume pointer (current task id, subtask board, status, `If interrupted, resume from` block, recent failure modes). If its status is `in_progress` or `blocked`, do not start new work.
- `README.md`: this file.
- `INDEX.md`: compact total index for humans and agents; start here when navigating.
- `AGENT_MASTER_PROMPT.md`: canonical operating prompt for future Dream agents; contains the mandatory load protocol (lists `TASK_SNAPSHOT.md` as item 1).
- `WORKFLOW_STATUS.md`: current workflow phase, active workstreams, blocked decisions, and recommended next user decision.
- `RESEARCH_STATE.md`: current decisions, assumptions, open questions, and cycle history.

Subdirectories:

- `paradigm/`: how Dream operates (paradigm, workflow, data model, rules draft, content roadmap, cross-spec signal contract, teacher audience profile placeholder).
- `planning/`: active research-planning artifacts (graph, branch matrix, shortlist surface, mechanism intake, action taxonomy, multi-track canvas, thesis stress test, minimal demo candidates, work risk register, C2 Memory v0.3 design study, C2 Memory P0 prototype plan, C2 Memory ablation review, C2 Memory P0 execution DEC template).
- `sources/`: source mining artifacts (`FRONTIER_SOURCE_MAP.md`).
- `units/`: Research Units, scoring, reproduction readiness.
- `handoff/`: collaboration roadmap and frontend handoff prompt for Gemini CLI.
- `logs/`: question log and future running logs.
- `archive/`: historical / superseded documents (Phase 1 artifacts, early prompt drafts).
- `cycles/`: per-cycle research logs.
- `decisions/`: decision memos that require commitment or deferral.
- `experiments/`: experiment plans and explicitly authorized local prototypes. Cycle 031 added `prototypes/memory_v03_p0/` for the local P0 fixture/logging gate.
- `literature/`: literature guidance board (curated reading order, deconfusion notes, paper-related-work skeleton); not a duplicate inventory.
- `specs/`: finalist mechanism specs and architecture addenda, including current C2 Memory v0.3 addendum and Memory v0.3 ablation addendum.
- `storyboards/`: teacher demo storyboards (one per finalist demo target; created via `templates/demo_storyboard.md`; drafting does NOT authorize showing).
- `registry/`: lightweight indexes for sources, research units, and decisions.
- `templates/`: reusable forms (source card, research unit, decision memo, cycle log, experiment plan, frontend design handoff, proxy case card, finalist mechanism spec, demo storyboard).

Key files by subdirectory:

- `paradigm/RESEARCH_PARADIGM.md`: operating paradigm, research loop, evidence ladder, user-discussion gates.
- `paradigm/RESEARCH_WORKFLOW.md`: source-to-implementation workflow.
- `paradigm/RESEARCH_DATA_MODEL.md`: schema for sources, mechanisms, units, decisions, experiments.
- `paradigm/RESEARCH_SKILL_RULES_DRAFT.md`: evolving rules for a project skill and future Codex skill.
- `paradigm/RESEARCH_CODE_DISCIPLINE.md`: behavior rules for research synthesis and Dream-driven code (adapted from Karpathy's CLAUDE.md observations + a Dream-native honesty override).
- `paradigm/RESEARCH_CONTENT_ROADMAP.md`: research-content-first roadmap.
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`: formal contract for read-only / handoff signals between finalist specs (v1 covers Critic / Memory / Permanence / Composer).
- `paradigm/TEACHER_AUDIENCE_PROFILE.md`: placeholder file for the user to populate; gates D3 (first teacher demo target).
- `planning/MULTI_TRACK_RESEARCH_CANVAS.md`: multi-branch comparison canvas.
- `planning/RESEARCH_GRAPH_AND_PAPER_START.md`: graph-based research method and paper scaffold.
- `planning/BRANCH_COMPARISON_MATRIX.md`: branch-level comparison matrix.
- `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md`: user decision surface for choosing 2-3 branches.
- `planning/ARCHITECTURE_MECHANISM_INTAKE.md`: branch-neutral intake map.
- `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md`: compact A1-A8 action taxonomy and P1-P8 proxy protocols.
- `planning/DREAM3R_THESIS_STRESS_TEST.md`: Dream3R / GEM-3R candidate stress test.
- `planning/MINIMAL_DEMO_CANDIDATES.md`: teacher-demo candidate analysis.
- `planning/WORK_RISK_REGISTER.md`: consolidated cross-spec risk view (per-spec risks aggregated; cross-spec risks like contract drift, annotation budget overflow, numbering reconciliation).
- `sources/FRONTIER_SOURCE_MAP.md`: verified and pending source map.
- `units/RESEARCH_UNIT_BANK.md`: structured Dream Research Units.
- `units/IDEA_SCOREBOARD.md`: score table for candidate ideas.
- `units/REPRODUCTION_READINESS_MATRIX.md`: repo-level smoke-test and KYKT integration readiness notes.
- `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md`: canonical prompt and boundary for Gemini CLI / frontend implementation agents.
- `handoff/COLLABORATION_ROADMAP.md`: human-agent collaboration path and near-term deployment sequence.
- `logs/QUESTION_LOG.md`: interview history and next questions.
- `archive/PHASE1_RESEARCH_PLAN.md`, `archive/PHASE1_EXECUTION_LOG.md`, `archive/PHASE1_DECISION_MEMO.md`: Phase 1 historical artifacts.
- `archive/MASTER_RESEARCH_PROMPT_DRAFT.md`: superseded by `AGENT_MASTER_PROMPT.md`.

## Working Loop

Use this loop after each discussion:

1. Update `RESEARCH_STATE.md` with decisions.
2. Update `logs/QUESTION_LOG.md` with the question/answer trail.
3. Update `paradigm/RESEARCH_PARADIGM.md` when the operating model or decision gates change.
4. Refine `AGENT_MASTER_PROMPT.md` when the operating prompt, load protocol, phase, or decision gates change.
5. Refine `paradigm/RESEARCH_SKILL_RULES_DRAFT.md` when we learn a reusable rule.
6. Later, split stable rules into:
   - a project-local version under `E:\kykt\Dream`
   - a reusable Codex skill

## Current Operating Mode

Dream starts with a balanced two-track plan:

```text
Breadth Map + Minimal Demo
```

The breadth track discovers and scores architecture mechanisms. The demo track keeps one small teacher-facing proof path alive so the work stays concrete.

Current operational phase:

```text
Phase 1.5: Research Workflow Deployment
```

This means:

- no model reproduction yet
- no heavy checkpoint downloads yet
- no KYKT app navigation changes yet
- run research-content and thesis-validation cycles first
- use backend/app/frontend work only as support for the research

Current preliminary thesis candidate:

```text
Dream3R: Geometry-Governed State and Test-Time Reasoning for Long-Context 3R
```

This is not a final commitment. The current stress-test reframe is:

```text
GEM-3R: Geometry-Governed Executive Memory for 3R
```

GEM-3R is a proposed branch inside Dream, not a selected final thesis. The current process is to compare multiple branches before deepening any one direction.

## Non-Negotiables

- Keep the work grounded in 3R / visual geometry, not generic AI trend collection.
- Favor architecture-level novelty over pure application packaging.
- Require some path to a convincing demo.
- Require some path to KYKT app integration.
- Keep engineering cost controlled unless a specific experiment justifies going heavier.
- Separate evidence from speculation.
- Avoid claiming a method works before a minimal experiment or defensible proxy exists.
- Do not move from planned experiment to actual reproduction without a user decision.
- Do not implement KYKT frontend design work in Codex by default; prepare a Gemini CLI handoff prompt unless the user explicitly asks Codex to edit frontend code.
