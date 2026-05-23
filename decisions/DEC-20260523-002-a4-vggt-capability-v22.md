# DEC-20260523-002: Close v0.5 Axis A4 - VGGT adapter and capability_card v2.2

decision_id: DEC-20260523-002
date: 2026-05-23
axis: A4
parent_spec: SPEC-20260522-001-dream3r-v05-axes.md
evidence_cycle: CYCLE-20260523-002
status: proposed (pending user ratification)

---

## Decision

**Close Axis A4 as a contract-and-adapter closure.**

Dream3R now has an explicit VGGT Composer adapter, an additive capability-card v2.2 regime (`feed_forward_manyview`), and an 8-expert Composer registry surface. This closes the structural gap where VGGT existed only as a comparator and could not be represented distinctly from Fast3R.

This DEC does **not** claim a real VGGT checkpoint has been downloaded or evaluated. The adapter currently reports fallback behavior honestly until the user authorizes checkpoint acquisition and server-side real inference.

## closes_iff satisfaction

Per SPEC-20260522-001 §A4:

| Criterion | Satisfied | Evidence |
|---|---|---|
| capability_card schema bumped to v2.2 with feed-forward many-view profile | Yes | `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.2 change log; `composer_experts/method_profiles.py` `REGIME_ORDER` has 6 regimes |
| `vggt_adapter.py` added under `composer_experts/`; `method_profiles.py` gains `"vggt"` | Yes | `composer_experts/vggt_adapter.py`; `METHOD_PROFILES["vggt"]` |
| `ExpertRegistry.register_all_defaults` registers the 8th adapter | Yes | `composer_experts/__init__.py`; tests assert `len(registry.names) == 8` |
| `ComposerDecision.backend_status` reports the 8th row | Yes | adapter status reports `"vggt"` with `backend == "fallback"` before checkpoint load |
| server tick confirms `backend == "real"` for loaded VGGT checkpoint | Deferred / waived for this DEC | No checkpoint download authorized; tests deliberately assert fallback honesty instead of manufacturing a real claim |
| `SOTA_FEATURE_MATRIX.md` VGGT row moves from comparator-only to wired adapter status | Yes | Section 2 VGGT row updated during CYCLE-20260523-002 |

## Waived sub-conditions

The real-checkpoint sub-condition is waived for this closure because VGGT checkpoint acquisition requires separate user authorization. The closed surface is the v2.2 capability contract, registry expansion, fallback-safe adapter, and tests. A future A2-style checkpoint DEC can promote VGGT from fallback/stub status to real-wired once the checkpoint is available and a server tick proves `backend == "real"`.

## Consequence

- `capability_card` has six regimes, including `feed_forward_manyview`.
- Composer registry cardinality is now eight experts: MASt3R, Fast3R, Spann3R, CUT3R, MoGe-2, Depth Anything V2, Test3R, and VGGT.
- `n_regimes` default is six across config/model/synthetic/train/test surfaces.
- VGGT is represented honestly as a fallback adapter until checkpoint work is separately authorized.

## Linked artifacts

- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`
- `code/dream3r/composer_experts/vggt_adapter.py`
- `code/dream3r/composer_experts/method_profiles.py`
- `code/dream3r/composer_experts/base_adapter.py`
- `code/dream3r/composer_experts/__init__.py`
- `code/dream3r/config.py`
- `code/dream3r/model.py`
- `code/dream3r/modules.py`
- `code/dream3r/tests/test_vggt_integration.py`
- `code/dream3r/tests/test_composer_experts.py`
- `code/dream3r/tests/test_composer_dispatch_contract.py`
- `code/dream3r/tests/test_sequence_training.py`
- `code/dream3r/tests/test_training_convergence.py`
- `code/dream3r/tests/test_real_sequence_eval_contract.py`
- `code/dream3r/tests/test_evaluate_metrics.py`
- `code/dream3r/tests/test_visualization_contract.py`
- Local test pass rerun in CYCLE-20260523-002: 195 passed
- Server test pass recorded by handoff: 194 passed
