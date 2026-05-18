# Dream3R Cycle 033: Full Architecture Advancement Plan

Status: **active implementation** (W1-W16 implemented and verified; W17-W18 remain future P3 targets)

Date: 2026-05-10 (updated with SOTA gap analysis and W11-W18 breakthrough workstreams)

## Goal

Push Dream3R v0.3 codebase from "scaffold with stubs" to "architecturally competitive with state-of-the-art 3R methods and beyond." This means every module must produce real, meaningful computation — not stub outputs, not broken feedback loops, not placeholder routing.

Dream3R's innovation is not a single trick. It is the composition of multiple advances:

1. **3R reconstruction core** — competitive with MASt3R / Fast3R / CUT3R / Spann3R / VGGT
2. **NSA (Native Sparse Attention)** — adapted from DeepSeek for 3D streaming
3. **Control-graph architecture** — bus-mediated cross-module contracts (CR-1..CR-6)
4. **Spatial memory with AnchorBank** — geometric anchor retrieval with 3D position embeddings
5. **Expert routing with cost awareness** — learned dispatch across multiple 3R backbones
6. **Object permanence tracking** — slot attention with ISA-style per-slot reference frames
7. **Critic verification loop** — geometric consistency-based error detection and repair
8. **Foundation model backbone** — frozen DINOv2/v3 encoder as visual prior
9. **Active/stable state architecture** — solving the bounded-memory forgetting problem
10. **Self-supervised geometric losses** — Sampson distance, covisible maps, cycle consistency

All ten pillars must reach a level where the architecture can be presented as a coherent, working system that advances beyond the current SOTA, not a collection of plumbed-but-inert interfaces.

## SOTA landscape (as of 2026-05-10)

Key competitive targets:
- **VGGT** (CVPR 2025 Best Paper): unified feed-forward, pose+depth+pointmap+tracking, alternating frame/global attention. Accuracy ceiling.
- **CUT3R** (CVPR 2025 Oral): state-token recurrence for streaming. Forgetting problem spawned Point3R, Mem3R, LONG3R.
- **Fast3R** (CVPR 2025): all-to-all attention, 1000+ images, "train short test long". Non-streaming.
- **DeepSeek NSA** (ACL 2025 Best Paper): 3-branch compress/select/sliding. 9x training speedup.
- **Point3R** (NeurIPS 2025): spatial pointer memory with 3D hierarchical position embeddings.
- **OnlineX** (March 2026): active/stable state decoupling for streaming.
- **STream3R** (2025): causal decoder-only 3R, FlashAttention-compatible.
- **DINOv3** (late 2025): 7B ViT teacher, Gram Anchoring, RoPE. Default feature backbone.
- **tttLRM** (CVPR 2026 Highlight): test-time training layers for implicit 3D representation.

Dream3R's differentiation: **no existing method combines** NSA sparse attention + explicit spatial memory + multi-expert routing + bus-mediated control contracts + object permanence + Critic verification in one streaming architecture. The challenge is making each of these real, not just plumbed.

---

## Workstream overview

| ID | Workstream | What it advances | Priority |
|----|-----------|-----------------|----------|
| W1 | Bus temporal semantics | Control-graph (3) | P0 — blocks W2, W5-W7 |
| W2 | CR-3 retrieval policy | NSA (2) + Control-graph (3) | P0 |
| W3 | Spatial memory payload | Spatial memory (4) | P0 |
| W4 | Expert adapter real integration | Expert routing (5) + 3R core (1) | P1 |
| W5 | Sequence-level training | All | P1 |
| W6 | Permanence mechanism hardening | Permanence (6) | P1 |
| W7 | Critic loop closing | Critic (7) | P1 |
| W8 | NSA architecture refinement | NSA (2) | P2 |
| W9 | Loss and training advancement | 3R core (1) | P2 |
| W10 | Evaluation and metrics | All | P2 |
| **W11** | **DINOv2/v3 frozen encoder** | **Foundation backbone (8)** | **P1 — highest impact** |
| **W12** | **3D position embeddings for AnchorBank** | **Spatial memory (4)** | **P1 — depends on W3** |
| **W13** | **Active/stable state decoupling** | **State architecture (9)** | **P1 — depends on W5** |
| **W14** | **SSR Grassmannian drift regularizer** | **State architecture (9)** | **P1 — plug-and-play** |
| **W15** | **Critic geometric consistency signals** | **Critic (7) + Losses (10)** | **P2 — depends on W7** |
| **W16** | **ISA per-slot reference frames** | **Permanence (6)** | **P2 — depends on W6** |
| **W17** | **Mamba-Transformer hybrid blocks** | **NSA (2) + State (9)** | **P3 — architectural** |
| **W18** | **3DGS output head** | **3R core (1) + Losses (10)** | **P3 — new output format** |

---

## W1: Bus temporal semantics (P0)

### Current problem

`MemoryBus.reset()` is called at the top of `Dream3R.forward()` (model.py:141), which clears all signals. Any attempt to read previous-tick signals (e.g., `conflict_score(t-1)` at model.py:156) gets `None`. This means:
- Memory never sees Critic feedback from the previous window
- Permanence never adapts mint conservatism based on prior conflict
- Composer never adjusts routing based on prior Critic confidence
- CR-3, CR-1, and all cross-tick contracts are dead code in practice

### Required changes

**bus.py:**
- Add a `_previous_signals` dict alongside `_signals`
- Change `reset()` to rotate: `_previous_signals = self._signals.copy(); _signals.clear()`
- Add `read_previous(signal_name, consumer)` method that reads from `_previous_signals`
- Update `get_contract_log()` to distinguish current vs previous reads
- Keep `_owner_table` enforcement unchanged

**model.py:**
- Replace `self.bus.read("conflict_score", "memory")` with `self.bus.read_previous("conflict_score", "memory")`
- Same for all other t-1 reads (dynamic_ratio for Permanence, conflict_score for Permanence, conflict_score for Composer)
- Remove the misleading `prev_conflict_sig` / `prev_dynamic_sig` naming that implies temporal reads but actually reads current (empty) tick

### Verification

- Unit test: publish signal at tick t, call reset(), verify `read()` returns None but `read_previous()` returns the signal
- Integration test: run 2-window forward pass, verify Memory receives non-None conflict_score at window 2
- Contract log test: verify log entries distinguish `source: "current"` vs `source: "previous"`

### Files touched

- `bus.py`: ~30 lines added/modified
- `model.py`: ~15 lines modified
- `tests/test_bus_temporal.py`: new, ~80 lines

---

## W2: CR-3 retrieval policy (P0, depends on W1)

### Current problem

