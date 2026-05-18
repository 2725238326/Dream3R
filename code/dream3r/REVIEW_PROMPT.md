# Dream3R v0.3 Code Review Prompt

Use this prompt to onboard a new agent (Claude, Codex, or human) for reviewing,
extending, or debugging the Dream3R v0.3 codebase.

---

## Context

Dream3R is a streaming 3D reconstruction architecture organized around 6 modules
communicating through a typed memory bus (C6). The project lives at:

- **Local (Windows):** `E:\kykt\Dream\code\dream3r\` — editing, orchestration, markdown
- **Server (Linux):** `/hdd3/kykt26/code/dream3r/dream3r/` — GPU execution, training

SSH: `ssh BUAA-Server` (config alias for `kykt26@172.17.140.97`)

## Architecture at a glance

```
C1 Perceiver ─── T1 frame_tokens, T2 pointmap, T3 evidence (17 signals)
      │
C3 Permanence ── dynamic_ratio, suppress_static_write ──┐
      │                                                   │ CR-2
C2 SpatialMemory ── NSA(compressed+selected+sliding) ────┤
      │              AnchorBank(K=256, bus-gated writes)  │ CR-3
      │              StateTokenRecurrence(32 tokens)      │
      │                                                   │
C5 ComposerRouter ── 7 experts, cost-normalized routing ──┤
      │                                                   │ CR-1
C4 Critic ── conflict_score, repair_action ───────────────┘
      │
C6 MemoryBus ── publish/read/handoff + CR-1..CR-6 gates
```

## File map (29 Python files)

### Core modules
| File | What it does | Key classes |
|------|-------------|-------------|
| `model.py` | Top-level orchestrator, one bus tick = one window | `Dream3R`, `build_dream3r` |
| `modules.py` | C1-C5 computational cores (v01 + v03) | `Perceiver`, `SpatialMemory`, `Permanence`, `Critic`, `ComposerRouter` |
| `bus.py` | C6 typed tensor namespace, CR-1..CR-6 | `MemoryBus`, `BusSignal`, `EvidenceLabel` |
| `nsa_attention.py` | 3-branch Native Sparse Attention | `NSAAttention`, `CompressedBranch`, `SelectedBranch`, `SlidingBranch` |
| `anchor_bank.py` | Bounded spatial K/V memory | `AnchorBank`, `WriteResult`, `ReadResult` |
| `losses.py` | Multi-task loss with geometry/retrieval/routing/drift terms | `Dream3RLoss` |
| `config.py` | YAML config + presets | `load_config`, `PRESETS`, `config_to_model_args` |

### Composer experts (7 adapters)
| File | Expert | Latency | Strength |
|------|--------|---------|----------|
| `composer_experts/mast3r_adapter.py` | MASt3R | 35ms | real checkpoint path + deterministic fallback |
| `composer_experts/fast3r_adapter.py` | Fast3R | 12ms | checkpoint artifacts present; env missing `omegaconf` |
| `composer_experts/spann3r_adapter.py` | Spann3R | 28ms | real checkpoint path + streaming memory fallback |
| `composer_experts/cut3r_adapter.py` | CUT3R | 30ms | state token recurrence |
| `composer_experts/moge2_adapter.py` | MoGe-2 | 18ms | sparse_view 0.9 |
| `composer_experts/depthanything_adapter.py` | DAv2 | 8ms | monocular depth |
| `composer_experts/test3r_adapter.py` | Test3R | 120ms | offline verification |

MASt3R is loadable through `DREAM3R_RUN_MAST3R_INTEGRATION=1`. Spann3R is loadable through `DREAM3R_RUN_SPANN3R_INTEGRATION=1`; the server currently uses slow PyTorch RoPE2D fallback because the cuda RoPE2D extension is absent. Other unloaded adapters use deterministic image-derived fallback outputs, not random projections. Fast3R has repo/checkpoint artifacts present, but the current `dream3r` conda env lacks `omegaconf`.

### Training infrastructure
| File | Purpose |
|------|---------|
| `train.py` | DDP, AMP, multi-stage LR with freeze/unfreeze, checkpoint I/O |
| `data/synthetic.py` | Deterministic synthetic sequences + DTU stub |
| `evaluate.py` | Pointmap/depth/Chamfer/F-score + architecture metrics |
| `bench_frame_budget.py` | Per-module p50/p95/p99 latency + architecture/memory profiler |

### Tests
| File | Covers |
|------|--------|
| `smoke_test.py` | 9-section integration test (v03 forward/backward/bus/NSA/AnchorBank/experts/v01-compat/dataset) |
| `tests/test_nsa_attention.py` | NSA branch shapes, masks, gradients |
| `tests/test_anchor_bank.py` | Write/read/gating/quarantine/prune/batch |
| `tests/test_composer_experts.py` | Registry, capability matrix, deterministic adapter fallback |
| `tests/test_spatial_memory.py` | SpatialMemory + ComposerRouter init/forward/multi-window/dispatch metadata |
| `tests/test_mast3r_integration.py` | Optional real MASt3R checkpoint + dispatch path |
| `tests/test_fast3r_integration.py` | Fast3R fallback contract + artifact/dependency status |
| `tests/test_spann3r_integration.py` | Optional real Spann3R checkpoint + dispatch path |
| `tests/test_drift_regularizer.py` | W14 Grassmannian state drift regularizer |
| `tests/test_3d_retrieval.py` | W12 3D-aware AnchorBank retrieval |

## Key contracts to preserve

1. **Bus ownership**: every signal has a single owner in `bus.py:_owner_table`. Adding new signals requires registering ownership here.
2. **CR gates**: CR-1 (reroute spread gate), CR-2 (permanence write suppress), CR-3 (retrieval depth + confidence/permanence bias), CR-4 (tiebreak), CR-5 (label propagation), CR-6 (audit log).
3. **AMP safety**: all mask fills must use `torch.finfo(dtype).min` not `-1e9`. All bank writes must `.float()` before storing.
4. **v01/v03 dual mode**: `model.py` supports `version="v01"` and `version="v03"` via config. v01 classes have `_v01` suffix and are preserved for ablation.
5. **Tensor shapes** (v03 small preset):
   - Input: `[B, N=4, P=196, D=768]`
   - State tokens: `[B, S=32, D_mem=128]`
   - AnchorBank: capacity 256, key/value `[B, 256, 128]`
   - Evidence: `[B, N, 17, 32]`

## Known gaps (not yet implemented)

| ID | Gap | Priority |
|----|-----|----------|
| A4 | AnchorBank stores spatial payload and supports 3D-aware retrieval; pose is still identity until real data loader provides poses | Medium |
| A5 | DINOv3-S backbone not integrated (Perceiver still uses ViT-Base/identity) | Medium |
| A6 | Test3R lazy invocation path (Critic triggers off-path verification) | Medium |
| C1 | DTUDataset is a stub (returns random tensors) | Medium |
| C2 | No data augmentation | Low |
| D1-D4 | Depth/3D metrics implemented; pose eval, ECE, visualization still pending | Medium |
| E1 | Sequence-level synthetic streaming implemented; real dataset streaming pending | Medium |
| E2 | MASt3R and Spann3R real paths implemented; Fast3R blocked on env dependency; remaining experts deterministic fallback | High |
| E4 | AnchorBank.write still has per-batch Python loop | Low |

## How to verify changes

```bash
# SSH to server
ssh BUAA-Server

