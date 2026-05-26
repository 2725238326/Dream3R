# HANDOFF — 2026-05-27 morning (Overnight Pipeline Verification)

**Mission:** Verify the overnight pipeline that ran during the 2026-05-26
evening session, harvest numbers, and update DEC-007 + CYCLE with the
new evidence. No new training is expected.

The overnight pipeline executed two independent investigations:

- **A. ETH3D dense-GT oracle** — rebuilt the 50-window ETH3D oracle
  using `rig_scan_eval/*.ply` laser-scan depth instead of SfM-sparse
  `points3D.txt` points. Re-ran (a) ETH3D zero-shot transfer with
  `router_kitti_robust_v1`, retrained (b) ETH3D-only and (c) Joint v3
  with the new oracle.
- **C. Multi-seed sweep** — re-trained (a) KITTI-robust, (b)
  ETH3D-only (sparse oracle, unchanged), and (c) Joint v2 across 5
  seeds {7, 11, 13, 17, 19} with LOO each. 15 train+LOO runs total.

---

## 1. First action

Read this file. Then:

```text
ssh BUAA-Server "cat /hdd3/kykt26/code/dream3r/runs/overnight_20260526/progress.log"
```

That log records `START / OK / FAIL` for every step. Search for
`FAIL` first — if any, the corresponding `<step>.log` in the same
directory has stderr/stdout.

If everything is `OK`, jump to §3 (harvest) and §4 (write up). If
something failed, see §6 (failure triage).

---

## 2. Background (why this matters)

DEC-006/007 ETH3D numbers (54% / 48% LOO route accuracy, +5.78%
rel_imp for Joint v2) were computed against an oracle built from
**SfM-sparse `points3D.txt`** (~10 patches per window). User raised
two concerns that motivated tonight's pipeline:

1. **GT density imbalance:** KITTI windows have ~200 patches/window
   GT (LiDAR), ETH3D had ~10 (SfM). The ETH3D oracle label is
   computed on a noisier signal; the ETH3D numbers may move when
   evaluated against denser GT.
2. **Single-seed reporting:** all DEC-007 numbers came from seed=7.
   Same-pipeline different-seed variance is unknown.

A addresses concern 1, C addresses concern 2. Both are pure
validation passes for the DEC-007 honest claim — they don't open new
directions.

---

## 3. Harvest checklist

### A. Dense oracle results

```text
ssh BUAA-Server "conda run -n dream3r python -c '
import json
for path in [
    \"/hdd3/kykt26/code/dream3r/runs/eth3d_dense_oracle/oracle_expert_labels.json\",
    \"/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d_dense/results.json\",
    \"/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_ablation/results.json\",
    \"/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_loo/results_loo.json\",
    \"/hdd3/kykt26/code/dream3r/runs/router_joint_v3_dense_loo/results_loo.json\",
]:
    print(\"===\", path, \"===\")
    d = json.load(open(path))
    print(json.dumps({k: v for k, v in d.items() if k not in (\"per_fold\", \"routes\", \"top_regimes\", \"sequences\", \"metrics\")}, indent=2)[:1200])
'"
```

Compare against the sparse-oracle baselines from DEC-007:

| metric | sparse (DEC-007) | dense (today) | Δ |
|---|---|---|---|
| ETH3D oracle counts | spann3r=23, mast3r=16, fast3r=11 | ? | ? |
| (a) ETH3D zero-shot route acc | 32% | ? | ? |
| (b) ETH3D-only LOO route acc | 54% | ? | ? |
| (b) ETH3D-only LOO rel_imp | +6.39% | ? | ? |
| (c) Joint v3 KITTI LOO route acc | 71.19% (v2 sparse) | ? | ? |
| (c) Joint v3 ETH3D LOO route acc | 48.00% (v2 sparse) | ? | ? |

**Honest claim impact:** if dense numbers stay within ±5pp of sparse,
DEC-007 claim stands. If they move >10pp, the original sparse oracle
was noisy and we need to revise the headline (oracle_quality caveat).

### C. Multi-seed sweep results

