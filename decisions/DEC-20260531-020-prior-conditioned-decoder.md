# DEC-20260531-020 — Prior-conditioned ProposalSetDecoder

date: 2026-05-31
status: accepted; seed-7 controls closed negative

## Context

ProposalSetDecoder v0/v1 did not prove Dream-state causality. DEC-019 then
isolated the Dream state and found a clean positive signal: StatePriorHead,
which uses only `memory_context + conflict_score`, beats best-single and
no-state/shuffle controls on both KITTI and ETH3D for seed 7.

This means the current failure is not "state has no signal". The failure is
that the decoder can ignore or dilute state when it is only concatenated to
proposal tokens or passed through a weak linear bias.

## Decision

Add an explicit StatePrior-style MLP branch inside the non-core
ProposalSetDecoder:

```text
Dream state + conflict -> state_prior_mlp -> expert prior logits
proposal tokens -> proposal mixer -> local patch logits
final logits = local patch logits + linear state bias + state prior logits
```

The output remains a convex fusion over scale-normalized cached real proposal
pointmaps. This is still a bounded decoder, not a native standalone model.

## Allowed

- Modify non-core `code/dream3r/proposal_set_decoder.py`.
- Modify non-core `train_proposal_set_decoder.py` to record prior entropy and
  config.
- Add `run_prior_conditioned_decoder_sweep.sh`.
- Run seed-7 correct/no-state/shuffle controls on existing SCF caches.

## Forbidden

- Frozen-core edits.
- Cache rebuild.
- Checkpoint download.
- Environment mutation.
- New expert admission.

## Success Criteria

The prior-conditioned decoder is useful only if correct-state beats both
no-state and shuffle-state on KITTI and does not worsen ETH3D relative to those
controls. If it still fails while DEC-019 StatePrior succeeds, the next step is
two-stage prior pretraining / distillation, not a larger mixed decoder.

## Initial Verification

Local structure tests:

```text
python -B -m pytest code/dream3r/tests/test_proposal_set_decoder.py \
  code/dream3r/tests/test_state_prior_head.py -q
6 passed
```

Server 1-epoch smoke over existing SCF caches:

```text
runs/stage6_fusion/prior_conditioned_decoder_smoke_seed7
KITTI Ours_ProposalSetDecoder = 0.1480 vs best_single 0.1523
ETH3D Ours_ProposalSetDecoder = 0.1875 vs best_single 0.1585
```

The smoke validates runtime only. The seed-7 controls decide whether the prior
branch fixes decoder state causality.

## Seed-7 Result

Server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/prior_conditioned_decoder_sweep/
```

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| correct-state | 0.1523 | -0.00 pp | 0.1828 | -15.37 pp |
| no-state | 0.1201 | +21.18 pp | 0.1717 | -8.35 pp |
| shuffle-state | 0.1481 | +2.77 pp | 0.1855 | -17.07 pp |

Best single references in the same split:

```text
KITTI: 0.1523
ETH3D: 0.1585
```

The correct-state prior-conditioned decoder does not meet the success
criteria. No-state is better than correct-state on both domains, and
shuffle-state is better on KITTI. This means the joint decoder did not preserve
the causal state-prior signal discovered in DEC-019.

## Consequence

This branch is negative as a final decoder update. The useful finding is
diagnostic: StatePriorHead proves state signal exists, but joint
ProposalSetDecoder training can override or collapse it.

Next architecture action:

```text
1. Pretrain StatePriorHead / expert prior on cached proposals.
2. Freeze or KL-regularize that prior inside ProposalSetDecoder.
3. Train local proposal-token refinement only after the prior remains causal.
```

Do not scale the current joint decoder or add more token-mixer capacity before
this two-stage prior constraint exists.

## Follow-up Implementation

The trainer now supports the two-stage route directly:

```text
--state-prior-checkpoint <latest.pt>
--freeze-state-prior
--prior-kl-weight 0.1
```

Smoke command using the DEC-019 checkpoint:

```text
runs/stage6_fusion/prior_frozen_decoder_smoke_seed7
```

Smoke result after loading and freezing StatePrior:

```text
KITTI: Ours_ProposalSetDecoder = 0.1451 vs best_single 0.1523
ETH3D: Ours_ProposalSetDecoder = 0.1480 vs best_single 0.1585
```

This smoke intentionally reproduces the StatePrior behavior at epoch 1. It is
not a final decoder win, but it proves the executable two-stage path preserves
the positive DEC-019 prior before local proposal-token refinement is trained.

## Frozen-prior Sweep

Completed server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/frozen_prior_decoder_sweep/
```

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| frozen-prior correct-state | 0.1452 | +4.68 pp | 0.1480 | +6.64 pp |
| frozen-prior shuffle-state | 0.1525 | -0.11 pp | 0.2468 | -55.75 pp |

The frozen-prior path preserves the DEC-019 positive signal and keeps a strong
state-control separation. Current proposal-token refinement does not improve
beyond the StatePrior result, but it no longer destroys the state prior when
the prior branch is frozen and KL-anchored.

## Current Architecture Boundary

The current usable Dream3R model should be described as:

```text
proposal teachers + Dream state -> trained frozen StatePrior -> bounded convex fusion
```

ProposalSetDecoder remains an experimental refinement layer behind the prior,
not the primary result, until it proves a gain over frozen StatePrior without
losing shuffle/no-state separation.
