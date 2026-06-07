# Dream3R RC Reproduction Notes

Date: 2026-06-05

## Scope

This document reproduces the release-candidate decision, not a paper-scale
benchmark sweep.

The selected RC is:

```text
frozen StatePrior + bounded residual refinement
```

The selected metrics are:

```text
KITTI abs-rel: 0.1448
ETH3D abs-rel: 0.1475
```

Metric direction: lower is better.

## Local Verification

Run local integration tests for the VGGT-Omega adapter and cache-admission
helpers:

```powershell
cd E:\Dream3R
python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
```

Expected result:

```text
27 passed
```

Inspect the mirrored selected-result artifact:

```powershell
Get-Content runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
Get-Content runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

## Server Verification

Use BUAA-Server GPU1 for all model execution:

```bash
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
export CUDA_VISIBLE_DEVICES=1
```

Run the integration tests on the server environment:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
```

Expected result:

```text
27 passed
```

Inspect the selected bounded candidate:

```bash
cat runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
cat runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

Expected selected values:

```text
correct-state KITTI/ETH3D: 0.1448 / 0.1475
shuffle-state KITTI/ETH3D: 0.1521 / 0.2467
```

## VGGT-Omega Admission Recheck

VGGT-Omega checkpoint:

```text
/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
sha256: c02da418b18bb01d0392598d3f6147366bcde1bb70fd08a5e3bf7925b0667934
```

Run oracle admission and emit 4-expert SCF caches:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.eval_vggt_omega_oracle_admission \
  --max-windows-per-domain 50 \
  --output runs/v22_admission/vggt_omega_oracle/oracle_admission_50x2_cache_20260605.json \
  --output-cache-dir runs/v22_admission/vggt_omega_cache_gate
```

Expected summary:

```text
KITTI: old oracle 0.1763 -> new oracle 0.1742, VGGT wins 2/50
ETH3D: old oracle 0.1419 -> new oracle 0.1158, VGGT wins 35/50
fallback_contamination_count: 0
failure_flags: []
```

Run the 4-expert SCF controls:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.train_scf_head \
  --cache runs/v22_admission/vggt_omega_cache_gate/scf_kitti_vggt_omega_cache.pt \
          runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt \
  --output-dir runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7 \
  --seed 7 --epochs 200
```

Repeat with:

```text
--no-state      -> runs/v22_admission/vggt_omega_cache_gate/scf_no_state_seed7
--shuffle-state -> runs/v22_admission/vggt_omega_cache_gate/scf_shuffle_state_seed7
```

Expected control result:

```text
correct-state: KITTI 0.2296, ETH3D 0.0570
no-state:      KITTI 0.1966, ETH3D 0.0583
shuffle-state: KITTI 0.2180, ETH3D 0.0598
```

Interpretation: VGGT-Omega is admitted as a real optional teacher backend, but
not as the RC model path because the state-causality control is not robust on
KITTI.

