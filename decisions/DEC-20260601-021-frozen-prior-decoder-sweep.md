# DEC-20260601-021 — Frozen-prior decoder sweep

date: 2026-06-01
status: accepted; seed-7 controls closed scaffold-positive

## Context

DEC-019 proved that Dream state contains a usable expert-prior signal.
DEC-020 then showed that joint ProposalSetDecoder training can collapse or
override that prior: correct-state did not beat no-state/shuffle controls.

The next minimal repair is therefore not a larger decoder. It is a two-stage
decoder:

```text
StatePriorHead checkpoint -> frozen expert prior
ProposalSetDecoder -> local proposal-token refinement under prior constraint
```

## Decision

Run a frozen-prior ProposalSetDecoder sweep using the DEC-019 checkpoint:

```text
runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt
```

Training flags:

```text
--state-prior-checkpoint runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt
--freeze-state-prior
--prior-kl-weight 0.1
```

## Allowed

- Use existing SCF caches only.
- Use existing DEC-019 StatePrior checkpoint only.
- Train the non-core ProposalSetDecoder refinement layers.
- Run seed-7 correct-state and shuffle-state controls.

## Forbidden

- Frozen-core edits.
- Cache rebuild.
- Checkpoint download.
- Environment mutation.
- New expert admission.
- Claiming native Dream3R quality before controls close.

## Success Criteria

The frozen-prior decoder is useful only if:

```text
correct-state stays at or above StatePriorHead quality on KITTI/ETH3D,
and correct-state beats shuffle-state on both domains.
```

If it matches StatePrior but does not improve, it is still useful as a stable
scaffold for later refinement. If shuffle-state matches or beats correct-state,
the prior is not being preserved causally.

## Active Server Run

```text
root:   /hdd3/kykt26/code/dream3r
script: dream3r/scripts/run_frozen_prior_decoder_sweep.sh
out:    runs/stage6_fusion/frozen_prior_decoder_sweep/
gpu:    CUDA_VISIBLE_DEVICES=1
```

Controls:

```text
frozen_prior_state_seed_7
frozen_prior_shuffle_state_seed_7
```

## Initial Evidence

The first epoch of `frozen_prior_state_seed_7` reproduces DEC-019:

```text
KITTI Ours_ProposalSetDecoder = 0.1451 vs best_single 0.1523
ETH3D Ours_ProposalSetDecoder = 0.1480 vs best_single 0.1585
```

## Seed-7 Result

Server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/frozen_prior_decoder_sweep/
```

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| frozen-prior correct-state | 0.1452 | +4.68 pp | 0.1480 | +6.64 pp |
| frozen-prior shuffle-state | 0.1525 | -0.11 pp | 0.2468 | -55.75 pp |

Correct-state preserves DEC-019 StatePrior quality and beats shuffle-state on
both domains. This closes the causality control positively.

## Consequence

The frozen-prior route is a stable scaffold, not yet an improved decoder:

```text
StatePriorHead:       KITTI 0.1451, ETH3D 0.1480
Frozen-prior decoder: KITTI 0.1452, ETH3D 0.1480
```

The useful result is that freezing the prior prevents the joint decoder collapse
seen in DEC-020. The next refinement should keep the prior frozen and add a
small, bounded residual/token refinement path with explicit improvement gates.
Do not unfreeze or enlarge the joint decoder before that bounded refinement
gate exists.

## KL Sensitivity Probe

After the main `prior_kl_weight=0.1` sweep, a lighter KL probe was run:

```text
OUT=runs/stage6_fusion/frozen_prior_decoder_kl001_sweep
PRIOR_KL_WEIGHT=0.01
bash dream3r/scripts/run_frozen_prior_decoder_sweep.sh
```

Result:

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| frozen-prior correct-state, KL=0.01 | 0.1451 | +4.76 pp | 0.1480 | +6.64 pp |
| frozen-prior shuffle-state, KL=0.01 | 0.1525 | -0.11 pp | 0.2468 | -55.75 pp |

Lowering KL from 0.1 to 0.01 preserves causality but still does not improve
beyond StatePriorHead. The next refinement must change the refinement mechanism
or training target, not only the KL weight.
