# Dream3R v0.2 implementation roadmap

artifact_id: planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md

date: 2026-05-07

cycle: 020 (S3 deliverable per DEC-20260506-004; cycle 020 spans 2026-05-06 launch → 2026-05-07 closure)

status: v0.2 implementation roadmap (markdown only; planning artifact; NOT a task execution authorization)

honesty_label: every per-task entry carries an inline evidence label + estimated effort (engineering-hours + lines-of-code; both inferred). NSA-related tasks are speculative for 3R transfer per NSA_MEMORY memo. DINOv3-S backbone tasks are paper-derived. Composer expert pool tasks are paper-known per expert + engineering-judgment per adapter. Effort estimates are inferred and will need calibration after first task execution.

linked_artifacts:
- decisions/DEC-20260506-004-cycle-020-launch-code-structure-and-implementation-roadmap.md (parent)
- planning/DREAM3R_V02_CODE_STRUCTURE.md (sibling cycle 020 deliverable; consumed as INPUT)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; six numbered deltas)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2 ablation plan; ABL-v02-1..9 inform Tier 4 ABL harness tasks)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; per-expert adapter inheritance)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; informs T-v02-C2 tasks)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; informs T-v02-C1)
- code/dream3r/PLAN.md (v0.1 user-authored roadmap; preserved unchanged; coexists)

## Identity

This artifact is the v0.2 implementation roadmap. It breaks DREAM3R_V02_CODE_STRUCTURE.md per-file changes into reviewable tasks (T-v02-N) with explicit pre-execution review checklist + post-execution validation checklist for each task. The checklists are the load-bearing other-agent handoff hook per user instruction 2026-05-06.

This file is paired with planning/DREAM3R_V02_CODE_STRUCTURE.md (sibling artifact). The structure file answers WHAT changes; this roadmap answers HOW (per-task breakdown + review surface).

## Approval

Approved scope: per `DEC-20260506-004` (cycle 020 launch + combined code structure + implementation roadmap; user-decided 2026-05-06 with "行" + "高强度推进").

Approved review-surface pattern: per user instruction 2026-05-06 ("其他agent审阅修改" + "你文档更新清楚哈"). Each task has explicit pre-execution review checklist + post-execution validation checklist.

NOT approved by this artifact:

- task execution. Each task carries an explicit execution gate ("requires separate DEC + per-step micro gates + reviewer authorization"); no task is self-authorizing by SPEC-005 / SPEC-004 / DEC-004 / this roadmap alone.
- training, GPU runs, checkpoint download (gated per F-002).
- KYKT navigation change, frontend implementation, demo storyboard promotion past `draft`.
- finalization of Dream3R candidacy.
- retiring of any non-finalist track or v0.1 ABL.
- modification of code/dream3r/PLAN.md (preserved unchanged).
- in-place modification of any task's review checklist (B-roadmap-F; supersede via fresh DEC + v0.3 addendum).

## Scope of v0.2 implementation roadmap

```text
markdown only
candidate-not-final (DEC-20260501-004)
no-all-in (DEC-20260504-002)
architecture-first mainline (DEC-20260506-001)
v0.2 architecture deltas locked (DEC-20260506-002)
v0.2 ablation deltas locked (DEC-20260506-003)
v0.2 code structure planned (DREAM3R_V02_CODE_STRUCTURE.md)
v0.2 implementation roadmap: this file (DEC-20260506-004)
```

This roadmap defines 22 tasks (T-v02-A, T-v02-B, T-v02-C1, T-v02-C2-mem-bank, T-v02-C2-nsa, T-v02-C5, T-v02-EXPERT-1..7, T-v02-D, T-v02-E, T-v02-F, T-v02-ABL-1..9). It does NOT prescribe a single linear execution path; the dependency graph + tier ordering let reviewer authorize any subset that satisfies dependencies.

## Reading order

```text
1. Read this file (you are here).
2. Read DREAM3R_V02_CODE_STRUCTURE.md (sibling; INPUT for per-task
   scope reference).
3. Read DEC-20260506-004 (parent decision; trajectory revision
   context).
4. Reference SPEC-20260506-004 v0.2 architecture (Delta 1..6 anchor)
   as needed.
5. Reference SPEC-20260506-005 v0.2 ablation plan (ABL-v02-1..9
   anchor) as needed for Tier 4 ABL harness tasks.
6. Reference code/dream3r/PLAN.md (v0.1 user-authored roadmap)
   for v0.1 phase-1 done-checkbox context (some checkboxes are
   substrate for v0.2 tasks).
```

## Task taxonomy

```text
Tier 1: Prerequisites (must run first; unblock other tasks)
  T-v02-A   Frame-budget benchmark scaffolding
  T-v02-B   YAML config system

Tier 2: Per-module v0.2 changes (parallelizable)
  T-v02-C1            Perceiver C1 backbone swap
  T-v02-C2-mem-bank   Memory C2 anchor bank (NEW file)
  T-v02-C2-nsa        Memory C2 NSA selection gate (NEW file)
  T-v02-C5            Composer C5 expansion to 7-expert pool
  T-v02-EXPERT-1      MASt3R adapter
  T-v02-EXPERT-2      Fast3R adapter
  T-v02-EXPERT-3      Spann3R adapter
  T-v02-EXPERT-4      CUT3R adapter
  T-v02-EXPERT-5      MoGe-2 adapter
  T-v02-EXPERT-6      DepthAnything-V2 adapter
  T-v02-EXPERT-7      Test3R adapter

Tier 3: Integration + validation
  T-v02-D   model.py bus tick reorchestration
  T-v02-E   smoke_test.py v0.2 update
  T-v02-F   data_dtu.py + train.py for first v0.2 training

Tier 4: Ablation execution scaffolding (one task per ABL-v02-N)
  T-v02-ABL-1   NSA-removal harness
  T-v02-ABL-2   DINOv3 backbone tier harness
  T-v02-ABL-3   Frozen vs unfreeze harness
  T-v02-ABL-4   Composer best-of-N harness
  T-v02-ABL-5   Capability_match measurement harness
  T-v02-ABL-6   Selection-gate signal subsetting harness
  T-v02-ABL-7   Head training schedule harness
  T-v02-ABL-8   Frame-budget benchmark harness
  T-v02-ABL-9   NSA kernel benefit decomposition harness
```

22 tasks total. Total estimated effort across all tasks: ~80-150 engineering-hours (inferred); ~2500-3500 NEW LOC + ~800-1200 MODIFIED LOC.

## Per-task structure (uniform schema)

Each T-v02-N entry below carries:

```text
task_id           short stable identifier
depends_on        list of T-v02-N tasks that must complete first
tier              Tier 1 / Tier 2 / Tier 3 / Tier 4
drives            v0.2 Delta(s) or ABL(s) the task implements
ev_label          paper-known / paper-derived / inferred /
                  speculative / engineering-judgment
estimated_effort  engineering-hours (inferred) + LOC (NEW + MODIFIED)
scope             which files; what changes (cite CODE_STRUCTURE
                  per-file manifest)
inputs            existing files; spec sections; v0.1 PLAN.md
                  checkboxes consumed
outputs           modified files; new files; tests; logs
pre_execution     5-10 items reviewer verifies BEFORE execution
review_checklist  starts (verifies scope is correctly understood)
post_execution    5-10 items reviewer verifies AFTER execution
validation        completes (verifies changes match scope + tests
checklist         pass + no regression)
execution_gate    fresh DEC + per-step micro gates required;
                  reviewer authorization; F-002 server-side
```

