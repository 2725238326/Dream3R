# Dream3R Cycle 034: Stabilization, Sync Discipline, and Dependency-Gated Planning

Status: **S1-S5 complete; W17-W19/W21-W22 demo evidence paths runnable**

Date: 2026-05-10

## Boundary

Server `/hdd3/kykt26/code/dream3r/` is a run/verification mirror only. It is not a git workspace. The local repository under `E:\kykt` is the version source.

Do not start work that requires:

- Installing packages
- Downloading checkpoints
- Pulling large external model assets
- Adding renderer/runtime dependencies such as `mamba_ssm`, `gsplat`, or 3D Gaussian rasterizers

Those items are allowed only after explicit approval.

## Current Baseline

Cycle 033 has W1-W16 implemented and verified on server. Cycle 034 added stabilization, Mamba hybrid recurrence, GaussianHead tensor contract, synthetic ablation/export tooling, and the first KITTI real-data smoke path.

Local source has been brought back in sync with the server-verified package. Use `scripts/sync_verify_server.ps1` for future pushes/pulls/verification. Server git must not be used.

## Immediate Work

### S1: Sync Discipline

Status: **done**

Goal: remove ambiguity about whether local or server code is authoritative.

Protocol:

1. Make edits locally.
2. Run `scripts/sync_verify_server.ps1 -Mode push`.
3. Run `scripts/sync_verify_server.ps1 -Mode test`.
4. For final validation, run `scripts/sync_verify_server.ps1 -Mode test -FullTests`.

Server git must not be used.

### S2: W15 Calibration Without New Dependencies

Status: **done**

Problem: geometric Critic signals now work, but the current conflict scale is a fixed constant. This is acceptable for a functional loop, not enough for robust training.

Tasks:

- Move `geometric_conflict_scale` and `geometric_clean_bias` into config/model parameters.
- Add tests that consistent pointmaps stay below a calibrated conflict threshold while shifted/depth-inconsistent pointmaps exceed it.
- Track `critic_geometric_log` metrics in evaluation so calibration can be monitored.
- Keep the existing no-checkpoint/no-install rule.

Exit criteria:

- `test_geometric_critic.py`, `test_evaluate_metrics.py`, smoke, and full tests pass.

Implementation notes:

- `critic_geometric_conflict_scale` and `critic_geometric_clean_bias` are now config/model parameters and thread into `Critic`.
- `Evaluator` now aggregates `critic_geometric_log` metrics for Sampson distance, covisibility inconsistency, and depth inconsistency.
- `test_geometric_critic.py` covers calibrated clean-vs-shifted pointmap behavior and config threading.
- Random smoke inputs can still produce high geometric conflict losses; this is now observable rather than hard-coded.

Verification:

- `dream3r.tests.test_geometric_critic`: pass
- `dream3r.tests.test_evaluate_metrics`: pass
- `dream3r.tests.test_critic_loop`: pass
- `dream3r.tests.test_loss_advancement`: pass
- `dream3r.smoke_test`: pass
- Full `dream3r.tests.test_*` suite: pass

### S3: W16 Stress Tests Without New Dependencies

Status: **done**

Problem: ISA slot poses are wired, but the tests are synthetic and short.

Tasks:

- Add a multi-window synthetic camera-motion test using only tensor pointmaps.
- Verify `object_slot_poses[..., :3]` follows controlled apparent translation.
- Verify pose-aware matching beats feature-only matching when features are ambiguous.
- Keep quaternion as identity until a real rotation update rule is justified.

Exit criteria:

- `test_isa_slots.py`, `test_permanence_v2.py`, sequence training, smoke, and full tests pass.

Implementation notes:

- `test_isa_slots.py` now includes a six-window synthetic camera-motion sequence.
- The stress test verifies slot pose translation follows controlled x/y motion over multiple windows.
- Pose-aware slot matching is now tested against a feature-only assignment when feature identity is unreliable.
- Quaternion remains identity-only; no rotation update rule was introduced.

Verification:

- `dream3r.tests.test_isa_slots`: pass
- `dream3r.tests.test_permanence_v2`: pass
- `dream3r.tests.test_sequence_training`: pass
- `dream3r.smoke_test`: pass
- Full `dream3r.tests.test_*` suite: pass

