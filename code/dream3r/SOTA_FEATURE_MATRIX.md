# Dream3R SOTA Feature Matrix

Last updated: 2026-05-25 (Stage 4 closed; Stage 5 S1 three-real-expert Composer ablation strengthened with regime-label features; supersedes 2026-05-23 v0.5 A4/A6/A8 closure pass while preserving its differentiation / evidence-map sections at the end)

Status: family-grouped second pass. Every method named in `NEXT_PHASE_ROADMAP.md` W20 plus the three monocular priors already wired into the Composer expert registry is covered. Methods named in the roadmap but absent from `registry/source_registry.md` are explicitly flagged as drafting artifacts.

## Purpose

This file answers one question:

> For every external 3R-relevant method we cite, which Dream3R module is supposed to absorb its mechanism, and at what implementation tier does that mapping currently sit?

It is the cross-link between three sources of truth:

1. `registry/source_registry.md` — what papers/projects exist.
2. `code/dream3r/composer_experts/method_profiles.py` plus the actual code under `code/dream3r/` — what is wired in.
3. `ARCHITECTURE_V04_STATUS.md` — what closed-loop guarantee, if any, is in place after the v0.4 round.

It is **not**:

- a reproduction-readiness table (that lives at `units/REPRODUCTION_READINESS_MATRIX.md`)
- a finalist-comparison matrix (`planning/BRANCH_COMPARISON_MATRIX.md`)
- a literature spine (`literature/SPINE_*.md`)

When the three sources above disagree, this matrix records the disagreement under "Remaining gap" rather than picking one.

## Evidence and Status Vocabulary

`Implementation status` is one of:

- `real-wired (no local ckpt)` — adapter loader path exists, real checkpoint loads on server; locally degrades to fallback because no checkpoint is resolvable.
- `deterministic fallback` — adapter exists, image-derived deterministic output; v0.4 `ComposerDecision.backend_status.backend == "fallback"`. Not a model.
- `stub` — adapter exists but neither real nor fallback path produces a meaningful 3R signal; `backend == "stub"`.
- `scaffold` — typed policy / updater surface exists and is unit-tested, but the learned or server-validated behavior is deferred.
- `mechanism integrated` — not an adapter; mechanism lives inside a Dream3R core module (e.g., NSA inside `C2 SpatialMemory`).
- `contract-only` — tensor / dataclass contract exists but is **not** in the main forward path (per `ARCHITECTURE_V04_STATUS.md`).
- `comparator-only` — referenced in literature / spec; no code wiring; cited for evidence framing.
- `named, not in registry` — appears in `NEXT_PHASE_ROADMAP.md` W20 but has no `SRC-*` row and no code path; treated as a roadmap drafting artifact until resolved.

