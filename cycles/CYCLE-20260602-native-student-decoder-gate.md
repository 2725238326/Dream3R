# CYCLE-20260602: native student decoder gate

Date: 2026-06-02
Status: closed; executable native gate, metric-flat versus bounded baseline
Decision: `decisions/DEC-20260602-024-native-student-decoder-gate.md`

## Trigger

The user asked to lock the bounded frozen-StatePrior baseline and push one
high-impact Dream3R architecture gate, preferring native student
decoder/distillation over existing proposal caches and using VGGT-Omega only if
native work blocked.

## Baseline lock

Verified on BUAA-Server:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/
```

| control | KITTI abs_rel | ETH3D abs_rel | temporal / scale reported |
| --- | ---: | ---: | --- |
| frozen_prior_state_seed_7 | 0.1448 | 0.1475 | yes |
| frozen_prior_shuffle_state_seed_7 | 0.1521 | 0.2467 | yes |

## Work completed

1. Added `NativeStudentDecoder` outside frozen core.
2. Added cached-proposal native student trainer with:
   - frozen DEC-019 StatePrior teacher;
   - proposal dropout;
   - supervised abs_rel plus teacher distillation loss;
   - fallback contamination count;
   - state/no-state/shuffle controls;
   - patch-oracle, temporal, and scale metrics.
3. Added `run_native_student_decoder_sweep.sh`.
4. Added targeted unit tests.
5. Synced only new non-core files to BUAA-Server.
6. Ran local tests, server tests, one-epoch smoke, and a 20-epoch seed-7 gate.

## Changed code files

```text
code/dream3r/native_student_decoder.py
code/dream3r/scripts/train_native_student_decoder.py
code/dream3r/scripts/run_native_student_decoder_sweep.sh
code/dream3r/tests/test_native_student_decoder.py
```

No frozen-core file was edited.

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

## Result

| control | KITTI abs_rel | ETH3D abs_rel | fallback contamination |
| --- | ---: | ---: | ---: |
| native student correct-state | 0.1451 | 0.1480 | 0 |
| native student no-state | 0.1557 | 0.1730 | 0 |
| native student shuffle-state | 0.1525 | 0.2468 | 0 |

State causality is preserved, but the native student does not beat the bounded
baseline:

```text
bounded baseline: 0.1448 / 0.1475
native gate20:    0.1451 / 0.1480
```

## Conclusion

The architecture claim advanced from "native distillation plan" to "executable
native student/distillation gate with server controls." It did not advance the
best-model metric claim. The current best bounded model remains the frozen
StatePrior fusion plus disagreement-bounded residual refinement.

## Next executable gate

Do not reopen residual-head micro-sweeps. The next native gate should modify
the objective, not just capacity:

```text
add dropout-consistency and/or temporal/scale state-projection objectives,
then rerun the same state/no-state/shuffle controls against the locked
0.1448 / 0.1475 bounded baseline.
```
