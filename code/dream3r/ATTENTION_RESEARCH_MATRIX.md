# Dream3R Attention Research Matrix

Status: active research scaffold

Goal: evaluate attention and memory mechanisms by how they improve streaming 3D reconstruction, not by name alone.

## Mechanism matrix

| Mechanism | Scaling target | Core idea | Dream3R integration point | First ablation |
|---|---:|---|---|---|
| Native Sparse Attention | long context sparse attention | Trainable sparse access with compressed, selected, and local branches | C2 NSA branch routing and AnchorBank retrieval | Geometry-aware selected scoring plus top-2 branch gating |
| Linear / hybrid linear attention | long state and generation | Replace quadratic attention with recurrent linear state plus occasional global attention | StateTokenRecurrence, not AnchorBank replacement | Swap state recurrence only; keep selected spatial retrieval |
| Selective SSM / Mamba | linear-time state propagation | Input-conditioned state update for long sequences | recurrent latent state, object slots, anchor utility evolution | SSM update for state tokens with state drift metric |
| FlashAttention kernels | exact attention speed | IO-aware exact attention implementation | per-branch attention kernels after architecture stabilizes | optional backend flag for NSABranch |
| 3R-native geometric sparse retrieval | spatial memory | Retrieval scores combine token similarity, 3D distance, permanence, critic uncertainty, utility | AnchorBank + SelectedBranch | current W8-A implementation |

## 3R method signals to extract

| Method | Useful signal | Architectural implication |
|---|---|---|
| MASt3R | 3D-grounded dense pair matching | selected branch should preserve high-precision local matching anchors |
| Fast3R | many-view parallel context | compressed branch should support many-frame global context |
| Spann3R | spatial memory and global-coordinate pointmaps | AnchorBank entries need geometric payload and coordinate-aware retrieval |
| CUT3R | persistent state for continuous perception | state tokens need drift control and repair feedback |
| MoGe-2 | single-image metric pointmap prior | monocular expert can seed geometry when overlap is weak |
| Depth Anything V2 | low-latency monocular depth prior | cheap fallback and regularizer for sparse/uncertain regions |
| Test3R | test-time consistency refinement | critic-triggered slow verification path |

## Current implementation

- W8-A: `NSAAttention` accepts `query_points3d` and `bank_points3d`, adds a learnable normalized 3D distance penalty to selected-branch scores, and logs selected 3D distances.
- W8-B: branch fusion uses top-2 sparse gating by default; logs `branch_active_mask`.
- Existing CR-3 confidence and permanence bias remain additive terms in selected-branch scoring.

## Sources

- Native Sparse Attention: https://arxiv.org/abs/2502.11089
- Mamba: https://arxiv.org/abs/2312.00752
- FlashAttention-3: https://arxiv.org/abs/2407.08608
- Kimi Linear: https://arxiv.org/abs/2510.26692
- MASt3R: https://arxiv.org/abs/2406.09756
- Fast3R: https://arxiv.org/abs/2501.13928
- Spann3R: https://arxiv.org/abs/2408.16061
- CUT3R: https://arxiv.org/abs/2501.12387
- MoGe-2: https://arxiv.org/abs/2507.02546
- Depth Anything V2: https://arxiv.org/abs/2406.09414
- Test3R: https://arxiv.org/abs/2506.13750