## Tier 1: Prerequisites

### T-v02-A: Frame-budget benchmark scaffolding

```text
task_id          T-v02-A
depends_on       (none; Tier 1 prerequisite)
tier             1
drives           Delta 1 (frame budget) + ABL-v02-8 surface
ev_label         inferred (latency on TITAN RTX is unmeasured)
estimated_effort 8-12 engineering-hours; ~200 LOC NEW (bench_frame_budget.py)
                 + ~30 LOC MODIFIED (model.py instrumentation hooks)
                 + ~20 LOC MODIFIED (smoke_test.py latency-toggle test)

scope            Create code/dream3r/bench_frame_budget.py per
                 CODE_STRUCTURE §"NEW: bench_frame_budget.py".
                 Add latency instrumentation hooks to model.py per
                 CODE_STRUCTURE §"MODIFIED: model.py" (opt-in via
                 config; default off; observe-only).
                 Add latency-toggle test to smoke_test.py per
                 CODE_STRUCTURE §"MODIFIED: smoke_test.py".

inputs           CODE_STRUCTURE §"NEW: bench_frame_budget.py" +
                 §"MODIFIED: model.py" + §"MODIFIED: smoke_test.py".
                 SPEC-20260506-004 Delta 1 component allocation.
                 PLAN.md §"当前基线" server env + hardware spec.

outputs          code/dream3r/bench_frame_budget.py (NEW)
                 code/dream3r/model.py (MODIFIED)
                 code/dream3r/smoke_test.py (MODIFIED)
                 + JSON benchmark report consumable by reviewer
                 + tensorboardX log for tail-latency traces

pre_execution_review_checklist:
  [ ] Verify TITAN RTX is the target hardware; refuse to run on
      unsupported hardware without explicit override.
  [ ] Verify scope is "scaffolding" not "production benchmark";
      a production benchmark requires a separate DEC.
  [ ] Verify benchmark covers per-component + end-to-end + lazy-
      path triggering paths.
  [ ] Verify reported numbers structure: p50 / p95 / p99 (not just
      mean).
  [ ] Verify hardware detection logic is explicit (do not silently
      default to A100/H100 numbers from paper).
  [ ] Verify config flag for instrumentation is opt-in default-off.
  [ ] Verify no GPU memory leak in instrumentation hooks (test by
      running benchmark for 60+ seconds continuously).

post_execution_validation_checklist:
  [ ] Verify v0.1 smoke_test path still passes (regression check).
  [ ] Verify benchmark report JSON parses and contains expected
      keys (per_component / end_to_end / lazy_path).
  [ ] Verify reported numbers are TITAN RTX specific (hardware
      name in output).
  [ ] Verify p95 + p99 are within reasonable factors of p50 (not
      orders of magnitude off; sanity check).
  [ ] Verify tensorboardX log is non-empty and has tail-latency
      traces.
  [ ] Verify instrumentation overhead is under 1 ms per frame
      (otherwise it skews benchmark results).
  [ ] Verify CLI flag --bench works without modifying default
      smoke_test behavior.

execution_gate:  fresh DEC required (suggested DEC-yyyymmdd-NNN-
                 t-v02-a-frame-budget-scaffolding); per-step micro
                 gates G_clone (no clone needed; existing repo) /
                 G_install (no install if env stable) / G_run +
                 G_log_use (log policy per F-002). Reviewer
                 authorization required before execution. F-002
                 server-side per /hdd3/kykt26/code/dream3r/.
```

### T-v02-B: YAML config system

```text
task_id          T-v02-B
depends_on       (none; Tier 1 prerequisite)
tier             1
drives           Delta 2 + Delta 3 + Delta 5 + all ABL-v02-N
                 harnesses (config-flag surface)
ev_label         inferred (config schema design is not paper-derived)
estimated_effort 12-16 engineering-hours; ~300 LOC NEW (config.py)
                 + ~50 LOC MODIFIED (model.py loader integration)
                 + 3-5 yaml preset files NEW

scope            Build out code/dream3r/config.py per CODE_STRUCTURE
                 §"MODIFIED: config.py". Define YAML schema with
                 sections: model / backbone / memory / composer /
                 losses / training / ablation. Provide presets:
                 small_v01, small_v02, base_v02, abl_v02_<N> per
                 ABL harness. Per-config validation at load time.

inputs           CODE_STRUCTURE §"MODIFIED: config.py".
                 SPEC-20260506-004 v0.2 architecture for config
                 axis selection (DINOv3 tier; NSA K + k + W; expert
                 pool composition; loss weights; training schedule).
                 SPEC-20260506-005 v0.2 ablation plan for ABL preset
                 overlay design (one preset per ABL-v02-N).

outputs          code/dream3r/config.py (MODIFIED; ~300 LOC)
                 code/dream3r/configs/small_v01.yaml (NEW; v0.1
                                                     baseline preset)
                 code/dream3r/configs/small_v02.yaml (NEW; v0.2
                                                     default preset)
                 code/dream3r/configs/base_v02.yaml (NEW; v0.2
                                                    larger preset)
                 code/dream3r/configs/abl_v02_<N>.yaml (NEW; 9
                                                       ABL preset
                                                       overlays)

pre_execution_review_checklist:
  [ ] Verify schema sections are layered (not flat).
  [ ] Verify preset hierarchy: defaults -> v01 / v02 -> ablation
      overlays.
  [ ] Verify v0.1 yaml files (if any exist from PLAN.md phase 1.2)
      load unchanged after refactor.
  [ ] Verify ABL preset overlays cover all 9 ablations from SPEC-
      005.
  [ ] Verify per-config validation fails loud on unsupported
      combinations (e.g., DINOv3-L on TITAN RTX); no silent
      fallback to a different config.
  [ ] Verify config.load() signature is unchanged (backward-compat).
  [ ] Verify no required field has a sensible default that would
      mask a misconfiguration (defaults should be conservative
      v0.2 settings; explicit when ablation differs).

post_execution_validation_checklist:
  [ ] Verify config.load("small_v02.yaml") returns a valid Config
      object usable by model.py.
  [ ] Verify config.load("small_v01.yaml") still works (backward-
      compat).
  [ ] Verify all 9 ABL preset overlays load without error and
      produce distinct config objects.
  [ ] Verify per-config validation rejects an intentionally
      malformed config (test case).
  [ ] Verify config schema is documented in config.py docstring
      or accompanying CONFIG_SCHEMA.md.
  [ ] Verify v0.1 model code path (small_v01 preset) produces
      identical outputs as before this task (regression check).

execution_gate:  fresh DEC required; per-step micro gates as above.
                 F-002 server-side. Reviewer authorization required.
```

## Tier 2: Per-module v0.2 changes

### T-v02-C1: Perceiver C1 backbone swap

