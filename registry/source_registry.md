# Source Registry

Last updated: 2026-05-05 (cycle 013 source mining pass: 7 new SRC entries SRC-2026-009..015 covering MapAnything / Julian Ost AAAI-2026 driving permanence / tttLRM / awesome-dust3r / DUSt3R-MASt3R-VGGT MVS evaluation / NTIRE 2026 / VGGT)

Status: seeded from Phase 1 source map. This file is the lightweight index; detailed notes stay in `sources/FRONTIER_SOURCE_MAP.md` and cycle logs.

## Schema

```text
source_id:
title:
url:
year:
track:
evidence:
mechanism_one_liner:
readiness:
linked_units:
```

## Seed Sources

| ID | Title | URL | Year | Track | Evidence | Mechanism | Readiness | Linked units |
|---|---|---:|---:|---|---|---|---|---|
| SRC-2024-001 | DUSt3R | https://github.com/naver/dust3r | 2024 | direct_3r | paper, code, checkpoints, demo | pose-free pointmap reconstruction | P0 baseline | RU-002, RU-014 |
| SRC-2024-002 | MASt3R | https://github.com/naver/mast3r | 2024 | direct_3r | paper, code, checkpoints, demo | 3D-grounded matching and sparse global alignment | P1 baseline | RU-002 |
| SRC-2024-003 | MonST3R | https://github.com/Junyi42/monst3r | 2024 | direct_3r | paper, code, demo | dynamic-video pointmap reconstruction | P1 dynamic | RU-013 |
| SRC-2024-011 | Spann3R | https://github.com/HengyiWang/spann3r | 2024 | direct_3r | paper, code | spatial memory for global pointmap prediction | P1 memory comparator | RU-001, RU-004, RU-014, RU-015 |
| SRC-2025-001 | Fast3R | https://github.com/facebookresearch/fast3r | 2025 | direct_3r | paper, code, checkpoint, demo | many images in one forward pass | P1 scale | RU-002, RU-014 |
| SRC-2025-002 | CUT3R | https://github.com/CUT3R/CUT3R | 2025 | direct_3r | paper, code, checkpoints, demo | persistent-state continuous 3D perception | P2 architecture baseline | RU-001, RU-014 |
| SRC-2025-003 | Point3R | https://github.com/YkiWu/Point3R | 2025 | direct_3r | paper, code, checkpoint | explicit spatial pointer memory | P2 comparator | RU-004, RU-014 |
| SRC-2026-001 | STream3R | https://github.com/NIRVANALAN/STream3R | 2026 | direct_3r | paper, code, app, inference path | causal transformer and stream session for 3R | P2 comparator | RU-010, RU-014 |
| SRC-2025-004 | TTT3R | https://github.com/Inception3D/TTT3R | 2025 | architecture_transfer | paper, code, demo command | test-time update rule for CUT3R | P2 add-on | RU-003, RU-011, RU-012 |
| SRC-2024-004 | Splatt3R | https://github.com/btsmart/splatt3r | 2024 | demo_enabler | paper, code, checkpoint, Gradio | uncalibrated image pairs to 3D Gaussians | P0 visual | RU-008 |
| SRC-2024-005 | InstantSplat | https://github.com/NVlabs/InstantSplat | 2024 | demo_enabler | paper, code, scripts | sparse-view SfM-free Gaussian Splatting | P0/P1 visual | RU-008 |
| SRC-2025-005 | MV-DUSt3R+ | https://github.com/facebookresearch/mvdust3r | 2025 | direct_3r | paper, code, checkpoints, Gradio | sparse-view pose-free RGB reconstruction | P1 visual/geometry | RU-008 |
| SRC-2025-006 | NoPoSplat | https://github.com/cvg/NoPoSplat | 2025 | demo_enabler | paper, code, checkpoints | sparse unposed images to Gaussians | P2 comparator | RU-008 |
| SRC-2023-001 | Mamba | https://arxiv.org/abs/2312.00752 | 2023 | architecture_transfer | paper, code known | selective state space sequence modeling | mechanism | RU-001 |
| SRC-2024-006 | Mamba-2 / SSD | https://arxiv.org/abs/2405.21060 | 2024 | architecture_transfer | paper, code | state space duality and efficient state layer | mechanism | RU-001, RU-010 |
| SRC-2024-007 | VMamba | https://arxiv.org/abs/2401.10166 | 2024 | architecture_transfer | paper, code | 2D selective scan routes | mechanism | RU-009 |
| SRC-2024-008 | MambaOut | https://arxiv.org/abs/2405.07992 | 2024 | negative_control | paper, code | SSM is not always needed for vision | caution | RU-001, RU-010 |
| SRC-2025-007 | Test3R | https://arxiv.org/abs/2506.13750 | 2025 | architecture_transfer | paper, code | test-time geometric consistency | P2/P3 | RU-003, RU-011 |
| SRC-2025-008 | CTRL | https://arxiv.org/abs/2502.03492 | 2025 | architecture_transfer | paper, code | critic-revision through RL-trained critic | mechanism | RU-011 |
| SRC-2025-009 | SEAL | https://arxiv.org/abs/2506.10943 | 2025 | architecture_transfer | paper, code | self-edit driven adaptation | mechanism | RU-012 |
| SRC-2025-010 | POMATO | https://arxiv.org/abs/2504.05692 | 2025 | direct_3r | paper | pointmap matching plus temporal motion | comparator | RU-013 |
| SRC-2025-011 | D^2USt3R | https://arxiv.org/abs/2504.06264 | 2025 | direct_3r | paper | 4D pointmaps for dynamic scenes | comparator | RU-013 |
| SRC-2025-012 | LONG3R | https://arxiv.org/abs/2507.18255 | 2025 | direct_3r | paper, project | memory gating and 3D spatio-temporal memory for long sequences | core comparator | RU-001, RU-014, RU-015 |
| SRC-2026-002 | LoGeR | https://arxiv.org/abs/2603.03269 | 2026 | direct_3r | paper, project | chunked long-context reconstruction with TTT global memory and SWA local memory | core comparator | RU-010, RU-014, RU-015 |
| SRC-2026-003 | Mem3R | https://arxiv.org/abs/2604.07279 | 2026 | direct_3r | paper, project | hybrid memory decoupling camera tracking from geometric mapping | core comparator | RU-004, RU-012, RU-015 |
| SRC-2026-004 | PAS3R | https://arxiv.org/abs/2603.21436 | 2026 | direct_3r | paper | pose-adaptive streaming state update | core comparator | RU-001, RU-015 |
| SRC-2026-005 | FILT3R | https://arxiv.org/abs/2603.18493 | 2026 | direct_3r | paper, code promised | Kalman-style latent filtering for streaming 3R | mechanism | RU-001, RU-015 |
| SRC-2026-006 | LongStream | https://arxiv.org/abs/2602.13172 | 2026 | direct_3r | paper, project | gauge-decoupled streaming visual geometry and cache refresh | comparator | RU-010, RU-014, RU-015 |
| SRC-2026-007 | OVGGT | https://arxiv.org/abs/2603.05959 | 2026 | visual_geometry | paper, project, code | constant-budget cache compression and dynamic anchor protection | mechanism | RU-010, RU-014, RU-015 |
| SRC-2026-008 | RayMap3R | https://raymap3r.github.io/ | 2026 | dynamic_3r | project, code claimed | inference-time RayMap for dynamic streaming reconstruction | comparator, verify before reproduction | RU-013, RU-015 |
| SRC-2024-009 | MASt3R-SfM | https://arxiv.org/abs/2409.19152 | 2024 | direct_3r | paper, code via MASt3R ecosystem | matching, retrieval, and global SfM alignment | comparator | RU-002, RU-015 |
| SRC-2024-010 | SLAM3R | https://arxiv.org/abs/2412.09401 | 2024 | direct_3r | paper, code | sliding-window dense SLAM using pointmap prediction and registration | comparator | RU-014, RU-015 |
| SRC-2025-013 | Easi3R | https://arxiv.org/abs/2503.24391 | 2025 | dynamic_3r | paper, project | training-free dynamic adaptation / motion separation | comparator | RU-013, RU-015 |
| SRC-2025-014 | G-CUT3R | https://arxiv.org/abs/2508.11379 | 2025 | guided_3r | paper | guided CUT3R with depth / calibration / pose priors | comparator | RU-002, RU-015 |
| SRC-2022-001 | ActiveNeRF | https://arxiv.org/abs/2209.08546 | 2022 | architecture_transfer | paper, ECCV | uncertainty-driven active view selection for NeRF | A8 comparator | future active-perception unit |
| SRC-2023-002 | DINOv2 | https://arxiv.org/abs/2304.07193 | 2023 | architecture_transfer | paper, code, checkpoints | self-supervised all-purpose visual features | A6/A7 visual prior | RU-011, RU-013, RU-015 |
| SRC-2023-003 | CoTracker | https://arxiv.org/abs/2307.07635 | 2023 | architecture_transfer | paper, code, checkpoints | joint 2D point tracking in long video | A6 object identity prior | RU-013 |
| SRC-2023-004 | DEVO | https://arxiv.org/abs/2312.09800 | 2023 | architecture_transfer | paper, RA-L | deep event visual odometry from monocular events | A7 event prior | RU-006 |
| SRC-2024-012 | SAM 2 | https://arxiv.org/abs/2408.00714 | 2024 | architecture_transfer | paper, code, checkpoints, demo | promptable image/video segmentation foundation model | A6 dynamic/static mask prior | RU-013 |
| SRC-2024-013 | SpatialTracker | https://arxiv.org/abs/2404.04319 | 2024 | architecture_transfer | paper, code | tracks 2D pixels in 3D space; V2 (2507.12462) unifies track, depth, pose | A6 3D-aware motion prior | RU-013 |
| SRC-2024-014 | Depth Anything V2 | https://arxiv.org/abs/2406.09414 | 2024 | architecture_transfer | paper, code, checkpoints | monocular depth foundation model; finer and more robust | A7 depth prior | RU-011, RU-015 |
| SRC-2024-015 | Depth Pro | https://arxiv.org/abs/2410.02073 | 2024 | architecture_transfer | paper, code, checkpoints | zero-shot metric monocular depth, sharp boundaries, fast | A1/A7 metric-scale prior | RU-011, RU-015 |
| SRC-2024-016 | Metric3D v2 | https://arxiv.org/abs/2404.15506 | 2024 | architecture_transfer | paper, code | zero-shot metric depth and surface normal from single image | A7 joint geometry prior | RU-006, RU-011 |
| SRC-2024-017 | FisherRF | https://arxiv.org/abs/2311.17874 | 2023/2024 | architecture_transfer | paper, code, ECCV | Fisher-information active view selection and uncertainty for radiance fields | A8 view-gain anchor | future active-perception unit |
| SRC-2024-018 | ActiveSplat | https://arxiv.org/abs/2410.21955 | 2024 | architecture_transfer | paper, project, RA-L | active mapping, view selection, path planning on 3DGS | A8 active-3DGS anchor | future active-perception unit, RU-008 |
| SRC-2024-019 | ActiveGS | https://arxiv.org/abs/2412.17769 | 2024 | architecture_transfer | paper | active scene reconstruction using Gaussian splatting | A8 comparator | future active-perception unit |
| SRC-2026-009 | MapAnything | https://arxiv.org/abs/2509.13414 | 2026 | direct_3r | paper (v3 Jan 2026) | universal feed-forward metric 3D reconstruction; references spatial-memory 3R | Composer regime comparator; verify regime label compression at L3 | RU-002, RU-014 |
| SRC-2026-010 | Julian Ost AAAI-2026 driving permanence | https://www.ostjul.com/ | 2026 | dynamic_4d | paper, project page | scene-graph driving generation with explicit object permanence + causal NVS | Permanence positioning anchor; deconfuse name-collision in CRITICAL_NOTES.md | RU-013 |
| SRC-2026-011 | tttLRM | https://github.com/cwchenwang/tttLRM | 2026 | architecture_transfer | paper, code, project page (CVPR 2026) | test-time training for long-context autoregressive 3D reconstruction | Critic + Memory bridge; long-context successor to Test3R / TTT3R | RU-001, RU-003, RU-011, RU-012 |
| SRC-2026-012 | awesome-dust3r curated index | https://github.com/ruili3/awesome-dust3r | 2025/2026 | meta-index | code-curated index | regularly-updated DUSt3R/MASt3R follow-up index (VGGT, MASt3R-SLAM, Light3R-SfM, π³, MoGe-2, STream3R, Dens3R, ViPE, ...) | meta-resource for ongoing mining; pull individual rows when specific gap appears | n/a |
| SRC-2026-013 | DUSt3R/MASt3R/VGGT MVS evaluation | https://www.tandfonline.com/doi/full/10.1080/10095020.2025.2597491 | 2025 | benchmark / evaluation | paper | empirical MVS evaluation across DUSt3R + MASt3R + VGGT on high-res + multi-camera videos | Composer capability_card sanity check at L3 | RU-002, RU-014 |
| SRC-2026-014 | NTIRE 2026 3D Restoration and Reconstruction Challenge | https://www.codabench.org/competitions/13854/ | 2026 | benchmark / challenge | challenge page | CVPR NTIRE 2026 challenge track | venue-positioning anchor for Phase 2 paper writing; no Dream commitment to participate | n/a |
| SRC-2026-015 | VGGT | https://github.com/facebookresearch/vggt | 2025 | direct_3r | code (Meta open-source) | feed-forward visual-geometry transformer | Composer comparator gap (cycle 009 + 012 cards do NOT include VGGT row); v2.2 capability_card schema candidate for cycle 014+ | RU-002, RU-014 |

