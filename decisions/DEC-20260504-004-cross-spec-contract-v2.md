# DEC-20260504-004 Cross-Spec Signal Contract v1 -> v2 (cost-typed route_regret)

decision_id: DEC-20260504-004

date: 2026-05-04

scope: cross-spec signal contract version (paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md)

decision: Promote the cross-spec signal contract from v1 to v2. v2 extends `route_regret` from regime-typed to regime-typed AND cost-typed by adding a `cost_normalized` axis to `capability_match`. v1 prose is preserved under "Superseded versions" per Discipline rule 5 (Honesty Override). `cases/CASE-20260505-COMPOSER-03.md` v2 row is promoted to canonical recommendation; v1 row is preserved.

status: accepted

requires_user_approval: yes (this DEC IS the user approval gate; user message 2026-05-04: "1 a 吧" in response to the cycle 009 closeout S8 packet, which framed option (a) as "adopt as v2")

## Context

Cycle 009 closeout (`cycles/CYCLE-20260505-001.md` "Contract Usage Audit (S6)" + "Closeout (S7)") surfaced a v1 -> v2 candidate from `cases/CASE-20260505-COMPOSER-03.md`. The candidate was not adopted within cycle 009 because adoption is a contract version event requiring user authorization.

The cycle-009 portfolio showed:

- Under v1, `route_regret` is regime-typed: `capability_match` is computed per regime (static_pair / dynamic_video / many_view / streaming_with_memory / static_collection), and the route recommendation follows the regime-conditioned spread.
- COMPOSER-03 input pair (Fast3R vs MASt3R-SfM on a many-view regime) produces a v1 capability-only spread of 0.325 -> recommends MASt3R-SfM. Under a cost-adjusted spread at alpha = 0.5 (a v2 framing the card spelled out hypothetically), the spread on input 2 collapses to exactly 0 -> CR-4 fires and the recommendation flips to "no binding choice" (surfaces to Advisor).
- The cost-axis evidence is paper-derived from the cost claims in the Fast3R and MASt3R-SfM papers respectively; this is consistent with cycle 009 D2' paper-derived posture.

Without v2, CR-4 has no live exercise in any cycle 009 case card other than as loophole protection (CRITIC-02) or non-binding declaration (COMPOSER-01); the contract carries a CR-4 rule that is decoratively present but never arbitrates a real tie. v2 adoption gives CR-4 routine exercise in cost-asymmetric regimes.

## Evidence

- User verbatim on this decision: "1 a 吧" (responding to the cycle 009 S8 closeout packet which framed option (a) as "adopt as v2 (regime-typed AND cost-typed; CR-4 starts firing routinely in cost-asymmetric regimes; route_recommendation can flip vs v1)")
- Source artifact for the v2 candidate: `cases/CASE-20260505-COMPOSER-03.md` "Cross-Spec Contract Usage (CR-6)" section + "Predicted Proxy Outcome" section
- Audit recording: `cycles/CYCLE-20260505-001.md` "Contract Usage Audit (S6)" v1 -> v2 candidates entry 1
- Spec foundation: `specs/SPEC-20260504-001-3r-composer.md` `one_line_thesis` line 146 ("3R needs a regime-typed route_regret axis, not a meta-model") is now extended to "regime-typed AND cost-typed" per v2

## What Changes

### Contract document changes (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`)

1. Versioning section: bump current version marker from v1 to v2.
2. Per-SPEC Published Signals: Composer's `capability_match` row gets a new sub-axis `cost_normalized` (paper-proven on the relative-ordering axis; inferred on the absolute scaling). The prior axes are preserved.
3. Conflict Resolution Rules: CR-4 commentary extended to clarify that under v2, ties on `cost_adjusted_match` (capability_match weighted with cost_normalized at alpha = 0.5 initial) are the routine arbitration trigger, not just edge cases.
4. v1 Change Log section: reformatted as "v1 history" subsection under a new "v2 Change Log" parent; v1 content preserved verbatim under "Superseded versions".
5. v2 Change Log: records this DEC as the authorization, the cost_normalized axis introduction, and the alpha = 0.5 inferred initial value.

### Case card change (`cases/CASE-20260505-COMPOSER-03.md`)