CR-3 functions (`gate_cr3`, `cr3_retrieval_bias`, `cr3_permanence_bias` in bus.py:123-160) compute meaningful values, but:
1. Their inputs are always `None` because W1 is broken
2. The effect in `nsa_attention.py:236-239` is a hardcoded `+2.0` bias on selected branch gate logits when confidence is low — this is a reasonable idea but the constant `2.0` is arbitrary and not tunable
3. `cr3_permanence_bias` is passed through but never actually used in NSA scoring — it's accepted as a parameter but has no effect on attention weights or bank retrieval

### Required changes

**nsa_attention.py:**
- Make the confidence bias strength a learnable parameter or configurable hyperparameter instead of hardcoded `2.0`
- Actually use `permanence_bias` in the selected branch: add it as a scoring bias on bank key similarity (entries associated with permanent/stable objects should be preferred under uncertainty)
- Add a `retrieval_log` dict to the NSA return: `{"effective_top_k": ..., "confidence_bias_applied": ..., "permanence_bias_applied": ..., "selected_scores_before_bias": ..., "selected_scores_after_bias": ...}`

**bus.py:**
- `gate_cr3()`: the current thresholds (0.4, 0.7) are reasonable but should be configurable via `__init__` params, not hardcoded
- Consider making `gate_cr3` return a float scaling factor instead of discrete int jumps (8 -> 12 -> 16 -> 32), so the behavior is smoother and more testable

### Verification

- Test: inject high conflict_score into bus previous signals, run forward, verify `effective_top_k` increased and `confidence_bias_applied > 0`
- Test: inject low dynamic_ratio (high permanence), verify `permanence_bias_applied > 0` and stable entries score higher
- Test: inject zero conflict (high confidence), verify no bias applied
- Log inspection: verify `retrieval_log` is present in model output

### Files touched

- `nsa_attention.py`: ~25 lines modified
- `bus.py`: ~10 lines modified
- `tests/test_cr3_policy.py`: new, ~100 lines

---

## W3: Spatial memory payload (P0)

### Current problem

`AnchorBank` (anchor_bank.py) stores only `keys` and `values` as latent vectors. It has no spatial content — no 3D points, no pose information, no patch IDs. This means:
- Retrieved anchors cannot be traced back to their source frame or 3D location
- The "spatial" in "SpatialMemory" is aspirational, not real
- Memory retrieval cannot be geometrically conditioned (e.g., "retrieve anchors near this 3D region")

### Required changes

**anchor_bank.py:**
- Add registered buffers for spatial payload:
  - `source_frame_pose`: `[B, capacity, 4, 4]` — camera-to-world transform of the frame that wrote this anchor
  - `source_patch_ids`: `[B, capacity]` (long) — patch index within the source frame
  - `points3d_mean`: `[B, capacity, 3]` — mean 3D point of the patch that this anchor represents
- Update `reset()` to zero-initialize these buffers
- Update `write()` to accept optional spatial payloads and store them
- Update `ReadResult` dataclass to include spatial payloads from retrieved entries
- Update `read()` to gather spatial payloads alongside keys/values

**modules.py (SpatialMemory):**
- In `forward()`, compute spatial payloads from the Perceiver's pointmap output:
  - `points3d_mean` = mean of `t2_pointmap` over the patch dimension for selected write candidates
  - `source_frame_pose` = identity for now (real poses come later with real data); but the slot exists
  - `source_patch_ids` = the `top_indices` already computed for write candidates
- Pass these to `anchor_bank.write()`
- Include retrieved spatial payloads in the output dict as `memory_retrieval_log`

**model.py:**
- Pass `t2_pointmap` into SpatialMemory so it can extract spatial payloads
- Include `memory_retrieval_log` in the model output

### Verification

- Test: write anchors with known 3D points, read them back, verify points3d_mean matches
- Test: verify ReadResult contains spatial payloads with correct shapes
- Test: verify occupancy, prune, and quarantine still work correctly with spatial payloads
- Integration: run forward pass, verify `memory_retrieval_log` in output contains spatial data

### Files touched

- `anchor_bank.py`: ~60 lines added/modified
- `modules.py`: ~30 lines modified
- `model.py`: ~10 lines modified
- `tests/test_spatial_payload.py`: new, ~80 lines

---

## W4: Expert adapter real integration (P1)

### Implementation status (2026-05-09)

Implemented:
- `MASt3RAdapter` now has a deterministic image-derived fallback instead of random tensors
- real MASt3R checkpoint discovery via `MAST3R_REPO` / `MAST3R_CHECKPOINT` or server defaults
- `load_checkpoint()` loads `/hdd3/kykt26/code/mast3r/checkpoints/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth`
- real model forward maps MASt3R pointmaps/confidence into the `ExpertOutput` contract
- `ExpertRegistry.adapter_status()` reports availability, loaded state, backend, attention regime, and latency estimate
- all non-real adapters now use deterministic image-derived fallback outputs instead of `torch.randn`
- `ComposerRouter.dispatch()` records dispatch latency, selected expert name/id, and adapter availability/loading metadata
- Composer routing test verifies MASt3R is preferred for static indoor regimes when cost penalty is disabled
- optional server integration test in `tests/test_mast3r_integration.py`

Verified on server:
- normal fallback contract test passes without loading the large model
- `DREAM3R_RUN_MAST3R_INTEGRATION=1` successfully loads the checkpoint and runs one forward pass

### Implementation status update (2026-05-10)

Implemented:
- Fast3R adapter now has a real checkpoint-loading path using `/hdd3/kykt26/code/fast3r` and `/hdd3/kykt26/models/fast3r/Fast3R_ViT_Large_512`
- Fast3R adapter installs the PyTorch math attention fallback used by the server runner for sm75 compatibility
- `ExpertRegistry.adapter_status()` now distinguishes `has_checkpoint_artifacts` from runtime `is_available`
- MASt3R integration test now verifies loaded MASt3R can be invoked through `ComposerRouter.dispatch()`
- Fast3R integration test verifies fallback contract and records the current runtime dependency blocker
- Spann3R adapter now has a real checkpoint-loading path using `/hdd3/kykt26/code/spann3r/checkpoints/spann3r.pth`
- Spann3R real forward maps native streaming pointmaps/confidence into the shared `ExpertOutput` contract
- Spann3R optional integration test verifies both direct adapter forward and `ComposerRouter.dispatch()`

Verified on server:
- Fast3R repo and checkpoint artifacts are present
- `DREAM3R_RUN_FAST3R_INTEGRATION=1` reaches dependency validation and reports the missing `omegaconf` runtime dependency instead of failing the normal test suite
- MASt3R loaded dispatch path remains green
- `DREAM3R_RUN_SPANN3R_INTEGRATION=1` loads the real Spann3R checkpoint and runs the dispatch path successfully

