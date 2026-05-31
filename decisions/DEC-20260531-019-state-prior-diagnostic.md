# DEC-20260531-019 — StatePrior diagnostic for Dream-state causality

date: 2026-05-31
status: accepted; seed-7 diagnostic closed

## Context

ProposalSetDecoder v0 produced a stable small KITTI gain but failed ETH3D and
did not prove Dream-state causality because correct-state and shuffled-state
were effectively tied. The v1 state-bias follow-up slightly improved seed 7
but still showed only tiny correct-state separation on KITTI and none on
ETH3D.

The next question is therefore not "make the decoder larger"; it is whether
the current Dream state (`memory_context` + conflict score) contains a useful
expert-prior signal at all.

## Decision

Add a non-core StatePrior diagnostic head:

```text
inputs:  memory_context + conflict_score only
output:  window-level soft expert weights
fusion:  convex fusion over existing real proposal cache
```

The head intentionally does not use proposal geometry or proposal confidence in
its weighting network. It is a state-causality diagnostic, not a final decoder.

## Allowed

- Add non-core `state_prior_head.py`.
- Add cached-proposal trainer `train_state_prior_head.py`.
- Add local unit tests.
- Run seed-7 correct/no-state/shuffle controls on existing SCF caches.

## Forbidden

- Frozen-core edits.
- Cache rebuild.
- Checkpoint download.
- Environment mutation.
- New expert admission.

## Success Criteria

The current Dream state is considered useful only if:

```text
correct-state beats no-state and shuffled-state on KITTI,
and does not worsen ETH3D relative to the same controls.
```

If correct-state does not separate from shuffled-state, state representation is
not causally strong enough for ProposalSetDecoder/native distillation.

## Initial Smoke

One-epoch server smoke loaded 296 entries and 3 experts.

```text
KITTI Ours_StatePrior = 0.1467 vs best_single 0.1523
ETH3D Ours_StatePrior = 0.2108 vs best_single 0.1585
```

This is runtime smoke only. The controlled seed-7 run decides whether the
signal is real.

## Seed-7 Result

Server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/state_prior_sweep/
```

All three controls ran on existing SCF caches only:

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| correct-state | 0.1451 | +4.73 pp | 0.1480 | +6.64 pp |
| no-state | 0.1472 | +3.33 pp | 0.2003 | -26.38 pp |
| shuffle-state | 0.1622 | -6.51 pp | 0.2111 | -33.18 pp |

Reference best singles in the same cache split:

```text
KITTI: best_single = 0.1523 (MASt3R)
ETH3D: best_single = 0.1585 (Spann3R)
```

Correct-state beats both controls on both domains. This is the first clean
post-ProposalSetDecoder evidence that the current Dream state contains a
causal expert-prior signal.

## Consequence

ProposalSetDecoder v0/v1 failed because its state path did not use the state as
a stable expert-prior/control signal. The next architecture action is not
"larger decoder" or another unstructured concatenation. The next action is to
make the learned state prior an explicit input/regularizer for the proposal-set
decoder and native distillation path:

```text
Dream state -> expert prior -> proposal-token decoder -> native pointmap
```

StatePriorHead remains a diagnostic/prototype component, not the final model
head.
