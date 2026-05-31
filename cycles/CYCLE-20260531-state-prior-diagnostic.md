# CYCLE-20260531 — StatePrior diagnostic

date: 2026-05-31
status: closed; seed-7 server controls complete
decision: `decisions/DEC-20260531-019-state-prior-diagnostic.md`

## Trigger

ProposalSetDecoder v0/v1 did not establish Dream-state causality. The user
asked to keep pushing, so the next surgical step is to isolate state signal
instead of scaling the same decoder.

## Actions

1. Added `code/dream3r/state_prior_head.py`.
2. Added `code/dream3r/scripts/train_state_prior_head.py`.
3. Added `code/dream3r/tests/test_state_prior_head.py`.
4. Added `code/dream3r/scripts/run_state_prior_sweep.sh`.
5. Ran local tests and static checks.
6. Synced non-core files to BUAA-Server.
7. Ran 1-epoch server smoke.
8. Ran seed-7 correct/no-state/shuffle sweep on GPU 1.

## Local Verification

```text
python -m pytest code/dream3r/tests/test_state_prior_head.py -q
2 passed

python -m py_compile code/dream3r/state_prior_head.py \
  code/dream3r/scripts/train_state_prior_head.py \
  code/dream3r/tests/test_state_prior_head.py
```

## Server Smoke

```text
runs/stage6_fusion/state_prior_smoke_seed7
```

Smoke result:

```text
KITTI: Ours_StatePrior 0.1467 vs best_single 0.1523
ETH3D: Ours_StatePrior 0.2108 vs best_single 0.1585
```

## Server Run

```text
root:   /hdd3/kykt26/code/dream3r
script: dream3r/scripts/run_state_prior_sweep.sh
out:    runs/stage6_fusion/state_prior_sweep/
gpu:    CUDA_VISIBLE_DEVICES=1
```

Completed controls:

```text
state_seed_7
no_state_seed_7
shuffle_state_seed_7
```

## Result

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| correct-state | 0.1451 | +4.73 pp | 0.1480 | +6.64 pp |
| no-state | 0.1472 | +3.33 pp | 0.2003 | -26.38 pp |
| shuffle-state | 0.1622 | -6.51 pp | 0.2111 | -33.18 pp |

Best single references:

```text
KITTI: 0.1523
ETH3D: 0.1585
```

Correct-state beats no-state and shuffle-state on both domains. Shuffle-state
collapses below best-single, so the result is not explained by model capacity or
cached proposal geometry alone.

## Boundary

No cache rebuild, checkpoint download, environment mutation, expert admission,
or frozen-core edit.

## Architecture Update

The current Dream state has usable expert-prior signal. ProposalSetDecoder
v0/v1 failed because the decoder did not preserve that signal as a stable
control path. Next work should inject the learned StatePrior-style prior into
ProposalSetDecoder/native distillation instead of expanding an unstructured
state-concat decoder.
