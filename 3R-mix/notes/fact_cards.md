# PDF-level fact cards for the 3R survey

Status: second-pass evidence notes after local PDF abstract/front-matter extraction.

Date: 2026-05-11.

Scope: These cards support wording in `main.typ`. They are not a full paper-by-paper reading log; benchmark numbers, training data details, code licenses, and checkpoint terms still require direct full-paper/repository checks before stronger claims.

## Evidence discipline

- Use PDF-confirmed mechanism claims for taxonomy: input regime, output representation, state/memory type, and test-time mechanism.
- Do not convert abstract-level performance phrases such as "state-of-the-art", "outperforms", "real-time", or "in seconds" into survey-level rankings unless a comparable benchmark table is read and cited.
- Treat project-page or GitHub availability separately from reproducibility, license clearance, and local quality.
- Preserve distinctions that are easy to blur: pairwise pointmap vs many-view forward pass, recurrent state vs external spatial memory, dynamic pointmap vs 4D Gaussian rendering, test-time consistency learning vs long-sequence memory update.

## Core pointmap and matching

| model | PDF-confirmed mechanism | safe survey wording | caution |
|---|---|---|---|
| DUSt3R | Casts dense unconstrained stereo 3D reconstruction as pointmap regression without prior camera calibration or poses; proposes global alignment for more than two images. | DUSt3R is the pointmap basis of the recent 3R family. | Do not imply that it solves long sequence, dynamic scenes, or all multi-view scaling alone. |
| MASt3R | Recasts image matching as a 3D task on top of DUSt3R-style pointmaps; adds dense local features, matching loss, and fast reciprocal matching. | MASt3R is a matching-enhanced branch rather than a simple replacement for DUSt3R. | Performance language needs benchmark-specific support. |
| MASt3R-SfM | Uses foundation-model local reconstructions and matches, plus low-memory global alignment and retrieval, for unconstrained SfM. | It is the strongest bridge in this corpus between learned 3D matching and classical global SfM. | It is not a lightweight per-window critic. |

## Multi-view and unified geometry

| model | PDF-confirmed mechanism | safe survey wording | caution |
|---|---|---|---|
| Fast3R | Processes many views in one Transformer forward pass and avoids iterative pairwise global alignment. | Fast3R is a many-view scaling response to pairwise DUSt3R-style cost. | The title phrase "1000+ images" is a regime claim; quality still depends on benchmark context. |
| MV-DUSt3R+ | Uses multi-view decoder blocks and cross-reference-view fusion to reconstruct sparse views in a single stage. | MV-DUSt3R+ addresses sparse multi-view and visual-output-oriented reconstruction. | The "2 seconds" phrase should not be generalized without hardware and input conditions. |
| VGGT | Predicts camera parameters, depth maps, point maps, and 3D point tracks from one/few/hundreds of views. | VGGT is a unified visual geometry model and a major comparator. | Do not write it as replacing all 3R branches; streaming/dynamic/license conditions remain separate. |
| MapAnything | Ingests images plus optional intrinsics, poses, depth, or partial reconstructions; regresses metric scene geometry and cameras through depth maps, raymaps, poses, and scale. | MapAnything represents flexible input conditioning and metric feed-forward geometry. | "Universal" must be explained as an input/supervision design, not universal reliability. |
| Pow3R | Accepts combinations of intrinsics, relative pose, dense/sparse depth, and images at test time. | Pow3R is a prior-aware DUSt3R-family extension. | Prior availability and prior correctness are separate system assumptions. |

## Streaming, state, and memory

