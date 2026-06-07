# Dream Research Workspace

Last updated: 2026-06-08 (Context compaction anchor added at `handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md`. Read it after `TASK_SNAPSHOT.md` to recover the full current state: v1.1 usable model, v1.0 fallback, VGGT/Qwen/Foundation3R status, frozen core, validation evidence, and next priorities.)

Last updated: 2026-06-07 (Tonight usable Dream3R model package added: `v1.1-rc1` in `code/dream3r/release_v11.py`, documented at `release/USABLE_MODEL_V1_1.md`, verified locally and on BUAA-Server. It routes KITTI to v1.0-rc1 and ETH3D to VGGT-Omega-expanded SCF: KITTI/ETH3D `0.1448/0.0570`.)

Last updated: 2026-06-07 (Foundation3R VGGT feature student added and gated: real VGGT-Omega aggregator features are cached for KITTI/ETH3D 50+50, `input_mode=vggt_features` now defaults to teacher-only loss, and GPU1 teacher-only 20e gives state `0.3237/0.1424`, no-state `0.3260/0.1489`, shuffle `0.3246/0.1330`. This proves VGGT features help versus scratch, but state causality is not established, so it is experimental and not official.)

Last updated: 2026-06-07 (Foundation3R scratch-student diagnostic closed negative: contract/cache/training scaffolds are usable, but scratch student 20e/50e GPU1 diagnostics stay far behind dense teacher and state controls do not separate. Stop unchanged scratch sweeps; next proposal-free route is a pretrained-visual-representation student with the same no-proposal/no-teacher-inference contract.)

Last updated: 2026-06-07 (Foundation3R training-entry smoke closed positive: `train_foundation3r.py` added, local/server tests pass, and BUAA-Server GPU1 1-epoch smoke on the 50+50 dense cache runs with proposal/teacher inference disabled. Next is the 20-epoch state/no-state/shuffle gate.)

Last updated: 2026-06-07 (Foundation3R 50+50 real dense teacher cache gate closed positive: KITTI 50/50 and ETH3D 50/50 windows, failures 0, fallback 0, GT/state present, proposal leak audit clean. Next is `train_foundation3r.py`.)

Last updated: 2026-06-06 (Foundation3R Sprint 0/1 scaffold-positive: proposal-free image-to-pointmap contract, dense teacher cache builder, local/server tests, mock cache smoke, and real VGGT-Omega KITTI/ETH3D 1-window dense teacher cache smokes are complete. Next is 50+50 real dense teacher cache.)

Last updated: 2026-06-06 (Foundation3R proposal-free execution plan added at `planning/DREAM3R_FOUNDATION3R_PROPOSAL_FREE_PLAN_20260606.md`: separate release and foundation lines, lock proposal-free inference contract, then build VGGT-Omega dense teacher cache before writing new training code.)

Last updated: 2026-06-06 (Proposal-free AbsRel/capacity gate closed negative: trainer now supports `teacher_absrel_weight` and larger decoder args, but GPU1 gate20 remains state `0.3326/0.4058` versus teacher `0.1360/0.1470`, with no meaningful state/control separation. Stop shallow proposal-free head sweeps.)

Last updated: 2026-06-06 (Proposal-free teacher distillation gate closed negative: stripped teacher cache + `teacher_weight` training are implemented, but GPU1 gate20 remains far from teacher target and state does not beat no-state. Next proposal-free work must change backbone/pretraining, not retune the same shallow head.)

Last updated: 2026-06-06 (Proposal-free route started: `code/dream3r/proposal_free_3r_decoder.py` and `code/dream3r/scripts/train_proposal_free_3r.py` add a clean `image tokens + Dream state -> pointmap` contract with no proposal inputs. GPU1 gate20 is negative, so this is a scaffold for dense teacher distillation/pretraining, not a model claim.)

Last updated: 2026-06-06 (Unified domain-conditional gate passed locally and on BUAA-Server: KITTI state/no-state/shuffle `0.1448/0.1553/0.1521`, ETH3D state/no-state/shuffle `0.0570/0.0583/0.0598`; `promotable_to_official=true`. This is the v1.1 promotion candidate, while `v1.0-rc1` remains the current official package until a deliberate version switch.)

