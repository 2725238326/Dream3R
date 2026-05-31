# CYCLE-20260601 — Bounded prior refinement

date: 2026-06-01
status: closed; small-positive
decision: `decisions/DEC-20260601-022-bounded-prior-refinement.md`

## Trigger

The user asked to continue and emphasized that the architecture needs serious
work. DEC-021 closed frozen-prior fusion as scaffold-positive but not improved
beyond StatePriorHead, so the next bounded step is residual refinement over the
frozen prior.

## Actions

1. Added zero-initialized bounded residual refinement to
   `ProposalSetDecoder`.
2. Added `--residual-refine-scale` to `train_proposal_set_decoder.py`.
3. Wired `RESIDUAL_REFINE_SCALE` into `run_frozen_prior_decoder_sweep.sh`.
4. Extended unit tests for zero initialization and residual bound.
5. Synced changed files to BUAA-Server.
6. Ran server py_compile and 1-epoch smoke.
7. Ran seed-7 correct/shuffle controls with
   `RESIDUAL_REFINE_SCALE=0.05`.

## Verification

Local:

```text
python -B -m pytest code/dream3r/tests/test_proposal_set_decoder.py \
  code/dream3r/tests/test_state_prior_head.py -q
8 passed
```

Server smoke:

```text
runs/stage6_fusion/bounded_refine_smoke_seed7
KITTI: Ours_ProposalSetDecoder 0.1451 vs best_single 0.1523
ETH3D: Ours_ProposalSetDecoder 0.1475 vs best_single 0.1585
```

## Server Run

```text
root:   /hdd3/kykt26/code/dream3r
out:    runs/stage6_fusion/bounded_refine_sweep/
script: dream3r/scripts/run_frozen_prior_decoder_sweep.sh
gpu:    CUDA_VISIBLE_DEVICES=1
env:    RESIDUAL_REFINE_SCALE=0.05 PRIOR_KL_WEIGHT=0.1
```

Controls:

```text
frozen_prior_state_seed_7
frozen_prior_shuffle_state_seed_7
```

## Boundary

No core edit, cache rebuild, checkpoint download, environment mutation, or new
expert admission.

## Result

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| bounded-refine correct-state | 0.1448 | +4.93 pp | 0.1475 | +6.94 pp |
| bounded-refine shuffle-state | 0.1521 | +0.13 pp | 0.2467 | -55.68 pp |

Frozen-prior baseline from DEC-021:

```text
KITTI 0.1452, ETH3D 0.1480
```

## Conclusion

Small-positive. The bounded residual refinement beats frozen-prior on KITTI and
ETH3D and keeps shuffle-state clearly worse, especially on ETH3D. The gain is
small, so this should be reported as a bounded refinement over the load-bearing
StatePrior, not as proof that the full ProposalSetDecoder is solved.
