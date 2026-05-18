# Minimal Demo Candidates

Last updated: 2026-05-01

The first teacher demo does not need to prove the final paper. It should prove:

```text
We are building a new 3R research direction, and it already has a visible working surface.
```

## Demo 1: Dream Research Lane in KYKT

What the teacher sees:

- A KYKT panel listing ranked Dream research ideas.
- Each idea has evidence, source links, bottleneck, smallest experiment, and status.

Claim it supports:

- The project is now a research workbench, not just a runner UI.

Real vs mock:

- Real: source map, idea bank, scoring.
- Mock: backend automation if not wired.

Smallest path:

- Static JSON/TS config rendered in Overview or new Dream page.

Risk:

- Less visually stunning unless paired with model outputs.

KYKT architecture impact:

- Medium if adding a page; low if Overview panel only.

Decision:

- Good management-area seed.

## Demo 2: 3R Composer Controller

What the teacher sees:

- Upload/select an input sample.
- KYKT recommends model path: MASt3R / MonST3R / Fast3R / Spann3R / CUT3R.
- Shows why: input type, expected bottleneck, model status, existing evidence.

Claim it supports:

- A research system can compose multiple 3R models rather than betting on one.

Real vs mock:

- Real: model catalog, sample manifest, job history.
- Mock/early: learned controller; start with rule-based controller.

Smallest path:

- Add rule-based recommendation panel using existing KYKT metadata.

Risk:

- Could look like product logic, not architecture.

KYKT architecture impact:

- Low to medium.

Decision:

- Best first demo candidate.

## Demo 3: Test-Time Geometry Self-Check Report

What the teacher sees:

- A difficult sample is flagged.
- Report shows pair/triplet consistency issue.
- System proposes extra compute: retry, Test3R-like consistency, model switch, or confidence warning.

Claim it supports:

- 3R should reason at test time, not only run one forward pass.

Real vs mock:

- Real possible with existing outputs and simple consistency proxies.
- Full Test3R integration can come later.

Smallest path:

- Generate a diagnostic report from existing scene_meta, confidence, poses, and sample type.

Risk:

- Need avoid claiming actual correction before implemented.

KYKT architecture impact:

- Low. Fits Advisor/JobDetail.

Decision:

- Strong second demo, pairs well with Composer.

## Demo 4: Streaming Memory Visualization

What the teacher sees:

- A video stream enters a state-memory timeline.
- Frames with high pose novelty update memory strongly; redundant/low-confidence frames update weakly.
- The interface explains "geometry-gated memory update."

Claim it supports:

- Dream's architecture thesis: future 3R is about spatial memory update, not only pointmap prediction.

Real vs mock:

- Mock initially.
- Real signals can be estimated from existing pose/confidence after model outputs exist.

Smallest path:

- Build a visualization over existing MonST3R/Fast3R/Spann3R outputs.

Risk:

- If too mock-heavy, may feel conceptual.

KYKT architecture impact:

- Medium.

Decision:

- Best architecture-explainer demo.

## Demo 5: 3R-to-4DGS Asset Bridge

What the teacher sees:

- A video or result becomes an interactive 4D/3D asset pathway.
- The app explains how 3R pointmaps/poses initialize dynamic Gaussians.

Claim it supports:

- 3R can feed asset-generation and spatial-world pipelines.

Real vs mock:

- Real requires a chosen 4DGS repo and data path.
- Early version may be workflow/asset preview only.

Smallest path:

- Use existing GLB/PLY outputs and outline future Gaussian conversion.

Risk:

- More engineering-heavy and may drift away from architecture-first.

KYKT architecture impact:

- Medium to high.

Decision:

- Defer until first research map and composer/self-check demos are grounded.

## Demo 6: Pose-Free Gaussian Quick Win

What the teacher sees:

- A small set of uncalibrated images becomes an interactive Gaussian/novel-view result.
- The app frames this as "3R geometry becomes an inspectable visual asset."

Candidate sources:

- Splatt3R
- InstantSplat
- NoPoSplat
- MV-DUSt3R+

Claim it supports:

- The KYKT workbench can move from reconstruction research to visually compelling spatial assets.

Real vs mock:

- Real if one repo installs and runs with official sample/checkpoint.
- Mock only if shown as planned lane.

Smallest path:

- Try Splatt3R official demo first because it has a direct Gradio path and pretrained checkpoint.
- Keep MV-DUSt3R+ as a geometry-first alternative.
- Keep InstantSplat as the higher-visual-quality but heavier path.
- If setup is too heavy, use screenshots/project outputs as source-map evidence and do not claim local reproduction.

Risk:

- It may look like adopting another demo rather than creating a new architecture.

KYKT architecture impact:

- Medium if adding viewer support; low if initially only a research lane entry.

Decision:

- Strong first visual proof candidate, especially paired with Composer/Self-Check.
- Current tentative ordering: Splatt3R -> MV-DUSt3R+ -> InstantSplat -> NoPoSplat.

## Current Demo Recommendation

Do not pick one final demo yet. The likely first combined demo is:

```text
Dream Research Lane + 3R Composer Controller + Pose-Free Gaussian Quick Win
```

This is feasible, visible, and tied to the architecture story:

```text
Current 3R models have complementary failure modes.
Dream studies the state/update/reasoning mechanisms needed to unify them, while KYKT makes the results visible.
```

## Demo 7: Long-Context Hybrid Memory Benchmark

What the teacher sees:

- A small leaderboard / diagnostic matrix comparing long-sequence failure modes:
  - drift
  - forgetting
  - memory saturation
  - dynamic interference
  - compute growth

Candidate sources:

- CUT3R
- Point3R
- STream3R
- TTT3R
- LoGeR
- Mem3R
- PAS3R

Claim it supports:

- Dream is not only collecting papers. It is building a benchmark surface that can reveal why a new memory/update architecture is needed.

Real vs mock:

- Real at the metadata and literature-result level immediately.
- Real with local outputs after runners are integrated.

Smallest path:

- Create a static benchmark spec and fill it with published/project-page evidence plus KYKT local job availability.

Risk:

- A benchmark alone is not the final paper; it must feed an architecture decision.

Decision:

- Strong management-area seed for the Dream workspace.

## Demo 8: Dynamic State Split

What the teacher sees:

- A dynamic video is explained as three update channels:
  - static map write
  - dynamic motion field
  - suppressed / uncertain regions

Candidate sources:

- MonST3R
- POMATO
- D^2USt3R
- RayMap3R

Claim it supports:

- Dynamic reconstruction should not force every pixel into one persistent scene state.

Real vs mock:

- Initially schematic plus source-linked examples.
- Later can use MonST3R/RayMap3R-style outputs if runners become available.

Smallest path:

- Add dynamic/static update policy visualization to the Dream research lane.

Risk:

- Real dynamic model integration may be heavier than static 3R demos.

Decision:

- Good second-stage architecture explainer, not first demo.
