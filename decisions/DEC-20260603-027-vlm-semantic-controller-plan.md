# DEC-20260603-027: VLM semantic-controller research plan

Date: 2026-06-03
Status: accepted as research plan; implementation gated
Scope: Dream3R V11 controller research

## Context

The current bounded usable baseline is frozen-StatePrior plus bounded residual:

```text
KITTI/ETH3D: 0.1448/0.1475
```

Recent high-impact architecture gates did not produce a usable native model:

- native student decoder is executable and state-causal, but flat;
- image-state U1 is negative because correct-state loses to no-state;
- VGGT-Omega admission is blocked on the approved checkpoint.

The user asked whether a small open VLM such as Qwen can optimize the controller
and then selected Qwen3-VL-2B-Instruct for deeper consideration.

## Decision

Adopt a V11 research lane:

```text
Qwen3-VL-2B-Instruct as offline semantic support signal
  -> Router / Critic / Dream state auxiliary supervision / teacher scheduler
```

The VLM is not a geometry model. It must not be treated as a pointmap, depth,
camera, or ground-truth teacher source. Its first valid role is strict JSON
semantic risk labeling over existing windows.

Primary planning artifact:

```text
planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
```

New-agent handoff:

```text
handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
```

Cycle log:

```text
cycles/CYCLE-20260603-vlm-semantic-controller-plan.md
```

## Architecture boundary

V11 is allowed to influence:

- `ComposerRouter` feature inputs;
- Critic trigger thresholds;
- expensive teacher admission scheduling;
- optional auxiliary state supervision after offline label quality is proven.

V11 is not allowed to:

- replace proposal teachers or state-conditioned geometry;
- rerun U1 unchanged;
- edit frozen core files without a new explicit DEC;
- download checkpoints, mutate environments, or start training as part of this
  documentation pass;
- claim Dream3R is usable beyond the locked bounded baseline.

## First executable gate

The next implementation pass should create an offline label-cache builder:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
```

It should support:

- strict schema validation;
- explicit failure records;
- prompt hash and model id metadata;
- a mock backend for local tests;
- a Qwen backend only when weights and dependencies are available.

No VLM signal should enter training before a schema and repeatability smoke pass.

## Promotion rule

V11 can advance only if at least one gate passes:

- VLM-augmented Router beats current robust-stat Router on held-out or
  cross-domain route regret, and shuffled VLM labels are worse;
- VLM-augmented Critic improves hard-window trigger precision/recall or
  compute-quality tradeoff, with geometry confirmation;
- VLM auxiliary state supervision beats no-state, shuffle-state, and the
  locked 0.1448/0.1475 baseline;
- VLM teacher scheduler spends heavy teacher budget on windows that actually
  improve downstream quality.

## Rejected alternatives

| Alternative | Rejection reason |
| --- | --- |
| Use Qwen as direct depth/camera/pointmap teacher | Violates geometry evidence boundary and would create prose-to-geometry hallucination risk |
| Put online VLM calls into the model loop first | Too slow and difficult to debug; offline cache must prove value first |
| Add another residual-head micro-sweep | User explicitly asked for broader research direction and the V10 prompt already redirected away from micro-sweeps |
| Rerun U1 with more epochs only | U1 correct-state loses to no-state; epoch-only rerun does not address causal failure |

## Evidence label

Official Qwen capability evidence is source-observed from official Qwen GitHub
and Hugging Face model card. Dream3R benefit remains a testable hypothesis until
Router/Critic/state gates pass.
