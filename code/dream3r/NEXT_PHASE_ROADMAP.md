# Dream3R Next Phase Roadmap

Status: W19 first real-data smoke complete; W20-W22 baseline complete.

Date: 2026-05-10

## Purpose

Cycle 033/034 turned Dream3R into a runnable control-graph 3R prototype. The next phase must turn this into research evidence:

- Clear SOTA feature mapping.
- Real-data execution.
- Ablation tables.
- Visual evidence.
- Expert routing quality.
- Renderer and TTT paths only after core evidence is stable.

This roadmap covers the broad plan after the initial demo.

## Current Baseline

Implemented:

- Perceiver with DINO/fallback backbone path.
- SpatialMemory with NSA compressed/selected/sliding branches.
- AnchorBank stable memory with spatial payloads.
- Active/stable state promote and recall.
- Mamba hybrid recurrence path with `mamba_ssm` backend.
- Permanence slots with ISA-style reference poses.
- Geometric Critic repair loop.
- Composer expert routing and adapter contracts.
- GaussianHead tensor contract.
- Synthetic ablation runner for recurrence / NSA / stable memory.
- KITTI real-data smoke loader and `evaluate_real_sequence.py` entry.
- Demo artifact visualization/export pack.

Verified:

- Smoke test passes.
- Full `dream3r.tests.test_*` suite passes.
- `dream3r.demo_mamba_path` passes.
- `dream3r.ablate_recurrence` passes.
- `dream3r.evaluate_real_sequence` runs two real KITTI windows with `mamba_hybrid`.
- `dream3r.export_demo_artifacts` produces showcase JSON/charts/docs.
- Local/server package files match.

## Strategic Priorities

Order matters. Do not jump to renderer or new methods before real-data evidence exists.

1. Presentation and research framing.
2. Real data and metrics.
3. Ablations on the current architecture.
4. Visual diagnostics.
5. Expert routing quality.
6. Test-time adaptation and causal decoder comparisons.
7. 3DGS renderer path.

## W19: Real Data Path

Priority: highest after demo.

### Goal

Replace synthetic-only evidence with real image/depth/pose sequence evaluation.

### Scope

- DTU loader:
  - images
  - cameras
  - depth maps if available
  - pair/window construction
- KITTI loader:
  - continuous frame windows
  - camera intrinsics/extrinsics if available
- Ground-truth pointmap generation:
  - depth + camera intrinsics -> 3D points
  - pose transform support
- Real evaluation entry:
  - one command to run a few real windows
  - save metrics JSON

### Metrics

- pointmap L1 / RMSE
- depth AbsRel / RMSE
- confidence-weighted pointmap error
- sequence drift proxy
- memory occupancy over time
- NSA branch weights over time
- Critic conflict over time

### Files

- `data_dtu.py`
- `data_kitti.py`
- `evaluate_real_sequence.py`
- `tests/test_dtu_loader_contract.py`
- `tests/test_real_pointmap_generation.py`

### Exit Criteria

- Done first slice: KITTI rectified RGB/depth windows load without random tensors.
- Done first slice: two real sequence windows run through Dream3R.
- Done first slice: evaluation JSON is produced by `evaluate_real_sequence.py`.
- Remaining: DTU scene loader needs non-random depth/pointmap targets when depth files are available.
- Smoke and full tests remain passing.

## W20: SOTA Feature Matrix

Priority: immediate for demo and paper framing.

### Goal

Systematically map external 3R strengths into Dream3R modules.

### Methods to cover

- MASt3R
- Fast3R
- Spann3R
- CUT3R
- VGGT
- Point3R
- Mem3R / LONG3R
- STream3R
- OnlineX
- tttLRM
- DINOv2/v3
- NSA
- Mamba
- 3DGS / AnchorSplat

### Matrix columns

- Method
- Core strength
- Limitation
- Dream3R module that absorbs it
- Implementation status
- Evidence/test
- Remaining gap

### Files

- `SOTA_FEATURE_MATRIX.md`
- optionally `ATTENTION_RESEARCH_MATRIX.md` refresh

### Exit Criteria

