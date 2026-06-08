# Dream3R RC Verification Report

Date: 2026-06-05

Update 2026-06-08: v1.1.0 real proposal-cache runtime demo added. The new
entrypoint `code/dream3r/scripts/run_dream3r_v11_cache_demo.py` consumes
existing SCF/VGGT-Omega cache entries, validates strict branch expert order,
adapts cache `d_memory`, and writes JSON reports under
`runs/release/v11_cache_demo/`. Fresh local focused checks passed
`11 passed`. Fresh BUAA-Server GPU1 checks passed: KITTI real-cache demo,
ETH3D real-cache demo, focused tests `11 passed`, and cache-demo JSON parse.
This is runtime-contract evidence, not a benchmark rerun.

Update 2026-06-08: v1.1.0 is now the current complete official model package.
The package has an effective architecture doc, model card, architecture
diagram, verifier, full-model smoke, one-command branch demo, and runbook.
Fresh local checks passed: v1.1 verifier `pass`, v1.1 smoke `pass`, v1.1 demo
KITTI/ETH3D `pass`, v1.0 fallback verifier `pass`, release tests `14 passed`,
artifact/demo JSON parse `pass`, and `git diff --check` reports no whitespace
errors. Historical full-suite evidence remains `300 passed, 2 skipped`.
Fresh BUAA-Server GPU1 checks passed: demo KITTI/ETH3D `pass`, v1.1 verifier
`pass`, v1.0 fallback verifier `pass`, release tests `14 passed`, v1.2
architecture tests `4 passed`, and artifact/demo JSON parse `pass`.

Current complete model:

```text
Dream3R v1.1.0
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
KITTI / ETH3D: 0.1448 / 0.0570
```

Update 2026-06-06: after adding the official v1.0-rc1 architecture wrapper,
the full local test suite and BUAA-Server GPU1 training-smoke subset were run.
The RC remains unchanged.

Update 2026-06-06: a domain-conditional VGGT teacher candidate was evaluated.
It reports KITTI `0.1448` via v1.0-rc1 and ETH3D `0.0570` via VGGT-expanded
SCF correct-state. It was experimental at this point because it still needed a
unified domain-conditional cache/control rerun; that later gate passed and was
packaged as v1.1.0.

Update 2026-06-06: the unified domain-conditional gate was then run locally and
on BUAA-Server. It passes all declared state/no-state/shuffle controls and
reports `promotable_to_official=true`; it was then promoted into the official
`v1.1.0` package, while `v1.0-rc1` remains stable fallback.

## Current Verdict

Dream3R has a complete official model package:

```text
v1.1.0 domain_conditional_vggt_teacher
```

Metric direction: lower is better.

Completion entrypoints:

```text
release/COMPLETE_MODEL_V1_1.md
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/MODEL_CARD_V1_1.md
release/ARCHITECTURE_DIAGRAM_V1_1.md
release/AFTERNOON_DELIVERABLE_V1_1.md
code/dream3r/scripts/verify_v11_release.py
code/dream3r/scripts/smoke_v11_release_model.py
code/dream3r/scripts/run_dream3r_v11_demo.py
code/dream3r/scripts/run_dream3r_v11_cache_demo.py
```

## Stable Fallback Verdict

Dream3R has a release candidate:

```text
frozen StatePrior + bounded residual refinement
```

The candidate is selected because it is the strongest controlled state-causal
path currently available:

```text
KITTI abs-rel: 0.1448
ETH3D abs-rel: 0.1475
```

Metric direction: lower is better.

## Release Candidate Evidence

Selected server artifacts:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

State-causality control:

```text
correct-state KITTI/ETH3D: 0.1448 / 0.1475
shuffle-state KITTI/ETH3D: 0.1521 / 0.2467
```

The correct-state result remains better than the shuffled-state control,
especially on ETH3D.

## VGGT-Omega Gate Evidence

VGGT-Omega smoke test:

```text
backend: real
fallback_contamination_count: 0
runtime: 17.96s
VRAM: 7143.91 MB
```

Oracle admission, 50 KITTI + 50 ETH3D windows:

