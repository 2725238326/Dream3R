# Dream3R Research Literature and Project Map

Status: initial collected baseline for first-generation research.

Date: 2026-05-10

## Purpose

This document defines the research base Dream3R should accumulate around. It is organized by Dream3R module, not by publication date, because the goal is to support our architecture decisions and future paper framing.

Dream3R's working thesis:

> A control-graph architecture for streaming 3R that integrates foundation visual features, sparse long-context memory, active/stable spatial state, geometric self-critique, expert routing, object permanence, Mamba-style recurrence, and future 3DGS output.

## Reading Priority

### Tier 0: Must Read Before Any Paper/Presentation Claim

| Area | Paper / Project | Why It Matters For Dream3R |
|---|---|---|
| Pointmap 3R foundation | DUSt3R: Geometric 3D Vision Made Easy | Establishes pointmap regression as a unified camera-free 3D reconstruction paradigm. |
| Matching + 3R expert | MASt3R: Grounding Image Matching in 3D | Direct basis for our MASt3R expert adapter and matching-aware reconstruction story. |
| Unified geometry transformer | VGGT: Visual Geometry Grounded Transformer | Strongest high-level baseline for feed-forward geometry: camera, depth, pointmap, tracks. |
| Streaming state | CUT3R: Continuous 3D Perception Model with Persistent State | Basis for Dream3R active state recurrence and online pointmap accumulation. |
| Spatial memory | Spann3R: 3D Reconstruction with Spatial Memory | Direct precedent for reconstruction with external spatial memory. |
| Explicit spatial memory | Point3R: Streaming 3D Reconstruction with Explicit Spatial Pointer Memory | Closest conceptual neighbor to Dream3R AnchorBank and 3D-aware retrieval. |
| Long sequence memory | LONG3R: Long Sequence Streaming 3D Reconstruction | Important comparison for long-horizon memory gating and pruning. |
| Hybrid memory | Mem3R: Streaming 3D Reconstruction with Hybrid Memory via Test-Time Training | Recent 2026 direction; useful for active/stable memory and test-time adaptation framing. |
| Sparse long context | Native Sparse Attention | Basis for Dream3R compressed/selected/sliding NSA memory fusion. |
| Mamba recurrence | Mamba: Linear-Time Sequence Modeling with Selective State Spaces | Basis for W17 state-space recurrence path. |
| Object slots | Object-Centric Learning with Slot Attention | Basis for Permanence slot tracking. |
| Slot reference frames | Invariant Slot Attention | Basis for ISA-style slot-centric reference frames. |
| Visual foundation | DINOv2 | Basis for frozen backbone / robust visual features. |
| 3DGS output | 3D Gaussian Splatting | Basis for future renderable output representation. |
| Anchor-aligned 3DGS | AnchorSplat | Directly supports our GaussianHead + AnchorBank future direction. |

## Architecture-to-Literature Mapping

### C1 Perceiver and Visual Backbone

Core references:

- DINOv2: self-supervised visual features that transfer across image and pixel-level tasks.
- VGGT: geometry-aware transformer that predicts multiple 3D attributes in one feed-forward pass.
- DUSt3R / MASt3R: pointmap regression and dense matching as 3R primitives.

Dream3R implication:

- Use frozen or fallback foundation visual features for stable evidence extraction.
- Keep evidence heads trainable; backbone can be frozen or replaced.
- Do not frame Perceiver as merely a ViT encoder; frame it as evidence extraction for the control graph.

Code status:

- `Perceiver` supports backbone configuration and fallback.
- DINOv2 route is implemented as a configurable path with tests.

Open work:

- Compare DINOv2 vs VGGT/MASt3R features as Perceiver backbone.
- Add feature-quality diagnostics: patch correspondence, geometric consistency, retrieval quality.

### C2 SpatialMemory, AnchorBank, and Active/Stable State

Core references:

- CUT3R: persistent state tokens for online 3D perception.
- Spann3R: external spatial memory for reconstruction in a global coordinate frame.
- Point3R: explicit spatial pointer memory with 3D position embedding.
- LONG3R: long-sequence streaming memory with relevance filtering/pruning.
- Mem3R: hybrid memory that decouples tracking and mapping.

Dream3R implication:

- Active state should handle immediate recurrent updates.
- Stable state should be an explicit spatial memory, not just hidden tokens.
- Memory retrieval must be 3D-aware and bounded.
- Long-sequence performance should be evaluated by retention, drift, and retrieval quality.

