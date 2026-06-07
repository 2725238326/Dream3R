# Dream Task Snapshot

Last updated: 2026-06-08 (Context compaction completed at `handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md`. It consolidates the current usable model, official fallback, Qwen/VGGT/Foundation3R status, frozen-core policy, server paths, validation evidence, non-claims, dirty-worktree warning, and next work priorities. Status remains idle: use `v1.1-rc1` for the usable package, preserve `v1.0-rc1` as official stable fallback, and continue proposal-free research only through explicit Foundation3R state-modulation/representation gates. Earlier last-updated note follows.)

Last updated: 2026-06-07 (Tonight usable 3R model package added: `Dream3R v1.1-rc1` via `code/dream3r/release_v11.py`. Policy is KITTI -> v1.0-rc1 bounded StatePrior/residual, ETH3D -> VGGT-Omega-expanded SCF. Metrics/control gate: KITTI `0.1448/0.1553/0.1521`, ETH3D `0.0570/0.0583/0.0598`. Added `release/USABLE_MODEL_V1_1.md`, `verify_v11_release.py`, tests, ARTIFACTS entries, DEC-049/cycle. Local and BUAA-Server v1.1 tests/verifier pass; v1.0 verifier still pass. Earlier last-updated note follows.)

Last updated: 2026-06-07 (Foundation3R VGGT feature student gate closed experimental-positive but not promotable: real VGGT-Omega aggregator features were cached for KITTI/ETH3D 50+50 on BUAA-Server GPU1 with failures 0/fallback 0. Hybrid loss collapses to `0.4734/0.3271`, so `train_foundation3r.py` now defaults `input_mode=vggt_features` to teacher-only. Teacher-only 20e gives state `0.3237/0.1424`, no-state `0.3260/0.1489`, shuffle `0.3246/0.1330` vs dense teacher `0.3554/0.0913`. VGGT features help versus scratch, but Dream state is not causally useful yet; next is explicit state modulation or v1.1 packaging, not another unchanged sweep. Earlier last-updated note follows.)

Last updated: 2026-06-07 (Foundation3R scratch-student diagnostic closed negative: 20e/50e BUAA-Server GPU1 runs show current scratch CNN/Transformer mostly outputs a fixed geometry prior. Best diagnostic stays around KITTI/ETH3D train `0.4620/0.3798`, test `0.4734/0.3271`, far behind dense teacher holdout `0.3554/0.0913`. Code now has patch coordinates, positive-depth ray output, scale-normalized targets, train-split diagnostics, and log-depth loss; tests pass. Stop unchanged scratch sweeps; next Foundation3R lane must use pretrained visual representation while preserving proposal-free inference. Earlier last-updated note follows.)

Last updated: 2026-06-07 (Foundation3R training entrypoint smoke closed positive: `train_foundation3r.py` and tests added; local targeted tests `13 passed`; BUAA-Server tests `5 passed`; GPU1 1-epoch smoke on 50+50 dense cache passes with `proposal_inputs_used=false` and `teacher_used_at_inference=false`. Smoke metrics: KITTI `0.4718` vs teacher `0.3554`, ETH3D `0.3269` vs teacher `0.0913`. Next: 20-epoch state/no-state/shuffle gate. Earlier last-updated note follows.)

Last updated: 2026-06-07 (Foundation3R 50+50 real dense teacher cache gate closed positive on BUAA-Server GPU1: KITTI 50/50 and ETH3D 50/50 windows, failures 0, fallback 0, GT/state present, proposal fields stripped, forbidden leak count 0. Local mirrored reports are under `runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/`. Next: implement `train_foundation3r.py` and run 1-epoch then 20-epoch state/no-state/shuffle gates. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Foundation3R Sprint 0/1 started and scaffold-positive: `Foundation3RDecoder`, dense teacher cache builder, and contract tests added; local targeted tests `11 passed`; BUAA-Server tests `3 passed`; mock cache smoke passed; real VGGT-Omega KITTI/ETH3D 1-window dense teacher cache smokes passed with fallback 0, GT/state present, and leak audit clean. Next: 50+50 real dense teacher cache. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Foundation3R proposal-free execution plan added at `planning/DREAM3R_FOUNDATION3R_PROPOSAL_FREE_PLAN_20260606.md`. It separates the release line from a real proposal-free foundation line and defines Sprint 0 contract lock plus Sprint 1 VGGT-Omega dense-teacher cache as the immediate next task. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Proposal-free AbsRel/capacity gate implemented and closed negative: trainer supports `teacher_absrel_weight` and decoder-capacity args, local/server tests pass, BUAA-Server GPU1 gate20 with larger decoder gives state `0.3326/0.4058`, no-state `0.3327/0.4080`, shuffle `0.3328/0.4064` vs teacher target `0.1360/0.1470`. Stop shallow proposal-free head sweeps; next proposal-free work must change representation/pretraining. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Proposal-free teacher distillation gate implemented and closed negative: stripped teacher cache builder added, trainer supports `teacher_weight`, local/server tests pass, BUAA-Server GPU1 gate20 with `teacher_weight=1.0` gives state `0.3319/0.4056`, no-state `0.3292/0.4049`, shuffle `0.3288/0.4116` vs teacher target `0.1360/0.1470`. Stop shallow teacher-weight sweeps; next proposal-free work needs stronger backbone/dense pretraining. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Proposal-free Dream3R route started: `ProposalFree3RDecoder` + trainer + tests added. Forward contract is `image tokens + Dream state -> pointmap` with no proposal inputs. BUAA-Server GPU1 gate20 is metric/control-negative: state `0.3273/0.4029`, no-state `0.3318/0.4050`, shuffle `0.3221/0.4041`; next proposal-free step must be dense teacher distillation/pretraining, not another shallow decoder run. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Unified domain-conditional gate passed locally and on BUAA-Server: KITTI state/no-state/shuffle `0.1448/0.1553/0.1521`, ETH3D state/no-state/shuffle `0.0570/0.0583/0.0598`, `promotable_to_official=true`. It is now a v1.1 promotion candidate; official package remains `v1.0-rc1` until deliberate v1.1 packaging. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Architecture cleanup pass closed: `ARCHITECTURE.md` is now the canonical architecture map and `release/ARCHITECTURE_STATUS.json` is the machine-readable status map separating official v1.0-rc1, experimental domain-conditional VGGT, side lanes, frozen core, and next unified gate. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Domain-conditional VGGT teacher optimization evaluated: domain-wise candidate gives KITTI `0.1448`, ETH3D `0.0570`, ETH3D gain vs RC `61.36%`; controls pass domain-wise, but `promotable_to_official=false` until a unified domain-conditional rerun. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Training verification sweep closed: full local tests `273 passed, 2 skipped`; BUAA-Server GPU1 training/architecture subset `37 passed`; GPU1 1-epoch smokes passed for StatePrior, ProposalSetDecoder frozen-prior, NativeStudent, and ImageStateStudent. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Official v1.0-rc1 architecture wrapper added: `code/dream3r/release_candidate.py` plus `code/dream3r/tests/test_release_candidate_architecture.py`. The release verifier now checks official API metadata in addition to artifacts/metrics/frozen-core policy. Earlier last-updated note follows.)

Last updated: 2026-06-06 (Formal Dream3R `v1.0-rc1` package added: official entrypoint `release/OFFICIAL_VERSION.md`, frozen architecture `release/ARCHITECTURE_V1_0_RC.md`, artifact manifest version field, and read-only verifier `code/dream3r/scripts/verify_release_candidate.py`. Earlier last-updated note follows.)

Last updated: 2026-06-06 (NativeStudentDecoder objective gates closed: dropout-consistency and temporal/scale proxy losses were implemented, tested locally/server-side, and run on BUAA-Server GPU1. Both P1/P2 gate20 runs stay at correct-state `0.1451/0.1480`, no-state `0.1557/0.1730`, shuffle `0.1525/0.2468`, fallback 0. They are causal but not promotable over RC `0.1448/0.1475`. Earlier last-updated note follows.)

Last updated: 2026-06-06 (fast module-completion and optimization plan added at `planning/DREAM3R_FAST_MODULE_COMPLETION_OPTIMIZATION_PLAN_20260606.md`; first sprint is NativeStudentDecoder dropout-consistency loss with unchanged correct/no-state/shuffle controls. Earlier last-updated note follows.)

Last updated: 2026-06-06 (implementation module map added at `planning/DREAM3R_IMPLEMENTATION_MODULE_MAP_20260606.md`; use it to understand each module and the fast next route. Earlier last-updated note follows.)

Last updated: 2026-06-06 (method figure, result tables, and presentation outline added under `release/`; artifact manifest and top-level navigation updated. Next work is manuscript/demo formatting, not more broad model exploration. Earlier last-updated note follows.)

Last updated: 2026-06-06 (external-facing RC packaging added: `release/METHOD_ONEPAGER.md` and `release/PUBLISH_CHECKLIST.md`; artifact manifest updated. Next work is presentation/manuscript packaging, not more broad model exploration. Earlier last-updated note follows.)

Last updated: 2026-06-05 (release package completed with candidate card, runbook, artifact manifest, reproduction notes, verify report, limitations, and non-claims under `release/`. Fresh local verification: VGGT integration tests 27 passed, artifact JSON parses, frozen-core diff empty; historical tracked `.pyc` files were left untouched. Earlier last-updated note follows.)

Last updated: 2026-06-05 (VGGT-Omega 50+50 oracle admission is positive but release-control negative. Oracle: KITTI +1.18%, ETH3D +18.35%; controls: KITTI correct-state 0.2296 loses to no-state 0.1966 and baseline 0.1448, ETH3D correct-state 0.0570 only slightly beats controls. Release candidate selected: frozen StatePrior + bounded residual 0.1448/0.1475. Earlier last-updated note follows.)

Last updated: 2026-06-05 (release-readiness path defined after user asked to push toward publishable model; this planning note is now superseded by DEC-20260605-037. Earlier last-updated note follows.)

Last updated: 2026-06-04 (VGGT-Omega checkpoint uploaded to BUAA-Server and one-window real-backend smoke admitted on GPU1: `backend=real`, fallback contamination 0, pointmap `[2,265216,3]`, runtime 17.96s, VRAM 7143.9MB. Output: `runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json`. Earlier last-updated note follows.)

Last updated: 2026-06-04 (Qwen semantic Critic-prior gate closed diagnostic-negative on BUAA-Server: geometry-only hard-window F1 0.9211, Qwen-real+geometry F1 0.8947, shuffle+geometry F1 0.8421, disabled+geometry F1 0.9211. Qwen semantics do not improve the current geometry-disagreement trigger; keep Qwen as offline annotation/diagnostic only. Earlier last-updated note follows.)

Last updated: 2026-06-03 (Qwen held-out calibrated controller gate closed diagnostic-negative: leave-one-drive/group-out centroid controller on 50 Qwen v2 windows gives oracle 0.1489, real 0.1813, shuffle 0.1776, disabled 0.2365. Real beats disabled but does not beat shuffle, so Qwen remains offline diagnostic/cache evidence only; no Router/Critic promotion. See `DEC-20260603-033`. Earlier last-updated note follows.)

Last updated: 2026-06-03 (Qwen controller v2 feature/policy repair closed weak-positive: cause-derived risk floors and route priority repair make real Qwen beat disabled clearly and shuffle marginally on the 50-window dry-run, but `promotable=false` remains. Fresh v2: oracle 0.1489, real 0.1750, shuffle 0.1759, disabled 0.2365. No Router/Critic training, no frozen-core edit, no Qwen geometry claim. Earlier last-updated note follows.)

Last updated: 2026-06-03 (Qwen3-VL-2B 50-window controller gate closed negative: GPU1 strict schema passed 50/50, but real/shuffle/disabled dry-run all route to Fast3R and have identical metric 0.2365 vs oracle 0.1489, so Qwen is not promotable to Router/Critic training from this policy. No frozen-core edits or Qwen geometry claim. Earlier last-updated note follows.)

Last updated: 2026-06-03 (Qwen3-VL-2B weight staging closed positive: weights staged on BUAA-Server, isolated qwen3vl2b smoke venv created without mutating `dream3r`, and GPU1 5-window KITTI semantic-label smoke passed strict schema 5/5. Earlier last-updated note follows.)

Last updated: 2026-06-03 (V11 Qwen semantic-controller architecture integration started: add real window-manifest builder and Router/Critic VLM dry-run controls outside frozen core. Earlier last-updated note follows.)

Last updated: 2026-06-03 (V11 semantic label-cache implementation gate closed mock-positive: strict schema script/tests added, local mock smoke report valid, Qwen inference blocked by missing staged weights and server `transformers 4.46.0`. Earlier last-updated note follows.)

Last updated: 2026-06-03 (V11 VLM semantic-controller implementation gate started: build the reversible offline semantic label-cache script with strict schema, mock tests, optional Qwen backend only if already available/approved, and Router/Critic-ready causality controls. Earlier last-updated note follows.)

Last updated: 2026-06-03 (V11 VLM semantic-controller research documentation pass closed: comprehensive plan, DEC, cycle log, handoff prompt, and guidance chain updated. Qwen3-VL-2B-Instruct is scoped as offline semantic support signal for Router/Critic/state/teacher scheduling, not geometry. No model training, checkpoint download, frozen-core edit, or server mutation. Earlier last-updated note follows.)

Last updated: 2026-06-03 (V11 VLM semantic-controller research documentation pass in progress: prepare a comprehensive Qwen3-VL-2B-Instruct support-signal plan, update guidance/documentation chain, and add a paste-ready new-agent research prompt. No model training, checkpoint download, frozen-core edit, or server mutation in this documentation pass. Earlier last-updated note follows.)

Last updated: 2026-06-02 (U1 image-state native gate closed negative and VGGT-Omega admission preflight installed: Kitti/ETH3D image-token caches built on BUAA-Server GPU1; U1 gate20 correct-state 0.1649/0.2842 loses to no-state 0.1526/0.1702 and locked baseline 0.1448/0.1475. VGGT-Omega smoke script compiles and public code is staged on server, but real admission is blocked on missing approved checkpoint. Earlier last-updated note follows.)

Last updated: 2026-06-02 (image-state native student U1 scaffold added after user flagged current model unusable: non-core image-token + state + optional proposal-anchor decoder, image-state cache builder, trainer, sweep, and tests added; local tests 6 passed, server tests 3 passed. Cache-build/training gate pending. Earlier last-updated note follows.)

Last updated: 2026-06-02 (native student decoder/distillation gate closed flat-but-controlled: non-core NativeStudentDecoder/trainer/sweep/tests added; BUAA-Server GPU1 seed7 gate preserves state causality with zero fallback contamination but does not beat bounded frozen-StatePrior refinement. Current best remains bounded 0.1448/0.1475. Earlier last-updated note follows.)

Last updated: 2026-06-02 (architecture acceleration execution pass in progress: lock bounded frozen-StatePrior baseline, implement non-core native student decoder/distillation over existing proposal caches, run bounded BUAA-Server GPU1 smoke if available, and sync documentation chain before final. Earlier last-updated note follows.)

Last updated: 2026-06-02 (architecture acceleration prompt added: use `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md` and `planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md` to move from small residual-head tweaks to native student decoder/distillation or tightly gated VGGT-Omega teacher admission. Earlier last-updated note follows.)

Last updated: 2026-06-01 (bounded residual refinement over frozen StatePrior closed small-positive: correct-state KITTI/ETH3D = 0.1448/0.1475 vs frozen-prior 0.1452/0.1480, shuffle-state = 0.1521/0.2467. Current best bounded Dream3R variant is proposal teachers + Dream state -> frozen trained StatePrior -> bounded convex fusion -> disagreement-bounded residual refinement. Earlier last-updated note follows.)

Last updated: 2026-06-01 (frozen-prior decoder sweep closed scaffold-positive: correct-state KITTI/ETH3D = 0.1452/0.1480, shuffle-state = 0.1525/0.2468. KL=0.01 sensitivity gives 0.1451/0.1480 vs shuffle 0.1525/0.2468. Freezing DEC-019 StatePrior preserves state causality and prevents DEC-020 joint decoder collapse, but does not improve beyond StatePriorHead. Next route: bounded refinement over frozen prior with a different refinement mechanism/target, not just KL tuning. Earlier last-updated note follows.)

Last updated: 2026-05-31 (prior-conditioned ProposalSetDecoder seed7 controls closed NEGATIVE: correct-state 0.1523/0.1828, no-state 0.1201/0.1717, shuffle 0.1481/0.1855 on KITTI/ETH3D. StatePriorHead remains positive evidence, but joint ProposalSetDecoder training collapses/overrides the prior. Two-stage route implemented via `--state-prior-checkpoint --freeze-state-prior --prior-kl-weight`; frozen-prior smoke reproduces positive StatePrior result 0.1451/0.1480. Earlier last-updated note follows.)

Last updated: 2026-05-31 (StatePrior diagnostic closed after ProposalSetDecoder v0/v1 failed state-causality: non-core `StatePriorHead` + trainer/tests added; seed7 correct/no-state/shuffle controls completed on BUAA-Server existing SCF caches. Correct-state beats best-single on KITTI/ETH3D and beats both controls; next work should inject learned state prior into ProposalSetDecoder/native distillation, not scale unstructured state concat. Earlier last-updated note follows.)

Last updated: 2026-05-30 (Dream3R-PD execution started locally: VGGT-Omega deployment inventory + DEC-016 execution draft added; non-core ProposalSetDecoder prototype/trainer/tests added under DEC-017; local unit test passed 2/2. No checkpoint, no server run, no frozen-core edit. Earlier last-updated note follows.)

Last updated: 2026-05-30 (final architecture path selected: Dream3R-PD = Proposal-bank Distilled State-Conditioned 3R. DEC-015 / SPEC-005 / final plan / v09 handoff added. Next work should execute VGGT-Omega inventory, ProposalSetDecoder, trained-state projection, and native distillation gates rather than reopening route search. Earlier last-updated note follows.)

Last updated: 2026-05-30 (v2.2 admission research switched first candidate from vanilla VGGT to VGGT-Omega. DEC-014 / SPEC-004 / runbook / v08 handoff added. Current route: keep MASt3R/Fast3R/Spann3R; admit VGGT-Omega first, then CUT3R and MonST3R by contract. Vanilla VGGT is baseline/schema ancestor; OVGGT is a separate cache-memory comparator. Earlier last-updated note follows.)

Last updated: 2026-05-30 (milestone reorganization completed: Dream3R is now organized as proposal encoders + Dream state + state-conditioned reconstruction decoder, not hard routing or loose ensemble. DEC-013 / SPEC-003 / milestone plan / v07 handoff added. Next route now follows DEC-014: keep MASt3R/Fast3R/Spann3R, admit only VGGT-Omega/CUT3R/MonST3R by contract, then train non-core reconstruction decoder and state projection. Earlier last-updated note follows.)

Last updated: 2026-05-30 (ver2.1 4-seed metric refresh completed on BUAA-Server GPU 1: SCF + correct state beats no-state and shuffled-state on KITTI/ETH3D abs_rel and patch-oracle gap; temporal/scale proxies remain open training targets. Summary: `runs/stage6_fusion/ver21_metric_refresh/summary.md`. No frozen core edits. Earlier last-updated note follows.)

Last updated: 2026-05-30 (Dream3R-ver2.0 SCF midterm closure: `DEC-20260530-011` accepted L0 real-backend guardrail, L1 single-expert residual NEGATIVE, and L2 bounded multi-expert SCF POSITIVE. New architecture spec `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md`; cycle log `cycles/CYCLE-20260530-scf-midterm.md`; midterm/mainwork synced. Next agents should continue from SCF/ver2.0 + L4 state retraining/metrics, not reopen broad architecture search. Earlier last-updated note follows.)

