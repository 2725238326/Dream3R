# Dream3R v0.2 code structure planning

artifact_id: planning/DREAM3R_V02_CODE_STRUCTURE.md

date: 2026-05-06

cycle: 020 (S2 deliverable per DEC-20260506-004)

status: v0.2 code structure plan (markdown only; planning artifact; NOT a code change)

honesty_label: every per-file change carries an inline evidence label (paper-derived / speculative / engineering-judgment / inferred). NSA-related changes are speculative for 3R transfer per NSA_MEMORY memo. DINOv3-S backbone swap is paper-derived. Expert pool composition is engineering-judgment per DEC-002 + COMPOSER_CAPABILITY_DESCRIPTORS. Line-of-code estimates are inferred.

linked_artifacts:
- decisions/DEC-20260506-004-cycle-020-launch-code-structure-and-implementation-roadmap.md (parent)
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (v0.2 architecture deltas locked)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; six numbered deltas)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2 ablation plan; ABL-v02-1..9 inform module change scope)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (7-expert pool informs Composer redesign)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (NSA + anchor bank informs Memory redesign)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (DINOv3-S informs Perceiver redesign)
- code/dream3r/PLAN.md (v0.1 implementation roadmap by user; preserved unchanged; coexists)
- planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (sibling cycle 020 deliverable; consumes this file as INPUT)

## Identity

This artifact is the v0.2 code structure planning document. It maps SPEC-20260506-004 v0.2 architecture deltas (Delta 1..6) to specific changes in the existing v0.1 code under code/dream3r/. It does NOT execute any change; it documents WHAT changes for the implementation roadmap to consume as INPUT.

This file is paired with planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (sibling artifact). The two files split WHAT (this file; structure) from HOW (roadmap; per-task checklist for execution).

## Approval

Approved scope: per `DEC-20260506-004` (cycle 020 launch + combined code structure + implementation roadmap; user-decided 2026-05-06 with "行" + "高强度推进").

Approved review-surface pattern: per user instruction 2026-05-06 ("其他agent审阅修改" + "你文档更新清楚哈"). Each MODIFIED + NEW file has an explicit review surface subsection.

NOT approved by this artifact:

- code execution; this is planning-only.
- training, GPU runs, checkpoint download (gated per F-002).
- KYKT navigation change, frontend implementation, demo storyboard promotion past `draft`.
- finalization of Dream3R candidacy.
- retiring of any non-finalist track or v0.1 ABL.
- modification of code/dream3r/PLAN.md (the v0.1 user-authored roadmap; preserved unchanged).

## Scope of v0.2 code structure

```text
markdown only
candidate-not-final (DEC-20260501-004)
no-all-in (DEC-20260504-002)
architecture-first mainline (DEC-20260506-001)
v0.2 architecture deltas locked (DEC-20260506-002)
v0.2 ablation deltas locked (DEC-20260506-003)
v0.2 code structure: this file + sibling roadmap (DEC-20260506-004)
```

