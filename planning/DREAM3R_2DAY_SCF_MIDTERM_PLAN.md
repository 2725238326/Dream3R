# DREAM3R 2-Day SCF Midterm Convergence Plan

plan_id: DREAM3R-2DAY-SCF-MIDTERM
date: 2026-05-29
window: 2026-05-29 (Day 1) -> 2026-05-30 (Day 2)
status: active; planning + first safe step
decision_anchor: DEC-20260527-009 (state-conditioned reconstruction pivot)
spec_anchor: SPEC-20260527-001 (A9 real-backend guardrail / A10 multi-expert proposal bank / A11 long-sequence state objective)
handoff_anchor: handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md
read_only_evidence: DEC-20260526-007 (routing), DEC-20260527-008 (reroute NEGATIVE), MIDTERM-20260530 §3 (structural finding)

> This plan converges Dream3R into one honest midterm package around
> **Dream3R-SCF (State-Conditioned Fusion)**. It does not re-open broad
> architecture exploration. It is concrete enough that an executor can
> start without re-arguing the architecture.

---

## 1. Goal statement

**Model target (one sentence):**

```text
Dream3R-v0.6 (SCF) is a state-conditioned multi-expert fusion model: it
fuses fast3r / mast3r / spann3r proposal pointmaps under persistent
Memory/Anchor/NSA state and Critic/geometric reliability into one final
pointmap, instead of hard-selecting a single expert.
```

**Non-goals (explicit):**

- No new broad architecture exploration (no VGGT, GaussianHead, tttLRM,
  Test3R off-path, Critic reroute, or new router seed sweeps as the main
  path). Those are future work; admit them only as a baseline or input
  signal.
- No SOTA claim. No cross-dataset generalization claim.
- No "router-as-mainline" claim. Composer is demoted to proposal prior /
  regime probe / diagnostic baseline (DEC-009).
- No new checkpoint download, no long (>4h) training, no KYKT frontend,
  no v0.3/v0.5 core edits — unless a separate DEC / user approval is
  explicitly obtained.

**Honest framing the package must keep:** the routing-side control plane
is validated (DEC-007) but bounded; reroute alone is not enough
(DEC-008); the final pointmap currently equals one expert's standalone
output (MIDTERM §3). SCF is the smallest architecture that makes Memory /
reliability state *load-bearing for geometry*.

---

## 2. Model definition

### 2.1 Inputs (per window)

```text
proposal_pointmaps     [B, E, N, P, 3]   E = {fast3r, mast3r, spann3r}
proposal_confidences   [B, E, N, P, 1]
memory_context         [B, D_mem]        MemoryOutput.fused_context (D_mem=128 @ small_real)
anchor_nsa_summary     [B, D_a]          optional: bank_occupancy + nsa_branch_weights + drift proxy
conflict_score         [B, 1]            CriticDecision.conflict_score
geometry_features      [B, E] or [B,E,E] optional: sampson / depth-inconsistency per proposal
composer_prior         [B, E]            ComposerDecision routing_logits / cost_adjusted_scores
```

### 2.2 Outputs

```text
final_pointmap         [B, N, P, 3]
final_confidence       [B, N, P, 1]
expert_weights         [B, E, N, P] or [B, E]   (softmax over E)
correction_mask        [B, N, P, 1]              residual gate magnitude
```

### 2.3 Minimal architecture (proposal bank -> state encoder -> fusion head -> residual/correction)

```text
1. state encoder:   s = MLP(concat[ proj(memory_context),
                                     sigmoid(conflict_score),
                                     anchor_nsa_summary,
                                     composer_prior ])          [B, H]
2. weight head:     logits_e = WeightHead(s, proposal_confidence_e,
                                           geometry_features_e)  [B, E, (N,P)]
                    w = softmax(logits over E)
3. fusion:          fused = sum_e w_e * proposal_pointmap_e      [B, N, P, 3]
4. residual head:   delta = MLP(fused, s)                        [B, N, P, 3]
                    refined = fused + tanh(conflict_score) * delta
5. confidence:      final_confidence = sum_e w_e * proposal_confidence_e
```