```text
task_id          T-v02-C1
depends_on       T-v02-B (config provides DINOv3 tier flag)
tier             2
drives           Delta 2 (DINOv3-S replaces ViT-L)
ev_label         paper-derived (DINOv3 family well-published;
                 backwards-compat with DINOv2 patterns)
estimated_effort 10-14 engineering-hours; ~80 LOC MODIFIED (modules.py
                 C1 Perceiver class) + ~150 LOC NEW (optional
                 dinov3_backbone.py wrapper)

scope            Modify code/dream3r/modules.py C1 Perceiver class
                 per CODE_STRUCTURE §"MODIFIED: modules.py" §"C1
                 Perceiver class". Optional: split DINOv3 family
                 handling into code/dream3r/dinov3_backbone.py if
                 logic exceeds ~100 lines (decision per Q-cs-1
                 in CODE_STRUCTURE). Re-init heads from scratch
                 (cannot transfer ViT-L head weights). Frozen-
                 backbone default; partial-unfreeze opt-in via
                 config flag (ABL-v02-3 harness).

inputs           CODE_STRUCTURE §"MODIFIED: modules.py" + §"NEW:
                 dinov3_backbone.py".
                 DINOV3_C1_INTEGRATION_MEMO §"Concrete v0.2 design
                 sketch" + §"Migration path from v0.1".
                 T-v02-B config schema for backbone.dinov3_tier +
                 backbone.frozen flags.
                 PLAN.md §"阶段三 Backbone 接入" (v0.1 plan; SUPERSEDED
                 in v0.2 scope per CODE_STRUCTURE §"Pre-existing
                 v0.1 PLAN.md relationship").

outputs          code/dream3r/modules.py (MODIFIED; ~80 LOC delta)
                 code/dream3r/dinov3_backbone.py (NEW; OPTIONAL)
                 + DINOv3-S checkpoint downloaded server-side
                   (gated; requires fresh G_download DEC)

pre_execution_review_checklist:
  [ ] Verify backbone factory selects DINOv3-S by default.
  [ ] Verify -B / -L fallbacks accessible via config flag.
  [ ] Verify DINOv3 weights provenance (Meta hub) + license is
      compatible with project usage.
  [ ] Verify checkpoint download path is server-side (per F-002);
      this task depends on a SEPARATE G_download authorization for
      DINOv3-S checkpoint.
  [ ] Verify head re-init logic is explicit (random init at correct
      dtype/device); does NOT silently inherit ViT-L head shape.
  [ ] Verify patch size 14 (DINOv3 default); not silently
      inheriting 16 from v0.1 ViT-L.
  [ ] Verify frozen-backbone flag respects parameter freezing;
      partial-unfreeze respects top-N block specification.
  [ ] Verify Q-cs-1 decision (merge into modules.py vs split out
      to dinov3_backbone.py); reviewer signs off on file structure
      before implementation.

post_execution_validation_checklist:
  [ ] Verify C1.forward([B, T, 3, 384, 512]) returns dict with
      pointmap_token + confidence + evidence_token shapes consistent
      with v0.1 (additive `dinov3_features` key allowed).
  [ ] Verify head weights are NOT zero (sanity check for re-init).
  [ ] Verify frozen backbone has zero gradients (parameter
      requires_grad=False verification).
  [ ] Verify DINOv3-S forward latency on TITAN RTX matches DINOV3
      _C1 memo target ~20-30 ms / frame (within ~30 percent
      tolerance).
  [ ] Verify model loads successfully via config preset
      "small_v02.yaml".
  [ ] Verify v0.1 path (small_v01 preset; ViT-Base/L) still works
      (regression check).
  [ ] Verify backbone parameter count matches DINOv3 family expected
      values (~22M for -S; ~85M for -B).
  [ ] Verify license documentation in modules.py docstring or
      LICENSE_NOTES.md.

execution_gate:  fresh DEC required (e.g., DEC-yyyymmdd-NNN-t-v02-c1-
                 perceiver-dinov3-s); per-step micro gates including
                 G_download for DINOv3-S checkpoint; F-002 server-side.
                 Reviewer authorization required.
```

### T-v02-C2-mem-bank: Memory C2 anchor bank

```text
task_id          T-v02-C2-mem-bank
depends_on       T-v02-B (config provides anchor bank K + flags)
tier             2
drives           Delta 3 (anchor bank A direction per NSA memo)
ev_label         inferred (storage + eviction policy is implementation;
                 anchor bank concept paper-derived from NSA memo)
estimated_effort 10-12 engineering-hours; ~250 LOC NEW
                 (memory_anchor_bank.py)
scope            Create code/dream3r/memory_anchor_bank.py per
                 CODE_STRUCTURE §"NEW: memory_anchor_bank.py".
                 Bounded K=256 default; LRU eviction with permanence
                 protection; cosine top-k query path (used by ABL-v02-1
                 NSA-removal variant).

inputs           CODE_STRUCTURE §"NEW: memory_anchor_bank.py".
                 NSA_MEMORY_INTEGRATION_MEMO §"Concrete v0.2 design
                 sketch" anchor bank A_t structure.
                 T-v02-B config schema for memory.bank.K + .eviction
                 + .permanence_protect flags.

outputs          code/dream3r/memory_anchor_bank.py (NEW)
                 + unit test in code/dream3r/test_memory_anchor_bank.py
                   (NEW; one-file convention)

pre_execution_review_checklist:
  [ ] Verify K=256 default; configurable via config.
  [ ] Verify cosine top-k path exists independently of NSA path;
      ABL-v02-1 NSA-removal variant uses cosine path.
  [ ] Verify LRU eviction logic does not evict permanence-protected
      entries under any condition (review the eviction algorithm).
  [ ] Verify state_dict / load_state_dict round-trip preserves
      anchor entries + permanence links (review the serialization
      format).
  [ ] Verify shape compat: D-dim of AnchorBank matches C2 evidence
      token D-dim (config-validated at __init__).
  [ ] Verify unit test plan covers: full bank + add new entry +
      verify eviction; permanence-protected at capacity + verify
      NO eviction of protected entry.

post_execution_validation_checklist:
  [ ] Verify unit test passes: bank fills to K; add new entry
      triggers LRU eviction of oldest non-protected.
  [ ] Verify unit test passes: bank fills to K with all permanence-
      protected; add new entry FAILS or rejects (does not evict).
  [ ] Verify state_dict round-trip preserves all entries + freshness
      counters + permanence links.
  [ ] Verify cosine top-k query returns indices in sorted-by-similarity
      order.
  [ ] Verify peak memory of full bank (K=256, D=384) is reasonable
      (~few MB).
  [ ] Verify no GPU memory leak under repeated add+query cycles
      (run for N=10000 iterations as stress test).

execution_gate:  fresh DEC required; F-002 server-side per /hdd3/kykt26/.
                 Reviewer authorization required.
```

### T-v02-C2-nsa: Memory C2 NSA selection gate

