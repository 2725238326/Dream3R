# EXP-20260505-004: L3 Prerequisites Brief — Composer (3R Composer)

experiment_id: EXP-20260505-004

name: L3 Prerequisites Brief — Composer (SPEC-20260504-001 3R Composer)

linked_ru_ids: RU-002, RU-014, RU-015

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

Inventory the minimum prerequisites for producing L3-measured evidence of `route_regret`, the cost-typed falsification axis defined in `SPEC-20260504-001-3r-composer.md` and pinned in `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (contract-v2 promotion memo `decisions/DEC-20260504-004.md`; alpha = 0.5 initial inferred). "Minimum" means: what must be in place to run at least three 3R backbones on the same multi-regime workload, collect a capability_match matrix (accuracy, latency, cost_normalized) row-wise, and compute route_regret for the Composer's actual routing policy against the best-single-backbone oracle.

G2 status after cycle 012 is `inferred-with-real-inventory-anchor` (COMPOSER-04 provided the KYKT-metadata inventory anchor). G2 closure requires `measured` route_regret; this brief inventories that measurement path.

## Linked Artifacts

- spec: `specs/SPEC-20260504-001-3r-composer.md`
- contract: `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (cost-typed capability_match; route_regret; forward-reference null protocol)
- L2 evidence: `cases/CASE-20260505-COMPOSER-01.md`, `CASE-20260505-COMPOSER-02.md`, `CASE-20260505-COMPOSER-03.md` (v2 promotion), `CASE-20260505-COMPOSER-04.md` (KYKT-metadata-derived)
- storyboard: `storyboards/STORY-20260505-004-composer.md` (draft only)
- parent decision: `decisions/DEC-20260505-003-cycle-013-launch.md`
- contract v2 promotion memo: `decisions/DEC-20260504-004.md`
- cycle-013 source mining note: VGGT (SRC-2026-015) and DUSt3R/MASt3R/VGGT MVS evaluation (SRC-2026-013) surfaced as capability-card coverage gaps; inclusion in L3 smoke is recommended when time permits.

## Prerequisite Inventory

### (a) Repos + Checkpoints

Primary (required for Composer smoke test — minimum three backbones):

```text
DUSt3R    : https://github.com/naver/dust3r           (SRC-2024-001)
  - role: pose-free pairwise pointmap baseline; COMPOSER-01 row anchor
MASt3R    : https://github.com/naver/mast3r            (SRC-2024-002)
  - role: matching + sparse alignment; COMPOSER-01 / 03 row anchor
Fast3R    : https://github.com/facebookresearch/fast3r (SRC-2025-001)
  - role: many-view one-forward regime; COMPOSER-02 row anchor
```

Secondary (stronger coverage + cycle-013 identified gaps):

```text
Spann3R   : https://github.com/HengyiWang/spann3r      (SRC-2024-011;
             spatial-memory regime row)
CUT3R     : https://github.com/CUT3R/CUT3R             (SRC-2025-002;
             streaming regime row)
STream3R  : https://github.com/NIRVANALAN/STream3R    (SRC-2026-001;
             causal-transformer regime row)
MV-DUSt3R+ : https://github.com/facebookresearch/mvdust3r (SRC-2025-005;
             sparse-view multi-frame)
VGGT      : https://github.com/facebookresearch/vggt    (SRC-2026-015;
             cycle-013-mined gap; feed-forward VGT regime row
             NOT currently in COMPOSER-01..04)
MapAnything : arXiv paper SRC-2026-009 (repo URL to verify at clone
             time; universal feed-forward regime row)
```

Evaluation anchor (external sanity check for capability_match values):

```text
DUSt3R / MASt3R / VGGT MVS evaluation (SRC-2026-013): external
empirical evaluation on high-res + multi-camera videos. Use as a
cross-check for accuracy-axis values the smoke measures locally.
```

Dataset / workload design:

```text
Multi-regime workload (minimum 4 regimes, one scene each):
  R1 short causal pair      (2 frames, easy texture)
  R2 many-view static scene (10+ frames, CO3D / Mip-NeRF 360 subset)
  R3 streaming long clip    (500+ frames, per Memory-brief clip)
  R4 dynamic-present clip   (10-30 s, per Permanence-brief clip)

Each regime's cost function: w1*accuracy_error + w2*latency + w3*cost_normalized
with alpha = 0.5 as the initial cost-to-accuracy trade per DEC-20260504-004.
Actual weights are part of the measurement; do NOT pre-pin them.
```

### (b) GPU / Disk / Compile-Time Budget

All numbers inferred from public model size + repo conventions; NOT measured on any local box.

