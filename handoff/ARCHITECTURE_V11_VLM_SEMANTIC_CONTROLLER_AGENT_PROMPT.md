# Dream3R V11 VLM semantic-controller agent prompt

Use this prompt for a fresh agent when the goal is to explore whether
Qwen3-VL-2B-Instruct or another compact open VLM can produce better Dream3R
research ideas and an executable controller-improvement plan.

Post-implementation note, 2026-06-03: the first label-cache gate is implemented
and documented in `decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md`
and `cycles/CYCLE-20260603-vlm-semantic-label-cache-gate.md`. Local mock schema
tests pass and the mock smoke cache is at
`runs/vlm_semantic_controller/qwen3vl2b_smoke/`. DEC-20260603-030 later staged
Qwen weights/runtime; DEC-20260603-031 later ran the first real 50-window gate.

Post-integration note, 2026-06-03: the controller-integration gate is now
implemented and documented in
`decisions/DEC-20260603-029-qwen-semantic-controller-integration.md` and
`cycles/CYCLE-20260603-qwen-semantic-controller-integration.md`. Do not recreate
the manifest or dry-run scripts. Start from:

```text
code/dream3r/scripts/build_vlm_window_manifest.py
code/dream3r/scripts/eval_vlm_controller_dryrun.py
code/dream3r/tests/test_vlm_controller_integration.py
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json
```

The dry-run is mock-positive but intentionally non-promotable. Next work should
stage real Qwen labels first, then compare real/shuffle/disabled controls on
held-out windows before any Router/Critic training.

Post-weight note, 2026-06-03: Qwen3-VL-2B-Instruct is staged and runnable on
BUAA-Server. Read
`decisions/DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md` and
`cycles/CYCLE-20260603-qwen3vl2b-weight-staging-smoke.md`. Runtime paths:

```text
/hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
/hdd3/kykt26/envs/qwen3vl2b_smoke
```

GPU1 5-window KITTI smoke passed strict schema 5/5 at:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/qwen_labels_5win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/schema_report_5win_t320.json
```

Use `--max-new-tokens 320` or higher for real Qwen labels; 160 caused
truncated/non-JSON failures on 5-window smoke.

Post-50-window note, 2026-06-03: read
`decisions/DEC-20260603-031-qwen3vl2b-50win-controller-gate.md` and
`cycles/CYCLE-20260603-qwen3vl2b-50win-controller-gate.md`. The first
oracle-aligned 50-window real Qwen gate is schema-positive but
controller-negative:

```text
schema_pass_rate: 1.0 (50/50 valid)
oracle_mean: 0.14893413588404655
vlm_real: 0.2365107437968254
vlm_shuffle: 0.2365107437968254
vlm_disabled: 0.2365107437968254
promotable: false
```

Do not train/promote Router/Critic from this cache. The current prompt/features
collapse to non-discriminative labels for this dry-run: all route variants pick
Fast3R for 50/50 windows. Next Qwen work must redesign the semantic
prompt/features/policy and re-run real/shuffle/disabled controls.

Post-v2 repair note, 2026-06-03: read
`decisions/DEC-20260603-032-qwen-controller-v2-feature-policy-repair.md` and
`cycles/CYCLE-20260603-qwen-controller-v2-feature-policy-repair.md`. Cause-
derived risk floors and route-priority repair make Qwen weak-positive but still
not promotable:

```text
oracle_mean: 0.14893413588404655
vlm_real:    0.175017766058445
vlm_shuffle: 0.17588756889104842
vlm_disabled:0.2365107437968254
promotable:  false
```

Do not keep hand-tuning deterministic rules on the same 50 windows. The next
Qwen gate should be held-out calibrated or learned semantic control.

Post-held-out note, 2026-06-03: read
`decisions/DEC-20260603-033-qwen-heldout-calibrated-controller.md` and
`cycles/CYCLE-20260603-qwen-heldout-calibrated-controller.md`. The calibrated
leave-one-group-out gate is negative against shuffle:

```text
oracle_mean: 0.14893413588404655
vlm_real:    0.18129218325018884
vlm_shuffle: 0.17762137934565544
vlm_disabled:0.2365107437968254
promotable:  false
```

Do not promote the current Qwen 50-window cache into Router/Critic. Future Qwen
work needs broader window coverage and a pre-registered real > shuffle >
disabled promotion threshold.

```text
You are taking over Dream3R V11 on 2026-06-03.