```text
task_id          T-v02-C2-nsa
depends_on       T-v02-B (config), T-v02-C2-mem-bank (anchor bank
                 must exist for NSA selected branch)
tier             2
drives           Delta 3 + Delta 4 (NSA three-branch + selection gate)
ev_label         speculative (NSA-to-3R transfer; no published 3R
                 use per NSA memo §"Risk / honest limits")
estimated_effort 12-18 engineering-hours; ~300 LOC NEW
                 (nsa_attention.py) + ~80 LOC MODIFIED (modules.py
                 C2 Memory class to use NSAAttention)
scope            Create code/dream3r/nsa_attention.py per CODE_
                 STRUCTURE §"NEW: nsa_attention.py". Three-branch
                 (compressed + selected + sliding) + gate input
                 mix (critic_confidence + permanence_link). Hardware-
                 aware kernel hook OPT-IN with algorithmic fallback
                 default.

inputs           CODE_STRUCTURE §"NEW: nsa_attention.py" + §"MODIFIED:
                 modules.py" §"C2 Memory class".
                 NSA_MEMORY_INTEGRATION_MEMO §"Concrete v0.2 design
                 sketch".
                 T-v02-B config schema for memory.nsa.k + .compressed
                 + .sliding + .gate_inputs flags.
                 T-v02-C2-mem-bank AnchorBank class (composed in C2).

outputs          code/dream3r/nsa_attention.py (NEW)
                 code/dream3r/modules.py (MODIFIED; C2 Memory class)
                 + unit test in test_nsa_attention.py (NEW)

pre_execution_review_checklist:
  [ ] Verify three branches (compressed / selected / sliding) are
      independently testable.
  [ ] Verify gate input mix supports ABL-v02-6 subsetting (Critic-
      only / Permanence-only / both / neither variants via config).
  [ ] Verify hardware-aware kernel hook is opt-in via config flag;
      algorithmic fallback path is the default.
  [ ] Verify k=8 default; configurable.
  [ ] Verify NSAAttention.forward signature follows NSA paper +
      NSA_MEMORY_INTEGRATION_MEMO §"Concrete v0.2 design sketch".
  [ ] Verify gate signal masking is at INPUT level (forced-zero
      or forced-uniform); not at training level (would conflate
      training signal with inference signal).
  [ ] Verify Q-cs-3 decision honored (signal namespace additive,
      not split).

post_execution_validation_checklist:
  [ ] Verify each of 3 branches has independent unit test (3
      separate test functions).
  [ ] Verify ABL-v02-6 variant config (Critic-only / Permanence-
      only / both / neither) produces 4 distinct gate behaviors.
  [ ] Verify algorithmic fallback path runs without kernel
      compilation (TITAN RTX cu121 default).
  [ ] Verify NSA path returns correct shapes (consistent with
      query shape).
  [ ] Verify gradient flows through gate inputs (test backward
      pass to verify selection gate is differentiable).
  [ ] Verify v0.1 path (no NSA; cosine top-k via T-v02-C2-mem-
      bank) still works (regression check; ABL-v02-1 surface).
  [ ] Verify NSA + algorithmic fallback latency on TITAN RTX is
      reported (for ABL-v02-9 kernel decomp baseline).

execution_gate:  fresh DEC required; F-002 server-side. Reviewer
                 authorization required. NSA kernel availability on
                 cu121 + TITAN RTX is uncertain (per NSA memo
                 §"Risk / honest limits" item 2); reviewer should
                 verify kernel compatibility BEFORE authorizing
                 hardware-aware kernel path.
```

### T-v02-C5: Composer C5 expansion to 7-expert pool

```text
task_id          T-v02-C5
depends_on       T-v02-B (config), T-v02-EXPERT-1..7 (each adapter
                 must exist before Composer can route to it)
tier             2
drives           Delta 5 (7-expert pool per COMPOSER descriptors) +
                 Delta 6 main-claim D
ev_label         engineering-judgment (routing implementation;
                 per-expert paper-known from descriptors)
estimated_effort 8-12 engineering-hours; ~120 LOC MODIFIED
                 (modules.py C5 Composer class) + ~50 LOC
                 (routing logic refactor)

scope            Modify code/dream3r/modules.py C5 Composer class
                 per CODE_STRUCTURE §"MODIFIED: modules.py" §"C5
                 Composer class". Replace v0.1 single-classifier
                 regime detection with 7-expert routing layer.
                 Routing logic: capability_match + critic_confidence
                 + permanence_link -> expert selection. Fallback
                 fixed-routing-policy per COMPOSER routing policy
                 sketch.

inputs           CODE_STRUCTURE §"MODIFIED: modules.py" §"C5
                 Composer class".
                 COMPOSER_CAPABILITY_DESCRIPTORS §"Routing policy
                 sketch (v0.2 default)".
                 T-v02-EXPERT-1..7 adapter classes (composed at
                 __init__).
                 paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1
                 capability_match definition.

outputs          code/dream3r/modules.py (MODIFIED; C5 Composer)

pre_execution_review_checklist:
  [ ] Verify Composer composes 7 ExpertAdapter instances at __init__
      via composer_experts.get_expert(expert_id) factory.
  [ ] Verify routing policy matches COMPOSER_CAPABILITY_DESCRIPTORS
      §"Routing policy sketch (v0.2 default)" exactly; deviations
      need fresh DEC.
  [ ] Verify capability_match values are sourced from
      COMPOSER_CAPABILITY_DESCRIPTORS (not hardcoded; not silently
      drifted).
  [ ] Verify Test3R lazy invocation is OFF the streaming path
      (Composer.forward in streaming bus tick does NOT call
      test3r_adapter.forward()).
  [ ] Verify Composer fallback to fixed-routing-policy if learned
      router is not yet trained (zero-data scenario).
  [ ] Verify expert pool is NOT reduced to a subset silently (all
      7 experts must be in the registry).

post_execution_validation_checklist:
  [ ] Verify Composer.forward returns dict with routed_expert_id +
      expert_outputs keys.
  [ ] Verify all 7 experts are reachable through routing (test
      with synthetic inputs that should route to each).
  [ ] Verify Test3R is not invoked during streaming bus tick
      (instrument Test3R adapter; verify call count == 0 over
      streaming run).
  [ ] Verify Composer respects per-frame budget (when integrated
      with bus tick latency instrumentation; total Composer
      time < 1 ms).
  [ ] Verify capability_match table loaded matches descriptors
      file exactly (md5 or equivalent check at __init__).

execution_gate:  fresh DEC required; F-002 server-side. Reviewer
                 authorization required. ALL 7 T-v02-EXPERT-N tasks
                 must complete BEFORE this task starts (depends_on
                 chain enforced).
```

### T-v02-EXPERT-1..7: Per-expert adapters

For brevity, the 7 adapter tasks share a uniform schema below; per-expert specifics differ in checkpoint provenance + license + native API wrapping.