### S4: W17 Mamba Hybrid Path

Status: **done for demo; real `mamba_ssm` backend wired with PyTorch fallback**

W17 requires Mamba-style sequence modules. The server environment already has `mamba_ssm`, so no package installation was performed.

Scope:

- Add and exercise `state_recurrence_type="mamba_hybrid"`.
- Use `mamba_ssm.Mamba` when available.
- Keep PyTorch selective-scan fallback for local machines or broken kernels.
- Preserve the existing `"cross_attention"` recurrence as default.

Design contract:

- Add config key later: `state_recurrence_type`, allowed values:
  - `"cross_attention"`: current `StateTokenRecurrence`; default and always available.
  - `"mamba_hybrid"`: Mamba state-space evolution plus frame cross-attention, enabled only when configured.
- Keep recurrence input/output invariant:
  - `prev_state`: `[B, S_state, D_mem]`
  - `frame_tokens`: `[B, P, D_model]`
  - output: `[B, S_state, D_mem]`
- The hybrid block should have two responsibilities:
  - Temporal evolution over state tokens/windows through an O(N) state-space path.
  - Current-frame correction through cross-attention from state tokens to frame tokens.
- The fallback path preserves all current bus, AnchorBank, NSA, and drift-regularization contracts.
- `mamba_ssm` import happens inside `MambaHybridRecurrence.__init__`; module import remains safe without the package.

Implementation notes:

- `state_recurrence_type` now threads through config/model args.
- `build_state_recurrence()` returns the current cross-attention recurrence for `"cross_attention"`.
- `build_state_recurrence()` returns `MambaHybridRecurrence` for `"mamba_hybrid"`.
- `MambaHybridRecurrence` uses `mamba_ssm.Mamba(d_model=..., use_fast_path=False)` when available.
- The default fast path is disabled because the installed `causal_conv1d` extension has an ABI mismatch with `Mamba`'s fast CUDA call.
- If import or forward fails, it falls back to the internal PyTorch selective scan and records `backend_error`.
- `dream3r.demo_mamba_path` runs both `cross_attention` and `mamba_hybrid` across three windows for presentation.

Verification:

- `dream3r.tests.test_state_recurrence_factory`: pass
- `dream3r.demo_mamba_path`: pass; `mamba_hybrid` reports `backend: "mamba_ssm"` on server
- `dream3r.smoke_test`: pass
- Full `dream3r.tests.test_*` suite: pass

### S5: W18 Design Only

Status: **dependency-free tensor contract done; renderer implementation blocked by approval**

W18 requires a 3DGS output path and likely a renderer.

Allowed work:

- Define a pure tensor Gaussian parameter contract: means, scales/covariance, color, opacity, source anchor ids.
- Add a no-render shape-only test if useful.
- Document how AnchorBank entries map to Gaussian anchors.

Not allowed yet:

- Installing `gsplat` or rasterizers
- Implementing differentiable rendering
- Adding photometric render loss that depends on unavailable renderers

Tensor contract:

- Future optional output key: `gaussians`.
- Minimal shape-only schema:
  - `means`: `[B, G, 3]`, initialized from pointmap tokens and/or AnchorBank spatial payloads.
  - `scales`: `[B, G, 3]`, positive via `softplus` or clamped exponential.
  - `rotations`: `[B, G, 4]`, normalized quaternion; identity is acceptable for first non-rendering stage.
  - `colors`: `[B, G, 3]`, either image-conditioned when RGB is available or learned token projection.
  - `opacity`: `[B, G, 1]`, sigmoid confidence-like value.
  - `source_anchor_ids`: `[B, G]`, `-1` for frame-token Gaussians and bank index for AnchorBank-derived Gaussians.
- Anchor mapping:
  - Stable AnchorBank entries become persistent Gaussian candidates.
  - Active frame pointmap tokens can produce transient Gaussians.
  - `source_anchor_ids` is the bridge for pruning, stability scoring, and later render-loss attribution.
- Loss boundary:
  - Before renderer approval, only shape/range regularizers are allowed.
  - Photometric L1/SSIM render loss must wait for a real differentiable renderer.

Tests allowed before renderer approval:

