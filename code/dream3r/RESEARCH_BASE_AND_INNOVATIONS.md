# Dream3R Research Base and Innovation Brief

Status: research baseline summary with first real-data smoke evidence.

Date: 2026-05-10

## One-sentence positioning

Dream3R is a prototype for studying long-sequence 3D reconstruction with explicit spatial memory, geometry-based checking, multi-model interfaces, and switchable state recurrence.

## Architecture Update

Dream3R v0.3 is now organized as a bus-mediated control graph:

```text
Perceiver
  -> frame tokens, pointmap, confidence, evidence tokens

SpatialMemory
  -> active state tokens
  -> NSA compressed / selected / sliding branches
  -> stable AnchorBank recall and promote

Permanence
  -> object slots
  -> per-slot dynamic suppress
  -> ISA-style slot reference poses

Critic
  -> geometric conflict score
  -> repair action logits
  -> Sampson / depth / covisibility logs

ComposerRouter
  -> expert capability routing
  -> MASt3R / Spann3R / Fast3R-style adapter entry points

MemoryBus
  -> CR-1..CR-6 control contracts
  -> typed handoff between modules
```

The important architecture shift is that reconstruction is no longer treated as one opaque model call. Each subsystem produces inspectable signals that other subsystems consume.

## Functional Progress

Implemented and tested:

- v0.3 forward and backward pass.
- Multi-window streaming.
- DINOv2/foundation-backbone path with fallback.
- Active state recurrence.
- Stable AnchorBank memory.
- Active-to-stable promotion.
- Stable recall into NSA memory output.
- 3D-aware AnchorBank retrieval.
- NSA compressed / selected / sliding context fusion.
- Per-slot Permanence dynamic ratio and suppress handoff.
- Hungarian/cosine slot matching.
- ISA-style per-slot reference poses.
- Geometric Critic with pointmap-pair consistency.
- Critic repair action loop.
- Composer expert routing and adapter contracts.
- Real MASt3R and Spann3R adapter paths where environment permits.
- Mamba hybrid state recurrence path.
- Renderer-free GaussianHead tensor contract for future 3DGS output.
- Server sync and verification script.
- Demo script comparing cross-attention vs Mamba hybrid recurrence.
- Synthetic ablation runner, visualization pack, and artifact exporter.
- KITTI real-data smoke loader and evaluation entry.

Current verification:

- Smoke test passes.
- Full `dream3r.tests.test_*` suite passes.
- `dream3r.demo_mamba_path` passes.
- `dream3r.ablate_recurrence` passes.
- `dream3r.evaluate_real_sequence` passes on two KITTI windows.
- Local/server package file hashes match.

## Code Structure

Core files:

- `model.py`: top-level Dream3R orchestration.
- `modules.py`: Perceiver, Permanence, Critic, SpatialMemory, recurrence modules, ComposerRouter.
- `anchor_bank.py`: stable memory, write/read, 3D payloads, promote/recall support.
- `nsa_attention.py`: 3-branch native sparse attention.
- `bus.py`: typed module signals and CR gates.
- `config.py`: presets and model argument threading.
- `gaussian_head.py`: W18 Gaussian tensor contract.
- `losses.py`: pointmap, geometry, retrieval, routing, drift losses.
- `evaluate.py`: metrics including geometric Critic logs.
- `data_kitti.py`: KITTI rectified RGB/depth loader and depth-to-pointmap projection.
- `evaluate_real_sequence.py`: real sequence smoke/evaluation entry.
- `composer_experts/`: adapter registry and expert integration points.

Demo and planning files:

- `demo_mamba_path.py`: runnable Mamba-vs-cross-attention demo.
- `ablate_recurrence.py`: synthetic recurrence/memory ablation runner.
- `visualize_ablation.py`: SVG and markdown chart generation from ablation JSON.
- `export_demo_artifacts.py`: showcase artifact export.
- `DEMO_SUMMARY.md`: concise presentation summary and captured output.
- `RECENT_PROGRESS.md`: current canonical progress ledger.
- `REAL_DATA_SMOKE.md`: KITTI real-data smoke command, metrics, and caveats.
- `INITIAL_RESEARCH_DEMO_PLAN.md`: tonight closure and demo plan.
- `CYCLE_033_PLAN.md`: full workstream plan.
- `CYCLE_034_PLAN.md`: stabilization and Mamba path record.

