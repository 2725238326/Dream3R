# Frontier Source Map

Last updated: 2026-05-05 (cycle 013 source mining pass appended at end: 8 newly mined sources covering Mem3R / MapAnything / Julian Ost AAAI-2026 driving permanence / tttLRM CVPR-2026 / awesome-dust3r curated index / DUSt3R-MASt3R-VGGT MVS evaluation / NTIRE 2026 challenge / VGGT comparator)

This is the first-pass source map for Dream Phase 1. It prioritizes primary sources: arXiv, CVF/OpenReview, official project pages, and official GitHub repositories.

Evidence labels:

- `paper`: paper exists
- `code`: official or credible code exists
- `demo`: project/demo page or runnable demo exists
- `speculation`: Dream inference, not proven by source

## Early Thesis Signal

The direct 3R frontier after DUSt3R is no longer only "better pointmaps." It is increasingly about:

```text
how to update, store, compress, query, and correct spatial state over time.
```

This supports Dream's architecture-first framing.

## Direct 3R / Pointmap Family

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [DUSt3R](https://arxiv.org/abs/2312.14132) | 2023/2024 | direct_3r | Pose-free dense pointmap regression; global alignment for multi-view | paper, project/code known | Base paradigm; all follow-up ideas inherit pointmap output contract |
| [MASt3R](https://arxiv.org/abs/2406.09756) | 2024 | direct_3r | Adds 3D-grounded dense local features and fast reciprocal matching to DUSt3R | paper, code known | Strong static matching baseline; useful for composer lane |
| [MonST3R](https://arxiv.org/abs/2410.03825) | 2024/2025 | direct_3r | Extends pointmap estimation to dynamic video via per-timestep geometry fine-tuning | paper, project/code known | Dynamic geometry baseline already relevant to KYKT |
| [Spann3R](https://arxiv.org/abs/2408.16061) / [GitHub](https://github.com/HengyiWang/spann3r) | 2024/2025 | direct_3r | Spatial memory for global pointmap prediction without optimization-heavy alignment | paper, code | First memory-flavored 3R baseline in KYKT route |
| [Fast3R](https://arxiv.org/abs/2501.13928) | 2025 | direct_3r | Processes many images in one forward pass; avoids pairwise/global alignment bottleneck | paper, CVPR/code known | Speed/scaling baseline; good for composer and app demo |
| [MV-DUSt3R+](https://github.com/facebookresearch/mvdust3r) | 2025 | direct_3r | Sparse-view pose-free RGB-only reconstruction; supports NVS and relative pose estimation | code, Gradio, checkpoints | Good direct multi-view demo candidate; Linux/CUDA 12.4 path noted |
| [CUT3R](https://cut3r.github.io/) / [GitHub](https://github.com/CUT3R/CUT3R) | 2025 | direct_3r | Continuous updating transformer with persistent state for online pointmaps | paper, code, demo | Key stateful baseline; current KYKT env blocked but high conceptual value |
| [STream3R](https://arxiv.org/abs/2508.10893) / [GitHub](https://github.com/NIRVANALAN/STream3R) | 2025/2026 | direct_3r | Decoder-only / causal Transformer framing for sequential 3D reconstruction | paper, code, demo | Important comparator for any Mamba/linear-state claim |
| [Test3R](https://arxiv.org/abs/2506.13750) / [GitHub](https://github.com/nopQAQ/Test3R) | 2025 | architecture_transfer | Test-time geometric consistency objective over image triplets | paper, code | Best near-term path for "System-2 geometry self-check" demo |
| [TTT3R](https://arxiv.org/abs/2509.26645) | 2025/2026 | architecture_transfer | Frames streaming 3R as test-time training; confidence-derived memory update rate | paper, code page claimed | Strong bridge between memory and test-time adaptation |
| [LONG3R](https://arxiv.org/abs/2507.18255) | 2025 | direct_3r | Recurrent long-sequence 3R with memory gating and 3D spatio-temporal memory | paper, project page | Direct evidence that long-sequence memory is central |
| [Point3R](https://arxiv.org/abs/2507.02863) | 2025 | direct_3r | Explicit spatial pointer memory for streaming dense reconstruction | paper | Important for external geometric memory designs |
| [PAS3R](https://arxiv.org/abs/2603.21436) | 2026 | direct_3r | Pose-adaptive state update for long monocular streams | paper | Very close to Dream's proposed geometry-gated state update |
| [LoGeR](https://loger-project.github.io/) | 2026 | direct_3r | Hybrid memory for long-context geometric reconstruction | project page, paper link | Reinforces "context wall + data wall" framing |
| [Mem3R](https://lck666666.github.io/Mem3R/) | 2026 | direct_3r | Hybrid memory decoupling camera tracking and geometric mapping | project page | Relevant comparator for Dream memory designs |
| [RayMap3R](https://raymap3r.github.io/) | 2026 | direct_3r | Inference-time RayMap for dynamic streaming reconstruction | project page, code claimed | Useful for dynamic-memory and ray-based state ideas |
| [POMATO](https://arxiv.org/abs/2504.05692) | 2025 | direct_3r | Combines pointmap matching with temporal motion for dynamic 3D reconstruction | paper, code location claimed | Dynamic branch comparator; proves motion should be represented, not hidden in static alignment |
| [D^2USt3R](https://arxiv.org/abs/2504.06264) | 2025 | direct_3r | Regresses 4D pointmaps for dynamic scenes | paper | Strong evidence for pointmap-to-4D representation shift |

## Architecture Mechanisms

| Source | Year | Tag | Mechanism | Evidence | 3R translation |
|---|---:|---|---|---|---|
| [Mamba](https://arxiv.org/abs/2312.00752) | 2023/2024 | architecture_transfer | Selective state spaces; input-dependent propagation/forgetting; linear scaling | paper, code known | Replace temporal attention with geometry-gated state update |
| [Mamba-2 / SSD](https://arxiv.org/abs/2405.21060) / [GitHub](https://github.com/state-spaces/mamba) | 2024 | architecture_transfer | State Space Duality; SSM layer closer to efficient attention with faster implementation | paper, code | Candidate state layer for 3R temporal memory; compare to causal attention |
| [Vision Mamba / Vim](https://arxiv.org/abs/2401.09417) | 2024 | architecture_transfer | Bidirectional Mamba visual backbone with memory/compute efficiency | paper, code | Candidate feature backbone for high-res 3R inputs |
| [VMamba](https://arxiv.org/abs/2401.10166) | 2024 | architecture_transfer | 2D selective scan over multiple routes for vision | paper, code | Spatial scan design for image/pointmap tokens |
| [QuadMamba](https://arxiv.org/abs/2410.06806) | 2024 | architecture_transfer | Quadtree-adaptive visual scan | paper, code claimed | Route policy for adaptive image/pointmap token ordering |
| [GroupMamba](https://arxiv.org/abs/2407.13772) | 2024 | architecture_transfer | Channel-grouped selective scan with modulation | paper, code claimed | Split 3R state into geometry / appearance / motion groups |
| [EfficientViM](https://arxiv.org/abs/2411.15241) | 2024/2025 | architecture_transfer | Hidden-state mixer and multi-stage hidden-state fusion | paper, code claimed | Suggests state fusion should happen inside hidden state, not only across tokens |
| [MLLA / MILA](https://arxiv.org/abs/2405.16605) | 2024 | architecture_transfer | Linear attention interpreted through Mamba-like gates | paper, code claimed | Alternative cheap global mixing layer for long-view 3R |
| [Infini-attention](https://arxiv.org/abs/2404.07143) | 2024 | architecture_transfer | Local attention plus compressive long-term memory in one block | paper | Useful abstraction for chunked 3R: local alignment plus compressed global state |
| [Point Cloud Mamba](https://arxiv.org/abs/2403.00762) | 2024 | architecture_transfer | Serializes point clouds while preserving neighborhood adjacency | paper | External map memory can be scanned as spatial sequence |
| [MambaVision](https://arxiv.org/abs/2407.08083) / [GitHub](https://github.com/NVlabs/MambaVision) | 2024/2025 | architecture_transfer | Hybrid Mamba-Transformer vision backbone | paper, code | Hybrid design suggests not replacing all attention blindly |
| [MambaOut](https://arxiv.org/abs/2405.07992) / [GitHub](https://github.com/yuweihao/MambaOut) | 2024/2025 | negative_control | Removes SSM token mixer and shows SSM is not always needed for vision classification | paper, code | Forces Dream to justify SSM only for long-sequence / streaming / autoregressive geometry |
| [Kimi Linear](https://arxiv.org/abs/2510.26692) | 2025 | architecture_transfer | Kimi Delta Attention; fine-grained finite-state memory gating; hybrid full/linear attention | paper, code/checkpoints claimed | Alternative to Mamba for long-sequence 3R state update |
| [RAM-Net](https://arxiv.org/abs/2602.11958) | 2026 | architecture_transfer | Selectively addressable memory for linear attention | paper | Conceptual support for "fixed state + random-access sparse map" |
| [Adaptive Graph of Thoughts](https://arxiv.org/abs/2502.05078) | 2025 | background | Adaptive test-time reasoning graph | paper | Inspires adaptive geometry hypothesis expansion, but not directly 3R |
| [CTRL](https://arxiv.org/abs/2502.03492) / [GitHub](https://github.com/HKUNLP/critic-rl) | 2025 | architecture_transfer | Reinforcement-trained critic improves iterative critique-revision at test time | paper, code | Blueprint for a geometry critic that spends compute only on inconsistent regions |
| [SEAL](https://arxiv.org/abs/2506.10943) / [GitHub](https://github.com/Continual-Intelligence/SEAL) | 2025 | architecture_transfer | Model generates self-edits / update directives for adaptation | paper, code | Blueprint for controlled adapter updates in 3R under new scene/device distributions |

## Dynamic / 4D / Sensor / Demo Enablers

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [4D Gaussian Splatting for Real-Time Dynamic Scene Rendering](https://openaccess.thecvf.com/content/CVPR2024/html/Wu_4D_Gaussian_Splatting_for_Real-Time_Dynamic_Scene_Rendering_CVPR_2024_paper.html) | 2024 | demo_enabler | Dynamic scene rendering with 4D representation / deformation | paper, code/project | Strong teacher-facing visualization layer |
| [4D Gaussian Splatting: Towards Efficient Novel View Synthesis](https://huggingface.co/papers/2402.03307) | 2024 | demo_enabler | Anisotropic 4D XYZT Gaussians for dynamic scenes | paper, code | Another 4DGS path; verify repo maturity before use |
| [4DGS in the Wild](https://arxiv.org/abs/2411.08879) | 2024 | demo_enabler | Monocular casual video 4DGS with uncertainty regularization; notes SfM initialization failure | paper | Directly motivates 3R-as-initializer |
| [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting) | 2023 | demo_enabler | Real-time 3D Gaussian representation and viewer ecosystem | code, paper known | Base viewer/rendering layer for KYKT output demos |
| [InstantSplat](https://github.com/NVlabs/InstantSplat) | 2024 | demo_enabler | Sparse-view SfM-free Gaussian Splatting; supports 3DGS/2DGS/Mip-Splatting path | code, Docker/conda path | Strong visual demo, but heavier dependency stack |
| [Splatt3R](https://github.com/btsmart/splatt3r) | 2024 | demo_enabler | Feed-forward model predicting 3D Gaussians from uncalibrated image pairs | code, Gradio, checkpoint, noncommercial license | Strongest quick visual demo candidate if license is acceptable for class/research |
| [NoPoSplat](https://github.com/cvg/NoPoSplat) | 2025 | demo_enabler | Sparse unposed images to canonical 3D Gaussians, NVS and pose estimation | code, MIT, checkpoints | Good pose-free GS comparator; training is heavy but inference may be viable |
| [GS-CPR](https://github.com/XRIM-Lab/GS-CPR) | 2025 | demo_enabler | Gaussian Splatting camera pose refinement using MASt3R/SfM-style initialization | code | Bridge module for 3R-to-GS refinement |
| [MoSca](https://huggingface.co/papers/2405.17421) | 2024 | demo_enabler | Dynamic Gaussian fusion with motion scaffolds | paper, code | Good comparison for dynamic 4D asset demo |
| [SplineGS](https://huggingface.co/papers/2412.09982) | 2024 | demo_enabler | COLMAP-free monocular dynamic Gaussian reconstruction with splines | paper | Good lower-cost 4D demo candidate if code is available |
| [Hybrid 3D-4DGS](https://github.com/ohsngjun/3D-4DGS) | 2025 | demo_enabler | Static 3D + dynamic 4D Gaussian split | code claimed | Good explanatory dynamic-scene route, but heavier |
| [Instant4D](https://github.com/Zhanpeng1202/Instant4D) | 2025 | demo_enabler | Minute-scale 4D reconstruction stack with external modules | code claimed | Visually attractive but heavy engineering stack |
| [EAG3R](https://arxiv.org/abs/2512.00771) | 2025/2026 | architecture_transfer | Event-augmented pointmap geometry using MonST3R backbone and event/RGB fusion | paper | Confirms Event-DUSt3R idea is already emerging; use as reference not duplicate |
| [Interp3R](https://gist.science/paper/2603.14528) | 2026 | demo_enabler | Continuous-time pointmap interpolation using frames + events | secondary source currently | Needs primary arXiv verification; promising for continuous-time story |
| [Event-3DGS](https://github.com/lanpokn/Event-3DGS) | 2024 | demo_enabler | Event-camera Gaussian Splatting pipeline | code | Research branch; hardware/data/pose preprocessing likely heavy |
| [Next Best Sense](https://github.com/armlabstanford/NextBestSense) | 2025 | demo_enabler | Active sensing / next-best-view system with robot stack | code/docker claimed | Conceptually relevant, but too hardware-heavy for first demo |

## Comparator Completion Pass 2026-05-02

This pass records the comparator groups that must be carried into branch scoring and mechanism intake.

| Comparator group | Sources / models | Primary failure modes | Dream use |
|---|---|---|---|
| Base pointmap / matching | DUSt3R, MASt3R, MASt3R-SfM | F3, F6 | baseline contracts for pointmap, matching, and alignment |
| Many-view / sparse-view scale | Fast3R, MV-DUSt3R+ | F6, F3 | composer inputs and sparse/multiview capability cards |
| Spatial memory / global pointmap | Spann3R, Point3R | F1, F6 | required comparators for any external-memory or global-pointmap claim |
| Stateful / streaming 3R | CUT3R, STream3R, LONG3R | F1 | direct stateful baselines |
| Memory / cache frontier | LoGeR, Mem3R, PAS3R, FILT3R, LongStream, OVGGT | F1, F3 | strongest pressure against generic memory claims |
| Dynamic / 4D 3R | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R | F2, F3 | dynamic branch comparators; object permanence must go beyond motion estimation |
| Critic / test-time reasoning | Test3R, TTT3R, CTRL-style critic-revision | F3, F1 | geometry critic and revision-action comparators |
| Visual asset / Gaussian output | Splatt3R, InstantSplat, NoPoSplat, 4DGS variants | F6, F2, demo | teacher-visible evidence surface, not automatically thesis novelty |
| Guided / cross-modal | EAG3R, Event-3DGS, G-CUT3R, guided-prior methods | F5, F2, F3 | event/guided robustness branch and prior-conflict policy |
| Active perception | NBV, active perception, NextBestSense-style systems | F4, F3 | keep as design/simulation-first future branch |

New active intake artifact:

```text
planning/ARCHITECTURE_MECHANISM_INTAKE.md
```

Use it to translate sparse attention, linear attention, SSM/Mamba, attention residuals, RL, continual learning, new visual features, segmentation/tracking/flow/VOS, Gaussian/4D, event, depth, IMU, LiDAR, and guided-prior mechanisms into:

```text
Failure mode -> Mechanism -> Action -> Proxy metric -> Comparator -> Evidence level
```

## Initial Gaps

1. Need official GitHub/code status verification for 2026 sources: LoGeR, Mem3R, RayMap3R, PAS3R, Interp3R.
2. Need licensing and checkpoint availability for any repo before recommending reproduction.
3. Need KYKT sample compatibility check: image-only, video, dynamic video, long sequence, or special sensor input.
4. Need separate "paper result vs Dream hypothesis" labels for every derived idea.
5. Need direct paper verification for Splatt3R / InstantSplat / MV-DUSt3R+ / NoPoSplat before citing in formal proposal.

## Subagent-Derived Mechanism Vocabulary

Use this vocabulary when converting papers into Dream units:

| Mechanism | 3R meaning | Reject if |
|---|---|---|
| route scan | token/order policy for images, frames, pointmaps, pointers, or voxels | it is only "use Mamba" without route choice |
| persistent state | bounded hidden carrier across frames/chunks | no write/reset/evict policy is specified |
| external spatial memory | explicit growing map indexed by geometry | claimed as O(1) total memory |
| global-local hybrid | local geometry alignment plus sparse/global correction | full attention is still used everywhere |
| critic-revision | detect inconsistency, then locally revise output | it only reruns the same model without a critic |
| self-adapt update | constrained adapter/state update at test time | it is offline fine-tuning renamed as online adaptation |

## Cycle 003 Research-Content Update

New direct comparator signal:

| Source | Year | Mechanism | Dream implication |
|---|---:|---|---|
| [LoGeR](https://arxiv.org/abs/2603.03269) | 2026 | Chunked long-context reconstruction with hybrid memory: TTT global memory and sliding-window local memory | Dream must not claim generic hybrid memory as new; novelty must be executive policy over memory actions |
| [Mem3R](https://arxiv.org/abs/2604.07279) | 2026 | Decouples camera tracking from geometric mapping; uses TTT fast-weight memory and explicit fixed-size state | Tracking/mapping memory split should become a baseline assumption |
| [PAS3R](https://arxiv.org/abs/2603.21436) | 2026 | Pose-adaptive state update based on camera motion and scene structure | Geometry-gated update is already a direct competitor; Dream needs richer evidence and action space |
| [FILT3R](https://arxiv.org/abs/2603.18493) | 2026 | Training-free Kalman-style latent filtering with uncertainty and adaptive gain | Strong theoretical prior for belief-state 3R update |
| [LongStream](https://arxiv.org/abs/2602.13172) | 2026 | Gauge-decoupled streaming visual geometry, keyframe-relative poses, cache-consistent training and refresh | Coordinate-frame anchoring and cache contamination must be explicit failure modes |
| [OVGGT](https://arxiv.org/abs/2603.05959) | 2026 | O(1) constant-cost cache compression and dynamic anchor protection | Constant VRAM is no longer enough as novelty; Dream must govern what is protected and why |
| [MASt3R-SfM](https://arxiv.org/abs/2409.19152) | 2024/2025 | MASt3R matching, retrieval, and global SfM alignment | Matching/SfM integration is a comparator, not a thesis |
| [SLAM3R](https://arxiv.org/abs/2412.09401) | 2024/2025 | Sliding-window dense SLAM from pointmap predictions plus global registration | Real-time dense SLAM is already occupied; Dream should target long-term memory governance |
| [Easi3R](https://arxiv.org/abs/2503.24391) | 2025 | Training-free dynamic adaptation for 4D reconstruction | Dynamic training-free correction is occupied; Dream needs object permanence or controller-level action selection |
| [G-CUT3R](https://arxiv.org/abs/2508.11379) | 2025 | Guided CUT3R with depth / pose / calibration priors | Guidance is a useful branch, not enough as a thesis |

Updated thesis pressure:

```text
Dream3R should be reframed away from a single state update mechanism.
The stronger candidate is an executive-memory policy that arbitrates between latent update,
external memory, cache/anchor protection, geometry critic, dynamic branch, and adapter update.
```

New artifact:

```text
planning/DREAM3R_THESIS_STRESS_TEST.md
```

Subagent boundary update:

```text
Stable empty spaces are likely explicit memory control,
cross-session revisitable scene memory,
dynamic object permanence,
and a unified executive contract across reconstruction / matching / localization / SLAM.
```

## Cycle 005 Source Mining Pass (2026-05-02)

Goal: fill weak comparator coverage for branches beyond direct 3R: visual priors, metric-depth priors, active perception / NBV on NeRF/3DGS, and event-camera visual odometry.

All arXiv IDs in this section were verified by web search in CYCLE-20260502-005. Code / license / checkpoint / demo verification is still pending per the Initial Gaps rule above.

### Visual Priors (semantic, tracking, foundation features)

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [DINOv2](https://arxiv.org/abs/2304.07193) | 2023 | architecture_transfer | Self-supervised all-purpose visual features trained at scale; strong without finetuning | paper, code, checkpoints | Feature / semantic prior for A6 split_dynamic_static and A7 add_sensor_prior; supports dynamic branch and critic conflict check |
| [CoTracker](https://arxiv.org/abs/2307.07635) | 2023 | architecture_transfer | Transformer that tracks many 2D points jointly in long video, exploiting point dependencies | paper, code, checkpoints | Object identity and motion evidence for F2; candidate signal for A6 preserve_object_identity |
| [SAM 2](https://arxiv.org/abs/2408.00714) | 2024 | architecture_transfer | Promptable segmentation foundation model for images and videos with a data engine | paper, code, checkpoints, demo | Mask prior for dynamic/static separation; supports object permanence evidence without Dream training |
| [SpatialTracker](https://arxiv.org/abs/2404.04319) | 2024 | architecture_transfer | Lifts 2D pixel tracking to 3D space to handle occlusion and discontinuity | paper, code | 3D-aware track prior for F2 and F3; follow-up SpatialTrackerV2 (2507.12462) unifies tracking, depth, and pose |

### Monocular Metric-Depth Priors

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [Depth Anything V2](https://arxiv.org/abs/2406.09414) | 2024 | architecture_transfer | Large-scale monocular depth foundation model producing finer and more robust depth | paper, code, checkpoints | Depth prior for A7 add_sensor_prior and A7 check_prior_conflict; relates to F3 and F5 |
| [Depth Pro](https://arxiv.org/abs/2410.02073) | 2024 | architecture_transfer | Zero-shot metric monocular depth with sharp boundaries at near-real-time speed | paper, code, checkpoints | Metric scale prior for A1 state-update and A7 add_sensor_prior; directly relevant to gauge/anchor reasoning |
| [Metric3D v2](https://arxiv.org/abs/2404.15506) | 2024 | architecture_transfer | Zero-shot metric depth and surface normal from a single image | paper, code | Joint depth/normal prior; supports cross-modal branch and geometry critic |

### Active Perception / Next-Best-View

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [ActiveNeRF](https://arxiv.org/abs/2209.08546) | 2022 | architecture_transfer | Uncertainty-aware NeRF with active view selection via uncertainty estimation | paper, ECCV | Canonical NBV-in-neural-field anchor; supports A8 request_new_view |
| [FisherRF](https://arxiv.org/abs/2311.17874) | 2023/2024 | architecture_transfer | Fisher-information based active view selection and uncertainty quantification for radiance fields | paper, code, ECCV 2024 | Principled view-gain signal; required comparator for A8 proxy P7 |
| [ActiveSplat](https://arxiv.org/abs/2410.21955) | 2024 | architecture_transfer | Online active mapping with Gaussian splatting plus viewpoint selection and path planning | paper, RA-L 2025, project page | Active-3DGS anchor; strong teacher-demo path for A8 once mock simulation is designed |
| [ActiveGS](https://arxiv.org/abs/2412.17769) | 2024 | architecture_transfer | Active scene reconstruction using Gaussian splatting | paper | Comparator for ActiveSplat and FisherRF; supports design-only A8 proxy design |

### Event / Cross-Modal

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [DEVO (Deep Event Visual Odometry)](https://arxiv.org/abs/2312.09800) | 2023 | architecture_transfer | Learning-based monocular event-only VO with patch selector and pooled multinomial | paper, RA-L 2023 | Event-only pose / motion prior; required comparator for any event-augmented 3R claim (paired with EAG3R, Event-3DGS) |

### Existing Entry Clarification

`Next Best Sense` entry above refers to arXiv paper `2410.04680` ("Next Best Sense: Guiding Vision and Touch with FisherRF for 3D Gaussian Splatting"). It is a robotics extension that uses FisherRF as a component, not a standalone NBV method.

### Gap Closure Summary

| Target gap | Previous coverage | New anchors |
|---|---|---|
| Visual priors (A6/A7 semantic, tracking) | intake-only | DINOv2, CoTracker, SAM 2, SpatialTracker |
| Monocular depth priors (A7) | only indirectly via G-CUT3R | Depth Anything V2, Depth Pro, Metric3D v2 |
| Active perception / NBV (A8) | NextBestSense only | ActiveNeRF, FisherRF, ActiveSplat, ActiveGS |
| Event-camera 3R (A7 F5) | EAG3R, Event-3DGS, Interp3R | DEVO (event-only VO baseline) |

### Still-Open Sub-Gaps

- IMU / LiDAR guided 3R beyond G-CUT3R
- event-based dense reconstruction (beyond Event-3DGS) if we target cross-modal branch
- long-video tracking benchmarks relevant to F2 evaluation
- diffusion-prior 3R (if we later justify a generative-prior arm)
- VLM / scene-regime classification for composer L2

These gaps are noted, not scheduled. They should be filled only when a branch that owns them is chosen for mechanism spec drafting.

## Cycle 008.5 SPINE Anchor Map

Status: navigation overlay, not a new evidence claim. Added in cycle 008.5 to give a reader of this full source map a direct pointer to the curated reading order in `literature/SPINE_*.md`. Symmetric counterpart lives in `registry/source_registry.md` (`Cycle 008.5 SPINE Anchor Map` section).

Rule: this section maps inventory rows above to `literature/SPINE_*.md` files. It does NOT change any evidence label or readiness above. Per `literature/INDEX.md` Usage Rules, evidence-label edits happen in this inventory and in cycle logs, not silently in the SPINE files.

| Finalist SPINE | Linked spec | Required-reading anchors (titles as listed above) | Advanced-reading anchors |
|---|---|---|---|
| `literature/SPINE_CRITIC.md` | `specs/SPEC-20260503-001-geometry-critic.md` | Test3R; TTT3R; CTRL (cross-domain analog); MASt3R-SfM | G-CUT3R |
| `literature/SPINE_MEMORY.md` | `specs/SPEC-20260503-002-executive-memory.md` | CUT3R; STream3R; LONG3R; LoGeR; Mem3R; OVGGT | PAS3R; FILT3R; LongStream |
| `literature/SPINE_PERMANENCE.md` | `specs/SPEC-20260503-003-dynamic-object-permanence.md` | MonST3R; POMATO; D^2USt3R; Easi3R; RayMap3R | SAM 2; SpatialTracker; CoTracker |
| `literature/SPINE_COMPOSER.md` | `specs/SPEC-20260504-001-3r-composer.md` | DUSt3R; MASt3R; Fast3R; Spann3R | CUT3R; OVGGT; cross-domain MoE / routing literature (cited as `inferred` per `literature/INDEX.md` evidence discipline) |

Cross-cutting notes:

- CUT3R is required reading for Memory and advanced reading for Composer. The Memory finalist treats CUT3R as the canonical recurrent-state mechanism; the Composer finalist treats CUT3R as a streaming-regime row in the regime card, not as the routing mechanism itself.
- OVGGT is required reading for Memory and advanced reading for Composer for the symmetric reason (constant-budget cache as a Memory policy lever; long-stream regime row for Composer).
- Foundation visual / dynamic priors used as inputs to the Permanence pipeline (SAM 2, SpatialTracker, CoTracker) are advanced reading rather than required because they are pipeline inputs, not anchors of the Permanence mechanism claim.
- Mixture-of-experts and routing literature in the language / vision domains is intentionally left without a registry ID. Its evidence label in `literature/SPINE_COMPOSER.md` is `inferred`, owned by that SPINE file, and is not promoted to inventory rows here.

No new sources are added by this section; no evidence label or Dream-relevance text above is changed by this section.

## Cycle 013 Source Mining Pass (2026-05-05)

Targeted mining for cycle-013 Phase-2 prep. Focus on coverage gaps not already covered by SPINE files: (i) the most recent 2026 streaming-memory + dynamic-permanence + test-time-training papers, (ii) external curated indexes that catch what individual searches miss, (iii) benchmarks / challenges Dream may want to position against. Web-derived; URL-verified at mining time.

### Cycle 013 newly mined sources

| Source | Year | Tag | Mechanism | Evidence | Dream relevance |
|---|---:|---|---|---|---|
| [Mem3R](https://arxiv.org/abs/2604.07279) | 2026 | direct_3r / memory | Hybrid memory streaming 3R: implicit MLP fast-weight memory (camera tracking via Test-Time Training, LaCT-inspired) decoupled from explicit token memory (geometry); 793M -> 644M params; outperforms CUT3R on long sequences | paper | **High**: directly relevant to Memory finalist (SPEC-20260503-002) — concrete instance of "decouple tracking-state from mapping-state", a candidate Memory L3 ablation axis; supersedes some claims in `cases/CASE-20260504-MEMORY-02.md` Spann3R-vs-Dream framing because Mem3R is a closer contemporaneous comparator. Add to SPINE_MEMORY required reading at next SPINE refresh. |
| [MapAnything (v3 Jan 2026)](https://arxiv.org/abs/2509.13414) | 2026 | direct_3r | Universal feed-forward metric 3D reconstruction; references spatial-memory 3R approaches | paper | **Medium**: comparator for Composer's regime classification (it claims universal coverage; if true that compresses regime axes Composer relies on; needs careful regime label re-check at L3 time). Add to SPINE_COMPOSER advanced reading. |
| [Julian Ost AAAI-2026 (driving scenes)](https://www.ostjul.com/) | 2026 | dynamic_4d | Generates large-scale 3D driving scenes with explicit object permanence + causal NVS; scene-graph decomposition with object transforms | paper, project page | **Medium**: directly cites "object permanence" terminology — name-collision with Permanence finalist, useful for related-work positioning ("explicit-permanence in driving generation vs. action-set permanence in Dream"). Add to SPINE_PERMANENCE advanced reading; deconfuse in `literature/CRITICAL_NOTES.md`. |
| [tttLRM (CVPR 2026)](https://cwchenwang.github.io/tttLRM/) / [GitHub](https://github.com/cwchenwang/tttLRM) | 2026 | architecture_transfer | Test-time training for long-context autoregressive 3D reconstruction | paper, code | **High**: bridges Memory + Critic finalist concerns. Cycle-009 CRITIC-03 cites Test3R / TTT3R as anchors; tttLRM is the long-context successor. Add to SPINE_CRITIC + SPINE_MEMORY at next refresh. |
| [awesome-dust3r](https://github.com/ruili3/awesome-dust3r) | 2025/2026 | meta-index | Curated, regularly updated list of DUSt3R/MASt3R follow-ups (VGGT, MASt3R-SLAM, Light3R-SfM, π³, MoGe-2, STream3R, Dens3R, ViPE, ...) | code-curated index | **High**: meta-resource for ongoing source mining. Cycle-013 does NOT inline-cite all entries (would violate Discipline rule 3 Surgical Edits); instead cite the index as the inventory anchor and let cycle-014+ pull individual rows when a specific gap appears. |
| [DUSt3R / MASt3R / VGGT MVS evaluation (Taylor & Francis 2025)](https://www.tandfonline.com/doi/full/10.1080/10095020.2025.2597491) | 2025 | benchmark / evaluation | Empirical evaluation of DUSt3R + MASt3R + VGGT on a multi-view stereo benchmark with high-res images and multi-camera videos | paper | **Medium**: external comparator-evaluation work; useful for Composer's capability_card sanity check at L3 time. Add to SPINE_COMPOSER advanced reading. |
| [NTIRE 2026 3D Restoration and Reconstruction Challenge](https://www.codabench.org/competitions/13854/) | 2026 | benchmark / challenge | CVPR NTIRE 2026 challenge track | challenge page | **Low/Medium**: positioning anchor — a public benchmark Dream may target if Phase 2 paper writing aims for venue alignment. Recorded as inventory; no Dream commitment to participate. |
| [VGGT](https://github.com/facebookresearch/vggt) | 2025 | direct_3r | Feed-forward visual-geometry transformer; named in DUSt3R/MASt3R/VGGT evaluation paper above as a current SOTA comparator | code (Meta open-source; not Read by agent in cycle 013) | **Medium**: comparator the existing Composer capability_card may have undercounted (cycle 009 + 012 Composer cards do NOT include VGGT row). Surface as a v2.2 capability_card schema gap candidate for cycle 014+. |

### Cycle 013 mining methodology + boundary

```text
methodology:
  - Web search with queries scoped to 2026 + finalist-relevant
    keywords (streaming pointmap memory; dynamic scene + object
    permanence; test-time training + critic; DUSt3R follow-up
    benchmark).
  - Filter: keep results that name a specific paper / repo / page
    URL + a concrete mechanism claim. Drop blog posts, marketing
    pages, single-tweet announcements.
  - Cross-check: avoid duplicating any source already in cycle-005
    or cycle-008.5 SPINE Anchor Map sections above.
  - Time-bound: cycle 013 was a single mining pass within the cycle.
    Comprehensive coverage is NOT claimed; this is a targeted top-up,
    not a re-do of cycle 005.

boundary:
  - Each newly mined source is `paper` / `code` / `code-curated index` /
    `challenge page` evidence-labeled. None is `demo-observed` or
    `measured` because the agent did not run any of them.
  - Dream-relevance text reflects positioning judgment, not
    measurement; per Discipline rule 5 (Honesty Override) those
    text values are themselves `inferred`.
  - SPINE files are NOT retroactively edited in cycle 013 to fold in
    the new sources. The "add at next refresh" pointer is a deferred
    queue, not a closed action. Surgical Edits rule.
  - `registry/source_registry.md` gets new SRC-* rows for the cycle-013
    sources via a separate sync-pass Edit.
```

### Coverage gaps cycle 013 did NOT close

```text
- Active perception (F4): cycle 013 did not mine; consistent with
  Active Perception finalist still un-promoted.
- Cross-modal (F5) beyond what cycle 005 already mined: cycle 013
  did not extend; Cross-Modal finalist also un-promoted.
- Real-time / latency benchmarks: not surfaced (no targeted query;
  Composer's cost_normalized axis remains paper-derived per
  COMPOSER-04).
- Code-execution-derived evidence: out of scope by cycle-013
  authorization (markdown + inventory only).
```
