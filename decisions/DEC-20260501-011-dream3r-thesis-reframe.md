# DEC-20260501-011: Dream3R Thesis Reframe

Date: 2026-05-01

scope:

```text
thesis candidate / research direction
```

decision:

```text
Reframe Dream3R from a generic geometry-gated state idea toward an executive-memory thesis.
```

status:

```text
proposed candidate branch, not final
```

## Context

The user asked to begin research and clarified that the mainline is new research content, not app or backend work.

The first research-content cycle compared the current Dream3R candidate against recent 2025-2026 work in long-context 3R and visual geometry.

## Evidence

Recent work already covers many pieces of the original Dream3R framing:

- [CUT3R](https://arxiv.org/abs/2501.12387): persistent state for continuous 3D perception.
- [STream3R](https://arxiv.org/abs/2508.10893): causal Transformer formulation for sequential 3D reconstruction.
- [LONG3R](https://arxiv.org/abs/2507.18255): recurrent long-sequence reconstruction with memory gating and 3D spatio-temporal memory.
- [LoGeR](https://arxiv.org/abs/2603.03269): hybrid memory with TTT global memory plus sliding-window attention.
- [Mem3R](https://arxiv.org/abs/2604.07279): tracking/mapping memory decoupling and TTT fast-weight memory.
- [PAS3R](https://arxiv.org/abs/2603.21436): pose-adaptive state updates.
- [FILT3R](https://arxiv.org/abs/2603.18493): Kalman-style latent filtering for streaming 3R.
- [LongStream](https://arxiv.org/abs/2602.13172): gauge-decoupled long-stream visual geometry and cache refresh.
- [OVGGT](https://arxiv.org/abs/2603.05959): constant-cost cache compression and dynamic anchor protection.

Inference:

```text
A single state-space, cache, memory, or test-time update mechanism is unlikely to be enough for a surprising thesis.
```

## Options

### Option A: Keep Dream3R As Geometry-Gated State-Space 3R

Pros:

- simple story
- close to original Mamba/SSM direction

Cons:

- overlaps heavily with PAS3R, FILT3R, LONG3R, and OVGGT-style updates
- risks becoming a minor update rule rather than a new direction

### Option B: Reframe As GEM-3R

Working name:

```text
GEM-3R: Geometry-Governed Executive Memory for 3R
```

Pros:

- turns many frontier papers into comparators and components
- makes the novelty a policy/control layer rather than one memory mechanism
- can produce a teacher-facing demo without training first
- keeps state, memory, critic, dynamic, and cache ideas connected

Cons:

- broader and harder to formalize
- must avoid looking like only an engineering controller
- needs a clear proxy benchmark and eventual model-level experiment

### Option C: Delay Reframing

Pros:

- keeps options open

Cons:

- wastes research time under a weaker thesis name
- makes later literature comparison harder

## Recommendation

Keep Option B as one strong research branch, without finalizing the name.

Recommended working thesis:

```text
Long-context 3R requires a geometry-governed executive memory layer
that chooses when to write, preserve, compress, evict, verify, revise, or adapt spatial state.
```

## Risks

- Novelty risk: LoGeR / Mem3R / OVGGT already cover strong memory/cache ideas.
- Scope risk: an executive controller can become too broad.
- Evidence risk: without at least proxy experiments, the thesis remains speculative.
- Engineering risk: full model training is expensive and should not be started yet.

## User Approval Required

Approval is required before:

- finalizing `GEM-3R` as the project name
- selecting it as the primary thesis
- starting reproduction or implementation
- claiming teacher-demo readiness

No approval is required for:

- writing the mechanism spec
- updating research units and scoreboards
- drafting proxy benchmark plans

## Next Action

Superseded by DEC-20260502-001 before deepening.

Current next action:

```text
Compare GEM-3R with other candidate branches before creating a full mechanism spec.
```

Former proposed mechanism spec:

```text
GEM-3R state variables
GEM-3R geometry evidence vector
GEM-3R action set
GEM-3R controller policy
GEM-3R proxy benchmark
```
