# EXP-20260505-003: L3 Prerequisites Brief — Permanence (Dynamic Object Permanence)

experiment_id: EXP-20260505-003

name: L3 Prerequisites Brief — Permanence (SPEC-20260503-003 Dynamic Object Permanence)

linked_ru_ids: RU-013, RU-015

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

Inventory the minimum prerequisites for producing L3-measured evidence behind the Permanence finalist's claim (action-set object permanence: identity persistence across forced occlusion + static-map immunity under dynamic passage; distinct from per-frame motion accuracy). "Minimum" means: what must be in place for a single smoke clip that forces a dynamic object across a static map and measures (i) identity re-association after occlusion, (ii) static-map drift under dynamic passage, on at least one dynamic-aware baseline plus a permanence-augmented variant.

## Linked Artifacts

- spec: `specs/SPEC-20260503-003-dynamic-object-permanence.md`
- contract: `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (publisher of `suppress_static_write` consumed by Memory per CR-2; also relevant to forward-reference null protocol when Memory is not yet running)
- L2 evidence: `cases/CASE-20260504-PERMANENCE-01.md` (CR-2 cross-pair), `CASE-20260504-PERMANENCE-02.md` (re-entry), `CASE-20260504-PERMANENCE-03.md` (G4 closure on synthetic identity-validation clip, cycle 011)
- storyboard: `storyboards/STORY-20260505-003-permanence.md` (draft only)
- parent decision: `decisions/DEC-20260505-003-cycle-013-launch.md`
- name-collision deconfusion pointer: Julian Ost AAAI-2026 driving permanence (SRC-2026-010) handled in `literature/CRITICAL_NOTES.md` at next literature-sync pass; NOT a comparator for this smoke.

## Prerequisite Inventory

### (a) Repos + Checkpoints

Primary (required for Permanence smoke test):

```text
MonST3R   : https://github.com/Junyi42/monst3r
  - role: dynamic-aware pointmap baseline (SRC-2024-003);
    PERMANENCE-01 anchor
  - checkpoint: paper-provided; demo path published

SAM 2     : https://github.com/facebookresearch/sam2 (paper SRC-2024-012;
             repo URL to verify at clone time)
  - role: dynamic mask / segmentation prior; used as input to identity
    re-association step (not as mechanism itself)
  - checkpoint: Meta-provided; multiple sizes available

CoTracker : https://github.com/facebookresearch/co-tracker (SRC-2023-003)
  - role: 2D track provider for identity re-association across
    occlusion; used as input only
```

Secondary (for wider dynamic baseline coverage):

```text
POMATO    : SRC-2025-010 (repo URL to verify; pointmap + temporal motion)
D^2USt3R  : SRC-2025-011 (paper; 4D pointmaps)
Easi3R    : SRC-2025-013 (training-free dynamic adaptation)
RayMap3R  : https://raymap3r.github.io/ (SRC-2026-008; code claimed)
SpatialTracker : https://github.com/henry123-boy/SpaTracker (SRC-2024-013;
                 v2 URL to verify)
```

Dataset / clip candidates:

```text
Hand-curated short clip (10-30 s, 30 fps) with a person walking across
a static scene and briefly fully occluded by a column or doorway;
candidate sources: a self-captured clip (no IRB concerns; minimal
cost), a DAVIS dynamic clip, or a ScanNet sequence with dynamic
annotation. Avoid KYKT-internal clips for L3 smoke (KYKT data access
is gated separately per AGENT_MASTER_PROMPT.md section 6).
```

### (b) GPU / Disk / Compile-Time Budget

All numbers inferred from public model size + repo conventions; NOT measured on any local box.

```text
GPU memory (inference-only smoke on one 10-30 s clip):
  MonST3R inference over 300-900 frames: ~12-20 GB VRAM
    (inferred from MonST3R repo README; NOT verified)
  SAM 2 video segmentation over the same clip: ~8-16 GB
    (inferred from SAM 2 model-size table)
  CoTracker over the same clip: ~4-8 GB
    (inferred)
  Running all three sequentially: 24 GB class GPU is the inferred
    minimum; 48 GB class is safer.

Disk:
  Per-repo clone: 1-3 GB code + 2-15 GB checkpoints each
    (SAM 2 large variant is the heaviest)
  3-repo total: ~20-40 GB (inferred)
  Clip storage + intermediate dumps: 5-20 GB depending on resolution

Compile / env setup time:
  SAM 2 + MonST3R + CoTracker env can conflict on torch / CUDA pins;
  expect ~3-6 hours first-time on a clean box (inferred; more than
  Critic or Memory because of three-way dep conflict risk).