**Identity-at-init discipline** (reuse `fusion_head.py` pattern): zero-init
the residual head's final layer + tanh(conflict) gate so the head starts
at pure fusion (and at E=1, pure pass-through), and never degrades a strong
expert before gradient signal lands.

**L1 special case:** when E=1 and weights are fixed to 1, the SCF head
reduces exactly to the existing `Stage6FusionHead` (single-expert
residual). So L1 reuses current code; L2 generalizes it to E=3.

---

## 3. Required baselines

All baselines are computable from one all-expert proposal cache + GT, with
the same scale-aligned `abs_rel` metric used by `build_oracle_expert_labels.py`.

| ID | Baseline | How computed |
| --- | --- | --- |
| B0 | always_fast3r | proposal[fast3r] vs GT |
| B1 | always_mast3r | proposal[mast3r] vs GT |
| B2 | always_spann3r | proposal[spann3r] vs GT |
| B3 | hard router pick-one | router_joint_v3_dense pick -> proposal[pick] (DEC-007 canonical router) |
| B4 | oracle best per window | min_e abs_rel(proposal_e) — upper bound |
| Ours | Dream3R-v0.6 SCF | fused/refined head output |

B3 must use the existing canonical router checkpoint
`/hdd3/kykt26/checkpoints/router_joint_v3_dense/latest.pt`, not the
random-init router inside `build_dream3r("small_real")`.

---

## 4. Required ablations

| Ablation | Removes | Tests |
| --- | --- | --- |
| Ours − state | zero `memory_context` + `anchor_nsa_summary` | does persistent state condition depth? (A11) |
| Ours − reliability | zero `conflict_score` + `geometry_features` | does Critic/geometry reliability help? |
| Ours − residual (weights only) | drop step 4 (`delta`) | is soft fusion alone enough, or is correction needed? |
| Single-expert residual (L1) vs multi-expert fusion (L2) | E=1 vs E=3 | does proposal-bank fusion beat best single + state-correction? |

Each ablation shares the held-out split (seeded) so deltas are comparable.

---

## 5. Metrics

```text
abs_rel                        scale-aligned, _pointmap_abs_rel (oracle-consistent)
rel_imp vs best single         (best_single - ours) / best_single
oracle gap to B4               (ours - B4) / B4         (how much headroom remains)
temporal_consistency_proxy     cross-window pointmap stability on overlapping frames
scale_drift_proxy              per-window median-depth drift across a sequence
anchor_stability               anchor reuse / survival if exposed by MemoryOutput (optional)
```

`abs_rel` is the sanity metric. The Dream3R state claim is judged on
`temporal_consistency_proxy` + `scale_drift_proxy` (A11) — a head that
only ties on abs_rel but improves coherence is still a positive state
signal.

---

## 6. Two-day convergence schedule

### Day 1 AM — lock story + verify patch surface  (DONE this session)

- Re-read DEC-009 / SPEC-001 / MIDTERM §3 — midterm story locked:
  routing-side validated, reconstruction-plane missing, SCF is the fix.
- Verified the exact Stage 6 real-backend patch surface (see §7.1). The
  handoff Open Question #1 (does `registry.get(name)` return the same
  instance `dispatch()` uses?) is **resolved: YES** — both go through
  `ExpertRegistry.get()`, which lazily instantiates and caches in
  `_adapters`, and `orchestrator._dispatch_expert` reads from the same
  `self.model.composer.registry`.

### Day 1 PM — L0 guardrail patch (non-core) + smallest real cache

- Patch `train_fusion_head.build_cache` to load real adapters via the
  model registry and assert `is_loaded`, and to record per-entry
  `backend_status` (A9). **Local reversible edit — done in this session.**
- Extend cache to an **all-expert proposal bank** (A10): store fast3r +
  mast3r + spann3r pointmaps/confidences per window (new builder or a
  `--all-experts` mode), plus memory/anchor/NSA/critic/composer features.
- scp patched scripts to server; run `smoke_stage6_one_window` to confirm
  `backend == real`; rebuild smallest real-backend cache (KITTI subset +
  ETH3D). **Server actions are user-gated — command sketches in §10.**
- Fallback: if all-expert proposal extraction is more than a script-level
  change, ship L0 + L1 only and document the proposal-bank as Day-2 task.

### Day 2 AM — smallest honest comparison table

