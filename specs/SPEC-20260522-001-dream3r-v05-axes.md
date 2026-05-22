# Dream3R v0.5 axes spec — closing the v0.4 stub / fallback / proxy surface

spec_id: SPEC-20260522-001

spec_kind: architecture axes spec; candidate axes only, not approved deltas

parent_spec: SPEC-20260506-004 (Dream3R architecture v0.2; v0.3 addendum SPEC-20260508-001 closed C2)

parent_status_doc: `ARCHITECTURE_V04_STATUS.md` (v0.4 closure round, 2026-05-22) — defines what is real / fallback / stub / proxy / contract-only entering v0.5

parent_companion_doc: `code/dream3r/SOTA_FEATURE_MATRIX.md` (W20 second pass, 2026-05-22) — Gap Report items consumed below

parent_decision: none yet (this spec proposes axes; each axis closure requires its own DEC)

date: 2026-05-22

cycle: 043 candidate (sequel to cycle 042 proposal closeout; not yet cycle-logged at write time)

status: v0.5 axes draft, candidate-not-final per DEC-20260501-004 (operating principle: candidates require independent DEC + evidence before status promotion)

honesty_label: every axis below carries an explicit evidence label, a `closes_iff` criterion, and a `does_not_promise` clause. The v0.5 layer is additive to v0.4 by default; any v0.3 / v0.4 code mutation is called out per-axis.

linked_artifacts:

- `ARCHITECTURE_V04_STATUS.md` — per-axis [x] / [~] / [ ] checklist this spec reads from
- `ARCHITECTURE_V04_AGENT_PROMPT.md` — v0.4 closure authority (still active)
- `code/dream3r/SOTA_FEATURE_MATRIX.md` — Gap Report § feeds A2 / A4 / A6 / A8
- `code/dream3r/NEXT_PHASE_ROADMAP.md` — W19-W27 referenced, not duplicated
- `code/dream3r/contracts.py`, `repair.py`, `orchestrator.py` — v0.4 additive layer; v0.5 extends, does not rewrite
- `code/dream3r/composer_experts/method_profiles.py` — canonical 7-expert profile; A2 / A4 update this file
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 — CR-1..CR-6 unchanged in v0.5; new signals (if any) become CR-7+
- `planning/WORK_RISK_REGISTER.md` — R-4DGS-LIC-1 / R-EXT-PRIOR-1 / R-OOD-1 referenced
- `units/REPRODUCTION_READINESS_MATRIX.md` — readiness signal for each adapter axis
- `specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md` — C2 memory v0.3 baseline; v0.5 does NOT redo this

---

## Identity

This spec proposes the **axes** along which Dream3R should be promoted from v0.4 (architecture closure) to v0.5 (closing the explicit stub / fallback / proxy / contract-only surface left by v0.4).

It is **not** an approval to:

- modify the v0.3 main forward (`model.py`, `modules.py`, `bus.py`, `anchor_bank.py`, `nsa_attention.py`, `composer_experts/*`) — these remain byte-identical baselines unless an axis closure DEC explicitly authorizes a change.
- ratify any axis closure. Each axis closure requires its own DEC plus the listed authorizations (F-002 server work, checkpoint downloads, etc.).
- claim that any axis below has been validated. Every closure is conditional on a future evidence pass.

The spec uses the term **axis** rather than **delta** to make this candidate-not-final status explicit. Promotion from axis-draft → axis-approved requires a per-axis DEC referencing `closes_iff` below.

## v0.4 → v0.5 boundary recap

Entering v0.5, the following surfaces are explicitly **open** per `ARCHITECTURE_V04_STATUS.md`:

