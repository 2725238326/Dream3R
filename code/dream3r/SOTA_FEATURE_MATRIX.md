# Dream3R SOTA Feature Matrix

Status: first mapping for demo and paper framing, updated with real-data smoke evidence.

Date: 2026-05-10

## Purpose

This matrix prevents Dream3R from name-dropping SOTA methods without explaining what was actually absorbed. Each method is mapped to:

- its useful idea,
- its limitation,
- the Dream3R module that absorbs or answers it,
- current implementation status,
- evidence,
- remaining gap.

## Matrix

| Method / Direction | Core Strength | Limitation / Gap | Dream3R Absorption | Status | Evidence | Remaining Gap |
|---|---|---|---|---|---|---|
| MASt3R | Strong pointmap-style 3D reconstruction and matching | Heavy model, not a streaming control architecture | Expert adapter and ComposerRouter capability | Partially real | `test_mast3r_integration`, adapter status, dispatch metadata | Real quality/runtime routing table |
| Spann3R | Streaming-oriented 3R with memory behavior | Method-specific memory, not unified with multi-expert control graph | Expert adapter plus reference for SpatialMemory | Partially real | `test_spann3r_integration` | Real sequence comparison |
| Fast3R | Scales to many views and all-to-all reasoning | Non-streaming; env dependency blocker remains | Expert adapter contract and future routing target | Fallback/blocked | `test_fast3r_integration` | Resolve `omegaconf`/runtime dependency and run real forward |
| CUT3R | State-token recurrence for streaming 3R | Bounded-memory forgetting under long sequences | `StateTokenRecurrence` and active state | Implemented | `test_sequence_training`, `test_state_recurrence_factory` | Real long-sequence ablation |
| VGGT | Unified feed-forward geometry prediction, strong accuracy ceiling | Large monolithic predictor; less explicit control/repair | Backbone/evidence inspiration and future benchmark target | Referenced | Architecture docs | Benchmark comparison only after real data |
| Point3R | Spatial pointer memory and 3D-aware retrieval | Not combined with bus, Critic, expert routing | 3D-aware `AnchorBank` retrieval | Implemented | `test_3d_retrieval`, `test_spatial_payload` | Real spatial retrieval metrics |
| Mem3R / LONG3R | Long-context memory for 3R | Memory mechanisms are not exposed as full control graph | Active/stable memory and AnchorBank lifecycle | Implemented | `test_active_stable`, `test_anchor_bank` | Long sequence degradation curve |
| OnlineX | Active/stable state decoupling | External design, not integrated with Dream3R modules | Active state tokens + stable AnchorBank promote/recall | Implemented | `test_active_stable`, ablation `no_stable_memory` | Real-data stability proof |
| STream3R | Causal decoder-only streaming 3R | Different architectural route from Dream3R | Roadmap comparison, not implemented | Planned | `NEXT_PHASE_ROADMAP.md` W26 | Write relation note and optional adapter design |
| tttLRM | Test-time training for scene-specific adaptation | Requires careful update scope and metrics | Future TTT adapter path | Planned | `NEXT_PHASE_ROADMAP.md` W25 | Implement safe TTT loop after real-data baseline |
| DINOv2 / DINOv3 | Strong frozen visual prior | Checkpoints may be unavailable; not a 3R system alone | Perceiver backbone path with fallback | Implemented | `test_dinov2_backbone` | DINOv3-specific path and feature ablation |
| DeepSeek NSA | Efficient compressed/selected/sliding sparse attention | Language long-context method, not 3D-specific by default | `NSAAttention` maps branches to active state, AnchorBank, sliding frames | Implemented | `test_nsa_attention`, ablation `no_nsa` | Real-data branch utility analysis |
| Mamba | O(N) state-space sequence modeling | Kernel/ABI fragility; needs global correction | `MambaHybridRecurrence` plus frame cross-attention | Implemented | `test_state_recurrence_factory`, `demo_mamba_path`, ablation `mamba_hybrid` | Quality and length-scaling ablation |
| Slot Attention / Object permanence | Object-like latent grouping | Vanilla slots lack frame-to-frame spatial reference | Permanence slots with ISA-style reference poses | Implemented | `test_isa_slots`, `test_permanence_v2` | Real object trajectory visualization |
| Epipolar / Sampson consistency | Geometry-grounded verification | Usually used as loss, not control feedback | Geometric Critic conflict and repair loop | Implemented | `test_geometric_critic`, `test_critic_loop` | Calibrated thresholds and repair precision/recall |
| 3D Gaussian Splatting / AnchorSplat | Real-time renderable 3D representation | Renderer dependency and training complexity | `GaussianHead` tensor contract and AnchorBank source ids | Contract only | `test_gaussian_head_contract` | Renderer-backed output and photometric loss |

## Dream3R Differentiation

Dream3R's claim is not that every borrowed idea is individually new. The claim is the integration pattern:

1. A 3R reconstruction path produces pointmap, confidence, and evidence tokens.
2. Active state tokens evolve per streaming window.
3. Stable AnchorBank stores spatial anchors with payloads.
4. NSA fuses active state, selected stable anchors, and sliding recent context.
5. Critic checks geometric consistency and emits repair actions.
6. Permanence tracks object slots with reference poses.
7. ComposerRouter exposes external 3R methods as routeable expert capabilities.
8. Mamba recurrence can replace cross-attention recurrence without changing the rest of the control graph.
9. GaussianHead defines the future renderable representation contract.

## Evidence Map

| Claim | Current Evidence |
|---|---|
| Control graph is runnable | `smoke_test`, full `dream3r.tests.test_*` |
| Mamba path is real | `demo_mamba_path`, `test_state_recurrence_factory` |
| NSA can be ablated | `ablate_recurrence` with `no_nsa` |
| Stable memory can be ablated | `ablate_recurrence` with `no_stable_memory` |
| Geometric Critic works | `test_geometric_critic`, `test_critic_loop` |
| Slot reference poses work | `test_isa_slots` |
| Expert adapters are represented | `test_composer_experts`, integration tests |
| 3DGS path is bounded | `test_gaussian_head_contract` |
| Real RGB/depth sequence can execute | `evaluate_real_sequence`, `test_kitti_loader_contract`, `test_real_sequence_eval_contract` |

## Missing Evidence

The following must not be overclaimed yet:

- Real-data reconstruction quality.
- SOTA benchmark ranking.
- Long-sequence stability on real scenes.
- Expert routing quality gains.
- Test-time adaptation gains.
- Renderer-backed Gaussian output.

These are explicitly scheduled in `NEXT_PHASE_ROADMAP.md`.
