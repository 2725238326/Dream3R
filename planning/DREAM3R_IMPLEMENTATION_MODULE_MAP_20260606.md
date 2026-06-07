# Dream3R Implementation Module Map

Date: 2026-06-06
Purpose: explain what each implemented module does, what is release-claimable,
and where to continue fast without reopening broad exploration.

Update: NativeStudentDecoder objective patches were implemented and tested after
this map was created. Dropout-consistency and temporal/scale proxy gate20 runs
remain flat at `0.1451 / 0.1480`, so the RC is unchanged.

## Current Short Answer

Dream3R currently has a release-candidate implementation, but not the full
ideal proposal-free model.

Release-candidate path:

```text
real proposal teachers
-> cached proposal bank
-> Dream state / conflict metadata
-> frozen StatePrior
-> bounded convex fusion
-> disagreement-bounded residual refinement
```

Selected RC:

```text
frozen StatePrior + bounded residual refinement
KITTI / ETH3D abs-rel: 0.1448 / 0.1475
```

Metric direction: lower is better.

## Module Map

| Layer | File(s) | What It Does | Status | Claim Boundary |
| --- | --- | --- | --- | --- |
| Main frozen model | `code/dream3r/model.py` | Main Dream3R forward path wiring perception, memory, permanence, critic, composer, and reconstruction outputs. | frozen core | Do not edit for RC packaging. |
| Perception / memory / critic blocks | `code/dream3r/modules.py` | Implements Perceiver, MemorySSM, Permanence, Critic, Composer, state recurrence, spatial memory, and routing surfaces. | implemented mixed scaffold/active | Useful architecture substrate; not all sub-blocks are metric-promoted. |
| Signal bus | `code/dream3r/bus.py` | MemoryBus plus CR1-CR5 signal gates and handoff labels. | implemented | Contract substrate, not standalone quality evidence. |
| Anchor memory | `code/dream3r/anchor_bank.py` | Read/write/prune/quarantine/promote/tick API for stable anchors. | implemented | Architecture mechanism; not the RC metric driver. |
| NSA attention | `code/dream3r/nsa_attention.py` | Compressed, selected, and sliding attention branches. | implemented | Mechanism support; not currently the release metric claim. |
| v0.4 typed contracts | `code/dream3r/contracts.py` | Dataclasses for Perception, Memory, Permanence, Critic, Composer, expert dispatch, repair, reconstruction. | implemented | Good for pipeline clarity and QA. |
| v0.4 pipeline | `code/dream3r/orchestrator.py` | Wraps the model into a typed V04Pipeline with dispatch and assembled outputs. | implemented | Contract/pipeline evidence, not RC head. |
| Repair executor | `code/dream3r/repair.py` | Local rerun, window rerun, Test3R off-path, and action recording. | implemented | Repair scaffold; not release head. |
| SCF head | `code/dream3r/scf_head.py` | Multi-expert state-conditioned convex fusion over proposal caches. | accepted earlier baseline | Precursor to RC; shows proposal fusion works. |
| StatePrior head | `code/dream3r/state_prior_head.py` | State-only expert prior over cached real proposals. | accepted diagnostic | Evidence that Dream state carries useful expert-prior signal. |
| ProposalSetDecoder | `code/dream3r/proposal_set_decoder.py` | Per-patch proposal-set mixing, explicit StatePrior-style branch, bounded residual refinement. | RC implementation surface | Release path when StatePrior is loaded/frozen and residual is bounded. |
| Native student decoder | `code/dream3r/native_student_decoder.py` | Compact student over frozen StatePrior teacher with proposal dropout plus optional dropout-consistency / temporal / scale objectives in the trainer. | executable; objective patches tested; flat vs RC | Preserves causality but does not beat RC. |
| Image-state student | `code/dream3r/image_state_student_decoder.py` | Image-token native reconstruction path with optional proposal anchors. | negative gate | Implemented but not usable as current model. |
| VGGT-Omega admission | `code/dream3r/scripts/smoke_vggt_omega_adapter.py`, `eval_vggt_omega_oracle_admission.py`, `stage_vggt_omega_admission.py` | Real VGGT-Omega backend smoke, oracle admission, 4-expert cache creation. | admitted teacher lane | Future teacher; not RC. |
| Qwen semantic controller | `code/dream3r/scripts/build_vlm_semantic_labels.py`, `eval_vlm_controller_dryrun.py`, `eval_vlm_calibrated_controller.py`, `eval_vlm_semantic_critic_gate.py` | Strict JSON semantic labels plus real/shuffle/disabled controls. | diagnostic only | Not geometry and not current controller. |

## How The RC Path Is Written

### 1. StatePriorHead

File: `code/dream3r/state_prior_head.py`

Key idea:

```text
memory_context + conflict_score -> expert logits -> convex proposal fusion
```

It intentionally avoids proposal geometry in the weighting network so the gate
can isolate whether Dream state itself predicts useful expert preference.

Output:

```text
final_pointmap
final_confidence
expert_weights
```

Status:

```text
accepted diagnostic; state signal is real
```

Do not overclaim it as the final model head.

### 2. ProposalSetDecoder

File: `code/dream3r/proposal_set_decoder.py`

Key idea:

```text
proposal xyz/confidence/residual-to-mean
+ Dream state
+ conflict score
+ expert identity
-> per-patch proposal mixer
-> expert weights
-> convex fused base
-> bounded residual delta
```

Important properties:

- Uses scale-normalized proposal pointmaps.
- Has an explicit StatePrior-style MLP branch.
- Can load a pretrained StatePrior checkpoint into that branch.
- Can freeze the StatePrior branch.
- Residual refinement is bounded by local proposal disagreement.
- Initial residual output is zero-initialized.

Output:

```text
final_pointmap
base_pointmap
residual_delta
final_confidence
expert_weights
state_prior_weights
uncertainty
```

Status:

```text
release-candidate surface when run as frozen StatePrior + bounded residual
```

### 3. Training Script For RC

File: `code/dream3r/scripts/train_proposal_set_decoder.py`

Key flags:

```text
--state-prior-checkpoint
--freeze-state-prior
--prior-kl-weight
--residual-refine-scale
--shuffle-state
--no-state
```

This is the script that makes the causality controls possible:

```text
correct-state
no-state
shuffle-state
```

Selected artifact:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
```

## What Is Implemented But Not Promoted

### NativeStudentDecoder

File: `code/dream3r/native_student_decoder.py`

What it does:

```text
frozen StatePrior teacher
+ proposal dropout
+ student residual
-> native-ish student output
```

Result:

```text
correct-state: 0.1451 / 0.1480
selected RC:   0.1448 / 0.1475
```

Follow-up objective gates:

```text
P1 dropout-consistency gate20:          0.1451 / 0.1480
P2 dropout + temporal/scale gate20:    0.1451 / 0.1480
no-state / shuffle controls:           still worse than correct-state
fallback_contamination_count:          0
```

Conclusion:

```text
executable and causal, but simple objective strengthening did not beat RC
```

### ImageStateStudentDecoder

File: `code/dream3r/image_state_student_decoder.py`

What it does:

```text
image tokens + state tokens + optional proposal anchors -> pointmap
```

Result:

```text
correct-state loses to no-state and baseline
```

Conclusion:

```text
implemented but negative; do not rerun unchanged
```

### VGGT-Omega

What is implemented:

```text
checkpoint staging
real backend smoke
oracle admission evaluator
4-expert SCF cache/control gate
```

Result:

```text
ETH3D oracle-positive
KITTI/state-control release-negative
```

Conclusion:

```text
future domain-conditional teacher, not RC
```

### Qwen3-VL

What is implemented:

```text
strict semantic JSON schema
mock backend tests
real staged Qwen label cache
controller dry-run
held-out calibrated controller
semantic Critic-prior gate
```

Result:

```text
diagnostic negative against shuffle/geometry controls
```

Conclusion:

```text
offline annotation only, not model path
```

## What You Can Tell Others

Safe claim:

```text
We implemented a controlled state-conditioned proposal-fusion architecture.
The usable RC freezes the learned StatePrior and applies only bounded residual
refinement. It passes shuffle-state controls on KITTI/ETH3D.
```

Unsafe claim:

```text
We implemented a complete proposal-free Dream3R geometry foundation model.
```

## Fastest Next Engineering Route

Do not reopen Qwen or rerun U1 unchanged.

The fastest useful next route after the native objective gates is:

1. Keep RC frozen for release.
2. Build presentation/manuscript around `release/`.
3. Do not repeat native-student dropout/temporal/scale objective sweeps unless
   the teacher/target design changes.
4. Any future model-improvement branch must reuse the same three controls:

```text
correct-state
no-state
shuffle-state
```

5. Promote only if it beats:

```text
KITTI / ETH3D: 0.1448 / 0.1475
```

Detailed execution record:

```text
planning/DREAM3R_FAST_MODULE_COMPLETION_OPTIMIZATION_PLAN_20260606.md
decisions/DEC-20260606-038-native-student-objective-gates.md
```

## Module Ownership For Next Edits

| Goal | Edit Here | Do Not Edit |
| --- | --- | --- |
| Release packaging | `release/`, `planning/`, top-level docs | frozen core |
| RC rerun or ablation | `scripts/train_proposal_set_decoder.py`, run scripts | `model.py`, `modules.py` |
| Native student improvement | `native_student_decoder.py`, `scripts/train_native_student_decoder.py` | RC artifacts; do not repeat same objective sweeps unchanged |
| Image-native redesign | `image_state_student_decoder.py`, cache/trainer scripts | do not rerun U1 unchanged |
| VGGT teacher research | VGGT admission/eval scripts | do not call it RC without controls |
| Qwen diagnostics | VLM semantic scripts | do not use as geometry |

## Current Completion Estimate

| Scope | Completion | Reason |
| --- | ---: | --- |
| Release-candidate architecture | 80-85% | implemented, tested, server artifacts selected, docs packaged |
| Full Dream3R ideal architecture | 40-50% | state-conditioned fusion works; native proposal-free decoder not competitive |
| External presentation package | 70-80% | method one-pager, figure, result tables, outline exist; needs slide/deck rendering |
| Paper-scale evaluation | 25-35% | controlled RC evidence exists; broader multi-seed/multi-dataset benchmark not complete |
