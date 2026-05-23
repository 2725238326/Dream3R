# Cross-Spec Signal Contract

Last updated: 2026-05-23 (cycle 20260523; v2.1 -> v2.2 additive revision: Composer capability_card gains `feed_forward_manyview` regime for VGGT; v2 cost substance and v2.1 forward-reference protocol unchanged)

Status: active contract; revision policy below.

## Purpose

The four finalist specs (Critic / Memory / Permanence / Composer) each own a small action subset and publish read-only signals that other specs consume. Without a written contract, each spec's case-card pass in cycle 009 would silently invent assumptions about what the others provide.

This file is the formal contract. It defines:

1. who publishes which signal
2. who consumes it
3. the contract type (read-only, handoff, or no-cross)
4. how conflicts between specs are resolved
5. how the contract itself is versioned

This contract is `inferred`. It has not been exercised by L2 case cards. Cycle 009 case cards are the first test. Corrections produce a new revision rather than a silent edit, per `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5 (Honesty Override).

## Scope

The contract covers only the four finalist specs and the cross-modal / active-perception specs that may be drafted in later cycles. It does not cover:

- KYKT app contracts (Advisor / Sample Matrix / runner schemas; those are separate)
- backend service contracts (out of scope for cycle 008.5)
- frontend handoff contracts (handled by `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md`)

The contract is consumed at L2 case-card time. It is not consumed by L1 design content; specs may reference the contract abstractly without requiring case-card data.

## Signal Owner Table

The following table lists every signal that crosses spec boundaries. Signals defined inside a single spec and not consumed elsewhere are not listed here.

| Signal | Producer SPEC | Consumer SPEC(s) | Contract type | First exercised by |
|---|---|---|---|---|
| `conflict_score` | Critic SPEC-20260503-001 | Memory SPEC-20260503-002, Permanence SPEC-20260503-003 | read-only | cycle 009 case cards |
| `route_history` | Critic SPEC-20260503-001 | Composer SPEC-20260504-001 | read-only | cycle 009 case cards |
| `recommended_action` | Critic SPEC-20260503-001 | Memory, Permanence, Composer (informational) | read-only | cycle 009 case cards |
| `route_regret_estimate` | Critic SPEC-20260503-001 | Composer SPEC-20260504-001 | read-only | cycle 009 case cards |
| `latent_drift_proxy` | Memory SPEC-20260503-002 | Critic SPEC-20260503-001 | read-only | cycle 009 case cards |
| `anchor_set` | Memory SPEC-20260503-002 | Permanence (informational) | read-only | cycle 009 case cards |
| `policy_log` | Memory SPEC-20260503-002 | Composer (informational) | read-only | cycle 009 case cards |
| `dynamic_ratio` | Permanence SPEC-20260503-003 | Memory (gate for A1/A2), Critic (informational) | read-only | cycle 009 case cards |
| `object_track_stability` | Permanence SPEC-20260503-003 | Memory (informational) | read-only | cycle 009 case cards |
| `suppress_static_write(r)` | Permanence SPEC-20260503-003 | Memory (handoff: Memory must honor) | handoff | cycle 009 case cards |
| `admit_static_write(r)` | Permanence SPEC-20260503-003 | Memory (handoff: Memory's A2 write pipeline) | handoff | cycle 009 case cards |
| `pollution_log` | Permanence SPEC-20260503-003 | Composer (informational) | read-only | cycle 009 case cards |
| `capability_match` | Composer SPEC-20260504-001 | Critic SPEC-20260503-001 (gate for A5 reroute_model) | read-only | cycle 009 case cards |
| `capability_card` | Composer SPEC-20260504-001 | Critic, Memory, Permanence (informational) | read-only | cycle 009 case cards |
| `sample_regime_card` | Composer SPEC-20260504-001 | Critic, Memory, Permanence (informational) | read-only | cycle 009 case cards |
| `route_recommendation` | Composer SPEC-20260504-001 | Critic A5 (when Critic decides reroute) | handoff | cycle 009 case cards |

Contract type definitions:

- **read-only**: consumer may read the value to inform its own decisions but must not mutate, override, or echo it back as authoritative
- **handoff**: producer emits an action the consumer must execute (or explicitly refuse with a logged reason)
- **no-cross**: signal is internal to the producer; not in this table

## Per-SPEC Published Signals

This section restates the published surface of each finalist spec so a consumer does not have to mine the full SPEC body.

### Critic SPEC-20260503-001 publishes

- `conflict_score(t)`: scalar derived from {pose_novelty, view_overlap, reprojection_residual, pointmap_conflict, confidence_drop, prior_rgb_conflict}; range and threshold `theta_conflict` are inferred per Critic spec
- `recommended_action`: one of {accept, rerun_local_region, reroute_model, open_anchor_budget, request_prior, conflict_unresolved}
- `route_history(t)`: list of (model, action) pairs already tried for this input window
- `route_regret_estimate`: gap between chosen route's `capability_match` and best-known `capability_match` for this regime; computed from Composer's published `capability_card`

What Critic does NOT publish:

- learned weights for `conflict_score` aggregation (none exist; weights are inferred)
- a binary "this output is wrong" verdict (Critic emits a score and recommended action only)

### Memory SPEC-20260503-002 publishes

- `latent_drift_proxy`: combination of pose_novelty + confidence_drop drift over windows
- `anchor_set(t)`: set of protected anchor indices in the memory store
- `cache_window(t)`: bounded sliding cache window contents (informational)
- `policy_log(t)`: append-only log of A1/A2/A3 sub-action choices

What Memory does NOT publish:

- the memory store contents themselves (Memory does not own the store; it owns the policy)
- a cross-job memory state (Memory's contract is per-job)

### Permanence SPEC-20260503-003 publishes

- `dynamic_ratio(r, t)`: per-region dynamic-content ratio
- `object_track_stability(o, t)`: per-object identity-confidence trace
- `suppress_static_write(r)`: handoff to Memory; Memory must honor or log refusal
- `admit_static_write(r)`: handoff to Memory's A2 write pipeline
- `pollution_log(t)`: append-only log of suppress / admit / defer decisions
- `object_track_set(t)`: set of `{object_id, last_seen_t, last_position, identity_confidence}` records

What Permanence does NOT publish:

- per-frame motion fields beyond `dynamic_horizon` (evicted)
- 4DGS asset descriptors (out of scope per SPEC-003 boundaries)

### Composer SPEC-20260504-001 publishes

- `capability_card(model_id)`: per-model capability profile across input regimes (static pair, many-view, streaming, dynamic, sparse-view, feed-forward many-view, etc.). v2 adds a `cost_normalized` axis (paper-derived from per-paper cost claims; relative-ordering paper-proven, absolute scaling inferred). v2.2 adds the `feed_forward_manyview` regime so VGGT is not collapsed into Fast3R's dense sequential row.
- `sample_regime_card(input)`: per-input regime classification
- `capability_match(model_id, input)`: scalar match score in [0, 1] from card join. **v2**: now exposes both a capability-only spread and a `cost_adjusted_match` formed by weighting the capability-only spread with `cost_normalized` at `alpha = 0.5` (initial value, inferred). Consumers may use either; CR-4 arbitrates ties on the cost-adjusted spread under v2.
- `route_recommendation(input)`: ordered list of model_ids from best to worst expected capability_match. Under v2, the ordering may flip vs v1 in cost-asymmetric regimes.
- `route_regret(chosen, input)`: gap between chosen model's match and best-known model's match. Regime-typed AND cost-typed under v2 (was regime-typed only in v1).

What Composer does NOT publish:

- model accuracy claims (capability cards encode regime fit, not measured accuracy)
- a single "best model" selection unless asked via `route_recommendation`

## Conflict Resolution Rules

When two specs disagree, the contract specifies which spec's decision wins.

### Rule CR-1: Critic A5 reroute requires Composer agreement on capability_match spread

If Critic says `reroute_model` for an input but Composer's `capability_match` has zero spread across the comparator pool for that regime (i.e. no alternative model has higher expected match), Critic must downgrade to `conflict_unresolved` and surface to Advisor. Critic does not invent a model that Composer has not characterized.

Rationale: A5 reroute is meaningful only when the alternative is differentiated. Allowing Critic to override would silently bake un-versioned capability assumptions into reroute decisions.

### Rule CR-2: Permanence suppress_static_write is binding on Memory

If Permanence emits `suppress_static_write(r)`, Memory's A2 must apply it. Memory may NOT override and write the suppressed region into the static map even if its own `write_value_estimate` would otherwise admit the write.

If Memory cannot honor (e.g. structural limitation), Memory logs `cross_spec_refusal{producer=Permanence, signal=suppress_static_write, reason=...}` and surfaces to Advisor. Silent override is a contract violation.

Rationale: the dynamic-pollution claim collapses if Memory ignores Permanence. A refusal must be visible.

### Rule CR-3: Memory drift signal does not gate Critic verification

If Memory's `latent_drift_proxy` is high but Critic's per-window evidence vector shows no `pointmap_conflict` or `reprojection_residual`, Critic does NOT auto-trigger A5 just from drift. Drift is informational for Critic. The A5 trigger condition remains the conjunction of `conflict_score(t) > theta_conflict` and the other Critic-internal preconditions.

Rationale: Memory and Critic must remain falsifiable independently. If drift could trigger A5 directly, Memory's P2/P3 results and Critic's P1/P5 results would couple, defeating cycle 009's parallel-track design.

### Rule CR-4: Composer route_recommendation does not bind Critic when capability_match is tied

If Composer's top-1 and top-2 `capability_match` are within `epsilon_tie` (default 0.05; inferred), Composer publishes both as candidates. Critic's A5 reroute_model picks among them by Critic-internal preference (e.g. preference for already-cached models, or for models whose route_history has not been tried this window). Composer does not force the choice.

Under v2 (per `decisions/DEC-20260504-004-cross-spec-contract-v2.md`), CR-4 is the routine arbitration trigger for ties on `cost_adjusted_match` (the v2 cost-normalized spread). v1 framing — where CR-4 only protected against rare exact ties on capability-only spread — remains valid as a fallback, but the canonical CR-4 firing condition under v2 is a tie on the cost-adjusted spread within `epsilon_tie`.

Rationale: route_regret is informative as a spread, not as a forced ranking under noise. Cost asymmetry produces ties in the cost-adjusted spread routinely (paper-derived; see `cases/CASE-20260505-COMPOSER-03.md` v2 row); CR-4 must arbitrate those, not just rare exact ties on capability alone.

### Rule CR-5: All cross-spec signals carry their producer's evidence label

A signal's evidence label propagates with it. If Memory's `latent_drift_proxy` is `inferred`, Critic must treat it as `inferred` when reading it. Critic must not silently upgrade an inferred input to paper-proven status downstream. This is a direct application of `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5.