```text
Stub:
  Perception DINOv3-S backbone (backbone_status.backend == "stub")

Deterministic fallback (5 / 7 Composer adapters):
  Spann3R / CUT3R / MoGe-2 / DepthAnything / Test3R adapters

Real-wired but no local checkpoint (2 / 7 Composer adapters):
  MASt3R (load path wired, no ckpt locally)
  Fast3R (load path wired, local conda blocked on omegaconf)

Proxy (not promoted to final asset):
  Permanence dynamic_mask_proxy

Contract-only (NOT in main forward by design):
  GaussianHead / 4DGS

Comparator-only structural gap:
  VGGT (cycle 014 CASE-COMPOSER-05 capability_card v2.2 gap)
  STream3R (W26 design study not started)
  Memory primitive comparators (Point3R / Mem3R / LONG3R / LoGeR / PAS3R / FILT3R / OVGGT / LongStream / SLAM3R)
  Test-time mechanism comparators (tttLRM, TTT3R)

Behavioral observation needing follow-up:
  NSA sliding branch weight 0.000 on KITTI smoke (`RECENT_PROGRESS.md` Tier 2)

Internal-only repair path:
  v0.4 RepairExecutor actions 1 / 2 use internal model.forward rerun, never Test3R-as-off-path
```

v0.5 is the spec layer that decides which of these are closed in the next development sprint and which remain comparator-only or contract-only by design.

## Approval and boundaries

Approved in this spec (writes only):

- the **list** of v0.5 axes and their `closes_iff` criteria below.
- the **non-modification** of v0.3 main forward as a default policy.
- the **additive** posture for the v0.4 layer (contracts / repair / orchestrator).

Not approved by this spec:

- server code edit
- model run
- training or fine-tuning
- checkpoint download
- KYKT navigation or frontend change
- final thesis selection
- claim that any v0.5 axis has been closed empirically
- merging 4DGS / GaussianHead into the main forward (axis A7 below explicitly stays guarded)
- promoting `dynamic_mask_proxy` to a D2 final asset (axis A3 explicitly conditions promotion on evidence)

Evidence labels used per axis:

```text
code-observed:
  state directly visible in current code under code/dream3r/.

server-observed:
  state visible only on /hdd3/kykt26/code/dream3r/ per RECENT_PROGRESS.md;
  not reproducible locally.

paper-proven:
  source paper / project page provides the mechanism specification.

inferred:
  Dream3R synthesis; not directly grounded in code or paper.

unknown:
  not measured and not derivable from current artifacts.
```

A `closes_iff` clause is a sufficient condition list; satisfying it is necessary before promoting the axis to "closed" via DEC. Insufficient evidence keeps the axis open.

---

## Axis A1. DINOv3-S backbone real integration

Surface category: Perception (C1) backbone

Current v0.4 state (code-observed): `Perceiver.__init__` accepts `backbone_type="dinov3"`; with `use_backbone=True` the perceiver tries `torch.hub` then `timm`, and on local Windows / Python 3.13 both fail because `timm` is not installed and `torch.hub` has no DINOv3 cache. `backend_status` honestly reports `is_loaded=False`, `backend="stub"`. No false `real` claim is emitted.

Gap: DINOv3-S has no concrete release pinned in our codebase. The string `"dinov3"` is a placeholder.

`closes_iff`:

1. A specific DINOv3 release (e.g., DINOv3-S/14 from a named source URL) is recorded in `registry/source_registry.md` as a new `SRC-2026-*` row with `code` evidence.
2. `Perceiver._try_load_backbone("dinov3")` resolves the recorded checkpoint deterministically, either via `torch.hub` (if the upstream provides a hub spec) or via a documented manual download path under `/hdd3/kykt26/`.
3. `backend_status["backend"] == "real"` on at least one server tick with the loaded backbone, asserted by a new `tests/test_dinov3_backbone.py` integration test (server-only, no local fallback required).
4. The `RECENT_PROGRESS.md` Tier 1 ledger gains a "DINOv3-S backbone real" row.

Required actions: (a) DINOv3 release survey + SRC row add; (b) `timm` install or hub spec under `dream3r` conda env on server; (c) `Perceiver._try_load_backbone` extension; (d) integration test; (e) F-002 server authorization for steps (b)-(d).

Dependencies: none from other v0.5 axes. Blocks: nothing critical, but every quality experiment downstream will use whichever backbone is loaded.

