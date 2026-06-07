# Cycle 20260607: Foundation3R 50x2 Dense Teacher Cache

Date: 2026-06-07
Status: closed data-gate-positive
Decision: `decisions/DEC-20260607-045-foundation3r-50x2-dense-teacher-cache.md`

## Goal

Scale the Foundation3R dense teacher path from 1-window smoke to a `50+50`
real VGGT-Omega training cache.

## Action

Built manifests on BUAA-Server:

```text
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/kitti_50win_manifest.json
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/eth3d_50win_manifest.json
```

Generated real VGGT-Omega dense teacher caches on GPU1:

```text
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/kitti_dense_teacher_cache.pt
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/eth3d_dense_teacher_cache.pt
```

Ran server schema/leak audit and mirrored JSON reports locally.

## Result

```text
KITTI: 50/50 windows, failures 0, fallback 0
ETH3D: 50/50 windows, failures 0, fallback 0
proposal_fields_stripped: true
proposal_inputs_used: false
teacher_used_at_inference: false
forbidden_leak_count: 0
shape_fail_count: 0
missing_gt_count: 0
missing_state_count: 0
```

## Verdict

Positive data gate. Foundation3R now has a real 50+50 dense teacher training
cache with clean proposal-leak controls.

Next work is not more cache plumbing. It is `train_foundation3r.py`, followed
by a 1-epoch smoke and a 20-epoch 50+50 state/no-state/shuffle gate.