- Train SCF head + ablations on the cache (cache-based training is fast,
  ~minutes per seed). Produce the comparison table B0/B1/B2/B3/B4/Ours +
  ablations on a seeded held-out split.
- Use explicit `not run` cells where compute is missing. No fabricated
  numbers (CLAUDE.md rule 4 / RESEARCH_CODE_DISCIPLINE honesty override).

### Day 2 PM — finalize midterm package

- Write `decisions/DEC-20260530-011-scf-midterm.md` (honest verdict).
- Write `cycles/CYCLE-20260530-scf-midterm.md` (phase-by-phase).
- Update `mainwork.md` §5 (Stage 6 addendum) + `mainwork/midterm/MIDTERM-20260530.md`
  §4.4 (real-backend numbers) + §5 (roadmap from outcome).
- End with the exact next executor task.

---

## 7. File / task map

### 7.1 Verified patch surface (real-backend guardrail, A9 / L0)

Target: `code/dream3r/scripts/train_fusion_head.py` → `build_cache()`,
lines ~115-117:

```python
model = build_dream3r(preset)        # registers adapter CLASSES only
model.eval()
pipeline = build_v04_pipeline(model, max_repair_attempts=1).to(device)
```

Verified facts that make the guardrail correct and surgical:

- `build_dream3r("small_real")` (`model.py:151-155`) builds
  `ExpertRegistry().register_all_defaults()` (registers 8 classes) and
  calls `composer.load_from_registry()` — which only copies the capability
  matrix + latency vector (`modules.py:1352-1359`). **It never calls
  `adapter.load_checkpoint()`** → root cause of the fallback-stub baseline.
- `ExpertRegistry.get(name)` (`composer_experts/__init__.py:35-38`) lazily
  instantiates and **caches** the adapter in `self._adapters[name]`.
- `ComposerRouter.dispatch` (`modules.py:1422-1442`) and
  `orchestrator._dispatch_expert` (`orchestrator.py:348-414`) both retrieve
  the adapter via `self.model.composer.registry.get(sorted(names)[idx])` →
  the **same cached instance**. So pre-loading via
  `model.composer.registry.get(name).load_checkpoint()` before the forward
  loop guarantees dispatch returns a real backend.
- Real-expert names + no-arg `load_checkpoint`: `fast3r`, `mast3r`,
  `spann3r` (default server checkpoint paths baked in; verified
  `mast3r.load_checkpoint(path=None)` / `spann3r.load_checkpoint(path=None)`).
- Reference pattern: `build_oracle_expert_labels.py:91-99` `_load_adapter`
  (`load_checkpoint()` then `assert is_loaded`).
- Per-entry backend status to record:
  `out.expert.backend_status["is_loaded"]` and `["backend"]`
  (`DispatchedExpertOutput`, `contracts.py:151-164`;
  populated in `orchestrator.py:397-414`).

### 7.2 Files to ADD (non-core; allowed)

| File | Role |
| --- | --- |
| `code/dream3r/scf_head.py` | Multi-expert SCF fusion head (E-generalization of `Stage6FusionHead`) |
| `code/dream3r/scripts/v04_pipeline_scf.py` | `V04PipelineWithFusion`-style subclass exposing all-expert proposals (or extend existing subclass) |
| `code/dream3r/scripts/train_scf_head.py` | All-expert cache builder + SCF trainer + B0-B4 + ablation eval (may extend `train_fusion_head.py`) |

New files are NOT core. The core off-limits list is exactly: `model.py`,
`anchor_bank.py`, `nsa_attention.py`, `bus.py`, `orchestrator.py`,
`repair.py`, `modules.py`, `contracts.py`, `config.py`.

### 7.3 Read-only references (do not edit)

```text
model.py (build_dream3r, presets)        orchestrator.py (_dispatch_expert, _assemble_output)
modules.py (ComposerRouter.dispatch)     contracts.py (DispatchedExpertOutput / MemoryOutput / CriticDecision)
fusion_head.py (Stage6FusionHead)        scripts/v04_pipeline_with_fusion.py
scripts/build_oracle_expert_labels.py (_load_adapter, _pointmap_abs_rel, _resize_images)
```

