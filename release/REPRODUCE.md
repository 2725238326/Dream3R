# Dream3R Reproduction Notes

Date: 2026-06-08

## Scope

This document reproduces the current complete official model package and the
stable fallback, not a paper-scale benchmark sweep.

The current complete package is:

```text
Dream3R v1.1.0
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
KITTI / ETH3D: 0.1448 / 0.0570
```

The stable fallback is:

```text
Dream3R v1.0-rc1 frozen StatePrior + bounded residual refinement
KITTI / ETH3D: 0.1448 / 0.1475
```

Metric direction: lower is better.

## Local v1.1 Completion Check

```powershell
cd E:\Dream3R
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json
python -B code\dream3r\scripts\verify_release_candidate.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py code\dream3r\tests\test_release_v11_smoke_model.py code\dream3r\tests\test_v11_demo_script.py -q
```

Expected:

```text
v1.1 verifier: pass
v1.1 smoke: pass
v1.1 demo: pass, demo_kitti.json + demo_eth3d.json written
v1.0 fallback verifier: pass
stable-core mode: git_diff
release tests: 14 passed
full test suite: 300 passed, 2 skipped
```

## Server v1.1 Completion Check

Use BUAA-Server GPU1 for model code:

```bash
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
export CUDA_VISIBLE_DEVICES=1
conda run -n dream3r python -B dream3r/scripts/verify_v11_release.py --root .
conda run -n dream3r python -B dream3r/scripts/smoke_v11_release_model.py --output runs/release/v11_smoke/smoke_v11_release_model.json
conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain kitti --output runs/release/v11_demo/demo_kitti.json
conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain eth3d --output runs/release/v11_demo/demo_eth3d.json
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain kitti --output runs/release/v11_cache_demo/cache_demo_kitti.json --max-entries 1 --device cuda
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain eth3d --output runs/release/v11_cache_demo/cache_demo_eth3d.json --max-entries 1 --device cuda
conda run -n dream3r python -B dream3r/scripts/verify_release_candidate.py --root .
conda run -n dream3r python -B -m pytest --assert=plain dream3r/tests/test_release_candidate_architecture.py dream3r/tests/test_release_candidate_verifier.py dream3r/tests/test_release_v11_architecture.py dream3r/tests/test_release_v11_verifier.py dream3r/tests/test_release_v11_smoke_model.py dream3r/tests/test_v11_demo_script.py -q
```

Expected:

```text
v1.1 verifier: pass
v1.1 smoke: pass
v1.1 demo: pass, demo_kitti.json + demo_eth3d.json written
v1.1 real-cache demo: pass, cache_demo_kitti.json + cache_demo_eth3d.json written
v1.0 fallback verifier: pass
stable-core mode: skipped_not_git_repo on the BUAA-Server package mirror
release tests: 14 passed
cache-demo focused tests: 11 passed
```

The cache demo is runtime-contract evidence over existing proposal-cache
entries. Do not report its one-entry AbsRel values as official benchmark
metrics.

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
