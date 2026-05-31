# Dream Workflow Status

Last updated: 2026-06-01 (bounded residual refinement over frozen StatePrior closed small-positive: correct-state 0.1448/0.1475 on KITTI/ETH3D vs frozen-prior 0.1452/0.1480; shuffle-state 0.1521/0.2467. Current best bounded Dream3R variant is frozen trained StatePrior fusion plus disagreement-bounded residual refinement.)

Last updated: 2026-06-01 (frozen-prior decoder sweep closed scaffold-positive: correct-state 0.1452/0.1480 on KITTI/ETH3D, shuffle-state 0.1525/0.2468; KL=0.01 sensitivity gives the same pattern. Frozen StatePrior preserves causality and prevents joint decoder collapse; next route is bounded refinement over frozen prior with a different refinement mechanism/target, not KL tuning alone.)

Last updated: 2026-05-31 (prior-conditioned ProposalSetDecoder seed7 controls closed NEGATIVE: correct-state does not beat no-state/shuffle and no-state is better on both domains. StatePriorHead remains positive; two-stage prior pretrain/freeze path is now implemented and frozen-prior smoke reproduces 0.1451/0.1480 on KITTI/ETH3D.)

Last updated: 2026-05-31 (StatePrior diagnostic closed: non-core `StatePriorHead` shows Dream state contains usable expert-prior signal. Seed7 correct-state beats best-single on KITTI/ETH3D and beats no-state/shuffle controls; next work should make this prior an explicit ProposalSetDecoder/native-distillation control path.)

Last updated: 2026-05-30 (Dream3R-PD execution started locally: VGGT-Omega deployment inventory / DEC-016 draft and non-core ProposalSetDecoder prototype / trainer / tests landed; 2 local tests passed; server execution gated.)

Last updated: 2026-05-30 (final architecture path selected: Dream3R-PD = Proposal-bank Distilled State-Conditioned 3R. DEC-015 / SPEC-005 / final plan / v09 handoff added; broad route search should stay closed.)

Last updated: 2026-05-30 (v2.2 admission research updated: DEC-014 / SPEC-004 / runbook / v08 handoff switch the first candidate from vanilla VGGT to VGGT-Omega. Vanilla VGGT is baseline/schema ancestor; OVGGT is a separate cache-memory comparator.)

Last updated: 2026-05-30 (model-first milestone reorganization completed: Dream3R is now routed as proposal encoders + Dream state + state-conditioned reconstruction decoder. DEC-013 / SPEC-003 / milestone plan / v07 handoff added; next candidate experts now limited to VGGT-Omega, CUT3R, MonST3R per DEC-014.)

Last updated: 2026-05-30 (ver2.1 4-seed metric refresh completed on BUAA-Server GPU 1: correct state beats no-state and shuffled-state on KITTI/ETH3D abs_rel and patch-oracle gap; temporal/scale proxies remain open training targets. Summary: `runs/stage6_fusion/ver21_metric_refresh/summary.md`.)

Last updated: 2026-05-30 (Dream3R-ver2.0 SCF midterm closure: DEC-20260530-011 accepted bounded state-conditioned multi-expert fusion as the usable model. L0 real-backend guardrail fixed fallback contamination; L1 residual is negative; L2 SCF is positive. New spec: `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md`; new cycle: `cycles/CYCLE-20260530-scf-midterm.md`.)

Last updated: 2026-05-29 (historical two-day SCF convergence handoff corrected; superseded by 2026-05-30 DEC-011/DEC-012.)

Last updated: 2026-05-27 (state-conditioned reconstruction pivot: DEC-20260527-009 + SPEC-20260527-001 created after Stage 6 baseline pathology and user route adjustment. Hard expert selection is now a proposal-prior / diagnostic baseline, not the headline architecture claim. No code change.)

Last updated: 2026-05-22 (cycle 043 architecture-focus round after user re-prioritization "架构是最重要的内容; 开题报告和综述放一边": `code/dream3r/SOTA_FEATURE_MATRIX.md` expanded to family-grouped second pass (W20 plan); `specs/SPEC-20260522-001-dream3r-v05-axes.md` drafted (8 axes A1-A8 covering DINOv3-S backbone / adapter ckpt loading / dynamic_mask proxy → D2 / VGGT + capability_card v2.2 / Test3R Critic-triggered off-path / NSA sliding branch utility / GaussianHead conditional entry deferred / tttLRM A1 sub-action). Both candidate-not-final per DEC-20260501-004. No code change; v0.3 + v0.4 layers byte-identical. Parallel to v0.4 closure round below.) (v0.4 architecture closure round, parallel to the proposal track: `code/dream3r/contracts.py` + `repair.py` + `orchestrator.py` + three new test files added; 24/24 new tests + 130/130 pre-existing tests pass; `ARCHITECTURE_V04_STATUS.md` records the per-axis checklist and explicit stub/fallback/proxy list. v0.3 code is byte-identical to before this round. The proposal track (cycle 042 closeout) is preserved below.)

