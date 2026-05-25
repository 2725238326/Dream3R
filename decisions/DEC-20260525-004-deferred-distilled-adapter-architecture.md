# DEC-20260525-004 - Deferred Distilled Adapter Architecture

## Status

Deferred. Not implemented. Recorded as future work.

## Context

In the Stage 5 S1 expanded-closure discussion (2026-05-25), user proposed
replacing the current "Router → load full expert model → forward" runtime
flow with a distilled-adapter architecture:

- A shared 3D backbone (e.g., DINOv3) runs once per input.
- Each real expert model (MASt3R, Spann3R, Fast3R, plus future additions)
  is distilled into a lightweight adapter (~30 MB) that lives on top of the
  shared backbone.
- The Router picks an adapter instead of a full model. Teacher (full) models
  exist only at training time and are dropped at deployment.

The user explicitly framed it as "router uses the model's strength region,
not the whole model loaded full-size."

## Decision

Defer this architecture. Continue Stage 5 with the current "Router → full
real model" design.

## Rationale

### 1. The pain point this architecture solves is not yet active

Current inference holds three real models in GPU memory: MASt3R 1.2 GB +
Spann3R 0.7 GB + Fast3R 1.0 GB = ~3 GB on a 24 GB TITAN RTX. Per-window
forward is in the 100-300 ms range, which is fine for offline KITTI
evaluation. The "must distill to save memory / speed" trigger is not active.

### 2. The engineering cost is large and the failure mode is bad

The distillation path requires:

- Teacher pointmap caching at scale (extend KITTI oracle from 59 to
  200-500 windows, plus ETH3D, plus any future dataset).
- Three independent adapter distillation runs, each with its own
  data scope decision (oracle-winner-only vs full data vs weighted).
- Router retraining against adapter outputs (the output distribution differs
  from full-model output, so transfer is not automatic).
- Critic recalibration: the existing Stage 4 critic was trained on
  full-model pointmaps; adapter outputs may shift the conflict_score
  distribution.
- Cross-dataset distilled adapter validation: a KITTI-distilled MASt3R
  adapter may be worse than the actual MASt3R on ETH3D.

If any link breaks, the existing closure (DEC-20260525-003) is at risk of
regression. The current Router → full model design has no such fragility.

### 3. Project goal is demo, not unified architecture

`mainwork.md §0` reads: "default goal: working demo (option 2) — end-to-end
KITTI, real pointmap, single-creative-point ablation. Not SOTA, every number
real." Stage 5 S1 expanded closure already meets that bar (78% hold-out
route accuracy on 59 KITTI windows). The remaining gap to a complete demo
story is cross-dataset evidence (ETH3D), not architectural unification.

### 4. The distilled-adapter narrative is a separate paper

If the team later targets a conference submission, the distilled-adapter
design is a strong second contribution that can be carried by its own
distillation paper or a follow-up. It does not need to be entangled with
the multi-expert routing closure that Stage 5 S1 is delivering.

## Trigger Conditions

Switch to distilled-adapter architecture when ANY of the following becomes
true, not before:

1. **GPU memory becomes the binding constraint.** Adding a 4th or 5th real
   expert (VGGT ~4 GB, CUT3R, etc.) drives total full-model footprint
   beyond 16-18 GB on a single 24 GB GPU.
2. **Inference latency becomes the binding constraint.** A real-time demo,
   live viewer, or 30+ FPS streaming target requires per-window forward
   under 50 ms.
3. **Conference-paper SOTA pursuit.** A submission target that requires a
   "unified 3D model" narrative rather than "expert routing" narrative.

Until one of these fires, the Router → full real model design is the
correct engineering choice for this project.

## What Is Preserved For Future Pickup

When the trigger fires, the future agent should be able to start without
re-litigating this discussion:

- Architecture sketch (in CYCLE-20260525-stage5-s1-three-expert.md follow-up
  conversation 2026-05-25): shared backbone + per-expert lightweight adapter
  + Router picks adapter.
- Distillation data scope decision: "oracle-winner-only" was proposed. Risk:
  Fast3R has only 4 wins in 59-window oracle, so data extension to 200-500
  windows is a prerequisite.
- Training schedule sketch: (0) freeze design, (1) teacher pointmap cache,
  (2) per-adapter distillation, (3) router retrain, (4) critic recalibrate,
  (5) cross-dataset validation.
- Risk register: distillation accuracy loss, oracle data insufficiency for
  rare-winner models, cross-dataset distilled-adapter degradation.

## Boundary

This decision changes nothing in code. Server artifacts, checkpoints, and
docs from DEC-20260525-001 through DEC-20260525-003 remain authoritative.