Current W4 blocker:
- The `dream3r` conda env is missing `omegaconf`, required by Fast3R. No package install was performed in this cycle.
- Spann3R uses the slow PyTorch RoPE2D fallback on the server because the cuda-compiled RoPE2D extension is not present.

### Remaining problem

MASt3R and Spann3R now have real loadable paths, and Fast3R has checkpoint artifacts plus a guarded loader. Remaining adapters still need true backends or explicit blocker reporting:
- CUT3R: repo/checkpoints present, adapter still deterministic fallback
- MoGe-2 / DepthAnything / Test3R: fallback only
- Fast3R: true forward blocked by missing `omegaconf`

### Required changes

This workstream originally connected at least ONE real adapter to validate the interface. That is complete for **MASt3R** and extended to **Spann3R**. Next real-adapter targets:
- Resolve Fast3R runtime dependency and run the true forward path
- Connect CUT3R as the next stateful streaming expert
- Add latency/status reporting for each loaded real backend

The original first target was **MASt3R** because:
- Server already has `mast3r_runner.py` and the conda env
- MASt3R's architecture (ViT encoder + decoder for pairwise matching) maps cleanly to the ExpertOutput contract
- It's the most widely cited baseline in the 3R literature

**composer_experts/mast3r_adapter.py:**
- Replace `torch.randn` with actual MASt3R inference:
  - Load pretrained MASt3R encoder (from existing server checkpoint)
  - Extract patch-level features from MASt3R's ViT
  - Project to ExpertOutput format: pointmap, confidence, evidence_tokens
- Implement real `load_checkpoint()` that loads MASt3R weights
- Implement real `is_loaded` property
- Keep the adapter self-contained — it should work as a drop-in replacement

**Integration path (server-side):**
- Verify MASt3R checkpoint exists at expected path on server
- Write a minimal integration test that loads the adapter and runs one forward pass
- Confirm ExpertOutput shapes match the contract
- Confirm the adapter can be registered in ExpertRegistry and dispatched by ComposerRouter

**Other adapters:**
- Keep deterministic fallback until a backend is wired. Each adapter follows the same status/reporting pattern; once a checkpoint is available, it must expose `has_checkpoint_artifacts`, `is_available`, and optional real integration tests.
- Update capability_cards to reflect real vs stub status in ExpertRegistry

### Verification

- Server-side test: load MASt3R adapter, run one forward pass on a real image pair, verify output shapes
- Server-side test: load Spann3R adapter, run one forward pass on a two-view sequence, verify output shapes
- Routing test: with one real adapter and 6 stubs, verify ComposerRouter prefers the real adapter for static indoor regimes (where MASt3R excels)
- Routing test: dispatch loaded Spann3R through `ComposerRouter` and verify metadata marks the selected loaded backend
- Profile: measure MASt3R/Spann3R adapter latency and compare against the `latency_estimate_ms` in the capability card

### Files touched

- `composer_experts/mast3r_adapter.py`: major rewrite (~150 lines)
- `composer_experts/spann3r_adapter.py`: real loader/forward/status path
- `composer_experts/__init__.py`: minor update for real/stub status
- `tests/test_mast3r_integration.py`: new, ~60 lines (server-side only)
- `tests/test_spann3r_integration.py`: optional real checkpoint + dispatch path

### Constraints

- Requires server access and method checkpoints
- Should not change the adapter interface — the `ExpertOutput` contract is stable
- Remaining fallback adapters must remain deterministic, never random

---

## W5: Sequence-level training harness (P1, depends on W1)

### Current problem

`train.py` calls `model(x, regime)` per batch with no state carry-over. The model's `forward()` accepts `prev_memory_state` and `prev_object_slots` but these are never passed. Each training step treats the window as the start of a fresh sequence. This means:
- State recurrence (StateTokenRecurrence) is never exercised across windows
- AnchorBank never accumulates entries across windows during training
- Bus feedback is never available from a previous window (compounded by W1)
- The model cannot learn temporal dependencies

### Required changes

**train.py:**
- Add a `sequence_length` config parameter (default: 3 windows)
- Modify the training loop to unroll across windows:
  ```python
  prev_state = None
  prev_slots = None
  total_loss = 0
  for t in range(sequence_length):
      x_t = batch["features"][:, t]  # [B, N, P, D] for window t
      outputs = model(x_t, regime, prev_memory_state=prev_state,
                       prev_object_slots=prev_slots, timestep=t)
      prev_state = outputs["latent_state_tokens"].detach()  # detach for truncated BPTT
      prev_slots = outputs["object_track_set"].detach()
      losses = loss_fn(outputs, targets_t)
      total_loss = total_loss + losses["total"]
  total_loss.backward()
  ```
- Support configurable truncated BPTT: detach state every N windows (default: detach every window for memory safety; optionally allow gradient flow for 2-3 windows)

**data/synthetic.py:**
- Extend `SyntheticSequenceDataset` to produce multi-window sequences: each sample is `[seq_len, N_frames, P, D]` instead of `[N_frames, P, D]`
- Add inter-window consistency: objects that persist across windows should have correlated features (enabling the model to learn permanence tracking)

### Verification

- Test: run 3-window training step, verify `bank_occupancy > 0` at window 2
- Test: verify `prev_state` is not None at window 2
- Test: verify loss decreases over training epochs (convergence)
- Test: verify gradient flow does not explode (check grad norms per window)
- Memory test: verify GPU memory stays within bounds for 3-window unroll on a single GPU

### Files touched

- `train.py`: ~50 lines modified/added
- `data/synthetic.py`: ~40 lines modified
- `tests/test_sequence_training.py`: new, ~60 lines

---

## W6: Permanence mechanism hardening (P1)

### Implementation status update (2026-05-10)

Implemented:
- `Permanence.dynamic_ratio` and `suppress_static_write` are per-slot tensors, preserving object-level granularity.
- `Permanence.match_slots()` performs one-to-one cosine assignment across windows using exact DP/Hungarian-equivalent matching for the small slot count.
- `AnchorBank.write()` consumes per-entry/per-slot `bus_dynamic_ratio` when dimensions align, suppressing only affected entries.
- `Dream3R.forward()` exposes `suppress_static_write` and `cr2_per_slot_suppress`; v0.1 keeps legacy aggregated dynamic ratio for backward compatibility.

Verified on server:
- `python -m dream3r.tests.test_permanence_v2`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Current problem

Permanence (modules.py:257-349) implements Slot Attention correctly, but:
1. The mint gate (line 294) takes `conflict_score` but this is always `None` (W1 issue), so mint conservatism is never conflict-modulated
2. `dynamic_ratio` is a single scalar per batch (line 333) — it averages over all slots, losing per-object information
3. The `suppress_static_write` decision (line 341) is a binary any-slot argmax — if ANY slot has region=0 (suppress), the entire batch suppresses. This is too aggressive for multi-object scenes.
4. Object identity is not validated across windows — there's no mechanism to match slots from window t-1 to slots at window t

