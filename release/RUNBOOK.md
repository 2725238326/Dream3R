# Dream3R RC Runbook

Date: 2026-06-05
Version: `v1.0-rc1`

Start from:

```text
release/OFFICIAL_VERSION.md
release/ARCHITECTURE_V1_0_RC.md
```

Run the local release verifier:

```powershell
python -B code\dream3r\scripts\verify_release_candidate.py
```

## Server

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
```

Use GPU1 for model code:

```text
CUDA_VISIBLE_DEVICES=1
```

## Selected Release Evidence

Bounded baseline:

```text
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

Key metrics:

```text
correct-state KITTI/ETH3D: 0.1448 / 0.1475
shuffle-state KITTI/ETH3D: 0.1521 / 0.2467
```

## VGGT-Omega Gate Evidence

```text
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json
runs/v22_admission/vggt_omega_oracle/oracle_admission_50x2_cache_20260605.json
runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7/results.json
runs/v22_admission/vggt_omega_cache_gate/scf_no_state_seed7/results.json
runs/v22_admission/vggt_omega_cache_gate/scf_shuffle_state_seed7/results.json
```

VGGT-Omega is admitted as a real teacher backend, not as the RC model.

## Re-run VGGT Oracle Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.eval_vggt_omega_oracle_admission \
  --max-windows-per-domain 50 \
  --output runs/v22_admission/vggt_omega_oracle/oracle_admission_50x2_cache_20260605.json \
  --output-cache-dir runs/v22_admission/vggt_omega_cache_gate
```

## Re-run VGGT Control Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.train_scf_head \
  --cache runs/v22_admission/vggt_omega_cache_gate/scf_kitti_vggt_omega_cache.pt \
          runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt \
  --output-dir runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7 \
  --seed 7 --epochs 200
```

Repeat with `--no-state` and `--shuffle-state` for controls.