This file documents per-file changes for v0.2 implementation. It does NOT prescribe execution order (that is the roadmap's job). It does NOT authorize any change (per-task DEC + per-step micro gates required).

## Reading order

```text
1. Read this file (you are here).
2. Read DEC-20260506-004 (parent decision).
3. Read SPEC-20260506-004 v0.2 architecture (Delta 1..6 reference).
4. Read sibling planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md
   (consumes this file as INPUT for per-task scoping).
5. Reference code/dream3r/PLAN.md (v0.1 roadmap; preserved unchanged;
   coexists; some phase-1 checkboxes are SUPERSEDED in v0.2 scope).
6. Reference v0.2 ablation plan SPEC-005 ONLY when a code change ties
   to a specific ABL-v02-N harness (ABL execution surface is in
   roadmap; not this file).
```

## Existing v0.1 code structure (substrate; per code/dream3r/PLAN.md + INDEX)

```text
code/dream3r/
├── __init__.py            package entry
├── bus.py        ~130 lines    C6 Memory Bus + CR-1..CR-6 gates (zero parameters)
├── modules.py    ~280 lines    C1 Perceiver / C2 Memory / C3 Permanence / C4 Critic / C5 Composer
├── model.py      ~150 lines    Dream3R main + bus tick orchestration; preset configs (small / small_vit)
├── losses.py     ~90  lines    multi-loss L_total: pointmap + critic P1/P5 + permanence P4 + action entropy
├── smoke_test.py ~100 lines    end-to-end validation: forward + backward + bus signals + CR-1 gate + memory carry-over
├── config.py                   YAML config (planned per PLAN 1.2; partial)
├── data_dtu.py                 DTU DataLoader (planned per PLAN 2; partial)
├── train.py                    training driver (planned per PLAN 1.2; partial)
└── PLAN.md                     v0.1 implementation roadmap (user-authored 2026-05-06; preserved unchanged)
```

v0.1 phase-1 checkboxes already done per PLAN.md:

```text
[x] C1 Perceiver: timm ViT-Base + multi-layer MLP heads
[x] C2 Memory: input concat fix + suppress_mask dim fix + LayerNorm
[x] C3 Permanence: Slot Attention rewrite per Locatello 2020
[x] C4 Critic: 2-layer TransformerEncoder over 17 evidence tokens
[x] C6 Bus: read() + Critic reads capability_match + latent_drift_proxy
```

v0.1 phase-1 checkboxes pending per PLAN.md (now SUPERSEDED in v0.2 scope; see §"Pre-existing v0.1 PLAN.md relationship"):

```text
[ ] C5 Composer: regime classifier with real input metadata
[ ] C2 Memory: GRU -> Mamba SSM swap          (SUPERSEDED in v0.2:
                                               replaced by NSA + anchor bank
                                               per Delta 3 + NSA memo)
```

v0.1 phase-2..6 checkboxes (training infra / data / backbone / training / ablation / scaling) carry forward into v0.2 with delta-specific changes; details in per-file manifest below.

## v0.2 delta -> module mapping table

| v0.2 Delta | Driver | MODIFIED files | NEW files | STABLE files |
|---|---|---|---|---|
| Delta 1 frame budget | DINOV3_C1 + NSA memo + COMPOSER descriptors | smoke_test.py, model.py | bench_frame_budget.py | bus.py, losses.py |
| Delta 2 DINOv3-S backbone | DINOV3_C1 memo | modules.py (C1), config.py | dinov3_backbone.py (optional wrapper) | bus.py |
| Delta 3 NSA + anchor bank | NSA memo | modules.py (C2), model.py | memory_anchor_bank.py, nsa_attention.py | bus.py |
| Delta 4 sparse attention | NSA memo | shares Delta 3 NSA layer | (no separate file) | bus.py |
| Delta 5 7-expert Composer | COMPOSER descriptors | modules.py (C5), model.py, config.py | composer_experts/__init__.py + 7 adapter files | bus.py |
| Delta 6 main-claim narrowing | DEC-002 | (documentation only) | (none) | all |

Aggregate impact:

```text
MODIFIED files: 5 (modules.py, model.py, losses.py, smoke_test.py, config.py)
                + train.py (training schedule per Delta 2 + ABL-v02-7)
NEW files     : 11 (bench_frame_budget.py, dinov3_backbone.py optional,
                memory_anchor_bank.py, nsa_attention.py, composer_experts/
                __init__.py, mast3r_adapter.py, fast3r_adapter.py,
                spann3r_adapter.py, cut3r_adapter.py, moge2_adapter.py,
                depth_anything_v2_adapter.py, test3r_adapter.py)
              # = 12 NEW python modules total
STABLE files  : bus.py (CR-1..CR-6 gates carry; signal-space additive)
                losses.py (L_total structure carries; weights vary per
                           ABL-v02-7 head schedule)
```

## Per-file change manifest

### MODIFIED: modules.py (C1-C5 cores)

```text
file:           code/dream3r/modules.py
v01_size:       ~280 lines
v02_size_est:   ~480 lines (~+200 lines for v0.2 deltas; -50 lines
                for sub-module extraction to NEW files; net ~+170)
drives:         Delta 2 + Delta 3 + Delta 5
ev_label:       paper-derived (Delta 2) + speculative (Delta 3) +
                engineering-judgment (Delta 5)
```

Changes:

- **C1 Perceiver class** — backbone swap from timm ViT-Base/L to DINOv3-S (default) or DINOv3-B (fallback). Heads (pointmap_head, confidence_head, evidence_head) re-init from scratch (cannot transfer ViT-L head weights to DINOv3 feature space). Frozen-backbone default; partial-unfreeze opt-in via config flag (per ABL-v02-3 harness). Patch size 14 (DINOv3 default).
- **C2 Memory class** — refactor from GRU/Mamba to bounded anchor bank + NSA-style three-branch retrieval. Memory state delegates storage to NEW memory_anchor_bank.py and selection to NEW nsa_attention.py. C2 itself becomes a thin orchestrator. Mamba SSM retained as optional medium-term substrate (config flag).
- **C5 Composer class** — replace single-module regime classifier with 7-expert routing layer. Each expert is loaded via NEW composer_experts/ adapter modules. Composer itself contains: route() function (capability_match + critic_confidence + permanence_link -> expert selection); fallback fixed-routing-policy (per COMPOSER routing policy sketch).
- **C3 Permanence class** — UNCHANGED in v0.2 (slot attention per Locatello 2020 carries; bounded slots respected by NEW anchor bank).
- **C4 Critic class** — UNCHANGED in v0.2 (2-layer TransformerEncoder over 17 evidence tokens carries).

Interface stability:

- C1.forward(images: Tensor [B, T, 3, H, W]) -> dict — signature unchanged; output dict adds `dinov3_features` key for downstream feature reuse.
- C2.forward(perception_summary, evidence_tokens, ...) -> dict — signature unchanged; new kwargs `critic_confidence` + `permanence_link` flow into NSA selection gate.
- C5.forward(perception_summary, ...) -> dict — signature unchanged; output dict adds `routed_expert_id` + `expert_outputs` keys.

Risk + review surface:

```text
- Risk: head re-init invalidates DUSt3R-pretrained pointmap weight
  transfer; v0.2 code path must NOT fall back to v0.1 head weights.
- Risk: anchor bank + NSA imports add new dependency on
  memory_anchor_bank.py + nsa_attention.py — verify both files
  exist before C2.forward is invoked.
- Risk: Composer 7-expert pool requires 7 adapter modules + their
  checkpoints; missing checkpoints must fail loud at __init__,
  not silent at forward.

Review surface (for reviewing agents before authorizing
T-v02-C1 / T-v02-C2-mem-bank / T-v02-C2-nsa / T-v02-C5):

[ ] Verify backbone factory selects DINOv3-S by default; -B / -L
    fallbacks accessible via config flag.
[ ] Verify C1 head weights are explicitly re-init (not silent
    random init from a wrong dtype).
[ ] Verify C2 anchor bank K=256 default; modifiable via config.
[ ] Verify NSA selection gate reads BOTH critic_confidence + permanence
    _link; subsetting via config flag (for ABL-v02-6 harness).
[ ] Verify C5 routing policy matches COMPOSER_CAPABILITY_DESCRIPTORS
    routing policy sketch; deviations documented in fresh DEC.
[ ] Verify expert adapter modules exist before Composer __init__
    succeeds; missing adapter raises an explicit error, not silent.
[ ] Verify C3 Permanence is NOT changed (sanity check; no scope creep).
[ ] Verify C4 Critic is NOT changed (sanity check).
[ ] Run smoke_test.py (Tier 3 task T-v02-E) before declaring done.
```

### MODIFIED: model.py (Dream3R main + bus tick)

```text
file:           code/dream3r/model.py
v01_size:       ~150 lines
v02_size_est:   ~210 lines (~+60 lines for v0.2 routing + bus tick
                additions)
drives:         Delta 1 + Delta 3 + Delta 5
ev_label:       inferred (bus tick reorchestration impact)
```

Changes:

- Add Delta 1 latency instrumentation hooks per bus tick step (optional via config; for T-v02-A frame-budget benchmark scaffolding).
- Update C2 Memory invocation to pass critic_confidence + permanence_link signals into the NSA selection gate (per Delta 3).
- Update C5 Composer invocation to pass routing context (input regime metadata + capability_match table) into the 7-expert router (per Delta 5).
- Bus tick order unchanged from v0.1; the read-write protocol per window (v0.1 SPEC-001 §"Read-write protocol per window") carries forward without modification.
- Preset configs expand: existing `small` + `small_vit` carry as v0.1 reference; ADD `small_v02` (DINOv3-S + anchor bank K=256 + NSA k=8 + 7-expert pool default) and `base_v02` (DINOv3-B + larger K) presets.

Interface stability:

- Dream3R.forward(...) signature unchanged.
- Dream3R config schema EXPANDS (additive); v0.1 configs continue to load (backward-compat for v0.1 ablations).

Risk + review surface:

```text
- Risk: bus tick hooks for latency instrumentation must NOT change
  numerical outputs (instrumentation is observe-only).
- Risk: preset config sprawl — new v02 presets must be additive,
  not silent overwrites of v01 presets.

Review surface (for reviewing agents before authorizing T-v02-D):

[ ] Verify bus tick order matches v0.1 SPEC-001 §"Read-write
    protocol per window"; no reordering.
[ ] Verify latency instrumentation is opt-in (default off); no
    silent overhead in production runs.
[ ] Verify config keys for v0.1 presets are NOT removed; v0.1 +
    v0.2 presets coexist.
[ ] Verify critic_confidence + permanence_link signal flow:
    written by C4 + C3, read by C2 NSA gate. Bus contract
    log captures the read.
[ ] Run v0.1 smoke_test (existing) before v0.2 changes to
    establish baseline; run v0.2 smoke_test after to verify no
    regression on v0.1 path.
```

### MODIFIED: smoke_test.py (end-to-end validation)

```text
file:           code/dream3r/smoke_test.py
v01_size:       ~100 lines
v02_size_est:   ~180 lines (~+80 lines for v0.2 module-isolation
                + end-to-end + latency-instrumentation tests)
drives:         Delta 1 + Delta 2 + Delta 3 + Delta 5
ev_label:       inferred
```

Changes:

- Add per-module isolation tests for NEW modules: memory_anchor_bank.py (K=256 capacity + LRU eviction + permanence-protect), nsa_attention.py (three-branch + selection gate input mix), composer_experts adapters (one-test-per-adapter sanity).
- Add v0.2 end-to-end forward pass with `small_v02` preset; verify shapes + bus contract log non-empty + CR-1..CR-6 gates fire on synthetic adversarial input (per v0.1 ABL-1 + v0.2 ABL-v02-6 surface).
- Add latency instrumentation enable test (toggles model.py instrumentation hooks; verifies output numerics unchanged).
- Retain v0.1 smoke test path (default config = `small_vit`); v0.2 smoke test runs as a separate code path under `small_v02` preset.

Interface stability:

- main() entry point unchanged; CLI flag `--v02` selects v0.2 preset (additive).
- Existing v0.1 test functions preserved as `test_v01_*` for parity tracking.

Risk + review surface:

```text
- Risk: smoke test divergence between v0.1 + v0.2 paths leads to
  silent v0.1 regression — keep both paths runnable until v0.2
  is fully validated.

Review surface (for reviewing agents before authorizing T-v02-E):

[ ] Verify v0.1 smoke test path still passes after v0.2 additions
    (regression check).
[ ] Verify per-module isolation tests cover the NEW modules (anchor
    bank + NSA + 7 adapters; one test per file).
[ ] Verify end-to-end test verifies bus contract log captures
    expected reads + writes per Delta 3 (NSA selection gate).
[ ] Verify CR-1..CR-6 gate triggering test uses synthetic
    adversarial input similar to v0.1 ABL-8 (CR-rule ablation
    inputs).
[ ] Verify smoke test exit code is informative (error if any module
    isolation test fails; error if v0.1 regression detected).
```

### MODIFIED: config.py (YAML config + presets)

```text
file:           code/dream3r/config.py
v01_size:       partial (per PLAN.md phase 1.2 [ ] checkbox)
v02_size_est:   ~300 lines (full YAML schema for v0.1 + v0.2 presets;
                config-flag surface for ABL-v02-N harnesses)
drives:         Delta 2 + Delta 3 + Delta 5 + ABL harnesses
ev_label:       inferred
```

Changes:

- Define YAML schema with sections: `model` (preset selection), `backbone` (DINOv3 tier + frozen-flag), `memory` (NSA K + k + W + signal mix flags), `composer` (expert pool selection + routing policy), `losses` (per-loss weights), `training` (schedule + DDP), `ablation` (ABL-v02-N variant selection flags).
- Provide presets: `small_v01` (v0.1 baseline; ViT-Base + GRU; 1-card test), `small_v02` (v0.2 default; DINOv3-S + NSA + 7-expert), `base_v02` (DINOv3-B + larger K + full pool), `abl_v02_<N>` (per-ablation preset overlays for ABL-v02-1..9).
- Per-config validation at load time (fail loud on unsupported combinations e.g., DINOv3-L on TITAN RTX).

Interface stability:

- Config loader signature unchanged.
- v0.1 yaml files load unchanged (backward-compat).

Risk + review surface:

```text
- Risk: YAML schema sprawl — keep schema layered (model / backbone /
  memory / composer / losses / training / ablation); each ABL-v02-N
  is one preset overlay, not a flat option.

Review surface (for reviewing agents before authorizing T-v02-B):

[ ] Verify schema sections are layered, not flat.
[ ] Verify preset hierarchy: defaults -> v01 / v02 -> ablation
    overlays.
[ ] Verify per-config validation fails loud (no silent fallback
    to a different config).
[ ] Verify v0.1 yaml files load unchanged.
[ ] Verify ABL-v02-N preset overlays cover all 9 ablations from
    SPEC-005.
```

### MODIFIED: train.py (training driver)

```text
file:           code/dream3r/train.py
v01_size:       partial (per PLAN.md phase 1.2 [ ] checkbox)
v02_size_est:   ~400 lines (DDP + amp + ckpt + tensorboard + grad-ckpt
                + multi-stage training schedule for ABL-v02-7 harness)
drives:         Delta 2 + ABL-v02-7
ev_label:       inferred
```

Changes:

- DDP multi-card training (2-3 cards on TITAN RTX; CUDA_VISIBLE_DEVICES control).
- Mixed precision via torch.amp (per PLAN phase 1.2 [ ]).
- Gradient checkpointing (per PLAN phase 1.2 [ ]; long-sequence VRAM saving).
- Multi-stage training schedule (head-only warmup -> Top-N unfreeze -> full unfreeze; per ABL-v02-7 harness; controlled via config schedule key).
- Checkpoint save / resume (per PLAN phase 1.2 [ ]).
- TensorBoardX logging (per PLAN phase 1.2 [ ]).

Interface stability:

- CLI flags expand additive; existing flags preserved.
- Training loop function signature stable.

Risk + review surface:

```text
- Risk: DDP introduces correctness bugs (incorrect gradient sync;
  incorrect random seed handling); requires multi-seed validation.
- Risk: Multi-stage schedule may cause training instability; reviewer
  should verify schedule-stage transitions are smooth (no gradient
  spike at stage boundaries).

Review surface (for reviewing agents before authorizing T-v02-F
+ ABL-v02-7 harness execution):

[ ] Verify DDP correctness via gradient-sync test (compare 2-card
    vs 1-card outputs over short run).
[ ] Verify mixed precision does not silently change loss landscape
    (dtype-agnostic test).
[ ] Verify multi-stage schedule transitions are explicit checkpoint
    boundaries (each stage saves a ckpt before transitioning).
[ ] Verify TensorBoardX log includes per-stage loss curves +
    per-bus-signal traces (for debugging).
[ ] Verify checkpoint resume restores all relevant state (model +
    optimizer + scheduler + RNG seeds).
```

### MODIFIED: __init__.py (package entry)

```text
file:           code/dream3r/__init__.py
change:         export NEW modules (memory_anchor_bank / nsa_attention
                / composer_experts) from package namespace; preserve
                existing exports.
ev_label:       engineering-judgment (export hygiene)
```

Review surface:

```text
[ ] Verify new exports do not shadow existing names.
[ ] Verify __all__ list is updated.
```

### NEW: memory_anchor_bank.py

```text
file:           code/dream3r/memory_anchor_bank.py (NEW)
size_est:       ~250 lines
drives:         Delta 3 (anchor bank A direction per NSA memo)
ev_label:       inferred (storage + eviction policy is implementation;
                anchor bank concept is paper-derived from NSA memo)
```

Module contents:

- `class AnchorBank` — bounded anchor bank with K=256 default capacity.
  - `__init__(K, D, eviction='lru', permanence_protect=True)`.
  - `add(anchor_embedding, scene_pose_metadata, permanence_link)` — admission policy with eviction.
  - `query(query_vec, top_k=8)` — cosine top-k baseline (used by ABL-v02-1 NSA-removal variant).
  - `evict()` — LRU among non-permanence-protected entries.
  - `state_dict() / load_state_dict()` — checkpointing.
- Per-anchor entry struct: `anchor_embedding (D-dim) + scene_pose_metadata + freshness_counter + permanence_link`.
- Per Delta 3 + NSA memo §"Concrete v0.2 design sketch".

Interface stability:

- AnchorBank is a NEW class; no existing API to preserve.
- C2 Memory module composes AnchorBank instance.

Risk + review surface:

```text
- Risk: eviction policy bug (e.g., evicting permanence-protected
  entry under high pressure); needs explicit unit test.
- Risk: anchor embedding D-dim mismatch with C2's evidence_token
  D-dim — verify shape compat at __init__.

Review surface (for reviewing agents before authorizing T-v02-C2-mem-bank):

[ ] Verify K=256 default; configurable via config.
[ ] Verify cosine top-k path exists (not just NSA path); ABL-v02-1
    NSA-removal variant uses cosine path.
[ ] Verify LRU eviction does not evict permanence-protected entries
    under any condition.
[ ] Verify state_dict / load_state_dict round-trip preserves
    anchor entries + permanence links.
[ ] Verify unit test covers: full bank + add new entry + verify
    eviction; permanence-protected at capacity + verify NO eviction
    of protected entry.
[ ] Verify shape compat: D-dim of AnchorBank matches C2 evidence
    token D-dim.
```

### NEW: nsa_attention.py

```text
file:           code/dream3r/nsa_attention.py (NEW)
size_est:       ~300 lines
drives:         Delta 3 + Delta 4 (NSA three-branch + selection gate)
ev_label:       speculative (NSA-to-3R transfer; no published 3R use
                per NSA memo §"Risk / honest limits")
```

Module contents:

- `class NSAAttention` — three-branch (compressed + selected + sliding) sparse attention layer.
  - `__init__(D, k=8, compressed_size=32, sliding_window=4)`.
  - `forward(query, anchor_bank, evidence_window, gate_inputs)` — gate_inputs is dict with optional `critic_confidence` + `permanence_link` keys; missing keys mask out (used by ABL-v02-6 signal subsetting harness).
  - Three branches:
    - Compressed: aggregate anchor bank into ~32 compressed summary tokens; cheap full-attn to coarse scene context.
    - Selected: gate(query, anchor_embedding, evidence, critic_confidence, permanence_link) -> top-k anchors; full-attn over selected.
    - Sliding: last W frames of evidence -> full-attn.
  - Three branch outputs combined via gating.
- Hardware-aware kernel hook (optional via config flag for ABL-v02-9 kernel decomp harness; falls back to algorithmic NSA without fused kernel).

Interface stability:

- NSAAttention is a NEW class; no existing API to preserve.
- C2 Memory module composes NSAAttention instance.

Risk + review surface:

```text
- Risk: NSA hardware-aware kernel may not compile on cu121 + TITAN
  RTX (per NSA memo §"Risk / honest limits" item 2); algorithmic
  fallback path must be functional.
- Risk: signal subsetting via gate_inputs dict missing-key masking
  must be explicit, not silent default-zero (the test should fail
  loud if gate is mis-configured).

Review surface (for reviewing agents before authorizing T-v02-C2-nsa):

[ ] Verify three branches are independently testable (unit test
    per branch).
[ ] Verify gate input mix supports ABL-v02-6 subsetting (Critic-
    only / Permanence-only / both / neither variants via config).
[ ] Verify hardware-aware kernel hook is opt-in; fallback path
    is the default until kernel is verified on TITAN RTX.
[ ] Verify k=8 default; configurable via config (for ABL-v02-1
    cosine top-k variant uses same k).
[ ] Verify forward signature is consistent with NSA paper +
    NSA_MEMORY_INTEGRATION_MEMO §"Concrete v0.2 design sketch".
```

### NEW: composer_experts/ subdirectory

```text
files:          code/dream3r/composer_experts/__init__.py (NEW; ~100 lines)
                + 7 adapter files (NEW; each ~150-200 lines):
                  mast3r_adapter.py
                  fast3r_adapter.py
                  spann3r_adapter.py
                  cut3r_adapter.py
                  moge2_adapter.py
                  depth_anything_v2_adapter.py
                  test3r_adapter.py
total_size_est: ~1300 lines (7 adapters × ~180 + __init__.py 100)
drives:         Delta 5 (7-expert pool per COMPOSER descriptors)
ev_label:       paper-known (per-expert innovation + interface) +
                engineering-judgment (adapter design)
```

Per-adapter contents (uniform pattern):

- `class <Expert>Adapter` — wraps the expert's native inference path; maps to Bus token space (T2 / T3 / T5 / T6 per COMPOSER descriptors).
  - `__init__(checkpoint_path, device, ...)` — loads expert checkpoint; fails loud if missing.
  - `forward(input_regime, **kwargs)` — runs expert; returns dict with Bus-publishable outputs.
  - `capability_match` — class-level inferred values from COMPOSER_CAPABILITY_DESCRIPTORS; supersedes to measured if ABL-v02-5 measurement pass executed.
  - `latency_estimate` — paper-derived per-expert latency target.
  - `attention_regime` — full / linear / sparse per descriptor.

Per-adapter Bus token mapping (per COMPOSER descriptors §"Per-expert adapter sketch"):

```text
mast3r_adapter        : pair pointmap -> T2 / dense matches -> T3
                        / reciprocal matches -> T5 candidates
fast3r_adapter        : per-image pointmap -> T2 / poses -> T6
spann3r_adapter       : incremental pointmap -> T2 / spatial
                        anchors -> T5 / memory state seed -> Bus
cut3r_adapter         : pointmap -> T2 / persistent state -> Bus
                        medium-term state slot
moge2_adapter         : single-view pointmap -> T2 (scale-norm)
                        / mono_recovery_pointmap -> Bus
depth_anything_v2_adapter
                      : depth map -> T3 evidence (cheap prior)
test3r_adapter        : Bus read C4 flagged region -> triplet
                        select; consistency score -> T3 evidence
                        (revision verdict)
```

`__init__.py` contents:

- Expert factory function `get_expert(expert_id) -> ExpertAdapter`.
- Expert registry dict mapping expert_id -> adapter class.
- `available_experts()` returns the 7 admitted expert ids; missing-checkpoint experts raise explicit error at registry initialization (NOT silent skip).

Interface stability:

- All 7 adapter files are NEW; no existing API to preserve.
- C5 Composer composes ExpertAdapter instances per the active pool.

Risk + review surface:

```text
- Risk: adapter divergence — if an expert's native API changes
  (e.g., Spann3R upstream version bump), the adapter must be
  versioned. Per-adapter version pinning required.
- Risk: missing checkpoint silent fallback would mask routing
  errors. Must fail loud.
- Risk: adapter latency varies wildly per expert; routing policy
  must respect per-frame budget (per Delta 1) — expensive experts
  (Test3R) are off-streaming-path lazy invocation only.
- Risk: license incompatibility (MASt3R non-commercial; per
  COMPOSER descriptors §"Pool members" EXPERT-01 evidence label);
  reviewer must verify license before checkpoint download
  authorization.

Review surface (for reviewing agents before authorizing
T-v02-C5 + per-adapter T-v02-EXPERT-N):

[ ] Verify each adapter wraps the expert's NATIVE inference; do
    NOT re-implement the expert (this is a routing layer, not a
    re-implementation).
[ ] Verify each adapter's checkpoint provenance + license is
    documented in the adapter file's docstring.
[ ] Verify __init__.py expert registry is the SINGLE source of
    truth for available experts; C5 Composer reads from registry.
[ ] Verify capability_match values match COMPOSER_CAPABILITY_
    DESCRIPTORS exactly (no silent drift); ABL-v02-5 measurement
    pass updates these values via fresh DEC, not in-place edit.
[ ] Verify Test3R adapter is OFF the streaming path (lazy
    invocation only; verify Composer routing does not call
    test3r_adapter.forward() in the streaming bus tick).
[ ] Verify adapter unit tests exist (one test file per adapter;
    sanity forward + shape check + latency-budget compliance
    check).
```

### NEW: bench_frame_budget.py

```text
file:           code/dream3r/bench_frame_budget.py (NEW)
size_est:       ~200 lines
drives:         Delta 1 (frame budget) + ABL-v02-8 harness
ev_label:       inferred
```

Module contents:

- Per-component latency profiling: C1 / C2 / C3 / C4 / C5 / C6 each measured under realistic streaming load (not isolated forward passes).
- End-to-end streaming benchmark: continuous 30 FPS input over multiple seconds; reports p50 / p95 / p99 per-frame latency.
- Lazy-path test: Test3R triggered at low / medium / high frequency; verifies off-streaming claim.
- Output: JSON report consumable by reviewer + tensorboard log.

Interface stability:

- Standalone CLI script.
- Imports model.py + smoke_test.py utilities for setup.

Risk + review surface:

```text
- Risk: latency measurement on TITAN RTX must NOT report A100/H100
  numbers (per Delta 1 honest evidence label); verify hardware
  detection.

Review surface (for reviewing agents before authorizing T-v02-A
+ ABL-v02-8 harness execution):

[ ] Verify hardware detection (TITAN RTX); refuse to run on
    unsupported hardware without explicit override.
[ ] Verify per-component measurement uses identical input + context
    state; latency depends on context.
[ ] Verify end-to-end measurement runs continuously over multiple
    seconds (not single-frame averages).
[ ] Verify lazy-path measurement explicitly triggers Test3R at
    documented frequencies.
[ ] Verify reported numbers include p50 + p95 + p99 (mean alone
    insufficient).
```

### NEW: dinov3_backbone.py (optional wrapper)

```text
file:           code/dream3r/dinov3_backbone.py (NEW; OPTIONAL)
size_est:       ~150 lines (if needed)
drives:         Delta 2
ev_label:       paper-derived (DINOv3 family; backwards-compat with
                DINOv2 usage patterns)
```

Module contents (OPTIONAL — may be merged into modules.py if simple):

- DINOv3 backbone factory: `get_dinov3_backbone(tier: 'S'|'B'|'L', frozen: bool)`.
- Patch size 14 (DINOv3 default).
- Per-tier param + latency targets logged at __init__.
- License + checkpoint path documented.

Decision (per Open Question Q-cs-1 below): merge into modules.py if simple; split out if DINOv3 family handling grows beyond ~100 lines.

Risk + review surface:

```text
[ ] Verify DINOv3 weights provenance (Meta hub) + license +
    Hugging Face hub paths.
[ ] Verify checkpoint download path is server-side (per F-002).
[ ] Verify per-tier latency targets match DINOV3_C1 memo
    §"Why DINOv3-S replaces v0.1's ViT-L".
```

## Stable / unchanged in v0.2

```text
file: bus.py
v0.1 size: ~130 lines
v0.2 change: NONE
rationale: CR-1..CR-6 gates carry forward unchanged per SPEC-004
           Delta 6 + §"What carries forward unchanged from v0.1";
           signal namespace is additive (new signals like
           critic_confidence + permanence_link are read by C2 NSA
           gate; bus already supports additive signals via typed
           namespace).

Review surface (for any agent considering bus.py changes):
[ ] If you think bus.py needs change for v0.2: STOP. Open a fresh
    DEC to revisit. Bus stability is a v0.2 architecture invariant.
```

```text
file: losses.py
v0.1 size: ~90 lines
v0.2 change: NONE structural; loss WEIGHTS may vary per ABL-v02-7
             head training schedule (configurable; not a code
             rewrite).
rationale: L_total multi-loss structure (pointmap + critic P1/P5
           + permanence P4 + action entropy) carries forward.
           Weight tuning is config-level, not code-level.

Review surface:
[ ] Verify loss weight changes go via config, not via code edit.
```

## Interface stability statement

The following v0.1 public APIs MUST NOT change syntactically in v0.2 (other modules + downstream code rely on them):

```text
1. Dream3R.forward(images, **kwargs) -> dict
   v0.1 signature; v0.2 preserves; output dict EXPANDS additive.

2. C1 Perceiver / C2 Memory / C3 Permanence / C4 Critic / C5 Composer
   .forward signatures preserved. C2 + C5 expand kwargs additive.

3. Bus.publish / Bus.read / Bus.handoff / Bus.contract_log signatures
   preserved unchanged. Signal namespace additive.

4. CR-1..CR-6 gate function signatures preserved unchanged.

5. config.load(yaml_path) signature preserved; schema EXPANDS
   additive (v0.1 yamls continue to load).

6. smoke_test.main() entry point preserved; CLI flags additive.

7. losses.compute_total_loss(predictions, targets, weights) signature
   preserved; weights argument now consumable by ABL-v02-7 schedule.
```

Semantic changes (honest to flag; reviewers should verify):

```text
1. C1 forward output dict adds `dinov3_features` key — downstream
   consumers may want this for feature reuse (additive; backward-
   compat).

2. C2 forward output dict adds `selected_anchors` + `memory_retrieval
   _log` keys per Delta 3 — Permanence + Critic may want to read
   these (additive).

3. C5 forward output dict adds `routed_expert_id` + `expert_outputs`
   keys per Delta 5 (additive).

4. Bus signal namespace adds `critic_confidence` + `permanence_link`
   + `selected_anchors` + `memory_retrieval_log` (additive).

5. config schema adds `backbone.dinov3_tier` + `memory.nsa.*` +
   `composer.experts.*` + `ablation.v02.*` sections (additive).
```

## Server-side deployment surface (per F-002)

```text
Local             : E:\kykt\Dream\code\dream3r\           (editing)
Server            : /hdd3/kykt26/code/dream3r/             (execution)
Server env        : conda env `dream3r` (Python 3.10; torch 2.5.1+cu121;
                    causal-conv1d 1.6.1; mamba-ssm 2.2.4; transformers
                    4.46.0; timm 1.0.26; einops 0.8.2; scipy 1.15.3;
                    tensorboardX 2.6.5)
Server hardware   : 4 × NVIDIA TITAN RTX 24 GB
GPU recommendation: 2-3 cards via DDP for training (per PLAN.md)

v0.2 deployment requires (per F-002 + cycle 020 §"Not allowed by this DEC"):
  fresh DEC per checkpoint download (DINOv3-S; CUT3R; MoGe-2;
                                     DepthAnything-V2; Test3R;
                                     others as needed)
  fresh DEC per per-task execution (T-v02-A..F + T-v02-ABL-1..9)
  per-step micro gates G_clone / G_install / G_download / G_run /
                       G_log_use per cycle 015 D5' pattern

NSA kernel availability on cu121 + TITAN RTX is uncertain (per NSA
memo §"Risk / honest limits" item 2). Algorithmic fallback path is
the default until kernel is verified.

Local box (Windows; per F-002): markdown + planning + code editing
+ shallow read-only clones for code review only. Never run training
locally.
```

## Pre-existing v0.1 PLAN.md relationship

```text
code/dream3r/PLAN.md is the v0.1 implementation roadmap authored by
the user 2026-05-06. It is preserved unchanged in cycle 020 (per
DEC-20260506-004 §"Not allowed by this DEC" item 2).

PLAN.md sections relationship to v0.2:

§"当前基线" (current baseline)         : carries forward unchanged.
                                         Server env + data + hardware
                                         status remain canonical.

§"阶段一 1.1 模块级代码审查和重构":
  Done [x] items                       : carry forward as substrate
                                         for v0.2; v0.2 builds on
                                         them.
  [ ] C5 Composer regime classifier   : SUPERSEDED in v0.2. v0.2
                                         replaces single-classifier
                                         with 7-expert pool +
                                         capability_match routing per
                                         Delta 5. v0.2 roadmap T-v02-C5
                                         is the new task.
  [ ] C2 GRU -> Mamba SSM swap        : SUPERSEDED in v0.2. v0.2
                                         replaces with anchor bank
                                         + NSA per Delta 3. Mamba
                                         optional medium-term
                                         substrate (config flag).
                                         v0.2 roadmap T-v02-C2-mem-
                                         bank + T-v02-C2-nsa are
                                         the new tasks.

§"阶段一 1.2 训练基础设施"            : carries forward into v0.2 with
                                         additive ABL-v02-7 schedule
                                         support. v0.2 roadmap T-v02-B
                                         (YAML config) + T-v02-F
                                         (training driver) consume
                                         these checkboxes.

§"阶段一 1.3 代码质量"                : carries forward unchanged.

§"阶段二 数据准备" (DTU + KITTI)      : carries forward unchanged into
                                         v0.2. v0.2 roadmap T-v02-F
                                         depends on this.

§"阶段三 Backbone 接入"                : v0.1 plans timm ViT-Base then
                                         DUSt3R ViT-L. v0.2 SUPERSEDES:
                                         use DINOv3-S default per
                                         Delta 2. DUSt3R ViT-L
                                         remains v0.1 reference
                                         baseline (for ABL-v02-2
                                         backbone tier comparison).

§"阶段四 第一轮训练"                   : carries forward; v0.2 uses
                                         small_v02 preset (per
                                         T-v02-B config).

§"阶段五 Tier 1 消融实验"             : v0.1 lists ABL-1, ABL-2, ABL-3.
                                         v0.2 ablation plan SPEC-005
                                         ADDS ABL-v02-1..9. v0.1
                                         ABLs remain canonical for
                                         v0.1 architecture testing;
                                         v0.2 ABLs cover v0.2
                                         architecture surfaces.

§"阶段六 扩大规模"                     : carries forward; gated.
```

## Risks (v0.2 code structure delta)

```text
R-cs-1.  NSA kernel unavailable on cu121 + TITAN RTX.
         Mitigation: nsa_attention.py provides algorithmic fallback
         path as default. ABL-v02-9 measures kernel benefit if
         available; null result is honest.

R-cs-2.  DINOv3-S pointmap quality regression vs ViT-L baseline.
         Mitigation: -B fallback documented in modules.py C1 +
         config preset; ABL-v02-2 measures regression.

R-cs-3.  Adapter divergence as upstream experts version-bump.
         Mitigation: per-adapter version pinning + per-adapter
         unit test (sanity forward + shape check). Fresh DEC for
         any expert version upgrade.

R-cs-4.  License incompatibility (MASt3R non-commercial; etc.).
         Mitigation: per-adapter license documented in docstring;
         reviewer authorization gate before any checkpoint
         download (per F-002).

R-cs-5.  Bus tick reorchestration introducing numerical drift.
         Mitigation: model.py changes preserve bus tick order;
         smoke_test verifies v0.1 path passes after v0.2 additions.

R-cs-6.  Multi-stage training schedule instability (head warmup
         -> Top-N unfreeze transitions).
         Mitigation: explicit checkpoint boundaries at stage
         transitions; multi-seed validation per ABL-v02-7.

R-cs-7.  Config schema sprawl across v0.1 + v0.2 + 9 ABL overlays.
         Mitigation: layered schema (sections + preset hierarchy);
         per-config validation at load time; ABL preset overlays
         are additive, not replacements.

R-cs-8.  v0.1 PLAN.md silent supersede.
         Mitigation: v0.1 PLAN.md preserved unchanged; supersede
         relationships explicitly documented in §"Pre-existing
         v0.1 PLAN.md relationship" above; reviewers can compare.
```

## Boundaries (v0.2 code structure delta)

```text
B-cs-A.  Cycle 020 produces 2 NEW planning files. NO source code is
         modified by cycle 020 itself. Each per-file change manifest
         entry above is a PROPOSAL for execution; execution requires
         fresh DEC per task per F-002.

B-cs-B.  v0.1 code/dream3r/PLAN.md is preserved unchanged. Supersede
         relationships are documented in §"Pre-existing v0.1 PLAN.md
         relationship"; PLAN.md text is NOT edited.

B-cs-C.  v0.1 + v0.2 code paths coexist. v0.1 ablations (ABL-1..ABL-10)
         remain runnable on v0.1 presets. v0.2 ablations (ABL-v02-1..9)
         run on v0.2 presets. No v0.1 code path is deleted.

B-cs-D.  All NEW python modules (memory_anchor_bank / nsa_attention /
         composer_experts/ + 7 adapters / bench_frame_budget /
         dinov3_backbone optional) are SCOPED to code/dream3r/
         package; no top-level utility modules added outside.

B-cs-E.  Bus stability invariant: bus.py is NOT modified in v0.2.
         CR-1..CR-6 gates + signal namespace + read-write protocol
         all carry forward unchanged. Signal additions are namespace
         additive only. Any proposed bus.py change requires fresh
         DEC + v0.3 architecture revision (NOT a code refactor DEC).

B-cs-F.  Per-file review surface subsections in this artifact are
         informative for other-agent handoff. Modifying them in-place
         is NOT allowed; supersede via a v0.3 addendum + fresh DEC
         (Honesty Override).
```

## Linked artifacts (full list)

Decisions:

- DEC-20260506-004 (cycle 020 launch + this artifact scope; parent)
- DEC-20260506-003 (cycle 019 ablation plan v0.2 addendum)
- DEC-20260506-002 (cycle 018 v0.2 architecture deltas)
- DEC-20260506-001 (mainline architecture-first)
- DEC-20260501-004 (Dream3R candidate-not-final)
- DEC-20260504-002 (no-all-in any single finalist)
- DEC-20260505-005 (cycle 015 Critic L3 pilot scope; informs T-v02-C5
  + per-adapter checkpoint inventory)

Specs:

- SPEC-20260506-004 (v0.2 architecture; six numbered deltas; INPUT)
- SPEC-20260506-005 (v0.2 ablation plan addendum; ABL-v02-1..9 inform
  Tier 4 ABL harness tasks in roadmap)
- SPEC-20260506-001 (v0.1 architecture; substrate)
- SPEC-20260506-002 (v0.1 ablation plan; v0.1 ABL-1..ABL-10 carry)
- SPEC-20260506-003 (v0.1 comparator map; informs Composer pool
  expansion Delta 5)
- SPEC-20260503-001..003 + SPEC-20260504-001 (4 finalist mechanism
  specs; INPUT for module-level decisions)

Planning artifacts:

- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; 7-expert
  pool + capability_match + routing policy sketch)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; NSA + anchor
  bank design sketch)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; DINOv3 family
  + frozen-backbone design sketch)
- planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (sibling cycle 020
  deliverable; consumes this file)

Code artifacts:

- code/dream3r/PLAN.md (v0.1 user-authored roadmap; preserved
  unchanged; coexists)
- code/dream3r/ source files (READ-ONLY in cycle 020; no modification)

Paradigm / contract:

- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1; capability_match +
  route_regret + signal owner table; informs C5 routing implementation)
- paradigm/RESEARCH_CODE_DISCIPLINE.md (rules 3 Surgical Edits + 5
  Honesty Override; both honored)
- paradigm/ARCHITECTURE_MECHANISM_INTAKE.md (F1..F6 failure modes;
  used in adapter capability inheritance)

Failure modes:

- F-001 (32 MB request-limit; this artifact stays under ~1000 lines)
- F-002 (server topology; all v0.2 code execution server-side)

Cycle log:

- cycles/CYCLE-20260506-005.md (cycle 020 log)

## Open questions

```text
Q-cs-1. Should dinov3_backbone.py be a separate file or merged into
        modules.py?
        Decision: merge into modules.py if implementation stays
        under ~100 lines. Split out if DINOv3 family handling
        grows. Defer to T-v02-C1 implementation reviewer.

Q-cs-2. Should composer_experts/ subdirectory have a base class
        ExpertAdapter, or should each adapter independently implement
        the interface?
        Decision: base class with shared `capability_match` +
        `latency_estimate` + `attention_regime` slots. Per-expert
        forward() implementation independent. Defer concrete base
        class design to T-v02-C5 reviewer.

Q-cs-3. Should v0.2 introduce a new bus.py signal namespace section
        or live in the existing namespace additively?
        Decision: additive only (per B-cs-E bus stability invariant).
        New signals (critic_confidence + permanence_link +
        selected_anchors + memory_retrieval_log) added to existing
        namespace; no namespace section split.

Q-cs-4. ABL-v02-N harness tasks: should each ABL get a dedicated
        harness file, or should harness logic live in ablation/
        subdirectory with one file per ABL family?
        Decision: defer to roadmap T-v02-ABL-N task design. Likely
        ablation/ subdirectory with one file per ABL-v02-N. Open
        for roadmap to refine.

Q-cs-5. CUT3R + Test3R + MoGe-2 + DepthAnything-V2 checkpoints are
        not yet inventoried on dream3r server. Per-adapter
        T-v02-EXPERT-N tasks gated on G_download per checkpoint.
        Should per-checkpoint G_download go cycle-by-cycle (one per
        DEC) or batched (one DEC for all 4 missing checkpoints)?
        Decision: per-checkpoint individual G_download per F-002 +
        DEC-005 (cycle 015 micro-gate pattern). Reviewer authorizes
        each download independently. No batching.

Q-cs-6. Existing C2 Memory in modules.py uses GRU/Mamba per v0.1.
        v0.2 replaces with anchor bank + NSA. Should v0.1 GRU/Mamba
        path be DELETED or PRESERVED as legacy code path under
        a config flag?
        Decision: PRESERVE under config flag for ABL-v02-1
        cosine-top-k variant comparison (v0.1 substrate is one
        comparator point). Mark as legacy in docstring; document
        in §"Pre-existing v0.1 PLAN.md relationship".
```