### Required changes

**modules.py (Permanence):**
- After W1 fix, verify that `bus_conflict_score` actually arrives with real values
- Change `dynamic_ratio` from batch-mean to per-slot: return `[B, n_slots, 1]` instead of `[B, 1]`
- Change `suppress_static_write` from batch-any to per-slot or weighted: return a per-slot suppress decision, then let the bus aggregate (e.g., weighted by slot attention confidence)
- Add a slot matching mechanism for cross-window identity: use Hungarian matching or cosine similarity between `prev_slots` and current `slots` to establish correspondences. This is critical for tracking persistent objects across windows.

**bus.py:**
- Update `gate_cr2()` to handle per-slot suppress signals (aggregate to per-batch if Memory needs a single decision)
- Add `cr2_per_slot_suppress()` for modules that want per-slot granularity

### Verification

- Test: create 2-window sequence with known persistent objects, verify slot matching assigns consistent IDs
- Test: verify per-slot dynamic_ratio differs between static and dynamic objects
- Test: verify suppress is not triggered for the entire batch when only one slot is suppressed

### Files touched

- `modules.py`: ~40 lines modified
- `bus.py`: ~15 lines added
- `tests/test_permanence_v2.py`: new, ~80 lines

---

## W7: Critic loop closing (P1)

### Implementation status update (2026-05-10)

Implemented:
- Action 0 is now explicit `noop` in `repair_action_log`.
- Action 1 (`increase_retrieval`) is consumed by Memory on the next tick and raises NSA selected top-k.
- Action 2 (`reroute`) is consumed by Composer on the next tick and forces low critic confidence for routing.
- Actions 3/4/5 remain documented stubs for later reset/refine/skip semantics.

Verified on server:
- `python -m dream3r.tests.test_critic_loop`
- `python -m dream3r.tests.test_cr3_policy`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Current problem

The Critic (modules.py:356-406) produces `conflict_score` and `repair_logits`, but:
1. `repair_logits` has 6 actions but the model never acts on them — they're computed but discarded
2. The Critic reads `capability_match` and `latent_drift_proxy` from the bus, but currently these are same-tick reads, not cross-tick. After W1, the question is: should the Critic read current or previous values?
3. There's no mechanism for the Critic to actually trigger repair — the "recommended_action" is not consumed by any module

### Required changes

**model.py:**
- Define what each repair action means in practice:
  - 0: no_action — default, do nothing
  - 1: increase_retrieval — signal Memory to increase top-k next tick (already partially implemented via CR-3)
  - 2: reroute — signal Composer to change expert selection (already gated by CR-1)
  - 3: reset_memory — signal Memory to partially reset AnchorBank (quarantine low-confidence entries)
  - 4: refine — signal Memory to re-attend with higher precision (reduce sliding window, increase selected branch weight)
  - 5: skip — signal all modules to skip update and carry forward previous state
- Implement at least actions 0, 1, 2 as bus signals that downstream modules consume in the next tick (via `read_previous` from W1)
- The other actions (3, 4, 5) can be stubbed but documented

**bus.py:**
- Add owner table entries for repair action signals
- Add `recommended_action` to the previous-signal rotation

### Verification

- Test: inject high conflict, verify Critic recommends non-zero action
- Test: at next tick, verify Memory reads the recommended action and adjusts behavior
- Test: verify CR-1 gate blocks reroute when capability spread is low

### Files touched

- `model.py`: ~30 lines modified
- `bus.py`: ~10 lines added
- `modules.py`: ~10 lines modified (Critic output handling)
- `tests/test_critic_loop.py`: new, ~70 lines

---

## W8: NSA architecture refinement (P2)

### Current problem

NSA (nsa_attention.py) is functionally correct but architecturally basic compared to the DeepSeek NSA paper:
1. No blockwise parallel attention — current implementation is standard MHA per branch
2. No kernel-level optimization — pure PyTorch, no Triton/CUDA kernels
3. The compressed branch uses a simple linear projection instead of learned compression tokens
4. Gate fusion is a simple 3-way softmax — no hierarchical or sparse gating

### Required changes (research-grade, not production)

**nsa_attention.py:**
- Replace the gate MLP with a MoE-style top-2 gating: at each query position, only activate the top-2 branches instead of all 3. This saves compute and forces specialization.
- Add a compression quality loss: the compressed branch output should reconstruct the full sequence when upsampled (auxiliary loss, not primary)
- Add optional FlashAttention integration: if `flash_attn` is available, use it for the per-branch MHA. This is a pure speed optimization that doesn't change the architecture.

**Longer-term (not in this cycle):**
- Triton kernel for fused 3-branch attention
- Blockwise parallelism for long sequences
- Hierarchical compression (multi-level state tokens)

### Verification

- Test: with top-2 gating, verify one branch weight is always ~0
- Profile: measure latency reduction from FlashAttention integration
- Quality: verify branch specialization (compressed = long-term, selected = spatial, sliding = local) via weight analysis

### Files touched

- `nsa_attention.py`: ~60 lines modified/added
- `tests/test_nsa_attention.py`: updated, ~30 lines added

---

## W9: Loss and training advancement (P2)

### Implementation status (2026-05-09)

Implemented:
- `geometric_consistency` over cross-window pointmap displacement on overlapping patches
- `retrieval_quality` from selected anchor scores and finite 3D anchor distances
- routing utilization loss hardened for sparse branch weights
- `state_drift_regularization` on latent drift proxy
- configurable small weights in `config.py` and sequence-loop plumbing in `train.py`
- persistent Bus/AnchorBank state is detached across optimizer steps to prevent stale autograd graphs
- tests in `tests/test_loss_advancement.py`, `tests/test_training_convergence.py`, and sequence regression coverage

### Current problem

The loss function (losses.py) has basic terms but lacks:
1. No geometric consistency loss between predicted pointmaps across windows
2. No retrieval quality loss (are retrieved anchors actually useful?)
3. No routing diversity loss (prevent the router from always picking the same expert)
4. No drift regularization (prevent latent state from drifting too far from initialization)

### Required changes

**losses.py:**
- Add `geometric_consistency_loss`: for overlapping regions between windows, predicted 3D points should be consistent under the ground-truth relative pose
- Add `retrieval_quality_loss`: retrieved bank entries should have high cosine similarity with the current frame's features in the overlapping region
- Add `routing_entropy_loss`: encourage the router to explore multiple experts during training (prevent mode collapse to a single expert)
- Add `state_drift_regularization`: penalize large L2 drift of state tokens from their initialization

