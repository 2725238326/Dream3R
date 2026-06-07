# Dream3R Clean Architecture Map - 2026-06-08

## Purpose

This note separates the current Dream3R codebase into clear lanes so future
work does not confuse release code, research scaffolds, diagnostic tools, and
negative experiment branches.

The current mess is mostly organizational, not absence of implementation:

1. The usable release path exists.
2. Several proposal-free research paths exist but are not promotable.
3. Qwen/VGGT/Foundation3R results are documented, but their roles are mixed in
   old summaries.
4. Frozen v0.4 core files still exist as substrate and should not be treated as
   the current release model.

## One-Sentence Current Model

Dream3R is currently a state-conditioned proposal-fusion 3R model with a
domain-conditional v1.1 wrapper: KITTI uses the v1.0 bounded StatePrior proposal
decoder, and ETH3D uses the VGGT-Omega-expanded SCF branch.

Current official entrypoint:

```python
from dream3r.release_v11 import build_dream3r_v11_release
```

Current stable fallback:

```python
from dream3r.release_candidate import build_dream3r_release_candidate
```

## Lane 1 - Usable Release

This is the only branch that should be shown as the working model today.

| Component | File | Role | Status |
| --- | --- | --- | --- |
| v1.1 wrapper | `code/dream3r/release_v11.py` | Domain switch: KITTI -> v1.0, ETH3D -> VGGT-Omega SCF | formal official release |
| v1.0 wrapper | `code/dream3r/release_candidate.py` | Stable bounded proposal-fusion fallback | stable fallback |
| State prior | `code/dream3r/state_prior_head.py` | Learned Dream-state prior over proposal experts | active support |
| Proposal decoder | `code/dream3r/proposal_set_decoder.py` | Proposal-bank reconstruction head | active support |
| SCF head | `code/dream3r/scf_head.py` | Convex state-conditioned fusion head | active support |

Current controlled metrics, AbsRel lower is better:

```text
v1.0-rc1: KITTI 0.1448, ETH3D 0.1475
v1.1.0: KITTI 0.1448, ETH3D 0.0570
```

Rule: use this lane for demos, release packaging, and paper-facing baseline
claims. Do not describe it as proposal-free.

## Lane 2 - Proposal-Free Research

This is the independent foundation-model ambition, but it is not solved.

| Component | File | Role | Status |
| --- | --- | --- | --- |
| ProposalFree3R | `code/dream3r/proposal_free_3r_decoder.py` | First image/state -> pointmap scaffold | negative |
| Foundation3R | `code/dream3r/foundation3r_decoder.py` | VGGT feature / dense-teacher proposal-free student | negative gate |
| Dense teacher cache | `code/dream3r/scripts/build_foundation3r_dense_teacher_cache.py` | Builds proposal-free dense targets | data path works |
| Foundation trainer | `code/dream3r/scripts/train_foundation3r.py` | Trains scratch/VGGT-feature student | works, not promotable |

Recent Foundation3R state-modulation gate:

```text
state:         KITTI 0.3222, ETH3D 0.1504
no-state:      KITTI 0.3392, ETH3D 0.1484
shuffle-state: KITTI 0.3500, ETH3D 0.1353
```

Conclusion: KITTI shows state benefit, but ETH3D fails causality because
shuffle-state is best. This lane must not be promoted.

Rule: the next attempt must change target/data/architecture. Do not rerun
small-decoder, scalar-loss, or same-feature sweeps.

## Lane 3 - Teacher / Proposal Bank Infrastructure

These are inputs and teachers, not the final Dream3R claim by themselves.

| Component | File(s) | Role | Status |
| --- | --- | --- | --- |
| Composer experts | `code/dream3r/composer_experts/*.py` | Fast3R/MASt3R/Spann3R/VGGT-style proposal producers | infrastructure |
| VGGT-Omega admission | `code/dream3r/scripts/stage_vggt_omega_admission.py` | Real-backend checkpoint admission | admitted |
| VGGT oracle eval | `code/dream3r/scripts/eval_vggt_omega_oracle_admission.py` | Tests whether VGGT helps proposal bank | ETH3D useful |
| SCF cache builder | `code/dream3r/scripts/build_scf_cache.py` | Creates proposal-bank training/eval caches | infrastructure |

Rule: VGGT-Omega is a strong teacher/proposal branch. It is not the full
Dream3R architecture and not a proof of proposal-free 3R.

## Lane 4 - Diagnostic / Non-Geometry Signals

These may support analysis but should not be part of the headline model.

| Component | File(s) | Role | Status |
| --- | --- | --- | --- |
| Qwen semantic labels | `code/dream3r/scripts/build_vlm_semantic_labels.py` | Offline semantic annotation/cache | diagnostic only |
| Semantic controller tests | `code/dream3r/tests/test_vlm_*.py` | Schema and controller regression | useful tests |
| Critic/router tools | `code/dream3r/scripts/build_critic_*.py` | Critic data experiments | not current release |

Rule: Qwen is not a geometry model and current Qwen gates are negative for
Router/Critic promotion. Keep it as metadata/diagnostic unless a new causal
gate beats geometry-only and shuffle controls.

## Lane 5 - Frozen Substrate

These files are architectural substrate from the v0.4 era. They should not be
edited for quick release or Foundation3R sweeps.

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

Rule: keep frozen unless a new decision explicitly opens core architecture.

## What Is Actually Missing

For a genuinely useful, improved, independent 3R model, Dream3R still lacks:

1. A proposal-free visual representation that can beat teacher/proposal baselines
   on holdout splits.
2. A state-conditioning mechanism that passes correct/no-state/shuffle controls
   across KITTI and ETH3D.
3. Training targets tied to real geometry quality, not only weak teacher mimicry.
4. Larger and cleaner cross-domain training data than the current 50+50 window
   research caches.
5. One clean public API per claim: release proposal-fusion API vs proposal-free
   research API.

## Cleanup Rules For Future Work

Use the following status labels consistently:

```text
release_active      - can be used and described as current Dream3R
stable_fallback     - conservative fallback release identity
research_active     - worth changing and gating
diagnostic_only     - useful for annotation/evidence, not a model claim
negative_closed     - do not rerun unchanged
frozen_substrate    - do not edit without a new decision
```

## Immediate Execution Order

1. Treat `v1.1.0` as the official model package.
2. Keep `v1.0-rc1` as the stable fallback and regression gate.
3. Mark Foundation3R state-modulation as `negative_closed`.
4. Start the next proposal-free round only if it changes at least one of:
   target, data scale, or architecture.
5. Avoid adding new named modules until the proposal-free redesign has a
   concrete gate and deletion/retirement list.

## Paper Narrative Boundary

Current paper-safe framing:

Dream3R introduces a Dream-state-conditioned proposal-fusion framework for 3R.
The released model uses real proposal teachers, learned state priors, bounded
residual refinement, and a domain-conditional VGGT-Omega branch for ETH3D.

Not safe to claim yet:

```text
Dream3R is a fully proposal-free independent 3R foundation model.
Qwen improves geometry.
Foundation3R is promotable.
VGGT-Omega alone is Dream3R.
```