## Discipline notes

```text
- Surgical Edits (rule 3): this artifact is a NEW file. v0.1 code/
  dream3r/PLAN.md body NOT modified. Pre-existing markdown lint
  warnings on parent files NOT fixed in cycle 020.

- Honesty Override (rule 5): every per-file change carries an
  inline evidence label. NSA-related changes are speculative for
  3R transfer per NSA memo §"Risk / honest limits". DINOv3-S
  backbone swap is paper-derived per DINOV3_C1 memo. Expert pool
  adapter design is engineering-judgment per COMPOSER descriptors.
  Line-of-code estimates throughout this file are inferred (no
  actual code is written in cycle 020).

- F-001 anti-32MB: this artifact stays under ~1000 lines. v0.1 code
  source files (bus.py / modules.py / model.py / losses.py /
  smoke_test.py) NOT Read in cycle 020; PLAN.md summary + INDEX
  summary suffice for planning-level mapping. SPEC-001 / SPEC-004 /
  SPEC-005 / 3 cycle 018 planning files / cycle 019 cycle log
  already in context from prior cycles.

- F-002 server topology: cycle 020 is markdown only. /hdd3/kykt26/
  untouched. Per-task execution (T-v02-A..F + T-v02-ABL-1..9 +
  per-adapter T-v02-EXPERT-N) goes server-side per F-002 rules
  with fresh per-task DEC + per-step micro gates.

- Hard rules from AGENT_MASTER_PROMPT.md section 6 (carried): no
  reproduction; no checkpoint download; no training; no KYKT
  navigation change; no frontend implementation; no thesis
  finalization; no retiring of any non-finalist track. All in
  force.

- DEC-20260501-004 candidate-not-final + DEC-20260504-002 no-all-in
  carried unchanged. v0.2 code structure plans v0.2 candidate code;
  it does NOT commit to v0.2 as final thesis.

- Review surface for other agents: per user instruction
  "其他agent审阅修改 + 文档更新清楚" + "高强度推进", every per-file
  change has a review surface. Modifying review surface in-place
  is NOT allowed (B-cs-F); supersede via fresh DEC + v0.3 addendum.
```

## Version history

```text
v0.2  2026-05-06  cycle 020 S2 deliverable; this file. NEW v0.2 code
                  structure planning artifact. Maps SPEC-20260506-004
                  v0.2 architecture deltas (Delta 1..6) to v0.1 code
                  module changes under code/dream3r/. 5 MODIFIED
                  files (modules.py / model.py / losses.py /
                  smoke_test.py / config.py + train.py); 11-12 NEW
                  files (memory_anchor_bank.py + nsa_attention.py +
                  composer_experts/ subdir with __init__.py + 7
                  adapter files + bench_frame_budget.py + optional
                  dinov3_backbone.py); bus.py + losses.py STABLE
                  (signal namespace + L_total structure carry).
                  Per-file review surface subsection added per user
                  request "其他agent审阅修改" for other-agent
                  handoff. v0.1 PLAN.md preserved unchanged;
                  supersede relationships documented. R-cs-1..8 +
                  B-cs-A..F added. No code touch. Markdown only.
```
