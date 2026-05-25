# CYCLE 20260525 Stage 5 S1 Demo Packaging (KITTI)

## Scope

Package the Stage 5 S1 expanded result into a runnable, reproducible demo:
load the trained router, pick two contrast windows from the 59-window
oracle, run all three real experts live, compare router's pick to oracle's
pick, and emit matplotlib figures + ASCII PLY pointmaps.

No new training. No new evaluation. The demo IS the integration test for
the S1 closure artifacts (DEC-20260525-003).

## Design

Agreed with the user (2026-05-25 evening):

- Live forward of three real experts (Fast3R, MASt3R, Spann3R), not
  precomputed metrics. Router runs the same `regime_stats` feature path
  as the trained checkpoint with frozen normalization stats from the
  checkpoint.
- Two contrast windows from
  `runs/stage5_s1_expand_oracle/oracle_expert_labels.json`:
  - Best MASt3R-winning window (lowest MASt3R abs_rel among MASt3R wins).
  - Best Spann3R-winning window (lowest Spann3R abs_rel among Spann3R
    wins).
- 3 matplotlib PNGs per window:
  - `fig1_pointmap.png` — 4-frame RGB strip + pred depth (viridis) + GT
    depth + abs error.
  - `fig2_routing.png` — regime probs (6 bars) + router expert logits
    (3 bars, highlighted on router's pick) + MATCH/MISMATCH label.
  - `fig3_expert_compare.png` — per-expert abs_rel bars (green where
    router and oracle agree, yellow=router only, blue=oracle only,
    grey=neither).
- ASCII PLY pointmap: standard PLY header + per-vertex `x y z r g b`
  with patch-center RGB sampled from the resized image. Scale-aligned to
  GT median (single scalar per window). No Open3D dependency on the
  server side; users can open in MeshLab / CloudCompare / Open3D locally.

## Files

New code:

- `code/dream3r/scripts/demo.py` — end-to-end script (router load,
  window selection, expert forward, metric/PLY/figures, summary JSON).
- `code/dream3r/DEMO.md` — server-side reproduction instructions.

Reused (no changes):

- `code/dream3r/data/kitti_long.py` (window loader)
- `code/dream3r/scripts/build_oracle_expert_labels.py` (metric +
  resize helpers)
- `code/dream3r/scripts/eval_router_ablation.py` (`_load_router`)
- `code/dream3r/scripts/train_router_only.py` (`_feature_tensor`)
- `code/dream3r/composer_experts/{fast3r,mast3r,spann3r}_adapter.py`

## CLI

```text
python -m dream3r.scripts.demo \
  --root /hdd3/kykt26/data \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
  --experts fast3r mast3r spann3r \
  --output-dir /hdd3/kykt26/code/dream3r/runs/demo_stage5_s1 \
  --window-frames 4 --image-size 224 --align-scale \
  --feature-mode regime_stats
```

The `dream3r` conda env on the server now has `matplotlib` installed
(via `pip install matplotlib`); this was the only missing dependency on
first run.

## Server Run

First run hit `ModuleNotFoundError: No module named 'matplotlib'` after
all three expert forwards succeeded. Installed matplotlib in the
`dream3r` env and re-ran end-to-end. Exit code 0.

Output:

```text
/hdd3/kykt26/code/dream3r/runs/demo_stage5_s1/
  summary.json
  window_00_2011_09_26_drive_0015_sync_03_oracle_mast3r/
    summary.json
    pointmap_pred.ply              (232 vertices)
    figures/
      fig1_pointmap.png
      fig2_routing.png
      fig3_expert_compare.png
  window_01_2011_09_28_drive_0165_sync_03_oracle_spann3r/
    summary.json
    pointmap_pred.ply              (264 vertices)
    figures/
      fig1_pointmap.png
      fig2_routing.png
      fig3_expert_compare.png
```

Both windows: router's choice matches oracle's choice.

Window 00 (oracle = MASt3R):

```text
sequence:        2011_09_26_drive_0015_sync_03
router_expert:   mast3r
oracle_expert:   mast3r            -> MATCH
per_expert_abs_rel:
  fast3r:  0.2466
  mast3r:  0.0745   <- chosen
  spann3r: 0.1808
router_logits:   [-139.17, 75.98, -0.83]
router_probs:    [0.0, 1.0, 4.4e-34]
ply_n_points:    232
```

Window 01 (oracle = Spann3R):

```text
sequence:        2011_09_28_drive_0165_sync_03
router_expert:   spann3r
oracle_expert:   spann3r           -> MATCH
per_expert_abs_rel:
  fast3r:  0.2818
  mast3r:  0.1448
  spann3r: 0.0951   <- chosen
router_logits:   [-4.46, -4.67, 5.11]
router_probs:    [7e-5, 6e-5, 0.9999]
ply_n_points:    264
```

## What This Changes

- Stage 5 S1 KITTI closure now has a runnable artifact, not just JSON
  files in `runs/`. Anyone with the checkpoint + KITTI raw data can
  reproduce the result and visually inspect the routing decisions.
- DEMO.md serves as the canonical reproduction reference for the demo
  goal in `mainwork.md §0`.

## Limitations

- This is a per-window visual demo, not a held-out evaluation. The
  oracle labels JSON used for window selection was the same one that
  trained the router; for held-out evidence, see the LOO results in
  DEC-20260525-003.
- The PLY uses single-scalar scale alignment to GT depth median per
  window; this matches the abs_rel metric definition but is not a
  pose-aware fusion across frames. For multi-frame fusion the user
  would need a separate pipeline.
- Critic / repair pipeline is not wired into the demo. The router's
  decision is the demo's headline; critic/repair behavior is covered by
  Stage 4's pipeline ablation (DEC-20260525-001), not re-run here.

## Boundary

Touched (new files):

- `code/dream3r/scripts/demo.py`
- `code/dream3r/DEMO.md`

Not touched:

- All v0.3/v0.5 core modules.
- All Stage 5 S1 artifacts (oracle, router checkpoint, LOO results).

New server artifacts:

- `/hdd3/kykt26/code/dream3r/runs/demo_stage5_s1/{summary.json, window_*/}`

New env state:

- `matplotlib` added to `dream3r` conda env (via `pip install matplotlib`).

## Conclusion

Stage 5 S1 closure (DEC-20260525-003) is now packaged as a runnable demo
with reproducible commands and visual artifacts. Demo confirms the
expected router behavior on both contrast windows: router agrees with
oracle on both, and the chosen expert's abs_rel is consistently the
lowest among the three on each window.
