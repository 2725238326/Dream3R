# Dream3R v0.4 Architecture Closure Status

Last updated: 2026-05-22 (v0.4 closed-loop orchestrator + contracts + RepairExecutor + dispatch wiring + 24 new tests added; 130 existing tests still pass)

## Purpose

This file records what the v0.4 architecture closure round actually
shipped and what is still stub / fallback / proxy. It is the canonical
verification document for the agent prompt at
`E:\Dream3R\ARCHITECTURE_V04_AGENT_PROMPT.md`.

The v0.3 path (model.py, modules.py, bus.py, anchor_bank.py,
nsa_attention.py, composer_experts/*) was preserved unchanged. v0.4 is
an additive orchestrator + contract layer on top.

## Files added this round

| File | Role |
|---|---|
| `code/dream3r/contracts.py` | Typed dataclasses for every module IO + final ReconstructionOutput |
| `code/dream3r/repair.py` | `RepairExecutor` — closes the critic -> repair feedback loop |
| `code/dream3r/orchestrator.py` | `V04Pipeline` — wraps Dream3R with v0.4 closed loops |
| `code/dream3r/tests/test_v04_architecture_contract.py` | 11 tests, asserts full ReconstructionOutput contract |
| `code/dream3r/tests/test_repair_executor_contract.py` | 6 tests, asserts action 1/2/3 actually rerun / reroute / cap |
| `code/dream3r/tests/test_composer_dispatch_contract.py` | 7 tests, asserts composer dispatch is real and reroute changes expert |

No files were deleted. `code/dream3r/model.py`, `modules.py`, `bus.py`,
`anchor_bank.py`, `nsa_attention.py`, `composer_experts/*` are
byte-identical to before.

## v0.4 closed-loop checklist

`[x]` = real, runnable, test-covered.
`[~]` = scaffold or proxy (works end-to-end, but the underlying signal
or backend is a fallback).
`[ ]` = not implemented; blocked on listed dependency.

### 1. Perception (C1)

- [x] Unified `PerceptionOutput` contract emitted on every tick
  (feature_tokens, pointmap_proposal, confidence, evidence_signals,
  backbone_status).
- [x] `backbone_status` honestly reports `is_loaded` + `use_backbone` +
  `backbone_load_error` + `backend` label (`real` / `fallback` / `stub`).
- [~] DINOv3-S backend is not present. With `use_backbone=True` and
  `backbone_type="dinov3"`, the existing v0.3 perceiver tries
  torch.hub then timm and falls back to none; the orchestrator labels
  this as `stub`. No false `real` claim is emitted.

### 2. Memory (C2)

- [x] `MemoryOutput` contract emitted (fused_context, latent_drift_proxy,
  bank_occupancy, selected_anchor_stats, retrieval_log,
  memory_backend_status).
- [x] Compressed / selected / sliding NSA three-branch retained from v0.3.
- [x] AnchorBank default capacity `K=256` is reported via
  `memory_backend_status["bank_capacity"]` and asserted in tests.
- [x] `cross_attention` and `mamba_hybrid` state recurrence types both
  supported (build_state_recurrence factory); test asserts the type is
  reported.
- [x] `latent_drift_proxy` and `bank_occupancy` are read by the Critic
  via the bus (`cr3_retrieval_bias`, contract log captures the read).

### 3. Permanence (C3)

- [x] `PermanenceOutput` contract emitted with
  `dynamic_logits`, `dynamic_mask_proxy` (derived bool, not claimed as
  final D2 asset), `dynamic_ratio`, `suppress_static_write`,
  `object_track_set`, `stable_promotion_log`.
- [x] `suppress_static_write` is the CR-2 handoff already published in
  v0.3 and consumed by Memory's write_decision head (modules.py
  SpatialMemory.forward gates write_logits[:,0] when suppress_mask is
  true).
- [~] Final D2 dynamic mask is NOT claimed. The contract field is named
  `dynamic_mask_proxy` and the docstring explicitly says "proxy".

### 4. Critic (C4)

- [x] `CriticDecision` contract emitted with `conflict_score`,
  `repair_action` (v0.4 code 0/1/2/3), `reroute_hint` (bool),
  `reason_codes`, `local_window_ids`, `critic_log`.
- [x] Sampson / depth / covisibility / confidence consistency already
  aggregated by v0.3 Critic.compute_geometric_consistency; passed
  through to `critic_log["geometric_consistency_log"]`.
- [x] `latent_drift_proxy` and `bank_occupancy` from Memory enter
  Critic via the bus (CR-3 retrieval bias + contract log).
- [x] Repair action mapping: v0.3 Critic's 6-way head (0=no, 1=local,
  2=reroute, 3..5=stub) is mapped to v0.4 4-way contract (0=no,
  1=local, 2=window, 3=reroute) with explicit severe-conflict
  escalation rule (sigmoid_conflict > 0.85 escalates 1 -> 2).

### 5. RepairExecutor

- [x] `action=0` is a real noop, recorded in the log.
- [x] `action=1` triggers a real local rerun: model.forward is called
  a second time with `recommended_action=1` injected into the bus's
  previous_signals so Memory bumps CR-3 retrieval depth (cr3_dynamic_k
  doubles per existing v0.3 code path).
- [x] `action=2` triggers a real window rerun: model.forward is called
  with `prev_memory_state=None, prev_object_slots=None,
  prev_object_slot_poses=None` (fresh state) and `recommended_action=2`
  injected so Composer zeros critic_confidence.
- [x] `max_repair_attempts` (default 1) is honored. A second action
  request inside one pipeline.forward call returns the latest output
  without re-running the model, and the cap event is recorded
  (`succeeded=False`, `note="cap hit"`) in the log.
- [x] `action=3 / reroute_hint=True` does NOT rerun the model. Instead
  `_reroute_hint` is set and the orchestrator picks
  `route_recommendation[:, 1]` (second-best expert) for dispatch.
- [x] `repair_action_log` records every attempt with action_code,
  action_name, reason, succeeded, note, triggered_by_critic, and the
  `capped` flag.
- [x] No unbounded recursion: tested by issuing 5 action=1 requests
  back-to-back with max_attempts=2; final n_attempts == 2, capped == True.

### 6. Composer (C5)

- [x] Seven expert adapters present and registered via
  `ExpertRegistry.register_all_defaults` (MASt3R, Fast3R, Spann3R,
  CUT3R, MoGe-2, DepthAnything, Test3R).
- [x] `ComposerDecision` contract emitted with `selected_expert`,
  `routing_logits`, `cost_adjusted_scores`, `route_recommendation`,
  `capability_match`, `route_regret`, `reroute_applied`,
  `backend_status` (with full adapter status table).
- [x] Real dispatch path: `model.composer.dispatch(expert_id, images)`
  is called by the orchestrator on every tick. Result lands in
  `ReconstructionOutput.pointmap / confidence / evidence`.
- [x] Per-adapter `backend_status` distinguishes `real` (is_loaded=True,
  real checkpoint resolved) vs `fallback` (deterministic image-derived
  output flagged `deterministic_fallback`) vs `stub` (no real
  checkpoint and no fallback path).
- [~] MASt3R and Fast3R have real loader paths (load_checkpoint method
  + repo discovery), but locally no checkpoint is present, so backend
  status is `fallback`. No false `real` claim is emitted.
- [~] Spann3R / CUT3R / MoGe-2 / DepthAnything / Test3R adapters
  return deterministic fallback outputs; their `is_loaded` is False
  and backend is `fallback` / `stub` accordingly.
- [x] Reroute path is tested: forcing critic action=3 makes the
  orchestrator pick `route_recommendation[:, 1]` and the test
  asserts the rerouted expert id differs from the primary.

### 7. Final ReconstructionOutput

- [x] All required fields present: `pointmap`, `confidence`,
  `dynamic_logits`, `dynamic_mask_proxy`, `evidence`,
  `selected_expert`, `backend_status`, `conflict_score`,
  `memory_log`, `route_log`, `repair_action_log`, `contract_log`,
  `architecture_version="v0.4"`.
- [x] Typed sub-contracts also exposed (`perception`, `memory`,
  `permanence`, `critic`, `composer`, `expert`, `repair`) so callers
  can pattern-match without re-reading raw dicts.
- [x] Pointmap/confidence/evidence in the final output COME FROM the
  expert dispatch result, not from perception. Test asserts the patch
  count (P=196 from adapter's 14*14 grid) differs from perception's
  P=17 evidence count, proving the dispatch result actually flowed
  through.

## Forced closed-loop behaviors verified by tests

| Closed loop | Test |
|---|---|
| critic action=1 -> RepairExecutor -> local rerun | `test_action_one_triggers_real_local_rerun` |
| critic action=2 -> RepairExecutor -> window rerun, max_attempts honored | `test_action_two_triggers_window_rerun_and_respects_max_attempts` |
| critic action=3 / reroute_hint=True -> Composer picks alternate expert | `test_reroute_hint_changes_selected_expert` |
| No infinite recursion under persistent action requests | `test_repair_executor_does_not_loop_forever_when_actions_persist` |
| Permanence -> CR-2 -> Memory write gating | already covered by v0.3 `test_spatial_payload.py` + `test_bus_temporal.py` (preserved unchanged) |
| Memory -> bank_occupancy / latent_drift_proxy -> Critic | `test_contract_log_records_cross_module_reads` |
| Composer dispatch -> ExpertOutput -> final ReconstructionOutput | `test_expert_output_replaces_perception_pointmap_in_final_output` |

## Test results

Local environment: Python 3.13, torch 2.12.0+cpu, no GPU, no checkpoints.

```text
# v0.4 closure tests (new):
24 passed in 5.27s
  - test_v04_architecture_contract.py            11/11
  - test_repair_executor_contract.py              6/6
  - test_composer_dispatch_contract.py            7/7

# Full Dream3R test suite (no regression):
130 passed, 43 warnings in 34.28s
(Excluded integration tests that require real checkpoints:
 test_dinov2_backbone.py, test_fast3r_integration.py,
 test_mast3r_integration.py, test_spann3r_integration.py — these
 already required real models in prior cycles and were not touched.)
```

Test commands:

```bash
# All three new contract test files
cd E:/Dream3R/code
python -m pytest dream3r/tests/test_v04_architecture_contract.py \
                 dream3r/tests/test_repair_executor_contract.py \
                 dream3r/tests/test_composer_dispatch_contract.py -q

# Direct invocation (no pytest dependency)
python dream3r/tests/test_v04_architecture_contract.py
python dream3r/tests/test_repair_executor_contract.py
python dream3r/tests/test_composer_dispatch_contract.py

# Full suite minus heavy backbone integration tests
python -m pytest dream3r/tests/ -q \
    --ignore=dream3r/tests/test_dinov2_backbone.py \
    --ignore=dream3r/tests/test_fast3r_integration.py \
    --ignore=dream3r/tests/test_mast3r_integration.py \
    --ignore=dream3r/tests/test_spann3r_integration.py
```

## What is still stub / fallback / proxy

| Surface | State | Why | Unblock path |
|---|---|---|---|
| Perception DINOv3-S backend | stub | torch.hub + timm not installed locally | Server-side `pip install timm` or load DINOv2/v3 from hub; `Perceiver.__init__` already accepts `backbone_type="dinov3"` |
| Spann3R / CUT3R / MoGe-2 / DepthAnything / Test3R adapters | fallback (deterministic image-derived) | No real checkpoints / repo paths locally | Adapter `load_checkpoint(path)` per backbone on server |
| MASt3R / Fast3R adapters | fallback locally; real path wired | Real loader exists, no checkpoint locally | Already loadable on `/hdd3/kykt26/` per RECENT_PROGRESS.md; Fast3R blocked on `omegaconf` in dream3r conda env |
| Permanence dynamic mask | proxy (`dynamic_mask_proxy`) | Not promoted to D2 final asset per project rules | Requires DEC to ratify the proxy as final; out of scope this round |
| 4DGS / GaussianHead | contract-only | Per agent prompt: "4DGS 本轮只保留 contract，不纳入主 forward 主线" | Future round; W27 candidate per NEXT_PHASE_ROADMAP.md |

## Next minimal experiment

Once on the server with at least one real expert checkpoint loaded (the
RECENT_PROGRESS.md cycle 033/034 notes confirm MASt3R + Spann3R
adapters can load):

1. Run `python dream3r/tests/test_v04_architecture_contract.py` on the
   server with use_backbone=True and a loaded MASt3R adapter. Assert
   that `out.expert.backend_status["backend"] == "real"` for at least
   one batch element.
2. Run a 5-tick window sequence with the KITTI smoke loader; verify
   that `repair_action_log["n_attempts"]` is bounded across ticks and
   that `route_log["reroute_applied"]` flips to True on at least one
   high-conflict tick.
3. Compare cumulative pointmap L2 against the v0.3 baseline
   (`pointmap L2 = 20.4747` per RECENT_PROGRESS.md line 78). v0.4 is
   architecture-closure-only; we do not expect a quality gain without
   training, but we do expect no regression.

## Decisions made autonomously this round

Per the autonomous-decision rules in `ARCHITECTURE_V04_AGENT_PROMPT.md`:

1. v0.4 layer is **additive**: model.py / modules.py / bus.py /
   anchor_bank.py / nsa_attention.py / composer_experts/* are
   byte-identical to before. The v0.4 closure lives in three new files.
2. `max_repair_attempts` defaults to 1 per the agent prompt's
   conservative default. Tests cover both the default and a
   max_attempts=2 case to confirm the cap mechanism.
3. v0.4 action codes use the prompt's 0/1/2/3 mapping. v0.3's
   6-way head is mapped (no=0, local=1, reroute=2 -> v04 action 3);
   action 2 (window_rerun) is synthesized via the severe-conflict
   escalation rule rather than directly read from the head.
4. Adapter dispatch falls back to a perception-derived stub when raw
   images are not supplied, so tests can run with feature-only inputs.
   Real ticks on the server pass raw images and hit the adapter
   forward path.
5. 4DGS / GaussianHead was NOT pulled into the v0.4 main forward per
   the prompt's exclusion rule. The existing `gaussian_head.py`
   tensor contract is untouched; its tests still pass.
6. The `dynamic_mask_proxy` field is explicitly named proxy in the
   contract, and the per-axis status table flags it as `[~]`. No
   false D2-final claim is emitted.