Does_not_promise: that DINOv3-S outperforms DINOv2 on KITTI smoke; v0.5 closes the integration axis, not the quality axis.

Evidence label entering v0.5: `code-observed` (stub status) + `paper-proven` (DINOv3 family exists) — but no specific release pinned.

## Axis A2. Composer adapter real-checkpoint loading

Surface category: Composer (C5) expert adapters

Current v0.4 state (code-observed): 7 adapters registered. MASt3R + Fast3R have real loader paths wired (`load_checkpoint` method + repo discovery); Spann3R / CUT3R / MoGe-2 / DepthAnything / Test3R return deterministic fallback. `method_profiles.py` correctly labels 4 of these as `"stub"`. v0.4 `ComposerDecision.backend_status` honestly reports `"fallback"` / `"stub"` per adapter at forward time.

Gap: 5 of 7 adapters are fallback-only. Even MASt3R + Fast3R have no local checkpoint resolved; Fast3R is additionally blocked on `omegaconf` in the dream3r conda env per `WORKFLOW_STATUS.md`.

`closes_iff`:

1. Each of the seven adapters has a real `load_checkpoint(path)` path implemented (not just declared) — code-observed.
2. On the server, at least one tick per adapter produces `ComposerDecision.backend_status[expert_id]["backend"] == "real"`, asserted by a per-adapter integration test (server-only).
3. Fast3R conda env unblocked: `omegaconf` resolution recorded as a one-line fix in `WORKFLOW_STATUS.md` Track A.
4. `composer_experts/method_profiles.py` `implementation_status` field updates from `"stub"` to `"checkpoint_available"` (or to a more granular tier) for each closed adapter — and the update is consistent with code, not intent.
5. `SOTA_FEATURE_MATRIX.md` Implementation Status Roll-Up is regenerated; the `deterministic fallback` count drops accordingly.

A2 may close per-adapter rather than all-at-once. Each per-adapter closure is its own sub-DEC.

Required actions: (a) survey checkpoint availability per adapter (server-side); (b) implement `load_checkpoint` per adapter; (c) per-adapter integration test; (d) `omegaconf` env fix for Fast3R; (e) F-002 server authorization; (f) **no checkpoint download authorization granted by this spec** — downloads must be approved separately per the `WORKFLOW_STATUS.md` "Blocked Until User Decision" list.

Dependencies: A4 (VGGT) is a parallel axis that does NOT block A2; they touch the same module but different rows. If A2 closes for some subset of adapters and A4 adds VGGT as the 8th, both can land in the same DEC.

Does_not_promise: that real-checkpoint adapters beat the deterministic fallback on KITTI smoke (the fallback is image-derived deterministic; real models may regress on this proxy until real evaluation lands per W21 / W23).

Evidence label entering v0.5: `code-observed` (fallback status) + `paper-proven` (each backbone exists per `SRC-*`).

## Axis A3. Permanence dynamic_mask promotion (`dynamic_mask_proxy` → final D2)

Surface category: Permanence (C3)

Current v0.4 state (code-observed): `PermanenceOutput.dynamic_mask_proxy` field is explicitly named `proxy`; docstring says "proxy". Final D2 dynamic mask is NOT claimed. `suppress_static_write` (CR-2) is the only consumer that actually gates v0.3 Memory write-decision; the proxy mask is currently a derived bool from `dynamic_logits`, not an independent asset.

Gap: the design space for promoting the proxy to a final D2 asset is unspecified. Existing finalist spec `SPEC-20260503-003-dynamic-object-permanence.md` defines the dynamic-permanence axis but does not pin what counts as a final D2 asset vs a transient proxy.

`closes_iff`:

1. A concrete promotion criterion is written into `SPEC-20260503-003` as a delta addendum: what evidence promotes a transient `dynamic_mask_proxy` into a D2 final mask (e.g., temporal consistency over N windows, identity_consistency above threshold, agreement with SAM 2 / CoTracker / SpatialTracker priors per `SPINE_PERMANENCE.md` advanced reading).
2. The promotion criterion is exercised on at least one real-data window (KITTI dynamic subset or equivalent) and recorded in `cycles/` log.
3. v0.4 `PermanenceOutput` is extended (additive): a new `dynamic_mask_final` field is added alongside `dynamic_mask_proxy`; both fields coexist for one transition cycle to prevent silent semantic drift.
4. The CR-2 handoff to Memory is upgraded to consume `dynamic_mask_final` when available, falling back to `dynamic_mask_proxy` otherwise; the CR-2 contract revision is logged in `CROSS_SPEC_SIGNAL_CONTRACT.md` as v2.2 or v3.

Required actions: (a) SPEC-20260503-003 addendum; (b) `PermanenceOutput` field add; (c) cross-spec contract revision; (d) one real-data window evaluation; (e) F-002 server authorization.

Dependencies: A6 (NSA sliding branch utility) is independent. A3 has read interaction with A5 (Test3R off-path) — if Test3R becomes a Critic-triggered verification path, its output could feed dynamic_mask promotion. The interaction is documented but not required.

Does_not_promise: that the promoted mask is correct on dynamic scenes. v0.5 closes the contract axis (what is a D2 final mask), not the quality axis (how often the proxy is right).

Evidence label entering v0.5: `code-observed` (proxy field exists, naming honest) + `inferred` (promotion criterion design).

## Axis A4. VGGT adapter + capability_card v2.2

Surface category: Composer (C5) + cross-spec signal contract

Current v0.4 state (code-observed + cycle 014 case): VGGT (SRC-2026-015) is not a Composer expert. Cycle 014's `CASE-COMPOSER-05` explicitly documents this gap as a per-card addendum, not a contract revision. `method_profiles.py` has 7 entries; VGGT would be the 8th.

Gap: VGGT is a feed-forward many-view profile that does not fit cleanly into Fast3R's row in `capability_card` schema v2.1. Adding it requires either: (a) capability_card schema v2.2 with finer feed-forward many-view distinction, or (b) repurposing Fast3R's row, which would be a regression.

`closes_iff`:

1. `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` capability_card schema is bumped to v2.2 with the additional axis (feed-forward many-view sub-profile or equivalent) drafted in cycle 014's queue.
2. A new `vggt_adapter.py` is added under `composer_experts/` with the same `ExpertAdapter` ABC; `method_profiles.py` gains a `"vggt"` entry.
3. `ExpertRegistry.register_all_defaults` is extended to register the 8th adapter.
4. v0.4 `ComposerDecision.backend_status` now reports an 8th row.
5. At least one server tick confirms `backend == "real"` for VGGT with a loaded checkpoint, asserted by `tests/test_vggt_integration.py`.
6. `SOTA_FEATURE_MATRIX.md` Section 2 row for VGGT moves from `comparator-only` to `real-wired`.

Required actions: (a) capability_card schema revision; (b) new adapter implementation; (c) registry extension; (d) integration test; (e) checkpoint resolution per A2 rules; (f) F-002 server authorization.

Dependencies: A4 touches `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` and may interact with A2's per-adapter closure batching. If A2 closes for MASt3R + Fast3R and A4 adds VGGT, capability_card v2.2 must be the contract revision that lands first.

Does_not_promise: that VGGT outperforms Fast3R or MASt3R on KITTI smoke. v0.5 closes the contract axis (capability_card v2.2) and the adapter axis (adapter exists, loads, returns ExpertOutput), not the quality axis.

Evidence label entering v0.5: `code-observed` (no adapter yet) + `paper-proven` (VGGT exists per SRC-2026-015).

## Axis A5. Test3R as Critic-triggered off-path (not only Composer dispatch)

Surface category: Critic (C4) + RepairExecutor (v0.4) + Composer (C5)

Current v0.4 state (code-observed): the v0.4 `RepairExecutor` actions 1 (local_rerun) and 2 (window_rerun) inject `recommended_action` into the bus and re-call `model.forward`. This deepens CR-3 retrieval and zeroes critic_confidence respectively. **Neither action invokes Test3R explicitly.** Test3R is wired only as a Composer expert (currently fallback), which is reached via `selected_expert` routing, not Critic dispatch.

