# Dream3R milestone reorganization — model-first roadmap

date: 2026-05-30
status: active milestone plan
decision: `decisions/DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md`
spec: `specs/SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md`

## Why this milestone exists

The project cannot keep drifting between "router", "fusion head", "memory",
and "new expert search". The next phase must produce a coherent 3R model.

The corrected model identity:

```text
Dream3R is a state-conditioned 3R reconstruction model.
External 3R systems are proposal encoders.
Dream3R owns the state and reconstruction decoder.
```

## Current milestone state

Completed:

- L0 real-backend guardrail fixed fallback contamination.
- L1 single-expert residual correction failed and is rejected.
- L2 SCF works as bounded state-conditioned fusion.
- 4-seed ver2.1 controls show correct state beats no-state and shuffled-state
  on KITTI/ETH3D abs_rel and patch-oracle gap.

Still open:

- state is not yet trained as geometry state;
- temporal/scale metrics are not yet improved;
- current expert bank has only 3 real proposals;
- Dream3R still needs a clearer reconstruction-decoder path toward native
  inference.

## Expert selection

Do not add experts because they are popular. Add only if they fill a missing
regime in the current proposal bank.

| priority | candidate | reason | immediate action |
| --- | --- | --- | --- |
| P0 keep | MASt3R | static/pairwise high-quality proposal | keep as core bank |
| P0 keep | Fast3R | many-view fast proposal | keep as core bank |
| P0 keep | Spann3R | memory-like/global-coordinate proposal | keep as core bank |
| P1 add | VGGT-Omega | upgraded VGGT-family feed-forward geometry foundation, distinct output signals | write admission contract; checkpoint gated |
| P1 add | CUT3R | persistent-state continuous 3D, aligns with Dream3R memory thesis | write admission contract; checkpoint gated |
| P1 add | MonST3R | dynamic pointmap proposal, tests Permanence/Critic | write admission contract; checkpoint gated |
| P2 watch | STream3R / InfiniteVGGT | long-stream causal/VGGT-family comparators | use as design pressure, not immediate integration |
| P2 watch | vanilla VGGT / OVGGT | vanilla VGGT is baseline; OVGGT is cache-memory comparator | do not confuse either with VGGT-Omega admission |
| P2 watch | Test3R / TTT3R | slow verification / test-time teacher | keep off default proposal path |
| P3 defer | 3DGS family | rendering/output target | defer until pointmap model is stable |

## What we create ourselves

The Dream3R-owned invention should be the reconstruction decoder:

```text
State-Conditioned Reconstruction Decoder
```

Minimum useful version:

```text
proposal tokens + Dream state tokens -> bounded final pointmap
```

It should optimize:

- scale-aligned abs_rel;
- patch-oracle gap;
- temporal delta;
- scale drift;
- proposal reliability calibration.

## High-speed task ladder

### Task A — presentation-safe model package

Output:

```text
one figure + one table + one paragraph:
Dream3R = proposal encoders + Dream state + reconstruction decoder
```

Use current numbers only. Do not claim SOTA.

### Task B — v2.2 admission plan

Output:

```text
adapter/cache/eval contract for VGGT-Omega, CUT3R, MonST3R
```

No checkpoint download. No model run. The purpose is to make the next server
run surgical.

### Task C — non-core decoder prototype

Output:

```text
ProposalSetDecoder prototype trained from existing caches
```

Start with existing 3-expert caches. Only after it beats SCFHead should the
expert bank expand.

### Task D — trained-state gate

Output:

```text
state projection / Critic calibration experiment
```

Pass condition:

```text
trained-state > current-state > no-state / shuffled-state
and temporal/scale proxies do not degrade
```

### Task E — native model path

Output:

```text
distillation plan: proposal-bank teacher -> native Dream3R decoder
```

This is the real path toward "a 3R model" rather than a permanent ensemble.

## Stop rules

- Stop adding experts if patch-oracle ceiling does not improve.
- Stop training a decoder if no-state catches correct-state.
- Stop claiming memory if temporal/scale does not improve.
- Stop any route that requires core edits before a DEC names the exact files
  and why non-core alternatives are insufficient.

## Immediate next handoff

Use `handoff/ARCHITECTURE_V07_MODEL_REORG_AGENT_PROMPT.md`.
