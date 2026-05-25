# HANDOFF — 2026-05-25 evening (Track A + Cross-dataset closure)

**Mission:** Close two tracks in one session.

1. **Track A — Demo packaging**: produce an end-to-end runnable demo of Stage
   5 S1 (KITTI) with 2 contrast windows + matplotlib figures + PLY pointmaps.
2. **Cross-dataset closure**: extract the already-uploaded ETH3D archives,
   write the dataloader, build the ETH3D oracle, run the KITTI-trained
   router on ETH3D, and close Stage 5 with a forthcoming
   `DEC-20260525-006-cross-dataset-closure.md`.

Both are independent — interleave them across the server (long-running) and
local (code-writing) sides.

---

## 1. Reading list (in order, don't skip)

| # | File | Why |
|---|---|---|
| 1 | `CLAUDE.md` | Project rules: surgical changes, no model on Windows, scp pattern, ask before destructive ops |
| 2 | `mainwork.md` §5 + §7 | Stage status table + first-action chain |
| 3 | `mainwork/STATUS-20260525.md` | Snapshot of where we are (decision + ETH3D upload state) |
| 4 | `cycles/CYCLE-20260525-stage5-s1-kitti-expand.md` | The 59-window KITTI evidence the demo will showcase |
| 5 | `decisions/DEC-20260525-003-stage5-s1-expand-closure.md` | S1 headline numbers + honest claim wording |
| 6 | `decisions/DEC-20260525-005-deferred-cross-dataset-validation.md` | Trigger #2 fired; the "What is preserved for future pickup" section IS your work plan |
| 7 | `decisions/DEC-20260525-004-deferred-distilled-adapter-architecture.md` | Still deferred — do NOT open this line |
| 8 | `code/dream3r/scripts/build_oracle_expert_labels.py` | Pattern to mirror for ETH3D oracle (adapter loading, oracle metric, sequence sampling) |
| 9 | `code/dream3r/data/kitti_long.py` | Dataset interface to mirror in `eth3d_long.py` |
| 10 | `code/dream3r/scripts/eval_router_ablation.py` | How the router is evaluated; will reuse for ETH3D transfer eval |

---

## 2. Server access

Configured SSH alias on the Windows host (`27252`): `ssh BUAA-Server`.

Manual form for portability:

```text
user:        kykt26
host:        172.17.140.97   (BUAA internal IP — must be on campus or VPN)
port:        22
identity:    C:\Users\27252\.ssh\id_rsa_buaa
conda env:   dream3r
```

Code root on server: `/hdd3/kykt26/code/dream3r/dream3r/`
Data root on server: `/hdd3/kykt26/data/`
Checkpoints: `/hdd3/kykt26/checkpoints/`
Run artifacts: `/hdd3/kykt26/code/dream3r/runs/`

Run a server-side python command via:

```bash
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m dream3r.scripts.<script>"
```

---

## 3. Hard constraints (from CLAUDE.md)

- **Local Windows = edit + sync only**. NEVER run the model locally.
- Code sync: edit in `E:\Dream3R\code\dream3r\` → `scp` to
  `/hdd3/kykt26/code/dream3r/dream3r/<file>`.
- **Do not touch**: `code/dream3r/model.py`, `code/dream3r/anchor_bank.py`,
  `code/dream3r/nsa_attention.py`, `code/dream3r/bus.py`. Read them, don't
  edit unless fixing a real bug.
- Ask user before: downloading >500 MB, modifying v0.3/v0.5 core modules,
  picking between two reasonable design choices, training >4h with no
  convergence.

---

## 4. State that is already done (do NOT redo)

KITTI Stage 5 S1 is sealed and you reuse its artifacts directly:

```text
Router checkpoint:
  /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt
  (feature_mode=regime_stats, n_examples=59, final_accuracy=0.9661)

KITTI 59-window oracle:
  /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json
  (expert_order=[fast3r, mast3r, spann3r], counts: mast3r=31, spann3r=24, fast3r=4)

KITTI regime labels:
  /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json
  (246 KITTI sequences with 6D regime probabilities)

