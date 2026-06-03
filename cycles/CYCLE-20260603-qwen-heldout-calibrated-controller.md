# Cycle 20260603: Qwen Held-Out Calibrated Controller

Date: 2026-06-03
Status: closed diagnostic-negative; not promotable
Decision: `decisions/DEC-20260603-033-qwen-heldout-calibrated-controller.md`

## Goal

Test whether Qwen3-VL-2B-Instruct semantic features contain a held-out
controller signal after the DEC-032 v2 repair, without hand-tuning deterministic
rules on the same 50 windows.

## Actions

1. Added a standalone calibrated controller evaluator:

```text
code/dream3r/scripts/eval_vlm_calibrated_controller.py
```

2. Added integration coverage:

```text
test_vlm_calibrated_controller_uses_heldout_groups_and_controls
```

3. Evaluator design:

```text
split: leave-one-KITTI-drive/group-out
train fold: oracle labels fit nearest-centroid semantic prototypes
held-out fold: cached VLM features only
variants: vlm_real, vlm_shuffle, vlm_disabled
```

4. Re-ran local and BUAA-Server verification.

5. Ran the evaluator on the DEC-032 real Qwen v2 50-window cache.

## Verification

Local:

```text
10 passed
```

Server:

```text
10 passed
```

Held-out calibrated result:

```text
n_windows: 50
n_groups: 27
split_strategy: leave_one_group_out
oracle_mean: 0.1489
default_expert_mean: 0.2365
vlm_real:     0.1813
vlm_shuffle:  0.1776
vlm_disabled: 0.2365
real_beats_disabled: true
real_beats_shuffle: false
promotable: false
```

Detailed counts:

```text
vlm_real counts:     fast3r=16, mast3r=21, spann3r=13; oracle accuracy=0.44
vlm_shuffle counts:  fast3r=11, mast3r=33, spann3r=6;  oracle accuracy=0.44
vlm_disabled counts: fast3r=50, mast3r=0,  spann3r=0;  oracle accuracy=0.08
```

Artifact:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/calibrated_controller_50win_t320_v2.json
```

## Boundary

No frozen-core edits, no geometry use from Qwen, no Router/Critic training, and
no model inference rerun in this cycle.

## Next

Do not promote the current Qwen cache into Router/Critic. Keep it as an offline
diagnostic/cache lane. Future Qwen work needs broader windows and a
pre-registered real > shuffle > disabled promotion threshold before any
training claim.