Last updated: 2026-06-06 (Canonical architecture entrypoint added at `ARCHITECTURE.md`; machine-readable status map added at `release/ARCHITECTURE_STATUS.json`. Use these first to separate official v1.0-rc1, experimental domain-conditional VGGT, and rejected/side lanes.)

Last updated: 2026-06-06 (Domain-conditional VGGT teacher optimization evaluated: KITTI keeps v1.0-rc1 `0.1448`, ETH3D uses VGGT-expanded state path `0.0570`, a 61.36% ETH3D gain vs RC. This passes domain-wise controls but is not official until a unified domain-conditional rerun. See `DEC-20260606-039`.)

Last updated: 2026-06-06 (Training verification sweep closed: full local tests `273 passed, 2 skipped`; BUAA-Server GPU1 training/architecture subset `37 passed`; 1-epoch GPU1 smokes passed for StatePrior, ProposalSetDecoder frozen-prior, NativeStudent, and ImageStateStudent.)

Last updated: 2026-06-06 (Dream3R official architecture wrapper added at `code/dream3r/release_candidate.py`; use `build_dream3r_release_candidate()` as the importable v1.0-rc1 architecture API. This fills the main code-surface gap between release docs and decoder/training scripts.)

Last updated: 2026-06-06 (Dream3R formal version package added: `release/OFFICIAL_VERSION.md`, `release/ARCHITECTURE_V1_0_RC.md`, and `code/dream3r/scripts/verify_release_candidate.py`. The official version is `v1.0-rc1`, frozen-StatePrior + bounded residual, KITTI/ETH3D `0.1448/0.1475`.)

Last updated: 2026-06-06 (NativeStudentDecoder objective optimization gate closed: dropout-consistency plus temporal/scale proxy losses are implemented, locally/server tested, and GPU1 gate20-complete. Correct-state remains causal at `0.1451/0.1480` with zero fallback contamination but does not beat the RC `0.1448/0.1475`, so frozen-StatePrior + bounded residual remains the release candidate. See `decisions/DEC-20260606-038-native-student-objective-gates.md`.)

Last updated: 2026-06-06 (Dream3R fast module-completion and optimization plan added at `planning/DREAM3R_FAST_MODULE_COMPLETION_OPTIMIZATION_PLAN_20260606.md`; first recommended optimization is NativeStudentDecoder dropout-consistency loss with correct/no-state/shuffle controls.)

Last updated: 2026-06-06 (Dream3R implementation module map added at `planning/DREAM3R_IMPLEMENTATION_MODULE_MAP_20260606.md`; use it to understand each module, what is claimable, and where to continue fast.)

Last updated: 2026-06-06 (Dream3R release candidate packaging advanced with external-facing method one-pager, method figure, result tables, presentation outline, and publish checklist. RC remains frozen-StatePrior + bounded residual `0.1448/0.1475`; VGGT-Omega and Qwen remain non-RC lanes. See `release/METHOD_ONEPAGER.md`, `release/METHOD_FIGURE.md`, `release/RESULT_TABLE.md`, and `release/PUBLISH_CHECKLIST.md`.)

Last updated: 2026-06-05 (Dream3R release candidate selected and packaged: frozen-StatePrior + bounded residual `0.1448/0.1475`. VGGT-Omega passed real smoke and oracle admission but failed release state-control on KITTI, so it remains an optional teacher lane. See `release/DREAM3R_RC_CARD.md`, `release/REPRODUCE.md`, and `release/VERIFY_REPORT.md`.)

Last updated: 2026-06-04 (VGGT-Omega one-window real-backend smoke admitted on BUAA-Server GPU1 after user-provided checkpoint upload. See `decisions/DEC-20260604-035-vggt-omega-admission-runner.md` and `runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json`.)

Last updated: 2026-06-04 (Qwen semantic Critic-prior gate closed diagnostic-negative on BUAA-Server: geometry-only hard-window F1 0.9211, Qwen real+geometry F1 0.8947, disabled+geometry F1 0.9211. Qwen remains offline annotation/diagnostic only. See `decisions/DEC-20260604-034-qwen-semantic-critic-prior-gate.md`.)