### 7.4 Core-file edits — BLOCKED unless DEC grants exemption

Any change to the §7.2 core list requires a separate DEC (e.g. if L4 state
retraining is reached). Not in scope for this 2-day window.

---

## 8. Execution gates

```text
L0 (guardrail)  MUST pass before any training/eval result is recorded:
                real adapters loaded + asserted is_loaded; cache stores
                per-entry backend_status; fallback-stub entries fail fast.
L1 (single)     may run only after L0 cache backend_status == real.
L2 (all-expert) cache MUST store all 3 proposals, not only selected_expert.
gate-server     any server run (cache build, training) is user-approval-
                required in this conversation. Command sketches only.
gate-download   any new checkpoint download / long training -> user approval.
gate-core       any core-file edit -> separate DEC.
```

---

## 9. Acceptance criteria

**Minimum useful result:**

```text
SCF (Ours) beats B3 (hard router) OR best single (min of B0/B1/B2) on at
least one held-out domain (KITTI or ETH3D), without worsening the
temporal-consistency / scale-drift proxy.
```

**Honest null result (equally acceptable as a midterm closure):**

```text
If SCF does not beat baselines, the package must still state a verdict:
  - state-not-informative: state inputs carry no depth-correction signal
    (Ours - state ablation ~ Ours), OR
  - head-too-weak: fusion/correction capacity is insufficient (oracle gap
    to B4 stays large while ablations are flat).
Either verdict feeds the post-midterm roadmap (L3 coherence objective /
L4 state retraining under a new DEC).
```

No result table ships without the L0 real-backend guardrail (§8). A
`not run` cell is acceptable; a fallback-stub number masquerading as a
real baseline is not.

---

## 10. Final handoff — exact first executor task

**First step (this session, local, no approval needed):** patch
`train_fusion_head.build_cache` with the L0 real-backend guardrail +
per-entry backend_status (see §7.1). Done as a local reversible edit.

**Next executor task (server, user-gated):** verify guardrail, then
rebuild the smallest real-backend cache. Draft command sketches (GPU 1,
non-destructive; do NOT run until this conversation approves):

```bash
# 0) sync patched script to server
scp E:\Dream3R\code\dream3r\scripts\train_fusion_head.py \
    BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/scripts/train_fusion_head.py

# 1) smoke one window — expect backend == real, abs_rel ~ 0.14-0.16 (not ~0.9)
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && CUDA_VISIBLE_DEVICES=1 \
    conda run -n dream3r python -m dream3r.scripts.smoke_stage6_one_window"

# 2) rebuild KITTI real-backend cache (guardrail asserts is_loaded)
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && CUDA_VISIBLE_DEVICES=1 \
    conda run -n dream3r python -m dream3r.scripts.train_fusion_head build-cache \
    --dataset kitti_long \
    --regime-labels runs/stage3_regime_labels/regime_labels.json \
    --output runs/stage6_fusion/kitti_cache_real.pt"

# 3) verify backend_status distribution in the rebuilt cache
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -c \"
import torch; from collections import Counter
b = torch.load('runs/stage6_fusion/kitti_cache_real.pt', map_location='cpu', weights_only=False)
print('n=', b['n_windows'], 'backends=', Counter(e.get('expert_backend') for e in b['entries']))\""
```

Acceptance of this executor step: rebuilt cache reports
`expert_backend == real` for every measured entry and KITTI baseline
abs_rel in the ~0.14-0.16 range (matching DEC-007), not ~0.9.

---

## Appendix — why this is the right minimal pivot

- DEC-007: routing is learnable but bounded by the expert pool.
- DEC-008: reroute is wired but adds no value at current scale (NEGATIVE).
- MIDTERM §3: `ReconstructionOutput.pointmap = expert.pointmap`; Memory /
  Anchor / NSA / Critic state is emitted but never conditions depth.
- Stage 6 first cache: baseline pathology — `build_dream3r("small_real")`
  never loaded real adapters, so the +60pp head gain was vs a fallback stub.

SCF is the smallest architecture that (a) fixes the truthfulness gap (L0),
(b) makes state load-bearing for geometry (L1/L2), and (c) is evaluable on
the Dream3R-specific claim (coherence, L3) — without re-opening broad
architecture exploration.
