# DEC-20260530-012 — Dream3R-ver2.1 should train and evaluate state, not revive routing

decision_id: DEC-20260530-012
date: 2026-05-30
scope: Dream3R post-midterm architecture refinement
decision: Adopt ver2.1 as a trained-state + metric-extension track on top of SCF; do not revive hard routing, unbounded residual correction, or broad expert-search as the next architecture path.
status: accepted for non-core eval direction; core training still gated

## Context

DEC-20260530-011 accepted bounded SCF as the first usable
state-conditioned reconstruction model. Its main limitation is also clear:
`memory.fused_context` is still a current-state embedding, not proof that
trained Memory / AnchorBank / NSA / Critic state improves reconstruction.

The next architecture step must therefore test state quality directly.

## Decision

The next Dream3R architecture track is **ver2.1 trained-state SCF**:

```text
real expert proposal bank
+ trained/calibrated state and reliability features
-> bounded SCF
-> abs_rel + patch-oracle + temporal + scale-drift evaluation
```

This keeps ver2.0's bounded fusion head and improves the signal feeding it.

## Rejected alternatives

- More hard-router sweeps: already demoted by DEC-009/DEC-011.
- Unbounded residual correction: rejected by L1 and residual ablation.
- New expert family as the main fix: too broad for the current evidence gap.
- Claiming trained memory value from random-init `memory.fused_context`: an
  overclaim.

## Immediate artifacts

- `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md`
- `planning/DREAM3R_VER21_STATE_TRAINING_PLAN.md`
- metric extensions in `code/dream3r/scripts/train_scf_head.py`

## 4-seed metric refresh evidence (server, GPU 1)

Executed on existing real-backend SCF caches:

```text
runs/stage6_fusion/ver21_metric_refresh/seed_{7,11,13,17}_{state,no_state,shuffle_state}/results.json
runs/stage6_fusion/ver21_metric_refresh/summary.{json,md}
```

| variant | KITTI Ours | KITTI rel_imp | KITTI patch_gap | ETH3D Ours | ETH3D rel_imp | ETH3D patch_gap |
| --- | --- | --- | --- | --- | --- | --- |
| SCF + correct state | 0.1386 +/- 0.0023 | +9.7925 +/- 2.7182% | 41.0525 +/- 2.0072% | 0.1628 +/- 0.0284 | +2.4375 +/- 3.0443% | 51.0900 +/- 5.7015% |
| SCF - state | 0.1460 +/- 0.0008 | +5.0400 +/- 1.6269% | 48.5150 +/- 2.1967% | 0.1773 +/- 0.0276 | -6.4650 +/- 1.8827% | 65.0225 +/- 9.3054% |
| SCF + shuffled state | 0.1487 +/- 0.0034 | +3.2700 +/- 2.1847% | 51.3275 +/- 5.3027% | 0.1846 +/- 0.0422 | -10.0850 +/- 8.9060% | 70.6475 +/- 16.2341% |

Interpretation: the 4-seed state gain is window-aligned. Correct state beats
both no-state and shuffled-state on both domains for abs_rel and patch-oracle
gap. Shuffling memory contexts degrades the result beyond no-state, which
supports the ver2.1 premise that state alignment matters.

Temporal/scale caveat:

| variant | KITTI temporal | KITTI scale | ETH3D temporal | ETH3D scale |
| --- | --- | --- | --- | --- |
| SCF + correct state | 0.0340 +/- 0.0038 | 0.0232 +/- 0.0011 | 0.0552 +/- 0.0091 | 0.0259 +/- 0.0018 |
| SCF - state | 0.0331 +/- 0.0019 | 0.0217 +/- 0.0018 | 0.0566 +/- 0.0117 | 0.0217 +/- 0.0026 |
| SCF + shuffled state | 0.0348 +/- 0.0031 | 0.0240 +/- 0.0011 | 0.0546 +/- 0.0100 | 0.0225 +/- 0.0009 |

Correct state improves fusion accuracy and patch-oracle gap, but does not yet
prove temporal or scale stability. Ver2.1 training should explicitly optimize
those terms rather than assuming they follow from abs_rel.

## Gate

Any server training, checkpoint download, or frozen-core edit still requires
a separate approval/DEC. This decision only fixes the next architecture
direction and non-core evaluation surface.