Last updated: 2026-06-03 (Qwen held-out calibrated controller gate closed diagnostic-negative: leave-one-group-out calibration on 50 Qwen v2 windows gives oracle 0.1489, real 0.1813, shuffle 0.1776, disabled 0.2365. Real beats disabled but loses to shuffle, so no Router/Critic promotion. See `decisions/DEC-20260603-033-qwen-heldout-calibrated-controller.md`.)

Last updated: 2026-06-03 (Qwen controller v2 repair closed weak-positive: cause-derived risk floors and route-priority repair make real Qwen beat disabled and marginally beat shuffle, but `promotable=false` remains. Fresh v2 dry-run: oracle 0.1489, real 0.1750, shuffle 0.1759, disabled 0.2365. See `decisions/DEC-20260603-032-qwen-controller-v2-feature-policy-repair.md`.)

Last updated: 2026-06-03 (Qwen3-VL-2B 50-window controller gate closed negative: strict schema passed 50/50, but real/shuffle/disabled dry-run all scored 0.2365 with Fast3R-only routes versus oracle 0.1489. The current Qwen policy is not promotable to Router/Critic training. See `decisions/DEC-20260603-031-qwen3vl2b-50win-controller-gate.md`.)

Last updated: 2026-06-03 (Qwen3-VL-2B weight staging completed: BUAA-Server weights and isolated smoke runtime are ready, and GPU1 5-window KITTI semantic-label smoke passed strict schema 5/5. See `decisions/DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md`.)

Last updated: 2026-06-03 (Dream3R V11 Qwen semantic-controller integration added locally: KITTI/ETH3D manifest builder and Router/Critic dry-run evaluator compare real/shuffle/disabled VLM semantic controls; mock dry-run is positive but `promotable=false`. See `decisions/DEC-20260603-029-qwen-semantic-controller-integration.md`.)

Last updated: 2026-06-03 (Dream3R V11 semantic label-cache gate implemented locally: strict JSON mock backend tests pass, mock smoke schema report written, Qwen inference blocked because weights are not staged and server Transformers is too old. See `decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md`.)

Last updated: 2026-06-03 (Dream3R V11 VLM semantic-controller research plan added. Qwen3-VL-2B-Instruct is scoped as an offline semantic risk labeler for Router/Critic/state/teacher scheduling, not as a geometry backend. See `planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md`.)

Last updated: 2026-06-02 (Dream3R usability gate updated: image-state U1 ran and failed quality controls; current usable bounded baseline remains 0.1448/0.1475. VGGT-Omega one-window smoke script is ready, public code is staged on BUAA-Server, but real admission is blocked on the approved checkpoint. See `decisions/DEC-20260602-025-image-state-native-student-u1.md` and `decisions/DEC-20260602-026-vggt-omega-admission-preflight.md`.)

Last updated: 2026-06-02 (native student decoder/distillation gate executed on BUAA-Server GPU1: native gate is executable and state-causal but metric-flat versus bounded frozen-StatePrior refinement; bounded refinement remains current best baseline. See `decisions/DEC-20260602-024-native-student-decoder-gate.md`.)

Last updated: 2026-06-02 (architecture acceleration prompt added: use `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md` to push native student decoder/distillation or gated teacher admission instead of small residual-head tweaks.)

Last updated: 2026-05-30 (Dream3R-PD local execution start: VGGT-Omega deployment inventory / DEC-016 draft and non-core ProposalSetDecoder prototype / trainer / tests added. See `decisions/DEC-20260530-017-proposal-set-decoder-prototype.md`.)

Last updated: 2026-05-30 (final architecture path selected: Dream3R-PD = Proposal-bank Distilled State-Conditioned 3R. See `decisions/DEC-20260530-015-final-architecture-selection.md`, `specs/SPEC-20260530-005-dream3r-pd-final-architecture.md`, and `planning/DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md`.)

Last updated: 2026-05-30 (v2.2 admission research switched first candidate to VGGT-Omega. See `decisions/DEC-20260530-014-v22-vggt-omega-admission.md`, `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md`, and `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md`.)

Last updated: 2026-05-30 (model-first milestone reorganization: Dream3R is now proposal encoders + Dream state + state-conditioned reconstruction decoder; next expert candidates now limited to VGGT-Omega/CUT3R/MonST3R per DEC-014. See `planning/DREAM3R_MILESTONE_REORG_20260530.md`.)

