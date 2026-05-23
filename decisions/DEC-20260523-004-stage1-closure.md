# DEC-20260523-004: Close Stage 1 — Minimum Viable Real

decision_id: DEC-20260523-004
date: 2026-05-23
stage: 1
parent_roadmap: mainwork.md
evidence_cycle: CYCLE-20260523-stage1
status: proposed (pending user ratification)

---

## Decision

Close Stage 1 (MVR) as success-criteria met.

Dream3R now runs a real KITTI image pair through:

```text
KITTI image pair
  -> DINOv3-B ONNX Perceiver
  -> existing Dream3R skeleton forward
  -> real MASt3R adapter
  -> pointmap
  -> KITTI depth abs-rel metric
```

## Success Criteria

| Criterion | Status | Evidence |
|---|---|---|
| One KITTI sequence, one image pair end-to-end | met | `2011_09_26_drive_0001_sync_02`, frames `0000000000,0000000001` |
| DINOv3-B backbone produces patch features | met | Perceiver tokens `[1, 2, 196, 768]` |
| MASt3R real adapter produces pointmap | met | backend `mast3r`, pointmap `[1, 2, 196, 3]` |
| Depth abs-rel < 0.5 | met | `0.1977723091840744` |
| Visualization nonblank/structured | met | `mast3r_depth_frame0.png`, 224x224, nonzero contrast |
| Local tests pass | met | `201 passed, 1 skipped` |
| Server tests pass | met | `199 passed, 1 skipped` |

## Documented Deviation

The roadmap requested `facebook/dinov3-vitb16-pretrain-lvd1689m` from Hugging Face. That repo is gated and the supplied account was rejected by the repo authors.

User approved using the public ONNX checkpoint `onnx-community/dinov3-vitb16-pretrain-lvd1689m-ONNX` instead. This closes Stage 1 as a real DINOv3-B integration, but not as the originally requested official PyTorch HF checkpoint path.

## Consequences

- Stage 1 status in `mainwork.md` moves from pending to done.
- Stage 2 can start from a real KITTI image-pair path and real pointmap output.
- The ONNX fallback is kept additive; default `use_backbone=False` and existing DINOv2 path remain unchanged.
- MASt3R default checkpoint path now follows project checkpoint policy: `/hdd3/kykt26/checkpoints/mast3r-vitl`.

## Linked Artifacts

- `cycles/CYCLE-20260523-stage1.md`
- `/hdd3/kykt26/checkpoints/dinov3-vitb16-onnx/`
- `/hdd3/kykt26/checkpoints/mast3r-vitl/`
- `/hdd3/kykt26/code/dream3r/runs/stage1_smoke/metrics.json`
- `/hdd3/kykt26/code/dream3r/runs/stage1_smoke/mast3r_depth_frame0.png`
