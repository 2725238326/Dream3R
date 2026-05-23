# CYCLE 20260523 Stage 2 — Memory Module Real Training

## Scope

Close Stage 2 by replacing the memory-only scaffold with a real KITTI long-window training and ablation loop.

## Changes

- Added `KITTILongSequenceDataset` with 8-frame windows, overlap 4, OXTS pose loading, and fallback pose support.
- Added Stage 2 memory loss terms:
  - memory consistency
  - cross-window pointmap consistency
  - anchor reuse
- Added `memory_only` training preset and train-mode freeze so only `memory.*` parameters train.
- Ran 20 epoch memory-only training on KITTI long windows and saved `/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt`.
- Added external `MemoryPointmapResidualHead` and training script.
- Added `eval_memory_ablation.py` for 50-window memory-on vs no-memory reset comparison.

## Verification

- T2.1 server smoke: 10 KITTI long-window batches, `features=(2,4,8,196,768)`, OXTS poses loaded.
- T2.2 focused tests passed locally and on server.
- T2.3 training completed:
  - train loss: 0.6283 -> 0.5382
  - val loss: 0.5356 -> 0.5342
  - checkpoint: `/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt`
- T2.4 final ablation:
  - `pointmap_drift`: 0.0164055977 -> 0.0
  - `depth_abs_rel`: 0.6164234567 -> 0.6153751266
  - `latent_drift_proxy`: 1.4436390686 -> 1.2045622849
- Full test suites:
  - local: `212 passed, 1 skipped`
  - server: `210 passed, 1 skipped`

## Limitations

The final drift improvement is from an external overlap-copy memory correction, not a core `model.forward` memory-conditioned pointmap head. This avoids changing the closed core model path but keeps the result narrow: Stage 2 proves cross-window consistency can be improved by memory, not that base reconstruction accuracy is substantially better.
