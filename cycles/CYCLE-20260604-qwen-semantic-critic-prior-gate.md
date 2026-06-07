# Cycle 20260604: Qwen Semantic Critic-Prior Gate

Date: 2026-06-04
Status: closed diagnostic-negative; not promotable
Decision: `decisions/DEC-20260604-034-qwen-semantic-critic-prior-gate.md`

## Goal

Test the user's narrower hypothesis: Qwen semantics may still assist Critic
verification triggers even if direct expert routing failed.

## Actions

1. Added a non-core evaluator:

```text
code/dream3r/scripts/eval_vlm_semantic_critic_gate.py
```

2. Added integration coverage proving the intended behavior on a synthetic
case: real semantics can improve a geometry trigger, while shuffle/disabled do
not.

3. Synchronized the new script/test to BUAA-Server and ran the gate on the
server-side Qwen v2 50-window cache.

## Verification

Local:

```text
11 passed
```

Server:

```text
11 passed
```

Server artifact:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/semantic_critic_gate_50win_t320_v2.json
```

Result:

```text
geometry_only F1:            0.9211
vlm_real_qwen_only F1:       0.7632
vlm_real_plus_geometry F1:   0.8947
vlm_shuffle_plus_geometry F1:0.8421
vlm_disabled_plus_geometry F1:0.9211
promotable: false
```

## Boundary

No Qwen model inference was run in this cycle; the script consumed the existing
server Qwen cache. No frozen-core edits, no Critic training, and no geometry
claim from Qwen.

## Next

Do not keep trying to promote the current Qwen 50-window cache. The productive
architecture path returns to teacher/proposal-bank admission, especially
VGGT-Omega checkpoint admission, or to building a real Critic/proposal-
disagreement cache before re-testing semantic priors.