### Rule CR-6: Cycle 009 case cards record contract usage

Each cycle 009 case card must list which cross-spec signals it consumed and what the producer's evidence label was at consumption time. If any consumed signal had label `unknown`, the case card carries a caveat. This is the test path for the contract itself.

## Versioning

This contract is versioned. The current version is **v2.1**.

Revision rules:

- A new signal added, removed, or repurposed produces a new version (v2, v3, ...).
- A change in conflict resolution rules produces a new version.
- A change in evidence-label propagation rules produces a new version.
- Pure typo fixes do not produce a new version.

Each version records:

- date
- summary of change
- which specs are affected
- which case cards exercised the change

When a new version supersedes an older one, the older version is preserved in this file under a "Superseded versions" section rather than deleted. Discipline rule 5 (Honesty Override): retracted contract clauses must be visible, not silently overwritten.

### Forward-reference null protocol (added in v2.1)

A reading card MAY return `null` for a CR-X read when the producer card has not yet been drafted within the current cycle. This is a **deferred read**, not a missing read.

When a card uses this protocol, it MUST document on the card body:

1. **fallback path**: what the consumer card does in the absence of the signal. The fallback must be stated as a concrete behavior, not as "the result is unknown".
2. **expected close-out cycle**: the cycle in which the producer card is expected to land. If the producer card is in the same cycle as the consumer card (in-cycle cross-pair, e.g. cycle 010 PERMANENCE-01 <-> MEMORY-01), state the cycle id; the close-out is in the same cycle's S6 audit. If the producer card is in a later cycle, state the cycle id and the gap entry that tracks it.
3. **producer card id (or reservation)**: the case card that will publish the signal. If the case card id is reserved but not yet drafted, cite the reservation site (spec line, DEC entry, or cycle log entry).

