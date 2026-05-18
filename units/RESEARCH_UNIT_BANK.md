# Research Unit Bank

Last updated: 2026-05-04 (cycle 008.5 appended decision line on RU-002 promoting to `spec_drafted`)

This is an initial bank. Scores and decisions may change after subagent outputs are merged.

## RU-001: Geometry-Gated State-Space 3R

Idea name: Geometry-Gated State-Space 3R

Source:

- [Mamba](https://arxiv.org/abs/2312.00752)
- [CUT3R](https://cut3r.github.io/)
- [PAS3R](https://arxiv.org/abs/2603.21436)
- [LONG3R](https://arxiv.org/abs/2507.18255)

Borrowed mechanism:

- Selective state update from SSM/Mamba.
- Persistent 3R state from CUT3R.
- Pose/motion-aware update from PAS3R.
- Long-sequence memory gating from LONG3R.

3R bottleneck:

- Long video reconstruction cannot rely on full attention or naive recurrent memory without drift/forgetting.

Architecture hypothesis:

```text
Replace temporal attention with a geometry-gated selective state update. The gate is conditioned on reprojection residual, confidence, dynamic mask, baseline / pose novelty, and loop-consistency.
```

Smallest experiment:

- Build a non-trained mock/controller around existing outputs: compute frame importance and simulate state update weights on existing KYKT jobs.
- Later test by modifying a lightweight temporal fusion module, not full pretraining.

Teacher demo form:

- Streaming memory visualization: frames enter, state cells update only when geometric novelty is high.

KYKT integration surface:

- Research lane + Sample Matrix evidence + possible future runner.

Evidence level:

- Level 1 now; Level 2 possible using existing jobs; Level 3 requires prototype.

Engineering cost:

- Medium if mock/controller; high if real model training.

Risks:

- Could duplicate existing 2026 streaming 3R if not positioned carefully.
- Need prove "geometry-gated" differs from pose-adaptive/state memory baselines.

Decision:

- Architecture candidate. Keep high priority but do not implement until source map is complete.

## RU-002: 3R Composer Controller

Idea name: 3R Composer Controller

Source:

- Existing KYKT route: MASt3R, MonST3R, Spann3R, Fast3R, CUT3R
- [Test3R](https://arxiv.org/abs/2506.13750)

Borrowed mechanism:

- Route by input regime and failure mode.
- Compare and select outputs based on confidence, artifact completeness, geometry consistency, and runtime.

3R bottleneck:

- No single 3R model dominates across static pair, multiview, long collections, dynamic videos, streaming inputs.

Architecture hypothesis:

```text
A lightweight controller can turn multiple 3R models into a stronger system by selecting, comparing, and validating model-specific outputs under a unified scene_meta contract.
```

Smallest experiment:

- Use KYKT job history and model catalog to create a controller report: recommended model per sample type and failure mode.

Teacher demo form:

- App panel: "Given this input, Dream chooses Fast3R/MonST3R/Spann3R because..."

KYKT integration surface:

- Overview research lane, Create guidance, Sample Matrix, Advisor.

Evidence level:

- Level 2 possible immediately from existing KYKT smoke jobs.

Engineering cost:

- Low to medium.

Risks:

- Less architecture-novel if only routing.
- Needs later transition into distillation/fusion or test-time checking to become paper-grade.

Decision:

- Best near-term demo candidate.
- 2026-05-04 (cycle 008.5): promoted to `spec_drafted` and linked to `specs/SPEC-20260504-001-3r-composer.md` (Composer finalist owns A5 routing facet; primary proxy P5 + capability_match; cross-spec contract with Critic A5 formalized in `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`). Per DEC-20260504-002, Composer is not the thesis spine; it is one of four parallel finalists. Next action is `CASE-20260505-COMPOSER-01..03` in cycle 009.

## RU-003: Test-Time Geometry Self-Check

Idea name: Test-Time Geometry Self-Check

Source:

- [Test3R](https://arxiv.org/abs/2506.13750)
- [TTT3R](https://arxiv.org/abs/2509.26645)
- test-time compute reasoning literature

Borrowed mechanism:

- Test-time optimization using geometric consistency.
- Adaptive compute only for hard cases.

3R bottleneck:

- Feed-forward 3R may fail under occlusion, low overlap, dynamic interference, or inconsistent pairwise pointmaps.

Architecture hypothesis:

```text
The system should allocate extra compute only when confidence/consistency signals indicate a hard geometric case, then run self-check loops over pose/depth/pointmap hypotheses.
```

Smallest experiment:

- Run or emulate consistency checks on triplets from KYKT samples.
- Generate report: original model output, detected inconsistency, suggested retry/model switch.

Teacher demo form:

- "System-2 3R" report showing the model catches its own geometric mistake.

KYKT integration surface:

- Advisor/report lane, JobDetail diagnostics, Sample Matrix quality flags.

Evidence level:

- Level 2 to Level 3 feasible.

Engineering cost:

- Medium if using Test3R code; low if report-only diagnostic.

Risks:

- Could be seen as evaluation layer rather than new model architecture.
- Need tie to adaptive compute / controller for novelty.

Decision:

- Strong demo + research bridge candidate.
- 2026-05-03 (cycle 008): promoted to `spec_drafted` and linked to `specs/SPEC-20260503-001-geometry-critic.md` (Critic finalist owns A4 + A5; primary proxy P1 + P5). Next action is `CASE-20260504-CRITIC-01..03` in cycle 011.

## RU-004: External Sparse Spatial Memory for 3R

Idea name: External Sparse Spatial Memory for 3R

Source:

- [Point3R](https://arxiv.org/abs/2507.02863)
- [Point Cloud Mamba](https://arxiv.org/abs/2403.00762)
- [RAM-Net](https://arxiv.org/abs/2602.11958)

Borrowed mechanism:

- Spatial pointer memory.
- Point cloud serialization.
- Selectively addressable memory.

3R bottleneck:

- Fixed-size recurrent state cannot literally store an unlimited scene; a realistic system needs external sparse map memory.

Architecture hypothesis:

```text
Separate fixed GPU state from growing scene memory: the model maintains compact recurrent state while writing spatial anchors into an external sparse map indexed by geometry.
```

Smallest experiment:

- Build an external map index over existing pointcloud/pose outputs and show query/update behavior.

Teacher demo form:

- 3D memory map that grows with observations while GPU state remains fixed.

KYKT integration surface:

- Long-term research management area, Sample Matrix, System diagnostics.

Evidence level:

- Level 1-2 now.

Engineering cost:

- Medium.

Risks:

- Needs careful wording: not true O(1) total memory, only O(1) model state.

Decision:

- Important correction to Mamba-3R claims; keep as foundational design rule.

## RU-005: 3R-to-4DGS Initialization Bridge

Idea name: 3R-to-4DGS Initialization Bridge

Source:

- [4D Gaussian Splatting CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/html/Wu_4D_Gaussian_Splatting_for_Real-Time_Dynamic_Scene_Rendering_CVPR_2024_paper.html)
- [4DGS in the Wild](https://arxiv.org/abs/2411.08879)
- MonST3R / Fast3R / Spann3R outputs

Borrowed mechanism:

- Use 3R pointmaps/poses/confidence as initialization for dynamic Gaussian representations.

3R bottleneck:

- 3R outputs are geometrically useful but not always teacher-demo-friendly; 4DGS is visually impressive but often initialization-sensitive.

Architecture hypothesis:

```text
3R can become the geometry initializer for a fast 4D asset pipeline, with confidence-aware Gaussian initialization and dynamic/static separation.
```

Smallest experiment:

- Convert existing pointcloud/pose/dynamic mask outputs into a prototype Gaussian initialization or at least a visual asset pipeline plan.

Teacher demo form:

- "Video -> 3R geometry -> interactive 4D asset" workflow.

KYKT integration surface:

- Output artifact lane, future 4D asset export, teacher demo.

Evidence level:

- Level 1-2 now; Level 3 requires integration with a 4DGS repo.

Engineering cost:

- Medium to high depending on repo choice.

Risks:

- More application/system than architecture unless tied to confidence-aware initialization.

Decision:

- Demo-enabler candidate, not primary thesis yet.

## RU-006: Event-Augmented Pointmap 3R

Idea name: Event-Augmented Pointmap 3R

Source:

- [EAG3R](https://arxiv.org/abs/2512.00771)
- event camera literature

Borrowed mechanism:

- Event/RGB fusion for dynamic/extreme-light geometry.

3R bottleneck:

- RGB-only 3R fails under motion blur, low light, and high-speed dynamics.

Architecture hypothesis:

```text
Asynchronous event streams can act as a temporal geometry correction signal for pointmap models.
```

Smallest experiment:

- Initially survey and reproduce existing EAG3R-style results if code appears.
- Without hardware, use synthetic/event dataset only.

Teacher demo form:

- RGB frame is blurred; event-assisted geometry remains stable.

KYKT integration surface:

- Research lane, not immediate runner unless datasets/code are available.

Evidence level:

- Level 1 now; Level 3 requires event data/code.

Engineering cost:

- Medium to high, hardware-dependent for real demo.

Risks:

- EAG3R already occupies much of this idea. Need avoid duplicate positioning.

Decision:

- Background / robustness enabler for now.

## RU-007: Attention-Residual / KDA 3R Memory Update

Idea name: Attention-Residual / KDA 3R Memory Update

Source:

- [Kimi Linear](https://arxiv.org/abs/2510.26692)
- Moonshot Attention Residuals materials need primary verification

Borrowed mechanism:

- Fine-grained finite-state memory gating and hybrid linear/full attention.
- Potential depth-wise selective reuse of prior representations.

3R bottleneck:

- Streaming 3R needs efficient long-context memory but must retain selective access to important prior views.

Architecture hypothesis:

```text
Use KDA-like finite-state memory for cheap temporal propagation, while retaining sparse full-attention or residual retrieval for keyframes / loop closures.
```

Smallest experiment:

- Compare conceptual memory update designs against Mamba and causal attention in a design memo.

Teacher demo form:

- Architecture diagram showing hybrid finite-state + sparse keyframe attention.

KYKT integration surface:

- Proposal/report lane.

Evidence level:

- Level 1 only.

Engineering cost:

- High if implemented deeply.

Risks:

- Language-model architecture may not transfer cleanly to geometry.
- Need avoid buzzword borrowing.

Decision:

- Speculative architecture candidate; keep for survey.

## RU-008: Pose-Free Gaussian Demo Bridge

Idea name: Pose-Free Gaussian Demo Bridge

Source:

- [Splatt3R](https://github.com/btsmart/splatt3r)
- [InstantSplat](https://github.com/NVlabs/InstantSplat)
- [NoPoSplat](https://github.com/cvg/NoPoSplat)
- [MV-DUSt3R+](https://github.com/facebookresearch/mvdust3r)

Borrowed mechanism:

- Use pose-free / sparse-view reconstruction to directly generate visually inspectable Gaussian assets or geometry.

3R bottleneck:

- Pure pointcloud/PLY outputs are often less impressive to non-specialists than interactive rendered assets.

Architecture hypothesis:

```text
A practical 3R workbench should separate geometry estimation from visual asset generation, while preserving pose-free inputs and unified artifact contracts.
```

Smallest experiment:

- Select one official repo with Gradio/checkpoints and run a known sample.
- Compare against existing KYKT MASt3R/Fast3R output on the same or similar input.

Teacher demo form:

- Upload 2-8 images -> unposed reconstruction -> interactive Gaussian/novel-view output.

KYKT integration surface:

- Output viewer, research lane, future runner profile `pose-free GS`.

Evidence level:

- Level 2-3 if repo setup succeeds.

Engineering cost:

- Medium.

Risks:

- Could drift toward graphics demo rather than architecture research.
- Need keep it framed as "demo/output surface" not final thesis.

Decision:

- Strong short-term demo enabler.

## RU-009: Route-Scan Policy Bank

Idea name: Route-Scan Policy Bank

Source:

- [VMamba](https://arxiv.org/abs/2401.10166)
- [Vision Mamba / Vim](https://arxiv.org/abs/2401.09417)
- [QuadMamba](https://arxiv.org/abs/2410.06806)
- [PointMamba](https://arxiv.org/abs/2402.10739)
- [Mamba2D](https://arxiv.org/abs/2412.16146)

Borrowed mechanism:

- Multiple scan routes over image grids, point clouds, and adaptive partitions.

3R bottleneck:

- A single raster or chronological order is a poor carrier for geometry because 3D neighborhood, epipolar relation, temporal order, and object motion disagree.

Architecture hypothesis:

```text
Streaming 3R should not learn state update over an arbitrary token order. It should select or fuse route policies: image-raster, bidirectional, quadtree, space-filling curve, keyframe-order, and spatial-memory order.
```

Smallest experiment:

- Build a route-policy simulator over existing pointmaps / camera poses.
- Score each route by locality preservation, reprojection-neighbor consistency, and update redundancy.

Teacher demo form:

- Visual panel showing how the same scene is scanned by different route policies and why geometry-aware routes preserve memory better.

KYKT integration surface:

- Dream research lane and future model-architecture visualizer.

Evidence level:

- Level 1 now; Level 2 possible from existing pointcloud / pose outputs.

Engineering cost:

- Low to medium for simulator; high for model integration.

Risks:

- Needs a clear metric; otherwise it becomes a visual explanation rather than research evidence.

Decision:

- Add as an architecture subunit under RU-001.

## RU-010: Hybrid Context Router

Idea name: Hybrid Context Router

Source:

- [MambaVision](https://arxiv.org/abs/2407.08083)
- [Infini-attention](https://arxiv.org/abs/2404.07143)
- [MLLA / MILA](https://arxiv.org/abs/2405.16605)
- [EfficientViM](https://arxiv.org/abs/2411.15241)
- [SparX](https://arxiv.org/abs/2409.09649)

Borrowed mechanism:

- Use cheap local/state layers most of the time, and reserve expensive global mixing for high-value layers or chunks.

3R bottleneck:

- Full attention is too expensive for long videos, but pure recurrent state loses loop closure and far-view constraints.

Architecture hypothesis:

```text
A 3R model should route context by geometric need: local SSM/linear layers for frame-to-frame continuity, sparse global attention for keyframes, loop closure, and inconsistent regions.
```

Smallest experiment:

- Define a rule-based context router using pose novelty, confidence drop, dynamic ratio, and loop-candidate score.

Teacher demo form:

- Timeline that marks which frames get cheap streaming update and which frames trigger global context retrieval.

KYKT integration surface:

- Composer controller and self-check report.

Evidence level:

- Level 1-2 now.

Engineering cost:

- Medium.

Risks:

- Needs separation from ordinary keyframe selection in SLAM; novelty must be about neural context budget.

Decision:

- High-priority design candidate after source-map consolidation.

## RU-011: Geometry Critic-Revision Loop

Idea name: Geometry Critic-Revision Loop

Source:

- [Test3R](https://arxiv.org/abs/2506.13750)
- [TTT3R](https://arxiv.org/abs/2509.26645)
- [CTRL](https://arxiv.org/abs/2502.03492)
- System-2 / test-time compute literature

Borrowed mechanism:

- Train or design a critic that evaluates geometric consistency, then allocates revision compute to failure regions.

3R bottleneck:

- Hard views, occlusion, moving objects, and low overlap break single-pass pointmap predictions.

Architecture hypothesis:

```text
3R inference should be a budgeted loop:
draft pointmaps -> geometry critic -> local hypothesis revision -> accept / escalate.
```

Smallest experiment:

- Implement a non-learned critic report first: depth discontinuity, reprojection residual, confidence conflict, pair/triplet inconsistency.
- Later train a lightweight critic on success/failure labels from KYKT jobs.

Teacher demo form:

- A difficult sample where Dream shows the original reconstruction, the detected geometric conflict, and the chosen repair action.

KYKT integration surface:

- JobDetail diagnostics, Advisor, Dream research lane.

Evidence level:

- Level 2 feasible quickly; Level 3 if Test3R integration succeeds.

Engineering cost:

- Low for report-only; medium for Test3R; high for learned critic.

Risks:

- If no revision is implemented, it is only diagnostics. The second step must perform a concrete retry, model switch, or local optimization.

Decision:

- Merge with RU-003 as the main System-2 direction.
- 2026-05-03 (cycle 008): promoted to `spec_drafted` and linked to `specs/SPEC-20260503-001-geometry-critic.md` jointly with RU-003. Next action is `CASE-20260504-CRITIC-01..03` in cycle 011.

## RU-012: Self-Adapt Adapter for 3R

Idea name: Self-Adapt Adapter for 3R

Source:

- [SEAL](https://arxiv.org/abs/2506.10943)
- [Learning Mamba as a Continual Learner](https://arxiv.org/abs/2412.00776)
- [TTT3R](https://arxiv.org/abs/2509.26645)

Borrowed mechanism:

- Controlled test-time updates through self-edits, adapter deltas, or confidence-derived update rates.

3R bottleneck:

- A fixed 3R model struggles across new camera intrinsics, blur regimes, indoor/outdoor geometry, and long sequences.

Architecture hypothesis:

```text
Instead of full test-time training, 3R should update a narrow adapter/state path whose learning rate and scope are decided by geometry critic signals.
```

Smallest experiment:

- No full training yet. Draft adapter update rules and compare them against TTT3R-style state update in a design memo.

Teacher demo form:

- "The model detects a new scene regime and opens a restricted adaptation budget."

KYKT integration surface:

- Proposal lane first; later runner profile for adaptation experiments.

Evidence level:

- Level 1 now.

Engineering cost:

- Medium to high.

Risks:

- Easy to overclaim. Must not call it online learning unless deployment-time weights or adapter state actually change.

Decision:

- Keep as second-wave research; do not use as first demo.

## RU-013: Dynamic 4D Pointmap Branch

Idea name: Dynamic 4D Pointmap Branch

Source:

- [MonST3R](https://arxiv.org/abs/2410.03825)
- [POMATO](https://arxiv.org/abs/2504.05692)
- [D^2USt3R](https://arxiv.org/abs/2504.06264)
- [MASt3R-SfM](https://arxiv.org/abs/2409.19152)
- [SLAM3R](https://arxiv.org/abs/2412.09401)
- [Easi3R](https://arxiv.org/abs/2503.24391)
- [G-CUT3R](https://arxiv.org/abs/2508.11379)
- [RayMap3R](https://raymap3r.github.io/)

Borrowed mechanism:

- Dynamic pointmaps, temporal motion, 4D pointmap representation, and inference-time dynamic suppression.

3R bottleneck:

- Dynamic objects corrupt static pose/geometry alignment and create temporal flicker.

Architecture hypothesis:

```text
Dynamic 3R should output geometry plus a motion-aware validity field: static structure should update the long-term map; dynamic regions should update a separate short-horizon motion field or be suppressed for camera-state estimation.
```

Smallest experiment:

- Use MonST3R / RayMap3R-style outputs or public examples to classify sample types and show static/dynamic update policies.

Teacher demo form:

- Same video split into static memory update, dynamic object track, and rejected/conflict regions.

KYKT integration surface:

- Dynamic sample lane and future 4D asset bridge.

Evidence level:

- Level 1-2 now.

Engineering cost:

- Medium if using existing outputs; high if training a real 4D model.

Risks:

- POMATO and D^2USt3R already occupy direct dynamic pointmap territory, so Dream must contribute state/memory/reasoning control rather than a generic dynamic pointmap.

Decision:

- Keep as a required comparator branch for any final thesis.
- 2026-05-03 (cycle 008): promoted to `spec_drafted` and linked to `specs/SPEC-20260503-003-dynamic-object-permanence.md` (Permanence finalist owns A6; primary proxy P4 + identity_consistency; 4DGS asset path explicitly out of scope). Next action is `CASE-20260504-PERMANENCE-01..03` in cycle 011.

## RU-014: Long-Context Hybrid Memory Benchmark

Idea name: Long-Context Hybrid Memory Benchmark

Source:

- [LoGeR](https://loger-project.github.io/)
- [Mem3R](https://lck666666.github.io/Mem3R/)
- [Point3R](https://arxiv.org/abs/2507.02863)
- [PAS3R](https://arxiv.org/abs/2603.21436)
- [STream3R](https://arxiv.org/abs/2508.10893)

Borrowed mechanism:

- Chunking, hybrid memory, pointer memory, pose-adaptive update, and causal streaming.

3R bottleneck:

- Long sequences expose drift, memory saturation, and catastrophic forgetting.

Architecture hypothesis:

```text
Before inventing the final architecture, Dream needs a small benchmark harness that measures update policy behavior: drift over time, memory write frequency, re-observation consistency, and dynamic interference.
```

Smallest experiment:

- Create a benchmark spec using public sample videos and existing KYKT outputs.
- Start with metadata/metrics even before running every model locally.

Teacher demo form:

- Leaderboard-style panel: which model fails by drift, forgetting, dynamic interference, or compute blow-up.

KYKT integration surface:

- Dream management area, Sample Matrix, and future automated runner.

Evidence level:

- Level 2 feasible with existing/public results; Level 3 requires local runners.

Engineering cost:

- Medium.

Risks:

- Benchmark work can expand without producing a novel architecture. Keep it as evidence infrastructure, not the thesis itself.

Decision:

- High priority for Phase 2 planning.

## RU-015: Geometry-Governed Executive Memory for 3R

Idea name: Geometry-Governed Executive Memory for 3R

Working title:

```text
GEM-3R: Geometry-Governed Executive Memory for 3R
```

Source:

- [CUT3R](https://arxiv.org/abs/2501.12387)
- [STream3R](https://arxiv.org/abs/2508.10893)
- [LONG3R](https://arxiv.org/abs/2507.18255)
- [LoGeR](https://arxiv.org/abs/2603.03269)
- [Mem3R](https://arxiv.org/abs/2604.07279)
- [PAS3R](https://arxiv.org/abs/2603.21436)
- [FILT3R](https://arxiv.org/abs/2603.18493)
- [LongStream](https://arxiv.org/abs/2602.13172)
- [OVGGT](https://arxiv.org/abs/2603.05959)
- [Point3R](https://arxiv.org/abs/2507.02863)
- [POMATO](https://arxiv.org/abs/2504.05692)
- [D^2USt3R](https://arxiv.org/abs/2504.06264)

Borrowed mechanism:

- Persistent latent state from CUT3R.
- Causal streaming geometry from STream3R / LongStream.
- Hybrid memory from LONG3R / LoGeR / Mem3R.
- Pose-adaptive and Kalman-style update rules from PAS3R / FILT3R.
- Constant-budget cache and anchor protection from OVGGT.
- External spatial pointer memory from Point3R.
- Dynamic/static separation from POMATO / D^2USt3R.
- Matching/SfM and SLAM boundary awareness from MASt3R-SfM / SLAM3R.
- Training-free dynamic correction from Easi3R-style work.
- Guided reconstruction priors from G-CUT3R.

3R bottleneck:

- Long-context 3R now has too many partial memory solutions. The unsolved problem is deciding which state, memory, cache, dynamic, or reasoning action to take under changing geometry.

Architecture hypothesis:

```text
Treat long-context 3R as geometry-governed executive control:
observe -> score geometry evidence -> choose update / memory / cache / critic / dynamic actions -> verify.
```

Smallest experiment:

- No training first.
- Build a mechanism spec and proxy benchmark that simulates actions over existing model outputs or public sample metadata.
- Compare policies: uniform update, pose-adaptive update, Kalman update, anchor-protected cache, external memory write, critic-triggered revision.

Teacher demo form:

- "The 3R model explains what it remembers, forgets, verifies, and repairs" over a long/dynamic video timeline.

KYKT integration surface:

- Dream research lane, future management area, Advisor/report, Sample Matrix, and later backend research contract.

Evidence level:

- Source mechanisms are paper-proven.
- The executive-memory synthesis is inferred.
- Performance benefit is unknown until proxy or reproduction.

Engineering cost:

- Low to medium for mechanism spec and proxy benchmark.
- Medium for non-learned controller report.
- High for learned controller / model integration.

Risks:

- Could be too broad unless the action set and evaluation are precise.
- Must differentiate from LoGeR / Mem3R / OVGGT, which already cover strong memory and cache designs.
- Must differentiate from MASt3R-SfM / SLAM3R by focusing on long-term executive memory rather than ordinary reconstruction pipelines.
- Dynamic-scene claims must target object permanence and memory policy, not merely motion handling.
- Must avoid becoming only an app-level controller.

Decision:

- New top architecture thesis candidate, not final.
- 2026-05-03 (cycle 008): promoted to `spec_drafted` and linked to `specs/SPEC-20260503-002-executive-memory.md` (Memory finalist owns A1 + A2 + A3; primary proxy P2 + P3). Thesis status remains "candidate, not final"; spec drafting does not select the thesis. Next action is `CASE-20260504-MEMORY-01..03` in cycle 011.