Workspace: E:\Dream3R
Server repo: /hdd3/kykt26/code/dream3r
Server: ssh BUAA-Server
GPU for model code: CUDA_VISIBLE_DEVICES=1

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\planning\DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
3. E:\Dream3R\decisions\DEC-20260603-027-vlm-semantic-controller-plan.md
4. E:\Dream3R\cycles\CYCLE-20260603-vlm-semantic-controller-plan.md
5. E:\Dream3R\decisions\DEC-20260603-028-vlm-semantic-label-cache-gate.md
6. E:\Dream3R\cycles\CYCLE-20260603-vlm-semantic-label-cache-gate.md
7. E:\Dream3R\decisions\DEC-20260603-029-qwen-semantic-controller-integration.md
8. E:\Dream3R\cycles\CYCLE-20260603-qwen-semantic-controller-integration.md
9. E:\Dream3R\decisions\DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md
10. E:\Dream3R\cycles\CYCLE-20260603-qwen3vl2b-weight-staging-smoke.md
11. E:\Dream3R\decisions\DEC-20260603-031-qwen3vl2b-50win-controller-gate.md
12. E:\Dream3R\cycles\CYCLE-20260603-qwen3vl2b-50win-controller-gate.md
13. E:\Dream3R\decisions\DEC-20260603-032-qwen-controller-v2-feature-policy-repair.md
14. E:\Dream3R\cycles\CYCLE-20260603-qwen-controller-v2-feature-policy-repair.md
15. E:\Dream3R\decisions\DEC-20260603-033-qwen-heldout-calibrated-controller.md
16. E:\Dream3R\cycles\CYCLE-20260603-qwen-heldout-calibrated-controller.md
17. E:\Dream3R\handoff\ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md
18. E:\Dream3R\decisions\DEC-20260602-024-native-student-decoder-gate.md
19. E:\Dream3R\decisions\DEC-20260602-025-image-state-native-student-u1.md
20. E:\Dream3R\decisions\DEC-20260602-026-vggt-omega-admission-preflight.md
21. E:\Dream3R\planning\ARCHITECTURE_MECHANISM_INTAKE.md
22. E:\Dream3R\WORKFLOW_STATUS.md

Current truth:
- Dream3R is not yet usable as a native model.
- Current bounded usable baseline is frozen-StatePrior + bounded residual:
  KITTI/ETH3D 0.1448/0.1475.
- Native student decoder is executable and state-causal but flat.
- Image-state U1 is negative; do not rerun it unchanged.
- VGGT-Omega admission is blocked on the approved checkpoint.
- Qwen3-VL-2B-Instruct is staged and schema-smoke-positive as a semantic
  controller candidate, not a 3D geometry backend.
- V11 label-cache and controller dry-run code now exists; do not recreate it.
  Start from `build_vlm_semantic_labels.py`, `build_vlm_window_manifest.py`,
  `eval_vlm_controller_dryrun.py`, `eval_vlm_calibrated_controller.py`, and
  the DEC-028 through DEC-033 gate results.
- The held-out calibrated Qwen gate is negative against shuffle. Do not train
  Router/Critic from the current 50-window cache.

Your job:
Design and execute the smallest reversible gate that tests whether VLM semantic
signals help Dream3R control decisions.

Already implemented:
1. Offline VLM semantic label cache builder with strict schema, prompt hash,
   model id, explicit failure records, mock backend, and local-only Qwen loading
   interface.
2. KITTI/ETH3D VLM window-manifest builder.
3. Router/Critic dry-run evaluator with real/shuffle/disabled controls.
4. Local mock tests and mock dry-run artifact.

Next implementation:
1. Do not repeat DEC-031 or DEC-032 unchanged.
2. Do not repeat DEC-033 unchanged; it already shows real does not beat shuffle.
3. If continuing Qwen, broaden the window set first and pre-register a real >
   shuffle > disabled promotion threshold before any Router/Critic training.
4. Keep `max_new_tokens >= 320` unless a stronger schema-constrained decoding
   route is implemented.

Frozen core files. Do not edit without a new explicit DEC:
code/dream3r/model.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/modules.py
code/dream3r/contracts.py
code/dream3r/config.py

State-causality and control requirements:
- compare real VLM labels to shuffled VLM labels;
- compare real VLM labels to VLM-disabled features;
- preserve current router/critic baselines;
- do not allow semantic labels to replace geometry evidence;
- report fallback or schema contamination explicitly.

Success criteria:
- local tests pass;
- no frozen-core diff;
- label cache schema is valid;
- failure modes are explicit;
- a next Router/Critic gate can consume the cache without changing geometry.

Final response must include:
- changed files;
- verification commands;
- whether Qwen inference actually ran or was blocked;
- exact output paths;
- next single executable gate;
- documentation chain updates.

Before final, update:
TASK_SNAPSHOT.md
WORKFLOW_STATUS.md
INDEX.md
mainwork.md
registry/decision_registry.md
README.md
RESEARCH_STATE.md
AGENT_MASTER_PROMPT.md
cycle log
```

## Short paste prompt

```text
Read E:\Dream3R\TASK_SNAPSHOT.md, then E:\Dream3R\planning\DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md and E:\Dream3R\handoff\ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md. V11 label-cache, controller dry-run, Qwen3-VL-2B weight staging, first 50-window real gate, v2 feature/policy repair, and DEC-20260603-033 held-out calibrated controller gate already exist; do not recreate them unchanged. DEC-20260603-033 is negative against shuffle, so do not train/promote Router/Critic from the current Qwen cache. Qwen is only an offline semantic controller signal, not a geometry model. Preserve frozen core files, use BUAA-Server GPU1 only for model code, and update the documented chain before final.
```
