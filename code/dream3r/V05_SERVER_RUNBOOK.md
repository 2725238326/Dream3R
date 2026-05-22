# Dream3R v0.5 Server Runbook

> Generated from v0.5 iteration test plan. This runbook details steps for
> syncing code to the server, running local + server tests, and verifying
> long-sequence memory evidence on KITTI.

---

## 1. Code Synchronization

```bash
# From local machine — sync to server
rsync -avz --exclude='__pycache__' /path/to/Dream3R/code/dream3r/ kykt26@server:/hdd3/kykt26/code/dream3r/
```

**Files changed in this iteration:**

| File | Change |
|------|--------|
| `contracts.py` | Added `OffpathVerification` dataclass, action 4 in `REPAIR_ACTION_NAMES`, `offpath_verification` field in `RepairReport` |
| `repair.py` | Added `_test3r_offpath()` handler for action 4, imports `OffpathVerification` |
| `orchestrator.py` | Added `offpath_verification` dict to `repair_action_log` assembly |
| `evaluate_real_sequence.py` | Added `effective_top_k`, `sliding_branch_fired` to window summary JSON |
| `tests/test_v04_edge_cases.py` | **NEW** — 7 edge-case contract tests |
| `tests/test_v04_multitick_state.py` | **NEW** — 8 multi-tick state carry tests |
| `tests/test_v04_test3r_offpath.py` | **NEW** — 7 Test3R off-path scaffold tests |

---

## 2. Run Local Tests (CPU-only, no checkpoint / no data required)

```bash
cd /hdd3/kykt26/code

# v0.4 architecture contract (existing, 11 tests)
python -m pytest dream3r/tests/test_v04_architecture_contract.py -v --tb=short

# Repair executor contract (existing, 6 tests)
python -m pytest dream3r/tests/test_repair_executor_contract.py -v --tb=short

# NEW: Edge-case tests (7 tests)
python -m pytest dream3r/tests/test_v04_edge_cases.py -v --tb=short

# NEW: Multi-tick state tests (8 tests)
python -m pytest dream3r/tests/test_v04_multitick_state.py -v --tb=short

# NEW: Test3R off-path tests (7 tests)
python -m pytest dream3r/tests/test_v04_test3r_offpath.py -v --tb=short

# Full batch (all v0.4/v0.5 tests, 39 total)
python -m pytest dream3r/tests/test_v04_architecture_contract.py \
                 dream3r/tests/test_repair_executor_contract.py \
                 dream3r/tests/test_v04_edge_cases.py \
                 dream3r/tests/test_v04_multitick_state.py \
                 dream3r/tests/test_v04_test3r_offpath.py \
                 -v --tb=short
```

**Expected:** 39 tests pass (11 + 6 + 7 + 8 + 7).

---

## 3. Run KITTI Real-Sequence Evaluation (server-side, requires GPU + data)

```bash
cd /hdd3/kykt26/code

# 8-window KITTI run (mamba_hybrid, NSA enabled, stable memory enabled)
python -m dream3r.evaluate_real_sequence \
    --data-root /hdd3/kykt26/data \
    --max-windows 8 \
    --max-sequences 1 \
    --recurrence mamba_hybrid \
    --output demo_artifacts/real_sequence/kitti_8win_v05.json

# 10-window KITTI run
python -m dream3r.evaluate_real_sequence \
    --data-root /hdd3/kykt26/data \
    --max-windows 10 \
    --max-sequences 1 \
    --recurrence mamba_hybrid \
    --output demo_artifacts/real_sequence/kitti_10win_v05.json
```

---

## 4. Output JSON Path

```
demo_artifacts/real_sequence/kitti_8win_v05.json
demo_artifacts/real_sequence/kitti_10win_v05.json
```

---

## 5. Fields to Check in Output JSON

For each window entry in `"windows"`:

| Field | Type | What to verify |
|-------|------|----------------|
| `nsa_branch_mean.compressed` | float | Non-zero if NSA is active |
| `nsa_branch_mean.selected` | float | Non-zero if bank has entries |
| `nsa_branch_mean.sliding` | float | Non-zero indicates sliding branch fired |
| `latent_drift_proxy` | float | Should change across windows |
| `bank_occupancy` | float | Should grow monotonically (or plateau) |
| `selected_anchor_3d_distance` | float | Non-zero after bank has entries |
| `effective_top_k` | int/null | Non-null when NSA retrieval is active |
| `sliding_branch_fired` | bool | True if sliding branch was in top-k gates |
| `conflict_score_mean` | float | Critic output per window |
| `recommended_action` | list[int] | Action codes per batch element |

Top-level fields:

| Field | What to verify |
|-------|----------------|
| `recurrence_type` | `"mamba_hybrid"` |
| `recurrence_backend` | Not an error string |
| `memory_use_nsa` | `true` |
| `enable_stable_memory` | `true` |

---

## 6. V04Pipeline Fields (when running via orchestrator)

When using `V04Pipeline` (not raw `Dream3R.forward`), the `ReconstructionOutput` includes:

| Field | Source |
|-------|--------|
| `repair_action_log.offpath_verification` | Test3R off-path result (null if action != 4) |
| `repair_action_log.implemented_actions` | `[0, 1, 2, 3, 4]` |
| `memory_log.selected_anchor_stats.branch_weights_mean` | NSA gate weights [3] |
| `memory_log.retrieval_log` | Full retrieval diagnostics |
| `backend_status.expert.backend` | `"real"` / `"fallback"` / `"stub"` |
| `route_log.reroute_applied` | Whether action 3 triggered reroute |

---

## 7. Local vs. Server Execution Summary

| Step | Where | Status |
|------|-------|--------|
| Write edge-case tests | Local | Done |
| Write multi-tick tests | Local | Done |
| Write Test3R off-path tests | Local | Done |
| Extend contracts.py (action 4) | Local | Done |
| Extend repair.py (off-path handler) | Local | Done |
| Extend orchestrator.py (offpath log) | Local | Done |
| Extend evaluate_real_sequence.py | Local | Done |
| Run CPU-only test suite | **Server** | Pending |
| Run KITTI 8-10 window evaluation | **Server** | Pending (requires GPU + data) |
| Verify NSA branch weights in JSON | **Server** | Pending |
| Verify bank_occupancy growth | **Server** | Pending |
| Verify repair_action_log schema | **Server** | Pending |

---

## 8. What Is NOT Closed

- **A1 (DINOv3-S backbone):** Not started, requires checkpoint
- **A2 (Real expert adapter):** Fallback only, requires checkpoint loading
- **A3 (Dynamic mask promotion):** `dynamic_mask_proxy` is proxy, not D2 final
- **A4 (Critic scoring):** Stub geometric consistency, needs server evidence
- **A5 (Test3R off-path):** Scaffold complete, fallback only, not closed
- **A6 (NSA sliding branch):** Fields exported, server KITTI run needed for evidence
- **A7 (Loss function):** Not started
- **A8 (End-to-end demo):** Not started
