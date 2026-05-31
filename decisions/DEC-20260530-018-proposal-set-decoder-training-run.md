# DEC-20260530-018 — ProposalSetDecoder server training run

date: 2026-05-30
status: accepted

## Context

DEC-017 added the local non-core ProposalSetDecoder prototype but left server
training gated. The user then requested training to start.

Existing real-backend SCF caches are available on the server:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/scf_kitti_cache.pt
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/scf_eth3d_cache.pt
```

## Decision

Authorize a server-side cached-proposal ProposalSetDecoder sweep on GPU 1.

Allowed:

- scp non-core ProposalSetDecoder files to the server package tree;
- run a 1-epoch smoke on existing SCF caches;
- run a background sweep using existing caches only;
- write results under `runs/stage6_fusion/proposal_set_decoder_sweep/`.

Not allowed by this DEC:

- checkpoint download;
- cache rebuild;
- new expert admission;
- environment mutation;
- frozen-core edits.

## Execution Shape

The sweep script is:

```text
code/dream3r/scripts/run_proposal_set_decoder_sweep.sh
```

Default schedule:

```text
state_seed_7
state_seed_11
state_seed_13
no_state_seed_7
shuffle_state_seed_7
```

Each run uses:

```text
CUDA_VISIBLE_DEVICES=1
epochs=300
lr=1e-3
```

## Smoke Evidence

The 1-epoch smoke loaded 296 entries and 3 experts:

```text
experts = fast3r, mast3r, spann3r
train = 237
test = 59
```

Initial smoke result:

```text
KITTI Ours_ProposalSetDecoder = 0.1482
KITTI best_single = 0.1523
ETH3D Ours_ProposalSetDecoder = 0.1855
ETH3D best_single = 0.1585
```

This is not a final result; it only proves runtime compatibility and confirms
the training path is live.

## First Full Result

`state_seed_7` completed with mixed evidence:

```text
KITTI Ours_ProposalSetDecoder = 0.1477
KITTI best_single = 0.1523
KITTI rel_imp_vs_best_single_pp = 3.01

ETH3D Ours_ProposalSetDecoder = 0.1857
ETH3D best_single = 0.1585
ETH3D rel_imp_vs_best_single_pp = -17.18
```

This supports a narrow KITTI-positive claim only. It does not support a broad
cross-domain improvement claim.

## Full Sweep Addendum

The completed v0 sweep shows:

```text
State / KITTI:  0.1478 +/- 0.0004 vs best_single 0.1526 +/- 0.0003
State / ETH3D:  0.1869 +/- 0.0292 vs best_single 0.1715 +/- 0.0269
Shuffle / KITTI: 0.1477 +/- 0.0006
Shuffle / ETH3D: 0.1863 +/- 0.0258
No-state / KITTI: 0.1595 +/- 0.0623
No-state / ETH3D: 0.2125 +/- 0.0741
```

Conclusion:

```text
ProposalSetDecoder v0 is a bounded proposal mixer with a stable small KITTI
gain, but it does not prove Dream-state causality because correct-state and
shuffled-state are effectively tied. The ETH3D result is negative.
```

## Follow-up Authorization

Authorize a narrow non-core state-bias v1 follow-up:

- add a zero-initialized state-to-expert-logit head;
- run local unit tests;
- run a 1-epoch server smoke;
- run only `state_seed_7` first under
  `runs/stage6_fusion/proposal_set_decoder_state_bias_sweep/`.

Do not expand v1 to a full sweep unless seed 7 improves over v0 and motivates
a shuffle-state control.

## Follow-up Result

State-bias v1 seed 7:

```text
Correct-state / KITTI: 0.1470
Shuffle-state / KITTI: 0.1477

Correct-state / ETH3D: 0.1829
Shuffle-state / ETH3D: 0.1827
```

Decision:

```text
Do not expand state-bias v1 to a full sweep now. It gives a tiny KITTI
state-control separation but no ETH3D state-control separation. The next
meaningful step is not more seeds of the same head; it is a better trained
state objective / state representation before native distillation.
```

## Acceptance

The run can support a positive architecture claim only if final results show:

- correct-state ProposalSetDecoder beats best single or SCF on at least one
  domain;
- no-state / shuffled-state controls do not match correct-state;
- oracle and patch-oracle gaps are reported honestly;
- temporal and scale proxies are included.

If the sweep does not improve over SCF, keep Dream3R-PD as an implementation
path but present SCF as the honest midterm prototype.