`Evidence` labels match the canonical ladder from `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5: `paper-proven`, `code-observed`, `demo-observed`, `inferred`, `unknown`.

`Dream3R module` references the canonical names: C1 Perceiver, C2 SpatialMemory (+ AnchorBank, NSAAttention, build_state_recurrence), C3 Permanence, C4 Critic, C5 Composer (+ ComposerRouter, ExpertRegistry), C6 MemoryBus, plus the v0.4 additive layer: `contracts.py`, `repair.RepairExecutor`, `orchestrator.V04Pipeline`. `GaussianHead` is listed separately because v0.4 keeps it out of the main forward.

## Section 1. Direct Pairwise / Static-Scene 3R

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| MASt3R | SRC-2024-002 | dense 3D-grounded pair matching; sparse global alignment via MASt3R-SfM | pair-centric; needs global mapper for sequence | C5 Composer expert `mast3r_adapter`; `method_profiles["mast3r"]`; capability_card row | real-wired (no local ckpt) | `tests/test_mast3r_integration.py` (server-only); `RECENT_PROGRESS.md` Tier 1 lists adapter loadable | per cycle 014 cards: no per-pair pose-residual case on KYKT-style metadata using real MASt3R; depends on F-002 server run |
| DUSt3R | SRC-2024-001 | pose-free pointmap reconstruction; the original; foundational comparator | superseded for matching by MASt3R; pair-centric | not an adapter (subsumed by MASt3R adapter); cited as baseline in `RU-002`, `RU-014` | comparator-only | `SPINE_COMPOSER.md` Required Reading; baseline reference | no head-to-head DUSt3R-vs-MASt3R route via Composer; out of scope unless a baseline expert is added |
| MASt3R-SfM | SRC-2024-009 | global SfM alignment built on MASt3R matching | requires MASt3R ecosystem | comparator for global-alignment policy under Composer | comparator-only | `SPINE_CRITIC.md` Required Reading | not wired; future Composer-level global-alignment action |

## Section 2. Many-View / Streaming Reconstruction

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| Fast3R | SRC-2025-001 | many-image single-pass reconstruction; reduced sequential error | needs batched views to expose advantage | C5 Composer expert `fast3r_adapter`; `method_profiles["fast3r"]` | real-wired (no local ckpt); local conda blocked on `omegaconf` per `WORKFLOW_STATUS.md` Track A | `tests/test_fast3r_integration.py` (server-only) | server env fix (`omegaconf`) before any real Fast3R route comparison |
| Spann3R | SRC-2024-011 | external spatial memory; ordered/unordered dense reconstruction | retrieval-policy-dependent quality | C5 Composer expert `spann3r_adapter`; conceptual analog of `AnchorBank` per `method_profiles["spann3r"]` | real-wired (no local ckpt) | `tests/test_spann3r_integration.py` (server-only); `CYCLE-20260525-stage5-s1-three-expert.md` shows Spann3R wins oracle on 2 KITTI windows and the strengthened `regime_stats/features` learned router selects Spann3R on both | Stage 5 evidence is still a 12-window KITTI closure ablation, not cross-dataset/SOTA proof |
| CUT3R | SRC-2025-002 | persistent latent state for continuous perception; streaming-friendly | state drift needs explicit critic/memory control | C5 Composer expert `cut3r_adapter`; analog of `StateTokenRecurrence` per `SPINE_MEMORY.md` | deterministic fallback | `composer_experts/method_profiles.py` declares `implementation_status="stub"`; no real adapter checkpoint resolution | adapter `load_checkpoint(path)` not implemented; CR-3 retrieval boost path was designed against this comparator |
| VGGT | SRC-2026-015 | feed-forward visual-geometry transformer; Meta open-source | no temporal state; real checkpoint not downloaded in local/server handoff | C5 Composer expert `vggt_adapter`; `method_profiles["vggt"]`; capability_card v2.2 `feed_forward_manyview` regime distinct from Fast3R dense sequential | deterministic fallback | `tests/test_vggt_integration.py`; `DEC-20260523-002` closes contract/adapter surface; backend reports `fallback` until checkpoint authorization | real VGGT checkpoint load + server tick still deferred to future A2-style checkpoint DEC |
| STream3R | SRC-2026-001 | causal transformer + session-bounded streaming state | session state ≠ unbounded scene memory (see `literature/CRITICAL_NOTES.md`) | comparator for `build_state_recurrence` choice; W26 design study planned | comparator-only | `SPINE_MEMORY.md` Required Reading entry; not wired | W26 `STREAM3R_RELATION.md` needs drafting before any optional `causal_decoder_adapter.py` |
| SLAM3R | SRC-2024-010 | sliding-window dense SLAM via pointmap prediction + registration | windowed SLAM, not streaming state recurrence | comparator for window-policy under C5 Composer / C4 Critic | comparator-only | `SPINE_MEMORY.md` Advanced not yet; cited in `RU-014/015` | window-policy never benchmarked against Dream3R sliding-window choice |
| MV-DUSt3R+ | SRC-2025-005 | sparse-view pose-free RGB reconstruction; multi-view extension | not streaming | candidate Composer expert (sparse-view regime row) | comparator-only | `SPINE_COMPOSER.md` Required Reading | no adapter; could fill the sparse-view route currently dominated by MASt3R |
| OVGGT | SRC-2026-007 | constant-budget cache compression and dynamic anchor protection on streaming 3R | anchor-cache governance, not full recurrence | comparator for AnchorBank capacity (K=256) + `bus_dynamic_ratio` protection logic | comparator-only | `SPINE_MEMORY.md` Required Reading; explicit comparator pressure here | no AnchorBank-vs-OVGGT direct benchmark; W21 ablation memory variant |
| LongStream | SRC-2026-006 | gauge-decoupled streaming visual geometry + cache refresh | cache-refresh-specific scope | comparator for AnchorBank refresh policy | comparator-only | `SPINE_MEMORY.md` Advanced Reading | not wired |

## Section 3. Memory Primitive Comparators (External Pointer / Hybrid)

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| Point3R | SRC-2025-003 | explicit spatial pointer memory; geometry-indexed external entries | external pointer ≠ hybrid KV+map (Mem3R) ≠ anchor cache (OVGGT) | comparator for `AnchorBank` retrieval policy; no expert adapter | comparator-only | `SPINE_MEMORY.md` Required Reading; `CRITICAL_NOTES.md` deconfusion entry | AnchorBank retrieval never benchmarked vs Point3R primitive |
| Mem3R | SRC-2026-003 | hybrid memory: KV cache for tracking + separate map memory | not equivalent to OVGGT or Point3R primitive | comparator for `AnchorBank` write/merge policy; SPINE_MEMORY required reading | comparator-only | `CASE-20260504-MEMORY-01..03` cycle 010 cards cite Mem3R as comparator | no head-to-head metric; W21 ablation suite plans memory primitive variants |
| LONG3R | SRC-2025-012 | 3D spatio-temporal memory with gating; long-sequence pruning | gating hard-wired, not policy-selected | comparator for `C2 SpatialMemory` write-decision head | comparator-only | `SPINE_MEMORY.md` Required Reading; long-sequence positioning | long-sequence degradation curve missing (Tier 3 in `RECENT_PROGRESS.md`) |
| LoGeR | SRC-2026-002 | chunked long-context reconstruction; TTT global + sliding-window local | hybrid; not decoupled | comparator for hybrid memory axis (distinct from Mem3R's decoupling axis) | comparator-only | `SPINE_MEMORY.md` Required Reading | not wired |
| PAS3R | SRC-2026-004 | pose-adaptive streaming state update | update-gain-specific | comparator for v0.5 long-sequence A1 sub-action choice | comparator-only | `SPINE_MEMORY.md` Required Reading | A1 sub-action selection not implemented |
| FILT3R | SRC-2026-005 | Kalman-style latent filtering for streaming 3R | latent-Kalman, not SLAM-Kalman | comparator for v0.5 long-sequence A1 sub-action choice | comparator-only | `SPINE_MEMORY.md` Required Reading | same as PAS3R |

## Section 4. Monocular Priors

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| DINOv2 | SRC-2023-002 | self-supervised visual feature backbone | features only; no geometry | C1 `Perceiver` backbone path (`backbone_type="dinov2"`, frozen) | real-wired (no local ckpt); locally falls back to random projection | `tests/test_dinov2_backbone.py` (server-only); `RECENT_PROGRESS.md` Tier 1 | local-machine path requires `timm` or `torch.hub` cache; same blocker as DINOv3 |
| DINOv3 | (no SRC row; emerging family) | next-generation self-supervised visual features | not yet pinned to a specific release | C1 `Perceiver` backbone path (`backbone_type="dinov3"`) | stub | `ARCHITECTURE_V04_STATUS.md` § 1 lists DINOv3-S explicitly as stub; `backend_status["backend"]=="stub"` | concrete release pinning + `load_checkpoint` path; v0.5 spec action — see `specs/SPEC-20260522-001-dream3r-v05-axes.md` |
| MoGe-2 | external (arXiv 2507.02546; not yet in `registry/source_registry.md`) | single-image metric pointmap prior | monocular ⇒ needs multiview consistency check | C5 Composer expert `moge2_adapter`; `method_profiles["moge2"]` | deterministic fallback | `composer_experts/method_profiles.py` `implementation_status="stub"`; no test | adapter `load_checkpoint`; **SRC row needs adding** to `source_registry.md` |
| Depth Anything V2 | SRC-2024-014 | robust monocular depth foundation model; low latency | relative depth ≠ full multiview reconstruction | C5 Composer expert `depthanything_adapter`; `method_profiles["depthanything"]` | deterministic fallback | `composer_experts/method_profiles.py` `implementation_status="stub"` | adapter `load_checkpoint`; Depth Pro / Metric3D v2 left as alternates |
| Depth Pro | SRC-2024-015 | zero-shot metric monocular depth; sharp boundaries | not unified into expert registry | candidate alternate for `depthanything_adapter` slot or new metric-depth expert | comparator-only | `RU-011/015` linked | adapter design |
| Metric3D v2 | SRC-2024-016 | zero-shot metric depth + surface normal | not unified into expert registry | candidate alternate for joint-geometry monocular prior | comparator-only | `RU-006/011` linked | adapter design |

## Section 5. Test-Time Refinement and Critic Mechanisms

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| Test3R | SRC-2025-007 | test-time self-supervised consistency refinement | high latency; selective use | C5 Composer expert `test3r_adapter`; also conceptual analog for C4 Critic-triggered slow verification | deterministic fallback | `composer_experts/method_profiles.py` `implementation_status="stub"`; `SPINE_CRITIC.md` Required Reading | adapter `load_checkpoint`; v0.4 `RepairExecutor` actions 1/2/3 use internal rerun (see `repair.py`) rather than Test3R off-path dispatch — bridging this is a v0.5 axis |
| TTT3R | SRC-2025-004 | test-time update rule for CUT3R recurrent state | per-pair, not long-context | comparator for `RepairExecutor` action 1 (local rerun) | comparator-only | `SPINE_MEMORY.md` Advanced Reading; `SPINE_CRITIC.md` Required Reading | Dream3R `_local_rerun` injects `recommended_action=1` and bumps CR-3 retrieval — not the TTT3R update rule itself; gap is whether this is sufficient |
| tttLRM | SRC-2026-011 | test-time training at long-context / sequence scale | sequence-level drift target != per-pair; real gradient step not implemented yet | C2 Memory A1 action policy scaffold: `MemoryA1Action.TEST_TIME_TRAIN`, `StateUpdatePolicy`, `TTTStateUpdater`, W25 `TTT_PLAN.md` | scaffold | `tests/test_memory_action_policy.py` (14 tests); `DEC-20260523-003` closes policy-scaffold surface | replace scaffold with real TTT gradient step, train policy, and record long-sequence server tick in W25 |
| CTRL | SRC-2025-008 | critic-revision via RL-trained critic | RL training cost | comparator for C4 Critic learning regime (Dream3R Critic is heuristic, not RL-learned) | comparator-only | `SPINE_CRITIC.md` Required Reading; `RU-011` linked | not on near-term roadmap |
| SEAL | SRC-2025-009 | self-edit driven adaptation | LLM-domain mechanism transfer | comparator for v0.5 TTT scope | comparator-only | `RU-012` linked | architecture-transfer only |
| G-CUT3R | SRC-2025-014 | guided CUT3R with depth / calibration / pose priors | needs auxiliary priors at inference | comparator for guided-prior injection at C1 Perceiver | comparator-only | `RU-002/015` linked | guided-prior contract design not started |

## Section 6. Attention / State-Recurrence Mechanisms

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| Native Sparse Attention (NSA) | external (DeepSeek arXiv 2502.11089; not in source_registry.md) | trainable sparse access: compressed + selected + sliding branches | requires careful branch routing; short low-bank windows can correctly suppress sliding | C2 `NSAAttention` (three branches realized as `compressed`, `selected`, `sliding`) | mechanism integrated | `tests/test_nsa_*`; `cycles/CYCLE-20260523-001.md`; 128-window KITTI evidence plus bank ablation | RESOLVED by `DEC-20260523-001`: sliding fires on long sequences/post-saturation; 2-window zero is expected under low bank occupancy |
| Mamba (S6) | SRC-2023-001 | selective state-space sequence modeling, linear-time | Mamba-only vision is not always better (see MambaOut) | `build_state_recurrence(type="mamba_hybrid")` factory in C2; `MemorySSM_v01` hybrid path | mechanism integrated | `tests/test_state_recurrence_factory.py`; `demo_mamba_path` on server; `RECENT_PROGRESS.md` Tier 1 | local fast path uses `mamba_ssm` only when available; `use_fast_path=False` documented; W21 ablation `mamba_hybrid` vs `cross_attention` synthetic-only so far |
| Mamba-2 / SSD | SRC-2024-006 | state-space duality; efficient state layer | architecture-transfer; not 3R-specific | candidate refinement for `build_state_recurrence`; not separately wired | comparator-only | none direct | out of scope until W21 ablation closes cross-attn vs mamba_hybrid |
| VMamba | SRC-2024-007 | 2D selective scan routes | vision-only; not state-recurrence-for-3R | comparator for spatial scan in C1 Perceiver | comparator-only | `RU-009` linked | not on near-term roadmap |
| MambaOut | SRC-2024-008 | negative control: SSM not always needed | claim is dataset-conditional | reference for keeping `cross_attention` fallback alive (not removed) | comparator-only | none direct | informs decision not to drop cross_attention path |
| FlashAttention-3 | external (arXiv 2407.08608) | IO-aware exact attention kernels | implementation-detail, not architecture | optional backend flag for `NSABranch` per `ATTENTION_RESEARCH_MATRIX.md` | comparator-only | none direct | left as later optimization |
| Kimi Linear | external (arXiv 2510.26692) | linear-attention hybrid for long context | architecture-transfer | comparator for `cross_attention` recurrence alternative | comparator-only | listed in `ATTENTION_RESEARCH_MATRIX.md` sources | not wired |

## Section 7. Permanence / Dynamic-Object Comparators

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| MonST3R | SRC-2024-003 | dynamic-video pointmap reconstruction | dynamic pointmap, not object identity | comparator for `Permanence` dynamic-mask logic | comparator-only | `SPINE_PERMANENCE.md` Required Reading; `CASE-20260504-PERMANENCE-01` cycle 010 used MonST3R regime | dynamic_mask currently a proxy (`dynamic_mask_proxy`); promotion to D2 deferred to v0.5 |
| POMATO | SRC-2025-010 | pointmap matching + temporal motion | motion estimation, not permanence | comparator only | comparator-only | `SPINE_PERMANENCE.md` Required Reading | not wired |
| D^2USt3R | SRC-2025-011 | 4D pointmaps for dynamic scenes | 4D pointmap focus | comparator only | comparator-only | `SPINE_PERMANENCE.md` Required Reading | not wired |
| Easi3R | SRC-2025-013 | training-free dynamic adaptation / motion separation | training-free; not learned permanence | comparator for v0.5 permanence axis | comparator-only | `SPINE_PERMANENCE.md` Required Reading | not wired |
| RayMap3R | SRC-2026-008 | inference-time RayMap for dynamic streaming reconstruction | inference-time mechanism | comparator only; verify before any reproduction | comparator-only | `SPINE_PERMANENCE.md` Required Reading | reproduction unverified |
| Julian Ost AAAI-2026 driving permanence | SRC-2026-010 | scene-graph driving generation with explicit object permanence | driving-specific scene graph | positioning anchor + deconfusion target | comparator-only | `CRITICAL_NOTES.md` name-collision entry needed | name-collision deconfusion |
| SAM 2 | SRC-2024-012 | promptable image/video segmentation | not a 3R mechanism per se | candidate input prior for `Permanence` slot masks | comparator-only | `SPINE_PERMANENCE.md` Advanced Reading | prior-injection contract design |
| CoTracker | SRC-2023-003 | joint 2D point tracking in long video | 2D tracking only | candidate input prior for `Permanence` object identity | comparator-only | `SPINE_PERMANENCE.md` Advanced Reading | prior-injection contract design |
| SpatialTracker | SRC-2024-013 | 3D-aware 2D point tracking; V2 unifies track+depth+pose | 3D-aware track only | candidate input prior for `Permanence` 3D motion | comparator-only | `SPINE_PERMANENCE.md` Advanced Reading | prior-injection contract design |
| Slot Attention / ISA reference poses | (no SRC row; foundational) | object-like latent grouping + invariant reference pose | vanilla slots lack frame-to-frame spatial reference | C3 `Permanence` slots with ISA-style reference poses | mechanism integrated | `tests/test_isa_slots.py`, `tests/test_permanence_v2.py` | real object trajectory visualization missing |

## Section 8. Rendering / 4D Targets

| Method | SRC | Core strength | Limitation | Dream3R module that absorbs it | Implementation status | Evidence / test | Remaining gap |
|---|---|---|---|---|---|---|---|
| Splatt3R | SRC-2024-004 | uncalibrated image pairs to 3D Gaussians; Gradio demo | pair-only; renderer-tied | candidate input for `GaussianHead` initialization (design only) | contract-only at GaussianHead level | `tests/test_gaussian_render_contract.py` (shape-only) | renderer install (W27) gates real path |
| InstantSplat | SRC-2024-005 | sparse-view SfM-free Gaussian splatting | renderer-tied | candidate input for `GaussianHead` initialization | contract-only | same as Splatt3R | same as Splatt3R |
| NoPoSplat | SRC-2025-006 | sparse unposed images to Gaussians | renderer-tied | candidate input for `GaussianHead` initialization | contract-only | same | same |
| MV-DUSt3R+ (4D usage) | SRC-2025-005 | sparse-view pose-free 4D bridge | listed twice (also Section 2) | candidate Composer expert + GaussianHead input | comparator-only | same | same |
| ActiveSplat | SRC-2024-018 | active mapping + view selection on 3DGS | active-perception domain (deferred branch) | conceptual anchor; out of v0.4 main forward | comparator-only | listed in `BRANCH_COMPARISON_MATRIX.md` Cross-Modal / Active row | branch is `lower-priority reserve` per cycle 008.5 |
| ActiveGS | SRC-2024-019 | active scene reconstruction with Gaussian splatting | active-perception domain | conceptual anchor | comparator-only | same | same |
| AnchorSplat | named in roadmap; **no SRC row** | (per W20 header "3DGS / AnchorSplat") — anchor-attached splat representation | name not pinned to a specific paper/project in `source_registry.md` | conceptual: would map to AnchorBank stable entries with attached Gaussians | named, not in registry | none | **roadmap drafting artifact**: either pin to a specific paper or remove from W20 list |

## Section 9. Methods Named in Roadmap But Not Mapped

| Roadmap name | Status | Investigation needed |
|---|---|---|
| OnlineX | no `SRC-*` row; not in any `SPINE_*.md`; no Dream3R code path | flag as drafting artifact. Either: (a) the roadmap author meant a specific paper (e.g., the "online 3R" family of streaming methods) — needs disambiguation; (b) it is a placeholder for a category already covered by STream3R / OVGGT / LongStream / Spann3R. Do not cite "OnlineX" in any case card or paper draft until resolved. |
| AnchorSplat | see Section 8 row | same flag |

## Cross-Cutting Implementation Status Roll-Up

Counted across Sections 1-8, by status (methods listed in multiple sections counted once):

| Status | Count | Methods |
|---|---:|---|
| real-wired (no local ckpt) | 4 | MASt3R, Fast3R, Spann3R, DINOv2 |
| deterministic fallback | 5 | CUT3R, MoGe-2, Depth Anything V2, Test3R, VGGT |
| stub | 1 | DINOv3 |
| scaffold | 1 | tttLRM-style Memory A1 action policy |
| mechanism integrated | 3 | NSA, Mamba (S6), Slot Attention / ISA |
| contract-only | 1 (family) | 3DGS family (Splatt3R / InstantSplat / NoPoSplat / MV-DUSt3R+) via GaussianHead |
| comparator-only | 23+ | DUSt3R, MASt3R-SfM, STream3R, SLAM3R, MV-DUSt3R+, OVGGT, LongStream, Point3R, Mem3R, LONG3R, LoGeR, PAS3R, FILT3R, Depth Pro, Metric3D v2, TTT3R, CTRL, SEAL, G-CUT3R, Mamba-2/SSD, VMamba, MambaOut, FlashAttention-3, Kimi Linear, MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R, SAM 2, CoTracker, SpatialTracker, Julian Ost AAAI-2026, ActiveSplat, ActiveGS |
| named, not in registry | 2 | OnlineX, AnchorSplat |

C5 Composer's eight expert adapters (MASt3R, Fast3R, Spann3R, CUT3R, MoGe-2, Depth Anything V2, Test3R, VGGT) are exactly the eight registered by `ExpertRegistry.register_all_defaults`; v0.5 `ComposerDecision.backend_status` reports the real/fallback/stub label per adapter at forward time.

## Gap Report (what this matrix exposes for the next planning round)

1. **Composer adapter checkpoint gap**: 5 of 8 adapters are deterministic-fallback locally (CUT3R, MoGe-2, Depth Anything V2, Test3R, VGGT). MASt3R, Fast3R, and Spann3R have real loader paths; Fast3R is additionally blocked by `omegaconf` in the dream3r conda env. Closing the remaining real-checkpoint gap is gated by F-002 server authorization + per-adapter `load_checkpoint`.
2. **VGGT structural gap - RESOLVED (DEC-20260523-002)**: VGGT now has a Composer adapter and a distinct `feed_forward_manyview` capability-card v2.2 row. The remaining VGGT gap is checkpoint authorization / real inference, not schema fit.
3. **DINOv3 stub is the only true stub**: the v0.4 `Perceiver.backbone_status` honestly returns `backend="stub"` when DINOv3 is requested. v0.5 spec must pin a concrete release.
4. **3DGS contract-only is deliberate, not a gap**: per agent prompt + W27. Do not promote in v0.5 without a renderer-install DEC and a license audit (see `R-4DGS-LIC-1` in `WORK_RISK_REGISTER.md`).
5. **Memory comparators (Point3R / Mem3R / LONG3R / LoGeR / PAS3R / FILT3R / OVGGT / LongStream / SLAM3R) never benchmarked**: W21 ablation suite was designed to cover memory-primitive variants; the table column would otherwise stay empty.
6. **"OnlineX" and "AnchorSplat" should be resolved or removed**: as named, they are roadmap drafting artifacts. They are noted here as a flag to the W20 author rather than silently ignored.
7. **NSA sliding branch — RESOLVED (DEC-20260523-001)**: 2-window KITTI smoke showed sliding-branch weight 0.000; this was the correct sparse-routing decision under low bank occupancy. 128-window long-sequence evaluation confirms sliding fires at 100% rate (weight ~28%) once bank saturates (K=256, by window 12). No code change needed. See `cycles/CYCLE-20260523-001.md` for full evidence.
8. **Permanence dynamic mask is proxy, not D2**: v0.5 A3 has started locally by adding optional `dynamic_mask_final` alongside `dynamic_mask_proxy` and making CR-2 prefer final then fall back to proxy. This is not an A3 closure: no D2 promotion criterion or real-data validation exists yet.
9. **Test3R as Critic-triggered off-path**: the v0.4 `RepairExecutor` actions 1/2 use internal rerun (model.forward with bus-injected `recommended_action`). Test3R-as-an-actual-off-path is wired only through Composer dispatch, never triggered by Critic. This is a design choice, not an oversight; v0.5 may revisit.
10. **A8 Memory A1 policy scaffold - RESOLVED at scaffold level (DEC-20260523-003)**: `memory_action.py` adds six A1 sub-actions plus `StateUpdatePolicy` and `TTTStateUpdater`. Real tttLRM gradient-step training and long-sequence server evidence are deferred to W25.
11. **MoGe-2 SRC row missing**: present in `method_profiles.py` but not in `source_registry.md`. Inventory hygiene action.

## Dream3R Differentiation

This restates the 2026-05-10 first-pass differentiation list, with v0.4/v0.5 layer additions appended:

1. A 3R reconstruction path produces pointmap, confidence, and evidence tokens (C1 → C5).
2. Active state tokens evolve per streaming window (C2 + `build_state_recurrence`).
3. Stable AnchorBank stores spatial anchors with payloads (`anchor_bank.py`, K=256 default).
4. NSA fuses active state, selected stable anchors, and sliding recent context (`nsa_attention.py`).
5. Critic checks geometric consistency and emits repair actions (Sampson / depth / covisibility).
6. Permanence tracks object slots with reference poses (`Permanence` + ISA).
7. ComposerRouter exposes external 3R methods as routeable expert capabilities (8 adapters registered, including VGGT).
8. Mamba recurrence can replace cross-attention recurrence without changing the rest of the control graph (`build_state_recurrence(type=...)`).
9. GaussianHead defines the future renderable representation contract — explicitly NOT in the v0.4 main forward.
10. **(v0.4)** `RepairExecutor` closes critic → rerun feedback loop with bounded re-attempts (`max_repair_attempts` default 1).
11. **(v0.4)** Typed `ReconstructionOutput` aggregate contract; every submodule has its own typed output dataclass; backend honesty enforced via `backend_status` labels.
12. **(v0.4)** Reroute path (`action=3 / reroute_hint=True`) picks `route_recommendation[:, 1]` without rerunning the model.
13. **(v0.5 A4)** capability_card v2.2 separates `feed_forward_manyview` from dense sequential routing so VGGT can be represented honestly.
14. **(v0.5 A8)** Memory A1 sub-action selection now has a typed scaffold for future trained long-context updates.
15. **(Stage 4 entry)** ComposerRouter `confidence_gate` is now a regime-aware MLP (`Linear(1+n_regimes, d_routing) -> GELU -> Linear(d_routing, d_routing)`) instead of the previous global `Linear(1, d_routing)`. The old gate could not represent per-regime routing flips because per-sample gradients on its shared weight cancelled exactly. The new gate consumes `[critic_confidence, regime_probs]` and lets training produce different `conf_mod` directions per regime. Backward-compatible `load_state_dict` migrates legacy checkpoints by dropping the untrained legacy gate keys.

## Evidence Map

Preserved from the 2026-05-10 first pass and extended with v0.4/v0.5 entries:

| Claim | Current Evidence |
|---|---|
| Control graph is runnable | `smoke_test`, full `dream3r.tests.test_*` (130 passing in v0.4 round) |
| Mamba path is real | `demo_mamba_path`, `test_state_recurrence_factory` |
| NSA can be ablated | `ablate_recurrence` with `no_nsa` variant |
| Stable memory can be ablated | `ablate_recurrence` with `no_stable_memory` variant |
| Geometric Critic works | `test_geometric_critic`, `test_critic_loop` |
| Slot reference poses work | `test_isa_slots` |
| Expert adapters are represented | `test_composer_experts`, integration tests |
| 3DGS path is bounded | `test_gaussian_head_contract` |
| Real RGB/depth sequence can execute | `evaluate_real_sequence`, `test_kitti_loader_contract`, `test_real_sequence_eval_contract` |
| **(v0.4)** Critic → rerun feedback loop is real | `test_repair_executor_contract.py` (action 1/2 actually rerun; action 3 does not) |
| **(v0.4)** `max_repair_attempts` cap is enforced | `test_repair_executor_does_not_loop_forever_when_actions_persist` |
| **(v0.4)** Composer dispatch flows into final output | `test_expert_output_replaces_perception_pointmap_in_final_output` |
| **(v0.4)** Reroute changes selected expert | `test_reroute_hint_changes_selected_expert` |
| **(v0.4)** Memory → Critic cross-module read | `test_contract_log_records_cross_module_reads` |
| **(v0.5 A4)** VGGT adapter + capability_card v2.2 | `test_vggt_integration.py`, `DEC-20260523-002` |
| **(v0.5 A6)** NSA sliding branch fires on long sequences | `cycles/CYCLE-20260523-001.md`, `DEC-20260523-001` |
| **(v0.5 A8)** Memory A1 action policy scaffold exists | `test_memory_action_policy.py`, `planning/TTT_PLAN.md`, `DEC-20260523-003` |
| **(Stage 4)** Critic + Repair closes on real KITTI pipeline ablation | `cycles/CYCLE-20260525-stage4-closure.md`, `decisions/DEC-20260525-001-stage4-critic-closure.md`, `stage4_repair_pipeline_ablation/results.json` (`critic_changed_route_count=1`, `t4_3=true`) |
| **(Stage 5 S1)** Three-real-expert Composer ablation | `cycles/CYCLE-20260525-stage5-s1-three-expert.md`, `decisions/DEC-20260525-002-stage5-s1-three-expert-closure.md`, `stage5_s1_router_ablation/results.json` (`relative_improvement_vs_best_single=0.0962807369`, `stage5_s1=true`) and strengthened `results_regime_stats.json` (`relative_improvement_vs_best_single=0.1412896043`, `learned_uses_ge_3_experts=true`, `stage5_s1=true`) |

## Missing Evidence

The following must not be overclaimed yet — preserved from 2026-05-10 first pass, augmented:

- Real-data reconstruction quality (Tier 3 per `RECENT_PROGRESS.md`).
- SOTA benchmark ranking.
- Long-sequence stability on real scenes.
- Expert routing quality gains (W23).
- Test-time adaptation gains (W25).
- Renderer-backed Gaussian output (W27).
- Critic threshold calibration on real data (W24).
- Adapter quality comparisons (5 of 8 are deterministic fallback locally).
- VGGT-as-a-real-route with a downloaded checkpoint and server tick (`backend == "real"`).
- **Generalization of richer learned routing**: Stage 5 S1 now has a real three-expert oracle and a strengthened feature-augmented learned-router gain with `learned_uses_ge_3_experts=true`. This is still a 12-window KITTI closure ablation; held-out/cross-dataset router generalization remains missing.

## Related Files

- `code/dream3r/NEXT_PHASE_ROADMAP.md` — W20 origin of this matrix.
- `code/dream3r/ATTENTION_RESEARCH_MATRIX.md` — narrower companion focused on attention / state mechanisms; rows here cross-link.
- `code/dream3r/ARCHITECTURE_V04_STATUS.md` — the per-axis v0.4 closure checklist this matrix cross-links.
- `code/dream3r/composer_experts/method_profiles.py` — canonical 8-expert profile table.
- `registry/source_registry.md` — `SRC-*` IDs cited above.
- `literature/SPINE_*.md` — required vs advanced reading per finalist.
- `units/REPRODUCTION_READINESS_MATRIX.md` — reproduction-readiness layer (separate axis from the mapping here).
- `planning/WORK_RISK_REGISTER.md` — `R-4DGS-LIC-1`, `R-EXT-PRIOR-1` row references.
- `specs/SPEC-20260522-001-dream3r-v05-axes.md` — v0.5 axes spec that consumes this matrix's Gap Report.

## Update Discipline

This file is amended, not silently rewritten:

- A new external method moves from `comparator-only` → `deterministic fallback` → `real-wired` only when an actual code path lands; do not promote a row based on intent.
- A row's `Implementation status` cell must match `composer_experts/method_profiles.py` or `ARCHITECTURE_V04_STATUS.md` at all times; if they disagree, this matrix follows code, not intent.
- Removing the `OnlineX` / `AnchorSplat` rows requires either a registry add (with `SRC-*` row) or a roadmap correction; do not silently drop them.
- When a method appears in a `SPINE_*.md` "required reading" list but is NOT yet a row here, add it as `comparator-only` rather than leaving it missing — completeness against literature spine is enforced at update time.
