# SPEC-20260530-001 — Dream3R-ver2.0 state-conditioned fusion architecture

status: accepted for midterm prototype; evidence-backed on real adapters
date: 2026-05-30
supersedes: SPEC-20260527-001 L0-L2 as the current executable architecture closure
decision_refs: DEC-20260527-009, DEC-20260530-011

## One-sentence definition

Dream3R-ver2.0 is a **state-conditioned multi-expert reconstruction system**:
it builds a real-backend proposal bank from Fast3R / MASt3R / Spann3R and
predicts a bounded convex fusion of their pointmaps using expert confidence,
persistent Dream3R state, and conflict/reliability signals.

This is not a hard expert selector. Composer remains useful as a proposal
prior, regime probe, and cost-aware scheduler, but the final reconstruction is
produced by fusion over real expert proposals.

## Built surface

All ver2.0 code is additive and outside the frozen v0.3/v0.5 core.

| Layer | File | Role |
| --- | --- | --- |
| L0 real-backend guardrail | `code/dream3r/scripts/train_fusion_head.py` | `ensure_real_backends()` loads and asserts real Fast3R / MASt3R / Spann3R adapters before cache building |
| L0 smoke | `code/dream3r/scripts/smoke_stage6_one_window.py` | Confirms the dispatched expert has `backend=real` and the head is identity at init |
| L2 model | `code/dream3r/scf_head.py` | `SCFHead`: softmax weights over all expert proposals; residual off by default |
| L2 cache | `code/dream3r/scripts/build_scf_cache.py` | Stores all expert pointmaps/confidences plus memory context, conflict score, composer prior, GT, and backend flags |
| L2 trainer/eval | `code/dream3r/scripts/train_scf_head.py` | Trains SCF and reports per-expert baselines, oracle, ours, rel_imp, and oracle gap |

Frozen core files remain untouched unless a future DEC grants an exemption:
`model.py`, `anchor_bank.py`, `nsa_attention.py`, `bus.py`,
`orchestrator.py`, `repair.py`, `modules.py`, `contracts.py`, `config.py`.

## Model contract

Inputs per window:

```text
images
+ Fast3R pointmap/confidence
+ MASt3R pointmap/confidence
+ Spann3R pointmap/confidence
+ memory.fused_context
+ critic.conflict_score
+ optional composer prior
-> SCFHead
```

Outputs:

```text
final_pointmap
final_confidence
expert_weights
correction_mask
```

The accepted midterm configuration is **convex fusion only**:

```text
proposal_pointmaps -> per-proposal median-depth normalization
confidence + memory_context + conflict_score + expert_id -> softmax weights
weighted sum over expert proposals -> final pointmap
```

Residual correction remains present behind a flag for future retrained-state
experiments, but it is not part of the accepted ver2.0 midterm model because
the real-backend L1 rerun and residual ablation both diverged.

## Evidence summary

All headline numbers below are from real adapters, not fallback stubs.

### L0 guardrail

The original Stage 6 cache was contaminated: `build_dream3r("small_real")`
registered adapters but did not load checkpoints, producing fallback-stub
baselines around `abs_rel ~= 0.93`. The ver2.0 guardrail loads adapters,
asserts `is_loaded`, and records backend status. Real fast3r baselines are
approximately `0.232` on KITTI and `0.213` on ETH3D.

### L1 negative

Single-expert residual correction on real fast3r is rejected:

| domain | baseline | head | verdict |
| --- | --- | --- | --- |
| KITTI | 0.2319 | 0.3412 | -47.1pp, worse |
| ETH3D | 0.2387 | 0.4580 | -91.9pp, worse |

This establishes that unbounded residual correction is unsafe with the
current random-init state.

### L2 positive

SCF 4-seed held-out result:

| domain | best single | Ours SCF | oracle | rel_imp vs best single | oracle gap |
| --- | --- | --- | --- | --- | --- |
| KITTI | 0.154 (MASt3R) | **0.139** | 0.137 | **+9.8% +/- 2.7%** | +1.6% |
| ETH3D | 0.166 (Spann3R) | **0.163** | 0.161 | **+2.4% +/- 3.0%** | +1.1% |

KITTI is the robust claim: 4/4 seeds improve over best single. ETH3D is a
marginal positive: 3/4 seeds improve, held-out n=10, and the result should be
reported as promising but noisy.

### State ablation

Seed 7:

| variant | KITTI rel_imp | ETH3D rel_imp |
| --- | --- | --- |
| SCF + state | +7.87% | +6.0% |
| SCF - state | +3.73% | -8.53% |
| SCF + residual | diverges | diverges |

The honest interpretation is narrow: `memory.fused_context` carries useful
window-discriminative conditioning signal for fusion. It does not prove that
a trained memory mechanism is already validated.

## Accepted claims

Dream3R-ver2.0 can claim:

- real-backend baselines are guarded against fallback contamination;
- hard expert selection is no longer the main architecture;
- bounded multi-expert state-conditioned fusion is the current usable model;
- SCF beats the best single real expert on KITTI and is close to oracle on
  KITTI/ETH3D under the current held-out split;
- state-conditioning improves SCF relative to fusion-only in the seed-7
  ablation.

Dream3R-ver2.0 must not claim:

- SOTA reconstruction;
- trained Memory / AnchorBank / NSA quality;
- cross-scene or leave-one-scene-out generalization;
- temporal stability or scale-drift improvement;
- that residual correction is safe.

## Ver2.0 closure standard

The architecture is considered complete for the 2026-05-30 midterm if these
artifacts are present and mutually consistent:

1. `DEC-20260530-011` records L0/L1/L2 evidence and limitations.
2. This spec defines the ver2.0 model contract and accepted claims.
3. `MIDTERM-20260530.md` reports the fallback pathology, real-backend L1
   negative, L2 SCF positive, and next-step limitations honestly.
4. The next-agent prompt starts from SCF/ver2.0 and does not reopen broad
   architecture exploration.

## Next version

Dream3R-ver2.1 should test whether the state itself can become genuinely
depth-informative:

1. retrain Memory/Critic with a depth/coherence-aligned objective;
2. rerun `--no-state` and trained-state ablations;
3. add temporal consistency and scale-drift metrics;
4. add per-patch oracle analysis;
5. optionally use Composer as a cost-aware proposal scheduler when all expert
   proposals are too expensive to run.