1. The v2 cost-adjusted recommendation table is promoted to canonical "Predicted Proxy Outcome" position.
2. The v1 capability-only recommendation table is preserved verbatim under a "Superseded under v2" subsection.
3. The card's `evidence_label` line is unchanged (paper-proven for cost claims; inferred for alpha and the regime mapping).
4. Cross-Spec Contract Usage (CR-6) section: CR-4 instance flipped from "exercised in v2 framing (conditional)" to "exercised under v2 (canonical)".

### What does NOT change

- v1 prose is preserved, not deleted (Discipline rule 5 Honesty Override).
- No retro-renumbering of any pre-existing IDs (Discipline rule 3 Surgical Edits).
- No change to CR-1, CR-2, CR-3, CR-5, CR-6 wording. Those rules are version-stable across v1 -> v2.
- No measured-performance claim is introduced. alpha = 0.5 is explicitly inferred.
- No cycle 009 case card other than COMPOSER-03 is modified (the others are CR-4-trivial or CR-4-loophole-protection cards; their CR-4 entries continue to read correctly under v2).
- No spec body change in any of the four finalist specs (SPEC-20260503-001..003 + SPEC-20260504-001). Specs reference the contract by name; the contract itself carries the version. Spec line 146 (Composer's `one_line_thesis`) reads as v2-compatible since it asserts an axis exists, not which axes exist.

## Options Considered

(a) Adopt as v2: chosen. Routine CR-4 exercise; cost-axis becomes a published Composer signal; route_recommendation can flip vs v1 in cost-asymmetric regimes. Cost: one contract-document version event + one case-card promotion + sync-chain stamps. **User selected.**

(b) Defer (keep v1): rejected. Defers the routine CR-4 exercise indefinitely; cost-axis remains an open research direction without a publication-ready home. The cycle 009 audit already records CR-4 as "decoratively present but never arbitrating a real tie under v1" — leaving v1 unchanged perpetuates that gap.

(c) Fold into v1.x (treat cost_normalized as a v1 documentation extension): rejected. CR-4's behavior changes (it now fires routinely on cost-adjusted ties), which is a conflict-resolution-rule change. Per the contract's own versioning rules ("A change in conflict resolution rules produces a new version"), this is a v2 event, not a v1.x typo-fix.

## Forward Linkages

- `cycles/CYCLE-20260504-002.md` (cycle 010 cycle log) carries v2-active case cards as the new default; CR-4 audit must include cost-adjusted ties.
- `decisions/DEC-20260504-005-cycle-010-launch.md` (cycle 010 launch memo) records v2 as active for all cycle 010 cards.
- Cycle 010 closeout audit (planned) re-checks CR-1..CR-6 under v2 across the 6 cycle-010 cards plus the 6 retained cycle-009 cards (COMPOSER-03 promoted; the others unchanged).
- alpha = 0.5 is initial; cycle 010 or a later cycle may surface a v2.1 candidate with a different alpha if paper-derived cost claims diverge from the assumed proxy. Such a surface would be a Honesty Override note inside a case card, not a silent contract edit.

## Discipline Compliance

- Discipline rule 1 (Falsifiability): v2 is falsifiable in the same way v1 was — the per-card route_recommendation is paper-derived and a future cycle that produces measured numbers can show the v2 recommendation is wrong. v2 adds an axis without removing any falsification path.
- Discipline rule 2 (Minimum Viable Mechanism): the cost_normalized axis is the minimum addition that makes route_regret cost-typed; it does not introduce non-cost / non-regime axes.
- Discipline rule 3 (Surgical Edits): the contract document edit appends rather than retroactively rewrites; v1 is preserved as superseded.
- Discipline rule 4 (Falsifiable Research Goals): primary failure mode F6 (Fragmented Model Ecology) gains a stronger route_regret signal under v2; the falsification axis (P5 route_regret) is unchanged.
- Discipline rule 5 (Honesty Override): v1 prose preserved verbatim; alpha = 0.5 carries `inferred` label; no measured claim introduced.

## Companion Files

- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` (the artifact this DEC modifies)
- `cases/CASE-20260505-COMPOSER-03.md` (the artifact this DEC promotes)
- `cycles/CYCLE-20260505-001.md` "Contract Usage Audit (S6)" (the audit that surfaced the candidate)
- `decisions/DEC-20260504-005-cycle-010-launch.md` (the cycle 010 launch memo that consumes this DEC)
- `cycles/CYCLE-20260504-002.md` (the first cycle whose case cards are v2-default)
