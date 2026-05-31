# CYCLE-20260601 — Frozen-prior decoder sweep

date: 2026-06-01
status: closed; scaffold-positive
decision: `decisions/DEC-20260601-021-frozen-prior-decoder-sweep.md`

## Trigger

The user asked to continue. DEC-020 closed the joint prior-conditioned decoder
as negative, but its follow-up smoke showed that loading and freezing the
DEC-019 StatePrior checkpoint preserves the positive signal. The next concrete
step is to run that frozen-prior path as a controlled sweep.

## Actions

1. Confirmed current state from `TASK_SNAPSHOT.md` / `WORKFLOW_STATUS.md`.
2. Started `run_frozen_prior_decoder_sweep.sh` on BUAA-Server GPU 1.
3. The first epoch of `frozen_prior_state_seed_7` reproduced StatePrior quality.
4. Closed both correct-state and shuffle-state controls.
5. Ran a lower-KL sensitivity probe with `PRIOR_KL_WEIGHT=0.01`.

## Server Run

```text
root:   /hdd3/kykt26/code/dream3r
out:    runs/stage6_fusion/frozen_prior_decoder_sweep/
script: dream3r/scripts/run_frozen_prior_decoder_sweep.sh
gpu:    CUDA_VISIBLE_DEVICES=1
```

Controls:

```text
frozen_prior_state_seed_7
frozen_prior_shuffle_state_seed_7
```

## Result

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| frozen-prior correct-state | 0.1452 | +4.68 pp | 0.1480 | +6.64 pp |
| frozen-prior shuffle-state | 0.1525 | -0.11 pp | 0.2468 | -55.75 pp |

Correct-state beats shuffle-state on both domains and preserves DEC-019
StatePrior quality.

## Boundary

No core edit, cache rebuild, checkpoint download, environment mutation, or new
expert admission.

## Conclusion

This is scaffold-positive: frozen StatePrior prevents the joint-decoder collapse
from DEC-020 and keeps state causality, but it does not improve beyond
StatePriorHead. Next work should add bounded refinement on top of the frozen
prior, with improvement gates against both StatePrior and shuffle-state.

## KL Sensitivity

```text
runs/stage6_fusion/frozen_prior_decoder_kl001_sweep/
```

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| frozen-prior correct-state, KL=0.01 | 0.1451 | +4.76 pp | 0.1480 | +6.64 pp |
| frozen-prior shuffle-state, KL=0.01 | 0.1525 | -0.11 pp | 0.2468 | -55.75 pp |

Lower KL keeps the same scaffold behavior. It does not create refinement gain.