Code status:

- `StateTokenRecurrence` is active state.
- `AnchorBank` is stable state.
- Active-to-stable promote and stable recall are implemented.
- AnchorBank stores spatial payload and supports 3D-aware retrieval.

Open work:

- Real sequence evaluation for memory drift.
- Ablation: active-only vs stable-only vs active+stable.
- Compare Dream3R AnchorBank against Point3R pointer memory and LONG3R pruning.

### C2 W17 Mamba-Hybrid Recurrence

Core references:

- Mamba: selective state-space model for linear-time sequence modeling.
- NSA: long-context sparse attention; Mamba complements rather than replaces it.
- CUT3R / LONG3R: streaming state recurrence baselines in 3R.

Dream3R implication:

- Mamba-style recurrence is a candidate for long-horizon active state evolution.
- NSA still handles memory fusion; Mamba evolves the active state tokens.
- The important comparison is not "Mamba vs Transformer globally", but "Mamba active recurrence + NSA memory fusion vs cross-attention recurrence + NSA memory fusion."

Code status:

- `state_recurrence_type="mamba_hybrid"` is implemented.
- Server uses `mamba_ssm.Mamba(use_fast_path=False)`.
- PyTorch selective-scan fallback exists.
- `demo_mamba_path` compares cross-attention and Mamba-hybrid paths.

Open work:

- Ablation on synthetic streaming convergence.
- Real sequence timing and quality comparison.
- Investigate `causal_conv1d` ABI mismatch before enabling Mamba fast path.

### C3 Permanence and Object Slots

Core references:

- Slot Attention: object-centric representation via iterative attention.
- Invariant Slot Attention: slot-centric reference frames for spatial symmetries.
- Dynamic 3R lines such as D^2USt3R are relevant because moving objects break pure camera-pose alignment.

Dream3R implication:

- Object permanence should not be a binary mask only.
- Slots need identity, dynamic/static status, and frame-local reference pose.
- Slot pose should assist cross-window matching when appearance/features are ambiguous.

Code status:

- `Permanence` outputs `object_track_set`, `dynamic_ratio`, `suppress_static_write`, and `object_slot_poses`.
- Multi-window ISA stress tests exist.
- Pose-aware matching is tested against feature-only matching.

Open work:

- Learn real slot rotations rather than identity quaternions.
- Evaluate dynamic scenes and object-level consistency.

### C4 Critic and Geometric Self-Verification

Core references:

- Classical epipolar geometry and Sampson distance.
- Test3R: test-time learning / consistency for 3D reconstruction.
- DUSt3R / MASt3R / VGGT: pointmap and correspondence outputs make geometric checks cheap to define.

Dream3R implication:

- Critic should consume geometry, not just learned evidence tokens.
- Repair actions should be tied to downstream behavior: retrieval, reroute, suppress, verify.
- Calibration matters because conflict scores can be high under synthetic/random pointmaps.

Code status:

- Critic computes Sampson-like, depth, covisibility, and confidence disagreement signals.
- `critic_geometric_log` is exposed and evaluated.
- Repair actions 0/1/2 are consumed by downstream logic.

Open work:

- Calibrate conflict thresholds on real data.
- Add Test3R-style off-path verification or test-time consistency only when compute budget allows.

### C5 ComposerRouter and Expert 3R Adapters

Core references:

- DUSt3R / MASt3R / Fast3R / Spann3R / CUT3R / VGGT family.
- Fast3R: all-to-all multi-view feed-forward scaling.
- Test3R: verification/optimization at test time.

Dream3R implication:

- We should not clone every 3R method internally.
- Use strong methods as experts with capability cards, latency cost, and Critic feedback.
- Research question: when should Dream3R route to which expert?

Code status:

- Composer expert registry exists.
- MASt3R and Spann3R real paths are integrated.
- Fast3R contract/fallback exists; dependency cleanup remains.

Open work:

- Real expert output quality table.
- Routing ablation: capability-only vs cost-aware vs Critic-aware.

### C6 MemoryBus and Control-Graph Framing

Core references:

- There is no exact direct baseline for this in 3R; this is one of Dream3R's architectural claims.
- Related conceptual neighbors: modular perception systems, blackboard architectures, critic-controller loops.

Dream3R implication:

- Bus signals are the backbone of the "control-graph" claim.
- Every cross-module influence should be explicit, logged, and testable.