Wall-clock for first smoke loop (clip in, dynamic mask out, identity
tracks out, dynamic-aware pointmap out, identity re-association log
out, static-map drift measurement out): ~2-4 hours end-to-end
  (inferred; dominated by SAM 2 video segmentation on longer clips)
```

### (c) Expected Smoke-Test Path

```text
1. Fix one short clip (10-30 s) with a known occlusion event at a
   known time index t_occ.
2. Run SAM 2 -> per-frame dynamic mask; identify the target object
   track and the occlusion span [t_occ_start, t_occ_end].
3. Run CoTracker -> 2D tracks for the target object pre-occlusion;
   after occlusion, check which tracks re-associate. Record
   identity_consistency = correct_reassociation / total_reassociations.
4. Run MonST3R on the clip with dynamic mask applied -> dynamic
   pointmap D and static pointmap S.
5. Compute static_map_drift = distance between S computed from full
   clip vs. S computed from clip with the dynamic-passage window
   excised; define drift metric per spec SPEC-20260503-003.
6. Implement permanence-signal stub: publish `suppress_static_write`
   during [t_occ_start, t_occ_end] based on SAM 2's mask union.
7. Re-run steps 4-5 with the permanence signal applied; compare drift
   and identity_consistency deltas.

Minimum single success criterion for smoke (L3 evidence for
PERMANENCE-01 only, NOT full paper claim): identity_consistency > 0.7
on at least one re-entry event AND static_map_drift_with_signal <
static_map_drift_without_signal on the same clip.

Threshold anchor: 0.7 is the value deferred from cycle 011 as a v2.2
candidate (not promoted); used here as a smoke threshold, not as a
contract-pinned value. Record actual measurements and let cycle-014+
decide whether to promote.
```

### (d) Minimum Code Change

```text
new file : dream_permanence_loop.py  (~200-350 LOC estimated)
  - orchestrates steps 1-7 above
  - wraps SAM 2 / CoTracker / MonST3R inference as subprocess or
    editable install
  - implements permanence-signal publisher as a thin in-process
    function (no cross-spec signal contract serialization yet; Memory
    consumer is stubbed by an in-file function)
  - emits JSONL log: one line per clip (clip_id, t_occ, identity_track_count,
    reassociation_correct, static_map_drift_no_signal, static_map_drift_with_signal)

new file : permanence_signal_spec.yaml
  - documents the `suppress_static_write` signal schema actually
    emitted by the smoke; aligned with CROSS_SPEC_SIGNAL_CONTRACT.md
    v2.1 but NOT a contract revision (contract v2.1 unchanged)
```

## Evidence Label Discipline

- `identity_consistency` and `static_map_drift` become `measured` evidence only on the specific clip + hardware used. One clip is not coverage; it is existence evidence.
- The 0.7 identity_consistency threshold is `heuristic` (deferred from cycle 011 v2.2 candidates); smoke does NOT pin it into the contract.
- SAM 2 + CoTracker outputs are `prior inputs`, not Permanence mechanism outputs. A smoke success credits the Permanence mechanism only for the *signal-publication + drift-delta* pair; it does not credit SAM 2 or CoTracker as part of the Permanence claim.

## Stop Conditions

```text
(a) SAM 2 or CoTracker license prohibits intended research use -> stop;
    re-scope to license-compatible alternatives; do NOT proceed.
(b) Clip selection drifts toward KYKT-internal data -> stop; KYKT
    data access is gated.
(c) Any step produces output that requires more than 2x the inferred
    disk footprint (e.g., per-frame point-cloud dumps exceeding 100 GB)
    -> surface budget event; do not continue.
(d) Driver / CUDA conflict blocks installing all three primaries in one
    env -> try two primaries + one subprocess boundary; if still
    blocked, stop.
```

## What This Brief Does NOT Authorize

```text
- No clone, no download, no install, no run. Separate per-finalist
  DEC required.
- No retroactive edits to PERMANENCE-01..03 cards to pre-populate
  measured fields.
- No promotion of STORY-20260505-003 past `draft`.
- No promotion of 0.7 identity_consistency threshold into
  CROSS_SPEC_SIGNAL_CONTRACT.md (deferred v2.2 candidate; out of scope
  for L3 smoke).
- No deconfusion of the Julian Ost AAAI-2026 name-collision by editing
  an L2 card; deconfusion lives in `literature/CRITICAL_NOTES.md` per
  cycle 013 source-mining note.
- No KYKT data access, no frontend implementation, no teacher-demo
  readiness claim.
```