**train.py:**
- Add these losses to the training loop with configurable weights
- Default to small weights (0.01-0.05) so they don't dominate

### Verification

- Test: verify each loss term computes without NaN
- Test: verify routing entropy loss prevents single-expert collapse
- Training: verify total loss still converges with new terms

### Files touched

- `losses.py`: ~80 lines added
- `config.py`: ~10 lines (new weight params)
- `train.py`: ~5 lines (pass new loss terms)

---

## W10: Evaluation and metrics (P2)

### Implementation status (2026-05-09)

Implemented:
- pointmap L2 and threshold accuracy metrics
- depth AbsRel/SqRel/RMSE/RMSE_log/delta metrics
- Chamfer-L2 and F-score metrics at 0.05/0.10 thresholds
- architecture metrics for branch entropy, selected 3D anchor distance, geometry-bias usage, bank occupancy, routing entropy, and state drift
- frame-budget profiling now reports architecture metrics and peak CUDA memory alongside latency
- tests in `tests/test_evaluate_metrics.py`

### Current problem

`evaluate.py` exists but lacks standard 3D reconstruction metrics. Without metrics, there's no way to quantify architectural improvements.

### Required changes

**evaluate.py:**
- Add standard depth metrics: AbsRel, SqRel, RMSE, RMSE_log, delta thresholds (1.25, 1.25^2, 1.25^3)
- Add standard 3D metrics: Chamfer distance, F-score at multiple thresholds
- Add pointmap accuracy: per-point L2 error, percentage within thresholds
- Add architectural metrics: bank utilization, branch weight distribution, routing diversity, state drift magnitude
- Output a structured JSON report

**bench_frame_budget.py:**
- Add architectural metric tracking during profiling
- Report memory usage alongside latency

### Verification

- Test: compute metrics on synthetic data with known ground truth
- Test: verify metrics match expected values for perfect predictions (all errors = 0)

### Files touched

- `evaluate.py`: ~100 lines added
- `bench_frame_budget.py`: ~20 lines added

---

## W11: DINOv2/v3 frozen encoder (P1 — highest single-item impact)

### Implementation status update (2026-05-10)

Implemented:
- `Perceiver` accepts `backbone_type`, `backbone_freeze`, and `backbone_checkpoint_path`.
- DINOv2 hub backbones are frozen by default and expose patch tokens through `forward_features()` when available.
- Trainable pointmap/confidence heads and evidence projectors remain on top of the frozen backbone.
- Fallback path preserves existing timm/random-feature behavior when the requested backbone cannot be loaded.
- Config/model presets thread the new backbone options; `small` remains feature-input/no-backbone, `small_vit` uses DINOv2.

Verified on server without downloading weights by monkeypatching `torch.hub.load`:
- `python -m dream3r.tests.test_dinov2_backbone`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Why this matters

Every competitive 3R method (VGGT, MASt3R, Depth Anything, CUT3R) uses DINOv2 or DINOv3 as its visual backbone. DINOv3 (late 2025, 7B teacher) introduced Gram Anchoring for stable patch features and RoPE for resolution robustness. Dream3R's current Perceiver uses either a randomly initialized ViT or raw pre-extracted features. Without foundation-model-quality features, all downstream modules (memory, matching, routing) operate on weak input representations. This is the single largest quality gap.

### Required changes

**modules.py (Perceiver):**
- Add a `backbone_type` config: `"none"` (current), `"dinov2_vitb14"`, `"dinov2_vitl14"`, `"dinov3"` (future)
- For DINOv2/v3 modes:
  - Load frozen pretrained weights via `torch.hub.load("facebookresearch/dinov2", ...)` or local checkpoint
  - Freeze all backbone parameters (`requires_grad_(False)`)
  - Add a lightweight adapter: `nn.Linear(backbone_dim, d_model)` to project DINOv2 features to the model's internal dimension
  - Keep the evidence projectors, pointmap head, and confidence head as trainable layers on top of frozen features
- The backbone should be lazy-loaded: if `use_backbone=True` but the model is unavailable, fall back to current behavior with a warning

**config.py:**
- Add `backbone_type`, `backbone_freeze`, `backbone_checkpoint_path` parameters
- Default: `backbone_type="dinov2_vitb14"`, `backbone_freeze=True`

**model.py:**
- No changes needed — Perceiver already handles backbone vs pre-extracted features

### Verification

- Test: load DINOv2-B, freeze, run forward, verify output shapes match
- Test: verify backbone gradients are all None when frozen
- Test: verify evidence projectors and heads still receive gradients
- Profile: measure latency increase from DINOv2-B backbone (expect ~20-30ms per frame on server GPU)
- Quality: compare evidence token variance with DINOv2 features vs random init (should be dramatically higher)

### Server dependency

- `pip install timm` (likely already available)
- DINOv2-B weights auto-download from torch hub (~350MB) or can be pre-cached at `/hdd3/kykt26/models/dinov2/`
- DINOv3 requires manual download when available

### Files touched

- `modules.py`: ~40 lines modified (Perceiver backbone loading)
- `config.py`: ~5 lines added
- `tests/test_dinov2_backbone.py`: new, ~50 lines

---

## W12: 3D position embeddings for AnchorBank (P1, depends on W3)

### Why this matters

Point3R (NeurIPS 2025) showed that adding 3D hierarchical position embeddings to memory pointers dramatically improves spatial retrieval. Dream3R's W3 adds `points3d_mean` storage to AnchorBank, but retrieval is still purely based on latent vector similarity. Without 3D-aware retrieval, the memory cannot answer "what did I see near this 3D location?" — it can only answer "what looks similar in latent space?"

### Implementation status update (2026-05-10)

Implemented:
- `AnchorBank.encode_3d_position()` adds multi-frequency sinusoidal 3D position encoding.
- `AnchorBank.read()` now supports `query_points3d`, `spatial_retrieval_mode`, and `spatial_bias_alpha`.
- Supported modes: `latent_only`, `latent_plus_3d`, and `3d_only`.
- `SpatialMemory` / config now expose `anchor_spatial_bias_alpha` and `anchor_spatial_retrieval_mode`.
- Added `tests/test_3d_retrieval.py` for tied-latent spatial ranking and legacy latent-only equivalence.