## Current Phase

```text
Phase 1.5: Research Workflow Deployment
```

## Current Mode

```text
Two parallel tracks at a checkpoint:
  Track A (Dream3R v0.3 code, architecture-first mainline per DEC-20260506-001):
    server-verified on synthetic + first KITTI real-data smoke; W1-W18
    implementation present (W17-W18 tensor-contract level only); MASt3R +
    Spann3R real adapters loaded; Fast3R real path blocked on `omegaconf`
    in dream3r conda env; CUT3R / MoGe-2 / DepthAnything / Test3R remain
    deterministic fallback.
  Track B (3R-mix Chinese survey, separate workspace Dream/3R-mix/):
    18-page LaTeX manuscript; recommended deliverable
    `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`.
    **Wound down 2026-05-14 to arXiv-only route (route C, no venue
    submission)**; README rewritten as canonical entry, Typst legacy
    files marked deprecated, release checklist appended to
    NEW_CHAT_HANDOFF.md. Internal terms deliberately absent from
    manuscript surface.

No new reproduction or heavy install authorized.
No real-data training authorized.
No 3DGS renderer install authorized.
Paper writing is now a separate workstream (Track B) but still support, not
primary; Track A architecture-first mainline holds.
Frontend implementation remains delegated to Gemini CLI / designated frontend agent.
```

## Active Thesis Candidate

```text
Dream3R: Geometry-Governed State and Test-Time Reasoning for Long-Context 3R
```

Status:

```text
candidate, not final
```

## Active Workflow Decision

Deploy Dream as a markdown-first research pipeline:

```text
Source -> Mechanism -> 3R Translation -> Research Unit -> Score -> Decision -> Plan -> Implementation
```

## Canonical Agent Prompt

```text
E:\kykt\Dream\AGENT_MASTER_PROMPT.md
```

Use this prompt when handing Dream work to Codex, another agent, or a subagent.

## Canonical Frontend Handoff Prompt

```text
E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md
```

Use this prompt when preparing KYKT frontend design work for Gemini CLI.

## Active Workstreams

