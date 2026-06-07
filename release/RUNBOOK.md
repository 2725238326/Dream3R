# Dream3R Effective Model Runbook

Date: 2026-06-08
Version: `v1.1.0`
Stable fallback: `v1.0-rc1`

Start from:

```text
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/USABLE_MODEL_V1_1.md
release/OFFICIAL_VERSION.md
release/ARCHITECTURE_STATUS.json
```

## Local Completion Check

Run the current effective model verifier:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
```

Run the full-model smoke. This proves both v1.1 domain branches execute with
the documented proposal-bank runtime contract:

```powershell
python -B code\dream3r\scripts\smoke_v11_release_model.py `
  --output runs\release\v11_smoke\smoke_v11_release_model.json
```

Keep the v1.0 stable fallback verifier green:

```powershell
python -B code\dream3r\scripts\verify_release_candidate.py --root .
```

Targeted tests:

```powershell
python -B -m pytest --assert=plain `
  code\dream3r\tests\test_release_v11_architecture.py `
  code\dream3r\tests\test_release_v11_verifier.py `
  code\dream3r\tests\test_release_v11_smoke_model.py `
  code\dream3r\tests\test_release_candidate_architecture.py `
  code\dream3r\tests\test_release_candidate_verifier.py -q
```

Expected current effective model identity:

```text
version: v1.1.0
candidate: domain_conditional_vggt_teacher
KITTI / ETH3D: 0.1448 / 0.0570
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

Server verifier/smoke:

```text
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -B dream3r/scripts/verify_v11_release.py --root . --skip-frozen-core
conda run -n dream3r python -B dream3r/scripts/smoke_v11_release_model.py \
  --output runs/release/v11_smoke/smoke_v11_release_model.json
conda run -n dream3r python -B dream3r/scripts/verify_release_candidate.py --root . --skip-frozen-core
```

## Effective Release Evidence

v1.1 domain-conditional gate:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Key metrics:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Correct-state beats no-state and shuffle-state on both domains.

## Stable Fallback Evidence

Bounded baseline:

```text
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

v1.0 fallback metrics:

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

VGGT-Omega is admitted as a real teacher/proposal backend. In the current
effective v1.1 architecture it is used only through the ETH3D
domain-conditional branch, not as Dream3R by itself.

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