Verified on server:
- `python -m dream3r.tests.test_3d_retrieval`
- `python -m dream3r.tests.test_anchor_bank`
- `python -m dream3r.tests.test_spatial_payload`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`

### Required changes

**anchor_bank.py:**
- Add a 3D positional encoding function: `encode_3d_position(points3d) -> [B, N, d_pos]`
  - Use sinusoidal encoding with multi-scale frequencies (similar to NeRF positional encoding but with 3 input dims)
  - Hierarchical: coarse (room-scale) + fine (patch-scale) frequencies
- Modify `read()` to combine latent similarity with 3D proximity:
  - Compute 3D distance between query points and stored `points3d_mean`
  - Add a 3D proximity bonus to retrieval scores: `score = latent_sim + alpha * 3d_proximity`
  - `alpha` is a learnable scalar or configurable hyperparameter
- Add `spatial_retrieval_mode` config: `"latent_only"` (current), `"latent_plus_3d"` (new default), `"3d_only"` (for ablation)

**modules.py (SpatialMemory):**
- Pass query frame's pointmap-derived 3D positions into bank read
- Add 3D positional encoding to bank keys at write time

### Verification

- Test: write two anchors at different 3D locations with similar latent features; query near one location; verify the spatially closer anchor ranks higher
- Test: verify `spatial_retrieval_mode="latent_only"` reproduces current behavior exactly
- Ablation: compare retrieval precision with and without 3D position embeddings

### Files touched

- `anchor_bank.py`: ~50 lines added
- `modules.py`: ~15 lines modified
- `tests/test_3d_retrieval.py`: new, ~70 lines

---

## W13: Active/stable state decoupling (P1, depends on W5)

### Implementation status update (2026-05-10)

Implemented:
- `StateTokenRecurrence` is treated as active state; `AnchorBank` is treated as stable state.
- `SpatialMemory.promote_to_stable()` promotes high-confidence active state tokens into AnchorBank.
- `SpatialMemory.recall_from_stable()` injects retrieved stable anchors back into memory output on revisits.
- `AnchorBank.stability_score` increments per tick for valid non-quarantined entries and protects stable entries during prune/evict.
- Config/model expose `active_to_stable_threshold`, `stable_recall_threshold`, `stable_recall_strength`, and `stability_prune_bonus`.

Verified on server:
- `python -m dream3r.tests.test_active_stable`
- `python -m dream3r.tests.test_anchor_bank`
- `python -m dream3r.tests.test_spatial_memory`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Why this matters

OnlineX (March 2026) demonstrated that decoupling state into active (fast-changing local geometry) and stable (long-term global structure) prevents the temporal forgetting that plagues CUT3R's fixed-size state. Dream3R has `StateTokenRecurrence` (active-like) and `AnchorBank` (stable-like) but does not explicitly manage the promotion/demotion between them.

### Required changes

**modules.py (SpatialMemory):**
- Formalize AnchorBank as the "stable state" and StateTokenRecurrence as the "active state"
- Add a `promote_to_stable()` mechanism: when active state tokens reach high confidence (measured by write_confidence or Critic signal), promote them to AnchorBank entries
- Add a `recall_from_stable()` mechanism: when the model re-visits a previously seen region (detected by high retrieval scores from bank), inject the stable anchor back into active processing via cross-attention
- Add a `stability_score` per bank entry: entries that survive multiple windows without quarantine gain higher stability, making them harder to prune

**anchor_bank.py:**
- Add `stability_score` buffer: `[B, capacity]`, initialized to 0, incremented each tick for entries that remain valid and non-quarantined
- Modify `prune()` to factor in `stability_score`: stable entries require higher pressure to evict
- Add `promote()` method: accepts state tokens + confidence, writes to bank with initial stability=0

### Verification

- Test: run 5-window sequence, verify some entries reach stability > 3
- Test: verify stable entries survive pruning that removes newer entries
- Test: verify recall mechanism activates when revisiting a location (high retrieval score threshold)

### Files touched

- `modules.py`: ~50 lines modified
- `anchor_bank.py`: ~30 lines added
- `tests/test_active_stable.py`: new, ~80 lines

---

## W14: SSR Grassmannian drift regularizer (P1 — plug-and-play, no training needed)

### Why this matters

SSR (March 2026) provides a training-free Grassmannian manifold regularizer that prevents geometric drift in streaming reconstruction. It constrains state updates to lie on a smooth manifold, preventing the kind of accumulating error that causes long-sequence degradation. This is the highest impact-to-effort ratio item: it requires no training, no new parameters, and can be added as a single function call in the state update path.

### Implementation status update (2026-05-10)

Implemented:
- `StateTokenRecurrence.grassmannian_regularize()` removes a configurable parallel drift component from state updates.
- `grassmannian_strength` is threaded through `config.py`, `model.py`, and `SpatialMemory`.
- Default strength is `0.1`; `0.0` preserves the old update exactly.
- Added `tests/test_drift_regularizer.py`.

Verified on server:
- `python -m dream3r.tests.test_drift_regularizer`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- `python -m dream3r.tests.test_nsa_attention`
- `python -m dream3r.tests.test_anchor_bank`
- `python -m dream3r.tests.test_composer_experts`
- `python -m dream3r.tests.test_spatial_memory`

### Required changes

**modules.py (StateTokenRecurrence):**
- After computing `new_state`, apply Grassmannian projection:
  ```python
  def grassmannian_regularize(prev_state, new_state, strength=0.1):
      # Project the state update onto the tangent space of the Grassmannian
      # manifold at prev_state, preventing drift off the manifold
      delta = new_state - prev_state
      # Orthogonal projection: remove component parallel to prev_state
      proj = prev_state * (delta * prev_state).sum(dim=-1, keepdim=True) / (prev_state.norm(dim=-1, keepdim=True) ** 2 + 1e-8)
      regularized_delta = delta - strength * proj
      return prev_state + regularized_delta
  ```
- Add `grassmannian_strength` config parameter (default: 0.1)
- This is applied AFTER the cross-attention and self-attention updates, BEFORE the FFN

### Verification

- Test: run 10-window sequence with and without regularizer; measure state token L2 drift from initialization
- Test: verify regularized drift is monotonically smaller than unregularized
- Test: verify reconstruction quality (pointmap L2) does not degrade with regularizer

### Files touched

- `modules.py`: ~15 lines added
- `config.py`: ~2 lines added
- `tests/test_drift_regularizer.py`: new, ~40 lines

---

## W15: Critic geometric consistency signals (P2, depends on W7)

### Implementation status update (2026-05-10)

Implemented:
- `Critic` accepts `pointmap_pair` and `confidence_pair` alongside evidence tokens.
- Added differentiable Sampson-like geometric residual, covisible inconsistency, confidence disagreement, and depth inconsistency features.
- Geometry features are projected as an additional Critic transformer token and also bias `conflict_score`, so shifted/inconsistent pointmaps trigger repair pressure even before training.
- `Dream3R.forward()` passes the first overlapping view pair into Critic and exposes `critic_geometric_log`.
- `Dream3RLoss` now includes `sampson_distance` and `covisibility_consistency` losses; config/train weights are threaded.
- Added `tests/test_geometric_critic.py`.

Verified on server:
- `python -m dream3r.tests.test_geometric_critic`
- `python -m dream3r.tests.test_loss_advancement`
- `python -m dream3r.tests.test_critic_loop`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Why this matters

Test3R (2025) and TTT3R (2025-2026) showed that pairwise geometric consistency is the right self-supervised signal for detecting reconstruction errors. Dream3R's Critic currently reads abstract evidence tokens but has no access to actual geometric verification. Adding Sampson distance (epipolar consistency) and differentiable covisible maps (occlusion awareness) gives the Critic real geometric reasoning ability.

### Required changes

**modules.py (Critic):**
- Add geometric consistency inputs alongside evidence tokens:
  - `pointmap_pair`: `[B, 2, P, 3]` — predicted pointmaps for a pair of overlapping views
  - `confidence_pair`: `[B, 2, P, 1]` — confidence for each view
- Compute Sampson distance: measure epipolar consistency between the two pointmaps
- Compute covisible mask: differentiable estimate of which points are visible in both views
- Feed these as additional tokens to the Critic's transformer encoder
- The `conflict_score` should now reflect geometric inconsistency, not just abstract evidence disagreement

**losses.py:**
- Add `sampson_distance_loss`: penalize predicted correspondences that violate epipolar geometry
- Add `covisibility_consistency_loss`: penalize predictions where covisible regions have inconsistent depth/pointmap

### Verification

- Test: create a pair with known geometric inconsistency (shifted pointmap), verify Critic detects it (high conflict_score)
- Test: create a consistent pair, verify low conflict_score
- Test: verify Sampson distance is zero for perfectly consistent predictions

### Files touched

- `modules.py`: ~40 lines modified (Critic)
- `losses.py`: ~30 lines added
- `tests/test_geometric_critic.py`: new, ~60 lines

---

## W16: ISA per-slot reference frames (P2, depends on W6)

### Implementation status update (2026-05-10)

Implemented:
- `Permanence` now emits `object_slot_poses: [B, n_slots, 7]` with attention-weighted translation plus identity quaternion.
- Slot attention incorporates pointmap-derived token positions via `position_proj`.
- When previous slot poses are available, attention logits receive a pose-distance bias in each slot reference frame.
- `Permanence.match_slots()` supports pose-aware one-to-one matching, combining feature cosine assignment with pose proximity.
- `Dream3R.forward()` accepts `prev_object_slot_poses`, passes pointmap-derived positions into Permanence, and exposes `object_slot_poses`.
- Added `tests/test_isa_slots.py`.

Verified on server:
- `python -m dream3r.tests.test_isa_slots`
- `python -m dream3r.tests.test_permanence_v2`
- `python -m dream3r.tests.test_sequence_training`
- `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
- full `dream3r.tests.test_*` suite