```text
task_id          T-v02-EXPERT-N (N = 1..7)
                 1 = MASt3R / 2 = Fast3R / 3 = Spann3R / 4 = CUT3R /
                 5 = MoGe-2 / 6 = DepthAnything-V2 / 7 = Test3R
depends_on       T-v02-B (config)
tier             2
drives           Delta 5 (per-expert adapter for 7-pool)
ev_label         paper-known (per-expert innovation + interface) +
                 engineering-judgment (adapter design)
estimated_effort 6-10 engineering-hours per expert; ~150-200 LOC NEW
                 per adapter file
                 (T-v02-EXPERT-3 Spann3R + T-v02-EXPERT-7 Test3R
                  cheaper because checkpoints already on server
                  per cycle 015 inventory + planning/L3_PILOT
                  _SELECTION.md)
                 (T-v02-EXPERT-1 MASt3R: checkpoint already on
                  server per WORK.md inventory)
                 (T-v02-EXPERT-2 Fast3R: checkpoint already on
                  server)
                 (T-v02-EXPERT-4 CUT3R / 5 MoGe-2 / 6 DepthAnything
                  -V2: checkpoints NOT yet inventoried; require
                  fresh G_download per checkpoint)

scope            Per CODE_STRUCTURE §"NEW: composer_experts/
                 subdirectory" §"Per-adapter contents".
                 Wrap expert's NATIVE inference (do NOT re-implement
                 expert). Map outputs to Bus token space (T2 / T3 /
                 T5 / T6 per per-adapter Bus mapping table).

inputs           CODE_STRUCTURE §"NEW: composer_experts/" + per-
                 adapter Bus mapping table.
                 COMPOSER_CAPABILITY_DESCRIPTORS §"Pool members"
                 EXPERT-N section for per-expert innovation_point +
                 input_regime + output_schema + adapter_sketch.
                 Native expert checkpoint (per T-v02-EXPERT-N
                 checkpoint provenance below).

outputs          code/dream3r/composer_experts/<expert>_adapter.py
                 (NEW; one file per expert)
                 code/dream3r/composer_experts/__init__.py (NEW;
                 modified at first T-v02-EXPERT task; updated
                 progressively as more adapters are added)
                 + unit test in test_<expert>_adapter.py (NEW)

pre_execution_review_checklist:
  [ ] Verify adapter wraps expert's NATIVE inference; does NOT
      re-implement (this is a routing layer, not a re-implementation).
  [ ] Verify checkpoint provenance + license documented in adapter
      docstring.
  [ ] Verify checkpoint location on server (cite F-002 path).
  [ ] Verify adapter __init__ raises explicit error on missing
      checkpoint (not silent skip).
  [ ] Verify capability_match values from descriptors match
      adapter class-level values exactly.
  [ ] Verify Test3R adapter (EXPERT-7) has explicit "off-streaming-
      path" annotation in docstring.
  [ ] Verify license compatibility before checkpoint download
      (especially for MASt3R non-commercial license).

post_execution_validation_checklist:
  [ ] Verify adapter loads checkpoint successfully.
  [ ] Verify forward() returns dict with Bus-publishable outputs
      (per adapter's per-expert Bus mapping).
  [ ] Verify per-expert latency on TITAN RTX is within ~30 percent
      of paper-known target (sanity check; not strict measurement
      yet — that is ABL-v02-5).
  [ ] Verify shape compat: adapter output shapes match downstream
      expectations (e.g., MASt3R pointmap shape consistent with
      C2 Memory expectations).
  [ ] Verify unit test exists per adapter (sanity forward + shape +
      latency-budget compliance).
  [ ] Verify adapter is exported from __init__.py expert registry.

execution_gate:  fresh DEC PER EXPERT required (7 separate DECs);
                 per-checkpoint G_download per F-002 (one DEC per
                 missing-checkpoint expert: EXPERT-4 CUT3R + EXPERT-5
                 MoGe-2 + EXPERT-6 DepthAnything-V2 are the gated
                 downloads; the others reuse existing inventory).
                 Reviewer authorization required per expert.
                 Q-cs-5 decision honored (per-checkpoint individual
                 G_download; no batching).
```

## Tier 3: Integration + validation

### T-v02-D: model.py bus tick reorchestration

```text
task_id          T-v02-D
depends_on       T-v02-C1, T-v02-C2-mem-bank, T-v02-C2-nsa, T-v02-C5
tier             3
drives           Delta 3 + Delta 5 (model.py wires the new modules)
ev_label         inferred
estimated_effort 6-10 engineering-hours; ~60 LOC MODIFIED (model.py)

scope            Modify code/dream3r/model.py per CODE_STRUCTURE
                 §"MODIFIED: model.py". Wire C2 NSA selection gate
                 to read critic_confidence + permanence_link.
                 Wire C5 routing context (input regime metadata
                 + capability_match table). Bus tick order
                 unchanged. Add small_v02 + base_v02 presets.

inputs           CODE_STRUCTURE §"MODIFIED: model.py".
                 SPEC-20260506-001 v0.1 §"Read-write protocol per
                 window" (bus tick order MUST NOT change).
                 T-v02-C1..C5 results.

outputs          code/dream3r/model.py (MODIFIED)

pre_execution_review_checklist:
  [ ] Verify bus tick order matches v0.1 SPEC-001 §"Read-write
      protocol per window"; no reordering.
  [ ] Verify latency instrumentation hooks (from T-v02-A) are
      preserved.
  [ ] Verify config keys for v0.1 presets are NOT removed.
  [ ] Verify critic_confidence + permanence_link signal flow
      (written by C4 + C3, read by C2 NSA gate) is wired
      correctly.
  [ ] Verify Composer routing context (capability_match table)
      is passed to C5 via config or bus signal (not hardcoded).
  [ ] Verify small_v02 + base_v02 presets are additive (do not
      overwrite small / small_vit).

post_execution_validation_checklist:
  [ ] Verify Dream3R.forward signature unchanged.
  [ ] Verify Dream3R loads small_v02 preset successfully.
  [ ] Verify v0.1 path (small_vit preset) runs without modification
      (regression check).
  [ ] Verify bus contract log captures critic_confidence +
      permanence_link reads by C2 NSA gate.
  [ ] Verify CR-1..CR-6 gates fire correctly under v0.2 forward
      (smoke_test integration check; T-v02-E covers).
  [ ] Verify v0.2 forward shapes consistent with v0.1 (no
      unexpected dim changes).

execution_gate:  fresh DEC required; F-002 server-side. Reviewer
                 authorization required.
```

### T-v02-E: smoke_test.py v0.2 update

```text
task_id          T-v02-E
depends_on       T-v02-A, T-v02-D (latency hooks + bus tick must exist)
tier             3
drives           Delta 1 + Delta 2 + Delta 3 + Delta 5 (validation)
ev_label         inferred
estimated_effort 6-10 engineering-hours; ~80 LOC MODIFIED (smoke_test.py)

scope            Modify code/dream3r/smoke_test.py per CODE_STRUCTURE
                 §"MODIFIED: smoke_test.py". Add per-module isolation
                 tests for NEW modules (anchor bank + NSA + 7
                 adapters). Add v0.2 end-to-end forward + bus
                 contract log validation + CR-1..CR-6 gate
                 triggering. Retain v0.1 smoke test path.

inputs           CODE_STRUCTURE §"MODIFIED: smoke_test.py".
                 T-v02-C1..C5, T-v02-EXPERT-1..7, T-v02-D outputs.

outputs          code/dream3r/smoke_test.py (MODIFIED; ~80 LOC delta)

pre_execution_review_checklist:
  [ ] Verify v0.1 smoke test path still runs (regression check;
      a smoke_test that fails on v0.1 path is a no-go).
  [ ] Verify per-module isolation tests cover all NEW modules
      (one test per new file; anchor bank + NSA + 7 adapters).
  [ ] Verify end-to-end test verifies bus contract log captures
      expected reads + writes per Delta 3.
  [ ] Verify CR-1..CR-6 gate triggering test uses synthetic
      adversarial input similar to v0.1 ABL-8 (CR-rule ablation).
  [ ] Verify smoke test exit code is informative.

post_execution_validation_checklist:
  [ ] Verify v0.1 smoke_test path passes.
  [ ] Verify v0.2 smoke_test path passes (small_v02 preset).
  [ ] Verify per-module isolation tests all pass.
  [ ] Verify bus contract log non-empty under v0.2 forward.
  [ ] Verify CR-1..CR-6 fire under adversarial input.
  [ ] Verify smoke test runtime under realistic bound (under ~1
      minute on TITAN RTX).

execution_gate:  fresh DEC required; F-002 server-side. Reviewer
                 authorization required. This task is the GATE for
                 declaring v0.2 module integration complete.
```