When the producer card lands, the cycle closeout audit (S6 in cycle log) MUST verify:

1. the consumer card's documented fallback is consistent with the producer card's actual published value, OR
2. the consumer card is updated to consume the actual value, with a Surgical Edit (Discipline rule 3) recording the diff.

If neither is achievable (producer card retired, or consumer fallback proven wrong), the consumer card's CR-X usage is retired with a stated reason in the closeout audit. Forward-reference null is NOT an excuse to leave a CR-X read unresolved across cycles; the protocol is a rendering of the deferred read, not a permanent placeholder.

This protocol formalizes a pattern already exercised in:

- `cases/CASE-20260504-CRITIC-02.md` line 210 (CR-1 forward reference; closed by `cases/CASE-20260505-COMPOSER-01.md` in cycle 009)
- `cases/CASE-20260504-CRITIC-03.md` line 147 (CR-3 forward reference on Memory `latent_drift_proxy`; closed by `cases/CASE-20260504-MEMORY-01.md` in cycle 010)
- `cases/CASE-20260504-MEMORY-02.md` lines 110, 113 (CR-2 + Critic forward-reference null on a Spann3R-regime card; documented as gap, not closed retroactively)
- `cases/CASE-20260504-MEMORY-01.md` line 85 (Critic forward-reference null; closed by reading cycle-009 CRITIC-03 fallback path)

