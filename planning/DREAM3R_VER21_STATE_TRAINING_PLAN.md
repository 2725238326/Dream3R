# Dream3R-ver2.1 state-training and metric plan

date: 2026-05-30
status: step 1 completed as 4-seed control; further training/core edits gated
source_spec: `specs/SPEC-20260530-002-dream3r-ver21-state-training-metrics.md`

## Goal

Make Dream3R's state path accountable. Ver2.0 shows SCF can fuse proposals;
ver2.1 must test whether trained Memory / Critic state improves that fusion
over no-state and random-state controls.

## Step 1 — metric extension

Use the updated non-core script:

```text
code/dream3r/scripts/train_scf_head.py
```

It now reports:

- `B_patch_oracle`
- `patch_oracle_gap_pp`
- `Ours_temporal_delta_abs_rel`
- `Ours_scale_drift_proxy`

Server sketch:

```bash
CUDA_VISIBLE_DEVICES=1 python -m dream3r.scripts.train_scf_head \
  --cache runs/stage6_fusion/scf_kitti_cache.pt runs/stage6_fusion/scf_eth3d_cache.pt \
  --output-dir runs/stage6_fusion/scf_metric_refresh/seed_7 \
  --seed 7 --epochs 300
```

Executed 2026-05-30 on BUAA-Server GPU 1 for:

```text
seed_{7,11,13,17}_state
seed_{7,11,13,17}_no_state
seed_{7,11,13,17}_shuffle_state
```

Result summary:

```text
correct state:  KITTI +9.79%, ETH3D +2.44%
no state:       KITTI +5.04%, ETH3D -6.47%
shuffled state: KITTI +3.27%, ETH3D -10.09%
```

Correct state beats no-state and shuffled-state on both domains for abs_rel
and patch-oracle gap. Temporal/scale proxies remain open.

## Step 2 — frozen-state-projection experiment

Before touching core memory modules, train only small heads around the
existing cached state:

```text
memory.fused_context -> projection/calibration head -> SCF weights
```

Baselines:

- SCF + current state
- SCF - state
- SCF + shuffled state
- SCF + trained projection

Pass condition:

```text
trained projection beats both no-state and shuffled-state on abs_rel,
and does not worsen temporal_delta or scale_drift.
```

## Step 3 — Critic reliability calibration

Train a lightweight calibration head so `conflict_score` predicts proposal
error rank or patch-oracle residual. Do not use it as a reroute override.
Use it only as a reliability feature inside SCF.

Pass condition:

```text
patch_oracle_gap_pp decreases, or SCF weights become better calibrated
against oracle expert/patch labels.
```

## Step 4 — core-state DEC, only if needed

If projection/calibration helps, draft a DEC for controlled core-state
training. The DEC must explicitly name any frozen files it wants to touch and
why a non-core alternative is insufficient.

Potential training targets:

- Memory fused-context supervised by SCF oracle weights;
- AnchorBank write/read stability supervised by temporal delta;
- Critic conflict score supervised by proposal error rank.

## Stop conditions

- Stop if trained projection does not beat no-state and shuffled-state.
- Stop if temporal/scale metrics worsen while abs_rel improves marginally.
- Stop if the result relies on fallback backend entries.
- Stop before any core edit unless the DEC is written and approved.