Last updated: 2026-05-30 (ver2.1 4-seed metric refresh completed: correct state beats no-state and shuffled-state on KITTI/ETH3D abs_rel and patch-oracle gap; temporal/scale targets remain open. See `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md`.)

Last updated: 2026-05-30 (Dream3R-ver2.0 SCF midterm closure: accepted bounded state-conditioned multi-expert fusion; see `decisions/DEC-20260530-011-scf-midterm.md` and `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md`.)

Last updated: 2026-05-29 (historical two-day SCF convergence handoff corrected; superseded by 2026-05-30 DEC-011/DEC-012.)

Last updated: 2026-05-27 (state-conditioned reconstruction pivot: hard expert selection is demoted from headline claim to Composer-as-proposal-prior / diagnostic baseline. New architecture addendum: `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md`; decision: `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md`.)

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

Current architecture entrypoint:

```text
E:\Dream3R\ARCHITECTURE.md
```

Current compressed handoff:

```text
E:\Dream3R\handoff\CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
```

Canonical agent entry prompt (read after `TASK_SNAPSHOT.md`; lists `TASK_SNAPSHOT.md` as mandatory-load item 1):

```text
E:\kykt\Dream\AGENT_MASTER_PROMPT.md
```

Canonical frontend design handoff prompt:

```text
E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md
```

Current architecture acceleration handoff:

```text
E:\Dream3R\handoff\ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md
```

Current proposal-free Foundation3R plan:

```text
E:\Dream3R\planning\DREAM3R_FOUNDATION3R_PROPOSAL_FREE_PLAN_20260606.md
```

Current VLM semantic-controller handoff:

```text
E:\Dream3R\handoff\ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
```

Current VLM semantic controller gates:

```text
E:\Dream3R\decisions\DEC-20260603-028-vlm-semantic-label-cache-gate.md
E:\Dream3R\decisions\DEC-20260603-029-qwen-semantic-controller-integration.md
E:\Dream3R\decisions\DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md
E:\Dream3R\code\dream3r\scripts\build_vlm_semantic_labels.py
E:\Dream3R\code\dream3r\scripts\build_vlm_window_manifest.py
E:\Dream3R\code\dream3r\scripts\eval_vlm_controller_dryrun.py
E:\Dream3R\runs\vlm_semantic_controller\qwen3vl2b_smoke\schema_report.json
E:\Dream3R\runs\vlm_semantic_controller\qwen3vl2b_smoke\mock_controller_dryrun.json
E:\Dream3R\runs\vlm_semantic_controller\qwen3vl2b_real_smoke\schema_report_5win_t320.json
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
Post-midterm Dream3R-ver2.0: state-conditioned multi-expert fusion (SCF).
Composer / hard expert selection is a proposal prior and diagnostic baseline,
not the headline architecture. The current usable model fuses real Fast3R /
MASt3R / Spann3R proposal pointmaps with confidence, memory.fused_context,
and conflict/reliability signals.

The C2 Memory v0.3 planning chain remains the Memory substrate:
planning/MEMORY_V03_DESIGN_STUDY.md ->
specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md ->
planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md ->
specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md ->
planning/MEMORY_V03_ABLATION_REVIEW.md ->
planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md ->
experiments/prototypes/memory_v03_p0/README.md.

The current route-adjustment addendum is:
specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md.

The accepted ver2.0 closure spec is:
specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md.

The current ver2.1 refinement spec is:
specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md.

The current model-first roadmap is:
specs/SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md.

The current v2.2 admission runbook is:
planning/DREAM3R_V22_ADMISSION_RUNBOOK.md.

The selected final architecture plan is:
planning/DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md.

The latest ver2.1 server summary is:
BUAA-Server:/hdd3/kykt26/code/dream3r/runs/stage6_fusion/ver21_metric_refresh/summary.md.

The current architecture acceleration handoff is:
handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md.

The latest execution result is:
decisions/DEC-20260602-024-native-student-decoder-gate.md.
```

The latest architecture promotion result is:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
status: pass
target: v1.1 promotion candidate
official package still: v1.0-rc1
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
- `handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md`: startup prompt for the next agent to start from DEC-011 / ver2.0 SCF and plan L4 trained-state + temporal-metric work without reopening broad architecture exploration.
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
