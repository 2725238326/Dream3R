# EXP-20260505-002: L3 Prerequisites Brief — Memory (Executive Memory)

experiment_id: EXP-20260505-002

name: L3 Prerequisites Brief — Memory (SPEC-20260503-002 Executive Memory)

linked_ru_ids: RU-001, RU-004, RU-010, RU-014, RU-015

status:

```text
brief only; not an L3 authorization; gated per AGENT_MASTER_PROMPT.md section 6
```

approval_required:

```text
yes, before cloning / downloading / running anything listed below. Filing
this brief does NOT constitute authorization; a separate user DEC is
required before any repo clone, checkpoint download, install, or run.
```

## Goal

Inventory the minimum prerequisites for producing L3-measured evidence behind the Memory finalist's claim (policy bank over evidence vector; which update / cache / store rule to select per regime on a streaming workload). "Minimum" means: what must be in place to show that at least two distinct update rules, run on the same streaming workload under the same budget, select differently when routed through the policy bank versus either rule used alone.

## Linked Artifacts

- spec: `specs/SPEC-20260503-002-executive-memory.md`
- contract: `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (consumer of Permanence's `suppress_static_write` signal per CR-2)
- L2 evidence: `cases/CASE-20260504-MEMORY-01.md`, `CASE-20260504-MEMORY-02.md`, `CASE-20260504-MEMORY-03.md`
- storyboard: `storyboards/STORY-20260505-002-memory.md` (draft only)
- parent decision: `decisions/DEC-20260505-003-cycle-013-launch.md`

## Prerequisite Inventory

### (a) Repos + Checkpoints

Primary (required for Memory smoke test — must cover at least two distinct update rules):

```text
CUT3R    : https://github.com/CUT3R/CUT3R
  - role: persistent-state update rule baseline (SRC-2025-002)
  - checkpoint: paper-provided; demo path published

Spann3R  : https://github.com/HengyiWang/spann3r
  - role: spatial-memory global pointmap baseline (SRC-2024-011;
    MEMORY-02 anchor)
  - checkpoint: paper-provided
