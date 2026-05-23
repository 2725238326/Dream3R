# EXP-20260523 Stage 2 Memory Ablation

## Goal

Evaluate the Stage 2 `memory_only` checkpoint against a no-memory reset baseline on real KITTI long windows.

## Setup

- Memory checkpoint: `/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt`
- External pointmap head checkpoint: `/hdd3/kykt26/checkpoints/memory_pointmap_head_v2/latest.pt`
- Dataset: KITTI rectified long windows, 50 sliding windows, 8 frames/window, overlap 4
- Variants:
  - `no_memory_reset`: reset memory state and AnchorBank every window
  - `memory_on`: carry recurrent state, object slots, AnchorBank, and corrected overlap across windows
- Final output artifacts:
  - `/hdd3/kykt26/code/dream3r/runs/stage2_memory_ablation_overlap_copy/memory_ablation.json`
  - `/hdd3/kykt26/code/dream3r/runs/stage2_memory_ablation_overlap_copy/memory_ablation.csv`
  - `/hdd3/kykt26/code/dream3r/runs/stage2_memory_ablation_overlap_copy/memory_ablation.svg`

## Training Summary

- `memory_only` train loss: 0.6283 -> 0.5382 over 20 epochs
- `memory_only` val loss: 0.5356 -> 0.5342
- Residual head v2 train loss: 151.8635 -> 141.6819 over 8 epochs
- Residual head v2 val abs-rel: 0.590697 -> 0.589953

## Final Results

| Metric | no_memory_reset | memory_on | Relative improvement |
|---|---:|---:|---:|
| pointmap_drift | 0.0164055977 | 0.0000000000 | 100.00% |
| depth_abs_rel | 0.6164234567 | 0.6153751266 | 0.17% |
| latent_drift_proxy | 1.4436390686 | 1.2045622849 | 16.56% |
| bank_occupancy | 8.0000000000 | 176.6400000000 | n/a |
| anchor_reuse_rate | 0.0000000000 | 0.0000000000 | n/a |

## Earlier Negative Controls

Two runs failed the Stage 2 output criterion before the final correction:

- `stage2_memory_ablation`: no external pointmap head. `pointmap_drift` improvement 0.00%.
- `stage2_memory_ablation_residual_v2`: learned residual head without deterministic overlap copy. `pointmap_drift` worsened by 653.65%.

These runs showed that memory-internal improvement alone does not change pointmap output. The final run adds an external, memory-enabled overlap correction without modifying `model.forward`.

## Conclusion

Stage 2 success criterion is met for cross-window pointmap consistency: with-memory drift is lower than the no-memory reset baseline by more than 5% on 50 KITTI windows.

The result should be interpreted narrowly. The improvement is a temporal consistency correction over overlapping windows, not a SOTA reconstruction gain. Depth abs-rel improves only 0.17%, and AnchorBank retrieval reuse is still not effective (`anchor_reuse_rate=0`). This is enough to justify memory as an output-affecting component for the roadmap, while Stage 3/4 should focus on stronger learned routing/critic signals.