| Workstream | Status | Next artifact |
|---|---|---|
| Research workflow | active | `paradigm/RESEARCH_WORKFLOW.md` |
| Collaboration roadmap | active | `handoff/COLLABORATION_ROADMAP.md` |
| Data model | active | `paradigm/RESEARCH_DATA_MODEL.md` |
| Source registry | active; cycle 013 mining pass added SRC-2026-009..015 (7 new rows: MapAnything / Julian Ost AAAI-2026 driving permanence / tttLRM / awesome-dust3r curated index / DUSt3R-MASt3R-VGGT MVS evaluation / NTIRE 2026 / VGGT) | `registry/source_registry.md` |
| Research unit registry | seeded | `registry/research_unit_registry.md` |
| Decision registry | seeded | `registry/decision_registry.md` |
| Cycle logs | active | `cycles/CYCLE-20260522-001.md` (cycle 043 done; W20 SOTA Feature Matrix family-grouped second pass at `code/dream3r/SOTA_FEATURE_MATRIX.md` + v0.5 axes spec at `specs/SPEC-20260522-001-dream3r-v05-axes.md` with 8 axes A1-A8; markdown only; v0.3 + v0.4 code byte-identical; both candidate-not-final; sync chain applied to INDEX.md + WORKFLOW_STATUS.md + TASK_SNAPSHOT.md); `cycles/CYCLE-20260517-003.md` (cycle 042 done; Dream3R 开题报告 final revision + PDF compilation + advisor submission packaging — proposal track functionally closed); `cycles/CYCLE-20260517-001.md` (cycle 040 done; Dream3R 开题报告 § 5 + § 7 + § 8 dual-draft 起草 + STYLE_CONTRACT 43→48 rows + 5 corrective edits + sync chain); `cycles/CYCLE-20260516-004.md` (cycle 039 done; Dream3R 开题报告 § 3 + § 6 dual-draft 起草 + STYLE_CONTRACT 41→43 rows + 7 corrective edits per side on G4 negation-context + sync chain); `cycles/CYCLE-20260516-003.md` (cycle 038 done; Dream3R 开题报告 § 4 研究方案 / Dream3R v0.3 架构 dual-draft 起草 + STYLE_CONTRACT 22→41 rows + sync chain); `cycles/CYCLE-20260516-002.md` (cycle 037 done; Dream3R 开题报告 § 2 国内外研究现状 dual-draft 起草 + STYLE_CONTRACT §6 sync log + sync chain); `cycles/CYCLE-20260516-001.md` (cycle 036 done; advisor submission packaging + Dream3R 开题报告 dual-draft kickoff + risk register v1.2 + sync chain); `cycles/CYCLE-20260515-001.md` (cycle 035 done; survey-driven markdown deliverables + 4 risk register additions + sync chain); `cycles/CYCLE-20260511-001.md` (cycle 034 done; KITTI real-data smoke + Mamba/Gaussian + Track B 3R-mix kickoff); `cycles/CYCLE-20260510-001.md` (cycle 033 done; W1-W16 v0.3 architecture advancement); `cycles/CYCLE-20260508-008.md` (cycle 031 local Memory v0.3 P0 scaffold) |
| Dream3R v0.3 code (Track A) | active; server-verified at `/hdd3/kykt26/code/dream3r/`; first KITTI real-data smoke on `2011_09_26_drive_0001_sync_02` window pair (pointmap L2 20.47 = integration evidence, not trained quality) | `code/dream3r/REVIEW_PROMPT.md`, `code/dream3r/RECENT_PROGRESS.md`, `code/dream3r/NEXT_PHASE_ROADMAP.md` |
| Dream3R v0.4 architecture closure | **active**; closed loops shipped 2026-05-22: typed `contracts.py` + `RepairExecutor` (action 0/1/2/3 with `max_repair_attempts=1`) + `V04Pipeline` orchestrator + 24 new contract tests; 130 pre-existing tests still pass; v0.3 code unchanged. Stub/fallback list lives in `ARCHITECTURE_V04_STATUS.md`: DINOv3-S backbone, MoGe-2 / DepthAnything / Test3R adapter checkpoints, and dynamic-mask-as-final-D2 all explicitly NOT claimed | `ARCHITECTURE_V04_STATUS.md`, `code/dream3r/contracts.py`, `code/dream3r/repair.py`, `code/dream3r/orchestrator.py`, `code/dream3r/tests/test_v04_*.py` |
| Dream3R W20 SOTA Feature Matrix | **active**; cycle 043 family-grouped second pass shipped 2026-05-22: 8 family sections (Direct pairwise / Many-view streaming / Memory primitive comparators / Monocular priors / Test-time + Critic / Attention + state recurrence / Permanence + dynamic / Rendering + 4D); 30+ external methods mapped to Dream3R modules with explicit `real-wired (no local ckpt)` / `deterministic fallback` / `stub` / `mechanism integrated` / `contract-only` / `comparator-only` / `named, not in registry` status; Gap Report identifies OnlineX + AnchorSplat as roadmap drafting artifacts and MoGe-2 SRC row as missing; supersedes the 2026-05-10 first pass while preserving its differentiation list + evidence map | `code/dream3r/SOTA_FEATURE_MATRIX.md`, cross-links `ARCHITECTURE_V04_STATUS.md`, `composer_experts/method_profiles.py`, `registry/source_registry.md` |
| Dream3R v0.5 axes spec | **draft**; cycle 043 deliverable, candidate-not-final per DEC-20260501-004: 8 axes A1-A8 (A1 DINOv3-S backbone real / A2 per-adapter ckpt loading / A3 Permanence dynamic_mask_proxy → D2 promotion + CR-2 v2.2 / A4 VGGT + capability_card v2.2 / A5 Test3R Critic-triggered off-path + new action code / A6 NSA sliding branch utility on longer KITTI / A7 GaussianHead conditional main-forward entry — explicitly kept deferred / A8 tttLRM long-context A1 sub-action design). Each axis has explicit `closes_iff` + required actions + dependencies + non-promises + evidence label. v0.5 additive to v0.4 by default. Each axis closure requires its own DEC | `specs/SPEC-20260522-001-dream3r-v05-axes.md` |
| Dream3R state-conditioned reconstruction pivot | **active direction**; DEC-20260527-009 demotes hard expert selection from headline claim to proposal-prior / diagnostic-baseline role. New architecture target: persistent Memory / AnchorBank / NSA / Permanence / Critic state directly conditions the final pointmap via fusion/correction. Adds A9 real-backend guardrail, A10 multi-expert proposal bank, A11 long-sequence state objective. No code change in this pass | `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md`, `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md`, `cycles/CYCLE-20260527-state-conditioned-reconstruction.md` |
| Dream3R-ver2.0 SCF midterm closure | **accepted**; bounded state-conditioned multi-expert fusion is the current usable model. L0 real-backend guardrail passes; L1 residual head is negative; L2 SCF beats best single on KITTI and is marginal positive on ETH3D, near oracle. Composer is proposal prior / scheduler, not the headline architecture | `decisions/DEC-20260530-011-scf-midterm.md`, `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md`, `cycles/CYCLE-20260530-scf-midterm.md`, `code/dream3r/scf_head.py`, `code/dream3r/scripts/build_scf_cache.py`, `code/dream3r/scripts/train_scf_head.py` |
| Dream3R-ver2.1 state-training + metrics | **4-seed control executed**; correct state beats no-state and shuffled-state on abs_rel and patch-oracle gap. Temporal/scale proxies are not yet a win, so they become explicit training targets. Core edits remain gated by a future DEC | `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md`, `planning/DREAM3R_VER21_STATE_TRAINING_PLAN.md`, `decisions/DEC-20260530-012-ver21-state-training-metrics.md`, `cycles/CYCLE-20260530-ver21-architecture-refinement.md` |
| Dream3R model-first milestone reorganization | **accepted**; Dream3R is now defined as proposal encoders + Dream state + reconstruction decoder. Current bank remains MASt3R/Fast3R/Spann3R; next admission candidates are VGGT-Omega/CUT3R/MonST3R only; native Dream3R comes through decoder distillation, not blind expert search | `decisions/DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md`, `specs/SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md`, `planning/DREAM3R_MILESTONE_REORG_20260530.md`, `handoff/ARCHITECTURE_V07_MODEL_REORG_AGENT_PROMPT.md`, `cycles/CYCLE-20260530-milestone-reorg-model-roadmap.md` |
| Dream3R v2.2 VGGT-Omega admission research | **accepted for planning**; first v2.2 admission target is now VGGT-Omega, with vanilla VGGT kept as baseline/schema ancestor and OVGGT kept as a cache-memory comparator. No checkpoint/download/server run authorized by this doc pass | `decisions/DEC-20260530-014-v22-vggt-omega-admission.md`, `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md`, `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md`, `handoff/ARCHITECTURE_V08_V22_ADMISSION_AGENT_PROMPT.md`, `cycles/CYCLE-20260530-v22-admission-research.md` |
| Dream3R-PD final architecture selection | **accepted final path**; Dream3R-PD = proposal teachers + Dream state + proposal-set decoder + native decoder distillation with proposal dropout. This is the route to execute; fallback final prototype remains SCF if decoder/distillation gates fail | `decisions/DEC-20260530-015-final-architecture-selection.md`, `specs/SPEC-20260530-005-dream3r-pd-final-architecture.md`, `planning/DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md`, `handoff/ARCHITECTURE_V09_FINAL_SELECTION_AGENT_PROMPT.md`, `cycles/CYCLE-20260530-final-architecture-selection.md` |
| Dream3R-PD execution start | **local prototype + first server diagnostic closed**; VGGT-Omega inventory and execution DEC draft written; non-core ProposalSetDecoder + cached-proposal trainer + tests added. Server ProposalSetDecoder v0/v1 did not prove state causality. Follow-up StatePriorHead diagnostic proves the Dream state has expert-prior signal, so next execution should inject a learned prior into the decoder/distillation path rather than scaling unstructured state concatenation | `planning/VGGT_OMEGA_DEPLOYMENT_INVENTORY.md`, `decisions/DEC-20260530-016-vggt-omega-execution-draft.md`, `decisions/DEC-20260530-017-proposal-set-decoder-prototype.md`, `decisions/DEC-20260531-019-state-prior-diagnostic.md`, `code/dream3r/proposal_set_decoder.py`, `code/dream3r/state_prior_head.py`, `cycles/CYCLE-20260531-state-prior-diagnostic.md` |
| Dream3R StatePrior diagnostic | **accepted; seed7 closed**; correct-state beats best-single on KITTI/ETH3D and beats no-state/shuffle controls on existing SCF caches. This is evidence for state-conditioned expert prior, not a final model head | `decisions/DEC-20260531-019-state-prior-diagnostic.md`, `cycles/CYCLE-20260531-state-prior-diagnostic.md`, `code/dream3r/state_prior_head.py`, `code/dream3r/scripts/train_state_prior_head.py`, `code/dream3r/scripts/run_state_prior_sweep.sh`, `code/dream3r/tests/test_state_prior_head.py` |
| Dream3R prior-conditioned decoder | **closed negative; two-stage path implemented**; explicit StatePrior-style MLP prior branch added to ProposalSetDecoder, but seed7 joint controls show correct-state does not beat no-state/shuffle. Trainer now supports `--state-prior-checkpoint --freeze-state-prior --prior-kl-weight`; frozen-prior smoke reproduces StatePrior's positive result before refinement training | `decisions/DEC-20260531-020-prior-conditioned-decoder.md`, `cycles/CYCLE-20260531-prior-conditioned-decoder.md`, `code/dream3r/proposal_set_decoder.py`, `code/dream3r/scripts/train_proposal_set_decoder.py`, `code/dream3r/scripts/run_prior_conditioned_decoder_sweep.sh`, `code/dream3r/scripts/run_frozen_prior_decoder_sweep.sh`, `code/dream3r/tests/test_proposal_set_decoder.py` |
| Dream3R frozen-prior decoder | **closed scaffold-positive**; loading/freezing DEC-019 StatePrior preserves state causality and beats shuffle-state on both domains. KL=0.1 and 0.01 both preserve the prior but do not improve beyond StatePriorHead, so next route is a different bounded refinement mechanism/target over the frozen prior | `decisions/DEC-20260601-021-frozen-prior-decoder-sweep.md`, `cycles/CYCLE-20260601-frozen-prior-decoder-sweep.md`, `code/dream3r/scripts/run_frozen_prior_decoder_sweep.sh` |
| Dream3R bounded residual refinement | **closed small-positive**; zero-initialized residual offset bounded by local proposal disagreement improves frozen-prior from 0.1452/0.1480 to 0.1448/0.1475 and keeps shuffle-state at 0.1521/0.2467. This is the current best bounded Dream3R model variant | `decisions/DEC-20260601-022-bounded-prior-refinement.md`, `cycles/CYCLE-20260601-bounded-prior-refinement.md`, `code/dream3r/proposal_set_decoder.py`, `code/dream3r/scripts/train_proposal_set_decoder.py`, `code/dream3r/scripts/run_frozen_prior_decoder_sweep.sh` |
| Dream3R two-day SCF convergence handoff | **superseded by DEC-011 result**; keep as historical prompt shape, but next agents should start from the updated prompt and continue ver2.0/L4, not recreate the pre-run plan | `handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md`; historical plan `planning/DREAM3R_2DAY_SCF_MIDTERM_PLAN.md` |
| Dream3R v0.5 iteration test plan | **ready for execution planning**; 2026-05-22 plan converts v0.4 closure + v0.5 axes into concrete testing sprints: S0 local v0.4 edge hardening, S1 A6 KITTI 8-10 window memory evidence, S2 A2 staged real-backend adapter closure, S3 A5 Test3R off-path, S4 A3 dynamic-mask promotion design, with server runbook outline and evidence schema. Planning artifact only; no v0.5 axis closed | `planning/DREAM3R_V05_ITERATION_TEST_PLAN.md`, `handoff/ARCHITECTURE_V05_AGENT_START_PROMPT.md` |
| 3R-mix Chinese survey (Track B) | **wound down 2026-05-14 (route C: arXiv-only)**; 2026-05-14 quality pass added CroCo + MASt3R mechanism + §10 failure modes + `fig:timeline`; 2026-05-15 prose naturalization pass rewrote 10 paragraphs to drop LLM-style enumerated structures, parallel patterns and workflow vocabulary; 18 A4 pages, 44 references, 6 figures (4 TikZ + 2 paper-Fig.1 composites), 5 booktabs tables, 0 LaTeX errors / 0 warnings; deliberately decoupled from Dream/KYKT internal vocabulary | `Dream/3R-mix/README.md`, `Dream/3R-mix/NEW_CHAT_HANDOFF.md`, `Dream/3R-mix/main.tex`, `Dream/3R-mix/deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` |
| Experiment planning | active; local v0.3 P0 scaffold now exists and ABL-memory-0 passed, but later ablations still require separate DEC + gate | `experiments/prototypes/memory_v03_p0/outputs/summary_go_no_go.md` |
| Agent master prompt | active | `AGENT_MASTER_PROMPT.md` |
| C2 Memory v0.3 | active architecture addendum + P0 plan + reviewed ablation addendum + local P0 scaffold. ABL-memory-0 passed as a fixture/logging gate only; C2 memory quality remains unvalidated | `specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md` + `planning/MEMORY_V03_DESIGN_STUDY.md` + `planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md` + `specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md` + `planning/MEMORY_V03_ABLATION_REVIEW.md` + `experiments/prototypes/memory_v03_p0/README.md` |
| Research content roadmap | active | `paradigm/RESEARCH_CONTENT_ROADMAP.md` |
| Multi-track research canvas | active; cycle 008.5 four-finalist + no-all-in section appended | `planning/MULTI_TRACK_RESEARCH_CANVAS.md` |
| Research graph / paper start | active; cycle 008.5 F6 row note + Next Concrete Artifact supersede applied | `planning/RESEARCH_GRAPH_AND_PAPER_START.md` |
| Branch comparison matrix | filled first comparative pass (cycle 004); cycle 008.5 supersede annotations applied | `planning/BRANCH_COMPARISON_MATRIX.md` |
| Branch shortlist decision surface | user approved option B (cycle 008) | `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` |
| Architecture mechanism intake | first-pass active | `planning/ARCHITECTURE_MECHANISM_INTAKE.md` |
| Action taxonomy / proxy metrics | first compact pass (cycle 006); cycle 008.5 A5 split + supersede annotations applied | `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` |
| Proxy case-card template | active form; first portfolio populated in cycle 009 (6 cards: 3 Critic + 3 Composer, paper-derived) | `templates/proxy_case_card.md` + `cases/` |
| Finalist mechanism spec template | populated for three finalists in cycle 008 | `templates/finalist_mechanism_spec.md` |
| Geometry Critic finalist spec | draft (L1); L2 case cards drafted in cycle 009 (paper-derived under v1 contract); D3 first teacher demo target = Critic per cycle 011 DEC-20260505-001; demo storyboard `STORY-20260505-001-critic.md` drafted in cycle 011 (status: draft only; showing not authorized) | `specs/SPEC-20260503-001-geometry-critic.md` + `cases/CASE-20260504-CRITIC-01..03.md` + `storyboards/STORY-20260505-001-critic.md` |
| Executive Memory finalist spec | draft (L1); L2 case cards drafted in cycle 010 under v2 contract (3 cards across MonST3R / Spann3R / MASt3R regimes); CR-3 producer side closes cycle-009 CRITIC-03 forward-reference null | `specs/SPEC-20260503-002-executive-memory.md` + `cases/CASE-20260504-MEMORY-01..03.md` |
| Dynamic Object Permanence finalist spec | draft (L1); L2 case cards drafted in cycle 010 under v2 contract (3 cards: MonST3R primary + MASt3R static control + synthetic identity-validation); CR-2 producer side closes cycle-009 gap G1 | `specs/SPEC-20260503-003-dynamic-object-permanence.md` + `cases/CASE-20260504-PERMANENCE-01..03.md` |
| 3R Composer finalist spec | draft (L1); L2 case cards drafted in cycle 009 (paper-derived); CASE-COMPOSER-03 v2 row promoted to canonical per DEC-20260504-004; CASE-COMPOSER-04 KYKT-metadata-derived added in cycle 012 (advances G2 inferred -> inferred-with-real-inventory-anchor; G2 NOT closed); CASE-COMPOSER-05 added cycle 014 as VGGT capability-card gap addendum (per-card gap, no v2.2 contract revision); demo storyboard `STORY-20260505-004-composer.md` drafted cycle 012 | `specs/SPEC-20260504-001-3r-composer.md` + `cases/CASE-20260505-COMPOSER-01..05.md` + `storyboards/STORY-20260505-004-composer.md` |
| Cross-spec signal contract | **v2.1 active** (per DEC-20260505-001): additive revision over v2 — adds "Forward-reference null protocol" subsection formalizing the pattern exercised by cycle-009 + cycle-010 cards; v2 substance unchanged (alpha = 0.5 inferred; signal owner table; CR-1..CR-6; cost_adjusted_match; route_regret cost-typed). v1 + v2 prose preserved. Cycle 011 G5 closed by this revision; cycle 010 G4 closed-by-documentation under the protocol. v2 -> v3 candidates 8x8 grid partition + identity_consistency threshold pinning deferred. | `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` + `decisions/DEC-20260505-001-cycle-011-launch-and-d3-demo-target.md` |
| Literature guidance board | v1 active; post-cycle-013 SPINE refresh fold-in done. PAPER_RELATED_WORK_SKELETON.md upgraded cycle 013 to prose draft. Cycle 014 added PAPER_PHASE2_BLUEPRINT.md as a claim-safe paper-writing plan; G7 advanced to blueprint anchor but not closed | `literature/INDEX.md` + four `literature/SPINE_*.md` + `literature/CRITICAL_NOTES.md` + `literature/PAPER_RELATED_WORK_SKELETON.md` + `literature/PAPER_PHASE2_BLUEPRINT.md` |
| Work risk register | v1.2 active (cycle 036 +3 proposal-cycle rows R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1 appended after v1.1 cycle 035 +4 cross-spec rows R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1); consolidates per-spec + cross-spec + proposal-cycle risks | `planning/WORK_RISK_REGISTER.md` |
| Dream3R 开题报告 dual-draft (Track C) | **完成 (functionally closed)**; cycles 036-042 (7 cycles) 累计 ~19300 内 + ~15000 外 字; §1-§9 all complete; PDF compiled (263 KB); advisor cover note + submission record ready; STYLE_CONTRACT v1 closed 50 rows; remaining action = user actual submission + optional revision cycle 043 | `planning/proposal_dream3r/` (OUTLINE + STYLE_CONTRACT + DRAFT_INTERNAL + DRAFT_EXTERNAL + deliverables/ + references.bib) |
| Track B advisor submission packaging | active; cycle 036 packaging + cycle 037 SHA256 pre-fill — Chinese cover note (~600 字, G2 vocab-clean) + submission record with recipient / channel / submitted_at slots (pdf_sha256 已于 2026-05-16 预填 = A0763DB7AB7A1E8E1427D4DCC8CB62BC15F94F3F2D915AD0BFBB235CC99C64B0) + Track A relationship internal meta (not delivered to advisor); actual submission action (email / IM / portal / offline) is post-cycle user action | `3R-mix/deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` + `SUBMISSION_RECORD_2026-05-16.md` + `RELATION_TO_TRACK_A_2026-05-16.md` |
| Demo storyboard template | active form; all 4 finalists now have draft storyboards (Critic from cycle 011 = D3 first demo target; Memory + Permanence + Composer from cycle 012); none authorized for showing; promotion to `approved-for-showing` requires a separate per-finalist DEC | `templates/demo_storyboard.md` + `storyboards/STORY-20260505-001..004.md` |
| Teacher audience profile | placeholder; awaits user input to unblock D3 | `paradigm/TEACHER_AUDIENCE_PROFILE.md` |
| Source mining (cycle 005 pass) | complete for visual priors, depth priors, active perception, event VO | `sources/FRONTIER_SOURCE_MAP.md` (Cycle 005 Source Mining Pass section) |
| Workspace reorganization (cycle 006) | complete; topical subdirectories + archive/ + INDEX.md | `cycles/CYCLE-20260502-006.md` |
| Research & code discipline (cycle 007) | active rulebook for synthesis behavior and Dream-driven code | `paradigm/RESEARCH_CODE_DISCIPLINE.md` |
| Finalist shortlist approval (cycle 008) | user-approved option B; three finalist specs drafted | `decisions/DEC-20260503-002-finalist-shortlist-approval.md` |
| Composer finalist upgrade (cycle 008.5) | user-approved; SPEC-20260504-001 drafted; cross-spec contract formalized | `decisions/DEC-20260504-001-composer-finalist-upgrade.md` |
| No-all-in posture (cycle 008.5) | user-locked; D3 deferred until cycle 009 case-card data + audience profile | `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` |
| Frontend handoff prompt | active | `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md` |
| KYKT backend integration | support only | no backend service changes yet |
| KYKT frontend integration | downstream only | no UI work unless research content and support contract exist |