### T-v02-F: data_dtu.py + train.py for first v0.2 training

```text
task_id          T-v02-F
depends_on       T-v02-A, T-v02-B, T-v02-C1..C5, T-v02-D, T-v02-E
tier             3
drives           Delta 2 + ABL-v02-7 (head training schedule
                 prerequisite)
ev_label         inferred
estimated_effort 16-24 engineering-hours; ~400 LOC NEW (train.py
                 expansion) + ~200 LOC NEW (data_dtu.py) + ~50 LOC
                 (DDP utilities + checkpoint utilities)

scope            Build out code/dream3r/data_dtu.py per PLAN.md
                 §"阶段二 数据准备". Build out code/dream3r/train.py
                 per CODE_STRUCTURE §"MODIFIED: train.py". Multi-
                 stage training schedule support for ABL-v02-7
                 harness. DDP + amp + ckpt + tensorboardX +
                 gradient checkpointing.

inputs           CODE_STRUCTURE §"MODIFIED: train.py".
                 PLAN.md §"阶段二 数据准备" + §"阶段一 1.2 训练基础设施".
                 SPEC-20260506-005 ABL-v02-7 head training schedule
                 ablation requirements.

outputs          code/dream3r/data_dtu.py (NEW or MODIFIED; ~200 LOC)
                 code/dream3r/train.py (MODIFIED; ~400 LOC)
                 + DDP utilities
                 + checkpoint save/resume utilities

pre_execution_review_checklist:
  [ ] Verify DDP correctness via gradient-sync test plan (compare
      2-card vs 1-card outputs over short run).
  [ ] Verify mixed precision does not silently change loss landscape.
  [ ] Verify multi-stage schedule transitions are explicit checkpoint
      boundaries.
  [ ] Verify TensorBoardX log includes per-stage loss curves +
      per-bus-signal traces.
  [ ] Verify checkpoint resume restores all relevant state (model +
      optimizer + scheduler + RNG seeds).
  [ ] Verify DTU DataLoader correctness (frame pairs from cam +
      pair.txt).
  [ ] Verify GT pointmap generation from cam + depth (per PLAN.md).

post_execution_validation_checklist:
  [ ] Verify smoke training run (15 scenes; 2 cards; ~30 minutes)
      converges (loss decreases).
  [ ] Verify DDP run on 2 cards produces same loss curve as 1-card
      (within stochastic variance).
  [ ] Verify checkpoint save then resume produces identical loss
      after resume (deterministic resume).
  [ ] Verify multi-stage schedule transitions (head warmup -> Top-N
      unfreeze) without gradient explosion.
  [ ] Verify TensorBoardX log is non-empty and contains expected
      metrics.

execution_gate:  fresh DEC required (THIS IS A TRAINING-AUTHORIZATION
                 GATE; explicit user approval required per AGENT_
                 MASTER_PROMPT §6 hard rule "no training"); F-002
                 server-side. Reviewer authorization required.
                 NOTE: this task is the FIRST training authorization
                 in the v0.2 trajectory; all prior tasks are
                 markdown / code-review / non-training. The "no
                 training" hard rule is RELAXED for this specific
                 task ONLY upon fresh DEC; subsequent training
                 (ABL-v02-N execution) carries forward authorization.
```

## Tier 4: Ablation execution scaffolding

For brevity, Tier 4 tasks T-v02-ABL-1..9 share a uniform schema. Each ABL-v02-N harness task creates a minimal scaffold to run the corresponding ABL-v02-N from SPEC-20260506-005. Per-ABL specifics are in SPEC-005 §"ABL-v02-N" sections.

```text
task_id          T-v02-ABL-N (N = 1..9)
depends_on       T-v02-F (training driver must exist for any ABL
                 that requires training); plus per-ABL specifics:
                 T-v02-ABL-1: T-v02-C2-nsa + T-v02-C2-mem-bank
                 T-v02-ABL-2: T-v02-C1
                 T-v02-ABL-3: T-v02-C1
                 T-v02-ABL-4: T-v02-C5 + T-v02-EXPERT-1..7
                 T-v02-ABL-5: T-v02-EXPERT-1..7
                 T-v02-ABL-6: T-v02-C2-nsa
                 T-v02-ABL-7: T-v02-C1
                 T-v02-ABL-8: T-v02-A + T-v02-D
                 T-v02-ABL-9: T-v02-C2-nsa
tier             4
drives           ABL-v02-N specific (per SPEC-005)
ev_label         per ABL-v02-N evidence label in SPEC-005
estimated_effort 4-8 engineering-hours per ABL harness scaffold
                 + (separate) compute cost per SPEC-005 §"Compute
                 budget estimate addendum" (~2-400 GPU-hours per
                 ABL execution)

scope            Create ABL-v02-N scaffold (likely under code/dream3r/
                 ablation/<ablation>.py or extension to existing
                 modules). Scaffold provides: variant selection
                 via config flag (per T-v02-B ablation preset
                 overlay); metric collection per SPEC-005 §"Metrics";
                 result reporting in JSON + tensorboardX.

inputs           SPEC-20260506-005 §"ABL-v02-N" (full per-ABL spec).
                 Tier 1-3 task outputs (model + data + training
                 driver).
                 T-v02-B config preset abl_v02_<N>.yaml.

outputs          code/dream3r/ablation/<ablation_id>.py (NEW;
                 likely; final file structure TBD per Q-cs-4 from
                 CODE_STRUCTURE)
                 + per-ABL JSON result report
                 + tensorboardX log per execution

pre_execution_review_checklist (apply per-ABL via SPEC-005 §"ABL-v02-N
review checklist for other agents picking up this ABL"):
  [ ] All items from SPEC-20260506-005 §"ABL-v02-N" review
      checklist subsection (per-ABL).
  [ ] Verify scaffold reuses Tier 1-3 module changes; does NOT
      re-implement.
  [ ] Verify config preset abl_v02_<N>.yaml exists and loads.
  [ ] Verify scaffold dependencies on Tier 2-3 task outputs are
      met (depends_on chain).

post_execution_validation_checklist:
  [ ] Verify ABL execution completed without error.
  [ ] Verify result JSON contains expected metric keys per SPEC-
      005 §"ABL-v02-N" Metrics section.
  [ ] Verify falsification interpretation per SPEC-005 §"ABL-v02-N"
      is honestly applied to the result (no silent re-promotion
      of demoted pillar; no silent re-introduction of dropped
      candidate).
  [ ] Verify result is reproducible (re-run produces same result
      within stochastic tolerance).

execution_gate:  fresh DEC required PER ABL execution (9 separate
                 DECs); per-step micro gates G_run + G_log_use per
                 F-002. Reviewer authorization required.
                 Compute cost per SPEC-005 §"Compute budget estimate
                 addendum" (range ~2-400 GPU-hours; total ~1237
                 GPU-hours for all 9 ABLs; reviewer should chunk
                 execution by tier and signal-criticality).
```

## Task dependency graph (DAG)