# Navigate and activate
cd /hdd3/kykt26/code/dream3r
source activate dream3r

# Clear caches
find . -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Run smoke test (must pass all 9 sections)
CUDA_VISIBLE_DEVICES=0 python -m dream3r.smoke_test

# Run unit tests
python -m dream3r.tests.test_nsa_attention
python -m dream3r.tests.test_anchor_bank
python -m dream3r.tests.test_composer_experts
python -m dream3r.tests.test_spatial_memory
python -m dream3r.tests.test_mast3r_integration
python -m dream3r.tests.test_fast3r_integration
python -m dream3r.tests.test_spann3r_integration
python -m dream3r.tests.test_drift_regularizer
python -m dream3r.tests.test_3d_retrieval

# Optional real checkpoint integrations
CUDA_VISIBLE_DEVICES=0 DREAM3R_RUN_MAST3R_INTEGRATION=1 python -m dream3r.tests.test_mast3r_integration
CUDA_VISIBLE_DEVICES=0 DREAM3R_RUN_FAST3R_INTEGRATION=1 python -m dream3r.tests.test_fast3r_integration
CUDA_VISIBLE_DEVICES=0 DREAM3R_RUN_SPANN3R_INTEGRATION=1 python -m dream3r.tests.test_spann3r_integration

# Profile latency (p95 must be < 50ms)
CUDA_VISIBLE_DEVICES=0 python -m dream3r.bench_frame_budget --preset small --n-windows 30

# Quick training test (should see loss decreasing)
CUDA_VISIBLE_DEVICES=0 python -c "
import os; os.environ['CUDA_VISIBLE_DEVICES']='0'
from dream3r.config import load_config
from dream3r.train import train
cfg = load_config(preset='small', overrides={'gpus':'0','dataset':'synthetic','epochs':5,'batch_size':4,'num_workers':0,'n_train_sequences':50,'n_val_sequences':10,'log_every':5,'eval_every_epoch':5,'save_every_epoch':10})
train(cfg)
"
```

## Review checklist for any PR touching this code

- [ ] `python -m dream3r.smoke_test` passes all 9 sections
- [ ] All 4 unit test files pass
- [ ] `bench_frame_budget.py` p95 < 50ms
- [ ] No new `-1e9` literals (use `torch.finfo(dtype).min`)
- [ ] Any new bus signal registered in `bus.py:_owner_table`
- [ ] Any new module output key added to `model.py` return dict
- [ ] `config.py` updated if new hyperparameters added
- [ ] v01 backward compatibility preserved (don't break `build_dream3r("small_v01")`)
- [ ] No server-only imports at module level (all torch imports are fine; avoid importing CUDA-only packages at top level)

## Spec references (do not re-read full files, cite by section)

- Architecture v0.2: `specs/SPEC-20260506-004-dream3r-architecture-v02.md`
- Ablation plan v0.2: `specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md`
- Memory v0.3 addendum: `specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md`
- Memory ablation addendum: `specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md`