## Blocked Until User Decision

- any new reproduction, server run, model run, or heavy install
- any new checkpoint download
- C2 v0.3 server integration, model import, or any ablation beyond ABL-memory-0 without a separate DEC
- KYKT Dream page or navigation change
- Codex direct frontend implementation
- major Gemini CLI frontend redesign instruction
- final thesis selection
- deepening any single thesis branch as the default path
- reusable Codex skill packaging

## Recommended Next User Decision

Cycle 043 architecture-focus recommendation (cycle 043 closed 2026-05-22; user re-prioritized 2026-05-22 "架构是最重要的内容; 开题报告和综述放一边; 平台更新放到日程"; Track A architecture-first mainline confirmed primary; Track B/C parked):

```text
Cycle 043 completed W20 SOTA Feature Matrix expansion +
v0.5 axes spec drafting in markdown-only mode (no code change;
v0.3 + v0.4 layers byte-identical). Deliverables:
  - code/dream3r/SOTA_FEATURE_MATRIX.md (family-grouped 2nd pass)
  - specs/SPEC-20260522-001-dream3r-v05-axes.md (8 axes A1-A8)
Both candidate-not-final per DEC-20260501-004. v0.5 is additive
to v0.4 by default; v0.3 main forward stays byte-identical
unless an axis closure DEC says otherwise.

Next admissible direction under current priority (architecture > platform;
proposal + survey parked):

  A. User reviews SOTA matrix + v0.5 axes spec, selects
     which axes to promote first via DEC. Highest-leverage
     candidates per the spec's Recommended Sequencing table:
       Sprint 1 (server, F-002): A1 DINOv3-S, A2 per-adapter
                                   ckpt loading, A4 VGGT adapter,
                                   A6 NSA sliding branch utility
       Sprint 2 (server, F-002): A3 dynamic_mask promotion,
                                   A5 Test3R Critic off-path
       Deferred: A7 GaussianHead main-forward (renderer DEC),
                 A8 tttLRM A1 sub-action (W25 plan)

  B. Markdown-only architecture follow-ups (no server, no DEC needed):
       - W22 visualization pack (uses existing JSON; matplotlib)
       - W26 STREAM3R_RELATION.md design writeup
       - W21 ablation table reorganization
       - resolve OnlineX / AnchorSplat roadmap drafting artifacts
       - add MoGe-2 SRC row to source_registry.md

  C. Platform / KYKT integration scoping (per user 2026-05-22
     "后续平台更新也得放到日程里"). Scoping only; KYKT
     navigation + Codex frontend edits remain blocked per
     existing rules.

  D. User executes Track C 开题报告 submission (cycle 042
     packaging ready since 2026-05-17) — out of current priority
     but not closed.

  E. User executes Track B survey submission (cycle 037 SHA256
     pre-filled) — out of current priority but not closed.

  F. Pause and reassess.
```