Gap: the design intent stated in `SPINE_CRITIC.md` and `ATTENTION_RESEARCH_MATRIX.md` ("critic-triggered slow verification path") is not realized at the code level. Test3R-as-an-off-path is comparator-only despite being adapter-registered.

`closes_iff`:

1. A new v0.4 `RepairExecutor` action code 4 (or a documented re-use of action 3 reroute_hint with a special expert target) is defined for "Critic-triggered Test3R off-path verification".
2. The contract revision is recorded in `contracts.py` `REPAIR_ACTION_NAMES`; tests assert action 4 dispatches Test3R specifically (or the documented reroute target).
3. `RepairExecutor._test3r_offpath` (or equivalent) calls `model.composer.dispatch("test3r", images)` once with the latest perception output and returns the result as a verification ExpertOutput; the result is recorded in `repair_action_log` separately from the main `ReconstructionOutput.expert`.
4. Test3R adapter has a real `load_checkpoint` path (closes part of A2 for Test3R specifically).
5. At least one server tick shows the off-path firing on a high-conflict window, recorded in a new `cycles/` log entry.

Required actions: (a) v0.4 action code extension; (b) RepairExecutor extension; (c) Test3R adapter real path (intersection with A2); (d) integration test; (e) F-002 server authorization; (f) Test3R checkpoint resolution per A2 rules.

Dependencies: requires A2 partial closure for Test3R. Does not require A4. May interact with A3 if Test3R verification feeds dynamic_mask promotion.

Does_not_promise: that Test3R off-path improves Critic precision/recall. v0.5 closes the wiring axis, not the calibration axis (which is W24 in `NEXT_PHASE_ROADMAP.md`).

Evidence label entering v0.5: `code-observed` (no off-path wiring) + `inferred` (this is the documented design intent).

## Axis A6. NSA sliding branch utility verification

Surface category: SpatialMemory (C2) NSA

Current v0.4 state (server-observed): KITTI smoke `RECENT_PROGRESS.md` Tier 2 reports NSA branch weights `compressed 0.3927 / selected 0.6073 / sliding 0.000`. The sliding branch is allocated 0 weight on this window. The branch fusion code (`nsa_attention.py` branch routing) is unchanged.

Gap: this is not a bug — it may be the correct sparse routing under the window length (2 windows of `2011_09_26_drive_0001_sync_02`). But it is also possible the sliding branch is starved by a training-free bias. Without longer-sequence evidence, we cannot distinguish.

`closes_iff`:

1. The same KITTI smoke is rerun on a window count ≥ 8 (rather than 2) on the server.
2. NSA branch weights are reported per window; the cycle log explicitly states whether the sliding branch ever fires (weight > 0.05 on any window).
3. If the sliding branch consistently stays at 0, a deliberate routing investigation is recorded: either (a) confirm the current routing is correct under longer sequences, or (b) identify a training-free bias and decide whether to fix it.
4. The result is folded back into `SOTA_FEATURE_MATRIX.md` Section 6 NSA row "Remaining gap" cell.

Required actions: (a) longer KITTI window run on server; (b) cycle log entry; (c) optional `nsa_attention.py` routing investigation (does NOT require modification by default — investigation may conclude "no change needed").

Dependencies: none from other v0.5 axes.

Does_not_promise: that the sliding branch is useful. v0.5 closes the observation axis (we have evidence under longer sequences), not the design axis (whether to remove or re-weight the branch).

Evidence label entering v0.5: `server-observed` (0.0 weight on 2-window KITTI) + `unknown` (longer-sequence behavior).

## Axis A7. GaussianHead / 4DGS conditional main-forward entry

Surface category: GaussianHead + Composer (C5)

Current v0.4 state (code-observed): `gaussian_head.py` provides a tensor-only contract. `ARCHITECTURE_V04_STATUS.md` Section 7 lists it as `contract-only` and explicitly says "4DGS / GaussianHead was NOT pulled into the v0.4 main forward per the prompt's exclusion rule." This is a deliberate non-decision, not an oversight.