| model | PDF-confirmed mechanism | safe survey wording | caution |
|---|---|---|---|
| CUT3R | Maintains a stateful recurrent representation and outputs metric-scale pointmaps online in a common coordinate system. | CUT3R uses persistent recurrent state for continuous 3D perception. | Do not describe the state as an external spatial database. |
| Spann3R | Manages an external spatial memory and predicts per-image pointmaps in a global coordinate system. | Spann3R is the spatial-memory counterpart to recurrent-state approaches. | It is not identical to CUT3R, Mem3R, or Point3R. |
| Point3R | Maintains explicit spatial pointer memory associated with 3D scene structure. | Point3R is an explicit pointer-memory streaming branch. | Keep pointer memory distinct from hybrid memory and cache compression. |
| LONG3R | Uses memory gating, dual-source decoder, and 3D spatio-temporal memory with pruning/resolution adaptation. | LONG3R addresses long-sequence streaming with memory filtering. | Full code and benchmark status still need direct checks. |
| LoGeR | Uses chunking plus hybrid memory: parametric TTT memory for global frame anchoring and sliding-window attention for adjacent alignment. | LoGeR is a hybrid-memory long-context method. | Do not reduce it to "more cache"; its memory components have different roles. |
| Mem3R | Decouples camera tracking and geometric mapping; uses fast-weight TTT memory for tracking and token state for mapping. | Mem3R treats long streaming as hybrid tracking/mapping memory. | Different from LoGeR hybrid memory and OVGGT cache governance. |
| OVGGT | Bounds memory and compute with Self-Selective Caching and Dynamic Anchor Protection. | OVGGT is a constant-budget cache-governance method. | "Arbitrarily long" remains a paper claim unless independently verified. |
| PAS3R | Modulates state updates according to pose variation and image frequency cues. | PAS3R is pose-adaptive state update. | Do not mix it with generic memory expansion. |
| FILT3R | Adds a training-free Kalman-style latent filtering layer with per-token variance and adaptive gain. | FILT3R is latent filtering for recurrent state updates. | It is not classical SLAM graph filtering. |
| LongStream | Uses gauge-decoupled keyframe-relative poses, orthogonal scale learning, and cache refresh for long online sequences. | LongStream is a gauge/cache reformulation for long streaming geometry. | Keep it separate from STream3R's causal decoder framing. |

## Dynamic scenes and 4D

| model | PDF-confirmed mechanism | safe survey wording | caution |
|---|---|---|---|
| MonST3R | Fine-tunes DUSt3R-style pointmaps for dynamic scenes and estimates per-timestep geometry. | MonST3R adapts pointmap geometry to scenes with motion. | It does not by itself provide long-term object identity memory. |
| POMATO | Combines pointmap matching with temporal motion to improve dynamic reconstruction. | POMATO is a dynamic reconstruction method centered on 3D matching and motion. | Do not collapse it into D^2USt3R; their representations differ. |
| D^2USt3R | Regresses static-dynamic aligned pointmaps for dynamic scenes. | D^2USt3R is a dynamic pointmap branch. | 4D pointmaps are not 4D Gaussian assets. |
| Easi3R | Uses inference-time attention adaptation without model fine-tuning for dynamic segmentation, camera pose, and 4D dense point maps. | Easi3R is a training-free dynamic adaptation route. | It should not be written as a trained dynamic foundation model. |
| RayMap3R | Uses RayMap/image dual branch contrast to identify dynamic regions and suppress their memory-update interference. | RayMap3R is a training-free dynamic streaming framework. | Code maturity and application reliability need direct verification. |

## Test-time and output representation

| model | PDF-confirmed mechanism | safe survey wording | caution |
|---|---|---|---|
| Test3R | Performs test-time prompt tuning from image triplets by maximizing cross-pair geometric consistency. | Test3R is test-time consistency learning, not merely passive scoring. | Distinguish it from TTT3R's long-sequence memory update. |
| TTT3R | Frames recurrent 3D reconstruction as online test-time training and derives a memory update rate from alignment confidence. | TTT3R is a long-context recurrent-memory update method. | Report the 20 FPS / 6 GB / 2x claims only as paper claims unless independently verified. |
| G-CUT3R | Adds modality-specific prior encoders for depth, calibration, or camera positions to guide CUT3R. | G-CUT3R is guided feed-forward reconstruction with priors. | Prior conflict detection is a system-level extension, not necessarily a paper contribution. |
| Splatt3R | Extends MASt3R-style geometry to Gaussian attributes for uncalibrated image pairs. | Splatt3R bridges pose-free 3R and Gaussian output. | License/dependency status must be checked before application claims. |
| InstantSplat | Uses dense stereo priors, co-visibility, and Gaussian Bundle Adjustment for sparse views. | InstantSplat is a sparse-view Gaussian pipeline, not pure one-pass pointmap prediction. | The "seconds" claim needs hardware/input context. |
| NoPoSplat | Predicts 3D Gaussians from sparse unposed images in a canonical input-view coordinate frame. | NoPoSplat is feed-forward unposed sparse-view Gaussian reconstruction. | Keep photometric-loss/NVS framing distinct from geometric pointmap metrics. |