Track A architecture-first remains the mainline per DEC-20260506-001 and is now also confirmed primary by the 2026-05-22 user re-prioritization. The Dream3R 开题报告 (Track C) and 3R-mix survey (Track B) deliverables are both packaged at cycle 042 / cycle 037 closeout state; submission is the user's post-cycle action whenever they choose to re-open those tracks.

2026-05-30 immediate next handoff:

```text
Use handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md to start the next agent.
It now starts from DEC-20260530-011 / DEC-20260530-012 and
SPEC-20260530-001 / SPEC-20260530-002. The next task is not "invent an
architecture"; it is metric refresh and trained-state evaluation for SCF.
```

2026-05-30 model-first handoff:

```text
Use handoff/ARCHITECTURE_V07_MODEL_REORG_AGENT_PROMPT.md for any agent that
will decide expert admission, reconstruction decoder design, or native
Dream3R roadmap. The target is not more router search; it is proposal-bank
Dream3R -> trained-state Dream3R -> native decoder distillation.
```

2026-05-30 v2.2 admission handoff:

```text
Use handoff/ARCHITECTURE_V08_V22_ADMISSION_AGENT_PROMPT.md for the next
VGGT-Omega deployment research pass. It starts with repo/dependency/checkpoint
inventory and an execution DEC draft; it does not authorize checkpoint
download, install mutation, or server run by itself.
```

