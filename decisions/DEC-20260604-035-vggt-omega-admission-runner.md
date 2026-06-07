# DEC-20260604-035: VGGT-Omega admission runner

Date: 2026-06-04
Status: accepted; one-window real-backend smoke admitted after checkpoint upload
Scope: Dream3R v2.2 teacher/proposal-bank admission

## Context

DEC-20260604-034 closed the current Qwen semantic Critic-prior gate as
diagnostic-negative. The architecture lane should therefore return to the
proposal-bank path, especially VGGT-Omega teacher admission from DEC-026.

DEC-026 already staged public VGGT-Omega code and added a one-window smoke
script, but real admission was blocked on the missing approved checkpoint:

```text
/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
```

## Decision

Add a small, reversible staging runner around the existing smoke script. The
runner checks the upstream repo, smoke image list, checkpoint path, and
Hugging Face token state before any model load. If checkpoint access is missing,
it writes a machine-readable blocked status rather than accepting fallback or
stub outputs.

This does not edit frozen core files, does not train, and does not claim
VGGT-Omega admission.

After the user provided a local `vggt_omega_1b_512.pt`, upload it to the
approved BUAA-Server checkpoint path and run the real one-window smoke on GPU1.

## Implementation

Changed:

```text
code/dream3r/scripts/stage_vggt_omega_admission.py
code/dream3r/scripts/smoke_vggt_omega_adapter.py
code/dream3r/tests/test_vggt_integration.py
```

Server artifact:

```text
runs/v22_admission/vggt_omega_smoke/stage_status_20260604.json
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.stage.json
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.pt
```

The runner can:

1. report missing repo/image-list/checkpoint/token states;
2. optionally download `facebook/VGGT-Omega` / `vggt_omega_1b_512.pt` when a
   valid token is already available;
3. normalize the staged checkpoint to the existing `model.pt` path;
4. invoke `dream3r.scripts.smoke_vggt_omega_adapter` only when prerequisites
   are present.

## Verification

Local:

```text
python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
# 22 passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B -m pytest --assert=plain \
  dream3r/tests/test_vggt_integration.py -q
# 22 passed
```

Server staging run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.stage_vggt_omega_admission \
  --download --run-smoke \
  --output runs/v22_admission/vggt_omega_smoke/stage_status_20260604.json
```

Initial result before checkpoint upload:

```text
status: blocked
backend: not_run
failure_flags:
  - hf_token_missing
  - checkpoint_missing:/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
```

Checkpoint upload:

```text
local:  E:\Download\vggt_omega_1b_512.pt
server: /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
size:   4576706117
sha256: c02da418b18bb01d0392598d3f6147366bcde1bb70fd08a5e3bf7925b0667934
```

Real smoke after a minimal `depth_conf` shape fix:

```text
status: admitted
backend: real
fallback_contamination_count: 0
device: cuda
pointmap_shape: [2, 265216, 3]
confidence_shape: [2, 265216, 1]
depth_conf_shape: [1, 2, 448, 592]
runtime_ms: 17962.720496580005
vram_mb: 7143.912109375
pt_output: runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.pt
```

## Verdict

VGGT-Omega one-window real-backend admission is now open. This is not a full
cache/admission result yet; it only proves that the uploaded checkpoint loads,
runs on BUAA-Server GPU1, emits pointmaps/cameras/tokens, and avoids fallback
contamination. The next gate is a tiny KITTI/ETH3D cache plus oracle admission
against the existing MASt3R/Fast3R/Spann3R bank.