```text
GPU memory (inference-only smoke across 3+ backbones on 4 regimes):
  Each backbone: 8-24 GB VRAM peak depending on regime (dense many-view
    and streaming are heavier)
  One GPU can run the workload sequentially; running in parallel for
    latency measurement requires separate processes + careful VRAM
    accounting.
  Single-GPU smoke target: 24 GB class for 3-backbone sequential
    sweep; 48 GB class or multi-GPU for parallel latency measurement.
    (inferred, NOT verified)

Disk:
  Per-repo clone: 0.5-3 GB code + 2-8 GB checkpoints each
  Primary 3 repos: ~15-30 GB
  Primary + secondary (incl. VGGT + MapAnything): ~40-80 GB
  Workload datasets (CO3D subset + Mip-NeRF 360 subset + one streaming
    clip + one dynamic clip): 30-100 GB raw
  Total disk footprint: ~100-200 GB (inferred; NOT measured)

Compile / env setup time:
  Each 3R repo has its own torch / CUDA pin; shared env for all 3
    primaries is ~2-4 hours first-time (inferred)
  Adding VGGT + MapAnything + Spann3R + CUT3R + STream3R can double
    that (version conflicts; expect some repos in isolated conda envs)

Wall-clock for first smoke loop (sweep 3 backbones across 4 regimes,
collect accuracy + latency + cost per (backbone, regime) cell, compute
route_regret of any published routing policy against best-cell oracle):
~4-8 hours end-to-end excluding env setup, on a single 24 GB GPU
  (inferred; dominated by dense many-view regime)
```

### (c) Expected Smoke-Test Path

```text
1. Build capability_match matrix M[backbone][regime] empty.
2. For each backbone in {DUSt3R, MASt3R, Fast3R} and each regime in
   {R1, R2, R3, R4}:
     run inference; record accuracy_error, latency_ms, cost_normalized.
     fill M[backbone][regime].
3. Oracle: for each regime, pick the backbone with the lowest cost
   function value -> route_oracle[regime].
4. Paper-derived routing policy (from COMPOSER-01..03): pick per regime
   per capability_match as currently encoded -> route_paper[regime].
5. KYKT-metadata-derived routing policy (from COMPOSER-04): pick per
   regime per KYKT inventory anchor -> route_kykt[regime].
6. Compute route_regret_paper = sum over regimes of
     (cost(route_paper, regime) - cost(route_oracle, regime)).
7. Compute route_regret_kykt similarly. Compare.

Minimum single success criterion for smoke (L3 evidence for
COMPOSER-01 only, NOT G2 closure across the full regime taxonomy):
exists at least one regime where route_paper and route_kykt disagree,
AND at least one of them has strictly lower regret than naive
(always-DUSt3R) routing.

G2 full closure (stretch): requires route_regret measured across the
full regime taxonomy from SPEC-20260504-001, not just 4 regimes.
```

### (d) Minimum Code Change

```text
new file : dream_composer_sweep.py  (~300-500 LOC estimated)
  - orchestrates steps 1-7 above
  - wraps each backbone's inference entry point (subprocess or
    editable install)
  - normalizes accuracy metrics across backbones (each publishes
    different primary metric; use spec's cross-spec signal contract
    v2.1 capability_match schema)
  - emits JSONL log: one line per (backbone, regime) cell plus
    aggregate lines for each routing policy's total regret

new file : capability_match_schema.yaml
  - documents the matrix schema actually populated (backbones x
    regimes x {accuracy_error, latency_ms, cost_normalized})
  - reflects v2 cost-typed contract (DEC-20260504-004); no schema
    revision attempted during smoke

new file : route_policies.yaml
  - encodes route_paper and route_kykt as lookup tables hand-serialized
    from COMPOSER-01..04; route_oracle is computed, not encoded
```

## Evidence Label Discipline

- Accuracy / latency / cost_normalized values become `measured` evidence, but ONLY for the specific workload + hardware used.
- route_regret_paper and route_regret_kykt become `measured` relative to the oracle computed on that workload; they do NOT generalize without repeating on at least one other workload.
- The alpha = 0.5 cost-to-accuracy trade remains `inferred` after smoke unless the smoke explicitly ablates alpha and shows stability; ablation is out of scope for first smoke.
- VGGT + MapAnything exclusion from primary smoke is a scoping decision; their addition in a second-round smoke is recommended but does NOT invalidate first-round results (each is a row addition, not a row rewrite, per Discipline rule 3).

## Stop Conditions

```text
(a) Any primary checkpoint URL fails or license changes -> stop; do NOT
    substitute silently.
(b) VRAM exhaustion on a single regime blocks completing that column
    for all 3 primaries -> either drop that regime with an audit note
    OR upgrade hardware request; do NOT silently swap a smaller model
    in.
(c) Workload dataset access is blocked (license, download cap) -> stop;
    re-scope to license-compatible dataset; do NOT use a KYKT-internal
    dataset as substitute (KYKT data access is gated).
(d) Latency measurement noise exceeds the between-backbone signal
    (within-backbone std > between-backbone delta) -> increase
    repetitions; if still noisy, surface as a measurement-method
    failure, not a G2-closure attempt.
```

## What This Brief Does NOT Authorize

```text
- No clone, no download, no install, no run. Separate per-finalist
  DEC required.
- No retroactive edits to COMPOSER-01..04 cards; no retroactive edits
  to the v1 preserved row (Discipline rule 5 / DEC-20260504-004 v1-
  preserved rule in force).
- No promotion of STORY-20260505-004 past `draft`.
- No unilateral revision of alpha = 0.5 or of the cost_normalized
  axis definition (contract v2.1 substance unchanged in cycle 013;
  any revision is a separate DEC).
- No closure of G2 from first-round smoke alone; full G2 closure
  requires full-regime coverage.
- No KYKT runner log access (the other G2 closure path is separately
  gated and out of scope here).
- No frontend implementation; no teacher-demo readiness claim.
```
