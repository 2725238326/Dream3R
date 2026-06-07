# Cycle 20260604: VGGT-Omega Admission Runner

Date: 2026-06-04
Status: closed one-window real-backend admitted
Decision: `decisions/DEC-20260604-035-vggt-omega-admission-runner.md`

## Goal

Return from the negative Qwen semantic-control gates to the main Dream3R
proposal-bank path by making VGGT-Omega admission resumable and auditable.

## Actions

1. Added a non-core staging runner:

```text
code/dream3r/scripts/stage_vggt_omega_admission.py
```

2. Added integration tests for blocked and ready staging states:

```text
code/dream3r/tests/test_vggt_integration.py
```

3. Synchronized the runner/test to BUAA-Server and ran the staging command in
the `dream3r` conda environment.

4. Uploaded the user-provided checkpoint to the approved server path and fixed
the smoke adapter to accept VGGT-Omega's batched `depth_conf` shape.

## Verification

Local:

```text
22 passed
```

Server:

```text
22 passed
```

Server artifact before checkpoint upload:

```text
runs/v22_admission/vggt_omega_smoke/stage_status_20260604.json
```

Server result before checkpoint upload:

```text
status: blocked
backend: not_run
hf_token_present: false
failure_flags:
  - hf_token_missing
  - checkpoint_missing:/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
```

Server after checkpoint upload:

```text
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.stage.json
runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.pt
```

Result:

```text
status: admitted
backend: real
fallback_contamination_count: 0
pointmap_shape: [2, 265216, 3]
confidence_shape: [2, 265216, 1]
runtime_ms: 17962.720496580005
vram_mb: 7143.912109375
```

## Boundary

VGGT-Omega model inference ran only for a two-frame one-window smoke on
BUAA-Server GPU1. No checkpoint was downloaded through HF. No frozen core file
was edited. No fallback/stub backend is accepted by the admission path.

## Next

Build a tiny cache with the existing proposal bank plus VGGT-Omega on 5-10 KITTI
windows and, if cheap, 5-10 ETH3D windows. Promotion requires oracle gain versus
the current MASt3R/Fast3R/Spann3R bank and zero fallback contamination.
