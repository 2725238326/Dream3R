# SPINE_MEMORY: Executive Memory / State Governance

Last updated: 2026-05-05 (cycle 013 refresh: tttLRM SRC-2026-011 added to Advanced Reading as long-context state-update successor to TTT3R; Mem3R SRC-2026-003 already in Required Reading, re-confirmed)

Linked spec: `specs/SPEC-20260503-002-executive-memory.md`

Linked finalist: Executive Memory / State Governance (working title GEM-3R)

## One-Line Definition

A 3R controller that selects on each window from a small policy bank over A1 (state update) / A2 (memory write) / A3 (anchor + cache + context budget) sub-actions, conditioned on a geometry-grounded evidence vector rather than fixed windows or confidence-only thresholds.

Important: per DEC-20260504-002, Memory is not the thesis spine. It is borrowable as one component. The "GEM-3R" working title remains historical; do not promote it to thesis status without a separate user decision.

## Required Reading

These are the papers any Memory case-card author must read before adding an `anchor_set` or `policy_log` line.

### SRC-2025-002 CUT3R (paper-proven)

What this paper actually claims: persistent latent state for continuous 3D perception; the state is recurrent and is updated as new frames arrive.

What people often misread it as: an external memory store. CUT3R's state is a compressed recurrent state, not a writable spatial store. External pointer memory is Point3R / Mem3R; do not conflate.

### SRC-2026-001 STream3R (paper-proven)

What this paper actually claims: causal transformer + stream session for 3R; long-sequence streaming with explicit session boundaries.

What people often misread it as: a memory paper. STream3R is primarily a streaming-architecture paper; its memory contribution is session-bounded state, not unbounded scene memory.

### SRC-2025-012 LONG3R (paper-proven)

What this paper actually claims: 3D spatio-temporal memory with gating for long sequences; memory pruning is part of the architecture.

What people often misread it as: an executive controller. LONG3R hard-wires gating; Dream Memory controller selects gating policy. The pattern is similar; the controller layer is Dream's.

### SRC-2026-002 LoGeR (paper-proven)

What this paper actually claims: chunked long-context reconstruction with TTT-style global memory + sliding-window local memory; hybrid memory.

What people often misread it as: equivalent to Mem3R. LoGeR is hybrid (local + global); Mem3R decouples camera from mapping. The hybrid axis and the decoupling axis are different.

### SRC-2026-003 Mem3R (paper-proven)

What this paper actually claims: hybrid memory decoupling camera tracking from geometric mapping; the memory is structured as a KV cache for tracking + a separate map memory.

What people often misread it as: equivalent to OVGGT (anchor cache) or Point3R (external pointer). Mem3R memory != OVGGT memory != Point3R memory. See `CRITICAL_NOTES.md`.

### SRC-2026-007 OVGGT (paper-proven)

What this paper actually claims: constant-budget cache compression and dynamic anchor protection on streaming 3R.

What people often misread it as: a generic "memory paper". OVGGT is specifically anchor-cache governance under fixed budget. Dream Memory is closest to OVGGT in spirit; the explicit comparator pressure is highest here.

### SRC-2026-004 PAS3R (paper-proven)

What this paper actually claims: pose-adaptive streaming state update; the update gain depends on pose novelty.

What people often misread it as: a Mamba-3R variant. PAS3R uses pose-adaptive logic; Mamba-3R as an architecture story is not what PAS3R claims.

### SRC-2026-005 FILT3R (paper-proven)

What this paper actually claims: Kalman-style latent filtering for streaming 3R; explicit uncertainty-weighted update.

What people often misread it as: Bayesian SLAM. FILT3R is Kalman over the latent state, not over a SLAM graph; the update target is different.

### SRC-2025-003 Point3R (paper-proven)

What this paper actually claims: explicit spatial pointer memory; geometry-indexed external entries.

What people often misread it as: equivalent to Mem3R. Point3R is *external pointer*; Mem3R is hybrid (KV cache + map). See `CRITICAL_NOTES.md`.

## Advanced Reading

### SRC-2026-006 LongStream (paper-proven)

Gauge-decoupled streaming visual geometry with cache refresh. Useful when the case card asks about cache refresh policy specifically.

### SRC-2026-011 tttLRM (paper-proven)

Test-time training for long-context autoregressive 3D reconstruction. What it actually claims: TTT applied at the *long-context* scale, with a state-update rule that targets long-sequence regression errors rather than per-pair residuals.

What people often misread it as: an upgrade of TTT3R-the-same. The compute scope is different: TTT3R (SRC-2025-004) updates CUT3R's recurrent state on hard *pairs*; tttLRM updates a long-context reconstructor's state on *sequence-level* drift. In SPEC-20260503-002 terms, tttLRM is a candidate for A1 full_update under long-sequence regimes; the action choice vs PAS3R / FILT3R is an explicit comparator question, not a given.

Cite under A1 long-sequence regime comparator, not as a replacement for TTT3R / Test3R in the Critic pipeline.

### Sparse / linear attention background (SRC-2024-006 Mamba-2, etc.)

Architecture-transfer mechanisms. Useful for the related-work section when the paper cites architecture pressure beyond 3R proper. Do not cite as direct comparators.

## Skip With Reason

- 4DGS variants: out of scope; Memory does not own asset generation.
- generic LLM "memory" work (e.g. Infini-attention papers without 3R framing): cite at most once as architecture-transfer background; do not re-derive Memory action set from them.
- POMATO and D2USt3R: belong in SPINE_PERMANENCE; they are dynamic-pointmap papers, not memory papers.

## Cross-Paper Disagreement

- **OVGGT (anchor cache) vs Mem3R (KV cache + map) vs Point3R (external pointer)**: three different memory primitives, often grouped together. Dream Memory does not redefine the store; it defines the policy over an assumed store contract.
- **PAS3R vs FILT3R on update gain**: PAS3R uses pose-adaptive gain; FILT3R uses Kalman gain. Both are valid update policies; Dream Memory A1 selects between them.
- **CUT3R's persistent state vs STream3R's session state**: persistent across the entire video vs session-bounded. The case card author should be explicit about which scope the comparator policy assumes.

## Interface To SPEC-20260503-002

- Memory's A1/A2/A3 sub-action vocabulary maps directly to the comparators above: A1 contains {full_update from CUT3R, pose_adaptive_update from PAS3R, kalman_update from FILT3R, skip_update, reset_state}. A2 maps to {write/merge/ignore/defer} over a Mem3R / Point3R-style store. A3 maps to {protect anchor / evict cache / request global context} OVGGT-style.
- The novelty gap is the *controller selecting between sub-actions*, not the sub-actions themselves. Cycle 009 case cards must show the controller's `policy_log` exhibits more than one sub-action across A1/A2/A3 to defend novelty.
- P2 (anchor retention) anchors against OVGGT.
- P3 (memory growth and usefulness) anchors against Mem3R / Point3R.
- Cross-spec reads (per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`): Memory reads Critic's `conflict_score` for A1 skip_update gating, Permanence's `dynamic_ratio` for A2 ignore, and honors Permanence's `suppress_static_write(r)` per CR-2.

## Evidence Labels Summary

- CUT3R, STream3R, LONG3R, LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, Point3R, LongStream, tttLRM: paper-proven for their published memory / state-update claims.
- Dream policy bank (selecting among the above on evidence vector): inferred.
- theta_write, theta_context, anchor_budget thresholds: inferred.