```text
Tier 1 prerequisites:
  T-v02-A (frame-budget scaffolding)        [no deps]
  T-v02-B (YAML config)                     [no deps]

Tier 2 per-module (parallelizable after T-v02-B):
  T-v02-C1 (Perceiver DINOv3-S)             [B]
  T-v02-C2-mem-bank (anchor bank)           [B]
  T-v02-C2-nsa (NSA selection)              [B, C2-mem-bank]
  T-v02-EXPERT-1..7 (per-expert adapters)   [B]
  T-v02-C5 (Composer routing)               [B, EXPERT-1..7]

Tier 3 integration:
  T-v02-D (model.py wiring)                 [C1, C2-mem-bank, C2-nsa, C5]
  T-v02-E (smoke_test v0.2)                 [A, D]
  T-v02-F (training driver)                 [A, B, C1..C5, D, E]

Tier 4 ablation harnesses (per-ABL specifics; see Tier 4 schema):
  T-v02-ABL-1 NSA-removal                   [F + C2-nsa + C2-mem-bank]
  T-v02-ABL-2 DINOv3 backbone tier          [F + C1]
  T-v02-ABL-3 Frozen vs unfreeze            [F + C1]
  T-v02-ABL-4 Composer best-of-N            [F + C5 + EXPERT-1..7]
  T-v02-ABL-5 Capability_match measurement  [F + EXPERT-1..7]
  T-v02-ABL-6 Selection-gate signal subset  [F + C2-nsa]
  T-v02-ABL-7 Head training schedule        [F + C1]
  T-v02-ABL-8 Frame-budget benchmark        [F + A + D]
  T-v02-ABL-9 NSA kernel decomposition      [F + C2-nsa]
```

## Recommended execution order

Reviewer-driven; not prescriptive. Suggested order if executing all 22 tasks:

```text
1. T-v02-A           (Tier 1; cheapest; benchmark scaffolding ready)
2. T-v02-B           (Tier 1; YAML config foundation)
3. T-v02-C1          (Tier 2; backbone swap; unblocks training)
4. T-v02-C2-mem-bank (Tier 2; anchor bank; NEW file isolated)
5. T-v02-EXPERT-1, 2, 3 (Tier 2; checkpoints already on server)
6. T-v02-C2-nsa      (Tier 2; NSA selection gate)
7. T-v02-EXPERT-4, 5, 6, 7 (Tier 2; gated G_download per checkpoint)
8. T-v02-C5          (Tier 2; routing layer; depends on all 7
                      adapters being functional)
9. T-v02-D           (Tier 3; model.py wiring; integration point)
10. T-v02-E          (Tier 3; smoke_test v0.2; validates module
                      integration)
11. T-v02-F          (Tier 3; training driver; FIRST training
                      authorization gate)
12-20. T-v02-ABL-8 (frame-budget; cheapest ABL; compliance check)
       T-v02-ABL-2 (DINOv3 tier; backbone choice anchors)
       T-v02-ABL-3 (frozen vs unfreeze)
       T-v02-ABL-7 (head schedule)
       T-v02-ABL-1 (NSA-removal; tests Memory mechanism)
       T-v02-ABL-9 (NSA kernel decomp; only if ABL-1 positive)
       T-v02-ABL-6 (selection gate signal; only if ABL-1 positive)
       T-v02-ABL-5 (capability_match measurement)
       T-v02-ABL-4 (Composer best-of-N; depends on capability_match)
```

This ordering: cheapest Tier 1 first; backbone choice early (anchors training); per-module parallelizable; integration + smoke before training; ablations cheapest-first within Tier 4.

Reviewer may propose alternate order via fresh DEC.

## Compute / wall-clock budget estimate (cycle-020 inferred)

```text
Tier 1 (T-v02-A + T-v02-B):
  Engineering: ~20-28 hours
  Compute    : ~2 GPU-hours total (benchmark calibration only)

Tier 2 (T-v02-C1 + C2-mem-bank + C2-nsa + C5 + EXPERT-1..7):
  Engineering: ~80-110 hours
  Compute    : ~10 GPU-hours total (no training; sanity forwards)

Tier 3 (T-v02-D + E + F):
  Engineering: ~28-44 hours
  Compute    : ~30-50 GPU-hours (T-v02-F first training)

Tier 4 (T-v02-ABL-1..9):
  Engineering: ~36-72 hours scaffolding
  Compute    : ~1237 GPU-hours total (per SPEC-005 budget addendum)

Total:
  Engineering: ~164-254 hours
  Compute    : ~1280 GPU-hours

This is an INFERRED estimate. Calibration after first task execution
(likely T-v02-A) will refine.

Wall-clock estimate (assuming single full-time engineer-equivalent
+ TITAN RTX 24 GB × 4 cards available for compute):
  Tier 1     : ~3-4 days (mostly engineering)
  Tier 2     : ~10-14 days (parallelizable across modules)
  Tier 3     : ~4-6 days (engineering + first training)
  Tier 4     : ~50-70 days (compute-bound; ~1237 GPU-hours / 4 cards
               / 24 hours/day = ~13 days minimum compute; +
               engineering scaffolding overhead)
  Total      : ~67-94 days end-to-end

Wall-clock can be compressed by parallelizing Tier 4 ABLs across
multiple agents + multiple boxes (per F-002 server topology
permits 4-card concurrent use; multi-agent use is a separate
authorization).
```

## Boundaries (v0.2 implementation roadmap delta)

```text
B-roadmap-A.  Cycle 020 produces this roadmap as planning. NO task
              is authorized for execution by this artifact alone.
              Each T-v02-N task carries an explicit execution gate
              ("fresh DEC + per-step micro gates + reviewer
              authorization").

B-roadmap-B.  Per-task review checklists (pre-execution + post-
              execution) are informative for other-agent handoff.
              Modifying them in-place is NOT allowed; supersede via
              fresh DEC + v0.3 addendum (Honesty Override).

B-roadmap-C.  Task dependency graph is binding: a task with
              unsatisfied depends_on MUST NOT be authorized for
              execution. Reviewer verifies depends_on satisfaction
              before authorizing.

B-roadmap-D.  v0.1 PLAN.md remains canonical for v0.1 implementation.
              v0.2 roadmap supersedes v0.1 PLAN.md only for v0.2-
              specific tasks (per CODE_STRUCTURE §"Pre-existing v0.1
              PLAN.md relationship"). Reviewer should consult both.

B-roadmap-E.  Effort estimates are inferred at cycle 020 time.
              First task execution (likely T-v02-A) calibrates
              the estimate. Subsequent estimates may be revised
              via fresh DEC + v0.3 addendum.

B-roadmap-F.  No task in this roadmap re-introduces dropped
              candidates (Kimi-KDA / VGGT / MapAnything). Pool
              composition per CODE_STRUCTURE §"NEW: composer_experts/"
              is fixed for v0.2; alternatives go via v0.3 addendum.

B-roadmap-G.  T-v02-F (first training authorization) is the
              "no training" hard rule first relaxation. Subsequent
              training authorizations (ABL-v02-N execution) carry
              forward via per-ABL fresh DECs. Hard rule is per-task
              gate, not blanket revocation.
```

## Linked artifacts (full list)

Decisions:

- DEC-20260506-004 (cycle 020 launch + this roadmap scope; parent)
- DEC-20260506-003 (cycle 019 ablation plan v0.2 addendum; informs
  Tier 4 ABL scaffolding scope)