```text
ssh BUAA-Server "conda run -n dream3r python -c '
import json
from pathlib import Path
import statistics
runs = Path(\"/hdd3/kykt26/code/dream3r/runs/seed_sweep\")
for prefix, key in [
    (\"kitti_robust\",  \"loo_route_accuracy_vs_oracle\"),
    (\"eth3d_only\",   \"loo_route_accuracy_vs_oracle\"),
    (\"joint_v2\",     \"per_domain_loo_route_accuracy\"),
]:
    vals_acc = []
    vals_relimp = []
    for seed in (7, 11, 13, 17, 19):
        p = runs / f\"{prefix}_s{seed}_loo\" / \"results_loo.json\"
        if not p.exists():
            print(f\"  MISSING: {p}\")
            continue
        d = json.load(open(p))
        if prefix == \"joint_v2\":
            vals_acc.append(d[\"per_domain_loo_route_accuracy\"])
            vals_relimp.append(d[\"per_domain_rel_improvement_vs_best_single\"])
        else:
            vals_acc.append(d[\"loo_route_accuracy_vs_oracle\"])
            vals_relimp.append(d[\"relative_improvement_vs_best_single\"])
    print(f\"--- {prefix} ---\")
    print(\"  per-seed acc :\", vals_acc)
    print(\"  per-seed relimp:\", vals_relimp)
    if isinstance(vals_acc[0], float):
        print(f\"  mean={statistics.mean(vals_acc):.4f}  std={statistics.stdev(vals_acc):.4f}\")
'"
```

Report `mean ± std` for each experiment. Acceptance gate: claim is
seed-robust if std < 5pp on route accuracy.

---

## 4. Documentation updates (after numbers in hand)

### 4.1 Update DEC-20260526-007

Add a third addendum after "Per-Domain Norm Refinement → Joint v2":

```markdown
## Addendum (2026-05-27): Dense GT + Seed Robustness

### Dense GT oracle
- Rebuilt ETH3D 50w oracle using rig_scan_eval/*.ply (dense laser
  scan) instead of SfM-sparse points3D.txt.
- Dense oracle counts:        [fill in]
- Sparse oracle counts (DEC-006): spann3r=23, mast3r=16, fast3r=11
- ETH3D LOO numbers (dense):  [fill in]
- Headline claim revision:    [stand or revise based on Δ]

### Seed sweep
- 5 seeds × 3 experiments × LOO.
- (a) KITTI-robust LOO route acc: mean=? std=?
- (b) ETH3D-only LOO route acc:   mean=? std=?
- (c) Joint v2 KITTI LOO:         mean=? std=?
- (c) Joint v2 ETH3D LOO:         mean=? std=?
- Conclusion: claim is/is-not seed-robust within X pp.
```

### 4.2 Update CYCLE-20260526-cross-domain-router-retrain

Add a third addendum "Dense GT + Multi-seed (overnight)" with the
new tables.

### 4.3 Update mainwork.md §5

In the cross-domain follow-up subsection, replace the joint v2 row
with `joint v3 (dense + per-domain norm)` if those numbers are the
new canonical, OR add it as a separate row. Recommend keeping v2
sparse + v3 dense both visible — they are different oracles.

---

## 5. Server artifacts

New checkpoints (each ~5-10MB, no cleanup needed):

```text
/hdd3/kykt26/checkpoints/router_eth3d_v2_dense/latest.pt
/hdd3/kykt26/checkpoints/router_joint_v3_dense/latest.pt
/hdd3/kykt26/checkpoints/seed_sweep/{kitti_robust,eth3d_only,joint_v2}_s{7,11,13,17,19}/latest.pt
```

New results JSONs:

```text
/hdd3/kykt26/code/dream3r/runs/eth3d_dense_oracle/oracle_expert_labels.json
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d_dense/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/router_joint_v3_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/seed_sweep/<prefix>_s<seed>_loo/results_loo.json  # 15 files
```

---

## 6. Failure triage

If `progress.log` shows `FAIL` on any step:

| Step | Likely cause | Action |
|---|---|---|
| A0_dense_oracle_build | PLY parse / OOM on 200K-pt projection | inspect `A0_dense_oracle_build.log`; sanity already passed for delivery_area, so likely an electro/forest/playground/terrains scene-specific issue. Re-run with `--scenes <one scene>` to isolate. |
| A1_kitti_robust_eth3d_dense_transfer | feature_mode mismatch | Check `_load_router` accepts `regime_stats_robust`; should already after evening edits. |
| A2/A3 train | router NaN / loss explosion | rare; lower lr to 0.02. |
| C_*_train | seed not exposed in CLI | Already added seed CLI tonight; should not occur. |
| C_*_loo | LOO fold OOM on per-fold normalization | Reduce batch_size; LOO was 5-7min in evening's run. |

The orchestrator does **not** abort on later-step failure (each `run_step`
returns 0/1 but the loop continues). So a single failed seed in C is
OK — just exclude it from the mean.

---

## 7. Out of scope

- Do not start new experiments based on tonight's numbers without
  user approval.
- Do not modify v0.3/v0.5 core.
- Do not change KITTI windows or ETH3D regime labels.
- Track B (tttLRM) remains parked.

---

## 8. When you finish

Send the user:

1. A/C completed or which steps failed.
2. Dense vs sparse Δ summary table.
3. Multi-seed mean ± std table.
4. Whether DEC-007 honest claim changes (and exact wording if so).
5. Updated DEC-007 + CYCLE + mainwork.md commit ready.