## Cycle 008.5 SPINE Anchor Map

Status: navigation overlay, not a new evidence claim. Added in cycle 008.5 so a reader of this lightweight registry can jump to the literature guidance board without re-deriving which sources anchor which finalist. Symmetric counterpart lives at the end of `sources/FRONTIER_SOURCE_MAP.md` (`Cycle 008.5 SPINE Anchor Map` section).

Rule: this section maps inventory rows to `literature/SPINE_*.md` files. It does NOT change any evidence label above. If an evidence label needs to change, edit the row above and log it in a cycle file; do not change it here silently (per `literature/INDEX.md` Usage Rules).

| Finalist SPINE | Linked spec | Required-reading anchors (registry IDs) | Advanced-reading anchors |
|---|---|---|---|
| `literature/SPINE_CRITIC.md` | `specs/SPEC-20260503-001-geometry-critic.md` | SRC-2025-007 Test3R; SRC-2025-004 TTT3R; SRC-2025-008 CTRL; SRC-2024-009 MASt3R-SfM | SRC-2025-014 G-CUT3R |
| `literature/SPINE_MEMORY.md` | `specs/SPEC-20260503-002-executive-memory.md` | SRC-2025-002 CUT3R; SRC-2026-001 STream3R; SRC-2025-012 LONG3R; SRC-2026-002 LoGeR; SRC-2026-003 Mem3R; SRC-2026-007 OVGGT | SRC-2026-004 PAS3R; SRC-2026-005 FILT3R; SRC-2026-006 LongStream |
| `literature/SPINE_PERMANENCE.md` | `specs/SPEC-20260503-003-dynamic-object-permanence.md` | SRC-2024-003 MonST3R; SRC-2025-010 POMATO; SRC-2025-011 D^2USt3R; SRC-2025-013 Easi3R; SRC-2026-008 RayMap3R | SRC-2024-012 SAM 2; SRC-2024-013 SpatialTracker; SRC-2023-003 CoTracker |
| `literature/SPINE_COMPOSER.md` | `specs/SPEC-20260504-001-3r-composer.md` | SRC-2024-001 DUSt3R; SRC-2024-002 MASt3R; SRC-2025-001 Fast3R; SRC-2024-011 Spann3R | SRC-2025-002 CUT3R; SRC-2026-007 OVGGT; cross-domain MoE / routing literature (no SRC ID; cited as `inferred` per `literature/INDEX.md` evidence discipline) |

Cross-cutting notes:

- SRC-2025-002 CUT3R appears under MEMORY required and COMPOSER advanced. Required for Memory because state-recurrence is the mechanism; advanced for Composer because CUT3R is a streaming-regime model the regime card must encode, not the routing mechanism itself.
- SRC-2026-007 OVGGT appears under MEMORY required and COMPOSER advanced. Required for Memory because constant-budget cache compression is a Memory policy lever; advanced for Composer because OVGGT defines a long-stream regime row.
- Sources used as priors / mask inputs for Permanence (SAM 2, SpatialTracker, CoTracker) are listed under Permanence advanced rather than required because they are inputs to the Permanence pipeline, not anchors of its mechanism claim.
- Sources without a registry ID (e.g., MoE routing in language models) are intentionally left unmapped here; the SPINE file owns its `inferred` evidence label per `literature/INDEX.md` rules.

No new sources are added by this section; no readiness label is changed by this section.