KITTI closure metrics (DEC-003 headline):
  closure-set abs_rel improvement: 7.60% over best single expert
  held-out LOO route accuracy:     78% (vs 33% chance)
```

ETH3D archives are uploaded but NOT extracted:

```text
/hdd3/kykt26/data/eth3d/low_res_many_view/raw/
  multi_view_training_rig.7z              1.7G  (rig images, distorted)
  multi_view_training_rig_undistorted.7z  1.5G  (rig images, undistorted — primary)
  multi_view_training_rig_occlusion.7z    405M  (occlusion masks)
  multi_view_training_rig_scan_eval.7z    289M  (ground-truth scan / depth for evaluation)

/hdd3/kykt26/data/eth3d/low_res_many_view/training/     (empty target dir, already mkdir'd)
```

---

## 5. Track A — Demo packaging (KITTI Stage 5 S1)

### A1. Design (agreed with user 2026-05-25 evening)

- **Live forward** (not pre-computed metrics). Load the router checkpoint,
  pick 2 KITTI windows from the 59-window oracle, run real Fast3R / MASt3R
  / Spann3R adapters, compare oracle's expert with router's choice, print
  abs_rel, save pointmap → PLY, save matplotlib figures.
- **2 contrast windows**:
  - Window where oracle's pick is **MASt3R** AND router agrees.
  - Window where oracle's pick is **Spann3R** AND router agrees.
  Picking from `oracle_expert_labels.json` is enough; sort by lowest abs_rel
  within each oracle class.
- **3 matplotlib PNG figures** per window:
  1. 4-frame RGB strip + predicted pointmap (rendered as depth viridis) +
     GT pointmap + abs error map.
  2. Bar chart: regime probabilities (6 bars) + router expert logits (3 bars).
  3. Critic score timeline (per frame) + repair decision label.
- **PLY**: standard ASCII PLY (no Open3D dependency on server). Open3D can
  render it locally if user wants interactive view.

### A2. Files to write

```text
E:\Dream3R\code\dream3r\scripts\demo.py                     [new]
E:\Dream3R\code\dream3r\DEMO.md                             [new]
E:\Dream3R\cycles\CYCLE-20260525-demo-package.md            [new, at the end]
```

### A3. demo.py skeleton

Reuse patterns from `build_oracle_expert_labels.py`:

- `EXPERT_CLASSES = {fast3r: Fast3RAdapter, mast3r: MASt3RAdapter, spann3r: Spann3RAdapter}`
- `_load_adapter(name)`: instantiate + `.load_checkpoint()` + verify `.is_loaded`
- Use `KITTILongSequenceDataset` with `windows_per_sample=1`
- `_pointmap_abs_rel(pred, target, mask, align_scale=True)` for metric

New code in demo.py:

- `_load_router(checkpoint_path)`: load Stage 5 S1 expanded router. Mirror
  `_load_router` in `eval_repair_pipeline_ablation.py` or `eval_router_ablation.py`.
  Return `(router_module, feature_mode)`. Verify `feature_mode=="regime_stats"`.
- `_select_demo_windows(oracle_json)`: pick best MASt3R-winning + best
  Spann3R-winning window. Returns list of `(sequence_name, oracle_expert)`.
- `_save_pointmap_ply(points_xyz, colors_rgb, path)`: standard ASCII PLY
  header + body.
- `_save_demo_figures(window_data, out_dir)`: 3 matplotlib subplots saved
  as PNGs (use Agg backend on server).

### A4. CLI

```text
python -m dream3r.scripts.demo \
  --root /hdd3/kykt26/data \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
  --experts fast3r mast3r spann3r \
  --output-dir /hdd3/kykt26/code/dream3r/runs/demo_stage5_s1 \
  --window-frames 4 --image-size 224 --align-scale
```

### A5. Success criteria

- demo.py runs to completion on server with exit code 0
- `runs/demo_stage5_s1/` contains 2 subdirs (one per window) each with
  `pointmap_pred.ply`, `figures/*.png` (3 PNGs), `summary.json` (router
  choice, oracle choice, abs_rel for each expert)
- DEMO.md command line reproduces the run end-to-end
- Both demo windows show router's choice == oracle's choice (a sanity
  visual; if not, that's still honest — record it in the cycle doc)

### A6. Out of scope for Track A

- No new training
- No critic/repair changes
- No new tests (the demo IS the test)

---

## 6. Cross-dataset closure (ETH3D Low-res many-view)

### C1. Extract on server

```bash
ssh BUAA-Server "cd /hdd3/kykt26/data/eth3d/low_res_many_view/training && \
  7z x ../raw/multi_view_training_rig_undistorted.7z && \
  7z x ../raw/multi_view_training_rig_scan_eval.7z && \
  ls -la"
```

The `_undistorted` (1.5G) + `_scan_eval` (289M) archives are sufficient for
oracle building. The `_rig` (distorted) and `_occlusion` archives are
optional — skip unless we need them later.

Expected scene structure (verify after extract):

```text
training/
  delivery_area/
    images/                  (or images_undistorted/)
    scan_clean.ply           (or similar, the GT scan)
    cameras.txt              (or COLMAP/calibration files)
  electro/
  forest/
  playground/
  terrains/
```

If structure differs, READ existing ETH3D documentation in the extracted
files (look for `README.txt` or similar) before assuming the layout. ETH3D
ships a COLMAP-format `cameras.txt`/`images.txt`/`points3D.txt` + a depth
ground-truth mesh per scene.

### C2. Write `code/dream3r/data/eth3d_long.py`

Mirror the interface of `code/dream3r/data/kitti_long.py`. Required keys
in each window dict (verify against what `build_oracle_expert_labels.py`
consumes downstream):

```python
{
    "images": Tensor[N, 3, H, W],         # float in [0, 1]
    "depth_gt": Tensor[N, H, W],          # metric depth
    "valid_mask": Tensor[N, H, W],        # bool
    "pointmap_gt": Tensor[N, H, W, 3],    # camera-space xyz
    "pointmap_mask": Tensor[N, H, W],     # bool
    "intrinsics": Tensor[N, 3, 3],
    "camera_poses": Tensor[N, 4, 4],      # world→camera (or camera→world; match KITTI convention)
    "regime": int,                        # see regime mapping below
    "conflict_label": float,              # 0 placeholder is fine for cross-dataset
    "repair_label": int,                  # 0 placeholder
    "region_label": int,                  # 0 placeholder
    "sequence_name": str,                 # for oracle key
}
```

**Regime label**: KITTI uses 6D probability vectors over
`outdoor_static / dense_sequential / sparse_view / dynamic_scene / indoor_static / feed_forward_manyview`.
For ETH3D scenes:

- `delivery_area, electro` → `indoor_static` (1.0 prob on that bucket)
- `forest, terrains, playground` → `outdoor_static` (1.0 prob)

Hardcode this mapping in a `code/dream3r/data/eth3d_regime_labels.json`
file mirroring the format of `stage3_regime_labels/regime_labels.json`.
(Or expose a CLI flag — but hardcoded is simpler for 5 scenes.)

**Important**: ETH3D Low-res many-view does NOT have OXTS/GPS poses like
KITTI. Use ETH3D's own camera extrinsics (from COLMAP-style
`images.txt`). Skip the `_oxts_pose` path in `kitti_long.py`.

### C3. Parameterize `build_oracle_expert_labels.py` for ETH3D

Two options:

**Option A (cleaner)**: add `--dataset {kitti,eth3d}` flag to
`build_oracle_expert_labels.py`, switch the dataset class via a factory.
Keep KITTI path untouched.

**Option B (faster)**: write
`code/dream3r/scripts/build_oracle_expert_labels_eth3d.py` as a
near-clone with ETH3D dataset wired in. Code duplication acceptable for a
one-off cross-dataset eval.

**Recommendation**: Option B unless you find yourself copy-pasting >100
lines. Option A becomes worth it if you ever add a third dataset.

### C4. Build ETH3D oracle

Aim for 20-50 windows total across 5 scenes (matches the KITTI 59-window
N). With 5 scenes, that's ~4-10 windows per scene at `--window-frames 4`.

Command (Option B form):

```text
python -m dream3r.scripts.build_oracle_expert_labels_eth3d \
  --root /hdd3/kykt26/data \
  --regime-labels /hdd3/kykt26/code/dream3r/data/eth3d_regime_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --experts fast3r mast3r spann3r \
  --max-per-scene 10 \
  --window-frames 4 --image-size 224 --align-scale
```

(`--max-per-scene` is a new flag — see C2 for design.)

### C5. Run KITTI-router transfer eval on ETH3D

Write `code/dream3r/scripts/eval_cross_domain_router.py`. It loads the
Stage 5 S1 expanded router and evaluates it on the ETH3D oracle:

```text
python -m dream3r.scripts.eval_cross_domain_router \
  --regime-labels /hdd3/kykt26/code/dream3r/data/eth3d_regime_labels.json \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_router/results.json \
  --feature-mode regime_stats
```

Mirror `eval_router_ablation.py`'s output schema. Report:

- `learned_router`: ETH3D mean abs_rel when using KITTI router's choice
- `oracle_router`: ETH3D mean abs_rel when using oracle's choice
- `always_<expert>`: per-expert baselines (best single → likely changes
  from MASt3R on KITTI to ?? on ETH3D — that itself is evidence)
- `relative_improvement_vs_best_single`
- `route_accuracy_vs_oracle`: fraction of ETH3D windows where router
  agrees with oracle (compare with KITTI's 78% LOO route accuracy)
- `route_distribution_shift`: counts of each expert under router vs
  under oracle on ETH3D

### C6. Honest claim wording

Two possible outcomes — both are publishable as evidence:

- **Strong transfer**: KITTI router predicts oracle's expert on ≥50% of
  ETH3D windows. Claim: "router transfers to cross-domain ETH3D with
  meaningful (X%) above-chance route accuracy."
- **Weak / no transfer**: route accuracy at or below chance (33%). Claim:
  "the KITTI-trained router does not transfer to ETH3D; the regime →
  expert mapping is domain-specific. Cross-dataset routing requires
  per-domain training data."

Either outcome is honest. Do NOT massage to a "router beats baseline"
claim if the data doesn't show it.

### C7. Write DEC-006

`decisions/DEC-20260525-006-cross-dataset-closure.md`. Must include:

- Headline: cross-dataset route accuracy + abs_rel margin on ETH3D
- Comparison with KITTI 78% LOO baseline
- Per-expert ETH3D baselines (best single on ETH3D might NOT be MASt3R)
- All run artifact paths
- Explicit non-claims (still not SOTA, still not ScanNet, still 5-scene
  ETH3D only)
- Boundary: what code was touched (eth3d_long.py, build_oracle_*_eth3d.py,
  eval_cross_domain_router.py)

### C8. Update mainwork.md

- `§5` Stage 5 row: `🔶 S1 KITTI sealed, cross-dataset re-activated` →
  `✅ done` once DEC-006 is written
- Add a subsection under "Stage 5 cross-dataset re-activation" with the
  ETH3D headline numbers (mirroring how DEC-003's numbers are quoted)

### C9. Write cycle doc

`cycles/CYCLE-20260525-stage5-cross-dataset.md`. Same structure as
`CYCLE-20260525-stage5-s1-kitti-expand.md`: Scope, Window Selection,
Oracle Build, Router Train (skip — no new training), Transfer Eval,
What This Changes, Limitations, Boundary, Conclusion.

---

## 7. Recommended execution order

Interleave to overlap server-bound work with local code-writing:

| Step | Side | Task | Blocking? |
|---|---|---|---|
| 1 | server | Extract ETH3D archives (C1) — runs while you code | no |
| 2 | local | Write demo.py + DEMO.md (A2-A3) | no |
| 3 | server | scp + run demo.py (A4), inspect output | server only |
| 4 | server | (after step 1) `ls` extracted ETH3D, document structure | quick |
| 5 | local | Write eth3d_long.py (C2) + eth3d_regime_labels.json | no |
| 6 | local | Write build_oracle_expert_labels_eth3d.py (C3) | no |
| 7 | server | Run ETH3D oracle build (C4) — long-running (~30-60 min) | server only |
| 8 | local | (during step 7) Write eval_cross_domain_router.py (C5) | no |
| 9 | server | Run cross-dataset router transfer eval (C5) | server only |
| 10 | local | Write DEC-006, cycle doc, update mainwork.md (C7-C9) | no |
| 11 | local | Write demo cycle doc (A2 last entry) | no |

Steps 3, 7, 9 are server-bound and run sequentially; steps 2, 5, 6, 8 fill
the local-side wait time.

---

## 8. Success criteria for the whole handoff

You can mark this handoff complete when:

- [ ] demo.py runs on server, produces 2 windows × (PLY + 3 PNGs + JSON)
- [ ] DEMO.md commands reproduce demo run from a clean checkout
- [ ] CYCLE-20260525-demo-package.md written
- [ ] ETH3D `training/` contains all 5 scene dirs after extraction
- [ ] eth3d_long.py loads at least 1 window successfully (write a quick
      smoke test in `code/dream3r/tests/test_eth3d_long.py` if useful)
- [ ] ETH3D oracle JSON exists with ≥20 windows and 3 experts evaluated
- [ ] Cross-dataset transfer eval JSON exists with all required fields
      (see C5)
- [ ] DEC-20260525-006 written with honest claim wording
- [ ] CYCLE-20260525-stage5-cross-dataset.md written
- [ ] mainwork.md §5 Stage 5 row updated to `✅ done`
- [ ] mainwork.md §7 first-action chain updated to point to next handoff
      (or marked "no active handoff")

---

## 9. Out of scope (do NOT start)

- **Track B (S5 tttLRM)** — defer to next session after Stage 5 fully
  closes
- **DEC-004 (distilled adapter)** — trigger not fired
- **ScanNet** — no data, do not download
- **S3 GaussianHead** — 1-week branch, separate scope
- **S2 Permanence** — needs KITTI tracking data, not in scope here
- Cross-dataset router **training** on ETH3D — only transfer eval. If
  transfer is weak and user wants to push, ASK before training a new
  router on ETH3D oracle (would require LOO too).

---

## 10. Risks / things that may bite

1. **ETH3D extraction may fail** if `7z` is not on the server PATH. Check
   with `ssh BUAA-Server "which 7z"` first. Fallback: `apt list --installed
   | grep -i 7z`, or use `p7zip-full`.
2. **ETH3D camera convention** may differ from KITTI (world→camera vs
   camera→world; OpenCV vs OpenGL). Verify by checking the first scene's
   `cameras.txt` + a reprojection sanity check before mass oracle build.
3. **Image size mismatch**: ETH3D Low-res many-view images are typically
   ~600x500 px or similar; KITTI is 1242x375. The pipeline resizes to
   `--image-size 224` for fair comparison, but if pointmap GT is at
   native resolution, you need to resize both consistently.
4. **Spann3R/Fast3R may OOM** on ETH3D if image aspect ratio differs
   significantly. If it OOMs, try `--image-size 192` first before
   debugging the adapter.
5. **Regime distribution shift**: ETH3D has 2 indoor + 3 outdoor scenes;
   KITTI is overwhelmingly outdoor. The hardcoded regime labels (C2) need
   to honestly reflect this — if `indoor_static` gets 1.0 prob on
   delivery_area and electro, those windows will route differently from
   any KITTI window the router has ever seen. That IS the cross-dataset
   test.

---

## 11. When you finish

Send the user a short summary message:

- Both tracks closed? List the artifact paths.
- Either track partially closed? Explain which step blocked and why.
- DEC-006 path + headline number.

Then mark the handoff todo list complete and propose Track B (S5
tttLRM) as the next session's work — or whatever else the user wants.