Existing case cards that use the pattern are NOT retroactively edited to match v2.1 wording. Per Discipline rule 3 (Surgical Edits), v2.1 documents the protocol, not changes the cards. Future case cards drafted after 2026-05-05 use the v2.1 wording above.

## v2.2 Change Log

- 2026-05-23 (v0.5 A4 closure): contract promoted from v2.1 to v2.2 per `decisions/DEC-20260523-002-a4-vggt-capability-v22.md`. v2.2 is **additive only**: it adds `feed_forward_manyview` to Composer's capability-card regime vocabulary and leaves `cost_normalized`, `cost_adjusted_match`, CR-1..CR-6, alpha=0.5, and the v2.1 forward-reference null protocol unchanged. The code-level schema is `composer_experts.method_profiles.REGIME_ORDER` with six regimes.

## v2.1 Change Log

- 2026-05-05 (cycle 011 launch, sub-pass S4): contract promoted from v2 to v2.1 per `decisions/DEC-20260505-001-cycle-011-launch-and-d3-demo-target.md`. v2.1 is **additive only**: adds the "Forward-reference null protocol" subsection above. v2.1 does NOT touch alpha (still 0.5 inferred), the signal owner table, CR-1..CR-6 substantive rules, or evidence-label propagation. The other two cycle-010 v3 candidates (8x8 grid partition for Permanence regions; identity_consistency threshold pinning at ~0.7) are deferred and not promoted in v2.1; rationale recorded in DEC-20260505-001 (3). First case card drafted natively under v2.1: any cycle-011-or-later card; existing cycle-009 + cycle-010 cards remain v1 / v2 native and are not retroactively edited (Surgical Edits rule).

## v2 Change Log

- 2026-05-04 (cycle 010 launch, sub-pass B): contract promoted from v1 to v2 per `decisions/DEC-20260504-004-cross-spec-contract-v2.md`. v2 adds a `cost_normalized` sub-axis to Composer's `capability_card` and exposes `cost_adjusted_match` as an additional output of `capability_match`. CR-4 commentary extended to record cost-adjusted ties as the canonical arbitration trigger. `route_regret` reframed from regime-typed to regime-typed AND cost-typed. v1 prose preserved verbatim under "Superseded versions". First exercising case card under v2: `cases/CASE-20260505-COMPOSER-03.md` (v2 row promoted to canonical recommendation; v1 row preserved). alpha = 0.5 is the initial inferred weight; future cycles may surface a v2.1 with a different alpha if paper-derived cost claims diverge from the assumed proxy.

