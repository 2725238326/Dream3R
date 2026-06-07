# DEC-20260607-045: Foundation3R 50x2 dense teacher cache

Date: 2026-06-07
Status: accepted as data-gate positive
Scope: Dream3R proposal-free Foundation3R line

## Context

DEC-044 proved the Foundation3R contract and 1-window real VGGT-Omega dense
teacher cache path. The next gate was to scale the same path to a small but
non-trivial KITTI/ETH3D cache before writing training code.

## Decision

Build a real `50+50` Foundation3R dense teacher cache on BUAA-Server GPU1:

```text
KITTI: 50 windows
ETH3D: 50 windows
teacher backend: VGGT-Omega
```

The cache remains training-only. It must not store proposal-bank fields or
allow teacher/proposal use at inference.

## Server Artifacts

Server paths:

```text
BUAA-Server:/hdd3/kykt26/code/dream3r/runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/kitti_dense_teacher_cache.pt
BUAA-Server:/hdd3/kykt26/code/dream3r/runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/eth3d_dense_teacher_cache.pt
BUAA-Server:/hdd3/kykt26/code/dream3r/runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/dense_teacher_50x2_audit.json
```

Local mirrored reports:

```text
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/kitti_dense_teacher_cache.json
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/eth3d_dense_teacher_cache.json
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/dense_teacher_50x2_audit.json
```

The `.pt` training caches are intentionally kept on the server.

## Result

Audit summary:

```text
status: pass
KITTI n_windows: 50
ETH3D n_windows: 50
n_failures: 0 / 0
fallback_contamination_count: 0 / 0
proposal_inputs_used: false / false
teacher_used_at_inference: false / false
proposal_fields_stripped: true / true
forbidden_leak_count: 0 / 0
shape_fail_count: 0 / 0
missing_gt_count: 0 / 0
missing_state_count: 0 / 0
teacher_pointmap shape: [4,196,3]
teacher_confidence shape: [4,196,1]
teacher_valid_mask shape: [4,196]
```

## Verdict

The Foundation3R data gate is positive. Dream3R now has a verified real dense
teacher cache path for proposal-free training.

This is not a trained model result. It authorizes the next engineering step:

```text
implement train_foundation3r.py
run 1-epoch smoke
run 20-epoch 50+50 state/no-state/shuffle gate
keep proposal leak audit mandatory
```

Do not use this cache to claim model quality until a trained Foundation3R
checkpoint passes state-causality and proposal-leak controls.
