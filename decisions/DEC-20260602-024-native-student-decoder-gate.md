# DEC-20260602-024: Native student decoder/distillation gate

Date: 2026-06-02
Status: accepted; executable gate closed flat versus bounded baseline
Scope: Dream3R native decoder/distillation over existing proposal caches

## Context

DEC-023 redirected the next execution pass away from residual-head micro-sweeps
and toward a high-impact architecture gate:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded fusion/refinement baseline
-> native student decoder/distillation candidate
```

The locked bounded baseline is:

| control | KITTI abs_rel | ETH3D abs_rel |
| --- | ---: | ---: |
| bounded frozen-StatePrior refinement | 0.1448 | 0.1475 |
| bounded shuffle-state refinement | 0.1521 | 0.2467 |

## Decision

Add a non-core native student decoder gate:

```text
code/dream3r/native_student_decoder.py
code/dream3r/scripts/train_native_student_decoder.py
code/dream3r/scripts/run_native_student_decoder_sweep.sh
code/dream3r/tests/test_native_student_decoder.py
```

The gate loads the DEC-019 StatePrior checkpoint as a frozen teacher, trains a
compact native residual over cached proposal teachers, and uses proposal
dropout during training so the student is not only an all-teacher convex copier.

## Allowed

- Use existing SCF proposal caches only.
- Use the existing DEC-019 StatePrior checkpoint.
- Train non-core native student decoder parameters.
- Run bounded seed-7 state/no-state/shuffle controls on BUAA-Server GPU1.

## Forbidden

- Frozen-core edits.
- Cache rebuild.
- Checkpoint download.
- Environment mutation.
- New expert admission.
- Promoting the native student as the current best model unless it beats the
  bounded frozen-StatePrior refinement baseline.

## Verification

Local:

```text
python -B -m py_compile code/dream3r/native_student_decoder.py \
  code/dream3r/scripts/train_native_student_decoder.py \
  code/dream3r/tests/test_native_student_decoder.py

python -B -m pytest code/dream3r/tests/test_native_student_decoder.py \
  code/dream3r/tests/test_proposal_set_decoder.py \
  code/dream3r/tests/test_state_prior_head.py -q
# 11 passed
```

Server:

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
conda run --no-capture-output -n dream3r \
  python -B -m pytest dream3r/tests/test_native_student_decoder.py -q
# 3 passed
```

Smoke:

```text
CUDA_VISIBLE_DEVICES=1 \
OUT=runs/stage6_fusion/native_student_decoder_smoke_seed7 \
EPOCHS=1 \
bash dream3r/scripts/run_native_student_decoder_sweep.sh
```

Gate:

```text
CUDA_VISIBLE_DEVICES=1 \
OUT=runs/stage6_fusion/native_student_decoder_gate20_seed7 \
EPOCHS=20 \
bash dream3r/scripts/run_native_student_decoder_sweep.sh
```

## Seed-7 gate result

Server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/native_student_decoder_gate20_seed7/
```

| control | KITTI abs_rel | ETH3D abs_rel | fallback contamination |
| --- | ---: | ---: | ---: |
| native student correct-state | 0.1451 | 0.1480 | 0 |
| native student no-state | 0.1557 | 0.1730 | 0 |
| native student shuffle-state | 0.1525 | 0.2468 | 0 |

The native student preserves state causality:

```text
correct-state beats no-state and shuffle-state on KITTI/ETH3D.
```

It does not beat the locked bounded baseline:

```text
bounded baseline: 0.1448 / 0.1475
native gate20:    0.1451 / 0.1480
```

## Consequence

This is a successful architecture gate scaffold, not a model-quality promotion.
Dream3R now has a native student/distillation execution surface with proposal
dropout, frozen-StatePrior teacher control, state/no-state/shuffle controls,
temporal and scale proxies, and fallback contamination reporting.

The current best bounded Dream3R variant remains:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded convex fusion
-> disagreement-bounded residual refinement
```

The next single executable gate should change the native objective rather than
repeat small residual variants: add an explicit dropout-consistency metric/loss
or train the state projection against temporal/scale proxies, then rerun the
same state/no-state/shuffle controls.