Key tests:

- `test_state_recurrence_factory.py`: cross-attention and Mamba recurrence paths.
- `test_geometric_critic.py`: geometric Critic and config calibration.
- `test_active_stable.py`: active/stable state behavior.
- `test_3d_retrieval.py`: 3D-aware AnchorBank retrieval.
- `test_isa_slots.py`: ISA slot pose and matching behavior.
- `test_gaussian_head_contract.py`: 3DGS tensor schema.
- `test_sequence_training.py`: streaming sequence training smoke.
- `test_kitti_loader_contract.py`: real-data loader contract.
- `test_real_sequence_eval_contract.py`: real-sequence eval orchestration contract.

## Research Base

Dream3R is built on six research streams:

### 1. Generalizable 3R Reconstruction

Relevant baseline ideas:

- MASt3R-style pointmap reconstruction and matching.
- Fast3R-style many-view scaling and all-to-all reasoning.
- Spann3R-style spatial memory and streaming reconstruction.
- VGGT-style unified feed-forward geometry prediction.

Dream3R use:

- Treat these as expert capabilities or architectural references.
- Use pointmap/confidence/evidence outputs as common internal currency.

### 2. Streaming State Tokens

Relevant baseline ideas:

- CUT3R-style state token recurrence.
- Point3R / Mem3R / LONG3R-style attempts to address long-sequence forgetting.

Dream3R use:

- Active state tokens evolve per window.
- Stable AnchorBank stores durable spatial anchors.
- Active and stable state are explicitly decoupled.

### 3. Sparse Long-Context Attention

Relevant baseline ideas:

- NSA compressed / selected / sliding sparse attention.
- Efficient long-context retrieval and branch mixing.

Dream3R use:

- Compressed branch: active state tokens.
- Selected branch: AnchorBank retrieval.
- Sliding branch: recent frame tokens.

### 4. State-Space Recurrence

Relevant baseline ideas:

- Mamba-style O(N) state-space sequence modeling.
- Mamba-Transformer hybrid designs for long sequences plus global correction.

Dream3R use:

- `MambaHybridRecurrence` evolves state tokens through `mamba_ssm.Mamba`.
- Transformer cross-attention injects current-frame evidence.
- PyTorch selective-scan fallback keeps the code portable.

### 5. Geometric Self-Verification

Relevant baseline ideas:

- Epipolar consistency.
- Sampson distance.
- Covisibility and confidence consistency.
- Self-supervised geometry losses.

Dream3R use:

- Critic receives pointmap pair and confidence pair.
- Conflict score is adjusted by geometric consistency.
- Repair logits drive downstream action choices.

### 6. Future 3DGS Representation

Relevant baseline ideas:

- 3D Gaussian Splatting as real-time output representation.
- Anchor-aligned Gaussians for stable scene representation.

Dream3R use:

- `GaussianHead` defines means, scales, rotations, colors, opacity, and source anchor ids.
- Renderer is intentionally deferred until dependency approval.

## Innovation Points

### I1. Control-Graph 3R

Dream3R decomposes 3R into communicating modules rather than one black-box predictor. The MemoryBus makes module contracts observable and testable.

### I2. Active/Stable Memory Split

Active state handles short-term streaming updates. Stable AnchorBank handles long-term spatial recall. This directly targets bounded-memory forgetting.

### I3. NSA for 3D Reconstruction Memory

Dream3R maps NSA's compressed / selected / sliding branches onto active state, stable anchors, and recent windows.

### I4. Geometric Critic Repair Loop

The Critic is not just a classifier. It uses Sampson, depth, confidence, and covisibility signals to produce conflict and repair actions.

### I5. Object Permanence With ISA Slot Poses

Object slots are tied to per-slot reference poses. Matching can use both feature identity and spatial pose consistency.

### I6. Mamba-Hybrid State Recurrence