- DEC-20260506-002 (cycle 018 v0.2 architecture deltas)
- DEC-20260506-001 (mainline architecture-first)
- DEC-20260501-004 (Dream3R candidate-not-final)
- DEC-20260504-002 (no-all-in any single finalist)
- DEC-20260505-005 (cycle 015 Critic L3 pilot; per-step micro gate
  pattern carried forward to per-task DECs)

Specs:

- SPEC-20260506-004 (v0.2 architecture; six numbered deltas; INPUT)
- SPEC-20260506-005 (v0.2 ablation plan; ABL-v02-1..9 inform Tier 4
  task scopes)
- SPEC-20260506-001..003 (v0.1 architecture / ablation / comparator;
  substrate)
- SPEC-20260503-001..003 + SPEC-20260504-001 (4 finalist mechanism
  specs)

Planning artifacts:

- planning/DREAM3R_V02_CODE_STRUCTURE.md (sibling cycle 020
  deliverable; INPUT for per-task scope reference)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (per-expert
  capability table)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (informs T-v02-C2 tasks)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (informs T-v02-C1)
- planning/L3_PILOT_SELECTION.md (informs T-v02-EXPERT-N checkpoint
  inventory awareness)

Code artifacts:

- code/dream3r/PLAN.md (v0.1 user-authored roadmap; coexists)
- code/dream3r/ source files (referenced; not modified by cycle 020)

Paradigm / contract:

- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1 capability_match;
  Composer routing definition)
- paradigm/RESEARCH_CODE_DISCIPLINE.md (rules 3 + 5)

Failure modes:

- F-001 (32 MB request-limit; this roadmap stays under ~1100 lines)
- F-002 (server topology; all task execution server-side)

Cycle log:

- cycles/CYCLE-20260506-005.md (cycle 020 log)

## Open questions

```text
Q-roadmap-1. Are 22 tasks the right granularity, or should some be
             decomposed further? Specifically:
             - T-v02-F (training driver) is the largest task at
               16-24 hours; could split into T-v02-F-data
               (data_dtu) + T-v02-F-train (train.py) for clearer
               review.
             - T-v02-EXPERT-1..7 are 7 separate tasks; could batch
               into 2-3 DECs (e.g., on-server experts batched;
               off-server experts per DEC) — but Q-cs-5 decision
               in CODE_STRUCTURE forbids batching.
             Decision: defer to first execution-cycle launch DEC
             after reviewer feedback.

Q-roadmap-2. Should there be cross-task gating where T-v02-N
             completion REQUIRES a reviewer sign-off before
             T-v02-(N+1) authorization, or just dependency
             satisfaction (depends_on)?
             Decision: for Tier 1+2 modules, depends_on satisfaction
             is sufficient. For Tier 3+ integration and Tier 4
             ablations, reviewer sign-off on prior task results is
             required (per execution-cycle launch DEC pattern).

Q-roadmap-3. The first task execution (likely T-v02-A) will
             calibrate effort estimates. Should the roadmap be
             revised after the first task to refine estimates?
             Decision: yes; v0.3 addendum after T-v02-A completes.
             Per B-roadmap-E.

Q-roadmap-4. ABL-v02-5 capability_match measurement updates
             COMPOSER_CAPABILITY_DESCRIPTORS values. Is the
             update path "fresh DEC + v0.3 update of descriptors
             file" sufficient, or should it be a separate
             revision-tracking mechanism (e.g., capability_match
             measurement log)?
             Decision: fresh DEC + v0.3 update of descriptors
             file is sufficient for cycle 020. Future cycle may
             refine to a more-structured measurement log if
             multiple measurement passes accumulate.

Q-roadmap-5. T-v02-F (training driver) is the first training
             authorization. Should it be a single DEC, or split
             into G_train_smoke (small-scale validation) +
             G_train_production (full training) micro-gates?
             Decision: split into G_train_smoke (cheap; ~30 min;
             validates loss converges) + G_train_production
             (gated on smoke success; full DTU 15-scene per
             PLAN §"阶段四 第一轮训练"). Pattern matches cycle
             015 Critic L3 pilot's micro-gate chain.
```

## Discipline notes

```text
- Surgical Edits (rule 3): this artifact is a NEW file. v0.1 code/
  dream3r/PLAN.md NOT modified. Pre-existing markdown lint warnings
  on parent files NOT fixed in cycle 020.

- Honesty Override (rule 5): every per-task entry carries an inline
  evidence label + estimated effort. NSA-related tasks are
  speculative for 3R transfer. DINOv3-S backbone tasks are paper-
  derived. Effort estimates are inferred at cycle 020 time;
  calibration after first task execution. Trajectory revision
  preserved in DEC-20260506-004 §"Why this matters".

- F-001 anti-32MB: this artifact stays under ~1100 lines. Source
  code files NOT Read; CODE_STRUCTURE summary suffices for per-
  task scope reference. SPEC-005 ABL-v02-1..9 referenced by
  section anchor, not re-derived.

- F-002 server topology: cycle 020 is markdown only. /hdd3/kykt26/
  untouched. Per-task execution (T-v02-A..F + T-v02-EXPERT-1..7
  + T-v02-ABL-1..9) goes server-side per F-002 with fresh per-task
  DEC + per-step micro gates.

- Hard rules from AGENT_MASTER_PROMPT.md section 6 (carried): no
  reproduction; no checkpoint download; no training; no KYKT
  navigation change; no frontend implementation; no thesis
  finalization; no retiring of any non-finalist track. T-v02-F is
  the first task that relaxes "no training" hard rule (per
  B-roadmap-G); relaxation is per-task DEC, not blanket revocation.

- DEC-20260501-004 candidate-not-final + DEC-20260504-002 no-all-in
  carried unchanged. Each task tests v0.2 candidate code; tasks
  do NOT commit to v0.2 as final thesis.

- Review surface for other agents: per user instruction
  "其他agent审阅修改 + 文档更新清楚" + "高强度推进", every per-task
  entry has pre-execution review checklist + post-execution
  validation checklist. These are the primary handoff hooks for
  review agents. Modification path = fresh DEC + v0.3 addendum
  (B-roadmap-B); no in-place edits to checklists.
```

## Version history

```text
v0.2  2026-05-07  cycle 020 S3 deliverable; this file. NEW v0.2
                  implementation roadmap. 22 tasks (T-v02-A, T-v02-B,
                  T-v02-C1, T-v02-C2-mem-bank, T-v02-C2-nsa, T-v02-
                  C5, T-v02-EXPERT-1..7, T-v02-D, T-v02-E, T-v02-F,
                  T-v02-ABL-1..9) across 4 tiers. Per-task pre-
                  execution review checklist + post-execution
                  validation checklist subsections per user request
                  "其他agent审阅修改" for other-agent handoff.
                  Total estimated effort ~164-254 engineering-hours
                  + ~1280 GPU-hours compute (inferred TITAN RTX).
                  Wall-clock estimate ~67-94 days end-to-end (single
                  agent + 4-card concurrent compute). Task dependency
                  graph DAG documented. Recommended execution order
                  cheapest-first within tier; reviewer-revisable
                  via fresh DEC. T-v02-F is the first training
                  authorization gate per B-roadmap-G. v0.1 PLAN.md
                  preserved unchanged; supersede relationships
                  documented in CODE_STRUCTURE §"Pre-existing v0.1
                  PLAN.md relationship". B-roadmap-A..G + Q-roadmap-
                  1..5 added. No code touch. Markdown only.
```
