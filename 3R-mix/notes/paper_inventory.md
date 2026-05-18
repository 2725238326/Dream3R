# Paper inventory

Status: first-stage bibliography and PDF intake log for the 3R survey.

Inventory date: 2026-05-11.

Second-pass note: selected core papers have now been abstract/front-matter extracted into `notes/fact_cards.md`. This upgrades mechanism-level wording in `main.typ`, but benchmark tables, licenses, and full limitations remain pending full-paper/repository checks.

Source policy:

- Primary source is arXiv, CVF/ECCV, official project page, or official GitHub.
- PDFs listed as `downloaded` were saved under `E:\kykt\Dream\3R-mix\papers`.
- Reading status is deliberately conservative: `metadata/abstract checked` means the title, arXiv id, authors, and high-level abstract claim were checked, not that the full paper has been read.
- Code status in this file is not a license clearance. It must be rechecked from repository files before public use, commercial use, or reproduction claims.

## Core 3R papers

| cite key | model | year | title / source | local PDF | read status | code / project status |
|---|---:|---:|---|---|---|---|
| `dust3r` | DUSt3R | 2023/2024 | [DUSt3R: Geometric 3D Vision Made Easy](https://arxiv.org/abs/2312.14132) | `papers/dust3r_2312.14132.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: NAVER repo with code/checkpoints/demo |
| `mast3r` | MASt3R | 2024 | [Grounding Image Matching in 3D with MASt3R](https://arxiv.org/abs/2406.09756) | `papers/mast3r_2406.09756.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: NAVER repo with code/checkpoints/demo |
| `mast3r_sfm` | MASt3R-SfM | 2024 | [MASt3R-SfM: a Fully-Integrated Solution for Unconstrained Structure-from-Motion](https://arxiv.org/abs/2409.19152) | `papers/mast3r_sfm_2409.19152.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: code via MASt3R ecosystem; exact terms pending |
| `mvdust3rplus` | MV-DUSt3R+ | 2024/2025 | [MV-DUSt3R+: Single-Stage Scene Reconstruction from Sparse Views In 2 Seconds](https://arxiv.org/abs/2412.06974) | `papers/mvdust3rplus_2412.06974.pdf` | front matter + official repo checked 2026-05-13; full table extraction pending | official repo: code/checkpoints/Gradio; README lists CC BY-NC 4.0 |
| `fast3r` | Fast3R | 2025 | [Fast3R: Towards 3D Reconstruction of 1000+ Images in One Forward Pass](https://arxiv.org/abs/2501.13928) | `papers/fast3r_2501.13928.pdf` | front matter + system table checked 2026-05-13; full table extraction pending | official repo: code/demo/HF model; Linux/CUDA/PyTorch environment required |
| `vggt` | VGGT | 2025 | [VGGT: Visual Geometry Grounded Transformer](https://arxiv.org/abs/2503.11651) | `papers/vggt_2503.11651.pdf` | front matter + official repo checked 2026-05-13; local quality comparison not done | official repo: code/training/demo; license differs between original and commercial checkpoint |
| `mapanything` | MapAnything | 2025/2026 | [MapAnything: Universal Feed-Forward Metric 3D Reconstruction](https://arxiv.org/abs/2509.13414) | `papers/mapanything_2509.13414.pdf` | metadata/abstract checked; full reading pending | official code/license status 尚需确认 |
| `align3r` | Align3R | 2024/2025 | [Align3R: Aligned Monocular Depth Estimation for Dynamic Videos](https://arxiv.org/abs/2412.03079) | `papers/align3r_2412.03079.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |
| `pow3r` | Pow3R | 2025 | [Pow3R: Empowering Unconstrained 3D Reconstruction with Camera and Scene Priors](https://arxiv.org/abs/2503.17316) | `papers/pow3r_2503.17316.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |

## Long sequence, memory, and streaming

| cite key | model | year | title / source | local PDF | read status | code / project status |
|---|---:|---:|---|---|---|---|
| `cut3r` | CUT3R | 2025 | [Continuous 3D Perception Model with Persistent State](https://arxiv.org/abs/2501.12387) | `papers/cut3r_2501.12387.pdf` | metadata/abstract checked; Fig.1 crop visually verified 2026-05-13 | `registry-listed`: code/checkpoints/demo; setup cost noted |
| `spann3r` | Spann3R | 2024 | [3D Reconstruction with Spatial Memory](https://arxiv.org/abs/2408.16061) | `papers/spann3r_2408.16061.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: code; local adapter quality pending |
| `point3r` | Point3R | 2025 | [Point3R: Streaming 3D Reconstruction with Explicit Spatial Pointer Memory](https://arxiv.org/abs/2507.02863) | `papers/point3r_2507.02863.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: code/checkpoint; first demo path less direct |
| `stream3r` | STream3R | 2025/2026 | [STream3R: Scalable Sequential 3D Reconstruction with Causal Transformer](https://arxiv.org/abs/2508.10893) | `papers/stream3r_2508.10893.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: repo/app/inference path; license pending |
| `long3r` | LONG3R | 2025 | [LONG3R: Long Sequence Streaming 3D Reconstruction](https://arxiv.org/abs/2507.18255) | `papers/long3r_2507.18255.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |
| `loger` | LoGeR | 2026 | [LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory](https://arxiv.org/abs/2603.03269) | `papers/loger_2603.03269.pdf` | project page checked 2026-05-13; full table extraction pending | project page lists paper/arXiv/code; code license not read |
| `mem3r` | Mem3R | 2026 | [Mem3R: Streaming 3D Reconstruction with Hybrid Memory via Test-Time Training](https://arxiv.org/abs/2604.07279) | `papers/mem3r_2604.07279.pdf` | project page checked 2026-05-13; full table extraction pending | project page documents hybrid memory; code/license not fully read |
| `ovggt` | OVGGT | 2026 | [OVGGT: O(1) Constant-Cost Streaming Visual Geometry Transformer](https://arxiv.org/abs/2603.05959) | `papers/ovggt_2603.05959.pdf` | arXiv page checked 2026-05-13; full table extraction pending | arXiv lists project and code links; repository license not read |
| `pas3r` | PAS3R | 2026 | [PAS3R: Pose-Adaptive Streaming 3D Reconstruction for Long Video Sequences](https://arxiv.org/abs/2603.21436) | `papers/pas3r_2603.21436.pdf` | arXiv page checked 2026-05-13; full reading pending | no stronger code claim recorded beyond arXiv |
| `filt3r` | FILT3R | 2026 | [FILT3R: Latent State Adaptive Kalman Filter for Streaming 3D Reconstruction](https://arxiv.org/abs/2603.18493) | `papers/filt3r_2603.18493.pdf` | arXiv page checked 2026-05-13; full reading pending | arXiv says code will be released; availability/license not upgraded |
| `longstream` | LongStream | 2026 | [LongStream: Long-Sequence Streaming Autoregressive Visual Geometry](https://arxiv.org/abs/2602.13172) | `papers/longstream_2602.13172.pdf` | arXiv/project-page metadata checked 2026-05-13; full reading pending | arXiv lists project page; code/license not upgraded |

## Dynamic scenes and 4D

| cite key | model | year | title / source | local PDF | read status | code / project status |
|---|---:|---:|---|---|---|---|
| `monst3r` | MonST3R | 2024/2025 | [MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion](https://arxiv.org/abs/2410.03825) | `papers/monst3r_2410.03825.pdf` | metadata/abstract checked; Fig.1 crop visually verified 2026-05-13 | `registry-listed`: code/demo; figure reuse cleared by user confirmation |
| `pomato` | POMATO | 2025 | [POMATO: Marrying Pointmap Matching with Temporal Motion for Dynamic 3D Reconstruction](https://arxiv.org/abs/2504.05692) | `papers/pomato_2504.05692.pdf` | metadata/abstract checked; full reading pending | code/location claim 尚需确认 |
| `d2ust3r` | D^2USt3R | 2025 | [D^2USt3R: Enhancing 3D Reconstruction for Dynamic Scenes](https://arxiv.org/abs/2504.06264) | `papers/d2ust3r_2504.06264.pdf` | metadata/abstract checked; full reading pending | code status 尚需确认 |
| `easi3r` | Easi3R | 2025 | [Easi3R: Estimating Disentangled Motion from DUSt3R Without Training](https://arxiv.org/abs/2503.24391) | `papers/easi3r_2503.24391.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |
| `raymap3r` | RayMap3R | 2026 | [RayMap3R: Inference-Time RayMap for Dynamic 3D Reconstruction](https://arxiv.org/abs/2603.20588) / [project](https://raymap3r.github.io/) | `papers/raymap3r_2603.20588.pdf` | project page checked 2026-05-13; full reading pending | project page lists arXiv/code; application quality not locally verified |

## Test-time verification, adaptation, and guided priors

| cite key | model | year | title / source | local PDF | read status | code / project status |
|---|---:|---:|---|---|---|---|
| `test3r` | Test3R | 2025 | [Test3R: Learning to Reconstruct 3D at Test Time](https://arxiv.org/abs/2506.13750) | `papers/test3r_2506.13750.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: code; integration cost pending |
| `ttt3r` | TTT3R | 2025/2026 | [TTT3R: 3D Reconstruction as Test-Time Training](https://arxiv.org/abs/2509.26645) | `papers/ttt3r_2509.26645.pdf` | PDF front matter + project page checked 2026-05-13 | project page reports 20 FPS / 6 GB; cite only with hardware/sequence caveat |
| `gcut3r` | G-CUT3R | 2025 | [G-CUT3R: Guided 3D Reconstruction with Camera and Depth Prior Integration](https://arxiv.org/abs/2508.11379) | `papers/g_cut3r_2508.11379.pdf` | metadata/abstract checked; full reading pending | code status 尚需确认 |

## Gaussian and renderable output

| cite key | model / representation | year | title / source | local PDF | read status | code / project status |
|---|---:|---:|---|---|---|---|
| `splatt3r` | Splatt3R | 2024 | [Splatt3R: Zero-shot Gaussian Splatting from Uncalibrated Image Pairs](https://arxiv.org/abs/2408.13912) | `papers/splatt3r_2408.13912.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: code/checkpoint/Gradio; non-commercial note to verify |
| `instantsplat` | InstantSplat | 2024 | [InstantSplat: Sparse-view Gaussian Splatting in Seconds](https://arxiv.org/abs/2403.20309) | `papers/instantsplat_2403.20309.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: NVLabs repo/scripts; license file pending verification |
| `noposplat` | NoPoSplat | 2024/2025 | [No Pose, No Problem: Surprisingly Simple 3D Gaussian Splats from Sparse Unposed Images](https://arxiv.org/abs/2410.24207) | `papers/noposplat_2410.24207.pdf` | metadata/abstract checked; full reading pending | `registry-listed`: repo/checkpoints; demo path pending |
| `gaussian_splatting_3d` | 3DGS | 2023 | [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079) | `papers/3d_gaussian_splatting_2308.04079.pdf` | metadata/abstract checked; full reading pending | official INRIA/GraphDeco repo exists; application use pending |
| `gaussian_splatting_4d` | 4DGS | 2023/2024 | [4D Gaussian Splatting for Real-Time Dynamic Scene Rendering](https://arxiv.org/abs/2310.08528) | `papers/4dgs_realtime_2310.08528.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |
| `rotor_4dgs` | 4D-Rotor-GS | 2024 | [4D-Rotor Gaussian Splatting: Towards Efficient Novel View Synthesis for Dynamic Scenes](https://arxiv.org/abs/2402.03307) | `papers/4d_rotor_gs_2402.03307.pdf` | metadata/abstract checked; full reading pending | project/code status 尚需确认 |

## Supporting priors

| cite key | method | year | title / source | local PDF | read status | use in survey |
|---|---:|---:|---|---|---|---|
| `depth_anything` | Depth Anything | 2024 | [Depth Anything: Unleashing the Power of Large-Scale Unlabeled Data](https://arxiv.org/abs/2401.10891) | `papers/depth_anything_2401.10891.pdf` | metadata/abstract checked; full reading pending | background for monocular depth priors |
| `depth_anything_v2` | Depth Anything V2 | 2024 | [Depth Anything V2](https://arxiv.org/abs/2406.09414) | `papers/depth_anything_v2_2406.09414.pdf` | metadata/abstract checked; full reading pending | depth prior; avoid replacing 3R claims |
| `dinov2` | DINOv2 | 2023 | [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) | `papers/dinov2_2304.07193.pdf` | metadata/abstract checked; full reading pending | visual feature prior |
| `dinov3` | DINOv3 | 2025 | [DINOv3](https://arxiv.org/abs/2508.10104) / [Meta page](https://ai.meta.com/dinov3/) | `papers/dinov3_2508.10104.pdf` | metadata/abstract checked; full reading pending | optional newer feature prior; use sparingly |
| `cotracker` | CoTracker | 2023 | [CoTracker: It is Better to Track Together](https://arxiv.org/abs/2307.07635) | `papers/cotracker_2307.07635.pdf` | metadata/abstract checked; full reading pending | point tracking prior for dynamic sections |
| `sam2` | SAM 2 | 2024 | [SAM 2: Segment Anything in Images and Videos](https://arxiv.org/abs/2408.00714) | `papers/sam2_2408.00714.pdf` | metadata/abstract checked; full reading pending | mask/video segmentation prior |
| `spatialtracker` | SpatialTracker | 2024 | [SpatialTracker: Tracking Any 2D Pixels in 3D Space](https://arxiv.org/abs/2404.04319) | `papers/spatialtracker_2404.04319.pdf` | metadata/abstract checked; full reading pending | 3D-aware tracking prior |
| `depth_pro` | Depth Pro | 2024 | [Depth Pro: Sharp Monocular Metric Depth in Less Than a Second](https://arxiv.org/abs/2410.02073) | `papers/depth_pro_2410.02073.pdf` | metadata/abstract checked; full reading pending | metric depth prior |
| `metric3dv2` | Metric3D v2 | 2024 | [Metric3Dv2: A Versatile Monocular Geometric Foundation Model for Zero-shot Metric Depth and Surface Normal Estimation](https://arxiv.org/abs/2404.15506) | `papers/metric3dv2_2404.15506.pdf` | metadata/abstract checked; full reading pending | metric depth / normal prior |

## Non-paper local sources read for framing

| file | role |
|---|---|
| `E:\kykt\Dream\TASK_SNAPSHOT.md` | Active work status and honesty constraints; reinforces no unsupported quality claims. |
| `E:\kykt\Dream\code\dream3r\SOTA_FEATURE_MATRIX.md` | Dream-side feature mapping and explicit unsafe-claim list. |
| `E:\kykt\Dream\code\dream3r\RESEARCH_LITERATURE_MAP.md` | Module-to-literature map; safe/unsafe claim separation. |
| `E:\kykt\Dream\code\dream3r\RESEARCH_BASE_AND_INNOVATIONS.md` | Dream method background; use only in methodology/outlook sections. |
| `E:\kykt\Dream\code\dream3r\NEXT_PHASE_ROADMAP.md` | Future work and evidence gaps; do not cite as completed result. |
| `E:\kykt\Dream\sources\FRONTIER_SOURCE_MAP.md` | Primary source map and evidence labels. |
| `E:\kykt\Dream\registry\source_registry.md` | Lightweight URL/code status registry. |
| `E:\kykt\Dream\units\REPRODUCTION_READINESS_MATRIX.md` | Reproduction ranking and license/dependency caveats. |
| `E:\kykt\Dream\units\RESEARCH_UNIT_BANK.md` | Application-oriented research units and KYKT integration ideas. |
| `E:\kykt\Dream\literature\INDEX.md` | Evidence discipline for local literature notes. |
| `E:\kykt\Dream\literature\SPINE_CRITIC.md` | Test-time verification and adaptation distinctions. |
| `E:\kykt\Dream\literature\SPINE_MEMORY.md` | Memory/state/cache distinction notes. |
| `E:\kykt\Dream\literature\SPINE_PERMANENCE.md` | Dynamic 3R and object permanence boundary notes. |
| `E:\kykt\Dream\literature\SPINE_COMPOSER.md` | Model ecology and regime-routing framing. |
| `E:\kykt\ppt\3r_models_survey\research_notes.md` | Earlier Chinese explanation route for DUSt3R family and Depth Anything connection. |

## Immediate reading priorities before prose drafting

1. Read DUSt3R, MASt3R, Fast3R, VGGT, CUT3R, Spann3R, MonST3R in enough detail to support the opening half of the survey.
2. Read MASt3R-SfM, Test3R, TTT3R, G-CUT3R before writing the verification/adaptation chapter.
3. Read the 2026 memory papers as a group before making any taxonomy claim about memory/cache/state.
4. Read Splatt3R, InstantSplat, NoPoSplat, 3DGS, and 4DGS before writing application-output sections.
5. Use supporting priors only after deciding where they materially explain a 3R model's inputs, training, or failure handling.