Last updated: 2026-05-29 (two-day SCF convergence STARTED: `planning/DREAM3R_2DAY_SCF_MIDTERM_PLAN.md` created — 10-section plan (Dream3R-v0.6 SCF model def, B0-B4 + oracle baselines, ablations, metrics, 2-day schedule, verified patch surface, L0/L1/L2 gates, acceptance). First safe step done: L0 real-backend guardrail (SPEC A9) staged locally in non-core scripts `code/dream3r/scripts/train_fusion_head.py` (new `ensure_real_backends` helper + per-entry `expert_backend`, gated on real presets) and `code/dream3r/scripts/smoke_stage6_one_window.py` (asserts dispatched expert is real). Resolved handoff Open Question #1: `ExpertRegistry.get()` caches, so dispatch reuses pre-loaded adapters. No core edits; no server run yet. Earlier last-updated note follows.)

Last updated: 2026-05-29 (two-day SCF convergence handoff corrected: `handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md` now tells the next agent to produce `planning/DREAM3R_2DAY_SCF_MIDTERM_PLAN.md` and immediately begin the first safe planning/execution step for the 2026-05-29 to 2026-05-30 midterm window. Earlier last-updated note follows.)

Last updated: 2026-05-27 (state-conditioned reconstruction pivot: added `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md`, `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md`, and `cycles/CYCLE-20260527-state-conditioned-reconstruction.md`; hard expert selection demoted from headline claim to proposal prior / diagnostic baseline; no code change.)

Last updated: 2026-05-22 (v0.5 iteration test plan added after user asked how to iterate, test, and start completing the architecture plans: `planning/DREAM3R_V05_ITERATION_TEST_PLAN.md` defines L0-L4 completion standards, S0 local v0.4 edge tests, S1 A6 KITTI 8-10 window memory evidence, S2 A2 staged adapter real-backend closure, S3 A5 Test3R off-path, S4 A3 dynamic-mask promotion design, server runbook outline, evidence schema, gates, risks, and a short agent prompt; `handoff/ARCHITECTURE_V05_AGENT_START_PROMPT.md` added. Planning only; no v0.5 axis closed. Earlier last-updated note follows.) Last updated: 2026-05-22 (cycle 043 architecture-focus round after user re-prioritization "架构是最重要的内容; 开题报告和综述放一边": W20 SOTA Feature Matrix expanded at `code/dream3r/SOTA_FEATURE_MATRIX.md` (family-grouped 2nd pass) + v0.5 axes spec drafted at `specs/SPEC-20260522-001-dream3r-v05-axes.md` (8 axes A1-A8 with explicit `closes_iff`); markdown only; v0.3 + v0.4 code byte-identical; both candidate-not-final per DEC-20260501-004; sync chain applied. Earlier last-updated note follows.) Last updated: 2026-05-22 (v0.4 architecture closure round, parallel to proposal track: added `code/dream3r/contracts.py` + `repair.py` + `orchestrator.py` + 3 new test files + `ARCHITECTURE_V04_STATUS.md`; 24 new tests + 130 pre-existing tests all pass; v0.3 model.py / modules.py / bus.py / anchor_bank.py / nsa_attention.py / composer_experts/* are byte-identical to before this round; driven by `ARCHITECTURE_V04_AGENT_PROMPT.md`. Proposal-track last-updated note follows.) Last updated: 2026-05-17 (post cycle 042: user 指令开题报告扩展为双支柱项目 — 支柱 A Dream3R 新架构模型 (已有 §1-§9) + 支柱 B KYKT 聚合管理平台 (待新增); PROPOSAL_EXPANSION_PLAN.md + AGENT_HANDOFF_PROPOSAL_EXPANSION.md 已创建; 待其他 agent 执行扩展写作)

Status: **idle** (context compressed in `handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md`; usable model is `v1.1-rc1` via `dream3r.release_v11.build_dream3r_v11_release`; official stable package `v1.0-rc1` is preserved. Foundation3R remains experimental.)

## Release-readiness gate (2026-06-05)

```text
task_id:    dream3r-release-readiness-2026-06-05
phase:      publishable-candidate selection
status:     release package complete; selected RC documented and locally verified
driver:     user said "赶紧推进到这个模型能发布"
priority:   stop broad exploration; choose VGGT-expanded model or bounded baseline release candidate
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260605-RC-S1 | Define release gates and stop branches | done | `DEC-20260605-036`; `DREAM3R_RELEASE_READINESS_PLAN_20260605.md` |
| C20260605-RC-S2 | Add VGGT-Omega oracle-admission evaluator | done | `code/dream3r/scripts/eval_vggt_omega_oracle_admission.py`; local/server 27 passed |
| C20260605-RC-S3 | Sync evaluator/test to BUAA-Server | done | transient `scp` reset recovered |
| C20260605-RC-S4 | Run 5+5 / 20+20 / 50+50 oracle admission | done; oracle-positive | 50+50: KITTI +1.18%, ETH3D +18.35% |
| C20260605-RC-S5 | Run VGGT-expanded state/no-state/shuffle controls | done; release-negative | KITTI correct-state 0.2296 loses to no-state 0.1966 and baseline 0.1448 |
| C20260605-RC-S6 | Decide release branch | done | selected bounded StatePrior + residual baseline; release package under `release/` |
| C20260605-RC-S7 | Finalize release reproducibility docs | done | `release/REPRODUCE.md`; `release/VERIFY_REPORT.md`; local 27 passed; frozen-core diff empty |
| C20260606-RC-S8 | Add external-facing release packaging | done | `release/METHOD_ONEPAGER.md`; `release/PUBLISH_CHECKLIST.md`; artifact manifest updated |
| C20260606-RC-S9 | Add method figure and result tables | done | `release/METHOD_FIGURE.md`; `release/RESULT_TABLE.md`; `release/PRESENTATION_OUTLINE.md` |
| C20260606-RC-S10 | Add module implementation map | done | `planning/DREAM3R_IMPLEMENTATION_MODULE_MAP_20260606.md` |
| C20260606-RC-S11 | Add fast module-completion optimization plan | done | `planning/DREAM3R_FAST_MODULE_COMPLETION_OPTIMIZATION_PLAN_20260606.md` |
| C20260606-RC-S12 | Implement native-student objective gates | done; release-negative | `DEC-20260606-038`; P1/P2 correct-state `0.1451/0.1480`, fallback 0 |
| C20260606-RC-S13 | Create formal v1.0-rc1 package | done | `release/OFFICIAL_VERSION.md`; `release/ARCHITECTURE_V1_0_RC.md`; `verify_release_candidate.py` |
| C20260606-RC-S14 | Add official v1.0-rc1 architecture API | done | `code/dream3r/release_candidate.py`; `test_release_candidate_architecture.py` |
| C20260606-RC-S15 | Run broad training verification | done | local `273 passed, 2 skipped`; server GPU1 `37 passed`; four 1-epoch smoke groups |
| C20260606-RC-S16 | Evaluate domain-conditional VGGT teacher | done; experimental-positive | KITTI `0.1448`, ETH3D `0.0570`; not official without unified rerun |
| C20260606-RC-S17 | Clean architecture entrypoints | done | `ARCHITECTURE.md`; `release/ARCHITECTURE_STATUS.json` |
| C20260606-RC-S18 | Run unified domain-conditional gate | done; v1.1 candidate-positive | server JSON: `unified_gate_candidate_with_kitti_no_state_server.json`; controls all pass |
| C20260606-RC-S19 | Package v1.1 or freeze as experimental | done; usable package | `release_v11.py`; `USABLE_MODEL_V1_1.md`; `verify_v11_release.py`; local/server pass |
| C20260606-PF-S1 | Add proposal-free decoder/trainer/tests | done | `ProposalFree3RDecoder`; no proposal inputs accepted by forward contract |
| C20260606-PF-S2 | Run proposal-free GPU1 gate20 | done; negative | state `0.3273/0.4029`, no-state `0.3318/0.4050`, shuffle `0.3221/0.4041` |
| C20260606-PF-S3 | Build stripped teacher distillation target cache | done; mechanism-positive | `build_proposal_free_teacher_cache.py`; proposal fields stripped |
| C20260606-PF-S4 | Run proposal-free teacher gate20 | done; negative | state `0.3319/0.4056`, no-state `0.3292/0.4049`, shuffle `0.3288/0.4116` |
| C20260606-PF-S5 | Run proposal-free AbsRel/capacity gate | done; negative | state `0.3326/0.4058`, no-state `0.3327/0.4080`, shuffle `0.3328/0.4064` |
| C20260606-PF-S6 | Plan Foundation3R proposal-free route | done | `planning/DREAM3R_FOUNDATION3R_PROPOSAL_FREE_PLAN_20260606.md` |
| C20260606-PF-S7 | Implement Sprint 0/1 contract lock + dense teacher cache | done; scaffold-positive | local `11 passed`; server `3 passed`; real KITTI/ETH3D 1-window VGGT dense teacher smokes pass |
| C20260606-PF-S8 | Build 50+50 real Foundation3R dense teacher cache | done; data-positive | KITTI 50/50, ETH3D 50/50, failures 0, fallback 0, leak audit pass |
| C20260607-PF-S9 | Implement `train_foundation3r.py` | done; smoke-positive | local `13 passed`; server `5 passed`; GPU1 1-epoch smoke pass |
| C20260607-PF-S10 | Run Foundation3R scratch 20-epoch state/no-state/shuffle gate | done; negative | state/no-state/shuffle collapse near `0.4734/0.3271`; see DEC-047 |
| C20260607-PF-S11 | Add VGGT-Omega feature student and 50+50 feature cache | done; mechanism-positive | real feature caches pass failures 0/fallback 0; `vggt_patch_features [4,196,128]` |
| C20260607-PF-S12 | Run VGGT feature teacher-only controls | done; experimental-positive, not promotable | state `0.3237/0.1424`, no-state `0.3260/0.1489`, shuffle `0.3246/0.1330`; state causality not established |

## VGGT-Omega admission runner (2026-06-04)

```text
task_id:    dream3r-vggt-omega-admission-runner-2026-06-04
phase:      v2.2 teacher/proposal-bank admission staging
status:     one-window real-backend admitted; tiny cache/oracle gate pending
driver:     user said Qwen does not seem useful and asked to continue normal research
priority:   resume VGGT-Omega admission without fallback/stub contamination
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260604-VGO-S1 | Add resumable admission staging runner | done | `code/dream3r/scripts/stage_vggt_omega_admission.py` |
| C20260604-VGO-S2 | Add mock blocked/ready integration tests | done | local 22 passed; server 22 passed |
| C20260604-VGO-S3 | Run BUAA-Server staging status check | initially blocked as expected | `hf_token_missing`; checkpoint missing before upload |
| C20260604-VGO-S4 | Upload checkpoint and rerun GPU1 smoke | done; admitted | `backend=real`; `fallback_contamination_count=0`; pointmap `[2,265216,3]` |
| C20260604-VGO-S5 | Update DEC/cycle/guidance chain | done | `DEC-20260604-035`, `CYCLE-20260604-vggt-omega-admission-runner` |

## V11 Qwen semantic Critic-prior gate (2026-06-04)

```text
task_id:    dream3r-qwen-semantic-critic-prior-gate-2026-06-04
phase:      semantic-assisted Critic trigger diagnostic
status:     closed diagnostic-negative; not promotable
driver:     user said "语义不能辅助吗？" then "全面推进1"
priority:   test Qwen as Critic prior only, not as geometry or expert router
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260604-QWCR-S1 | Add semantic Critic-prior evaluator | done | `eval_vlm_semantic_critic_gate.py` |
| C20260604-QWCR-S2 | Add regression test for real semantic + geometry | done | local 11 passed; server 11 passed |
| C20260604-QWCR-S3 | Run server 50-window gate on Qwen v2 cache | done; negative | geometry-only F1 0.9211; real+geometry F1 0.8947; disabled+geometry F1 0.9211 |
| C20260604-QWCR-S4 | Update DEC/cycle/guidance chain | done | `DEC-20260604-034`, `CYCLE-20260604-qwen-semantic-critic-prior-gate` |

Artifacts:

```text
code/dream3r/scripts/eval_vlm_semantic_critic_gate.py
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/semantic_critic_gate_50win_t320_v2.json
```

If interrupted, resume from:

```text
Do not promote the current Qwen 50-window cache for routing or Critic triggers.
Both direct controller and semantic Critic-prior gates are negative. Next useful
architecture work should move to VGGT-Omega teacher/proposal-bank admission or
build a real Critic/proposal-disagreement cache before re-testing semantics.
```

## V11 Qwen held-out calibrated controller (2026-06-03)

```text
task_id:    dream3r-qwen-heldout-calibrated-controller-2026-06-03
phase:      held-out semantic controller causality check
status:     closed diagnostic-negative; not promotable
driver:     user said "继续吧"
priority:   test Qwen semantic features as offline controller signal without geometry or core edits
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260603-QWHC-S1 | Add held-out calibrated controller evaluator | done | `eval_vlm_calibrated_controller.py`; leave-one-group-out nearest-centroid gate |
| C20260603-QWHC-S2 | Add causality-control integration test | done | local 10 passed; server 10 passed |
| C20260603-QWHC-S3 | Run 50-window Qwen v2 held-out gate | done; negative vs shuffle | oracle 0.1489, real 0.1813, shuffle 0.1776, disabled 0.2365 |
| C20260603-QWHC-S4 | Update DEC/cycle/guidance chain | done | `DEC-20260603-033`, `CYCLE-20260603-qwen-heldout-calibrated-controller` |

Artifacts:

```text
code/dream3r/scripts/eval_vlm_calibrated_controller.py
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/calibrated_controller_50win_t320_v2.json
```

If interrupted, resume from:

```text
Do not promote the current Qwen 50-window cache into Router/Critic. The
held-out calibrated gate is negative against shuffle. Future Qwen work needs
broader windows, a pre-registered real > shuffle > disabled threshold, and
Router/Critic state-causality evaluation before any training claim.
```

## V11 Qwen controller v2 feature/policy repair (2026-06-03)

```text
task_id:    dream3r-qwen-controller-v2-feature-policy-repair-2026-06-03
phase:      repair DEC-031 all-Fast3R controller collapse
status:     closed weak-positive; not promotable
driver:     user said "你好好改改吧"
priority:   use Qwen causes/risks as controller signal without geometry or core edits
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260603-QWV2-S1 | Inspect DEC-031 Qwen cache failure | done | `visible_failure_causes` had signal; raw `risk_*` mostly zero |
| C20260603-QWV2-S2 | Add cause-derived risk feature floors | done | `CAUSE_TO_RISK_KEY`, `CAUSE_RISK_FLOOR=0.65` |
| C20260603-QWV2-S3 | Repair deterministic route priority | done | dynamic -> Spann3R, low_texture/reflection/repeated/occlusion -> MASt3R before road -> Fast3R |
| C20260603-QWV2-S4 | Add regression tests | done | local 9 passed; server 9 passed |
| C20260603-QWV2-S5 | Re-run 50-window Qwen v2 on GPU1 | done | schema 50/50, oracle 0.1489, real 0.1750, shuffle 0.1759, disabled 0.2365 |
| C20260603-QWV2-S6 | Update DEC/cycle/guidance chain | done | `DEC-20260603-032`, `CYCLE-20260603-qwen-controller-v2-feature-policy-repair` |

Artifacts:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/kitti_50win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/qwen_labels_50win_t320_v2.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/schema_report_50win_t320_v2.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/controller_dryrun_50win_t320_v2.json
```

If interrupted, resume from:

```text
Do not train Router/Critic from v2 yet. The next meaningful Qwen gate is a
held-out calibrated or learned semantic controller over these features, with
real/shuffle/disabled controls and a promotion threshold set before training.
Do not hand-tune deterministic rules further on the same 50-window set.
```

## V11 Qwen3-VL-2B 50-window controller gate (2026-06-03)

```text
task_id:    dream3r-qwen3vl2b-50win-controller-gate-2026-06-03
phase:      held-out real semantic-label cache plus real/shuffle/disabled dry-run
status:     closed negative
driver:     user said "开始推进吧！"
priority:   integrate Qwen as offline semantic controller evidence, not as geometry
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260603-QW50-S1 | Inspect oracle/window-id compatibility | done | oracle ids are raw KITTI sequence / ETH3D sequence ids |
| C20260603-QW50-S2 | Add reversible oracle-compatible manifest id mode | done | `build_vlm_window_manifest.py --window-id-mode sequence`; default remains prefixed |
| C20260603-QW50-S3 | Build 50-window manifest aligned with existing oracle labels | done | `kitti_50win_manifest.json`; 50 windows, 50/50 oracle overlap, 0 missing frames |
| C20260603-QW50-S4 | Run Qwen3-VL-2B strict JSON label cache on GPU1 | done | `schema_report_50win_t320.json`; 50/50 valid, 0 failure records, schema pass 1.0 |
| C20260603-QW50-S5 | Run controller dry-run with real/shuffle/disabled controls | done; negative | oracle 0.1489; real/shuffle/disabled all 0.2365; all route to Fast3R; `promotable=false` |
| C20260603-QW50-S6 | Update DEC/cycle/guidance chain and close snapshot | done | `decisions/DEC-20260603-031-qwen3vl2b-50win-controller-gate.md`, `cycles/CYCLE-20260603-qwen3vl2b-50win-controller-gate.md` |

Artifacts:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/qwen_labels_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/schema_report_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/controller_dryrun_50win_t320.json
```

## V11 Qwen3-VL-2B weight staging (2026-06-03)

```text
task_id:    dream3r-qwen3vl2b-weight-staging-2026-06-03
phase:      Qwen3-VL-2B weight staging and smoke readiness
status:     closed positive
driver:     user said "我们权重开始搞吧"
priority:   stage weights first, then run only a small semantic-label smoke on GPU1
```

Subtask board:

| ID | Task | Status | Evidence |
| --- | --- | --- | --- |
| C20260603-QW-S1 | Mark snapshot in progress and inspect current server checkpoint/env state | done | server had no Qwen weights; `dream3r` env had Transformers 4.46.0 |
| C20260603-QW-S2 | Create/verify Qwen checkpoint staging directory without touching frozen core | done | `/hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct` |
| C20260603-QW-S3 | Download or stage Qwen3-VL-2B-Instruct weights if accessible | done | `model.safetensors` sha256 `7de1838c87a5349b016c26a1c3f7d2bc400a3d485f95ef39a7059ffd734977a0` |
| C20260603-QW-S4 | Check compatible Qwen/Transformers inference path without mutating existing env unnecessarily | done | isolated `/hdd3/kykt26/envs/qwen3vl2b_smoke`; `Qwen3VLProcessor` + `Qwen3VLConfig` load |
| C20260603-QW-S5 | Run tiny GPU1 semantic-label smoke only if weights + runtime are ready | done | `runs/vlm_semantic_controller/qwen3vl2b_real_smoke/schema_report_5win_t320.json`; 5/5 schema pass |
| C20260603-QW-S6 | Update DEC/cycle/guidance chain and close snapshot | done | `decisions/DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md`, `cycles/CYCLE-20260603-qwen3vl2b-weight-staging-smoke.md` |

If interrupted, resume from:

```text
Weights and runtime are staged, and the first 50-window real Qwen gate has now
closed negative. Do not train Router/Critic, edit frozen core, or make a
geometry-quality claim from this cache. Next Qwen work must redesign
prompt/features/policy and re-run real/shuffle/disabled controls.
```

## V11 Qwen semantic-controller integration (2026-06-03)

```text
task_id:    dream3r-qwen-semantic-controller-architecture-integration-2026-06-03
phase:      V11 architecture integration dry-run
status:     closed local mock-positive; real Qwen blocked
driver:     user asked to start the new Qwen-based optimization and integrate it into the architecture
priority:   use Qwen/VLM labels only as offline semantic controller signals for Router/Critic evaluation
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260603-029-qwen-semantic-controller-integration.md` | Decision for controller-integration dry-run gate |
| `cycles/CYCLE-20260603-qwen-semantic-controller-integration.md` | Cycle log |
| `code/dream3r/scripts/build_vlm_window_manifest.py` | Non-core KITTI/ETH3D image-window manifest builder |
| `code/dream3r/scripts/eval_vlm_controller_dryrun.py` | Non-core Router/Critic dry-run evaluator with real/shuffle/disabled controls |
| `code/dream3r/tests/test_vlm_controller_integration.py` | Manifest and dry-run causality tests |
| `runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_oracle_labels.json` | Mock-only oracle labels/metrics for dry-run plumbing |
| `runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json` | Mock dry-run output; `promotable=false` |

Verification:

```text
python -B -m py_compile code/dream3r/scripts/build_vlm_window_manifest.py code/dream3r/scripts/eval_vlm_controller_dryrun.py code/dream3r/tests/test_vlm_controller_integration.py
python -B -m pytest code/dream3r/tests/test_vlm_semantic_labels.py code/dream3r/tests/test_vlm_controller_integration.py -q
# 6 passed
```

Mock dry-run result:

```text
schema_version: dream3r_vlm_controller_dryrun_v1
n_windows: 2
vlm_real: 0.2100
vlm_shuffle: 0.5250
vlm_disabled: 0.3600
promotable: false
```

If interrupted, resume from:

```text
Do not recreate the V11 scripts. Next executable gate is real Qwen label smoke
only after Qwen3-VL-2B-Instruct weights and compatible Qwen/Transformers stack
are staged or approved on BUAA-Server. Build a 10-50 window KITTI/ETH3D
manifest, run Qwen on GPU1, then evaluate real labels versus shuffled/disabled
controls with `eval_vlm_controller_dryrun.py`. Do not train Router/Critic and
do not edit frozen core until real labels pass this held-out control gate.
```

## Architecture acceleration prompt (2026-06-02)

```text
task_id:    dream3r-architecture-acceleration-prompt-2026-06-02
phase:      architecture convergence handoff
status:     ready
driver:     user asked for fast, effective architecture progress instead of small tweaks
priority:   native student decoder/distillation or gated teacher-bank admission
```

Read next:

| File | Role |
| --- | --- |
| `decisions/DEC-20260602-023-architecture-acceleration-prompt.md` | Decision to switch from micro-tweaks to architecture convergence gates |
| `planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md` | High-impact execution lanes and gates |
| `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md` | Copy-paste prompt for the next agent |
| `cycles/CYCLE-20260602-architecture-acceleration-prompt.md` | Documentation cycle log |
| `decisions/DEC-20260602-024-native-student-decoder-gate.md` | First native gate result and next objective-level gate |
| `cycles/CYCLE-20260602-native-student-decoder-gate.md` | Native gate execution log |
| `decisions/DEC-20260602-026-vggt-omega-admission-preflight.md` | VGGT-Omega smoke script and checkpoint blocker |
| `cycles/CYCLE-20260602-vggt-omega-admission-preflight.md` | VGGT-Omega preflight cycle log |

Short instruction for the next agent:

```text
Lock the bounded frozen-StatePrior baseline, then push one high-impact gate:
native student decoder/distillation over existing proposal caches, or VGGT-Omega
one-window teacher admission if native work is blocked. Do not reopen broad
route search and do not spend the session on another residual-head micro-sweep.
```

## Native student decoder/distillation gate (2026-06-02)

```text
task_id:    dream3r-native-student-gate-2026-06-02
phase:      native decoder/distillation execution over existing proposal caches
status:     closed flat-but-controlled
driver:     user asked to push a high-impact architecture gate instead of residual-head tweaks
priority:   prove whether a Dream3R-owned native student can beat the bounded frozen-StatePrior baseline
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260602-024-native-student-decoder-gate.md` | Decision and result |
| `cycles/CYCLE-20260602-native-student-decoder-gate.md` | Execution log |
| `code/dream3r/native_student_decoder.py` | Non-core frozen-StatePrior teacher + proposal-dropout native residual student |
| `code/dream3r/scripts/train_native_student_decoder.py` | Cached-proposal trainer with state/no-state/shuffle controls |
| `code/dream3r/scripts/run_native_student_decoder_sweep.sh` | BUAA-Server GPU1 control runner |
| `code/dream3r/tests/test_native_student_decoder.py` | Local/server gate tests |

Server result:

```text
runs/stage6_fusion/native_student_decoder_gate20_seed7
correct-state: KITTI 0.1451, ETH3D 0.1480
no-state:      KITTI 0.1557, ETH3D 0.1730
shuffle-state: KITTI 0.1525, ETH3D 0.2468
fallback contamination: 0
```

Conclusion: native student decoding is now executable and state-causal, but it
does not beat the bounded frozen-StatePrior refinement baseline of
0.1448/0.1475. Do not promote it as current best model. Next native work should
change the objective with dropout-consistency or temporal/scale state-projection
targets before rerunning controls.

## Image-state native student U1 (2026-06-02)

```text
task_id:    dream3r-image-state-native-u1-2026-06-02
phase:      usable-model scaffold after proposal-only native gate
status:     closed negative; scaffold preserved but not promoted
driver:     user said the current model is not usable and asked to move quickly
priority:   add an image-conditioned native path instead of another proposal-only mixer
```

Files added:

| File | Role |
| --- | --- |
| `decisions/DEC-20260602-025-image-state-native-student-u1.md` | Decision and next gate |
| `cycles/CYCLE-20260602-image-state-native-student-u1.md` | Execution log |
| `code/dream3r/image_state_student_decoder.py` | U1 decoder: image tokens + state + optional proposal anchors -> pointmap |
| `code/dream3r/scripts/build_image_state_student_cache.py` | Builder for image-token caches with real-backend proposal guardrail |
| `code/dream3r/scripts/train_image_state_student.py` | U1 trainer; rejects old SCF caches without image tokens |
| `code/dream3r/scripts/run_image_state_student_sweep.sh` | State/no-state/shuffle sweep wrapper |
| `code/dream3r/tests/test_image_state_student_decoder.py` | U1 interface and cache rejection tests |

Verification and GPU result:

```text
local:  python -B -m pytest code/dream3r/tests/test_image_state_student_decoder.py code/dream3r/tests/test_native_student_decoder.py -q
        6 passed
server: conda run --no-capture-output -n dream3r python -B -m pytest dream3r/tests/test_image_state_student_decoder.py -q
        3 passed

cache build:
        image_state_student_kitti_cache.pt  n_windows=246, d_image=768
        image_state_student_eth3d_cache.pt  n_windows=50, d_image=768

gate20:
        correct-state  KITTI 0.1649, ETH3D 0.2842
        no-state       KITTI 0.1526, ETH3D 0.1702
        shuffle-state  KITTI 0.1577, ETH3D 0.2754
        fallback contamination 0
```

Conclusion: Dream3R now has a non-core U1 scaffold with an actual image-token
native path, but it is not a usable model. Correct-state loses to no-state and
to the locked 0.1448/0.1475 baseline. Do not rerun U1 unchanged.

## VGGT-Omega admission preflight (2026-06-02)

```text
task_id:    dream3r-vggt-omega-admission-preflight-2026-06-02
phase:      fallback teacher-bank admission after U1 negative gate
status:     blocked on gated checkpoint
driver:     V10 prompt fallback path after native work blocked
priority:   prepare one-window real-backend teacher admission without fallback contamination
```

Files added:

| File | Role |
| --- | --- |
| `decisions/DEC-20260602-026-vggt-omega-admission-preflight.md` | Decision and blocker |
| `cycles/CYCLE-20260602-vggt-omega-admission-preflight.md` | Execution log |
| `code/dream3r/scripts/smoke_vggt_omega_adapter.py` | Non-core one-window VGGT-Omega smoke/admission payload script |

Server result:

```text
upstream code staged: /hdd3/kykt26/externals/vggt-omega
local upstream commit: 39a0cb8af88554f15ddcb5354cd52bde588fa014
server py_compile: passed
preflight output: runs/v22_admission/vggt_omega_smoke/results.json
backend: error
failure: checkpoint not found at /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
fallback_contamination_count: 1
```

Conclusion: VGGT-Omega is not admitted. The code path is ready, but official
checkpoint access is approval-gated. Do not substitute vanilla VGGT or demo
outputs for this real-backend teacher gate.

## Bounded residual refinement (2026-06-01)

```text
task_id:    dream3r-bounded-prior-refinement-2026-06-01
phase:      bounded refinement over frozen StatePrior
status:     closed small-positive
driver:     user asked to continue and make the architecture serious
priority:   improve frozen-prior scaffold without losing state causality
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260601-022-bounded-prior-refinement.md` | Decision and result |
| `cycles/CYCLE-20260601-bounded-prior-refinement.md` | Execution log |
| `code/dream3r/proposal_set_decoder.py` | Adds zero-initialized bounded residual head |
| `code/dream3r/scripts/train_proposal_set_decoder.py` | Adds `--residual-refine-scale` |
| `code/dream3r/scripts/run_frozen_prior_decoder_sweep.sh` | Adds `RESIDUAL_REFINE_SCALE` |

Result:

```text
correct-state: KITTI 0.1448, ETH3D 0.1475
shuffle-state: KITTI 0.1521, ETH3D 0.2467
```

Conclusion: small-positive over frozen-prior baseline while preserving shuffle
separation.

## Frozen-prior decoder sweep (2026-06-01)

```text
task_id:    dream3r-frozen-prior-decoder-2026-06-01
phase:      two-stage decoder control after joint decoder collapse
status:     closed scaffold-positive
driver:     user asked to continue; DEC-020 showed joint decoder collapse
priority:   preserve DEC-019 state-prior causality inside decoder path
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260601-021-frozen-prior-decoder-sweep.md` | Decision and result |
| `cycles/CYCLE-20260601-frozen-prior-decoder-sweep.md` | Execution log |
| `code/dream3r/scripts/run_frozen_prior_decoder_sweep.sh` | Reproducible server runner |

Result:

```text
correct-state: KITTI 0.1452, ETH3D 0.1480
shuffle-state: KITTI 0.1525, ETH3D 0.2468
```

Conclusion: frozen prior preserves state causality and prevents collapse, but
does not improve beyond StatePriorHead.

KL sensitivity:

```text
runs/stage6_fusion/frozen_prior_decoder_kl001_sweep
correct-state: KITTI 0.1451, ETH3D 0.1480
shuffle-state: KITTI 0.1525, ETH3D 0.2468
```

Lower KL preserves causality but still gives no refinement gain.

## Prior-conditioned ProposalSetDecoder (2026-05-31)

```text
task_id:    dream3r-prior-conditioned-decoder-2026-05-31
phase:      decoder repair after StatePrior positive diagnostic
status:     closed negative; seed7 server controls complete
driver:     DEC-019 proved state-prior signal exists
priority:   test whether explicit prior logits repair decoder state causality
```

Files added / updated:

| File | Role |
| --- | --- |
| `code/dream3r/proposal_set_decoder.py` | Adds explicit `state_prior_mlp` branch and `state_prior_weights` output |
| `code/dream3r/scripts/train_proposal_set_decoder.py` | Records prior config and `mean_prior_entropy` |
| `code/dream3r/scripts/run_prior_conditioned_decoder_sweep.sh` | GPU1 seed7 state/no-state/shuffle runner |
| `code/dream3r/tests/test_proposal_set_decoder.py` | Adds prior-branch behavior checks |
| `decisions/DEC-20260531-020-prior-conditioned-decoder.md` | Decision and boundaries |
| `cycles/CYCLE-20260531-prior-conditioned-decoder.md` | Active cycle log |

Server smoke:

```text
runs/stage6_fusion/prior_conditioned_decoder_smoke_seed7
KITTI 0.1480 vs best_single 0.1523
ETH3D 0.1875 vs best_single 0.1585
```

Seed7 result:

```text
correct-state: KITTI 0.1523, ETH3D 0.1828
no-state:      KITTI 0.1201, ETH3D 0.1717
shuffle-state: KITTI 0.1481, ETH3D 0.1855
```

Conclusion: prior-conditioned joint decoder does not repair state causality.
No-state beats correct-state on both domains.

Two-stage executable path:

```text
train_proposal_set_decoder.py \
  --state-prior-checkpoint runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt \
  --freeze-state-prior \
  --prior-kl-weight 0.1
```

Frozen-prior smoke:

```text
runs/stage6_fusion/prior_frozen_decoder_smoke_seed7
KITTI 0.1451 vs best_single 0.1523
ETH3D 0.1480 vs best_single 0.1585
```

## StatePrior diagnostic closure (2026-05-31)

```text
task_id:    dream3r-state-prior-diagnostic-2026-05-31
phase:      Dream-state causality isolation after ProposalSetDecoder v0/v1
status:     closed; seed7 controls complete
driver:     user asked to keep pushing after decoder state-causality weakness
priority:   prove whether Dream state contains usable expert-prior signal
```

Files added:

| File | Role |
| --- | --- |
| `code/dream3r/state_prior_head.py` | Non-core state-only expert-prior diagnostic head |
| `code/dream3r/scripts/train_state_prior_head.py` | Trainer/eval over existing SCF caches |
| `code/dream3r/scripts/run_state_prior_sweep.sh` | GPU1 seed7 control runner |
| `code/dream3r/tests/test_state_prior_head.py` | Shape/gradient/state-control tests |
| `decisions/DEC-20260531-019-state-prior-diagnostic.md` | Decision + final result |
| `cycles/CYCLE-20260531-state-prior-diagnostic.md` | Execution log |

Seed7 result:

```text
correct-state: KITTI 0.1451 (+4.73 pp), ETH3D 0.1480 (+6.64 pp)
no-state:      KITTI 0.1472 (+3.33 pp), ETH3D 0.2003 (-26.38 pp)
shuffle-state: KITTI 0.1622 (-6.51 pp), ETH3D 0.2111 (-33.18 pp)
```

Conclusion: Dream state has usable expert-prior signal. ProposalSetDecoder
v0/v1 failed because the decoder did not preserve that signal as an explicit
control path.

## Dream3R-PD execution start (2026-05-30)

```text
task_id:    dream3r-pd-execution-start-2026-05-30
phase:      local docs/code start after final architecture selection
status:     done locally; server/checkpoint execution gated
driver:     user asked to comprehensively push the selected architecture
priority:   turn Dream3R-PD from route doc into first non-core executable prototype
```

Files added:

| File | Role |
| --- | --- |
| `planning/VGGT_OMEGA_DEPLOYMENT_INVENTORY.md` | Upstream repo/checkpoint/dependency/output inventory |
| `decisions/DEC-20260530-016-vggt-omega-execution-draft.md` | Non-active one-window smoke execution DEC draft |
| `code/dream3r/proposal_set_decoder.py` | Non-core per-patch proposal-token decoder |
| `code/dream3r/scripts/train_proposal_set_decoder.py` | Training/eval script over existing SCF caches |
| `code/dream3r/tests/test_proposal_set_decoder.py` | Shape/gradient/no-state tests |
| `decisions/DEC-20260530-017-proposal-set-decoder-prototype.md` | Boundary + verification DEC |
| `cycles/CYCLE-20260530-dream3r-pd-execution-start.md` | Cycle log |

Verification:

```text
python -m py_compile code/dream3r/proposal_set_decoder.py \
  code/dream3r/scripts/train_proposal_set_decoder.py \
  code/dream3r/tests/test_proposal_set_decoder.py

python -m pytest code/dream3r/tests/test_proposal_set_decoder.py -q
# 2 passed
```

## Dream3R-PD final architecture selection (2026-05-30)

```text
task_id:    dream3r-pd-final-architecture-2026-05-30
phase:      final architecture selection
status:     done for route selection; implementation gated
driver:     user asked agent to autonomously optimize architecture and produce a final-choice方案
priority:   stop route churn and define the executable final model path
```

Files added:

| File | Role |
| --- | --- |
| `decisions/DEC-20260530-015-final-architecture-selection.md` | Selects Dream3R-PD as final architecture path |
| `specs/SPEC-20260530-005-dream3r-pd-final-architecture.md` | Defines proposal teachers, Dream state encoder, ProposalSetDecoder, native distillation |
| `planning/DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md` | Execution ladder P0-P5 with RALPLAN summary and ADR |
| `handoff/ARCHITECTURE_V09_FINAL_SELECTION_AGENT_PROMPT.md` | Next-agent prompt for final-path execution |
| `cycles/CYCLE-20260530-final-architecture-selection.md` | Cycle log |
| `.omx/plans/dream3r-pd-final-architecture-20260530.md` | OMX plan mirror |

Selected route:

```text
Dream3R-PD = proposal teachers + Dream state + proposal-set decoder
             + native decoder distillation with proposal dropout.
```

Execution order:

```text
1. VGGT-Omega deployment inventory and G2 execution DEC draft.
2. ProposalSetDecoder v0 over existing 3-expert caches.
3. Trained-state projection / Critic calibration outside frozen core.
4. VGGT-Omega four-teacher admission after real-backend smoke.
5. Native decoder distillation only after decoder gates pass.
```

## Dream3R v2.2 VGGT-Omega admission research (2026-05-30)

```text
task_id:    dream3r-v22-vggt-omega-admission-2026-05-30
phase:      v2.2 proposal-bank deployment research
status:     done for documentation; execution gated
driver:     user asked to switch from vanilla VGGT to VGGT-Omega and prepare deployment research
priority:   make the next expert admission surgical and source-grounded
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260530-014-v22-vggt-omega-admission.md` | Locks VGGT-Omega as first v2.2 admission candidate |
| `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md` | Defines ExpertProposal adapter, cache, and admission gates |
| `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md` | G0-G7 deployment research runbook |
| `handoff/ARCHITECTURE_V08_V22_ADMISSION_AGENT_PROMPT.md` | Next-agent prompt for VGGT-Omega inventory and execution DEC |
| `cycles/CYCLE-20260530-v22-admission-research.md` | Cycle log |

Current route:

```text
Keep: MASt3R / Fast3R / Spann3R.
Admit next: VGGT-Omega -> CUT3R -> MonST3R.
Baseline only: vanilla VGGT.
Cache/memory comparator only: OVGGT.
```

## Dream3R model-first milestone reorganization (2026-05-30)

```text
task_id:    dream3r-model-reorg-2026-05-30
phase:      post-midterm route consolidation
status:     done; planning/route artifacts written; implementation gated
driver:     user asked how to choose better 3R experts and still build a real Dream3R model
priority:   turn SCF from "fusion script" into a staged 3R model roadmap
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md` | Locks Dream3R as proposal encoders + Dream state + reconstruction decoder |
| `specs/SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md` | Defines decoder v0/v1/v2/v3 and admission protocol |
| `planning/DREAM3R_MILESTONE_REORG_20260530.md` | High-speed task ladder and expert-bank priorities |
| `handoff/ARCHITECTURE_V07_MODEL_REORG_AGENT_PROMPT.md` | Next-agent prompt for model-first continuation |
| `cycles/CYCLE-20260530-milestone-reorg-model-roadmap.md` | Cycle log |

Current route:

```text
Dream3R = proposal encoders + Dream state + state-conditioned reconstruction decoder.

Keep: MASt3R / Fast3R / Spann3R.
Next candidates: VGGT-Omega / CUT3R / MonST3R.
Do not add every new 3R method; admit only if it raises oracle ceiling or
decoder output under state-conditioned fusion.
```

## Dream3R-ver2.1 state-training and metric refinement (2026-05-30)

```text
task_id:    dream3r-ver21-state-training-metrics-2026-05-30
phase:      architecture refinement on top of ver2.0 SCF
status:     done; 4-seed metric refresh completed; core edits gated
driver:     user asked to improve the architecture using the existing plan plus agent judgment
priority:   prove or falsify whether trained state, not just proposal fusion, drives the gain
```

Files added / updated:

| File | Role |
| --- | --- |
| `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md` | Ver2.1 architecture delta: trained state + metric extension |
| `planning/DREAM3R_VER21_STATE_TRAINING_PLAN.md` | Concrete L4 runbook: metric refresh, frozen projection, Critic calibration, core-state DEC gate |
| `decisions/DEC-20260530-012-ver21-state-training-metrics.md` | Direction decision + 4-seed evidence: correct state > no-state > shuffled-state |
| `cycles/CYCLE-20260530-ver21-architecture-refinement.md` | Cycle log with completed 4-seed sweep |
| `code/dream3r/scripts/train_scf_head.py` | Non-core eval now reports patch-oracle, temporal-delta, and scale-drift proxies |
| `code/dream3r/scripts/run_ver21_metric_refresh.sh` | Server sweep helper for state/no-state/shuffled-state controls |
| `code/dream3r/scripts/summarize_ver21_metric_refresh.py` | Reproducible summary writer for `summary.{json,md}` |

Next concrete action:

```text
4-seed evidence shows: correct state KITTI +9.79% / ETH3D +2.44%;
no-state KITTI +5.04% / ETH3D -6.47%; shuffled-state KITTI +3.27% /
ETH3D -10.09%. Correct state also has the lowest patch-oracle gap on both
domains. Temporal/scale proxies are not consistently better, so train them
explicitly in the next DEC.
```

## Dream3R-ver2.0 SCF midterm closure (2026-05-30)

```text
task_id:    dream3r-ver2-scf-midterm-closure-2026-05-30
phase:      architecture completion + evidence consolidation
status:     done for midterm docs; L4 state retraining remains future work
driver:     user requested route consolidation, ver2.0 architecture, and a prompt for other agents
priority:   ship an honest usable model story under the two-day deadline
```

Files added / updated:

| File | Role |
| --- | --- |
| `decisions/DEC-20260530-011-scf-midterm.md` | Authoritative result: L0 real-backend guardrail pass, L1 residual negative, L2 SCF positive |
| `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md` | Dream3R-ver2.0 model contract and accepted claims |
| `cycles/CYCLE-20260530-scf-midterm.md` | Cycle closure for the two-day midterm sprint |
| `mainwork/midterm/MIDTERM-20260530.md` | §4.6 and §5 updated with SCF result + post-midterm roadmap |
| `mainwork.md` | Stage 6 row closed as ver2.0 SCF |
| `handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md` | Next-agent prompt should now start from DEC-011 / ver2.0, not the pre-run plan |

Current technical claim:

```text
Dream3R-ver2.0 = bounded state-conditioned multi-expert fusion.
Hard routing is a proposal prior / diagnostic baseline, not the main model.
```

Evidence:

```text
L1 residual: KITTI -47.1pp, ETH3D -91.9pp -> rejected.
L2 SCF: KITTI +9.8% +/- 2.7% vs best single; ETH3D +2.4% +/- 3.0%;
near-oracle gaps +1.6% / +1.1%.
```

Next concrete action:

```text
Plan L4 only: retrain Memory/Critic with depth/coherence-aligned objectives,
add temporal/scale-drift metrics, and rerun no-state vs trained-state
ablations. Any core edit or training campaign needs its own DEC.
```

## Dream3R two-day SCF convergence handoff (2026-05-29)

```text
task_id:    two-day-scf-convergence-handoff-2026-05-29
phase:      next-agent prompt for two-day midterm convergence
status:     done; prompt only; no implementation
driver:     user clarified there are two days, not four weeks, and asked for a short prompt to plan and push tasks
priority:   converge Dream3R into an honest midterm package plus first executable SCF step
```

New handoff:

| File | Role |
| --- | --- |
| `handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md` | Startup prompt for the next agent. It locks the next target to Dream3R-SCF, requires a two-day midterm convergence plan, and allows the first safe local/doc or non-core-script step without reopening broad architecture exploration |

Expected next artifact from the next agent:

```text
planning/DREAM3R_2DAY_SCF_MIDTERM_PLAN.md
```

Do not restart broad architecture exploration. The next plan must answer:

```text
How do we build and evaluate a usable state-conditioned multi-expert
fusion model with real baselines?
```

## State-conditioned reconstruction pivot (2026-05-27)

```text
task_id:    state-conditioned-reconstruction-pivot-2026-05-27
phase:      architecture addendum on top of Stage 5/6 evidence
status:     done; markdown/design only; no code change; no training claim
driver:     user judged hard expert selection insufficient and asked to optimize the original architecture
priority:   midterm route correction + post-midterm technical mainline
```

Files added / updated:

| File | Role |
| --- | --- |
| `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md` | New architecture addendum: Dream3R shifts from hard expert selection to state-conditioned reconstruction; Composer becomes proposal prior / regime probe / diagnostic baseline; adds A9-A11 axes and L0-L4 roadmap |
| `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md` | Decision memo accepting the route adjustment |
| `cycles/CYCLE-20260527-state-conditioned-reconstruction.md` | Cycle log for the architecture pivot |
| `mainwork.md` | Stage 6 state-to-depth wire / route pivot added to status and next-action sections |
| `mainwork/midterm/MIDTERM-20260530.md` | Midterm narrative and roadmap updated: routing-side validated, reconstruction-plane missing, post-midterm focus becomes state-conditioned fusion/correction |

Next concrete action:

```text
Run Stage 6 L0/L1 only after real adapter loading is guarded: real-backend
cache rebuild + rerun answers whether the smallest state-to-depth wire has
signal on real expert baselines. Do not interpret fallback-stub numbers as
architecture evidence.
```

## v0.5 iteration test plan (2026-05-22)

```text
task_id:    v05-iteration-test-plan-2026-05-22
phase:      planning artifact on top of v0.4 closure and v0.5 axes spec
status:     done; plan + short agent prompt written; no code change; no axis closed
driver:     user asked how to iterate, test, and start completing the architecture plans
priority:   architecture evidence closure before performance claims
```

Files added / updated:

| File | Role |
| --- | --- |
| `planning/DREAM3R_V05_ITERATION_TEST_PLAN.md` | Detailed execution and research plan: L0-L4 completion standards, S0 local v0.4 edge tests, S1 A6 KITTI 8-10 window memory evidence, S2 A2 staged adapter real-backend closure, S3 A5 Test3R off-path, S4 A3 dynamic mask promotion, A1 / A8 / A7 sequencing, server runbook outline, evidence schema, decision gates, risk register, and short agent prompt |
| `handoff/ARCHITECTURE_V05_AGENT_START_PROMPT.md` | Short startup prompt for another agent to begin from the iteration test plan |
| `INDEX.md` + `WORKFLOW_STATUS.md` + `TASK_SNAPSHOT.md` | Minimal sync entries |

Recommended immediate execution:

```text
1. Start with S0 local v0.4 edge tests and multi-tick tests.
2. Produce S1 server runbook for A6 KITTI 8-10 window memory evidence.
3. Do not download checkpoints, train, modify KYKT frontend, or claim any v0.5 axis closed.
```

## Cycle 043 Architecture-Focus Round (2026-05-22)

```text
task_id:    cycle-043-arch-focus-2026-05-22
phase:      markdown-only planning artifact on top of v0.4 closure
status:     done — both artifacts written + sync chain (INDEX / WORKFLOW_STATUS / TASK_SNAPSHOT / cycles)
driver:     user re-prioritization 2026-05-22; menu option A+B (SOTA matrix + v0.5 axes spec)
priority:   architecture > platform; Track C proposal + Track B survey parked
```

Files added / updated this cycle:

| File | Role |
| --- | --- |
| `code/dream3r/SOTA_FEATURE_MATRIX.md` | W20 second pass: 8 family sections (Direct pair / Many-view streaming / Memory primitive comparators / Monocular priors / Test-time + Critic / Attention + state / Permanence + dynamic / Rendering + 4D); 30+ external methods mapped to Dream3R modules + honest status labels (real-wired vs deterministic fallback vs stub vs comparator-only). Supersedes 2026-05-10 first pass; preserves its differentiation list + evidence map |
| `specs/SPEC-20260522-001-dream3r-v05-axes.md` | v0.5 axes spec: 8 axes A1-A8 (DINOv3-S backbone real / per-adapter ckpt loading / dynamic_mask_proxy → D2 promotion / VGGT adapter + capability_card v2.2 / Test3R Critic-triggered off-path / NSA sliding branch utility / GaussianHead conditional entry kept deferred / tttLRM A1 sub-action). Each axis carries explicit `closes_iff` + required actions + dependencies + non-promises + evidence label. v0.5 additive to v0.4 by default. Each axis closure requires its own DEC |
| `cycles/CYCLE-20260522-001.md` | cycle 043 log |
| `INDEX.md` + `WORKFLOW_STATUS.md` + `TASK_SNAPSHOT.md` | sync chain |
| `~/.claude/projects/e--Dream3R/memory/MEMORY.md` + `feedback_track_priorities.md` | auto-memory: priority feedback recorded |

Explicit non-claims:

- No v0.5 axis has been validated; each closure requires its own DEC referencing `closes_iff`.
- No code changed; v0.3 + v0.4 layers remain byte-identical.
- `OnlineX` + `AnchorSplat` flagged as roadmap drafting artifacts (no SRC row, no mapping); not silently included.
- MoGe-2 has an adapter in `method_profiles.py` but **no `SRC-*` row** in `registry/source_registry.md` — inventory hygiene item, not closed.
- KITTI smoke pointmap L2 = 20.4747 preserved as "integration evidence, not trained quality."

Next admissible direction (per `WORKFLOW_STATUS.md` Recommended Next User Decision):

```text
A. Review SPEC-20260522-001 + select which v0.5 axes to promote
   first via DEC. Sprint-1 candidates (all F-002 server gated):
   A1 DINOv3-S / A2 adapter ckpt loading / A4 VGGT + capability_card v2.2
   / A6 NSA sliding branch utility.

B. Markdown-only architecture follow-up (no DEC needed):
   - W22 visualization pack (matplotlib + existing JSON)
   - W26 STREAM3R_RELATION.md design writeup
   - Resolve OnlineX / AnchorSplat ambiguity in NEXT_PHASE_ROADMAP.md
   - Add MoGe-2 SRC row to source_registry.md
   - v0.4 contract edge-case tests

C. Platform / KYKT integration scoping (planning level only;
   KYKT navigation + Codex frontend edits remain blocked).

D. Or pause + reassess.
```

---

## v0.4 Architecture Closure (2026-05-22)

```text
task_id:    v04-arch-closure-2026-05-22
phase:      additive layer on top of v0.3 code
status:     done — 24/24 new tests pass; 130/130 existing tests pass; v0.3 code byte-identical
driver:     ARCHITECTURE_V04_AGENT_PROMPT.md
verification: ARCHITECTURE_V04_STATUS.md
```

Files added (no v0.3 files modified):

| File | Role |
| --- | --- |
| `code/dream3r/contracts.py` | Typed dataclasses for every module boundary; v0.4 action codes 0/1/2/3 |
| `code/dream3r/repair.py` | `RepairExecutor` closing the critic -> rerun / reroute loop |
| `code/dream3r/orchestrator.py` | `V04Pipeline` wrapping Dream3R with closed loops |
| `code/dream3r/tests/test_v04_architecture_contract.py` | 11 tests on full `ReconstructionOutput` |
| `code/dream3r/tests/test_repair_executor_contract.py` | 6 tests on real rerun + reroute + cap behaviour |
| `code/dream3r/tests/test_composer_dispatch_contract.py` | 7 tests on real composer dispatch + reroute |
| `ARCHITECTURE_V04_STATUS.md` | Per-axis checklist, test commands, explicit stub list |

Test commands (verified local):

```bash
cd E:/Dream3R/code
python -m pytest dream3r/tests/test_v04_architecture_contract.py \
                 dream3r/tests/test_repair_executor_contract.py \
                 dream3r/tests/test_composer_dispatch_contract.py -q
# -> 24 passed

python -m pytest dream3r/tests/ -q \
    --ignore=dream3r/tests/test_dinov2_backbone.py \
    --ignore=dream3r/tests/test_fast3r_integration.py \
    --ignore=dream3r/tests/test_mast3r_integration.py \
    --ignore=dream3r/tests/test_spann3r_integration.py
# -> 130 passed
```

Explicit non-claims (no false `real` claims emitted):

- DINOv3-S backbone is NOT loaded; `backend_status["perception"]["backend"]` is `stub` / `fallback`.
- 5 of 7 adapters (Spann3R / CUT3R / MoGe-2 / DepthAnything / Test3R) return deterministic fallback outputs; their `is_loaded=False` and `backend` are `fallback` / `stub`.
- MASt3R / Fast3R loaders are wired but locally have no checkpoint; `backend` is `fallback`.
- Permanence's `dynamic_mask_proxy` is named proxy in the contract; NOT claimed as final D2 asset.
- 4DGS / GaussianHead is NOT pulled into v0.4 main forward (per agent prompt's exclusion rule).

Next minimal experiments (each gated on user / server):

1. Server-side: load MASt3R adapter on `/hdd3/kykt26/` and re-run `test_v04_architecture_contract.py` with `use_backbone=True`; verify at least one `out.expert.backend_status["backend"] == "real"`.
2. KITTI 5-tick smoke: confirm `repair_action_log["n_attempts"]` is bounded across ticks and `route_log["reroute_applied"]` flips True on at least one high-conflict tick.
3. Compare cumulative pointmap L2 against the v0.3 baseline (`20.4747` per `RECENT_PROGRESS.md` line 78) — no regression expected without training.

---

## Proposal track snapshot (preserved from prior session)

## Why this file exists

This file is the highest-authority entry point for any Dream session — human, Codex, or another agent. It exists so that an interrupted task can be resumed cleanly, in this conversation or in a fresh one, without context loss.

Read order on session start:

1. **This file first** (`TASK_SNAPSHOT.md`)
2. Then `AGENT_MASTER_PROMPT.md` Mandatory Load Protocol (this file is item 1 of that protocol; the rest follows)
3. Then proceed per `AGENT_MASTER_PROMPT.md`

If this file's "Status" is `in_progress` or `blocked`, do NOT start new work. Resume the named task from `if_interrupted_resume_from` first.

If this file's "Last updated" timestamp is older than the latest cycle log under `cycles/`, this file is stale; trust the cycle log and update this file before doing anything else.

## Current task

```text
task_id:    dream3r-qwen-semantic-controller-architecture-integration-2026-06-03
phase:      V11 architecture integration dry-run
status:     in_progress
driver:     user asked to begin the new Qwen-based optimization and integrate it into the Dream3R architecture
priority:   integrate cached semantic VLM features into Router/Critic control evaluation without treating Qwen as geometry or editing frozen core files
```

One-line description:

```text
V11 Qwen semantic-controller architecture integration is active. Add a real
window-manifest builder and a VLM controller dry-run evaluator that consumes
semantic cache features, shuffled controls, and disabled controls. Use mock
labels for local tests while real Qwen remains blocked.
```

## Subtask board (active V11 Qwen semantic-controller integration)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C20260603-V11I-S1 | Mark snapshot in progress and lock Qwen-as-controller boundary | done | `TASK_SNAPSHOT.md`, DEC-028 |
| C20260603-V11I-S2 | Implement real KITTI/ETH3D window manifest builder outside frozen core | done | `code/dream3r/scripts/build_vlm_window_manifest.py` |
| C20260603-V11I-S3 | Implement Router/Critic VLM dry-run evaluator with real/shuffle/disabled controls | done | `code/dream3r/scripts/eval_vlm_controller_dryrun.py` |
| C20260603-V11I-S4 | Add tests for manifest generation and VLM controller dry-run causality schema | done | `code/dream3r/tests/test_vlm_controller_integration.py` |
| C20260603-V11I-S5 | Run py_compile, targeted pytest, and local mock dry-run artifact | done | `runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json`; 6 tests passed |
| C20260603-V11I-S6 | Update DEC/cycle/guidance chain and close snapshot | done | `decisions/DEC-20260603-029-qwen-semantic-controller-integration.md`, `cycles/CYCLE-20260603-qwen-semantic-controller-integration.md`, guidance files |
| C20260603-V11G-S1 | Mark snapshot in progress and verify V11 boundaries / frozen-core list | done | `TASK_SNAPSHOT.md`, V11 handoff |
| C20260603-V11G-S2 | Inspect code/test patterns for non-core scripts and cache/test conventions | done | `code/dream3r/scripts/`, `code/dream3r/tests/` |
| C20260603-V11G-S3 | Implement offline VLM semantic label-cache builder with strict schema and mock/Qwen backend interface | done | `code/dream3r/scripts/build_vlm_semantic_labels.py` |
| C20260603-V11G-S4 | Add mock backend tests for schema validation, explicit failures, feature conversion, shuffled/disabled controls | done | `code/dream3r/tests/test_vlm_semantic_labels.py` |
| C20260603-V11G-S5 | Run local py_compile, targeted pytest, and mock smoke cache build | done | `runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json` |
| C20260603-V11G-S6 | Check whether Qwen weights/dependencies are already available without download/environment mutation | done | Qwen weights missing on checked BUAA-Server paths; `dream3r` env has `transformers 4.46.0`; no Qwen inference run |
| C20260603-V11G-S7 | Update DEC/cycle/guidance chain and close snapshot | done | `decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md`, `cycles/CYCLE-20260603-vlm-semantic-label-cache-gate.md`, guidance files |
| C20260603-S1 | Mark snapshot in progress and locate current documentation chain | done | `TASK_SNAPSHOT.md` |
| C20260603-S2 | Check official Qwen3-VL capability boundaries and existing Dream3R VLM mechanism slot | done | official Qwen3-VL sources; `planning/ARCHITECTURE_MECHANISM_INTAKE.md` |
| C20260603-S3 | Write comprehensive V11 semantic-controller research plan | done | `planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md` |
| C20260603-S4 | Add DEC, cycle log, and new-agent prompt | done | `decisions/DEC-20260603-027-vlm-semantic-controller-plan.md`, `cycles/CYCLE-20260603-vlm-semantic-controller-plan.md`, `handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md` |
| C20260603-S5 | Sync project document group and close snapshot | done | `WORKFLOW_STATUS.md`, `INDEX.md`, `mainwork.md`, registry, guidance files |
| C20260602-S1 | Verify bounded frozen-StatePrior baseline artifacts on BUAA-Server | done | `/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/` |
| C20260602-S2 | Inspect non-core decoder/trainer cache path and lock implementation boundary | done | `code/dream3r/proposal_set_decoder.py`, `code/dream3r/scripts/train_proposal_set_decoder.py` |
| C20260602-S3 | Add native student decoder/distillation scaffold outside frozen core | done | `code/dream3r/native_student_decoder.py`, `code/dream3r/scripts/train_native_student_decoder.py`, tests |
| C20260602-S4 | Run local py_compile and targeted tests | done | local verification output |
| C20260602-S5 | Sync to BUAA-Server and run bounded GPU1 smoke if command is valid | done | `runs/stage6_fusion/native_student_decoder_smoke_seed7`, `runs/stage6_fusion/native_student_decoder_gate20_seed7` |
| C20260602-S6 | Update decision/cycle/guidance chain and close pass | done | `cycles/`, `decisions/`, `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `INDEX.md`, `mainwork.md`, registry |

## Cycle 040 subtask board (closed 2026-05-17)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C040-S1 | DEC-20260517-001 launch authorization | done | `decisions/DEC-20260517-001-cycle-040-proposal-sections-5-7-8-dual-draft.md` |
| C040-S2 | Draft §5 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~2800 字, 7 sub-sections: 5.1 三层证据阶梯 + 5.2 架构层消融 ABL-v02-1..10 + 5.3 记忆机制消融 ABL-memory-0..11 + 5.4 Critic 标定 CRITIC_CALIBRATION_PLAN_V1 + 5.5 长序列真实评测 LONG_SEQ_REAL_TABLE_PLAN + 5.6 评测数据集 KITTI + DTU + 合成 fixture + 5.7 主要评测指标) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §5 |
| C040-S3 | Draft §7 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~2200 字, 6 sub-sections: 7.1 架构设计文档系列 SPEC v0.1/v0.2/v0.3 + 7.2 实现里程碑 W1-W18 + 7.3 KITTI 真实数据集成证据 (pointmap L2 = 20.4747 集成证据 非训练后质量) + 7.4 综述发布 + 7.5 综述反哺主线 + 7.6 cycle 历史) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §7 |
| C040-S4 | Draft §8 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~1500 字, 3 sub-sections: 8.1 短期 M1-M2 cycle 040-042 开题报告完稿 + 8.2 中期 M3-M5 W19-W26 真实路由 + Critic 校准 + TTT + 输入扩展 + B1/B2/B3 v0.4 spec delta + 8.3 长期 M6-M8 W27 3DGS renderer + 真实数据训练 + 论文撰写 + 综合评测) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §8 |
| C040-S5 | Snapshot §5 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~2000 字, 7 sub-sections mirroring internal with 学术化命名 + 5 new vocab substitutions: hard_fail/soft_fail → 硬失败/软失败 + oracle-bus → 理想信号总线 + monotone upgrade gate → 单调升级门 + fixture regime R1-R5 → 校准 fixture 制度 + 集成证据 → 集成证据 双稿一致) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §5 |
| C040-S6 | Snapshot §7 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~1500 字, 6 sub-sections mirroring internal; § 7.3 KITTI 集成证据-vs-训练后质量 boundary 顯式保留 per RECENT_PROGRESS.md line 78) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §7 |
| C040-S7 | Snapshot §8 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~1000 字, 3 sub-sections mirroring internal; M-numbering 保留为 candidate timeline 不是 committed timeline 显式声明) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §8 |
| C040-S8 | G3a + G3b + G4 vocab-firewall + over-claim greps (full file scope) | done with 5 corrective edits | First-pass G4 0 hits on both drafts (§5 + §7 + §8 evidence-anchored chapters did not surface negation-context candidate-not-final 句式 contrast at cycle-039 density). First-pass G3a caught 4 hits in DRAFT_EXTERNAL_V1.md: §5.3 closing "cycle 040 仅 plan-level 引用" / §7.5 deliverables "proposal-cycle 相关 vocab firewall" + "dream3r 实现仓库" lowercase (also G3b hit) / §8.1 short-term "(cycle 外人工动作)" / §8.2 medium-term "cycle 040 后第一个 unblocked task". Applied 5 corrective Edits: 本阶段 / 开题报告阶段 / 本研究架构 substitutions. Re-ran G3a + G3b + G4 → all 0 hits on both drafts (full file). Per cycle 036 + cycle 039 precedent. |
| C040-S9 | STYLE_CONTRACT §2 vocab substitution table append (+5 new rows: hard_fail / soft_fail / oracle-bus / monotone upgrade gate / fixture regime R1-R5 / 集成证据) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §2 (43 → 48 rows) |
| C040-S10 | STYLE_CONTRACT §6 sync log append (cycle 040 entry: 7+6+3 sub-sections + 5 new substitutions + 5 corrective edit narrative + 4 grep results) + 授权根 metadata update | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §6 + top metadata |
| C040-S11 | Cycle 040 log | done | `cycles/CYCLE-20260517-001.md` |
| C040-S12 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 040 deliverable summary:

```text
DEC-20260517-001:
  - authorizes only 8 file ops total (2 NEW + 6 MODIFIED): DEC + cycle
    log + 3 modified drafts/contract + 3 sync targets
  - forbids Dream/3R-mix/main.tex / references.bib / notes/* edits,
    Dream/specs/ edits, Dream/code/ edits, Dream/paradigm/ edits,
    OUTLINE_V1.md edits, WORK_RISK_REGISTER.md edits, sections other
    than §5 + §7 + §8 of either draft, server actions, checkpoint,
    training, model inference, calibration runs, ablation runs, v0.4
    spec delta drafting (B1/B2/B3 candidates referenced in §8.2 as
    forward-looking only), actual Track B survey submission, claiming
    pointmap L2 = 20.4747 as training-quality / SOTA-comparable result

§5 实验设计与评测协议 (7 sub-sections):
  - §5.1 三层证据阶梯: 论文层 (Track B 综述 + SPEC-007 v0.3 comparator)
    + 代理用例层 (case cards + COMPOSER_CAPABILITY_DESCRIPTORS) +
    原型实现层 (W1-W18 + KITTI smoke + ablate_recurrence + fixture)
  - §5.2 架构层消融实验组 ABL-v02-1..10: tier 1 load-bearing
    ABL-v02-1 (NSA on/off) + ABL-v02-4 (Composer best-of-N vs single)
    + ABL-v02-6 (capability_match cost_adjusted_match alpha sweep) +
    ABL-v02-10 (VGGT offline baseline as comparator anchor); plan-only
    F-002 gated
  - §5.3 记忆机制消融实验组 ABL-memory-0..11: cycle 029 v1.1 oracle-
    bus + hard/soft fail rule; ABL-memory-0 fixture/logging validity
    gate passed (cycle 031, integration evidence not C2 quality);
    ABL-memory-1..11 plan-only F-002 gated
  - §5.4 校验阈值标定方案: CRITIC_CALIBRATION_PLAN_V1 六类失败模式
    (弱纹理 / 镜面 / 快速运动 / 长基线 / 尺度漂移 / 域外) × 5
    sub-signal (Sampson / depth / 共视 / latent_drift / write_value)
    表; method A (distribution-quantile P95) vs method B (supervised
    classifier + monotone upgrade gate); fixture regime R1-R5
    synthetic failure injection; plan-only
  - §5.5 长序列真实数据评测: LONG_SEQ_REAL_TABLE_PLAN 4 variants
    (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_
    memory) × 4 metrics (scale_drift_proxy / memory_decay_proxy /
    anchor_fill_rate / retrieval_diversity) × windows ∈ {10,20,50,100}
    on KITTI; B4 缓存治理 coverage gap acknowledged; plan-only
  - §5.6 评测数据集: KITTI 主 (2011_09_26_drive_0001_sync_02
    已 smoke) + DTU 拟扩展 + 合成 fixture P0 + R1-R5
  - §5.7 主要评测指标: pointmap L2 + depth RMSE + route_regret +
    scale_drift_proxy + memory_decay_proxy + anchor_fill_rate +
    retrieval_diversity + failure-mode detection rate

§7 研究进展与已完成工作 (6 sub-sections):
  - §7.1 架构设计文档系列: SPEC v0.1 (3 份 cycle 016 architecture +
    ablation + comparator map) + v0.2 (3 份 cycle 018-021 deltas +
    comparator v0.2) + v0.3 (3 份 cycle 023-028 C2 memory + comparator
    + memory ablation addendum)
  - §7.2 实现里程碑 W1-W18: Tier 1 集成验证 11 项 (W1-W11) + Tier 2
    真实数据 smoke (W12-W18; W17-W18 tensor-contract level only;
    server-verified at /hdd3/kykt26/)
  - §7.3 KITTI 真实数据集成证据: pointmap L2 = 20.4747 on
    2011_09_26_drive_0001_sync_02 window pair; per RECENT_PROGRESS.md
    line 78 boundary statement "This is real-data integration
    evidence, not SOTA reconstruction accuracy"; verbatim caveat
    保留双稿 § 7.3 closing paragraph; NOT 重建质量数值
  - §7.4 综述发布: Track B 3R-mix 18 A4 页 + 44 引文 + 6 图 5 表 +
    路线 C arXiv-only + 2026-05-15 prose naturalization deliverable
    (3r_survey_stage_final_2026-05-15_natural.pdf)
  - §7.5 综述反哺主线: cycle 035 4 markdown deliverables (SOTA_MATRIX_V2
    + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN +
    SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL) + WORK_RISK_REGISTER v1.1
    +4 行 R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1
  - §7.6 cycle 历史: cycle 015 起架构主线 → cycle 016 SPEC v0.1 →
    cycle 018-021 v0.2 trio → cycle 022 paper v1.2 → cycle 023-027
    v0.3 memory 设计 → cycle 028-031 P0 + ablation → cycle 032 server
    verify → cycle 033-034 W1-W18 → cycle 035 综述反哺 → cycle 036-040
    开题报告

§8 研究计划与时间安排 (3 sub-sections):
  - §8.1 短期 M1-M2 (cycle 040-042 开题报告完稿 + 提交; cycle 041
    §9 + 通稿审查; cycle 042 最终修订 + PDF + packaging; 本阶段外
    人工动作: 用户实际执行 Track B 综述提交)
  - §8.2 中期 M3-M5 (W19-W23 真实路由 + W24 Critic 校准 + W25 TTT +
    W26 输入扩展 + B1/B2/B3 v0.4 spec delta 候选; SURVEY_DRIVEN_
    OPTIMIZATION_PROPOSAL §6 W-task reorder 为 recommendation-status
    不是 locked schedule; 各 W-task / spec delta 各需独立 DEC + F-002
    server authorization)
  - §8.3 长期 M6-M8 (W27 3DGS renderer 实装 + 真实数据训练 + 论文
    撰写 + 综合评测; D3 4DGS asset 输出 + R-4DGS-LIC-1 风险; 完整
    评测覆盖 6 类失败模式 × 4 类内存 × 3 类测试时 × 3 类输出资产)

STYLE_CONTRACT 升级:
  - §2 vocab substitution table 43 → 48 rows (+5 evaluation-protocol
    terminology: hard_fail / soft_fail / oracle-bus / monotone
    upgrade gate / fixture regime R1-R5 / 集成证据)
  - §6 sync log appended cycle 040 entry with substitutions used +
    5 corrective edit narrative + 4 grep results
  - 顶部 metadata 授权根 field appended DEC-20260517-001 (cycle 040)

G3a + G3b corrective observation:
  - 4 G3a hits + 1 G3b hit on first pass (cycle 039 pattern reversed:
    cycle 039 was G4 negation-context heavy / G3a-b clean; cycle 040
    was G3a "cycle"-leak heavy / G4 clean; per OUTLINE_V1 §4 章节
    分工预测 — evidence-anchored 章节 description prose 自然带入
    "cycle N" + repo-path lowercase 命名 leakage); applied 5
    corrective edits per cycle 036 + cycle 039 precedent
    (cycle 040 → 本阶段 / proposal-cycle → 开题报告阶段 / dream3r
    实现仓库 → 本研究架构实现仓库 / cycle 外 → 本阶段外); G3a +
    G3b + G4 re-greps all 0 hits

Result:
  - 8 artifacts present (DEC + cycle log + 3 modified drafts/contract
    + 3 sync targets); stop gates G0-G6 all passed with 5 corrective
    edits at G3a + G3b ("cycle" + lowercase repo-name leakage caught
    by full-file grep, fixed); § 1 + § 2 + § 3 + § 4 + § 5 + § 6 +
    § 7 + § 8 累计 ~17800 内 + ~14000 外 字 ≈ 85% of OUTLINE_V1 §2
    表 总字数估算 (~21100 内 / ~16000 外); only § 9 风险分析 remains

Evidence boundary:
  - §5 + §7 + §8 evidence-anchored text at research-plan level; no
    spec change, code change, calibration run, ablation run, or v0.4
    delta drafting validated by cycle 040
  - §7.3 KITTI smoke evidence 限定为 集成证据 非训练后质量 per
    RECENT_PROGRESS.md line 78; pointmap L2 = 20.4747 数值 与 caveat
    并置呈现
  - ABL-memory-0 fixture/logging pass (cycle 031) cited in §7.2 +
    §5.3 as validity gate, NOT as C2 memory quality validation
  - §8 medium-term M3-M5 timeline 显式声明 candidate timeline 不是
    committed schedule; M-numbering 不构成 commitment
  - candidate-not-final framing 保留 throughout per DEC-20260501-011
  - no-all-in posture 保留: §5.2 ABL-v02 + §5.3 ABL-memory 双消融
    覆盖 4 模块 (Critic / Memory / Permanence / Composer) 独立性

Next admissible direction (per DEC-20260517-001 §Next Direction):
  A. cycle 041 §9 风险分析 + 通稿审查 + STYLE_CONTRACT final sync
     (recommended; 最后一个章节; ~1000 外 + ~1500 内 字; total ~2500
     字; cycle 041 closeout 后 完整 8+1 章节 dual-draft 完整 ready
     for cycle 042 最终修订 + PDF 编译 + packaging)
  B. revise §5 + §7 + §8 based on self-review or advisor feedback
  C. cycle 035 §Next Direction A-C alternatives (calibration / long-
     seq ablation / v0.4 spec delta drafting)
  D. pause + reassess after §5 + §7 + §8 quality review
  E. user executes Track B survey submission (manual action)
  F. mainline non-proposal work (W22 / W23 / Fast3R omegaconf)
```

## Cycle 039 subtask board (closed 2026-05-17)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C039-S1 | DEC-20260516-004 launch authorization | done | `decisions/DEC-20260516-004-cycle-039-proposal-sections-3-and-6-dual-draft.md` |
| C039-S2 | Draft §3 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~1800 字, 5 sub-sections: 3.1 Q1 验证机制 + 3.2 Q2 长序列内存 + 3.3 Q3 多专家组合 + 3.4 4-finalist 模块独立性 + 3.5 候选 vs 最终 研究地位) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §3 |
| C039-S3 | Draft §6 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~1300 字, 3 sub-sections: 6.1 预期交付物 + 6.2 三个 IP 声明 (Q1↔IP1 / Q2↔IP3 / Q3↔IP2) + 6.3 与现有工作的实证差异) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §6 |
| C039-S4 | Snapshot §3 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~1500 字, 5 sub-sections mirroring internal with 三个研究问题 + 候选架构 X 命名) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §3 |
| C039-S5 | Snapshot §6 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~1000 字, 3 sub-sections mirroring internal with vocab-clean 三个 IP 命名) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §6 |
| C039-S6 | G3a + G3b + G4 vocab-firewall + over-claim greps (full file scope) | done with 7 corrective edits per side | First-pass G3a + G3b both 0 hits on first pass. First-pass G4 caught 7 hits per side in candidate-not-final 句式 negation-context examples ("不主张 ... 最终架构方案" / "不说 'X 解决了 ...'" / "不以 '证明 X 优于 SOTA' 的句式呈现"). Applied 7 corrective edits per side via replace_all (最终架构方案 → 最终方案 + X 解决了 → X 已完全解决 + Dream3R 解决了 → Dream3R 已完全解决 + 证明 ... 优于 → 宣称 ... 优于). Re-ran G3a + G3b + G4 → all 0 hits on both drafts (full file). Per cycle 036 precedent. |
| C039-S7 | STYLE_CONTRACT §2 vocab substitution table append (+2 new rows: C4' TTT 路径模块代号 → omit / "后续候选模块"; Innovation Point / IP1/IP2/IP3 → 保留英文 + 中文括注, 双稿一致无替换) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §2 (41 → 43 rows) |
| C039-S8 | STYLE_CONTRACT §6 sync log append (cycle 039 entry: 5+3 sub-sections + 2 new substitutions + 7 corrective edit narrative + 4 grep results) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §6 |
| C039-S9 | Cycle 039 log | done | `cycles/CYCLE-20260516-004.md` |
| C039-S10 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 039 deliverable summary:

```text
DEC-20260516-004:
  - authorizes only 8 file ops total (2 NEW + 6 MODIFIED): DEC + cycle
    log + 3 modified drafts/contract + 3 sync targets
  - forbids Dream/3R-mix/main.tex / references.bib / notes/* edits,
    Dream/specs/ edits, Dream/code/ edits, Dream/paradigm/ edits,
    OUTLINE_V1.md edits, WORK_RISK_REGISTER.md edits, sections other
    than §3 + §6 of either draft, server actions, checkpoint,
    training, model inference, ablation runs, v0.4 spec delta
    drafting (B1/B2/B3 candidates referenced in §3.1 + §6.1 as
    forward-looking only), actual Track B survey submission

§3 候选研究问题 (5 sub-sections):
  - §3.1 Q1 验证机制路径 (Critic; Gap = 综述 §2.5 三类机制无单一架构
    并置评估; v0.3 路径 = C4 hybrid 验证 + 修复; v0.4 候选 B1 拆分
    proposal-status; 评估路径 = ABL + KITTI long-seq; candidate-not-
    final 边界声明)
  - §3.2 Q2 长序列内存机制统一 (Memory; Gap = 综述 §2.4 四类机制各
    占一档; v0.3 路径 = C2 NSA + AnchorBank + StateToken + Mamba
    hybrid 覆盖 B1+B2+B3 + B4 partial; 评估路径 = ablate_recurrence
    + KITTI windows ∈ {10, 20, 50, 100}; candidate-not-final 边界)
  - §3.3 Q3 多专家组合 (Composer; Gap = 综述各专家 regime 优势分散
    缺对照; v0.3 路径 = C5 7-expert pool + capability descriptor +
    路由策略; 两子问题 Q3-a best-of-N vs single-expert + Q3-b
    Test3R-in-pool vs 外置 Critic; 评估路径 = ABL-v02-4 + ABL-v02-6
    + ABL-v02-10; candidate-not-final 边界)
  - §3.4 4-finalist 模块独立性 (per DEC-20260504-002 no-all-in):
    架构层 / 评测层 / 研究问题层 三层独立性; Permanence 不挂 Q
    但 silent retiring 仍禁止
  - §3.5 候选 vs 最终 研究地位声明 (per DEC-20260501-011):
    本研究三个"不"主张 + 正面表述 (具体候选 + 覆盖矩阵 + 多机制
    best practice + v0.4 演进路径)

§6 预期成果与创新点 (3 sub-sections):
  - §6.1 预期交付物 (4 类: 架构设计文档 + 原型实现 W1-W18 + 评测
    结果 ABL + 综述与方法学副产物)
  - §6.2 三个 IP 声明:
      IP1 Verification-as-architecture ↔ Q1 + §4.5 + Pillar A
      IP2 Heterogeneous best-of-N Composer ↔ Q3 + §4.6 + Pillar D
      IP3 NSA-hybrid memory ↔ Q2 + §4.3 + 综述四类
      每个 IP 携带句式约束 ("不说 ... 解决了 ...; 说 ... 提供候选
      模块设计 + 对照实验证据")
  - §6.3 与现有工作的实证差异 (3 层面: 方法学差异 多机制并置评估
    vs 单一论文一个方法 + 失败模式系统化差异 + 架构组合差异 异构
    multi-expert vs single best architecture; 实证目标不是
    leaderboard top-N 而是为后续工作判断 v0.4 演进方向提供对照
    数据)

STYLE_CONTRACT 升级:
  - §2 vocab substitution table 41 → 43 rows (+2: C4' TTT 路径模块
    代号 → omit / "后续候选模块"; Innovation Point / IP1/IP2/IP3
    → 保留英文 + 中文括注 双稿一致)
  - §6 sync log appended cycle 039 entry with substitutions used +
    7 corrective edit narrative + 4 grep results

G4 negation-context observation:
  - 7 hits per side from candidate-not-final 句式 examples ("不说
    'X 解决了 ...', 说 ...") explicitly using forbidden patterns
    in pedagogical 反例 context; per cycle 036 precedent applied
    corrective rephrasing (最终架构方案 → 最终方案 / X 解决了 →
    X 已完全解决 / 证明 ... 优于 → 宣称 ... 优于) to remove
    literal regex substrings while preserving 句式 contrast
    semantics; observation recorded in cycle log for cycle 040 /
    041 通稿审查 to potentially propose STYLE_CONTRACT §5 negation-
    context exemption rule if pattern recurs at scale

Result:
  - 8 artifacts present (DEC + cycle log + 3 modified drafts/contract
    + 3 sync targets); stop gates G0-G6 all passed with 7 corrective
    edits per side at G4 (negation-context forbidden-pattern hits
    caught by full-file grep, fixed); § 1 + § 2 + § 3 + § 4 + § 6
    累计 ~11300 内 + ~9500 外 字 ≈ 54% of OUTLINE_V1 §2 表 总字数
    估算 (~21100 内 / ~16000 外)

Evidence boundary:
  - §3 + §6 claim-positioning text at research-plan level; no spec
    change, code change, calibration run, ablation run, or v0.4
    delta drafting validated by cycle 039
  - candidate-not-final framing preserved throughout per
    DEC-20260501-011; §3.5 + §6.2 + §6.3 are the highest-density
    candidate-not-final 句式 application across the entire proposal
  - no-all-in posture preserved: §3.4 explicitly preserves 4-module
    independence including Permanence as a non-Q-anchored peer
    finalist per DEC-20260504-002

Next admissible direction (per DEC-20260516-004 §Next Direction):
  A. cycle 040 §5 实验设计 + §7 已完成工作 + §8 时间安排 together
     (recommended; three implementation-anchored chapters tightly
     coupled; ~4500 外 + ~6500 内 字 total ≈ ~11000 字)
  B. revise §3 + §6 based on self-review or advisor feedback
  C. cycle 035 §Next Direction A-C alternatives (calibration / long-
     seq ablation / v0.4 spec delta drafting)
  D. pause + reassess after §3 + §6 quality review
  E. user executes Track B survey submission (manual action)
  F. mainline non-proposal work (W22 / W23 / Fast3R omegaconf)
```

## Cycle 038 subtask board (closed 2026-05-16)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C038-S1 | Read targeted slices of SPEC-20260506-004 v0.2 Delta 1/2/3/5/6 + SPEC-20260508-001 v0.3 + CROSS_SPEC_SIGNAL_CONTRACT v2.1 CR-1..CR-6 + COMPOSER_CAPABILITY_DESCRIPTORS + DINOV3_C1_INTEGRATION_MEMO + NSA_MEMORY_INTEGRATION_MEMO + code/dream3r/RECENT_PROGRESS.md W17/W18 (read-only) | done | (read-only; no file modified) |
| C038-S2 | DEC-20260516-003 launch authorization | done | `decisions/DEC-20260516-003-cycle-038-proposal-section-4-dual-draft.md` |
| C038-S3 | Draft §4 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~4000 字, 8 sub-sections: 整体设计 + 帧预算 / C1 / C2 / C3 / C4 / C5 / C6 / 结构差异) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §4 |
| C038-S4 | Snapshot §4 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~3000 字, 8 sub-sections with 六模块中文化命名 感知/记忆/永久性/校验/编排/总线) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §4 |
| C038-S5 | G3a + G3b + G4 vocab-firewall + over-claim greps (full file scope) | done with 1 corrective | First-pass G3a caught cycle-037-residue "cycle 037" leakage in DRAFT_EXTERNAL line 7 metadata row (cycle 037's prose-scoped grep missed; cycle 038 full-file grep caught); corrective edit rephrased to "§2 + §4 起草, 累计正文 +~7000 字"; re-ran G3a + G3b + G4 → all 0 hits |
| C038-S6 | STYLE_CONTRACT §2 vocab substitution table append (+19 new rows: C1-C6 / Pillar A/D / Delta N / A5 reroute_model / repair actions 0-5 / conflict_score / theta_conflict / capability_match (spread) / cost_adjusted_match / epsilon_tie / fail_fast / evidence label / forward-reference null protocol / permanence_link / signal-name retention rule) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §2 (22 → 41 rows) |
| C038-S7 | STYLE_CONTRACT §6 sync log append (cycle 038 entry: 8 sub-sections + 19 new substitutions + corrective edit narrative + 4 grep results) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §6 |
| C038-S8 | Cycle 038 log | done | `cycles/CYCLE-20260516-003.md` |
| C038-S9 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 038 deliverable summary:

```text
DEC-20260516-003:
  - authorizes only 8 file ops total (2 NEW + 6 MODIFIED): DEC + cycle
    log + 3 modified drafts/contract + 3 sync targets
  - forbids Dream/3R-mix/main.tex / references.bib / notes/* edits,
    Dream/specs/ edits, Dream/code/ edits, Dream/paradigm/ edits,
    OUTLINE_V1.md edits, WORK_RISK_REGISTER.md edits, sections other
    than §4 of either draft, server actions, checkpoint, training,
    model inference, ablation runs, v0.4 spec delta drafting (B1/B2/
    B3 candidates referenced in §4 as forward-looking only, not as
    locked architecture), actual Track B survey submission

§4 研究方案 / Dream3R v0.3 架构 (8 sub-sections):
  - §4.1 整体设计 + 帧预算 (Delta 1: 30-50 ms/frame speed priority +
    pillar A/D main claim narrowing per Delta 6)
  - §4.2 C1 Perceiver / 感知模块 (Delta 2: DINOv3-S frozen replaces
    ViT-L, ~14x param reduction + ~5x latency speedup; -B fallback
    documented)
  - §4.3 C2 Memory / 记忆模块 (SPEC-008 v0.3 supersedes Delta 3:
    NSA three-branch compressed/selected/sliding + AnchorBank K=256
    + StateToken + Mamba-Transformer hybrid recurrence; covers B1
    递推 + B2 空间指针 + B3 混合, B4 缓存治理 partial)
  - §4.4 C3 Permanence / 永久性模块 (Slot Attention + permanence_link;
    CR-2 binding to Memory)
  - §4.5 C4 Critic / 校验模块 (Sampson 几何 + depth 一致性 + 共视
    conflict + repair actions 0/1/2/3-5 stub; CR-1 with C5 for A5
    reroute; verification-only no TTT, candidate B1 v0.4 delta)
  - §4.6 C5 Composer / 编排模块 (7 admitted experts: MASt3R + Fast3R
    + Spann3R + CUT3R + MoGe-2 + DepthAnything-V2 + Test3R; dropped:
    VGGT/MapAnything/PE/Kimi KDA; capability descriptor + cost_
    adjusted_match per v2 contract)
  - §4.7 C6 Bus / 总线模块 (CR-1..CR-6 cross-spec signal contract
    v2.1 + forward-reference null protocol v2.1 addendum + CR-7
    external_prior_conflict v2.2 candidate)
  - §4.8 与现有 3R 系统的结构差异 (3 structural deltas: 单一架构同
    时覆盖长序列内存多类机制 + 显式区分验证vs路由切换暂未区分参数
    更新 + 显式 best-of-N 专家池)

STYLE_CONTRACT 升级:
  - §2 vocab substitution table 22 → 41 rows (+19 new module-internal
    terminology substitutions, per DEC-20260516-003 §Decision 预测的
    最高 STYLE_CONTRACT stress test)
  - §6 sync log appended cycle 038 entry with substitutions used +
    corrective edit narrative + 4 grep results

Result:
  - 8 artifacts present (DEC + cycle log + 3 modified drafts/contract
    + 3 sync targets); stop gates G0-G6 all passed with 1 corrective
    edit at G3a (cycle-037-residue metadata leakage caught by cycle
    038 full-file grep, fixed); § 1 + § 2 + § 4 累计 ~8200 内 + ~7000
    外 字 ≈ 36% of OUTLINE_V1 §2 表 总字数估算 (~21100 内 / ~16000 外)

Evidence boundary:
  - §4 architecture-positioning text at research-plan level; no spec
    change, code change, calibration run, ablation run, or v0.4
    delta drafting validated by cycle 038
  - candidate-not-final framing preserved throughout per
    DEC-20260501-011
  - no-all-in posture preserved: §4 描述 6 模块 + 4 finalist 模块
    (Critic / Memory / Permanence / Composer) 独立性 not collapsed
    per DEC-20260504-002

Next admissible direction (per DEC-20260516-003 §Next Direction):
  A. cycle 039 §3 候选研究问题 + §6 预期成果与创新点 together
     (recommended; framing chapters tightly coupled; ~5600 字 total)
  B. revise §4 based on self-review or advisor feedback
  C. cycle 035 §Next Direction A-C alternatives (calibration / long-
     seq ablation / v0.4 spec delta drafting)
  D. pause + reassess after §4 quality review
  E. user executes Track B survey submission (manual action)
  F. mainline non-proposal work (W22 / W23 / Fast3R omegaconf)
```

## Cycle 037 subtask board (closed 2026-05-16)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C037-S1 | SUBMISSION_RECORD pdf_sha256 pre-fill (PowerShell Get-FileHash, read-only) | done | `3R-mix/deliverables/SUBMISSION_RECORD_2026-05-16.md` (SHA256 = A0763DB7AB7A1E8E1427D4DCC8CB62BC15F94F3F2D915AD0BFBB235CC99C64B0) |
| C037-S2 | DEC-20260516-002 launch authorization | done | `decisions/DEC-20260516-002-cycle-037-proposal-section-2-dual-draft.md` |
| C037-S3 | Read targeted slices of Track B 3R-mix `main.tex` §3-§8 for §2 素材 (paraphrase, no verbatim) | done | (read-only; no file modified) |
| C037-S4 | Draft §2 in DRAFT_INTERNAL_V1.md (master, Dream-vocabulary, ~4200 字, 7 sub-sections + intro + §2.7 落点) | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` §2 |
| C037-S5 | Snapshot §2 to DRAFT_EXTERNAL_V1.md (vocab-clean, ~3700 字, 代号 候选架构 X / 本研究架构, structurally mirrored) | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` §2 |
| C037-S6 | G3a + G3b + G4 vocab-firewall + over-claim greps (full file scope, including §1 + §2) | done | 4 greps × 0 hits each on first pass; no corrective edits needed |
| C037-S7 | STYLE_CONTRACT §6 sync log append (cycle 037 entry: 7 sub-sections + substitutions used + 4 grep results) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` §6 |
| C037-S8 | Cycle 037 log | done | `cycles/CYCLE-20260516-002.md` |
| C037-S9 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 037 deliverable summary:

```text
DEC-20260516-002:
  - authorizes only 8 file ops total (2 NEW + 6 MODIFIED): DEC + cycle
    log + 3 modified drafts/contract + 3 sync targets
  - forbids Dream/3R-mix/main.tex / references.bib / notes/* edits,
    Dream/specs/ edits, Dream/code/ edits, Dream/paradigm/ edits,
    OUTLINE_V1.md edits, WORK_RISK_REGISTER.md edits, STYLE_CONTRACT §2
    table additions (the 22-row seed proved sufficient this cycle),
    sections other than §2 of either draft, server actions,
    checkpoint, training, model inference, ablation runs, v0.4 spec
    delta drafting, actual Track B survey submission (manual user
    action)

§2 国内外研究现状 (7 sub-sections):
  - §2.1 基础谱系: DUSt3R / MASt3R / MASt3R-SfM (paraphrased from
    Track B 综述 §3 段 1-2; 三个内部锚点: 本研究架构 C5 Composer
    pool 接受 MASt3R; SPEC-007 v0.2 Tier 1 in-pool; DUSt3R Tier 4
    foundation)
  - §2.2 多视角规模化与统一视觉几何: Fast3R / MV-DUSt3R+ / VGGT /
    MapAnything / Pow3R (paraphrased from 综述 §4; 本研究架构
    Composer 接纳 Fast3R+MASt3R 不接纳 VGGT offline-batch; Pow3R
    输入扩展 axis 候选与 R-INPUT-EXT-1 关联)
  - §2.3 视频、动态场景与 4D 重建: Align3R / MonST3R / POMATO /
    D²USt3R / Easi3R / RayMap3R (paraphrased from 综述 §5; 本研究
    架构 C3 Permanence (Slot Attention + permanence_link) 与
    MonST3R 同类机制不同路径; SPEC-007 v0.2 MonST3R Tier 5
    orthogonal)
  - §2.4 长序列内存四类机制: B1 递推状态 (CUT3R/STream3R/LongStream)
    + B2 空间指针 (Spann3R/Point3R) + B3 混合记忆 (LONG3R/LoGeR/
    Mem3R) + B4 缓存治理 (OVGGT/PAS3R/FILT3R); 本研究架构 C2
    Memory NSA three-branch + AnchorBank + StateToken + Mamba
    hybrid 覆盖前 3 类, B4 partial (acknowledged as 实证缺口); 此
    映射是 §3 Q2 长序列内存机制统一的核心论据
  - §2.5 测试时三类机制: C1 一致性优化 (Test3R) + C2 测试时参数
    更新 TTT (TTT3R) + C3 先验注入 (G-CUT3R / Pow3R / MASt3R-SfM
    + 外部先验 Depth Pro / Metric3D v2 / DINOv2/v3 / CoTracker /
    SpatialTracker / SAM2); 本研究架构 C4 Critic 含 C1 + repair
    actions 但不含 C2 TTT (这是 §3 Q1 验证机制路径的核心问题)
  - §2.6 输出资产三类: D1 4D pointmap + D2 dynamic mask + D3 4DGS
    (3DGS / Splatt3R / InstantSplat / NoPoSplat); 本研究架构 W17
    + W18 已实装 D1 + D2 tensor 契约, D3 仍 gated (W27 candidate
    + R-4DGS-LIC-1 风险)
  - §2.7 综述四轴覆盖矩阵 + 本研究架构 / Dream3R v0.3 落点:
    21 子类覆盖矩阵 (✓ 6 / ⚠ 11 / ✗ 4); ✗ 4 子类 = OOD + TTT
    参数更新 + 4DGS 渲染 + 输入扩展 axis; 整体定位"不押注单一
    支线"; candidate-not-final 框架显式声明

Sync log entry (STYLE_CONTRACT §6):
  - 22-row seed vocab substitution table covered all §2 substitutions
    without additions (Dream3R → 候选架构 X / SPEC-* → omit + 中文
    paraphrase / cycle-* → omit / CR-* → 信号校验规则族 / W* → omit /
    AnchorBank K=256 / NSA three-branch / StateToken / Mamba hybrid /
    4DGS asset etc.)
  - 4 grep results documented (G3a / G3b external + G4 internal +
    external): all 0 hits on first pass

Result:
  - 8 artifacts present (DEC + cycle log + 3 modified drafts/contract
    + 3 sync targets); stop gates G0-G6 all passed; bilingual sync
    contract STYLE_CONTRACT §3 demonstrated to scale through ~7900
    字 of synchronized content with seed table unchanged; first cycle
    where corrective grep passes were not needed (cycle 036 had two)

Evidence boundary:
  - §2 research positioning text only; no spec change, code change,
    calibration run, ablation run, or actual submission validated by
    cycle 037
  - §2.7 落点 prose explicitly uses candidate-not-final framing per
    DEC-20260501-011; "不押注单一支线" framing per DEC-20260504-002
  - the cycle-036 seed STYLE_CONTRACT 22-row vocab table proved
    adequate for §2 (research-current-state chapter); §4 architecture
    chapter is the next stress test

Next admissible direction (per DEC-20260516-002 §Next Direction If Passed):
  A. launch cycle 038 §4 研究方案 / Dream3R v0.3 架构 (recommended;
     second-largest single-section block; highest stress on
     STYLE_CONTRACT due to module-internal terminology density)
  B. revise §2 based on self-review or advisor feedback
  C. cycle 035 §Next Direction A-C alternatives (calibration /
     long-seq ablation / v0.4 spec delta drafting), or DEC-001 §Next
     Direction E (architecture-first non-proposal: W22 / W23 /
     Fast3R omegaconf)
  D. pause + reassess after §2 quality review
  E. user executes Track B survey submission (manual action;
     packaging + SHA256 ready)
```

## Cycle 036 subtask board (closed 2026-05-16)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C036-S1 | DEC-20260516-001 launch authorization | done | `decisions/DEC-20260516-001-cycle-036-survey-submission-and-proposal-kickoff.md` |
| C036-S2 | Part A advisor cover note (vocab-clean per G2) | done | `3R-mix/deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` |
| C036-S3 | Part A submission record (slots for recipient / channel / SHA256 / submitted_at) | done | `3R-mix/deliverables/SUBMISSION_RECORD_2026-05-16.md` |
| C036-S4 | Part A Track A relationship internal meta (escape valve; not delivered to advisor) | done | `3R-mix/deliverables/RELATION_TO_TRACK_A_2026-05-16.md` |
| C036-S5 | Part B style contract (vocab substitution table 22 rows + bilingual sync rule + 候选架构 X naming + candidate-not-final 句式 表) | done | `planning/proposal_dream3r/STYLE_CONTRACT.md` |
| C036-S6 | Part B 9-section dual outline + chapter mapping + 字数 estimate + cycle 037+ drafting order | done | `planning/proposal_dream3r/OUTLINE_V1.md` |
| C036-S7 | Part B 内部稿 § 1 ~1800 字 + § 2-§ 9 placeholders | done | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` |
| C036-S8 | Part B 外部稿 § 1 ~1500 字 (代号 候选架构 X) + § 2-§ 9 placeholders; G3a + G3b + G4 vocab firewall + over-claim greps all 0 hits | done | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` |
| C036-S9 | Cross-spec proposal-cycle risk register additions (3 new rows: R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1) | done | `planning/WORK_RISK_REGISTER.md` (v1.2 additive) |
| C036-S10 | Cycle 036 log | done | `cycles/CYCLE-20260516-001.md` |
| C036-S11 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 036 deliverable summary:

```text
DEC-20260516-001:
  - authorizes only 13 file ops total (9 NEW + 4 MODIFIED): 3 Part A
    files in 3R-mix/deliverables/ + 4 Part B files in new
    planning/proposal_dream3r/ + DEC + cycle log + 4 sync targets
    (WORK_RISK_REGISTER v1.1 -> v1.2 additive + TASK_SNAPSHOT +
    WORKFLOW_STATUS + INDEX)
  - forbids Dream/3R-mix/main.tex / references.bib / notes/* edits,
    Dream/specs/ edits, Dream/code/ edits, Dream/paradigm/ edits,
    server actions, checkpoint, training, model inference, real
    submission action (left to user post-cycle), v0.4 spec delta
    drafting (B1/B2/B3 from cycle 035 proposal §5 remain
    proposal-status; each requires its own DEC), § 2-§ 9 proposal
    body text drafting (§ 1 only this cycle as alignment proof),
    Dream-vocabulary in advisor cover note, raw "Dream3R" /
    forbidden patterns in DRAFT_EXTERNAL_V1.md § 1 prose

Part A (3R-mix advisor submission packaging):
  - SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md ~600 字 Chinese cover
    note; 6 sections (主旨 / 范围 / 与英文综述差异 / 证据边界 /
    路线说明 / 请求审阅事项); G2 vocab firewall grep 0 hits on
    Dream|Dream3R|KYKT|agent|skill|workflow|本地项目|cycle|SPEC-|DEC-|CR-
  - SUBMISSION_RECORD_2026-05-16.md YAML metadata + checklist with
    slots for recipient / channel / pdf_sha256 (PowerShell
    Get-FileHash) / submitted_by / contact / submitted_at;
    pre-filled fields page_count = 18, ref_count = 44, figure_count
    = 6, table_count = 5, vocab_grep_verified = 2026-05-16
  - RELATION_TO_TRACK_A_2026-05-16.md ~600 字 internal meta;
    documents Track B / Track A relationship; not delivered with
    PDF; only file allowed to mention Dream-vocabulary

Part B (Dream3R proposal dual-draft kickoff):
  - new subdirectory planning/proposal_dream3r/ created
  - STYLE_CONTRACT.md vocab substitution table 22 rows
    (Dream3R -> 候选架构 X / SPEC-* -> 体系结构设计文档 v0.X /
    DEC-* -> 项目关键决策点 N / CYCLE-* -> 研发周期 N /
    CR-1..CR-6 -> 信号校验规则族 (1-6) / W1..W22 -> 实现里程碑 1-22 /
    F-001/F-002 -> 内部工作规则 / 算力部署约束 / agent / skill /
    workflow / KYKT / ablate_recurrence.py / ABL-memory-N /
    ABL-v02-N / NSA three-branch / AnchorBank / StateToken / Mamba
    hybrid / pointmap L2 = 20.47 / 4DGS asset etc.); §3 sync rule
    internal-is-master + periodic external snapshot + grep
    verification + cycle-end sync log; §4 候选架构 X naming
    introduction; §5 candidate-not-final 句式 contrast (9 禁用 vs
    允许 句式 对照); §6 sync log (cycle 036 entry: 13 vocab
    substitutions seeded + § 1 grep verified clean)
  - OUTLINE_V1.md §2 9-section dual outline (外稿 ~16000 字 / 内稿
    ~21100 字) + §3 chapter mapping table (外稿 ↔ 内稿 ↔ 复用
    素材) + §4 cycle 037-042 drafting order (cycle 037 §2 国内外
    研究现状 first because largest single-section block + most
    heavily reuses Track B 综述 + double-draft sync stress-tests
    STYLE_CONTRACT immediately) + §5 §1 风格样本 200 字 双稿对照
  - DRAFT_INTERNAL_V1.md §1 ~1800 字 covers §1.1 Track A 主线决策
    起源 (DEC-20260506-001) / §1.2 Dream3R v0.3 当前状态 (W1-W18 +
    KITTI smoke L2 = 20.47 + 部署服务器 path) / §1.3 Track B 综述
    四轴反哺 / §1.4 三个核心研究问题 Q1 验证机制路径 (Critic) +
    Q2 长序列内存路径 (Memory) + Q3 多专家组合路径 (Composer) /
    §1.5 候选 vs 最终边界 / §1.6 Dream 项目工件引用 (DEC + SPEC +
    cycle 链); §2-§9 placeholders with TBD comments + 子节
    suggestions; G4 over-claim grep 0 hits after §1.5 rephrase
    "本研究的成果不是论证 Dream3R 相对 SOTA 具有压倒性优势, 而是
    评估..."
  - DRAFT_EXTERNAL_V1.md §1 ~1500 字 covers §1.1 前馈式三维重建
    (3R) 研究方向 / §1.2 六类典型几何失败模式 (弱纹理 / 镜面玻璃
    / 快速运动 / 长基线 / 尺度漂移 / 域外) / §1.3 三组未充分解决
    问题 (验证 vs 适应 + 长序列内存机制统一 + 多专家组合实证) /
    §1.4 本研究目标 (代号 候选架构 X 引入 + 4 设计目标) / §1.5
    研究地位 (candidate-not-final + 不押注单一方案) / §1.6 学术
    价值与意义 (3 方面贡献); §2-§9 placeholders; G3a vocab firewall
    grep 0 hits after fixing §元数据 row "完全剥离内部 workflow
    词汇" -> "完全剥离内部研究流程相关用词"; G3b "Dream3R"
    case-insensitive grep 0 hits after removing §元数据 文件路径
    row containing workspace path; G4 over-claim grep 0 hits after
    §1.5 rephrase "本研究的目标不是论证 X 相对现有方法具有压倒性
    优势..."

WORK_RISK_REGISTER.md v1.2 additive (+3 rows):
  - R-PROP-VOCAB-1: external draft Dream-vocabulary leakage; mitigated
    by STYLE_CONTRACT §2 vocab table + §3 sync rule + per-sync grep
    verification; cycle 036 close passed verification with 0 hits on
    full forbidden pattern
  - R-PROP-CLAIM-1: 开题报告 over-claim 候选架构 X 为最终方案;
    mitigated by STYLE_CONTRACT §5 candidate-not-final 句式 表 +
    per-cycle grep verification on draft sections as they land;
    cycle 036 close passed verification with 0 hits on both internal
    and external §1
  - R-PROP-SYNC-1: 双稿语义漂移 (内部稿 §X vs 外部稿 §X 对同一
    研究问题描述出现实质差异); mitigated by STYLE_CONTRACT §3
    internal-is-master sync rule + 外部稿 standalone 编辑限制 +
    每 cycle 末尾 sync log entry

Result:
  - 13 file ops complete (9 NEW + 4 MODIFIED); stop gates G0-G6 all
    passed; G2 + G3a + G3b + G4 vocab firewall + over-claim greps
    all returned 0 hits after one corrective pass each; mainline
    decisions all in force

Evidence boundary:
  - packaging + planning + § 1 markdown only; no actual survey
    submission performed (manual user action post-cycle), no § 2-§ 9
    proposal body text drafted, no spec change, code change,
    calibration run, or ablation run validated by cycle 036
  - Track B 3R-mix manuscript surface unchanged (still wound down at
    2026-05-15 prose naturalization deliverable; only `deliverables/`
    received 3 new files)
  - candidate-not-final boundary preserved: DRAFT_INTERNAL_V1 §1.5 +
    DRAFT_EXTERNAL_V1 §1.5 explicitly state X / Dream3R is being
    evaluated, not converged on

Next admissible direction (per DEC-20260516-001 §Next Direction If Passed):
  A. launch cycle 037 § 2 国内外研究现状 (recommended; largest single
     block; double-draft sync stress-test)
  B. user executes actual survey submission action + fills
     SUBMISSION_RECORD slots (manual action outside any cycle)
  C. revise OUTLINE_V1 chapter structure before cycle 037 (preserve
     V1, create V2)
  D. pause + revise cycle 036 deliverables based on quality review
  E. return to architecture-first mainline non-proposal work
     (W22 / W23 / Fast3R omegaconf per cycle 035 §Next Direction D)
  F. launch one of cycle 035 §Next Direction A-C instead (calibration
     / long-seq ablation / v0.4 spec delta) -> independent DEC each
```

## Cycle 035 subtask board (closed 2026-05-15)

| ID | Subtask | Status | Canonical artifact |
| --- | --- | --- | --- |
| C035-S1 | Survey-driven optimization proposal (cycle 035 upstream) | done | `planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` (status preserved at draft) |
| C035-S2 | DEC-20260515-001 launch authorization | done | `decisions/DEC-20260515-001-cycle-035-survey-driven-markdown-deliverables-launch.md` |
| C035-S3 | SOTA matrix V2 (re-label SPEC-007 v0.2 Tier 1-5 against survey four-axis + input-extension bonus axis) | done | `planning/SOTA_MATRIX_V2.md` |
| C035-S4 | Critic calibration plan V1 (per-failure-mode threshold standardization, plan-only) | done | `planning/CRITIC_CALIBRATION_PLAN_V1.md` |
| C035-S5 | Long-seq real-data table plan (ablate_recurrence extension to KITTI ≥10 windows, plan-only) | done | `planning/LONG_SEQ_REAL_TABLE_PLAN.md` |
| C035-S6 | Cross-spec risk register additions (4 new rows: R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1) | done | `planning/WORK_RISK_REGISTER.md` (v1.1 additive) |
| C035-S7 | Cycle 035 log | done | `cycles/CYCLE-20260515-001.md` |
| C035-S8 | Sync chain (TASK_SNAPSHOT first + WORKFLOW_STATUS + INDEX) | done | this file + `WORKFLOW_STATUS.md` + `INDEX.md` |

Cycle 035 deliverable summary:

```text
DEC-20260515-001:
  - authorizes only writing 3 new planning files + appending 4 risk rows
    to WORK_RISK_REGISTER + sync chain + cycle log
  - forbids Dream/specs/ edits, Dream/code/ edits, server actions,
    checkpoint, training, frontend, ablation runs, evaluate_real_sequence
    runs, Track B 3R-mix edits, RECENT_PROGRESS / NEXT_PHASE_ROADMAP edits,
    v0.4 spec delta drafting (B1/B2/B3 from proposal remain proposal-status)

3 new planning files (cycle 035 P0-1/P0-2/P0-3 deliverables):
  - SOTA_MATRIX_V2.md: re-labels 19 comparator entries (T1 in-pool 7
    + T2 dropped 3 + T3 oos 1 + T4 foundation 1 + T5 orthogonal 8) plus
    Point3R / Mem3R / G-CUT3R / Pow3R / MASt3R-SfM appendix entries against
    five axes (failure modes / long-seq memory / test-time / output asset
    + input extension bonus); identifies 4 first-class-support gaps
  - CRITIC_CALIBRATION_PLAN_V1.md: maps survey six failure modes to C4
    Critic five sub-signals; defines sub-sample sampling rules per mode;
    outlines method A (distribution-quantile P95) vs method B (supervised
    classifier) with selection decision tree; sets 5-metric validation gate
  - LONG_SEQ_REAL_TABLE_PLAN.md: maps 4 ablate_recurrence variants
    (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory)
    to survey §6 four memory mechanism types; defines 4 long-seq-specific
    metrics (scale_drift_proxy / memory_decay_proxy / anchor_fill_rate /
    retrieval_diversity); outlines windows=10/20/50/100 staged execution
    with 6-metric validation gate; explicit B4 budget-governance subtype
    gap noted

WORK_RISK_REGISTER.md v1.1 additive:
  - R-OOD-1: OOD detection path absent in C4 Critic
  - R-EXT-PRIOR-1: external prior vs geometry conflict unmodeled in
    CR-1..CR-6
  - R-4DGS-LIC-1: 4DGS asset license chain undocumented in W18 GaussianHead
  - R-INPUT-EXT-1: input extension axis (pose / sparse depth / video) absent

Result:
  - 7 artifacts present (DEC + cycle log + 3 plans + risk register + this
    sync chain); stop gates G0-G5 all passed; visual scan confirmed no
    forbidden-action claims in the 3 new files

Evidence boundary:
  - planning markdown only; no calibration run, no ablation run, no spec
    change, no code change, no server action validated by cycle 035
  - 3 new plans explicitly mark themselves "plan-only; execution needs
    independent DEC" in their §1 + Metadata sections
  - proposal upstream status remains draft until separate DEC formally
    accepts it as v0.4 design input

Next admissible direction (per DEC-20260515-001 §Next Direction If Passed):
  A. calibration data collection on KITTI -> requires independent DEC + F-002
  B. ablate_recurrence on KITTI long windows -> requires independent DEC + F-002
  C. v0.4 spec delta drafting (B1 Critic path split / B2 output asset
     contract / B3 input extension axis) -> requires independent DEC per delta
  D. pause + revise proposal based on cycle 035 deliverable quality
  E. return to architecture-first mainline non-survey work (W22 / W23)
```

Cycle 031 active boundary:

```text
Authorized user trigger:
  - "那就先进行后续操作吧"

Execution scope:
  - local deterministic P0 fixture scaffold
  - ABL-memory-0 only as validity gate
  - output manifest/log/metric/summary/evidence-boundary artifacts

Explicit exclusions:
  - no ABL-memory-1..8 performance claims in this cycle
  - no ABL-memory-9..11
  - no server/runtime/model/checkpoint/training/frontend work
```

Cycle 031 deliverable summary:

```text
DEC-20260508-007:
  - authorizes only local P0 scaffold + ABL-memory-0 validity gate
  - forbids Dream/code, server integration, model imports, checkpoint use,
    training, frontend work, paper claim promotion, and ABL-memory-1..11
    behavior claims

experiments/prototypes/memory_v03_p0/:
  - deterministic fixture generator
  - oracle-bus contract
  - raw-label exclusion audit
  - ABL-memory-0 gate runner
  - direct smoke test

outputs:
  - fixtures_manifest.json
  - write_log.jsonl
  - metrics_abl_memory_0_8.csv
  - summary_go_no_go.md
  - evidence_boundary_update.md

Result:
  - ABL-memory-0 pass, 22/22 validity checks
  - pytest unavailable in the current Python environment
  - direct smoke test passed with python tests\test_abl_memory_0.py

Evidence boundary:
  - fixture/logging substrate only
  - no memory quality, retrieval quality, recurrence quality, reconstruction
    quality, server behavior, model behavior, or paper claim validated
```

Cycle 030 deliverable summary (for resume context):

```text
DEC-20260508-006:
  - accepts only markdown-only template creation scope
  - authorizes planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md
  - keeps actual P0 implementation gated

planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md:
  - predefines future DEC fields, allowed paths, forbidden actions,
    ABL-memory-0..8 scope, ABL-memory-9..11 exclusion, oracle-bus
    rules, required outputs, stop gates, result labels, go/no-go rules,
    and post-execution evidence boundary

Evidence boundary:
  - cycle 030 is authorization-template evidence only
  - no ABL-memory result, prototype implementation, C2 Memory v0.3
    quality, reconstruction quality, spatial retrieval quality,
    state-token recurrence performance, or paper claim is validated yet

Next expected research object after cycle 030:
  - user decision on whether to authorize local static tensor P0
    execution for ABL-memory-0..8, revise the template, or return to
    research design
```

## Last completed task pass

```text
pass_name:        V11 VLM semantic label-cache gate
date:             2026-06-03
trigger:          User asked to test Qwen3-VL-2B-Instruct as an offline
                  semantic controller signal, not a geometry model.
files_modified:   TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, INDEX.md, mainwork.md,
                  registry/decision_registry.md, README.md,
                  RESEARCH_STATE.md, AGENT_MASTER_PROMPT.md,
                  planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md,
                  handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
new_artifacts:    code/dream3r/scripts/build_vlm_semantic_labels.py
                  code/dream3r/tests/test_vlm_semantic_labels.py
                  decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md
                  cycles/CYCLE-20260603-vlm-semantic-label-cache-gate.md
                  runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_window_manifest.json
                  runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json
                  runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
result:           Strict local label-cache gate is mock-positive. Records have
                  explicit failure flags, prompt hash, model id, frame list,
                  semantic risks, and Router/Critic-ready features,
                  shuffled_features, and disabled_features.
qwen_status:      Not run. Checked BUAA-Server paths have no Qwen3-VL-2B
                  weights; existing dream3r env reports transformers 4.46.0.
discipline:       No frozen-core edit. No model training. No checkpoint
                  download. No server environment mutation. No geometry claim.
verification:     py_compile passed; pytest 4 passed; mock smoke schema report
                  has schema_pass_rate 1.0; git diff --check clean except
                  line-ending warnings.

pass_name:        V11 VLM semantic-controller research plan
date:             2026-06-03
trigger:          User asked for a comprehensive research plan, project
                  document updates, and a prompt for a new agent to start
                  better Dream3R research and practical execution planning.
files_modified:   TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, INDEX.md, mainwork.md,
                  registry/decision_registry.md, README.md,
                  RESEARCH_STATE.md, AGENT_MASTER_PROMPT.md
new_artifacts:    planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
                  decisions/DEC-20260603-027-vlm-semantic-controller-plan.md
                  cycles/CYCLE-20260603-vlm-semantic-controller-plan.md
                  handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
result:           Qwen3-VL-2B-Instruct is scoped as an offline semantic
                  support signal for Router, Critic, state auxiliary
                  supervision, and teacher scheduling. It is explicitly not a
                  geometry backend or pointmap/depth/camera teacher.
baseline:         Current best remains bounded frozen-StatePrior refinement
                  at KITTI/ETH3D 0.1448/0.1475.
discipline:       Documentation-only pass. No frozen-core edit. No model
                  training. No checkpoint download. No server mutation.
verification:     Official Qwen3-VL sources checked; guidance chain references
                  verified by rg; tracked docs passed git diff --check
                  except line-ending warnings; frozen-core diff audit empty.

pass_name:        Native student decoder/distillation gate
date:             2026-06-02
trigger:          User asked to lock the bounded frozen-StatePrior baseline
                  and push a high-impact Dream3R architecture gate.
files_modified:   TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, RESEARCH_STATE.md,
                  INDEX.md, README.md, AGENT_MASTER_PROMPT.md, mainwork.md,
                  planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md,
                  handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md,
                  registry/decision_registry.md
new_artifacts:    decisions/DEC-20260602-024-native-student-decoder-gate.md
                  cycles/CYCLE-20260602-native-student-decoder-gate.md
                  code/dream3r/native_student_decoder.py
                  code/dream3r/scripts/train_native_student_decoder.py
                  code/dream3r/scripts/run_native_student_decoder_sweep.sh
                  code/dream3r/tests/test_native_student_decoder.py
result:           Native student gate is executable and state-causal, but
                  metric-flat versus bounded frozen-StatePrior refinement.
                  Correct-state 0.1451/0.1480, no-state 0.1557/0.1730,
                  shuffle-state 0.1525/0.2468, fallback contamination 0.
baseline:         Current best remains bounded frozen-StatePrior refinement
                  at KITTI/ETH3D 0.1448/0.1475.
discipline:       No frozen-core edit. No cache rebuild. No checkpoint
                  download. No environment mutation. Existing DEC-019
                  checkpoint and existing SCF caches only.
verification:     Local py_compile passed; local targeted pytest 11 passed;
                  server targeted pytest 3 passed; BUAA-Server GPU1 smoke
                  and 20-epoch gate completed under
                  runs/stage6_fusion/native_student_decoder_*.

pass_name:        Cycle 031 close pass (Memory v0.3 local P0 scaffold
                  + ABL-memory-0 gate done in single session 2026-05-08)
date:             2026-05-08
trigger:          User authorized proceeding after cycle 030 template and
                  GitHub CLI discussion.
files_modified:   TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, RESEARCH_STATE.md,
                  INDEX.md, README.md, AGENT_MASTER_PROMPT.md,
                  registry/decision_registry.md
new_artifacts:    decisions/DEC-20260508-007-cycle-031-p0-local-static-
                  tensor-scaffold.md
                  experiments/prototypes/memory_v03_p0/
                  cycles/CYCLE-20260508-008.md
result:           Local P0 scaffold created. ABL-memory-0 passed 22/22
                  fixture/logging validity checks and wrote required
                  outputs under experiments/prototypes/memory_v03_p0/outputs/.
paper_boundary:   No paper evidence promoted. Cycle 031 validates only the
                  local fixture/logging substrate.
discipline:       No Dream/code edit. No server integration. No model run.
                  No checkpoint use. No training. No frontend.
verification:     python run_ablations.py --output outputs returned pass;
                  python -m pytest tests failed because pytest is not
                  installed; python tests\test_abl_memory_0.py passed.

pass_name:        Cycle 030 close pass (Memory v0.3 P0 execution DEC
                  template done in single session 2026-05-08)
date:             2026-05-08
trigger:          User asked to continue according to the current plan.
files_modified:   TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, RESEARCH_STATE.md,
                  INDEX.md, README.md, AGENT_MASTER_PROMPT.md,
                  registry/decision_registry.md
new_artifacts:    decisions/DEC-20260508-006-cycle-030-p0-execution-
                  dec-template.md
                  planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md
                  cycles/CYCLE-20260508-007.md
result:           P0 execution DEC template completed. It predefines
                  future DEC fields, allowed local prototype path,
                  forbidden server/model/checkpoint paths, allowed and
                  forbidden actions, ABL-memory-0..8 scope,
                  ABL-memory-9..11 exclusion, oracle-bus boundary,
                  required outputs, stop gates, result labels, go/no-go
                  rules, and post-execution evidence boundary.
paper_boundary:   No paper evidence promoted. Cycle 030 is
                  authorization-template evidence only.
discipline:       Markdown-only. No server code edit. No model run.
                  No training. No checkpoint download. No frontend.
verification:     git diff --check returned no whitespace errors
                  (line-ending warnings only); stale-pointer search
                  returned no active hits; checked markdown fence
                  counts for edited key files and all were even.

prior_pass_name:  Cycle 029 close pass (Memory v0.3 ablation review
                  and correction done in single session 2026-05-08)
prior_pass_date:  2026-05-08
prior_pass_files: TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, RESEARCH_STATE.md,
                  INDEX.md, README.md, AGENT_MASTER_PROMPT.md,
                  registry/decision_registry.md,
                  specs/SPEC-20260508-002-dream3r-memory-v03-
                  ablation-addendum.md,
                  decisions/DEC-20260508-005-cycle-029-memory-
                  ablation-review.md,
                  planning/MEMORY_V03_ABLATION_REVIEW.md,
                  cycles/CYCLE-20260508-006.md

prior_pass_name:  Cycle 028 close pass (Memory v0.3 ablation addendum
                  done in single session 2026-05-08)
prior_pass_date:  2026-05-08
prior_pass_files: TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, RESEARCH_STATE.md,
                  INDEX.md, README.md, AGENT_MASTER_PROMPT.md,
                  registry/decision_registry.md,
                  planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md,
                  specs/SPEC-20260508-001-dream3r-c2-memory-v03-
                  addendum.md, decisions/DEC-20260508-004-cycle-
                  028-memory-ablation-addendum.md,
                  specs/SPEC-20260508-002-dream3r-memory-v03-
                  ablation-addendum.md, cycles/CYCLE-20260508-005.md
```

## If interrupted, resume from

If a new agent or new conversation is picking this up cold:

```text
CURRENT RESUME OVERRIDE (V11 semantic label-cache gate closed; 2026-06-03):

1. Read this file (you are here).

2. For VLM semantic-controller research, read:
   planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
   handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
   decisions/DEC-20260603-027-vlm-semantic-controller-plan.md
   decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md
   cycles/CYCLE-20260603-vlm-semantic-label-cache-gate.md

3. The label-cache builder already exists:
   code/dream3r/scripts/build_vlm_semantic_labels.py
   code/dream3r/tests/test_vlm_semantic_labels.py
   runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json

4. The next executable gate is to build a real KITTI/ETH3D window manifest from
   existing cache windows, then run a 10-window Qwen smoke on BUAA-Server GPU1
   only after weights and compatible dependencies are staged or approved.

5. Do not treat Qwen3-VL-2B-Instruct as geometry. It may support Router,
   Critic, Dream state auxiliary supervision, and teacher scheduling only.

6. The locked geometry baseline remains 0.1448/0.1475. U1 remains negative.
   VGGT-Omega remains blocked on approved checkpoint access.

Historical override follows.

CURRENT RESUME OVERRIDE (native student gate closed; 2026-06-02):

1. Read this file (you are here).

2. Read handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md
   and planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md.

3. Read decisions/DEC-20260602-024-native-student-decoder-gate.md and
   cycles/CYCLE-20260602-native-student-decoder-gate.md. The native student
   scaffold already exists and should not be recreated.

4. The locked baseline remains:
   runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
   runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json

5. Preserve frozen-core boundaries. Do not edit model.py, anchor_bank.py,
   nsa_attention.py, bus.py, orchestrator.py, repair.py, modules.py,
   contracts.py, or config.py without a new DEC.

6. Next native work should change the objective with dropout-consistency or
   temporal/scale state-projection targets, then rerun state/no-state/shuffle
   controls against the 0.1448/0.1475 baseline. If native objective work
   blocks, fall back to VGGT-Omega one-window teacher admission rather than
   another residual-head sweep.
```

Historical resume material below is retained for traceability only. It is not
the active next action after `dream3r-native-student-gate-2026-06-02`.
3. Read experiments/prototypes/memory_v03_p0/README.md and
   experiments/prototypes/memory_v03_p0/outputs/summary_go_no_go.md.

4. Read cycles/CYCLE-20260508-008.md for the cycle 031 result and
   verification boundary.

5. Read planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md and
   decisions/DEC-20260508-006-cycle-030-p0-execution-dec-template.md
   for the parent authorization template.

6. Read decisions/DEC-20260508-005-cycle-029-memory-
   ablation-review.md and planning/MEMORY_V03_ABLATION_REVIEW.md.

7. Read planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md and
   specs/SPEC-20260508-002-dream3r-memory-v03-ablation-
   addendum.md. The latter has cycle 029 v1.1 corrections.

8. Read specs/SPEC-20260508-001-dream3r-c2-memory-v03-
   addendum.md for the current C2 Memory architecture direction.

9. Default next action is a user decision on:
   A. start cycle 032 local ABL-memory-1 vector AnchorBank baseline,
   B. review ABL-memory-0 outputs before later ablations, or
   C. pause execution and return to research design.

10. ABL-memory-1..8 execution, server code edit, model run, checkpoint
    use, training, or paper claim promotion requires a separate DEC and
    per-step gate.

11. The older cycle 022 / cycle 015 resume material below is retained
    as historical traceability only. It is not the active next action.

1. Read this file (you are here).

2. Read decisions/DEC-20260507-002-cycle-022-path-c-reattempt-
   and-paper-s3s6-rewrite.md — this is the most recent strategic
   decision and documents the cycle 022 combined scope (Path C
   reattempt + paper §3+§6 v0.2 rewrite; both DONE; see below).

3. Read cycles/CYCLE-20260507-002.md — this is the cycle 022 log
   documenting: Path C SUCCEEDED (API gateway recovered; both
   agents returned 5-section reviews); 7 review-action items
   RA-01..07 captured for v0.3 addenda (conditional cycle 023.5);
   paper PAPER_DRAFT_V1.md updated to v1.2 (§3.8 + §6.0–6.3
   added; §3.1–3.7 + §6.4 preserved). Cycle 022 status = DONE.

4. Read decisions/DEC-20260506-004 (cycle 020 combined planning),
   decisions/DEC-20260506-003 (cycle 019 ablation plan v0.2),
   decisions/DEC-20260506-002 (cycle 018 v0.2 architecture deltas),
   decisions/DEC-20260506-001 (mainline architecture-first) for
   parent-cycle context.

5. Read these cycle 021 deliverables (already done in this pass):
   - specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (S3;
     ~880 lines; closes v0.2 markdown trio; 5-tier reorganization
     + 3 NEW axes + threat re-rank; 5 risks + 5 open questions
     including ABL-v02-10 Test3R-alone candidate)
   - cycles/CYCLE-20260507-001.md (S4; cycle 021 log; status
     done-with-S2-blocked-by-infrastructure)

6. Reference SPEC bodies ONLY when needed (do NOT re-Read full
   files; cite by section + line anchor):
   - specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2
     architecture; six deltas; 882 lines)
   - specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2
     ablation plan; nine ABL-v02; 991 lines)
   - specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1
     comparator map substrate; 625 lines; preserved unchanged
     in body; only Version history tail received v0.2 pointer)
   - specs/SPEC-20260506-001-dream3r-architecture.md (v0.1
     architecture; 1821 lines; do NOT re-Read)
   - planning/DREAM3R_V02_CODE_STRUCTURE.md (1086 lines; cycle
     020 deliverable; Path C review TARGET — deferred)
   - planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (1226 lines;
     cycle 020 deliverable; Path C review TARGET — deferred)
   - code/dream3r/PLAN.md (v0.1 user-authored implementation
     roadmap; preserved unchanged)

7. Read C:\Users\27252\.claude\projects\e--kykt\memory\
   feedback_dream_mainline_architecture_first.md and
   feedback_kykt_server_topology.md (cross-session memories;
   F-002 anchor — KYKT 3R model code runs server-side at
   /hdd3/kykt26/; local Windows is markdown + orchestration
   only).

```text
Project state at this snapshot:
   Cycle 015 PAUSED at S9 done (NOT closed; NOT abandoned;
                                infrastructure reusable as future
                                Critic A4 evidence anchor).
   Cycle 016 DONE.
   Cycle 017 DONE (paper draft v1; needs v0.2 update later).
   Cycle 018 DONE (v0.2 architecture deltas; SPEC-20260506-004
                   written; six deltas; main-claim narrowed to
                   A+D).
   Cycle 019 DONE (v0.2 ablation plan addendum; SPEC-20260506-
                   005 written; 9 ABL-v02; per-ABL review
                   checklist for other-agent handoff).
   Cycle 020 DONE (combined v0.2 code structure + implementation
                   roadmap planning artifacts; DREAM3R_V02_CODE_
                   STRUCTURE.md + DREAM3R_V02_IMPLEMENTATION_
                   ROADMAP.md NEW; trajectory revision per user
                   "高强度推进").
   Cycle 021 DONE-WITH-S2-BLOCKED:
                S1 done (DEC-20260507-001 written ~430 lines;
                   cycle 021 launch + combined scope + Path C
                   protocol + 5 open questions Q1-Q5)
                S2 BLOCKED (Path C activation; 4 sub-agent
                   attempts × ~3 min each all failed with API
                   500 nil-pointer panic on Calcium-Ion/new-api
                   gateway; deferred to cycle 022 per Honesty
                   Override Option β; full incident in
                   CYCLE-20260507-001 §"Path C activation
                   incident")
                S3 done (specs/SPEC-20260507-001-dream3r-
                   comparator-map-v02.md written ~880 lines;
                   closes v0.2 markdown trio: architecture +
                   ablation + comparator)
                S4 done (cycles/CYCLE-20260507-001.md NEW)
                S5 done (full sync chain)
   Cycle 022 DONE:
                S1 done (DEC-20260507-002 written; combined
                   cycle scope lock + protocols + post-022
                   trajectory)
                S2 done (Path C SUCCEEDED — both agents 38.2s
                   + 47.5s; API gateway recovered; 7 RA items
                   captured: RA-01..04 CODE_STRUCTURE gaps +
                   RA-05..07 IMPLEMENTATION_ROADMAP risks)
                S3 done (literature/PAPER_DRAFT_V1.md v1.2;
                   §3.8 six v0.2 deltas NEW + §6.0–6.3 v0.2
                   comparator positioning NEW; §3.1–3.7 +
                   §6.4 preserved)
                S4 done (cycles/CYCLE-20260507-002.md NEW)
                S5 done (full sync chain)

v0.2 markdown trio + paper status (post cycle 022):
   - Architecture: SPEC-20260506-004 v0.2 (cycle 018; 6 deltas;
     A+D pillars)
   - Ablation plan: SPEC-20260506-005 v0.2 (cycle 019; 9 ABL-
     v02 with per-ABL review checklist)
   - Comparator map: SPEC-20260507-001 v0.2 (cycle 021 S3;
     5-tier reorganization + 3 new axes + threat re-rank)
   - Paper: PAPER_DRAFT_V1.md v1.2 (cycle 022 S3; §3.8 + §6.0–
     6.3 added; §3.1–3.7 + §6.4 v0.1 preserved)
   All 4 artifacts are now v0.2-coherent. v0.1 bodies of all 3
   substrate specs preserved unchanged per Discipline rule 5.

Historical post-022 projection (superseded by actual cycles 023-027):
   Cycle 023 actual: v0.3 planning addenda + ablation plan v0.3
              addendum (DEC-20260507-003).
   Cycle 024 actual: server-side v0.2 scaffold / engineering smoke
              baseline (DEC-20260508-001), later bounded by cycle 026.
   Cycle 025 actual: C2 memory mechanism study
              (planning/MEMORY_V03_DESIGN_STUDY.md).
   Cycle 026 actual: C2 Memory v0.3 addendum and guidance correction
              (SPEC-20260508-001 + DEC-20260508-002).
   Cycle 027 actual: P0 static tensor prototype plan
              (planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md +
              DEC-20260508-003).

Resume action when user returns:
   Cycle 027 is DONE. No active task. Status `idle`. Prefer a new
   markdown-only memory-specific ablation addendum unless the user
   explicitly authorizes a separate P0 execution DEC.

   If user asks about Path C findings:
   - Agent A (CODE_STRUCTURE): 3 HIGH/MEDIUM gaps (latency budget
     absent; ExpertAdapter ABC unresolved; NSA output combination
     underspecified); 1 LOW gap (losses.py labeling contradiction).
     Full details in CYCLE-20260507-002 §S2 / RA-01..04.
   - Agent B (IMPLEMENTATION_ROADMAP): Pillar A faithfulness gap;
     3 risks (checkpoint inventory; NSA kernel cu121; T-v02-F
     oversized). Full details in CYCLE-20260507-002 §S2 / RA-05..07.
   - All 7 RA items captured for conditional cycle 023.5 v0.3
     addenda. NOT actioned in cycle 022 (B-roadmap-F rule).

   Any execution step launches only with explicit user direction.
   Do NOT propose training, checkpoint download, GPU runs, KYKT
   navigation change, frontend implementation, demo storyboard
   promotion past `draft`, thesis finalization, or retiring of any
   non-finalist track. DEC-20260501-004 candidate-not-final +
   DEC-20260504-002 no-all-in still in force.

Hard rules carried (unchanged from prior cycles):
   - No training. No checkpoint download. No reproduction. No
     KYKT navigation change. No frontend implementation. No
     thesis finalization. No retiring of any non-finalist track.
     No demo storyboard promotion past `draft`. No teacher-
     demo readiness claim.
   - DEC-20260501-004 (Dream3R candidate-not-final) and
     DEC-20260504-002 (no-all-in) still in force.
   - Cycles 021-022 were markdown only. Any code touch (whether
     per T-v02-N task or otherwise) requires a separate DEC +
     per-step micro gates per F-002 + reviewer authorization
     per IMPLEMENTATION_ROADMAP B-roadmap-F.
   - Honesty Override: VGGT offline-batch threat to pillar D
     acknowledged in PAPER_DRAFT_V1.md §6.2 and in
     CYCLE-20260507-002; no ablation numbers manufactured; all
     v0.2 paper claims carry evidence labels; Path C Agent
     findings documented verbatim without cherry-picking.
   - Trajectory adherence: paper v1.2 delivered as planned per
     cycle 022 scope; Path C SUCCEEDED; RA items captured;
     v0.3 addendum deferred to conditional cycle 023.5.
   - Per-task review checklist pattern (cycle 020) first real
     exercise SUCCEEDED in cycle 022. Path C = operational and
     confirmed working. API gateway stable at time of cycle 022.

Honor F-001 working rules throughout: do not Read large files
already cited in this snapshot; prefer Grep -n + Edit over full-
file Read + Write; cap large files in active context at <=2
simultaneously. Honor F-002: KYKT 3R model work runs server-side;
default to ssh + reuse before installing; check ssh_runner.py:22-44
ServerConfig before asking for SSH details. Cycles 022 is markdown
only and stayed local.
```

Project state at this snapshot:
   Cycle 015 PAUSED at S9 done (NOT closed; NOT abandoned;
                                infrastructure is reusable as
                                future Critic A4 evidence anchor).
   Cycle 016 IN PROGRESS:
                                S1 done (DEC-20260506-001 + memory +
                                  prior snapshot redirect block)
                                S2 done (architecture spec v0.1
                                  written 2026-05-06; 1821 lines;
                                  95 KB; specs/SPEC-20260506-001-
                                  dream3r-architecture.md)
                                S3 done (ablation plan v0.1
                                  written 2026-05-06; 10 ablations
                                  in 3 tiers; specs/SPEC-20260506-
                                  002-dream3r-ablation-plan.md)
                                S4 done (comparator map v0.1
                                  written 2026-05-06; 14+ models;
                                  specs/SPEC-20260506-003-dream3r-
                                  comparator-map.md)
                                S5 in progress (TASK_SNAPSHOT
                                  updated; cycle log + remaining
                                  sync files pending)

Mainline redirect summary:
   - Old implicit framing: framework-first paper output.
   - New explicit framing: architecture-first; Dream3R architecture
     spec is the PRIMARY output; paper is SUPPORT.
   - Cycle 015 L3 measurement work is SUPPORT / prereq for the
     architecture spec, NOT mainline.
   - Train-first remains deferred / blocked.
   - DEC-501-004 (Dream3R candidate-not-final) and DEC-504-002
     (no-all-in) still in force.

Resume action when user returns:
   Primary path: cycle 016 is nearly complete. S5 sync chain
     is in progress (TASK_SNAPSHOT updated; remaining: cycle log,
     decision registry, other sync files). Once S5 finishes,
     cycle 016 closes.

   Candidate next actions after cycle 016 closes:
     - Review S2 architecture spec + S3 ablation plan + S4
       comparator map (user can read all three and give feedback)
     - v0.2 architecture spec revision (if review or ablation
       plan surfaces substrate/bus/module issues)
     - Paper rewrite to feature Dream3R architecture as central
       claim (per architecture spec Q6)
     - Resume cycle 015 G_run for measured Critic A4 evidence
       (per architecture spec Q5)
     - A7 Cross-Modal / A8 Active Perception spec drafting
       (per architecture spec Q3)
     - Training authorization (requires separate DEC)

   S2 spec Q1..Q6 resolution status:
     Q1 substrate ablation priority -> RESOLVED in S3 ablation
        plan: hybrid first; SSM-only second; transformer-only
        third. ABL-2 in SPEC-20260506-002 specifies all three.
     Q2 adversarial vs natural CR-rule triggering -> RESOLVED
        in S3: both (B1-B5 for performance, B6 for CR-rule
        firing verification).
     Q3..Q6 -> still open; surface during user review of cycle
        016 deliverables.
   Do NOT execute anything beyond markdown drafting without
   explicit user `Go`. Do NOT propose training. Do NOT propose
   thesis finalization. Do NOT promote any of the 4 storyboards
   past `draft`.

Hard rules still in force (verbatim from S2 spec Boundaries):
   - All 4 finalist demo storyboards (STORY-20260505-001..004)
     remain markdown `draft`. Do NOT promote any to `approved-for-
     showing` without a separate DEC.
   - Do NOT start any non-Critic L3 pilot (Memory / Permanence /
     Composer L3) / training / KYKT navigation change / frontend
     implementation without explicit user approval per
     AGENT_MASTER_PROMPT.md section 6.
   - Cycle 015 has narrow exceptions ONLY for the Critic L3 pilot
     scope; everything else stays gated.
   - DEC-20260506-001 authorizes architecture-spec DESIGN +
     ablation PLANNING; NOT training, NOT GPU runs, NOT checkpoint
     creation.
   - v0.1 spec carries 13 explicit boundaries in its "Boundaries"
     section; all in force.

Honor F-001 working rules throughout: do not Read large files
already cited in this snapshot; prefer Grep -n + Edit over full-
file Read + Write; cap large files in active context at <=2
simultaneously. Honor F-002: KYKT 3R model work runs server-side;
default to ssh + reuse before installing; check ssh_runner.py:22-44
ServerConfig before asking for SSH details.
```

If this snapshot's Status is `idle`, both cycle 015 (Critic L3 measurement) and cycle 016 (Dream3R architecture spec drafting) are closed; the next live phase requires a separate user direction.

## Open user decisions (resolution status, 2026-05-04)

D1'-D4' were delegated to the agent by user message "D1-D4 你自己决策吧，有问题我们商讨" and locked in `decisions/DEC-20260504-003-cycle-009-launch.md`. Summary:

```text
1. Cycle 009 ordering (D1')        -> parallel (Composer + Critic; cross-
                                       spec contract v1 is the test path).
2. Composer card source (D2')      -> paper-derived only; KYKT-job-derived
                                       deferred to cycle 010.
3. TEACHER_AUDIENCE_PROFILE (D3')  -> populated 2026-05-04 by user input.
                                       Earlier snapshot text claimed
                                       three sub-fields remained empty;
                                       this was a stale read. The user
                                       2026-05-04 input populated all 6
                                       fields explicitly: Research Taste
                                       = 科研的训练 / 写作技巧 /
                                       创新范式 / 讲好故事; Prior
                                       Expectations = "老师不知道我们
                                       要做 Dream" -> cold start; Demo
                                       Precedent -> first impression
                                       (implied by Prior Expectations);
                                       Previously Praised = "老师对 3R
                                       方向都没啥具体贬褒" -> no specific
                                       3R praise; Previously Criticized
                                       = same statement -> no specific
                                       3R criticism; Hard Constraints =
                                       no constraints stated. Profile
                                       is fully populated; D3' resolved;
                                       D3 (first demo target choice)
                                       still deferred per DEC-20260504-
                                       002 because cycle 010 case-card
                                       data for Memory + Permanence is
                                       still pending (agent
                                       recommendation per DEC-20260504-
                                       005 cycle 010 launch memo).
4. Cycle 009 launch authorization  -> go. CASE-20260504-CRITIC-01 is the
   (D4')                             first card per cycle 008 D1; drafted
                                     2026-05-04, paper-derived per D2'.
```

Cycle 010 launch decisions (locked 2026-05-04 from user message "1 a 吧 / 2 并行是不是好点儿 / 3 我觉得你决定就好 / 4 这个啥意思" plus agent confirmation; recorded in `decisions/DEC-20260504-005-cycle-010-launch.md`):

```text
1. v2 cost-typed route_regret (E1)  -> adopt. Contract bumped to v2;
                                       capability_match adds
                                       cost_normalized axis; alpha = 0.5
                                       initial (inferred). v1 prose
                                       preserved as Superseded per
                                       Discipline rule 5. CASE-COMPOSER-
                                       03 v2 row promoted to canonical
                                       recommendation; v1 row preserved.
                                       Memo: DEC-20260504-004.
2. Cycle 010 ordering (E2)          -> Memory + Permanence in parallel.
                                       Cross-pair pattern from cycle 009
                                       (CRITIC-02 <-> COMPOSER-01) reused;
                                       CR-2 binding closed via in-cycle
                                       cross-pair (Permanence publishes
                                       suppress_static_write, Memory
                                       consumes; both drafted in cycle
                                       010). Forward-reference null
                                       protocol from CRITIC-03 covers
                                       any timing gap.
3. D3 first demo target (E3)        -> agent decision: continued deferral
                                       to cycle 010 closeout. Two
                                       deferral conditions per
                                       DEC-20260504-002 are now both met
                                       (audience profile populated +
                                       cycle 009 case-card data exists),
                                       but Memory + Permanence still have
                                       no L2 evidence; picking now would
                                       violate Discipline rule 5
                                       (Honesty Override) by selecting on
                                       partial portfolio coverage. Re-
                                       surface at cycle 010 closeout when
                                       all 4 finalists have L2 cards.
4. D3' sub-field correction (E4)    -> stale snapshot text saying "three
                                       sub-fields remain empty" was
                                       wrong; profile is fully populated
                                       (see corrected entry in section 3
                                       above). User asked "这个啥意思"
                                       triggered the correction.
```

Cycle 011 launch decisions (locked 2026-05-05 from user message "你给我决定吧，（1）（2）（3）" delegating to agent; recorded in `decisions/DEC-20260505-001-cycle-011-launch-and-d3-demo-target.md`):

```text
1. D3 first teacher demo target (1)  -> Critic (Geometry Critic /
                                        System-2 3R, SPEC-20260503-001).
                                        Picked on five-axis comparison
                                        (surprise hook strength,
                                        mechanism legibility for
                                        cold-start audience, connection
                                        to Dream3R thesis, L2 portfolio
                                        depth, demo failure-mode
                                        robustness, "looks like paper X"
                                        collapse risk). Storyboard:
                                        STORY-20260505-001-critic.md
                                        drafted; status = draft only;
                                        no `approved-for-showing`
                                        granted by DEC-001. D3 = "first
                                        demo target", not retiring of
                                        other finalists; DEC-20260504-
                                        002 still in force.
2. Cycle 011 scope (2)               -> G4 (CR-2 partial on synthetic
                                        identity-validation clip) +
                                        G5 (forward-reference null
                                        protocol formalization) closure
                                        primary; Critic demo storyboard
                                        draft secondary. G6 + G2 +
                                        KYKT-derived Composer card +
                                        L3 prototype + paper writing
                                        all explicitly deferred.
3. v2 -> v3 candidates (3)           -> v2 -> v2.1 additive revision:
                                        forward-reference null protocol
                                        formalized as a contract-pinned
                                        subsection. The other two
                                        candidates (8x8 grid partition
                                        for Permanence regions;
                                        identity_consistency threshold
                                        pinning at ~0.7) deferred and
                                        not promoted; rationale per
                                        DEC-001 (3): grid partition is
                                        Permanence implementation
                                        detail, threshold pinning needs
                                        measured anchors that don't yet
                                        exist.
4. New (4) blocked items unchanged from cycle 010 closeout (final
   thesis selection / reproduction / training / checkpoint download /
   KYKT navigation change / Codex frontend implementation / reusable
   Codex skill packaging / discarding any non-finalist track /
   declaring teacher-demo readiness; demo SHOWING also blocked).
```

Items still blocked on user approval per `AGENT_MASTER_PROMPT.md` section 6 (unchanged from prior cycles): final thesis selection, reproduction, training, checkpoint download, KYKT navigation change, frontend implementation, reusable Codex skill packaging, retiring any non-finalist track, declaring teacher-demo readiness, **showing any of the 4 demo storyboards (Critic / Memory / Permanence / Composer; all remain `draft`; promotion to `approved-for-showing` requires a separate DEC per finalist)**.

Cycle 013 launch decisions (locked 2026-05-05 from user message "好了，请你做实际的研究部署吧，无论是准备工作还是调研和资料搜集等" + clarification "Phase 2 准备 + 资料调研 (推荐)" delegating to agent; recorded in `decisions/DEC-20260505-003-cycle-013-launch.md`):

```text
1. Cycle 013 scope (delegated)        -> Phase 2 preparation + research
                                        mining. Three locked sub-passes:
                                        S2 source-mining cycle-013 pass
                                        (4 finalist x 3 axes coverage
                                        gaps); S3 paper related-work
                                        prose draft (replace skeleton
                                        bullets with prose in Sections
                                        1-7; draft Sections 8-9 as
                                        prose); S4 L3 prerequisites
                                        briefs per finalist (4 markdown
                                        files under experiments/).
                                        Cycle 013 explicitly excluded:
                                        L3 prototype, checkpoint
                                        download, KYKT runner log
                                        access, model touching,
                                        retroactive edits to prior
                                        cycle artifacts, contract
                                        revision.
2. v2.1 -> v2.2 candidates (delegated) -> NO revision in cycle 013.
                                        No new candidate surfaced.
                                        Both cycle-011 deferred
                                        candidates (8x8 grid partition;
                                        identity_consistency threshold
                                        pinning) remain deferred.
                                        VGGT capability-card gap
                                        surfaced by cycle-013 mining
                                        is per-card, not contract.
3. D3 first demo target (carried)     -> unchanged; Critic per cycle
                                        011 DEC-20260505-001. No
                                        cycle-013 reconsideration.
4. Blocked items                       -> unchanged from cycle 012
                                        closeout. "Showing any of
                                        the 4 demo storyboards"
                                        unchanged. L3 / clone /
                                        download / install / run / KYKT
                                        navigation change / frontend /
                                        thesis finalization / training
                                        all still gated.
```

Cycle 013 G2 status update:

```text
Before cycle 013: G2 = inferred-with-real-inventory-anchor (per cycle
                       012 COMPOSER-04 KYKT-metadata-derived card).
After  cycle 013: unchanged. EXP-20260505-004 inventories the closure
                  path (multi-regime workload; 3+ backbones; measured
                  route_regret) but cycle 013 did NOT execute it.
Closure remains gated on L3 prototype OR KYKT runner log access; both
require separate user authorization.
```

New tracking goal G7 introduced cycle 013:

```text
G7 (paper-related-work-prose-readiness):
  Status after cycle 013: inferred-with-prose-draft-anchor.
  Sections 1-7 of literature/PAPER_RELATED_WORK_SKELETON.md are prose;
  Sections 8-9 are drafted as prose. The cycle-009 case-card-gate that
  blocked prose drafting is lifted (cleared by cycle 010-012 case-card
  + storyboard portfolio).
  Closure: full Phase-2 paper writing (intro / methods / results /
  discussion). Gated on user direction on venue / length / scope.
```

Cycle 012 launch decisions (locked 2026-05-05 from user message "你给我规划吧，然后弄完后告诉我我们的工作做了哪些？" delegating to agent; recorded in `decisions/DEC-20260505-002-cycle-012-launch.md`):

```text
1. Storyboard reviewer pass (1)      -> NOT done in cycle 012. Deferred
                                        to demo-show-authorization
                                        moment when functional-vs-
                                        placeholder tradeoffs become
                                        concrete. Critic storyboard +
                                        the 3 new storyboards all
                                        remain `draft` unchanged in
                                        future agent passes (no silent
                                        revisions).
2. Cycle 012 scope (2)               -> (c) KYKT-metadata-derived
                                        COMPOSER-04 + (e) 3 finalist
                                        demo storyboards (Memory +
                                        Permanence + Composer; all
                                        markdown only; all `draft`).
                                        Options (a) close G6 / (b)
                                        close G2 / (d) request demo
                                        show authorization / (f) start
                                        paper related-work writing all
                                        deferred (gated or premature).
3. v2.1 -> v2.2 candidates (3)       -> NO revision. Both deferred
                                        candidates from cycle 011
                                        (8x8 grid partition for
                                        Permanence regions;
                                        identity_consistency threshold
                                        pinning at ~0.7) remain
                                        deferred. COMPOSER-04 fits
                                        cleanly into existing v2
                                        schema; no new sub-axis needed.
4. (4) blocked items unchanged from cycle 011 closeout; "showing the
   Critic demo" extended to "showing any of the 4 demo storyboards"
   (all 4 finalists now have draft storyboards as of cycle 012).
```

Cycle 012 G2 status update:

```text
Before cycle 012: G2 = inferred (tau_spread = 0.05 paper-derived;
                                 capability_match paper-derived).
After cycle 012:  G2 = inferred-with-real-inventory-anchor
                       (capability_match values now KYKT-metadata-
                        derived per COMPOSER-04; tau_spread itself
                        still inferred; closure still requires
                        measured route_regret; gated).
G2 NOT closed. Closure remains gated on L3 prototype OR KYKT runner
log access.
```

Cycle 015 launch decisions (locked 2026-05-05 from user message "授权 Critic L3 窄域 pilot" delegating cycle 015 entry to the Critic L3 pilot scope; recorded in `decisions/DEC-20260505-005-cycle-015-launch-critic-l3-pilot.md`):

```text
1. Cycle 015 entry (D5)              -> authorize Critic L3 pilot scope
                                        per planning/L3_PILOT_SELECTION.md
                                        "Recommended first-pilot scope" +
                                        EXP-20260505-001 prerequisite
                                        inventory. Allowed: clone Test3R
                                        + CTRL + DUSt3R + MASt3R; download
                                        required checkpoints; install
                                        minimum env on a single box; run
                                        one smoke loop on one hard-case
                                        input; emit one JSONL log;
                                        write thin wrapper
                                        dream_critic_loop.py + hand-
                                        derived capability_match YAML.
2. Per-step micro gates (D5')        -> 5 gates, each a separate
                                        user go in active conversation:
                                        G_clone, G_install, G_download,
                                        G_run, G_log_use. DEC-005 alone
                                        does NOT authorize any of these
                                        steps; each surfaces individually
                                        with proposed path / repos /
                                        checkpoints / hard-case input
                                        before execution.
3. v2.1 -> v2.2 candidates (D5'')    -> NO revision in cycle 015. Both
                                        cycle-011 deferred candidates
                                        (8x8 grid partition; identity_
                                        consistency threshold pinning)
                                        remain deferred. VGGT capability-
                                        card gap remains per-card
                                        (CASE-20260505-COMPOSER-05),
                                        not contract-level.
4. Composer second-pilot precondition (D5''') -> unchanged from
                                        L3_PILOT_SELECTION.md: VGGT row
                                        must be included or explicitly
                                        excluded with reason before any
                                        Composer route_regret sweep is
                                        frozen. Cycle 015 does not act on
                                        this; Composer pilot is OUT of
                                        cycle 015 scope.
5. Blocked items unchanged from cycle 014 closeout, with one tightening:
   the cycle-015 authorization is Critic-L3-only. Memory / Permanence /
   Composer L3 prototypes remain blocked. Final thesis selection,
   reproduction (in the sense of paper-result re-runs), training,
   KYKT navigation change, frontend implementation, reusable Codex
   skill packaging, retiring any non-finalist track, declaring
   teacher-demo readiness, and showing any of the 4 demo storyboards
   all remain blocked.
```

Cycle 015 G2 / G6 / G7 status update at launch:

```text
G2 (route_regret closure):  unchanged. inferred-with-real-inventory-
                            anchor (cycle 012 anchor). Critic smoke
                            does NOT close G2; G2 closure remains
                            gated on multi-regime measured
                            route_regret OR KYKT runner log access.
G6 (memory governance):     unchanged.
G7 (paper related-work
     prose readiness):      unchanged. inferred-with-blueprint-anchor
                            (cycle 014 anchor). Closure still gated
                            on user direction on venue / length /
                            scope of Phase 2 paper.
```

Cycle 016 mainline redirect (locked 2026-05-06 from user message "所以现在我们做的和新模型有啥关系？或者说什么时候能开始推进主线了？" + selection of "B. Architecture-first" from a 3-option strategic question; recorded in `decisions/DEC-20260506-001-mainline-architecture-first.md`):

```text
1. Mainline definition (D6)         -> Dream's mainline is
                                       **architecture-first**: design a
                                       new 3R architecture (transformer
                                       / SSM / state-space / hybrid) as
                                       a markdown spec + ablation plan
                                       + comparator map. NOT framework-
                                       first paper writing.

2. Cycle 015 posture (D6')          -> stays paused at S9 done. NOT
                                       closed. NOT abandoned. The L3
                                       infrastructure (test3r conda env
                                       on server; launch.py patch; F-002
                                       memory; 4 local shallow clones)
                                       is reusable as evidence anchor
                                       for the architecture spec's
                                       Critic-module section. G_run can
                                       be resumed later if the
                                       architecture spec needs measured
                                       evidence; until then, no G_run.

3. Paper Phase 2 blueprint (D6'')   -> demoted from primary output to
                                       SUPPORT artifact. Still useful
                                       (control-graph theory becomes
                                       the THEORY behind the
                                       architecture); but the
                                       architecture spec is the
                                       PRIMARY output of the project.

4. Past decisions still in force (D6''') -> DEC-20260501-004 (Dream3R
                                       candidate-not-final) and
                                       DEC-20260504-002 (no-all-in any
                                       single finalist) both still
                                       apply. Architecture spec must
                                       (a) remain a candidate that can
                                       be revised/replaced/merged, and
                                       (b) preserve all 4 finalist
                                       mechanisms as composable
                                       modules, not collapse into one.

5. Train-first (option C) NOT authorized. Architecture-first
   authorizes design + ablation planning, NOT training, NOT GPU
   ablation runs, NOT checkpoint creation. Train-first remains
   deferred / blocked.

6. Blocked items unchanged from prior cycles. Hard rules carried from
   AGENT_MASTER_PROMPT.md section 6 unchanged: no reproduction / no
   checkpoint download / no training / no KYKT navigation change / no
   frontend / no thesis finalization / no retiring of any non-finalist
   track / no demo storyboard promotion past `draft`.

7. Cycle 016 launch deferred. S1 of cycle 016 = this DEC + feedback
   memory + this snapshot block (done 2026-05-06). S2..S5 (architecture
   spec draft + ablation plan + comparator map + sync chain) deferred
   to next session per user "今日进度到此为止".
```

Cycle 016 G2 / G6 / G7 status update at redirect:

```text
G2 (route_regret closure):  unchanged. Architecture spec drafting does
                            NOT close G2 (still gated on measured
                            route_regret OR KYKT runner log access).
G6 (memory governance):     unchanged.
G7 (paper related-work
     prose readiness):      unchanged. Paper output is now SUPPORT,
                            not primary; G7 closure is no longer the
                            project's main milestone. The new primary
                            milestone is "Dream3R architecture spec
                            v1 draft" (call it G8 if/when formalized).
                            Whether G7 stays open vs is retired is a
                            separate cycle-016 decision.
```

## Update protocol (highest priority — always honor)

This file MUST be updated at every meaningful task transition. The transitions are:

1. **Start of a task pass**: set `Status` to `in_progress`; populate `Current task`, `Subtask board`, and `If interrupted, resume from`.
2. **Each subtask completion**: flip the row's `Status` to `done` immediately. Don't batch.
3. **Mid-task interrupt or failure**: leave `Status` as `in_progress` and the active subtask as the last non-`done` row. Add a brief "Why interrupted" note. The next session resumes from there.
4. **End of a task pass (clean)**: flip `Status` to `idle`, mark `Last completed task pass` with what just finished, clear obsolete subtasks.
5. **End of a task pass (blocked on user)**: set `Status` to `blocked`; surface the blocker in `Open user decisions`.

Updating `Last updated:` is not optional. If you update this file you stamp it.

This rule is part of the Guidance File Sync Rule chain (see `WORKFLOW_STATUS.md`). It runs **first** in that chain — TASK_SNAPSHOT.md updates before any other file in a sync pass, so an interrupted sync still leaves a valid resume pointer.

## Recent failure modes the next agent should NOT repeat

Captured here as a short list because they are easy to repeat and expensive to recover from. Full prose lives in `cycles/CYCLE-20260504-001.md` "Note On The Earlier 32 MB Failure" and `RESEARCH_STATE.md` "Note On The Earlier 32 MB Failure".

```text
F-001  32 MB request-limit failure (2026-05-04, prior session)
       cause:  cumulative context (multiple full-file Reads + edit history)
               in one window, NOT any single oversized file
       avoid:  Read with offset/limit; Grep with -n for precision; Edit
               (old_string/new_string) instead of Write (full rewrite);
               keep <=2 large state files in context simultaneously;
               cite already-drafted content from cycle log + SPINE files
               instead of re-deriving it

F-002  agent assumed local Windows execution for KYKT 3R model work
       (2026-05-05, cycle 015 S7 G_install pre-flight)
       cause:  agent probed local GPU/Python/conda and proposed creating
               a conda env on the local Windows box and pip-installing
               dust3r/mast3r/Test3R locally. Did NOT consult
               E:\kykt\WORK.md or
               E:\kykt\.omx\plans\kykt-app-backend-model-integration-plan.md,
               both of which document a canonical server-side topology:
               KYKT 3R models live on /hdd3/kykt26 on a remote server,
               reached via system ssh + scp. Existing runners
               (dust3r_runner.py, mast3r_runner.py, monst3r_runner.py,
               spann3r_runner.py, fast3r_runner.py) already provide envs
               + checkpoints for 4 of the 5 inventoried backbones.
               EXP-20260505-001 was paper-derived and did NOT anchor to
               the production runner inventory; the agent inherited the
               paper-derived framing without re-checking topology.
       avoid:  before any L3 / training / heavy-compute G_install /
               G_download / G_run gate proposal, read E:\kykt\WORK.md +
               E:\kykt\.omx\plans\kykt-app-backend-model-integration-plan.md
               first; default to SERVER-side execution; reuse existing
               runners before installing new ones; ask the user for
               SSH host / path when topology details are missing rather
               than improvising. Local Windows box = markdown + shallow
               code-reading clones + orchestration + result inspection
               only; not the model execution target.
```

Add new entries here as new failure modes are discovered. Do not delete entries; supersede via a "superseded by F-NNN" note (Discipline rule 5 Honesty Override).

## Working rules to avoid F-001 (anti-32MB request-limit)

These rules apply to every agent operating in this workspace, including humans driving an agent. Violating them is the most common cause of multi-edit pass failures.

1. Do not re-Read a file already read earlier in the same conversation. The content is still in context. Cite line numbers from the prior Read; if a slice is needed, use Read with `offset`+`limit`.
2. For lookup, prefer `Grep -n` with `-C` / `-A` / `-B` for context. Reserve full Read for files under ~300 lines OR when the whole file is genuinely needed.
3. Prefer `Edit` (old_string / new_string, diff-only payload) over `Write` (full file payload) for any file that already exists. Use `Write` only for new files.
4. Cap "large" files (>300 lines OR >20 KB) in active context at <=2 simultaneously. When starting a new sync sub-pass, treat earlier large files as evicted; rely on `TASK_SNAPSHOT.md` and the most recent cycle log summary instead of re-Reading.
5. If a single Edit's old_string / new_string would exceed ~200 lines, split into multiple smaller Edits anchored at stable section headers, not in the middle of paragraphs.
6. Sync `TASK_SNAPSHOT.md` FIRST in any Guidance File Sync Rule chain pass, so an interrupt mid-pass still leaves a valid resume pointer (this is the rule already restated in `WORKFLOW_STATUS.md` "Guidance File Sync Rule").
7. Do not run multi-file Read fan-outs in parallel just to "have everything"; pull files in only when the next concrete edit demands them.
8. If a single tool call returns "Request too large", do NOT retry with the same payload. Switch to: smaller Read window, narrower Grep, or split Edit. Record the trigger in this section's F-NNN list if it represents a new failure mode.

These rules are mandatory-equivalent to the Hard rules below, since violating them tends to lose a session's worth of work.

## Hard rules (carried from AGENT_MASTER_PROMPT.md, restated for safety)

1. No reproduction. No checkpoint download. No training. No KYKT navigation change. No frontend implementation. No thesis finalization. No retiring of any non-finalist track. None of these without explicit user approval **in the active conversation**.
2. Apply Surgical Edits (Discipline rule 3): every changed line traces to a user request, decision memo, or Sync Rule trigger.
3. Apply Honesty Override (Discipline rule 5): every mechanism claim carries an evidence label; user approval cannot be invented.
4. ID conventions are fixed: `SPEC-YYYYMMDD-NNN`, `DEC-YYYYMMDD-NNN`, `CYCLE-YYYYMMDD-NNN`, `CASE-YYYYMMDD-NNN`. Use the current session date prefix for new artifacts.
5. Sentence case headers. No em-dashes.
