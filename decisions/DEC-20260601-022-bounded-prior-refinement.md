# DEC-20260601-022 — Bounded refinement over frozen StatePrior

date: 2026-06-01
status: accepted; seed-7 controls closed small-positive

## Context

DEC-019 proved Dream state contains a useful expert-prior signal. DEC-020
showed joint ProposalSetDecoder training collapses or overrides that signal.
DEC-021 then showed that freezing the trained StatePrior preserves causality:

```text
frozen-prior correct-state: KITTI 0.1452, ETH3D 0.1480
frozen-prior shuffle-state: KITTI 0.1525, ETH3D 0.2468
```

However, DEC-021 did not improve beyond StatePriorHead. The next useful step is
therefore a bounded refinement mechanism over the frozen prior, not a larger
joint decoder and not another KL-only sweep.

## Decision

Add a zero-initialized residual refinement head after frozen-prior convex
fusion:

```text
frozen StatePrior -> convex fused pointmap -> bounded residual offset
```

The residual offset is bounded by local proposal disagreement:

```text
delta = tanh(residual_head(...)) * proposal_disagreement * residual_refine_scale
```

This keeps epoch-0 behavior equal to frozen-prior fusion and prevents the
refinement branch from freely rewriting geometry.

## Allowed

- Modify non-core `proposal_set_decoder.py`.
- Modify non-core `train_proposal_set_decoder.py`.
- Reuse `run_frozen_prior_decoder_sweep.sh` with
  `RESIDUAL_REFINE_SCALE=0.05`.
- Use existing SCF caches and DEC-019 checkpoint only.

## Forbidden

- Frozen-core edits.
- Cache rebuild.
- Checkpoint download.
- Environment mutation.
- New expert admission.
- Unbounded pointmap residuals.

## Success Criteria

The branch is useful only if:

```text
correct-state beats frozen-prior baseline on KITTI or ETH3D,
does not regress the other domain materially,
and still beats shuffle-state on both domains.
```

If it matches frozen-prior without improvement, the branch is neutral. If it
improves only KITTI while hurting ETH3D or losing shuffle separation, it is a
negative cross-domain refinement.

## Initial Verification

Local:

```text
python -B -m pytest code/dream3r/tests/test_proposal_set_decoder.py \
  code/dream3r/tests/test_state_prior_head.py -q
8 passed
```

Server smoke with `residual_refine_scale=0.05`:

```text
runs/stage6_fusion/bounded_refine_smoke_seed7
KITTI: 0.1451 vs best_single 0.1523
ETH3D: 0.1475 vs best_single 0.1585
```

The smoke preserves frozen-prior quality and gives a small ETH3D improvement,
but the active correct/shuffle controls decide whether that improvement is
causal and stable.

## Seed-7 Result

Server path:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/
```

| Control | KITTI abs_rel | KITTI vs best single | ETH3D abs_rel | ETH3D vs best single |
|---|---:|---:|---:|---:|
| bounded-refine correct-state | 0.1448 | +4.93 pp | 0.1475 | +6.94 pp |
| bounded-refine shuffle-state | 0.1521 | +0.13 pp | 0.2467 | -55.68 pp |

Reference frozen-prior baseline from DEC-021:

```text
frozen-prior correct-state: KITTI 0.1452, ETH3D 0.1480
```

The bounded residual refinement improves the frozen-prior baseline slightly on
both domains while preserving a strong shuffle-state separation. The gain is
small, so this is a small-positive refinement, not a large architecture win.

## Consequence

The current best bounded Dream3R variant is:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded convex fusion
-> zero-initialized disagreement-bounded residual refinement
```

This is the first post-StatePrior decoder variant that improves over
frozen-prior without losing state causality. Future refinement should keep the
same gate:

```text
beat frozen-prior correct-state,
beat shuffle-state on both domains,
do not worsen temporal/scale proxies materially.
```
