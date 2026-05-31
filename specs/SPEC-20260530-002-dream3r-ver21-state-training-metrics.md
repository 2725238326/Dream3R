# SPEC-20260530-002 — Dream3R-ver2.1 trained-state and metric extension

status: accepted next architecture step; core implementation gated
date: 2026-05-30
depends_on: SPEC-20260530-001, DEC-20260530-011

## Purpose

Dream3R-ver2.0 proved that bounded state-conditioned fusion is a usable
model. It did **not** prove that Dream3R's Memory / AnchorBank / NSA /
Critic state has learned reconstruction value. Ver2.1 completes the
architecture by making state quality trainable and measurable.

## Core diagnosis

The remaining bottleneck is not another router or a more aggressive residual
head. The bottleneck is this contract:

```text
state must improve fusion because it encodes sequence geometry,
not because it is a fixed random embedding that happens to separate windows.
```

Therefore ver2.1 adds two pieces:

1. a depth/coherence-aligned state training objective;
2. metrics that can falsify temporal and scale claims.

## Architecture delta

Ver2.1 keeps the ver2.0 SCF output head:

```text
real proposal bank -> SCFHead -> final_pointmap
```

and changes the state path feeding it:

```text
images
-> Memory / AnchorBank / NSA / Critic state
-> state projection used by SCFHead
```

The state path should be trained with reconstruction-adjacent supervision
while the frozen expert proposal bank remains the controlled input. This
separates "better state" from "better expert".

## Proposed training objectives

All objectives are additive candidates; none authorizes core edits without a
DEC.

| Objective | Signal | Why it matters |
| --- | --- | --- |
| Fusion weight distillation | KL from SCF weights to per-window / per-patch oracle expert labels | teaches state to choose which proposal is reliable |
| Depth-aligned SCF loss | scale-aligned abs_rel of final pointmap | keeps state useful for reconstruction, not just classification |
| Temporal delta loss | adjacent-frame depth-change error | pressures state to encode sequence consistency |
| Scale-drift loss | stddev of per-frame log scale ratios | pressures state to stabilize long-window scale |
| Critic calibration | conflict/reliability predicts proposal error rank | makes Critic useful as reliability input, not reroute override |

The first safe version should freeze Fast3R / MASt3R / Spann3R and train only
small state projection / Critic calibration / SCF-side heads. Unfreezing
Dream3R core memory modules requires a separate DEC because core files are
currently frozen.

## Required metrics

Ver2.1 evaluation must report more than abs_rel:

| Metric | Meaning | Current implementation surface |
| --- | --- | --- |
| `B_patch_oracle` | lower bound from best expert per valid point | added to `train_scf_head.py` |
| `patch_oracle_gap_pp` | how far SCF is from patch-level proposal ceiling | added to `train_scf_head.py` |
| `Ours_temporal_delta_abs_rel` | adjacent-frame depth-change error proxy | added to `train_scf_head.py` |
| `Ours_scale_drift_proxy` | per-frame scale drift proxy | added to `train_scf_head.py` |
| trained-state delta | SCF(trained state) - SCF(no state) | future run |
| random-state control | SCF(trained state) - SCF(random-init state) | future run |

## Acceptance gate

Ver2.1 is useful only if at least one of these holds on held-out data:

1. trained state improves SCF over both no-state and random-init-state;
2. trained state reduces temporal delta or scale drift without losing abs_rel;
3. Critic/reliability calibration lowers patch-oracle gap.

If none holds, the honest conclusion is that SCF is a good proposal-fusion
head, but the current Dream3R state machinery is not yet the source of the
gain.

## Initial 4-seed evidence

The first ver2.1 metric refresh ran the three essential controls on the
existing real-backend SCF caches across seeds `7, 11, 13, 17`:

| variant | KITTI rel_imp | KITTI patch_gap | ETH3D rel_imp | ETH3D patch_gap |
| --- | --- | --- | --- | --- |
| SCF + correct state | +9.7925 +/- 2.7182% | 41.0525 +/- 2.0072% | +2.4375 +/- 3.0443% | 51.0900 +/- 5.7015% |
| SCF - state | +5.0400 +/- 1.6269% | 48.5150 +/- 2.1967% | -6.4650 +/- 1.8827% | 65.0225 +/- 9.3054% |
| SCF + shuffled state | +3.2700 +/- 2.1847% | 51.3275 +/- 5.3027% | -10.0850 +/- 8.9060% | 70.6475 +/- 16.2341% |

This upgrades the state claim: the gain depends on the **correctly aligned
window state**, not just the existence of a state-shaped input. Correct state
beats no-state and shuffled-state on both domains for abs_rel and patch-oracle
gap. It still does not validate trained memory quality, because the state
source is not yet retrained.

Temporal/scale metrics remain open: correct state improves abs_rel and
patch-oracle gap, but does not dominate no-state on the temporal or scale
proxies. Therefore ver2.1 should train temporal/scale objectives explicitly.

## Non-goals

- no new expert family as the main fix;
- no hard router revival;
- no unbounded residual correction;
- no SOTA claim;
- no core edit without a DEC.

## First executor task

Run the updated SCF eval on the existing `scf_{kitti,eth3d}_cache.pt` caches
and record the new oracle/temporal/drift columns. If that passes, draft the
smallest state-training DEC that either freezes core and trains projection
heads, or explicitly requests a core-edit exemption.