## v1 Change Log (closed; superseded by v2)

- 2026-05-04 (cycle 008.5): initial contract drafted alongside `decisions/DEC-20260504-001-composer-finalist-upgrade.md`. v1 covers Critic / Memory / Permanence / Composer published signals and six conflict resolution rules. First exercise: cycle 009 case cards (`cycles/CYCLE-20260505-001.md` "Contract Usage Audit (S6)").

## Superseded Versions

### v1 (cycle 008.5 to cycle 009 closeout)

The two text blocks that v2 modified are preserved here verbatim per Discipline rule 5 (Honesty Override). The rest of the v1 contract body — Purpose, Scope, Signal Owner Table, Per-SPEC Published Signals (Critic / Memory / Permanence rows), CR-1, CR-2, CR-3, CR-5, CR-6, Versioning rules, Out Of Scope, Companion Files — is identical between v1 and v2 and is not duplicated below.

#### v1: Composer SPEC-20260504-001 publishes (capability_match line, before v2)

```text
- `capability_card(model_id)`: per-model capability profile across input regimes (static pair, many-view, streaming, dynamic, sparse-view, etc.)
- `sample_regime_card(input)`: per-input regime classification
- `capability_match(model_id, input)`: scalar match score in [0, 1] from card join
- `route_recommendation(input)`: ordered list of model_ids from best to worst expected capability_match
- `route_regret(chosen, input)`: gap between chosen model's match and best-known model's match
```

#### v1: CR-4 wording (before v2 routine-arbitration extension)

```text
### Rule CR-4: Composer route_recommendation does not bind Critic when capability_match is tied

If Composer's top-1 and top-2 `capability_match` are within `epsilon_tie` (default 0.05; inferred), Composer publishes both as candidates. Critic's A5 reroute_model picks among them by Critic-internal preference (e.g. preference for already-cached models, or for models whose route_history has not been tried this window). Composer does not force the choice.

Rationale: route_regret is informative as a spread, not as a forced ranking under noise.
```

v1 was active from 2026-05-04 (cycle 008.5 closeout) through 2026-05-04 (cycle 010 launch). All cycle 009 case cards (`cases/CASE-20260504-CRITIC-01..03.md` + `cases/CASE-20260505-COMPOSER-01..03.md`) were drafted under v1. The audit recording v1's full coverage is `cycles/CYCLE-20260505-001.md` "Contract Usage Audit (S6)".

## Out Of Scope For This Contract

- learned signal aggregation (no learned weights for any signal in v1; all weights are inferred)
- multi-job state propagation (each contract instance is per-job; cross-job memory consolidation is a separate future contract)
- KYKT runner / Advisor / Sample Matrix integration (separate contract; see `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md` and the workflow status)
- Cross-Modal A7 ownership (still gated; the Cross-Modal spec is not drafted yet)
- Active Perception A8 ownership (still gated; the Active Perception spec is not drafted yet)

## Companion Files

- `paradigm/RESEARCH_CODE_DISCIPLINE.md` — the discipline rules this contract enforces, especially rules 3 (Surgical Edits) and 5 (Honesty Override)
- `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` — A1-A8 actions, P1-P8 proxies, evidence signal vector
- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` — F1-F6 failure modes and C1-C16 composition edges
- `specs/SPEC-20260503-001-geometry-critic.md` — Critic spec; reads Composer `capability_match`, publishes `conflict_score` and friends
- `specs/SPEC-20260503-002-executive-memory.md` — Memory spec; reads `conflict_score`, `dynamic_ratio`, honors `suppress_static_write`
- `specs/SPEC-20260503-003-dynamic-object-permanence.md` — Permanence spec; publishes `dynamic_ratio`, `suppress_static_write`, `object_track_stability`
- `specs/SPEC-20260504-001-3r-composer.md` — Composer spec; publishes `capability_card`, `capability_match`, `route_recommendation`
- `planning/WORK_RISK_REGISTER.md` — consolidated risk view including contract drift risk