- Every referenced method has an explicit Dream3R mapping.
- No method is only name-dropped.
- Demo/paper claims can cite this matrix.

## W21: Ablation Suite

Priority: high.

### Goal

Move from one-off synthetic checks to repeatable ablation tables.

### Initial ablations

- Recurrence:
  - cross-attention
  - Mamba hybrid
- Memory:
  - NSA on/off
  - stable memory on/off
  - active/stable promote threshold variants
- Critic:
  - geometric Critic on/off
  - repair action consumed/not consumed
- Expert routing:
  - learned router
  - fixed expert
  - cost-aware vs quality-only

### Metrics

Synthetic now:

- runtime
- state delta
- latent drift
- stable promotion rate
- NSA branch weights
- conflict score
- recommended action distribution

Real data now available for next table:

- pointmap/depth error via `evaluate_real_sequence.py`
- drift
- quality/runtime tradeoff

### Files

- `ablate_recurrence.py` already exists.
- Add `ablate_memory.py` only if recurrence runner becomes too broad.
- `ABLATION_BASELINE.md`
- `ABLATION_REALDATA.md` later.

### Exit Criteria

- One command runs the initial synthetic ablation table.
- Real-data table uses same variant naming.
- Tables are versioned in markdown.

## W22: Visualization Pack

Priority: high for presentation and debugging.

### Goal

Turn JSON/debug tensors into visual evidence.

### Visuals

- NSA branch weights over time.
- AnchorBank occupancy and stable score over time.
- Selected anchor 3D distance histogram.
- Critic conflict timeline.
- Repair action timeline.
- Active vs stable memory promotion timeline.
- Slot pose trajectories.
- Mamba vs cross-attention state drift curve.

### Files

- `visualize_logs.py`
- `scripts/export_demo_artifacts.ps1`
- `demo_artifacts/`
- `VISUALIZATION_GUIDE.md`

### Exit Criteria

- Demo run can produce at least 3 PNG charts.
- Charts use saved JSON, not live-only tensors.
- Visualizations do not require extra packages beyond current environment.

## W23: Expert Routing Quality

Priority: medium-high.

### Goal

Show ComposerRouter is useful, not just wired.

### Scope

- Adapter availability report.
- Fixed expert vs routed expert comparison.
- Runtime/quality table.
- MASt3R and Spann3R real dispatch where available.
- Fast3R and CUT3R dependency status.

### Metrics

- selected expert frequency
- dispatch latency
- pointmap/depth proxy error
- route regret
- capability match
- cost-adjusted score

### Files

- `evaluate_expert_routing.py`
- `EXPERT_ROUTING_REPORT.md`
- `tests/test_expert_routing_eval_contract.py`

### Exit Criteria

- Router decisions are logged.
- At least two real/fallback experts can be compared under the same interface.
- Report identifies dependency blockers honestly.

## W24: Critic Calibration

Priority: medium-high.

### Goal

Make geometric Critic thresholds meaningful on real data.

### Scope

- Collect Sampson/depth/covisibility distributions.
- Fit `critic_geometric_conflict_scale`.
- Track repair action precision/recall.
- Add calibration curves or bins.

### Metrics

- conflict AUROC if labels exist
- ECE-style calibration
- false positive repair rate
- false negative conflict rate
- mean geometric residual under recommended actions

### Files

- `calibrate_critic.py`
- `CRITIC_CALIBRATION.md`
- `tests/test_critic_calibration_contract.py`

### Exit Criteria

- Calibration script runs on synthetic and real subset.
- Config recommendation is documented.
- Metrics are included in evaluation output.

## W25: Test-Time Adaptation Path

Priority: medium, after real-data baseline.

### Motivation

`tttLRM` and related work suggest test-time layers can improve scene-specific geometry without full retraining.

### Scope

- Freeze backbone and most Dream3R modules.
- Allow small adaptation modules:
  - evidence projector
  - state refinement adapter
  - GaussianHead adapter later
- Run N adaptation steps on one sequence.
- Compare before/after geometry metrics.

### Files

- `test_time_adapt.py`
- `TTT_PLAN.md`
- `tests/test_ttt_contract.py`