Gap: there is no spec for **when** GaussianHead should enter the main forward. The roadmap's W27 lists prerequisites (renderer install, license audit) but not a contract for the architectural integration itself.

`closes_iff` (this axis intentionally keeps closure conditional and high-bar):

1. A renderer is approved by user DEC (per `WORKFLOW_STATUS.md` "Blocked Until User Decision": "any new heavy install").
2. License audit row `R-4DGS-LIC-1` in `WORK_RISK_REGISTER.md` resolves to a specific renderer choice with documented license compatibility.
3. A v0.5 architecture addendum (separate spec file, not this one) defines: (a) where in `V04Pipeline.forward` the GaussianHead would be invoked; (b) which AnchorBank stable entries are promoted to persistent Gaussians; (c) how photometric loss flows back into training (or whether v0.5 is inference-only Gaussian output).
4. A real renderer dispatch tick produces a non-zero rendered tensor, asserted by `tests/test_gaussian_render_real.py` (the existing `test_gaussian_render_contract.py` is shape-only).
5. v0.4 `ReconstructionOutput` is extended (additive) with a `rendered_image` field; the field is `None` when the renderer is absent.

**This spec does not approve A7 closure.** A7 is listed as an axis for completeness — its `closes_iff` is the union of W27 prerequisites plus an explicit user DEC.

Required actions: (a) renderer approval DEC from user; (b) license audit closure; (c) separate v0.5 addendum spec; (d) implementation; (e) integration test; (f) F-002 server authorization.

Dependencies: A7 is independent of A1-A6, A8 in spec terms. In practice, it is downstream of W21-W23 (real-data evidence) because rendering without a calibrated geometry baseline is premature.

Does_not_promise: that v0.5 will close A7. The likely v0.5 outcome for A7 is "remains contract-only, no change."

Evidence label entering v0.5: `code-observed` (contract exists) + `inferred` (integration design).

## Axis A8. tttLRM-style long-context A1 sub-action design

Surface category: Memory (C2) state-update policy + RepairExecutor (v0.4) interface

Current v0.4 state (paper-proven for tttLRM; code-observed for Dream3R): tttLRM (SRC-2026-011) defines test-time training at long-context / sequence scale, with a state-update rule that targets long-sequence regression errors rather than per-pair residuals. Dream3R's `RepairExecutor._local_rerun` injects `recommended_action=1` and bumps CR-3 retrieval — this is per-window, not long-context. The `SPINE_MEMORY.md` Advanced Reading entry explicitly flags tttLRM as a candidate for A1 `full_update` under long-sequence regimes.

Gap: Dream3R has no A1 sub-action vocabulary in code. The Memory finalist spec (`SPEC-20260503-002`) defines A1 as a sub-action set (`full_update`, `pose_adaptive_update`, `kalman_update`, `skip_update`, `reset_state`) but no code path selects among them.

`closes_iff`:

1. A1 sub-action enum is added to `contracts.py` (or to a new `memory_action.py`) with names matching `SPEC-20260503-002`.
2. `SpatialMemory.forward` (or a new `state_update_policy.py`) chooses among A1 sub-actions based on `evidence_signals` from C1 + `latent_drift_proxy` from C2 + `conflict_score` from C4.
3. The tttLRM-style sub-action (a long-context state update) is implemented as one of the A1 choices, distinct from `full_update`.
4. W25 `TTT_PLAN.md` is drafted (`NEXT_PHASE_ROADMAP.md` W25 prerequisite).
5. At least one server tick records the policy choosing tttLRM-style A1 on a long-sequence window, logged in `cycles/`.

Required actions: (a) A1 enum + policy code; (b) tttLRM-style sub-action implementation (in-architecture or off-path via a thin adapter); (c) W25 plan draft; (d) integration test; (e) F-002 server authorization.

Dependencies: A8 is downstream of A6 (long-sequence runs are needed to exercise long-context A1). Interacts with A5 (Test3R off-path verification could co-fire with A1 sub-action selection).

