# CYCLE-20260523-stage1: Stage 1 MVR closure

cycle_id: CYCLE-20260523-stage1
date: 2026-05-23
stage: 1 (Minimum Viable Real)
status: success-criteria-met

---

## Objective

Replace the random-tensor Stage 0 path with one real KITTI image pair, a real DINOv3-B backbone path, and a real MASt3R expert pointmap, then measure depth against KITTI projected depth.

## Implementation Summary

### T1.1 DINOv3 backbone

- Official `facebook/dinov3-vitb16-pretrain-lvd1689m` HF repo was gated and access was rejected for the supplied token.
- User approved public ONNX fallback: `onnx-community/dinov3-vitb16-pretrain-lvd1689m-ONNX`.
- Added `dinov3_vitb16_onnx` Perceiver branch via ONNXRuntime.
- Added `small_real` preset.
- Uploaded checkpoint to `/hdd3/kykt26/checkpoints/dinov3-vitb16-onnx/`.
- Installed `onnxruntime` CPU package in server `dream3r` env.

Evidence:

- Server smoke: `_ONNXBackbone`, output `(1, 4, 196, 768)`, frozen `True`.
- Local tests include `tests/test_dinov3_backbone.py`.

### T1.2 KITTI pair dataloader

- Added `dream3r.data.kitti_pair.KITTIPairDataset`.
- Loader reads existing rectified `jpg + npy depth + cam.txt` files.
- Output contract:
  - `images`: `[2, 3, H, W]`
  - `intrinsics`: `[2, 3, 3]`
  - `depth_gt`: `[2, H, W]`
  - `valid_mask`: `[2, H, W]`

Evidence:

- Server smoke on `/hdd3/kykt26/data/kitti/rectified`: 315 pairs in first sequence.
- First pair shape: images `(2, 3, 128, 416)`, intrinsics `(2, 3, 3)`, depth/mask `(2, 128, 416)`.

### T1.3 MASt3R real adapter

- Downloaded `naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric` to local `downloads/mast3r-vitl`.
- Uploaded snapshot to `/hdd3/kykt26/checkpoints/mast3r-vitl/`.
- Cleaned local download after upload.
- Repointed adapter default checkpoint to `/hdd3/kykt26/checkpoints/mast3r-vitl`.
- Reused existing official repo at `/hdd3/kykt26/code/mast3r`.
- Fixed real adapter preprocessing to match MASt3R `ImgNorm`: `[0,1] -> [-1,1]`.

Evidence:

- `DREAM3R_RUN_MAST3R_REAL=1` server test passed on GPU.
- KITTI pair smoke: pointmap `(1, 2, 196, 3)`, confidence `(1, 2, 196, 1)`, nonzero pointmap sum `4956.8979`, confidence mean `0.8467`, backend `mast3r`.

### T1.4 End-to-end real smoke

Added `dream3r.scripts.smoke_real_e2e`.

Pipeline:

```text
KITTI pair
  -> DINOv3-B ONNX Perceiver via Dream3R(CONFIGS["small_real"])
  -> existing Memory/Critic/Composer skeleton forward
  -> MASt3R real adapter
  -> pointmap
  -> raw depth_abs_rel vs KITTI projected depth
```

Key implementation choice:

- Perceiver uses 224x224 to keep `[1, 2, 196, 768]` tokens.
- MASt3R uses 512x160 KITTI-wide input to preserve geometry; raw metric depth is evaluated without median scaling.

Server command:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 MAST3R_REPO=/hdd3/kykt26/code/mast3r \
conda run -n dream3r python -m dream3r.scripts.smoke_real_e2e \
  --kitti_seq 00 \
  --pair 0,1 \
  --output /hdd3/kykt26/code/dream3r/runs/stage1_smoke/
```

Result:

```json
{
  "sequence_name": "2011_09_26_drive_0001_sync_02",
  "frame_ids": ["0000000000", "0000000001"],
  "perceiver_tokens": [1, 2, 196, 768],
  "mast3r_input_shape": [1, 2, 3, 160, 512],
  "expert_backend": "mast3r",
  "pointmap_shape": [1, 2, 196, 3],
  "confidence_shape": [1, 2, 196, 1],
  "depth_abs_rel": 0.1977723091840744
}
```

Visualization:

- Server: `/hdd3/kykt26/code/dream3r/runs/stage1_smoke/mast3r_depth_frame0.png`
- Local verification copy: `E:\Dream3R\tmp_verify\mast3r_depth_frame0.png`
- PNG stats: shape `(224, 224)`, min `0`, max `255`, std `60.1454`; visually structured, not blank/noise.

## Tests

- Local: `python -m pytest tests/ -q` -> `201 passed, 1 skipped`.
- Server: `conda run -n dream3r python -m pytest dream3r/tests/ -q` -> `199 passed, 1 skipped`.
- Server real MASt3R: `DREAM3R_RUN_MAST3R_REAL=1 ... pytest dream3r/tests/test_mast3r_real.py -q -s` -> `1 passed`.

## Files Changed

- `.gitignore`
- `code/dream3r/modules.py`
- `code/dream3r/config.py`
- `code/dream3r/model.py`
- `code/dream3r/data/__init__.py`
- `code/dream3r/data/kitti_pair.py`
- `code/dream3r/composer_experts/mast3r_adapter.py`
- `code/dream3r/scripts/__init__.py`
- `code/dream3r/scripts/smoke_real_e2e.py`
- `code/dream3r/pytest.ini`
- `code/dream3r/tests/test_dinov3_backbone.py`
- `code/dream3r/tests/test_kitti_pair.py`
- `code/dream3r/tests/test_mast3r_real.py`
- `code/dream3r/tests/test_smoke_real_e2e.py`

## Conclusion

Stage 1 MVR success criteria are met with one documented deviation: DINOv3-B uses a public ONNX checkpoint because the specified official HF PyTorch checkpoint is gated and unavailable. The substitution was user-approved and still uses DINOv3-B.
