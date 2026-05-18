# Dream Phase 1 Execution Log

Last updated: 2026-05-01

## 2026-05-01 Run 1

Status:

```text
Phase 1 comprehensive research started.
```

User instruction:

- start broad research
- do not end prematurely
- use gpt-5.4-mini subagents for assistance

Subagents launched:

1. Direct 3R / visual geometry frontier researcher.
2. Architecture-transfer researcher.
3. Demo enabler / KYKT integration researcher.

Main-controller actions:

- began online verification of primary sources
- created initial source map
- created initial research unit bank
- created initial idea scoreboard
- created initial minimal demo candidate memo

Important early signal:

```text
The 2025-2026 3R frontier is moving strongly toward streaming/state/memory/test-time update.
```

Implication:

- Memory/State 3R is likely the strongest architecture-first axis.
- Composer and Test-Time Compute are likely the best near-term demo axes.
- Cross-modal/event/4DGS should remain as demo and robustness enablers, not yet the core thesis.

Resolved / pending:

- reproduction-readiness subagent result: completed and merged
- first readiness table: completed in `units/REPRODUCTION_READINESS_MATRIX.md`
- master prompt: completed in `AGENT_MASTER_PROMPT.md`
- still pending: user discussion before Phase 2 implementation commitment

## Subagent Merge 1: Demo / KYKT Integration

Merged from demo-enabler researcher.

Important additions:

- Splatt3R and InstantSplat are strong short-term teacher-demo candidates.
- MV-DUSt3R+ is relevant for pose-free multi-view reconstruction.
- GS-CPR is a bridge from MASt3R/SfM to 3DGS refinement.
- Heavy dynamic 4DGS repos should not be the first demo unless the setup is already controlled.
- Event-camera routes are valuable but likely too hardware/data-heavy for first demo.

Current implication:

```text
First visible demo should likely combine:
  Dream research lane + 3R composer/controller + a pose-free GS visual path.
```

## Subagent Merge 2: Direct 3R Frontier

Merged from direct-3R frontier researcher.

Important additions:

- The 2024-2026 3R field separates into three visible lines:
  - matching / scale: DUSt3R -> MASt3R -> Fast3R -> MASt3R-SfM
  - state / streaming: CUT3R -> Spann3R -> Point3R -> STream3R -> TTT3R -> LoGeR / Mem3R / PAS3R
  - dynamic / 4D: MonST3R -> POMATO -> D^2USt3R -> RayMap3R
- The direct frontier is converging on memory capacity, drift control, dynamic/static separation, and test-time adaptation.
- A publishable Dream direction should not claim "we discovered memory"; it must specify a better memory carrier, update law, reset/evict rule, and verification loop.

Current implication:

```text
The strongest architecture-first thesis is:
  geometry-governed state and memory control for streaming/dynamic 3R.
```

## Subagent Merge 3: Architecture Transfer

Merged from architecture-transfer researcher.

Important additions:

- Mamba/SSM contributes useful operators, not a complete answer:
  - route scan
  - persistent state
  - global-local hybrid
  - latent compression
  - critic-revision
  - self-edit update
- MambaOut is an important negative control: SSM is not automatically valuable for all vision tasks. It is most defensible when the 3R task is long-sequence, streaming, or autoregressive.
- The best Dream framing is not "Mamba-3R replaces Transformer"; it is "3R needs explicit policies for route, write, compress, revise, and adapt."

Current implication:

```text
Dream should evaluate mechanisms by whether they change the 3R computation graph:
  route -> encode -> state write -> memory query -> geometry critic -> local revision.
```

## Subagent Merge 4: Reproduction Readiness

Status:

```text
Completed and merged.
```

Scope:

- Splatt3R / MV-DUSt3R+ / InstantSplat / NoPoSplat
- Fast3R / MonST3R / DUSt3R / MASt3R / CUT3R
- Point3R / STream3R / TTT3R / RayMap3R / LoGeR / Mem3R

Question:

```text
Which repo is the best Phase 2 smoke-test and KYKT demo candidate when license, checkpoint availability, dependency risk, and teacher-facing value are considered together?
```

Result:

```text
Recommended first reproduction set:
  Splatt3R + DUSt3R + InstantSplat

Next tier:
  MASt3R + MV-DUSt3R+ + Fast3R + CUT3R

Defer:
  NoPoSplat for lack of public UI,
  Point3R / STream3R / TTT3R for research comparators,
  RayMap3R / LoGeR / Mem3R until release surface is clearer.
```

Controller correction:

- Keep DUSt3R as the safest baseline smoke test.
- Keep Splatt3R as the first visual surprise smoke test.
- Keep InstantSplat as a promising permissive-license Gaussian path, but expect heavier setup.