Code status:

- MemoryBus has typed publish/read/handoff and CR gates.
- Smoke test logs consumers and signals.

Open work:

- Turn contract log into a visualization for presentation/paper.
- Add ablation disabling CR gates.

### W18 GaussianHead and 3DGS Output

Core references:

- 3D Gaussian Splatting: real-time radiance field rendering with anisotropic Gaussians.
- AnchorSplat: feed-forward 3DGS with 3D geometric priors and anchor-aligned Gaussian representation.

Dream3R implication:

- Gaussian output should be anchor-aligned, not merely pixel-aligned.
- AnchorBank entries are natural persistent Gaussian candidates.
- Renderer work is separate from tensor contract work.

Code status:

- `GaussianHead` outputs means, scales, rotations, colors, opacity, and source anchor ids.
- Contract tests pass.

Open work:

- Wire GaussianHead into model output only after renderer path is approved.
- Add `gsplat` or another backend only with explicit approval.
- Add photometric losses only when rendering is real, not stubbed.

## Project/Code Repositories To Track

| Project | Link | Track For |
|---|---|---|
| DUSt3R | https://github.com/naver/dust3r | Pointmap paradigm, global alignment, datasets/eval. |
| MASt3R | https://github.com/naver/mast3r | Matching + reconstruction expert integration. |
| VGGT | https://github.com/facebookresearch/vggt | Unified geometry prediction and possible backbone/expert. |
| CUT3R | https://cut3r.github.io/ | Persistent state streaming baseline. |
| Spann3R | https://hengyiwang.github.io/projects/spanner | Spatial memory baseline. |
| Point3R | https://github.com/YkiWu/Point3R | Explicit spatial pointer memory. |
| LONG3R | https://zgchen33.github.io/LONG3R/ | Long-sequence memory and pruning. |
| Mamba | https://github.com/state-spaces/mamba | State-space recurrence backend. |
| 3D Gaussian Splatting | https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/ | Renderer/output representation. |

## Paper-Framing Claims We Can Make Now

Safe claims:

- Dream3R implements a modular control-graph 3R prototype.
- It integrates active recurrent state and stable spatial memory.
- It uses NSA-style compressed/selected/sliding memory fusion.
- It exposes geometric Critic signals and repair actions.
- It supports both cross-attention and Mamba-style active state recurrence.
- It defines a future 3DGS tensor contract.

Claims not yet safe:

- Dream3R outperforms SOTA.
- Mamba-hybrid improves quality over cross-attention.
- AnchorBank beats Point3R/LONG3R memory.
- GaussianHead produces renderable high-quality 3DGS scenes.
- Expert routing improves reconstruction quality on real datasets.

## Immediate Research Tasks

### Tonight Completed

- Initial literature/project map collected.
- Module-to-literature mapping written.
- Safe vs unsafe paper claims separated.
- Next-phase reading and ablation priorities defined.

### Next 48 Hours

1. Build a one-page related-work table for presentation.
2. Add a bibliography block in BibTeX style for Tier 0 papers.
3. Create an ablation plan document:
   - Cross-attention vs Mamba-hybrid.
   - NSA on/off.
   - Active-only vs stable-only vs active+stable.
   - Critic off vs Critic repair actions.
   - Expert router off vs cost-aware vs Critic-aware.
4. Decide the first real dataset/eval route.

## Sources

- DUSt3R: https://arxiv.org/abs/2312.14132
- MASt3R: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/09080.pdf
- MASt3R project: https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/
- Fast3R: https://arxiv.org/abs/2501.13928
- Spann3R: https://arxiv.org/abs/2408.16061
- VGGT: https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.html
- CUT3R: https://arxiv.org/abs/2501.12387
- Point3R: https://arxiv.org/abs/2507.02863
- LONG3R: https://arxiv.org/abs/2507.18255
- Mem3R: https://arxiv.org/abs/2604.07279
- Native Sparse Attention: https://arxiv.org/abs/2502.11089
- Mamba: https://arxiv.org/abs/2312.00752
- DINOv2: https://arxiv.org/abs/2304.07193
- Slot Attention: https://arxiv.org/abs/2006.15055
- Invariant Slot Attention: https://huggingface.co/papers/2302.04973
- 3D Gaussian Splatting: https://arxiv.org/abs/2308.04079
- AnchorSplat: https://arxiv.org/abs/2604.07053
