# Dream3R Real Data Smoke

Status: W19 first slice done.

Date: 2026-05-11

## Goal

Move beyond synthetic-only evidence by running the Dream3R control graph on a real RGB/depth sequence. This is a smoke/evidence path, not a trained-quality benchmark.

## First Dataset

KITTI rectified data is used first because the server already has paired files:

- RGB: `/hdd3/kykt26/data/kitti/rectified/*/*.jpg`
- Depth: `/hdd3/kykt26/data/kitti/rectified/*/*.npy`

The loader converts each depth map into a sampled pointmap with approximate scaled KITTI intrinsics, and creates deterministic RGB/depth patch features for the existing no-backbone model path.

## Command

```bash
conda run -n dream3r python -m dream3r.evaluate_real_sequence \
  --data-root /hdd3/kykt26/data \
  --max-sequences 1 \
  --max-windows 2 \
  --recurrence mamba_hybrid \
  --output demo_artifacts/real_sequence/kitti_metrics.json
```

## Expected Output

The JSON contains:

- real-data metric summary from `Evaluator`
- per-window latency
- AnchorBank occupancy
- NSA branch means
- stable promotion rate
- selected anchor 3D distance
- Critic conflict score
- recommended repair action

## Interpretation Boundary

This path proves that real RGB/depth windows now flow through Dream3R's Perceiver-free feature path, SpatialMemory, AnchorBank, Permanence, Composer, and Critic. It does not claim trained accuracy until weights and real-data training/evaluation are added.

## Server Run

Completed on 2026-05-11:

- dataset: `kitti_rectified`
- sequence: `2011_09_26_drive_0001_sync_02`
- windows: 2, each with 4 frames
- device: `cuda`
- recurrence: `mamba_hybrid`
- backend: `mamba_ssm`
- output: `/hdd3/kykt26/code/dream3r/demo_artifacts/real_sequence/kitti_metrics.json`

Observed integration signals:

- pointmap L2: `20.4747`
- depth RMSE: `21.8658`
- memory occupancy: `60.0`
- NSA branch mean: compressed `0.3927`, selected `0.6073`, sliding `0.0`
- stable promotion rate: `1.0`
- selected anchor 3D distance: `0.0653`
- state drift magnitude: `0.7299`
- recommended action: `2` on both windows

These numbers are expected to be poor as geometry accuracy because no real-data training/checkpoint was introduced. The important result for this slice is that real RGB/depth windows now produce measurable geometry, memory, NSA, Critic, and repair-action logs through the same Dream3R path used by synthetic demos.