- Shape-only Gaussian contract test with synthetic tensors.
- Range tests: positive scales, opacity in `[0, 1]`, normalized rotations.
- Anchor-id mapping test against synthetic AnchorBank indices.

Implementation gating:

- Do not import `gsplat`, `diff_gaussian_rasterization`, or any renderer at module import time.
- Do not add `rendered_images` to the model output until a renderer backend exists.
- Do not add a photometric objective that silently returns zero; that would hide missing renderer coverage.

Implementation notes:

- `gaussian_head.py` defines `GaussianHead`, a renderer-free tensor parameter head.
- Output contract covers means, positive scales, normalized quaternion rotations, RGB colors, opacity, and source anchor ids.
- The head is intentionally not wired into `Dream3R.forward()` yet, so no renderer-facing output or render loss is implied.

Verification:

- `dream3r.tests.test_gaussian_head_contract`: pass
- `dream3r.smoke_test`: pass
- Full `dream3r.tests.test_*` suite: pass

### S6: W21/W22 Evidence Pack

Status: **done for synthetic demo evidence**

Implementation notes:

- `ablate_recurrence.py` compares `baseline_cross_attention`, `mamba_hybrid`, `no_nsa`, and `no_stable_memory`.
- `visualize_ablation.py` turns ablation JSON into SVG charts and a markdown summary.
- `export_demo_artifacts.py` builds a showcase folder with demo JSON, ablation JSON, charts, manifest, and copied docs.
- The table is documented in `ABLATION_BASELINE.md`.

Verification:

- `dream3r.tests.test_visualization_contract`: pass
- `dream3r.tests.test_export_demo_artifacts_contract`: pass
- Full `dream3r.tests.test_*` suite: pass

### S7: W19 Real-Data Smoke

Status: **first slice done**

Implementation notes:

- `data_kitti.py` loads server KITTI rectified RGB/depth pairs.
- Depth maps are projected into sampled pointmaps with approximate scaled KITTI intrinsics.
- `evaluate_real_sequence.py` runs real windows through Dream3R and saves metric/debug JSON.
- The current first slice uses the no-backbone feature path with deterministic RGB/depth patch features, so it is a real-data integration smoke, not a trained quality benchmark.
- `REAL_DATA_SMOKE.md` records the command, output path, metrics, and interpretation boundary.

Verification:

- `dream3r.tests.test_kitti_loader_contract`: pass
- `dream3r.tests.test_real_sequence_eval_contract`: pass
- `dream3r.evaluate_real_sequence`: pass on two KITTI windows with `mamba_hybrid` backend `mamba_ssm`
- `dream3r.smoke_test`: pass
- Full `dream3r.tests.test_*` suite: pass

## Recommended Next Execution Order

1. Use `dream3r.demo_mamba_path` as the short synthetic architecture demo.
2. Use `dream3r.evaluate_real_sequence` as the real-data smoke demo.
3. Build the next evidence table from real-data ablations before adding new architecture breadth.
4. Stop before renderer work unless `gsplat` or another renderer backend is explicitly approved.

## Latest Verification Log

Completed on 2026-05-10/2026-05-11:

- `scripts/sync_verify_server.ps1 -Mode push`: local/server package files match.
- `scripts/sync_verify_server.ps1 -Mode verify`: local/server package files match.
- `scripts/sync_verify_server.ps1 -Mode test`: smoke pass.
- `scripts/sync_verify_server.ps1 -Mode test -FullTests`: smoke plus all `dream3r.tests.test_*` pass.

Additional dependency-free contract tests added:

- `dream3r.tests.test_state_recurrence_factory`: pass
- `dream3r.tests.test_gaussian_head_contract`: pass

Mamba demo added:

- `dream3r.demo_mamba_path`: pass; server output shows CUDA device and `mamba_hybrid` backend `mamba_ssm`.

Real-data smoke added:

- `dream3r.evaluate_real_sequence`: pass on KITTI `2011_09_26_drive_0001_sync_02`, two windows, CUDA, `mamba_hybrid` backend `mamba_ssm`.
- Output JSON: `/hdd3/kykt26/code/dream3r/demo_artifacts/real_sequence/kitti_metrics.json`.