2026-05-30 final architecture handoff:

```text
Use handoff/ARCHITECTURE_V09_FINAL_SELECTION_AGENT_PROMPT.md for final-path
execution. The selected route is Dream3R-PD; next agents should run the
VGGT-Omega inventory, ProposalSetDecoder, trained-state projection, and
distillation gates instead of reopening architecture selection.
```

2026-05-27 route update:

```text
Hard expert selection is no longer the post-midterm headline. The accepted
ver2.0 architecture is state-conditioned reconstruction through SCF:
L0 real-backend guardrail -> L1 single-expert state-to-depth wire (negative)
-> L2 multi-expert proposal-bank fusion (positive/ver2.0) -> L3 long-sequence
coherence metrics -> L4 state retraining. Composer remains as proposal prior /
diagnostic baseline.
```

Still blocked on user approval:

- final thesis selection
- moving any finalist from L2 proxy evidence to L3 prototype code
- reproducing any candidate model
- training or fine-tuning
- downloading any new checkpoint
- changing KYKT navigation
- Codex directly editing KYKT frontend code
- packaging a reusable Codex skill
- declaring teacher-demo readiness
- discarding any non-finalist track (Cross-Modal, Active Perception)
- **showing any of the 4 demo storyboards** (Critic / Memory / Permanence / Composer; all `draft`; promotion to `approved-for-showing` requires a separate per-finalist DEC)
- **closing any v0.5 axis A1-A8** (each axis closure requires its own DEC referencing SPEC-20260522-001 `closes_iff` clauses)

## Guidance File Sync Rule

When Dream creates or promotes a workflow artifact, update the relevant guidance files in the same pass. **`TASK_SNAPSHOT.md` updates first in this chain** so that a sync interrupted partway through still leaves a valid resume pointer:

- `TASK_SNAPSHOT.md` (highest-authority resume pointer; updated first; see its own "Update protocol" section for transitions)
- `AGENT_MASTER_PROMPT.md`
- `README.md`
- `WORKFLOW_STATUS.md`
- `RESEARCH_STATE.md`
- current cycle log under `cycles/`
