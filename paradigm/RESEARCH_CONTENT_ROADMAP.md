# Dream Research Content Roadmap

Last updated: 2026-05-01

Status: active.

## Purpose

This document keeps Dream focused on its mainline:

```text
new 3R / spatial-intelligence research content first;
backend, KYKT app, and frontend only as supporting layers.
```

The objective is not to build an app feature first. The objective is to discover, validate, and present a direction that can surprise the teacher and later become a paper/proposal/demo foundation.

## Mainline Question

Dream should repeatedly ask:

```text
What new mechanism can change the 3R field's handling of long-context, dynamic, difficult, or uncertain spatial reconstruction?
```

Every serious idea should answer:

- what is new against current 3R models
- which bottleneck it attacks
- what mathematical or architectural intuition makes it plausible
- what evidence can be gathered cheaply
- what teacher-facing demonstration would make the idea visible
- how KYKT could eventually carry the workflow

## Active Research Axes

### Axis A: Geometry-Governed State 3R

Core question:

```text
Can a 3R model maintain long-horizon spatial state with explicit geometric write/read/forget rules instead of relying on full attention or opaque recurrent memory?
```

Useful mechanisms:

- SSM / Mamba-style selective state
- route-scan policies over frames, views, or spatial regions
- external sparse spatial memory
- uncertainty-gated memory writes
- dynamic/static separation before state consolidation

### Axis B: Test-Time Geometry Reasoning

Core question:

```text
Can a 3R model spend more inference compute on hard views by testing and revising geometric hypotheses?
```

Useful mechanisms:

- geometry critic
- loop consistency checks
- pose/pointmap hypothesis revision
- adaptive compute budgets
- TTT / test-time adaptation without uncontrolled drift

### Axis C: 3R Composer

Core question:

```text
Can we turn the fragmented 3R ecosystem into a regime-aware system that routes inputs to the right model, checker, memory, or asset generator?
```

Useful mechanisms:

- model capability cards
- failure-mode routing
- shared pointmap / camera / confidence contract
- comparison reports
- teacher-facing visual explanation of why one model path was chosen

### Axis D: Continual / Lifelong 3R

Core question:

```text
Can 3R reconstruction become a persistent learner over scenes instead of a one-shot predictor?
```

Useful mechanisms:

- adapter updates
- scene memory consolidation
- anti-forgetting constraints
- replay from sparse geometry state
- uncertainty-aware online update policies

### Axis E: Cross-Modal / 4D Extensions

Core question:

```text
Can sensors or 4D asset representations solve specific 3R failure modes rather than merely add novelty?
```

Useful mechanisms:

- event-camera blur-free motion cues
- IMU/depth/LiDAR priors
- 4D Gaussian Splatting initialized from 3R outputs
- continuous-time dynamic fields
- physical priors for non-rigid motion

## Near-Term Research Cycles

### Cycle 1: Dream3R Thesis Stress Test

Goal:

- define exactly what is new in `Dream3R`
- compare against CUT3R, Point3R, STream3R, TTT3R, LoGeR, Mem3R, and adjacent systems
- separate paper-grade claims from demo-grade claims

Outputs:

- novelty comparison table
- updated Research Units
- decision memo: keep, split, rename, or defer Dream3R

### Cycle 2: Mechanism Mining Beyond 3R

Goal:

- mine recent architecture, RL, continual learning, and vision work for mechanisms that can be translated into 3R

Outputs:

- 10-20 candidate mechanisms
- 3-6 accepted Research Units
- evidence labels for each mechanism

### Cycle 3: Teacher Surprise Story

Goal:

- turn the strongest research content into a 5-8 minute teacher-facing narrative

Outputs:

- storyboard
- claim/evidence/risk table
- demo candidate choice

### Cycle 4: Support Contract

Goal:

- define backend/data contracts only after the research content needs durable system support

Outputs:

- source/RU/decision/experiment schema
- lifecycle states
- artifact links
- API/task boundary draft

### Cycle 5: Planned Experiment

Goal:

- prepare the smallest evidence path without heavy reproduction unless approved

Outputs:

- experiment plan
- success criteria
- stop conditions
- approval checklist

## Priority Rule

When there is tension between research content and system implementation:

```text
Research content wins unless the user explicitly asks to implement the system layer.
```

Backend work is justified when it preserves or operationalizes research decisions.
Frontend work is justified when it presents an already-shaped research workflow.
App integration is valuable, but it must follow the research.