### Why this matters

Invariant Slot Attention (2025) showed that giving each slot its own learnable reference frame (translation, rotation, scale) makes object tracking equivariant under camera motion. Dream3R's Permanence tracks slots but has no mechanism to account for the fact that the same object appears at different positions/scales as the camera moves. Without this, slot matching across windows degrades rapidly under large viewpoint changes.

### Required changes

**modules.py (Permanence):**
- Add per-slot pose parameters: `slot_poses: [B, n_slots, 7]` (3 translation + 4 quaternion)
- Before slot attention iterations, transform input features into each slot's reference frame
- After slot attention, update slot poses based on the attention-weighted input positions
- The slot matching mechanism from W6 should use pose-aware similarity: slots are matched based on both feature similarity AND pose proximity

### Verification

- Test: track an object across 3 windows with camera rotation; verify slot pose updates track the apparent motion
- Test: verify slot matching accuracy improves vs W6 baseline (cosine-only matching)

### Files touched

- `modules.py`: ~50 lines modified
- `tests/test_isa_slots.py`: new, ~60 lines

---

## W17: Mamba-Transformer hybrid blocks (P3 — major architectural change)

### Why this matters

The 2025-2026 trend is Mamba-Transformer hybrids: Mamba for O(N) sequential processing, Transformer for global attention at critical positions. For streaming 3D, Mamba is natural for the temporal dimension (sequential frames), while Transformer handles spatial reasoning within each frame. SF-Mamba (March 2026) addresses the causality limitation with patch swapping.

### Required changes

**New file: `mamba_block.py`:**
- Implement a Mamba block (or wrap `mamba_ssm` package if available)
- Create `MambaTransformerBlock`: Mamba processes temporal sequence, Transformer handles spatial cross-attention
- This replaces `StateTokenRecurrence`'s cross-attention with a hybrid: Mamba for state evolution, Transformer for frame-state interaction

**modules.py:**
- Add `state_recurrence_type` config: `"cross_attention"` (current), `"mamba_hybrid"` (new)
- `MambaHybridRecurrence`: Mamba evolves state tokens temporally, Transformer cross-attends to current frame tokens

### Verification

- Test: verify Mamba hybrid produces same-shape outputs as cross-attention recurrence
- Profile: measure latency reduction for 10+ window sequences
- Quality: verify convergence on synthetic training

### Files touched

- `mamba_block.py`: new, ~100 lines
- `modules.py`: ~30 lines modified
- `config.py`: ~3 lines added

### External dependency

- `mamba_ssm` package (pip install mamba-ssm, requires CUDA)

---

## W18: 3DGS output head (P3 — new output representation)

### Why this matters

3D Gaussian Splatting has become the dominant 3D output representation, replacing NeRF for real-time rendering. AnchorSplat (2026) showed that anchor-aligned Gaussians with geometric priors outperform pixel-aligned ones. Adding a 3DGS prediction head to Dream3R enables:
- Novel view synthesis (renders from arbitrary viewpoints)
- Photometric self-supervision (render-and-compare loss)
- Direct comparison with VGGT and other methods on rendering benchmarks

### Required changes

**New file: `gaussian_head.py`:**
- Predict per-point Gaussian parameters from frame tokens: mean (3D position from pointmap), covariance (learned 6-param), color (RGB from input), opacity (from confidence)
- Use AnchorBank entries as Gaussian anchors: each bank entry becomes a Gaussian center with learned attributes
- Support differentiable rendering via `diff-gaussian-rasterization` or `gsplat`

**model.py:**
- Add optional `gaussian_head` module, controlled by config
- After SpatialMemory, predict Gaussians from frame tokens + bank entries
- Include rendered images in output dict

**losses.py:**
- Add photometric rendering loss: L1 + SSIM between rendered and input images
- This enables self-supervised training without ground-truth depth

### Verification

