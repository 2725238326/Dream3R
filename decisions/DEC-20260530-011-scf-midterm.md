# DEC-20260530-011 — Dream3R-v0.6 SCF midterm: real-backend guardrail, L1 negative, L2 multi-expert fusion positive

decision_id: DEC-20260530-011
date: 2026-05-30
scope: Dream3R state-conditioned fusion (SCF) midterm result + verdict
decision: Adopt bounded multi-expert soft fusion (SCF / L2) as the validated state-conditioned reconstruction mechanism for the midterm; retire the single-expert residual head (L1) and the unbounded residual variant as negative.
status: accepted (evidence-backed, real backends); core edits still gated

## Context

DEC-009 pivoted Dream3R from hard expert selection to state-conditioned
reconstruction and predicted that a naive residual head might be null or
negative. MIDTERM §4.4 carried a spurious **+60pp** Stage-6 result produced
on a contaminated cache: `build_dream3r("small_real")` registered expert
adapters but never called `adapter.load_checkpoint()`, so the baseline was a
fallback **stub** (abs_rel ~0.93), not a real expert.

This decision records the real-backend rerun and the L0/L1/L2 experimental
ladder of SPEC-20260527-001.

## What was built (non-core only; no v0.3/v0.5 core edits)

- **L0 guardrail** (`code/dream3r/scripts/train_fusion_head.py`
  `ensure_real_backends`, also applied in `smoke_stage6_one_window.py`):
  pre-loads `fast3r/mast3r/spann3r` via the cached `ExpertRegistry.get()`
  instance, asserts `is_loaded`, records per-entry `expert_backend`, and
  fails fast on any fallback stub. Resolves HANDOFF Open Question #1
  (registry caches, so dispatch reuses the pre-loaded adapter).
- **L2 SCF** (new files): `code/dream3r/scf_head.py` (`SCFHead`),
  `code/dream3r/scripts/build_scf_cache.py` (all-expert proposal bank,
  SPEC A10), `code/dream3r/scripts/train_scf_head.py` (train + B0-B4 eval).
  `SCFHead` is a **bounded convex combination** over E expert proposals
  (softmax weights from per-patch confidence + learnable expert prior +
  state), with per-proposal median-depth scale normalisation. Residual
  correction exists behind a flag, default **off**.

## Evidence (server, BUAA-Server, GPU 0-2, real adapters)

- `code-observed` / `server-observed`: caches
  `runs/stage6_fusion/{kitti,eth3d}_cache_real.pt` and
  `scf_{kitti,eth3d}_cache.pt` all carry `expert_backend == real` for every
  entry. Real fast3r baseline abs_rel **0.232** (KITTI) / **0.213** (ETH3D),
  not the ~0.93 stub. Pathology fixed.

### L1 — single-expert residual (`Stage6FusionHead`, seed 7, real fast3r)

| domain | baseline | head | delta |
| --- | --- | --- | --- |
| KITTI (49) | 0.2319 | 0.3412 | **-47.1pp** |
| ETH3D (10) | 0.2387 | 0.4580 | **-91.9pp** |

**Verdict: NEGATIVE.** Unbounded residual correction on a real expert makes
depth worse; held-out abs_rel degrades while train loss barely moves; ETH3D
head transiently explodes (>39 at epoch 140). Confirms SPEC L1 prediction
and HANDOFF Open Question #3: current (random-init) memory/critic state is
not depth-informative through a residual.

### L2 — multi-expert SCF fusion (4 seeds: 7/11/13/17, 80/20 held-out)

Per-expert and oracle baselines (4-seed mean abs_rel):

| domain | B_fast3r | B_mast3r | B_spann3r | best single | **Ours SCF** | B_oracle |
| --- | --- | --- | --- | --- | --- | --- |
| KITTI | 0.229 | 0.154 | 0.161 | 0.154 (mast3r) | **0.139** | 0.137 |
| ETH3D | 0.245 | 0.247 | 0.166 | 0.166 (spann3r) | **0.163** | 0.161 |

Headline (rel_imp vs best single / oracle gap), mean +/- sample std:

| domain | rel_imp vs best single | per-seed | oracle gap |
| --- | --- | --- | --- |
| KITTI (49) | **+9.8% +/- 2.7%** | +7.87 / +7.92 / +9.72 / +13.66 (4/4 pos) | +1.6% |
| ETH3D (10) | **+2.4% +/- 3.0%** | +6.0 / -1.44 / +2.48 / +2.71 (3/4 pos) | +1.1% |

**Verdict: POSITIVE.** SCF beats the best single expert on both domains
(KITTI robustly across all 4 seeds; ETH3D marginally, 3/4 seeds) and tracks
the per-window oracle almost exactly (gap ~1-2%). The bounded convex fusion
trains stably (no divergence), unlike the L1/residual heads. This satisfies
the plan's "minimum useful result": SCF beats best single on >= 1 held-out
domain.

### Ablations (seed 7; no-state also at seeds 11/13/17)

| variant | KITTI rel_imp | ETH3D rel_imp |
| --- | --- | --- |
| **Ours SCF (fusion + state)** | +7.87% | +6.0% |
| Ours - state (fusion only) | +3.73% | **-8.53%** |
| Ours + residual | diverges (ETH3D -74% @ ep1) | diverges |

**State is load-bearing**: removing `memory.fused_context` roughly halves
the KITTI gain and flips ETH3D negative (fusion-only cannot beat best
single on ETH3D). Adding the residual reintroduces the L1 divergence,
confirming convex fusion (bounded) is the correct design.

## Honesty / limitations

- The "state" here is `memory.fused_context` from a **random-init**
  SpatialMemory. The ablation shows it carries window-discriminative signal
  (a fixed input-dependent embedding) that improves fusion, but this is NOT
  evidence that a *trained* memory mechanism is what helps — that is the L4
  question. The honest claim is "state-conditioning helps the fusion", not
  "the trained memory is validated".
- ETH3D held-out set is tiny (n=10): the +2.4% is noisy and seed-11 is
  slightly negative. KITTI (n=49) is the reliable domain claim.
- Splits are 80/20 per seed (not leave-one-scene-out). The oracle gap, not
  rel_imp, is the most stable statistic and is consistently ~1-2%.
- Single window length (4 frames), DINOv3 features, 224px. No temporal /
  scale-drift metric yet (deferred to L3/L4).

## Decision

1. SCF (bounded multi-expert convex fusion conditioned on confidence +
   state) is the validated midterm mechanism for state-conditioned
   reconstruction. L1 single-expert residual and the residual variant are
   retired as negative.
2. MIDTERM §4.4's +60pp is formally retracted; §4.5/§4.6 carry the real
   numbers above.

## Next Action

1. (gated, L4) Retrain memory/critic with a depth-aligned objective and
   re-run the `--no-state` ablation to test whether *trained* state beats
   the random-init embedding.
2. (optional) Add per-patch oracle and a temporal-consistency metric to the
   SCF eval so the claim is not abs_rel-only.
3. Keep Composer as the cost-aware proposal scheduler feeding the bank.