```text
KITTI old oracle 0.1763 -> new oracle 0.1742, gain 1.18%, VGGT wins 2/50
ETH3D old oracle 0.1419 -> new oracle 0.1158, gain 18.35%, VGGT wins 35/50
fallback_contamination_count: 0
failure_flags: []
```

4-expert SCF controls:

```text
correct-state: KITTI 0.2296, ETH3D 0.0570
no-state:      KITTI 0.1966, ETH3D 0.0583
shuffle-state: KITTI 0.2180, ETH3D 0.0598
```

Interpretation: VGGT-Omega is a valid optional teacher and is strong on
ETH3D/indoor-like windows, but it is not a standalone release model path
because it fails the current KITTI/state-causality release gate.

## Unified Domain-Conditional Gate Evidence

The official v1.1.0 policy is:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

BUAA-Server output:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
status: pass
promotable_to_official: true
```

Controls:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Interpretation: this closes the previous unified-gate blocker and supplies the
evidence for the official `v1.1.0` package. `release/OFFICIAL_VERSION.md` now
identifies v1.1.0 as official; `v1.0-rc1` is retained as stable fallback.

## Qwen/VLM Gate Evidence

Qwen3-VL semantics remain diagnostic only.

Observed controls:

```text
50-window semantic controller: real/shuffle/disabled all 0.2365, oracle 0.1489
held-out calibrated gate: real 0.1813, shuffle 0.1776, disabled 0.2365
semantic Critic-prior: geometry-only F1 0.9211, real+geometry F1 0.8947
```

Interpretation: Qwen semantics did not produce a promotable state-causal
geometry signal.

## Local Checks

```text
python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
```

Result:

```text
27 passed
```

Expanded local verification, 2026-06-06:

```text
python -B -m pytest --assert=plain code/dream3r/tests -q
# 273 passed, 2 skipped
```

Expanded local verification, 2026-06-08:

```text
python -B -m pytest --assert=plain code/dream3r/tests -q
# 300 passed, 2 skipped
```

Targeted release/training subset:

```text
release candidate architecture/verifier
StatePriorHead
ProposalSetDecoder
NativeStudentDecoder
ImageStateStudentDecoder
memory/router/critic-only training
sequence/training convergence
critic training data
```

## Server Checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r conda run --no-capture-output -n dream3r python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
```

Result:

```text
27 passed
```

Expanded BUAA-Server GPU1 verification, 2026-06-06:

```text
CUDA_VISIBLE_DEVICES=1
37 passed
```

Server GPU1 training smokes, all `epochs=1`:

```text
runs/stage6_fusion/state_prior_train_smoke_20260606/
runs/stage6_fusion/proposal_set_decoder_train_smoke_20260606/frozen_prior_state_seed_7/
runs/stage6_fusion/native_student_train_smoke_20260606/
runs/stage6_fusion/image_state_student_train_smoke_20260606/
```

These smokes prove training entrypoints and cache/checkpoint paths still run;
they are not new model-promotion results.

## Hygiene Checks

Completed checks:

```text
git diff --check
stable-core diff check
artifact JSON parse check
```

Known caveat: `git diff --check` may report line-ending warnings from existing
CRLF/LF differences, but no whitespace errors were present in the verified
diff.

Known repository hygiene caveat: historical tracked `.pyc` files exist in the
workspace. They were left untouched to avoid unrelated release-package churn.

## Stable-Core Policy

The following stable-core files are not part of the release edits and remain
checked by the release verifiers:

```text
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/contracts.py
```

The following files are intentionally opened only for the documented
`v1.2-exp0` bridge and are reported as controlled exceptions:

```text
code/dream3r/model.py
code/dream3r/modules.py
code/dream3r/config.py
```

## Remaining Risks

- The RC is a bounded controlled candidate, not a SOTA/public-leaderboard
  claim.
- The official v1.1.0 package is still a controlled proposal-fusion release,
  not a proposal-free foundation model.
- Native proposal-free Dream3R decoding is not yet competitive with the
  selected bounded baseline. Sparse GT, stripped teacher, and larger
  scale-aligned teacher gates are all negative.
- Full paper-scale evaluation remains future work.
