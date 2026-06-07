# Cycle: v1.1 Usable Model Package

Date: 2026-06-07

## Goal

Deliver a usable 3R model surface tonight without misrepresenting experimental Foundation3R as production-ready.

## Completed

- Added `Dream3RDomainConditionalRelease`.
- Added v1.1 import builder.
- Added v1.1 verifier.
- Added v1.1 usable-model documentation.
- Updated artifact manifest.
- Synced model code, tests, verifier, and release docs to BUAA-Server.

## Result

```text
v1.1-rc1 usable model:
  KITTI -> v1.0-rc1 branch, 0.1448
  ETH3D -> VGGT-Omega-expanded SCF branch, 0.0570

controls:
  KITTI  0.1448 / 0.1553 / 0.1521
  ETH3D  0.0570 / 0.0583 / 0.0598
```

## Verification

```text
local tests: 6 passed
local verify_v11_release: pass
server tests: 6 passed
server verify_v11_release: pass
server verify_release_candidate v1.0: pass
```

## Next

If the goal is demo/release tonight, use v1.1-rc1. If the goal is a proposal-free foundation model, continue Foundation3R separately and do not block the usable package on it.

