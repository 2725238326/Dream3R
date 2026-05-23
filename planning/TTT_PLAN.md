# W25 Test-Time Training Plan — Dream3R Memory A1 Sub-Action Integration

**Status:** Draft  
**Axis:** A8 (tttLRM-style long-context A1 sub-action design)  
**Spec refs:** SPEC-20260522-001 §A8, SPEC-20260503-002 (Memory finalist)  
**Source:** SRC-2026-011 (tttLRM)

---

## 1. Objective

Integrate a tttLRM-style test-time training (TTT) sub-action into Dream3R's
C2 Memory state-update policy. The goal is to enable gradient-based state
correction during inference on long sequences (≥8 windows), reducing
accumulated drift without full retraining.

## 2. A1 Sub-Action Vocabulary (implemented in `memory_action.py`)

| Code | Name | When selected | Source |
|---|---|---|---|
| 0 | `full_update` | Default for most ticks | Dream3R baseline |
| 1 | `pose_adaptive_update` | Large camera baseline detected | PAS3R-style |
| 2 | `kalman_update` | Smooth motion, low conflict | FILT3R-style |
| 3 | `skip_update` | Extremely low drift & conflict | Conservative |
| 4 | `reset_state` | Critical failure / scene cut | Recovery |
| 5 | `test_time_train` | High drift on long sequences | tttLRM |

## 3. Current State (v0.5)

- ✅ `MemoryA1Action` enum with 6 sub-actions
- ✅ `StateUpdatePolicy` neural policy network (d_input=4, d_hidden=32)
- ✅ `TTTStateUpdater` scaffold (residual projection proxy for gradient step)
- ✅ Rule-based TTT boost: drift > 0.4 and window ≥ 8
- ✅ 14 unit tests passing

## 4. W25 Training Integration Milestones

### M1. Self-Supervised TTT Loss (Week 1-2)

Replace `TTTStateUpdater` scaffold with a real gradient step:

1. Compute **temporal consistency loss** between predicted pointmap at tick t
   and the back-projected pointmap from tick t-1 using ground-truth or
   estimated relative pose.
2. Detach memory state, clone, perform 1-3 gradient steps on the clone
   using the consistency loss, then replace the state.
3. Loss = `L_ttt = ||X_t - T_{t-1→t}(X_{t-1})||_2` weighted by confidence.

### M2. Policy Training (Week 2-3)

Train `StateUpdatePolicy` end-to-end:

1. **Reward signal:** Reduction in pointmap error after applying the selected
   sub-action vs. default `full_update`.
2. **Training strategy:** REINFORCE with baseline, or straight-through
   Gumbel-Softmax for differentiable policy.
3. **Data:** Synthetic long sequences (sequence_length ≥ 10) with injected
   drift and scene cuts.

### M3. Long-Sequence Evaluation (Week 3-4)

1. Run KITTI evaluation with A1 policy enabled (128+ windows).
2. Compare metrics with and without TTT:
   - Pointmap drift (cumulative L2 error)
   - Bank occupancy stability
   - NSA branch weight distribution
3. Record results in `cycles/` log.

### M4. Integration with RepairExecutor (Week 4)

1. Connect `StateUpdatePolicy` to `SpatialMemory.forward`:
   - Policy decision logged in `memory_retrieval_log["a1_action"]`
   - TTT updater invoked when policy selects action 5
2. Connect to `RepairExecutor`:
   - Action 1 (`local_rerun`) can co-fire with A1 policy
   - Action 4 (`test3r_offpath`) provides additional conflict signal

## 5. Risk Register

| Risk | Mitigation |
|---|---|
| TTT gradient step too slow for real-time | Cap at 1 step; profile latency |
| Policy collapses to always `full_update` | Entropy bonus in reward |
| State divergence after TTT step | Norm clamp on correction magnitude |
| Memory leak from detach-clone pattern | Explicit `del` + torch.cuda.empty_cache |

## 6. Non-Goals for W25

- Training a full tttLRM reproduction (we adapt the principle, not the model)
- Multi-step inner loop (single step only for v0.5/W25)
- Real-time inference deployment (latency budget not defined yet)

## 7. Dependencies

- A6 ✅ (long-sequence evidence confirms sliding branch behavior)
- A4 ✅ (VGGT adapter gives feed-forward comparison baseline)
- A5 ✅ (Test3R off-path provides additional conflict signal)
- Server GPU availability for long-sequence training runs

## 8. Exit Criteria

W25 closes when:
1. `TTTStateUpdater` performs a real gradient step (not scaffold)
2. `StateUpdatePolicy` is trained on synthetic data
3. KITTI long-sequence eval shows measurable drift reduction with TTT
4. Results documented in `cycles/` and `experiments/` logs
