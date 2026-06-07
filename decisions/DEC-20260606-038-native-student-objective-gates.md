# DEC-20260606-038: Native student objective gates

Date: 2026-06-06
Status: accepted; implemented but release-negative
Scope: Dream3R native student optimization

## Context

The current release candidate remains:

```text
frozen StatePrior + bounded residual refinement
KITTI / ETH3D abs-rel: 0.1448 / 0.1475
```

The native student decoder was already causal but flat:

```text
correct-state: 0.1451 / 0.1480
no-state:      0.1557 / 0.1730
shuffle-state: 0.1525 / 0.2468
```

The nearest reversible optimization was objective-level strengthening, not a
new geometry module.

## Decision

Add optional native-student objective terms:

```text
dropout-consistency loss
temporal proxy loss
scale-drift proxy loss
```

All new weights default to `0.0`, preserving existing behavior unless the sweep
opts in.

## Implementation

Updated:

```text
code/dream3r/scripts/train_native_student_decoder.py
code/dream3r/scripts/run_native_student_decoder_sweep.sh
code/dream3r/tests/test_native_student_decoder.py
```

New trainer flags:

```text
--dropout-consistency-weight
--temporal-loss-weight
--scale-drift-loss-weight
```

The dropout-consistency target is detached. Temporal and scale losses are
differentiable proxy terms over adjacent-frame aligned depth and median-scale
drift.

## Verification

Local:

```text
python -B -m pytest --assert=plain code/dream3r/tests/test_native_student_decoder.py -q
# 5 passed

python -B -m py_compile code/dream3r/scripts/train_native_student_decoder.py code/dream3r/native_student_decoder.py
# passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B -m pytest --assert=plain \
  dream3r/tests/test_native_student_decoder.py -q
# 5 passed
```

All GPU runs used BUAA-Server GPU1.

## Gate Results

### P1: Dropout consistency

Command shape:

```text
CUDA_VISIBLE_DEVICES=1
OUT=runs/stage6_fusion/native_student_dropout_consistency_gate20_seed7
EPOCHS=20
DROPOUT_CONSISTENCY_WEIGHT=0.25
PROPOSAL_DROPOUT=0.35
```

Results:

| Control | KITTI | ETH3D | fallback |
| --- | ---: | ---: | ---: |
| correct-state | 0.1451 | 0.1480 | 0 |
| no-state | 0.1557 | 0.1730 | 0 |
| shuffle-state | 0.1525 | 0.2468 | 0 |

### P2: Dropout consistency + temporal/scale proxy

Command shape:

```text
CUDA_VISIBLE_DEVICES=1
OUT=runs/stage6_fusion/native_student_temporal_scale_gate20_seed7
EPOCHS=20
DROPOUT_CONSISTENCY_WEIGHT=0.25
TEMPORAL_LOSS_WEIGHT=0.05
SCALE_DRIFT_LOSS_WEIGHT=0.05
PROPOSAL_DROPOUT=0.35
```

Results:

| Control | KITTI | ETH3D | fallback |
| --- | ---: | ---: | ---: |
| correct-state | 0.1451 | 0.1480 | 0 |
| no-state | 0.1557 | 0.1730 | 0 |
| shuffle-state | 0.1525 | 0.2468 | 0 |

Correct-state remains better than no-state/shuffle but does not beat the
selected RC.

## Verdict

The native student objective patches are valid and reversible, but they are not
promotable:

```text
RC:              0.1448 / 0.1475
native P1/P2:    0.1451 / 0.1480
```

Stop repeating small objective-weight sweeps on this same trainer. Future model
improvement needs a larger bounded change, such as a domain-conditional
VGGT-Omega teacher policy or a stronger native target, while the current
publishable path remains the frozen-StatePrior bounded baseline.
