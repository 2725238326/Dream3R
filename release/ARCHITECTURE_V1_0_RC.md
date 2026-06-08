# Dream3R v1.0-rc1 Architecture

Date: 2026-06-06
Status: frozen release-candidate architecture

## Architecture Summary

Dream3R v1.0-rc1 is a state-conditioned reconstruction architecture built from
real proposal teachers and a bounded Dream-state fusion head.

```text
Images / windows
  -> real proposal teachers: Fast3R, MASt3R, Spann3R
  -> cached proposal bank: pointmaps, confidence, conflict metadata
  -> Dream state: memory context + conflict/reliability signals
  -> frozen StatePrior: state-only expert prior
  -> ProposalSetDecoder: proposal-set fusion with frozen prior branch
  -> bounded residual refinement: local disagreement-bounded correction
  -> final pointmap
```

The architecture is official because it has a selected checkpoint/result pair,
state-causality controls, and explicit non-claims.

## Load-Bearing Components

| Component | File | Role In v1.0-rc1 |
| --- | --- | --- |
| State prior | `code/dream3r/state_prior_head.py` | Learns expert prior from Dream state and conflict features. |
| Proposal decoder | `code/dream3r/proposal_set_decoder.py` | Mixes cached proposal pointmaps with the frozen prior branch. |
| Official wrapper | `code/dream3r/release_candidate.py` | Stable `v1.0-rc1` import surface and metadata contract. |
| RC trainer | `code/dream3r/scripts/train_proposal_set_decoder.py` | Reproduces frozen-prior, bounded-residual, shuffle/no-state controls. |
| Release verifier | `code/dream3r/scripts/verify_release_candidate.py` | Checks local artifacts, metrics, docs, stable-core policy, and the controlled v1.2 core-unfreeze exception. |
| Proposal caches | server/local `runs/stage6_fusion/...` | Fixed evidence source for the selected gate. |

## Frozen Core Boundary

The official release package does not require edits to:

```text
code/dream3r/model.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/modules.py
code/dream3r/contracts.py
code/dream3r/config.py
```

Those files remain architecture substrate, not the selected RC metric path.

## Metrics And Controls

Selected result:

```text
correct-state KITTI / ETH3D: 0.1448 / 0.1475
shuffle-state KITTI / ETH3D: 0.1521 / 0.2467
```

The result is valid because:

1. correct-state beats the best single proposal expert in the selected gate;
2. correct-state beats shuffled-state on both domains;
3. the StatePrior branch is frozen rather than jointly collapsed;
4. residual refinement is bounded by local proposal disagreement;
5. fallback/stub contamination is excluded from admitted model-code gates.

## Official API Contract

```python
from dream3r.release_candidate import build_dream3r_release_candidate

model = build_dream3r_release_candidate(checkpoint_path=None, d_memory=32)
metadata = model.release_metadata()
```

Required input tensors:

```text
proposal_pointmaps:    [B, E, N, P, 3]
proposal_confidences:  [B, E, N, P, 1]
memory_context:        [B, D_mem]
conflict_score:        [B, 1]
```

Required output tensors:

```text
final_pointmap
base_pointmap
residual_delta
final_confidence
expert_weights
state_prior_weights
uncertainty
```

## Module Status

| Module | v1.0-rc1 Status | Promotion Boundary |
| --- | --- | --- |
| `StatePriorHead` | official support module | accepted diagnostic and frozen prior |
| `ProposalSetDecoder` | official metric path | frozen-prior + bounded residual only |
| `NativeStudentDecoder` | implemented side lane | not official; flat after objective gates |
| `ImageStateStudentDecoder` | implemented side lane | not official; negative gate |
| `VGGT-Omega` | admitted teacher lane | not official; domain-conditional future work |
| `Qwen3-VL` semantics | diagnostic lane | not official; no geometry claim |
| v0.4 contracts/orchestrator/repair | substrate | not the selected metric head |

## Forward Compatibility

The next official version can replace v1.0-rc1 only if it satisfies all of:

```text
1. beats 0.1448 / 0.1475 on the same RC gate or a stricter declared gate;
2. beats no-state and shuffle-state controls;
3. reports fallback_contamination_count == 0 where backend admission is involved;
4. preserves the official non-claims until new evidence removes them;
5. updates release/OFFICIAL_VERSION.md and release/ARTIFACTS.json.
```
