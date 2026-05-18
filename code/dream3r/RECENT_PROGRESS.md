# Dream3R Recent Progress Ledger

Status: current canonical summary for Cycle 033/034 and W19-W22.

Date: 2026-05-11

## What Changed

Dream3R has moved from a broad architecture sketch into a runnable, test-covered control-graph prototype with first real-data smoke evidence.

The current system includes:

- Perceiver/evidence path with DINOv2-compatible frozen-backbone support and fallback.
- SpatialMemory with NSA compressed / selected / sliding branches.
- Active state tokens and stable AnchorBank promote/recall.
- 3D-aware stable memory payloads and retrieval.
- Permanence slots with per-slot suppress and ISA-style reference poses.
- Geometric Critic with Sampson/depth/covisibility signals and repair actions.
- ComposerRouter and external 3R expert adapter contracts.
- Mamba hybrid state recurrence using server `mamba_ssm` when available.
- Renderer-free GaussianHead tensor contract for future 3DGS output.
- Synthetic ablation runner and visualization/export pack.
- KITTI real RGB/depth loader and real-sequence evaluation entry.

## Evidence Tiers

### Tier 1: Integration Verified

These are supported by server smoke and full unit tests:

- v0.3 forward/backward pass.
- multi-window streaming state update.
- NSA branch mixing.
- active-to-stable memory promote/recall.
- 3D-aware AnchorBank retrieval.
- Critic repair action handoff.
- permanence slot pose tracking.
- Mamba recurrence factory and demo path.
- Gaussian tensor contract.
- synthetic ablation and visualization artifact export.
- KITTI loader and real-sequence eval orchestration.

### Tier 2: Real Data Smoke Verified

KITTI rectified RGB/depth windows now run through Dream3R:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.evaluate_real_sequence \
  --data-root /hdd3/kykt26/data \
  --max-sequences 1 \
  --max-windows 2 \
  --recurrence mamba_hybrid \
  --output demo_artifacts/real_sequence/kitti_metrics.json
```

Latest server result:

- dataset: `kitti_rectified`
- sequence: `2011_09_26_drive_0001_sync_02`
- windows: 2
- device: `cuda`
- recurrence backend: `mamba_ssm`
- output JSON: `/hdd3/kykt26/code/dream3r/demo_artifacts/real_sequence/kitti_metrics.json`

Observed signals:

- pointmap L2: `20.4747`
- depth RMSE: `21.8658`
- memory occupancy: `60.0`
- NSA branch mean: compressed `0.3927`, selected `0.6073`, sliding `0.0`
- stable promotion rate: `1.0`
- selected anchor 3D distance: `0.0653`
- state drift magnitude: `0.7299`
- repair action: `2` on both windows

Interpretation: this is real-data integration evidence, not trained reconstruction quality.

### Tier 3: Research Claims Still Pending

These must not be claimed as solved yet:

- SOTA reconstruction accuracy.
- real-data ablation gains.
- calibrated real-data Critic thresholds.
- expert routing quality improvement.
- long-sequence degradation curves.
- renderer-backed 3DGS output.
- test-time adaptation gains.

## Demo Entry Points

### Synthetic Architecture Demo

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.demo_mamba_path
```

Shows:

- `cross_attention` and `mamba_hybrid` switchability.
- server `mamba_ssm` backend.
- active state change across windows.
- stable memory promotion.
- NSA branch mixing.
- Critic repair action output.

### Synthetic Ablation Demo

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.ablate_recurrence --windows 3 --seeds 33 34 35
```

Variants:

- `baseline_cross_attention`
- `mamba_hybrid`
- `no_nsa`
- `no_stable_memory`

### Demo Artifact Export

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.export_demo_artifacts \
  --output-dir demo_artifacts/showcase
```

Produces manifest JSON, demo JSON, ablation JSON, SVG charts, and copied key docs.

## Verification Snapshot

Latest verified on server:

- `sync_verify_server.ps1 -Mode verify`: local/server package files match.
- `dream3r.tests.test_kitti_loader_contract`: pass.
- `dream3r.tests.test_real_sequence_eval_contract`: pass.
- `dream3r.smoke_test`: pass.
- `sync_verify_server.ps1 -Mode test -FullTests`: pass.
- `dream3r.evaluate_real_sequence`: two real KITTI windows pass.

All torch/model/test commands are run only on the server conda environment:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m <module>
```

Local Windows is used for editing and markdown only.

## Current Architecture Position

Dream3R should be described as:

> a control-graph streaming 3R prototype that integrates active/stable spatial memory, NSA retrieval, geometric self-critique, expert routing, object permanence, and switchable Mamba/cross-attention recurrence.

It should not yet be described as:

> a trained SOTA real-data 3R model.

## Immediate Next Work

1. Real-data ablation table using the same variant names as synthetic ablation.
2. Critic calibration on real geometry distributions.
3. Expert routing quality report with real/fallback adapter availability.
4. DTU non-random depth/pointmap path if usable depth files exist.
5. Paper/demo pack cleanup: keep claims tied to tests, metrics, or JSON artifacts.