State recurrence can switch from cross-attention to a Mamba-backed hybrid path. On the server, `mamba_hybrid` uses `mamba_ssm.Mamba(use_fast_path=False)`.

### I7. Expert-Routed 3R Composition

Existing 3R systems are not copied blindly. They are represented as expert capabilities that Dream3R can route to and reason over.

### I8. Gaussian Output Contract

Dream3R defines how stable anchors and frame tokens can become Gaussian primitives before introducing renderer dependencies.

## Current Demo Evidence

Run:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.demo_mamba_path
```

Expected evidence:

- `device` is `cuda`.
- Both `cross_attention` and `mamba_hybrid` variants run.
- `mamba_hybrid.backend` is `mamba_ssm` on the server.
- `latent_state_tokens` stays `[1, 32, 128]`.
- `state_delta_mean_abs` is nonzero.
- `stable_promotion_rate` is visible in the demo.
- `nsa_branch_mean` shows active branch mixing.
- `recommended_action` is emitted by the Critic loop.

## Current Real-Data Smoke Evidence

Run:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.evaluate_real_sequence \
  --data-root /hdd3/kykt26/data \
  --max-sequences 1 \
  --max-windows 2 \
  --recurrence mamba_hybrid \
  --output demo_artifacts/real_sequence/kitti_metrics.json
```

Latest evidence:

- KITTI sequence `2011_09_26_drive_0001_sync_02`.
- Two real RGB/depth windows pass through Dream3R.
- `mamba_hybrid` uses backend `mamba_ssm`.
- Metrics include pointmap/depth error, memory occupancy, NSA branch weights, selected-anchor distance, Critic conflict, and repair action.

This is a real-data execution claim, not a quality claim.

## What This Does Not Claim Yet

Dream3R initial research does not yet claim:

- SOTA reconstruction quality on real benchmarks.
- Real-data ablation wins.
- Complete 3DGS rendering.
- Fast CUDA Mamba path stability.
- Fully calibrated Critic thresholds on real datasets.

The current claim is implementation and integration readiness: the main processing path is runnable, covered by tests, and ready for more systematic real-data evaluation.

## Next Research Milestones

### M1. Real Data Path

- Done first slice: KITTI RGB/depth loading and real sequence streaming evaluation.
- Next: DTU non-random depth/pointmap path when usable depth files exist.
- Next: expand real sequence metrics and add pose transform support.

### M2. Ablation Table

Run synthetic and real-data variants:

- `cross_attention` vs `mamba_hybrid`.
- NSA on/off.
- Active/stable memory on/off.
- Critic repair on/off.
- Expert routing on/off.

### M3. Critic Calibration

- Fit geometric conflict scale to real distributions.
- Track false positive/false negative repair decisions.
- Add ECE-style calibration metrics.

### M4. Expert Routing Quality

- Compare expert choice against output quality and runtime.
- Finish Fast3R dependency path if approved.
- Evaluate when MASt3R/Spann3R should be selected.

### M5. 3DGS Renderer

- Choose renderer backend.
- Wire `GaussianHead` into `Dream3R.forward()`.
- Add render loss only after real renderer support exists.

## Paper Skeleton

Working title:

> Dream3R: Control-Graph Streaming 3D Reconstruction with Active-Stable Memory, Geometric Critique, and Mamba Hybrid Recurrence

Proposed sections:

1. Introduction: fragmentation of current 3R systems.
2. Related Work: 3R, streaming memory, sparse attention, Mamba, geometric verification, 3DGS.
3. Architecture: control graph and bus contracts.
4. Memory: active/stable state, AnchorBank, NSA.
5. Verification and Repair: geometric Critic.
6. Object Permanence: slot reference frames.
7. Mamba Hybrid Recurrence.
8. Experiments: synthetic integration now, real-data ablation next.
9. Limitations and Roadmap.

## Formal presentation summary

本阶段完成了从研究路线、架构设计到可运行原型的推进。当前结果说明系统流程已经打通，并且可以在合成输入和 KITTI 真实数据上记录关键中间信号。下一阶段的重点是用真实数据消融、几何自检校准和多模型调度评估，验证这些设计是否能带来稳定的质量或效率收益。
