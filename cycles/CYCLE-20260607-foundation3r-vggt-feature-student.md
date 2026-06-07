# Cycle: Foundation3R VGGT Feature Student

Date: 2026-06-07

## Goal

Advance Foundation3R from scratch image tokens to pretrained VGGT-Omega visual features while keeping the inference contract proposal-free and teacher-free.

## Work Completed

- Added `Foundation3RVGGTFeatureDecoder`.
- Added VGGT-Omega aggregator feature extraction to the dense teacher cache builder.
- Built real 50 KITTI + 50 ETH3D VGGT feature caches on BUAA-Server GPU1.
- Ran failed hybrid-objective control and identified constant-depth collapse.
- Added auto loss-profile routing so `input_mode=vggt_features` defaults to teacher-only distillation.
- Ran 20-epoch teacher-only state/no-state/shuffle controls.

## Results

```text
hybrid 20e:
  state/no-state/shuffle all about KITTI 0.4734 / ETH3D 0.3271

teacher-only 20e:
  state         KITTI 0.3237 / ETH3D 0.1424
  no-state      KITTI 0.3260 / ETH3D 0.1489
  shuffle-state KITTI 0.3246 / ETH3D 0.1330
  dense teacher KITTI 0.3554 / ETH3D 0.0913
```

## Verdict

Experimental-positive for VGGT features, state-causality negative/unclear. This is a real proposal-free feature-student baseline, not a publishable final model.

## Next

Use this lane only for targeted state-modulation and representation experiments. Do not promote unless it beats official release baselines and passes correct/no-state/shuffle controls.

