# CYCLE-20260531 — Prior-conditioned ProposalSetDecoder

date: 2026-05-31
status: closed; seed-7 controls negative
decision: `decisions/DEC-20260531-020-prior-conditioned-decoder.md`

## Trigger

DEC-019 showed that Dream state contains useful expert-prior signal, while
ProposalSetDecoder v0/v1 failed to preserve that signal. The next surgical step
is to make the state prior an explicit decoder control branch.

## Actions

1. Added `state_prior_mlp` and `state_prior_weights` output to
   `code/dream3r/proposal_set_decoder.py`.
2. Updated `train_proposal_set_decoder.py` with prior config flags and
   `mean_prior_entropy`.
3. Added `run_prior_conditioned_decoder_sweep.sh`.
4. Extended ProposalSetDecoder unit tests.
5. Synced changed non-core files to BUAA-Server.
6. Ran server py_compile and 1-epoch smoke.
7. Ran seed-7 correct/no-state/shuffle sweep on GPU 1.
8. Added two-stage frozen-prior trainer path:
   `--state-prior-checkpoint`, `--freeze-state-prior`, `--prior-kl-weight`.
9. Added `run_frozen_prior_decoder_sweep.sh`.
10. Ran frozen-prior 1-epoch server smoke.

## Verification

Local:

```text
python -B -m pytest code/dream3r/tests/test_proposal_set_decoder.py \
  code/dream3r/tests/test_state_prior_head.py -q
6 passed
```

Server smoke:

```text
runs/stage6_fusion/prior_conditioned_decoder_smoke_seed7
KITTI: Ours_ProposalSetDecoder 0.1480 vs best_single 0.1523
ETH3D: Ours_ProposalSetDecoder 0.1875 vs best_single 0.1585
```

## Server Run

```text
root:   /hdd3/kykt26/code/dream3r
script: dream3r/scripts/run_prior_conditioned_decoder_sweep.sh
out:    runs/stage6_fusion/prior_conditioned_decoder_sweep/
gpu:    CUDA_VISIBLE_DEVICES=1
```

Completed controls:

```text
prior_state_seed_7
prior_no_state_seed_7
prior_shuffle_state_seed_7
```

## Result

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| correct-state | 0.1523 | -0.00 pp | 0.1828 | -15.37 pp |
| no-state | 0.1201 | +21.18 pp | 0.1717 | -8.35 pp |
| shuffle-state | 0.1481 | +2.77 pp | 0.1855 | -17.07 pp |

Correct-state does not beat controls. No-state is better on both domains and
shuffle-state is better on KITTI. The prior branch therefore did not repair
decoder state causality.

## Boundary

No cache rebuild, checkpoint download, environment mutation, expert admission,
or frozen-core edit.

## Conclusion

StatePriorHead remains the positive evidence. Joint ProposalSetDecoder training
can collapse or override that prior. Next work should be two-stage:

```text
pretrain/freeze or KL-regularize StatePrior -> train proposal-token refinement
```

Do not continue by adding more decoder capacity.

## Two-stage Smoke

```text
runs/stage6_fusion/prior_frozen_decoder_smoke_seed7
```

Loaded:

```text
runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt
--freeze-state-prior
--prior-kl-weight 0.1
```

Result:

```text
KITTI: Ours_ProposalSetDecoder 0.1451 vs best_single 0.1523
ETH3D: Ours_ProposalSetDecoder 0.1480 vs best_single 0.1585
```

This is runtime evidence that the two-stage path can preserve DEC-019's
positive StatePrior signal before training refinement. It is not yet a full
decoder sweep.