```

Secondary (stronger ablation once primary loop works; each adds one additional update / cache / store rule):

```text
STream3R  : https://github.com/NIRVANALAN/STream3R   (SRC-2026-001; causal-transformer state)
Point3R   : https://github.com/YkiWu/Point3R         (SRC-2025-003; external pointer)
LONG3R    : paper + project page per SRC-2025-012    (long-sequence gating)
Mem3R     : per SRC-2026-003 project page             (hybrid TTT fast-weight + explicit token memory;
             closer contemporaneous comparator to MEMORY-02's Spann3R framing per cycle-013 source mining)
OVGGT     : per SRC-2026-007 project + code           (constant-budget cache; MEMORY-03 anchor)
PAS3R / FILT3R / LongStream / LoGeR : deferred to second round.
```

Cycle 013 source mining note: Mem3R (SRC-2026-003) is the closest 2026 comparator to MEMORY-02's Spann3R framing. MEMORY-02's existing paper-derived framing is NOT retroactively edited (Surgical Edits rule 3); instead, a SPINE refresh pass in cycle 014+ will fold Mem3R in and the L3 smoke should plan to include Mem3R in the primary round if time permits.

### (b) GPU / Disk / Compile-Time Budget

All numbers inferred from public model size + repo conventions; NOT measured on any local box.

```text
GPU memory (inference-only smoke on streaming workload):
  CUT3R persistent-state inference over a 500-1000 frame clip: ~12-24
    GB VRAM peak (inferred; depends on frame resolution and state
    compression settings)
  Spann3R spatial memory inference over the same clip: similar order
    of magnitude
  Single-GPU smoke target: 24 GB class minimum; 48 GB class preferred
    if streaming both baselines back-to-back in one session
    (inferred, NOT verified)

Disk:
  Per-repo clone: 0.5-2 GB code + 2-8 GB checkpoints each
  Streaming workload data (a 500-1000 frame real scene dataset;
    candidates: ScanNet scene subset, 7-Scenes, CO3D subset, or a
    KYKT-exposed clip if available): 5-50 GB raw + derived features
  4-repo total inc. primary + two secondary: ~30-60 GB
    (inferred; NOT measured)

Compile / env setup time:
  PyTorch + CUDA stack + 2-4 repos (each with its own deps): ~2-4 hours
    first-time on a clean box (streaming 3R repos tend to have more
    conflicting version pins than pair-wise 3R)

Wall-clock for first smoke loop (stream the same clip through CUT3R
and Spann3R under identical budget, collect state footprint + drift
+ latency metrics): ~1-3 hours end-to-end excluding env setup
  (inferred; dominated by per-frame latency)
```

### (c) Expected Smoke-Test Path

```text
1. Fix one streaming clip (500-1000 frames, dynamic + static mix;
   selection criterion: reproducible via a public dataset, not a
   KYKT-internal clip).
2. Define a fixed state budget B (e.g., 2 GB peak, or K cached tokens).
3. Run CUT3R under budget B -> log drift, latency, final reconstruction.
4. Run Spann3R under budget B -> log same.
5. Implement policy-bank stub: a thin selector reading the
   evidence-vector (regime label, state-footprint ratio, pose-change
   rate) per segment; selector routes each segment to the predicted-
   better backbone.
6. Run the clip through the policy bank -> log same.
7. Compare: does the policy bank improve the weighted objective
   (drift - alpha * latency) beyond either backbone alone, under the
   same B?

Minimum single success criterion for smoke (L3 evidence for MEMORY-01
only, NOT full paper claim): exists at least one segmentation where
the policy bank's weighted objective strictly dominates both
baselines, AND the selector's regime-label input matches a human
annotation on that segment.
```

### (d) Minimum Code Change

```text
new file : dream_memory_loop.py  (~200-400 LOC estimated)
  - orchestrates steps 1-7 above
  - implements the policy-bank stub as a regime-typed lookup table
    (hand-specified thresholds, NOT learned; L2-policy-design level)
  - calls CUT3R / Spann3R inference paths as subprocess or editable
    install; records state footprint per step (torch.cuda.memory_stats
    or equivalent)
  - emits a JSONL log: one line per segment (segment_id, regime_label,
    selected_backbone, drift_metric, latency_ms, state_bytes)

new file : evidence_vector_schema.yaml
  - enumerates the evidence-vector fields the selector reads
    (regime_label, budget_pressure, pose_change_rate, prior_route_regret)
  - each field has evidence label `inferred` or `paper-derived`
    pending L3 measurement
```

## Evidence Label Discipline

- Drift metric and latency values produced by this smoke become `measured` evidence, but ONLY for the specific clip, budget, and hardware used.
- Policy-bank selector thresholds remain `L2-policy-design` (hand-specified) even after smoke; learning the selector is out of scope for L3 smoke and would require separate DEC.
- `state_bytes` measured under budget B is a per-run anchor; it does NOT generalize without repeating the smoke on at least two distinct clips.

## Stop Conditions

```text
(a) Any primary checkpoint URL fails -> stop and record; do NOT
    substitute silently.
(b) Streaming workload clip total frames exceed the 1000-frame cap
    without a budget justification -> stop; design was scoped to
    comparable-length runs.
(c) Env setup requires a CUDA version incompatible with the host
    machine's driver -> stop; driver change is out of scope.
(d) Either baseline's wall-clock exceeds 10x the inferred estimate
    on the first 50 frames -> surface as a budget event; do not
    force-complete.
```

## What This Brief Does NOT Authorize

```text
- No clone, no download, no install, no run. Separate per-finalist
  DEC required.
- No retroactive edits to MEMORY-01..03 cards to pre-populate
  measured fields.
- No promotion of STORY-20260505-002 past `draft`.
- No closure of any Memory-related research goal without measurement
  on at least two distinct streaming clips.
- No KYKT runner log access; no KYKT navigation change; no frontend
  implementation.
```