### Exit Criteria

- TTT loop runs on synthetic and one real subset.
- No global checkpoint mutation unless explicitly requested.
- Before/after metrics are logged.

## W26: STream3R / Causal Decoder Relation

Priority: medium, design first.

### Motivation

STream3R-style causal decoder-only 3R is a different streaming route. Dream3R currently uses state recurrence + NSA, not a decoder-only architecture.

### Scope

- Write architectural comparison.
- Define what Dream3R gains/loses relative to causal decoder-only.
- Consider optional causal decoder adapter, not core rewrite.

### Files

- `STREAM3R_RELATION.md`
- optional `causal_decoder_adapter.py` only after design approval.

### Exit Criteria

- Relationship is explicit in paper framing.
- No unsupported claim that Dream3R implements STream3R.

## W27: 3DGS Renderer Path

Priority: later, dependency-gated.

### Goal

Turn GaussianHead contract into renderable outputs.

### Scope

- Choose renderer:
  - `gsplat`
  - `diff-gaussian-rasterization`
  - other available backend
- Wire `GaussianHead` into `Dream3R.forward()`.
- Map AnchorBank stable entries to persistent Gaussians.
- Add render output only when backend exists.
- Add photometric loss only when render is real.

### Files

- `gaussian_head.py`
- `render_gaussians.py`
- `tests/test_gaussian_render_contract.py`
- `GAUSSIAN_RENDER_PLAN.md`

### Exit Criteria

- Renderer dependency approved and installed.
- Rendered image tensor is produced.
- Photometric loss has nonzero real rendering path.

## W28: Training Infrastructure Hardening

Priority: medium.

### Scope

- Checkpoint resume path test.
- Deterministic seed protocol.
- Run metadata capture.
- Config snapshots per run.
- Failure-safe logging.

### Files

- `train.py`
- `tests/test_checkpoint_resume.py`
- `RUN_PROTOCOL.md`

### Exit Criteria

- One interrupted/resumed short run reproduces expected state.
- Run directory contains config, metrics, and environment summary.

## W29: Documentation and Paper Pack

Priority: continuous.

### Scope

- Keep architecture diagram current.
- Maintain method matrix.
- Maintain ablation tables.
- Maintain limitations section.
- Track claims vs evidence.

### Files

- `RESEARCH_BASE_AND_INNOVATIONS.md`
- `SOTA_FEATURE_MATRIX.md`
- `ABLATION_BASELINE.md`
- `DEMO_SUMMARY.md`
- `PAPER_OUTLINE.md`

### Exit Criteria

- Every public claim has a file/test/demo backing it.
- Limitations are stated before reviewers ask.

## Recommended Execution Order

### Immediate, before/around demo

1. W20 SOTA feature matrix.
2. W22 visualization pack from existing demo/ablation JSON.
3. Keep W21 synthetic ablation baseline updated.
4. Use W19 KITTI smoke as real-data proof of execution, not quality.

### First research sprint

1. W21 real-data ablations.
2. W24 Critic calibration.
3. W23 expert routing quality.

### Second research sprint

1. W23 expert routing quality.
2. W25 test-time adaptation.
3. W26 STream3R relation.

### Later dependency-gated sprint

1. W27 3DGS renderer path.
2. W28 training hardening.
3. W29 paper pack.

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Synthetic results overclaimed | High | Label all current tables as integration evidence only |
| Real data loader takes longer than expected | High | Start with one DTU scene and one command |
| Mamba fast path ABI mismatch | Medium | Continue `use_fast_path=False`, document clearly |
| Expert dependencies block real routing | Medium | Separate availability from quality comparison |
| 3DGS renderer dependency churn | Medium | Keep GaussianHead contract separate until renderer approved |
| Visualization requires extra packages | Low | Use matplotlib if present; otherwise save CSV/JSON first |

## Final Direction

The next phase is not more architecture breadth for its own sake. The architecture is broad enough. The immediate task is converting breadth into evidence:

1. map external methods to Dream3R modules,
2. run real data,
3. ablate each architectural claim,
4. visualize signals,
5. then extend into TTT and 3DGS.