- Test: predict Gaussians from synthetic data, render from training viewpoint, verify low photometric error
- Test: render from novel viewpoint, verify plausible output
- Profile: measure rendering overhead (expect ~5-10ms per frame with gsplat)

### Files touched

- `gaussian_head.py`: new, ~120 lines
- `model.py`: ~20 lines modified
- `losses.py`: ~20 lines added
- `config.py`: ~5 lines added

### External dependency

- `gsplat` or `diff-gaussian-rasterization` package

---

## Execution order and dependencies

```
Phase 1 (P0 — unblocks everything):
  W1 (bus temporal) ──> W2 (CR-3 policy)
  W3 (spatial payload) [independent of W1]

Phase 2 (P1 — real architecture + breakthroughs):
  W4  (expert integration)         [independent]
  W5  (sequence training)          [depends on W1]
  W6  (permanence hardening)       [depends on W1]
  W7  (critic loop)                [depends on W1]
  W11 (DINOv2/v3 encoder)          [independent — highest single impact]
  W12 (3D position embeddings)     [depends on W3]
  W13 (active/stable decoupling)   [depends on W5]
  W14 (SSR drift regularizer)      [independent — plug-and-play]

Phase 3 (P2 — competitive edge):
  W8  (NSA refinement)             [independent]
  W9  (loss advancement)           [depends on W5]
  W10 (evaluation)                 [independent]
  W15 (Critic geometric signals)   [depends on W7]
  W16 (ISA per-slot frames)        [depends on W6]

Phase 4 (P3 — next-generation, separate cycle if needed):
  W17 (Mamba hybrid)               [major architectural change]
  W18 (3DGS output head)           [new output representation]
```

Recommended parallel execution:

- Phase 1: W1 first (1-2 sessions), then W2 + W3 in parallel
- Phase 2: W11 + W14 can start immediately (no dependencies). W4/W5/W6/W7 after W1. W12 after W3. W13 after W5.
- Phase 3: after Phase 2 stabilizes
- Phase 4: separate authorization required

---

## Constraints

- All code changes are server-side only (per F-002)
- Local Windows = editing + markdown + orchestration only
- No real data training without explicit user approval
- No checkpoint download without explicit user approval (DINOv2 auto-download via torch hub is acceptable for W11)
- Expert adapter integration (W4) requires server access for method checkpoints
- W17 (Mamba) requires `mamba_ssm` package install — separate approval needed
- W18 (3DGS) requires `gsplat` or `diff-gaussian-rasterization` — separate approval needed
- All verification is server-side via ssh

## Estimated scope

- W1-W10 (original): ~800-1200 lines, 8 test files, 5-8 sessions
- W11-W14 (P1 breakthroughs): ~300 lines, 4 test files, 3-4 sessions
- W15-W16 (P2 breakthroughs): completed 2026-05-10
- W17-W18 (P3 future): ~350 lines, separate cycle if needed
- Each workstream is independently testable and shippable

---

## Agent execution guidance

This section is for the executing agent. Read this before starting any workstream.

### Setup

1. Read `REVIEW_PROMPT.md` for current architecture overview and known gaps
2. Read this file completely — understand all workstreams and dependencies
3. Verify server access: `ssh BUAA-Server` then `cd /hdd3/kykt26/code/dream3r`
4. Verify current code state: `git status && git log --oneline -5`
5. Verify smoke test passes before any changes: `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`

### Per-workstream protocol

For each workstream W_n:

1. **Read** all files listed in "Files touched" completely
2. **Understand** the current implementation before changing anything
3. **Implement** the changes described — do not add scope beyond what's listed
4. **Test** using the verification steps listed. Every test must pass.
5. **Run smoke test** after changes: `CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test`
6. **Run unit tests**: `python -m dream3r.tests.test_nsa_attention && python -m dream3r.tests.test_anchor_bank && python -m dream3r.tests.test_composer_experts && python -m dream3r.tests.test_spatial_memory`
7. **Report** what changed, what was tested, what passed/failed

### Code quality rules

- No comments unless the WHY is non-obvious
- No docstrings longer than one line
- Match existing code style (type hints, Dict returns, bus publish/read pattern)
- Every new parameter must have a default value
- Every new test must be runnable standalone: `python -m dream3r.tests.test_<name>`
- Keep backward compatibility with v0.1 modules (they're preserved for ablation)
- Do not change the ExpertOutput dataclass interface
- Do not change the bus owner table without updating this plan
- Do not add external dependencies without noting them here

### Architecture invariants (do not break)

1. Bus ownership: only the designated owner can publish a signal
2. CR-1..CR-6 naming: these are the contract names used in specs and paper
3. v0.1 backward compatibility: `MemorySSM_v01` and `Composer_v01` must still work
4. ExpertOutput contract: `{pointmap, confidence, evidence_tokens, metadata}`
5. NSA 3-branch structure: compressed + selected + sliding
6. AnchorBank lifecycle: reset per sequence, tick per window
7. Model output dict: all existing keys must remain; new keys may be added

### Error handling

- If smoke test fails after changes, revert and investigate before proceeding
- If a workstream requires changes to an invariant listed above, stop and report — do not proceed
- If GPU memory exceeds available capacity during testing, reduce batch size or sequence length, do not remove functionality
- If an import fails (missing package), note it as a dependency and skip that test, do not install packages without approval

### What success looks like

After all Phase 1-3 workstreams complete:

- `bus.read_previous()` returns real signals at window 2+ (W1)
- CR-3 measurably changes retrieval depth and scoring under different conflict levels (W2)
- AnchorBank stores and retrieves 3D spatial payloads with 3D position embeddings (W3 + W12)
- At least two expert adapters produce real (non-random) features; MASt3R and Spann3R currently satisfy this (W4)
- Training unrolls across 3+ windows with state carry-over (W5)
- Permanence tracks objects across windows with per-slot granularity and ISA reference frames (W6 + W16)
- Critic repair actions are consumed by downstream modules and backed by geometric consistency signals (W7 + W15)
- NSA uses top-2 gating and optional FlashAttention (W8)
- Loss includes geometric consistency, retrieval quality, routing entropy, and drift regularization (W9)
- Standard depth/3D/architectural metrics are computed and reported (W10)
- Perceiver uses frozen DINOv2/v3 features as backbone (W11)
- AnchorBank retrieval is 3D-position-aware, not just latent-similarity (W12)
- State architecture has explicit active/stable decoupling with promotion mechanism (W13)
- Grassmannian regularizer prevents geometric drift in streaming mode (W14)
- All existing smoke tests (9/9) and unit tests (4/4) still pass
- New tests (14+ files) all pass
- Profiling stays under 30ms/frame for the `small` preset (relaxed from 20ms due to DINOv2 backbone)
