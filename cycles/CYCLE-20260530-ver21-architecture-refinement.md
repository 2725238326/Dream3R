# CYCLE-20260530 — Dream3R ver2.1 architecture refinement

date: 2026-05-30
status: closed with 4-seed server metric refresh
linked_decision: `decisions/DEC-20260530-012-ver21-state-training-metrics.md`
linked_spec: `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md`

## Objective

Improve the ver2.0 SCF architecture without reopening broad route search.
The refinement target is trained state and better metrics: prove or falsify
whether Dream3R's state machinery contributes beyond proposal fusion.

## Changes

- Added ver2.1 spec defining the trained-state and metric-extension track.
- Added a concrete state-training plan with no implicit server authorization.
- Extended non-core SCF eval to report:
  - per-patch oracle lower bound;
  - gap to patch oracle;
  - adjacent-frame temporal delta proxy;
  - scale-drift proxy.
- Recorded a DEC rejecting hard-router revival and unbounded residual as the
  next path.
- Added `--shuffle-state` control to `train_scf_head.py`.
- Synced SCF files to BUAA-Server and ran a 4-seed metric refresh on GPU 1
  for state / no-state / shuffled-state variants.
- Added `run_ver21_metric_refresh.sh` and
  `summarize_ver21_metric_refresh.py` to make the remaining sweep and
  summary reproducible.

## Server evidence

Artifacts:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/ver21_metric_refresh/seed_{7,11,13,17}_{state,no_state,shuffle_state}/results.json
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/ver21_metric_refresh/summary.md
```

| variant | KITTI Ours | KITTI rel_imp | KITTI patch_gap | ETH3D Ours | ETH3D rel_imp | ETH3D patch_gap |
| --- | --- | --- | --- | --- | --- | --- |
| correct state | 0.1386 +/- 0.0023 | +9.7925 +/- 2.7182% | 41.0525 +/- 2.0072% | 0.1628 +/- 0.0284 | +2.4375 +/- 3.0443% | 51.0900 +/- 5.7015% |
| no state | 0.1460 +/- 0.0008 | +5.0400 +/- 1.6269% | 48.5150 +/- 2.1967% | 0.1773 +/- 0.0276 | -6.4650 +/- 1.8827% | 65.0225 +/- 9.3054% |
| shuffled state | 0.1487 +/- 0.0034 | +3.2700 +/- 2.1847% | 51.3275 +/- 5.3027% | 0.1846 +/- 0.0422 | -10.0850 +/- 8.9060% | 70.6475 +/- 16.2341% |

Reading: correct state wins over no-state and shuffled-state across both
domains. Shuffling state degrades the result, so the benefit is not just head
capacity or a state-shaped input. The temporal/scale proxies are not yet a
win for correct state, so they become explicit training targets rather than
implicit claims.

Completed sweep log:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/ver21_metric_refresh/remaining_seeds.log
```

## Boundary

No frozen v0.3/v0.5 core files were edited. Server work was limited to the
non-core SCF trainer on existing caches.