Does_not_promise: that Dream3R will train a tttLRM-style update head. v0.5 closes the policy-selection axis; training the sub-action is W25 / W28 work, not v0.5.

Evidence label entering v0.5: `paper-proven` (tttLRM exists) + `inferred` (A1 sub-action selection design).

## Axes summary and recommended sequencing

| Axis | Surface | Closes iff (1-line) | Server required | Recommended order |
|---|---|---|---|---|
| A1 | Perception backbone | DINOv3 release pinned + loader + integration test | yes (F-002) | sprint 1 |
| A2 | Composer adapter checkpoints | per-adapter real load path + integration test | yes (F-002 per adapter) | sprint 1, per-adapter staged |
| A3 | Permanence dynamic_mask promotion | promotion criterion + CR-2 v2.2 + one real-data run | yes (F-002) | sprint 2 |
| A4 | VGGT adapter + capability_card v2.2 | adapter + schema revision + integration test | yes (F-002) | sprint 1 (parallel to A2) |
| A5 | Test3R Critic-triggered off-path | action 4 + RepairExecutor extension + Test3R real ckpt | yes (F-002) | sprint 2 (depends on A2 partial for Test3R) |
| A6 | NSA sliding branch utility | longer-sequence KITTI + cycle log | yes (F-002 light) | sprint 1 |
| A7 | GaussianHead main-forward entry | renderer DEC + license audit + new spec + real render test | yes (F-002 heavy) | **deferred** — no v0.5 closure expected |
| A8 | tttLRM A1 sub-action | A1 enum + policy + tttLRM-style sub-action + W25 plan | yes (F-002 heavy) | sprint 3 |

Sprints are spec-level groupings, not commitments. Each axis closure remains gated by its own DEC.

## What v0.5 explicitly does not touch

- v0.3 main forward code (model.py, modules.py, bus.py, anchor_bank.py, nsa_attention.py, composer_experts/* except for adding new adapters via A2 / A4)
- the AnchorBank capacity (K=256 stays default)
- the NSA three-branch routing logic (A6 is observation-only by default)
- the v0.3 C2 Memory spec (`SPEC-20260508-001`) — v0.3 mechanism remains the C2 baseline
- Cross-spec signal contract v2.1 prose (any new CR-* signals become CR-7+; existing CR-1..CR-6 prose unchanged)
- Track B (3R-mix Chinese survey) — out of scope per current user priority
- Track C (Dream3R 开题报告) — out of scope per current user priority
- Platform / KYKT integration — "on the agenda" per user 2026-05-22 but not v0.5 architecture work

## Open questions deferred to future spec

- Should the Composer expand beyond 8 adapters once VGGT lands? (Candidates: MV-DUSt3R+, MapAnything per SRC-2026-009.)
- Should `cross_attention` recurrence be retired now that `mamba_hybrid` is the default, or kept as the negative control per MambaOut (SRC-2024-008)?
- Is `dynamic_mask_final` a single asset or a per-object-slot asset? (Interacts with `Permanence.object_track_set`.)
- Does the v0.4 `RepairExecutor` need an action 5 for "do not produce a reconstruction this tick" (skip output) — distinct from action 0 (no_repair)?
- Should the Composer dispatch ever fan out to multiple experts in one tick (ensemble) rather than picking one? (Interacts with `route_recommendation[:, 0..k]`.)

These are not v0.5 axes; they are queued for a future spec round.

## Update discipline

This spec is amended, not silently rewritten:

- A new axis enters only when v0.4 (or a later closed-axis state) leaves an explicit stub / fallback / proxy / contract-only surface that does not already match an open axis.
- Closing an axis requires a DEC referencing the `closes_iff` clause; the DEC must record which sub-conditions are met and which are waived (with reason).
- Removing an axis without closure requires a DEC that supersedes this spec.
- When `ARCHITECTURE_V04_STATUS.md` is updated (e.g., the DINOv3-S stub label changes), this spec's axis status section is updated in the same pass.
