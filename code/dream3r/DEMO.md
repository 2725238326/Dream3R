# Dream3R Demo — Stage 5 S1 (KITTI)

End-to-end runnable demo of the Stage 5 S1 expanded router + three real experts
(Fast3R / MASt3R / Spann3R) on KITTI long windows.

The demo loads the trained router, picks two contrast windows from the 59-window
expanded oracle, runs every expert live, compares route choices against the
oracle, and emits matplotlib figures + an ASCII PLY pointmap per window.

## What the demo shows

Two contrast windows from `oracle_expert_labels.json`:

1. **MASt3R-winning window** — oracle's lowest MASt3R abs_rel among MASt3R wins.
2. **Spann3R-winning window** — oracle's lowest Spann3R abs_rel among Spann3R wins.

Per window we save:

- `pointmap_pred.ply` — ASCII PLY of the router-chosen expert's pointmap with
  patch-center RGB. Scale-aligned to GT median (single scalar).
- `figures/fig1_pointmap.png` — 4-frame RGB strip + predicted depth (viridis) +
  GT depth + abs error map.
- `figures/fig2_routing.png` — regime probabilities (6 bars) + router expert
  logits (3 bars, highlighted: green=router's choice). Title labels MATCH vs
  MISMATCH against oracle.
- `figures/fig3_expert_compare.png` — per-expert abs_rel on this window
  (green=router&oracle agreement, yellow=router only, blue=oracle only,
  grey=neither).
- `summary.json` — sequence, router choice, oracle choice, per-expert abs_rel,
  router logits, regime probs, PLY point count.

Top-level `summary.json` lists both windows + reproduction config.

## Server prerequisites

These artifacts must already exist on the server (all from the Stage 5 S1
expanded closure, DEC-20260525-003):

```text
/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json
/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json
/hdd3/kykt26/data/kitti/rectified/...
```

Expert checkpoints (per existing adapter defaults):

```text
/hdd3/kykt26/checkpoints/fast3r/Fast3R_ViT_Large_512/model.safetensors
/hdd3/kykt26/checkpoints/mast3r/...
/hdd3/kykt26/checkpoints/spann3r/...
```

Conda env: `dream3r` (matplotlib + numpy + torch + PIL + the expert deps).

## Reproduce command

```bash
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r \
  python -m dream3r.scripts.demo \
    --root /hdd3/kykt26/data \
    --regime-labels /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json \
    --oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
    --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
    --experts fast3r mast3r spann3r \
    --output-dir /hdd3/kykt26/code/dream3r/runs/demo_stage5_s1 \
    --window-frames 4 \
    --image-size 224 \
    --align-scale \
    --feature-mode regime_stats"
```

`--align-scale` enables median scale alignment per window for the abs_rel
metric (matches the oracle build setting).

## Expected output layout

```text
/hdd3/kykt26/code/dream3r/runs/demo_stage5_s1/
  summary.json
  window_00_<sequence>_oracle_mast3r/
    summary.json
    pointmap_pred.ply
    figures/
      fig1_pointmap.png
      fig2_routing.png
      fig3_expert_compare.png
  window_01_<sequence>_oracle_spann3r/
    summary.json
    pointmap_pred.ply
    figures/
      fig1_pointmap.png
      fig2_routing.png
      fig3_expert_compare.png
```

## Viewing the PLY

The PLY is plain ASCII so any viewer works. Locally:

```python
import open3d as o3d
pc = o3d.io.read_point_cloud("window_00_*/pointmap_pred.ply")
o3d.visualization.draw_geometries([pc])
```

Or load into MeshLab / CloudCompare directly.

## What this demo is and is not

- Live forward of three real experts (no precomputed metrics).
- Router runs the same `regime_stats` feature path as the trained checkpoint
  (frozen normalization stats loaded from the checkpoint).
- abs_rel uses `_pointmap_abs_rel` from the oracle build script — same metric
  as DEC-003 headline numbers.
- This is a per-window visualization, **not** a held-out eval. The oracle JSON
  the demo selects from was used during router training; the LOO held-out
  result (78% route accuracy) is in DEC-20260525-003.
- Not SOTA. Not cross-dataset (see cross-dataset closure for that).
