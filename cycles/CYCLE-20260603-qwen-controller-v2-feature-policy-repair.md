# Cycle 20260603: Qwen Controller V2 Feature/Policy Repair

Date: 2026-06-03
Status: closed weak-positive; not promotable
Decision: `decisions/DEC-20260603-032-qwen-controller-v2-feature-policy-repair.md`

## Goal

Repair the DEC-031 failure where strict Qwen labels existed but the controller
surface collapsed to Fast3R-only routing.

## Actions

1. Inspected DEC-031 Qwen records.

Finding:

```text
visible_failure_causes carried signal:
  occlusion=22, low_texture=17, dynamic=6, repeated_structure=3
risk_* numeric fields were mostly all zero.
suggest_verify_geometry was true for 50/50.
```

2. Patched feature extraction:

```text
visible_failure_causes -> matching risk_* feature floor
```

3. Patched deterministic policy:

```text
dynamic -> Spann3R
low_texture/reflection/repeated_structure/occlusion -> MASt3R
large_baseline/road fallback -> Fast3R
```

4. Added tests for cause-derived risk features and occlusion-before-road
routing.

5. Re-ran Qwen3-VL-2B-Instruct on the same 50 oracle-aligned KITTI windows with
the tightened prompt on BUAA-Server GPU1.

## Verification

Local:

```text
9 passed
```

Server:

```text
9 passed
```

DEC-031 cache re-evaluated with v2 features:

```text
oracle_mean: 0.1489
vlm_real:    0.1700
vlm_shuffle: 0.1721
vlm_disabled:0.2365
```

Fresh v2 Qwen run:

```text
schema_pass_rate: 1.0
valid_records: 50
failure_records: 0
oracle_mean: 0.1489
vlm_real:    0.1750
vlm_shuffle: 0.1759
vlm_disabled:0.2365
promotable: false
```

Detailed v2 dry-run:

```text
vlm_real expert counts: fast3r=7, mast3r=33, spann3r=10
vlm_shuffle counts:     fast3r=7, mast3r=33, spann3r=10
vlm_disabled counts:    fast3r=50, mast3r=0, spann3r=0
hard-window PR real:    precision=0.773, recall=0.895
hard-window PR shuffle: precision=0.727, recall=0.842
```

## Boundary

This is still a dry-run. No Router/Critic training, no core edit, and no Qwen
geometry claim.

## Next

Do not keep hand-tuning deterministic rules against the same 50-window set.
The next meaningful Qwen gate should be a held-out calibrated or learned
controller using these semantic features, with real/shuffle/disabled controls
and a promotion threshold set before training.
