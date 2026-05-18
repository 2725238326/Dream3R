# Session handoff 20260504-001: cycle 008 closeout + cycle 009 prep

handoff_id: SESSION-HANDOFF-20260504-001

date: 2026-05-04

scope: continue Dream research project from end-of-cycle-008 state into cycle 009 preparation

status: active execution brief; new agent should treat this as the primary task list for the session

## Why this handoff exists

The previous session closed cycle 008 (CYCLE-20260503-002), which drafted three finalist mechanism specs (Critic / Memory / Permanence) and recorded user-approved finalist set DEC-20260503-002.

In the same session the user gave four follow-up directions:

1. Decision 1 (cycle 009 first case-card pass owner): Critic first — locked
2. Decision 2 (Composer L1 vs L2 framing): upgrade Composer to a full finalist spec — locked, with timing accelerated to "now" not "after a finalist clears"
3. Decision 3 (first teacher demo target): user position is "memory is one borrowable component, do not all-in on any single finalist" — this is itself a directional decision and must be captured as such; the demo target itself is deferred until cycle 009 case-card data lands
4. Decision 4 (annotation budget per SPEC): 90 to 120 minutes per case card — locked

The user also asked for a literature guidance board because the existing source files are inventories rather than guidance, and asked for general acceleration ("全力提速") within the project structure.

This handoff document encodes all of the above as an execution-ready task list.

## Hard rules for the receiving agent

1. Follow `paradigm/RESEARCH_CODE_DISCIPLINE.md` five rules. Especially:
   - Rule 3 Surgical Edits: do not retro-renumber RESEARCH_STATE vs cycle log counters; do not silently fix sibling files outside the task scope.
   - Rule 5 Honesty Override: every new mechanism claim carries an evidence label; user approval cannot be invented.
2. Honor `AGENT_MASTER_PROMPT.md` section 6 boundaries. Still blocked on user approval: thesis selection, reproduction, training, checkpoint download, KYKT navigation change, frontend implementation, reusable Codex skill packaging, retiring any non-finalist track.
3. ID conventions are fixed: `SPEC-YYYYMMDD-NNN`, `DEC-YYYYMMDD-NNN`, `CYCLE-YYYYMMDD-NNN`, `CASE-YYYYMMDD-NNN`. Today is 2026-05-04, so new artifacts use `20260504` prefix.
4. Sentence case headers throughout. No em-dashes.
5. Existing directory layout is canonical. New artifacts go into existing directories where possible. The only new top-level directory authorized in this handoff is `literature/` (user explicitly approved its shape and purpose).
6. Apply Guidance File Sync Rule for every new artifact: update `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`, current cycle log, `INDEX.md`, `README.md`, and the relevant registry.

## What is locked and what is open

Locked by user this session:

- Critic gets cycle 009 first case-card pass
- Composer is upgraded to a finalist mechanism spec, drafted now
- No all-in on any single finalist; treat memory / critic / permanence as parallel borrowable components
- Annotation budget per case card: 90 to 120 minutes
- Literature guidance board to be created

Still open and gated on user input:

- First teacher demo target (deferred until cycle 009 case-card data exists)
- Teacher audience profile (placeholder file should ask the right questions; do not invent answers)
- Final thesis selection
- All L3 / L4 actions (reproduction, training, checkpoint, KYKT navigation, frontend implementation)

## Tasks in execution order

Tasks are ordered so that dependencies resolve naturally. Each task names the file path it produces or modifies.

### P0 Reflect locked decisions in the registry layer

Task 1. Write `decisions/DEC-20260504-001-composer-finalist-upgrade.md`.

- decision_id: DEC-20260504-001
- scope: thesis shortlist / mechanism-spec authorization
- decision: upgrade 3R Composer / Unified Model Ecology from supporting layer to a fourth finalist mechanism spec; draft now, not deferred to "after a finalist clears"
- evidence: user verbatim "决策2改成升格吧，因为确实有效果" plus "全力提速了" framing in the same turn
- rationale: A5 reroute_model in SPEC-20260503-001 (Critic) directly reads Composer capability_match signals; without a written Composer spec, A5 case cards in cycle 009 fall back to hand-written assumptions
- constraints unchanged: no reproduction, no training, no checkpoint download, no KYKT navigation change

Task 2. Write `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`.

- decision_id: DEC-20260504-002
- scope: thesis selection posture
- decision: no single finalist (Critic / Memory / Permanence) is treated as the thesis spine; memory in particular is borrowable as one component, not the headline; cycle 009 case cards run for all three on parallel tracks (with Critic first by D1)
- evidence: user verbatim "我觉得记忆系统啥的只是我们借鉴优点的一个部分，我觉得不能all in"
- implications: D3 (first teacher demo target) is deferred until cycle 009 produces L2 case-card data; do not pick a demo target unilaterally; instead surface it as an explicit decision point in WORKFLOW_STATUS

Task 3. Update `registry/decision_registry.md`.

- add a row for DEC-20260504-001 (composer upgrade)
- add a row for DEC-20260504-002 (no all-in)
- bump Last updated to 2026-05-04

Task 4. Update annotation budget references in the three existing finalist specs to reflect D4 (90 to 120 minutes per case card).

- `specs/SPEC-20260503-001-geometry-critic.md`:
  - in `Engineering Cost > L1_design_cost` block, replace "Annotation ceiling per case card: ~30-60 minutes of human labeling" with "Annotation budget per case card: 90-120 minutes per cycle 008 D4 (DEC-20260504-002 implies the same ceiling for parallel tracking)". Keep the original "low cost" framing for Critic since 30-60 minutes remains the expected median.
- `specs/SPEC-20260503-002-executive-memory.md`:
  - in `Engineering Cost > L1_design_cost` and in `Next Discussion Point For The User`, change references from "60 minutes / 120 minutes optional uplift" to "90-120 minutes per case card (no optional uplift; this is the ceiling)".
- `specs/SPEC-20260503-003-dynamic-object-permanence.md`:
  - in `Proxy Validation Plan > fail_fast_threshold`, replace "60 minutes of human effort" with "120 minutes of human effort per cycle 008 D4".
  - in `Engineering Cost > L1_design_cost`, change "60-minute ceiling is a hard fail-fast condition" to "120-minute ceiling is the hard fail-fast condition per cycle 008 D4".
  - in `Risks > engineering_risk`, update the 60-minute mention.
  - in `Next Discussion Point For The User`, update item 1 to reflect the 120-minute hard cap.

These are surgical edits. Do not touch unrelated content in the SPEC files.

### P1 Composer finalist spec

Task 5. Write `specs/SPEC-20260504-001-3r-composer.md` using `templates/finalist_mechanism_spec.md`.

- spec_id: SPEC-20260504-001
- branch_name: 3R Composer / Unified Model Ecology
- approval_decision_id: DEC-20260503-002 (original finalist authorization) + DEC-20260504-001 (composer upgrade timing)
- primary_failure_mode: F6 Fragmented Model Ecology
- secondary_failure_modes: F3, F1, F2
- owned_actions: A5 only (single owned action; smaller than Critic / Memory / Permanence by design, because Composer's leverage is the capability-card matrix rather than action ownership)
- support_actions: A3, A4, A7
- comparator anchors: DUSt3R, MASt3R, MASt3R-SfM, Fast3R, Spann3R, MonST3R, CUT3R, STream3R, SLAM3R, MV-DUSt3R+, Splatt3R, InstantSplat, NoPoSplat
- closest_comparator: Composer-style routing literature (none directly published in 3R; nearest analog is mixture-of-experts routing)
- weakest_comparator_pressure: pure model routing reads as system engineering rather than paper-grade architecture
- novelty_gap: capability cards + sample regime cards yield a measurable P5 route_regret axis that is missing from any single comparator
- core_claim_paragraph: 3R fragmentation is itself the research problem; a controller that maps input regimes to capability profiles produces a falsifiable route_regret signal that downstream finalists (Critic A5) can read
- mechanism_pseudocode: define capability_card schema, sample_regime_card schema, the route function, and the route_regret estimator
- primary_proxy: P5 route regret
- secondary_proxy: capability_match
- case_cards_to_fill: CASE-20260505-COMPOSER-01..03 reserved for cycle 009 (one per existing KYKT job pair: Fast3R vs Spann3R on shared input; MASt3R vs MonST3R for static vs dynamic regime; Fast3R vs MASt3R-SfM for many-view vs pair regime)
- acceptance_threshold: route_regret(Composer) < route_regret(single-default-model) on at least 2 of 3 case cards
- fail_fast_threshold: if route_regret has zero spread across all three case cards, retire to "support layer only" (no cycle 010 redraft)
- writing_value_if_only_negative: paper still benefits because the negative result frames the F6 problem precisely
- KYKT integration: research_lane + advisor_report only; no new runner; no navigation change
- cross-spec contract: Composer publishes capability_match read by Critic A5 (per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`, Task 6 below)
- evidence labels: mechanism_status `inferred`, action_policy_status `inferred`, performance_status `unknown`
- annotation budget: 90-120 minutes per case card per D4
- next_action: fill_case_cards
- end with the standard "Next Discussion Point For The User" section listing the open decisions Composer surfaces

Task 6. Write `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`.

- purpose: formal contract for the read-only signals each SPEC publishes for the others to consume; prevents action collisions and policy ambiguity in cycle 009 case cards
- structure:
  1. Signal owner table: signal name -> producer SPEC -> consumer SPECs -> contract type (read-only / handoff / no cross)
  2. Per-SPEC published signals (what Critic publishes to Memory and Permanence; what Memory publishes back; what Permanence publishes; what Composer publishes to Critic)
  3. Conflict resolution rules: when two SPECs disagree (e.g. Critic says reroute_model but Composer's capability_match has zero spread), define which SPEC's decision wins and why
  4. Versioning: this contract is versioned; cycle 009 case-card pass tests it; corrections go into a new contract revision rather than silent edits
- evidence labels: contract_status `inferred` (not yet exercised by case cards)
- update `AGENT_MASTER_PROMPT.md` mandatory load protocol to include this file

Task 7. Update RU registries to reflect Composer upgrade.

- `registry/research_unit_registry.md`: change RU-002 Current decision from "best near-term demo" to "spec_drafted (linked to SPEC-20260504-001)"; bump Last updated.
- `units/RESEARCH_UNIT_BANK.md`: append a 2026-05-04 decision line to RU-002 stating "(cycle 008.5): promoted to spec_drafted; linked to SPEC-20260504-001; owns A5; primary proxy P5 + capability_match"; bump Last updated.

### P2 Literature guidance board v1

Task 8. Create directory `literature/` and the following files.

`literature/INDEX.md`:

- one paragraph on purpose: "literature guidance, not literature inventory"
- explicit pointer to existing inventories (`sources/FRONTIER_SOURCE_MAP.md`, `registry/source_registry.md`) so users do not duplicate
- table of files in this directory
- usage rule: when adding a new spine entry, also add a line to `CRITICAL_NOTES.md` if the new paper is commonly confused with a comparator

`literature/SPINE_CRITIC.md`:

- one-line definition of the Critic finalist
- required reading section: at minimum Test3R, TTT3R, CTRL, MASt3R-SfM, plus 1-2 background System-2 / test-time compute papers; each entry has 1-2 lines on "what this paper actually claims" and "what people often misread it as"
- advanced reading section: G-CUT3R, SLAM3R, MV-DUSt3R+, Easi3R-as-counterexample
- skip-with-reason section: any sources that look related by title but are off-topic
- cross-paper disagreement section: where Test3R and TTT3R diverge, what is unsettled
- interface to SPEC-20260503-001: which signals come from where, which proxy metric maps to which paper
- evidence labels: every claim about a paper carries `paper-proven` / `code-observed` / `inferred` / `unknown`

`literature/SPINE_MEMORY.md`: same structure for Executive Memory finalist. Required reading minimum: CUT3R, STream3R, LONG3R, LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, Point3R. Advanced: LongStream, sparse / linear attention background. Critical entry: distinguish Mem3R (KV cache) from OVGGT (anchor cache) from Point3R (external pointer memory).

`literature/SPINE_PERMANENCE.md`: same structure for Dynamic Object Permanence finalist. Required reading: MonST3R, POMATO, D2USt3R, Easi3R, RayMap3R. Advanced: 4DGS variants (note explicitly out of scope for SPEC-003), G-CUT3R as guided boundary.

`literature/SPINE_COMPOSER.md`: same structure for the new Composer finalist. Required reading: DUSt3R, MASt3R, Fast3R, Spann3R as the diversity baseline; mixture-of-experts and routing literature as cross-domain analog. Critical entry: route regret as a 3R-specific framing not present in MoE literature.

`literature/CRITICAL_NOTES.md`:

- running log of "looks like X is X' but actually" insights
- seed entries (write at least these five):
  1. Test3R (consistency self-check at inference) vs TTT3R (lightweight training at inference): both labeled "test-time" but compute scope differs
  2. Mem3R memory = KV cache; OVGGT memory = anchor cache; Point3R memory = external pointer; not interchangeable
  3. POMATO and D2USt3R both extend DUSt3R with dynamics, but POMATO trains on dynamic-aware loss while D2USt3R uses dynamic-aware token routing
  4. SLAM3R is a SLAM-shaped consumer of 3R outputs, not a new 3R model family
  5. RayMap3R uses ray representations for dynamics; not a 4D Gaussian variant
- format: one entry = title + one-paragraph note + linked sources + last-updated stamp

`literature/PAPER_RELATED_WORK_SKELETON.md`:

- skeleton only; no prose
- section list mapped from F1-F6 failure modes
- each section lists which papers belong, drawn from the SPINE files
- two reserved sections: "what this paper does and does not claim about itself" (positioning) and "what we add" (Dream contribution)
- explicit note that this skeleton is for the eventual paper, not a finished related work section; updates as case cards land

Task 9. Wire the literature board into navigation.

- `INDEX.md`: add a `literature/` subsection between `experiments/` and `registry/` with a row per file
- `README.md`: add `literature/` to the Subdirectories list with one-line role description
- `AGENT_MASTER_PROMPT.md` mandatory load protocol: append `E:\kykt\Dream\literature\INDEX.md` after the existing list, and add literature spine pointers to the topical "inspect the most relevant active file for the requested task" subsection

### P3 Supporting artifacts

Task 10. Write `templates/demo_storyboard.md`.

- branch-neutral storyboard skeleton
- sections: title, one-line teacher takeaway, panels (visual layout), narrative beats, surprise hook, what could go wrong on the day, fail-safe alternative
- intended use: each finalist's eventual demo follows this template so the four demos compare cleanly
- explicit note: filling this template does not authorize showing the demo; demo authorization is a separate decision per AGENT_MASTER_PROMPT section 6

Task 11. Write `paradigm/TEACHER_AUDIENCE_PROFILE.md`.

- placeholder file, not invented content
- purpose paragraph
- empty fields the user is expected to populate: research taste (theory / system / visual), prior expectations on this work (cold start vs known direction), demo precedent (first impression vs reinforcement), what the teacher has previously praised in similar work
- explicit instruction: agents must not fill these fields without user input; until populated, decision 3 (demo target) and demo storyboard fields stay open

Task 12. Write `planning/WORK_RISK_REGISTER.md`.

- consolidated risk view across all four finalist specs and the cross-spec contract
- sections: per-SPEC risks (already authored in each SPEC), cross-SPEC risks (e.g. annotation budget overflow across four parallel case-card passes, signal contract drift, numbering reconciliation, teacher audience uncertainty), trigger conditions, current status
- format: table with columns Risk / Source SPEC / Trigger / Current status / Owner (Dream agent vs user gate)
- explicit cross-link to each SPEC's Risks section; do not duplicate prose; this register is an aggregator

### P4 Cycle log and final sync

Task 13. Write `cycles/CYCLE-20260504-001.md`.

- cycle_name: Cycle 008.5 closeout - composer upgrade, cross-spec contract, literature board v1, supporting artifacts
- declare per Discipline rule 4: primary failure modes in scope (carries forward F1, F2, F3, F6), owned actions (A5 added via Composer; existing A1-A4, A6 untouched), proxy bank unchanged, fail-fast unchanged
- list new artifacts: DEC-001, DEC-002, SPEC-004, CROSS_SPEC_SIGNAL_CONTRACT, all literature/ files, demo_storyboard template, TEACHER_AUDIENCE_PROFILE placeholder, WORK_RISK_REGISTER
- list modified artifacts per Surgical Edits log
- end with explicit "Next Discussion Points" carrying forward D3 (deferred) and the new decisions surfaced by Composer / cross-spec contract

Task 14. Update `WORKFLOW_STATUS.md`.

- bump Last updated to 2026-05-04
- Active Workstreams: add SPEC-004 row, cross-spec contract row, literature board row, work risk register row, demo storyboard template row, teacher audience profile row
- Recommended Next User Decision: replace the four-point list with the now-accurate state:
  - D1 locked (Critic first); D2 locked (Composer upgrade done); D4 locked (90-120 min budget)
  - D3 deferred per DEC-20260504-002; surfaces again after cycle 009 case-card data
  - new open decisions from Composer SPEC and cross-spec contract (each spec ends with its own next discussion point; aggregate them here)
- Blocked Until User Decision: unchanged

Task 15. Update `RESEARCH_STATE.md`.

- bump Last updated
- append a new section "Cycle 008.5 Closeout And Cycle 009 Prep" mirroring the cycle log; explicitly note that this is a sub-cycle within the cycle 008 numbering and not a new substantive research-process cycle (keeps Discipline rule 3 honest about counter divergence)

Task 16. Final cross-link verification.

- grep for any reference to "60 minutes" inside `specs/` directory; should be zero after Task 4
- grep for any new file path that is not referenced from `INDEX.md`; should be zero
- check `AGENT_MASTER_PROMPT.md` mandatory load protocol covers: literature/INDEX.md, paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md, paradigm/TEACHER_AUDIENCE_PROFILE.md
- check `registry/decision_registry.md` has both DEC-20260504-001 and DEC-20260504-002 rows
- check `registry/research_unit_registry.md` RU-002 row reads `spec_drafted (linked to SPEC-20260504-001)`

## Dependency graph

Tasks should be executed roughly in P0 -> P1 -> P2 -> P3 -> P4 order, but within each priority the agent may parallelize where files do not touch each other.

Hard dependencies:

- Task 5 (Composer SPEC) depends on Task 6 (cross-spec contract) being at least drafted because it cites the contract
- Task 8 literature SPINE files depend on Task 5 being drafted because SPINE_COMPOSER references SPEC-20260504-001
- Task 13 (cycle log) depends on all earlier tasks because it lists their artifacts
- Task 14, 15, 16 (final sync) depend on Task 13

Soft dependencies (efficiency only):

- Task 1, 2, 3 (decision memos and registry) can run before or after Task 4 (SPEC budget edits)
- Task 10, 11, 12 (templates / placeholder / risk register) can run any time after P1

## Verification checklist before closing the session

The receiving agent must self-verify before declaring the session complete:

1. All 16 tasks above are marked done
2. All new files referenced from `INDEX.md` and at least one of `WORKFLOW_STATUS.md` / `README.md`
3. `AGENT_MASTER_PROMPT.md` mandatory load protocol updated to include the four new mandatory files (specs/ already covered as a category in cycle 008; this session adds CROSS_SPEC_SIGNAL_CONTRACT, TEACHER_AUDIENCE_PROFILE, literature/INDEX, plus the SPEC-004 path under specs/)
4. No file under `specs/` mentions "60 minutes" as the annotation cap
5. `registry/decision_registry.md` has the two new DEC rows
6. `registry/research_unit_registry.md` RU-002 row says `spec_drafted`
7. `cycles/CYCLE-20260504-001.md` exists and lists all artifacts created or modified this session
8. No retro-renumbering of pre-existing cycle counters; numbering divergence remains documented in RESEARCH_STATE rather than silently fixed
9. No artifact claims paper-proven status for an unverified mechanism; all new mechanism / contract / capability claims carry `inferred` or `unknown`
10. The agent has not invented teacher audience profile content; the placeholder file lists fields and explicitly asks the user to fill them

## What to surface back to the user at session end

A short summary message containing:

- list of new artifacts (with paths)
- list of modified artifacts (with one-line reason each)
- the still-open decisions the user must make next:
  1. fill `paradigm/TEACHER_AUDIENCE_PROFILE.md` so D3 demo target can be unblocked
  2. authorize cycle 009 to start filling case cards (CASE-20260504-CRITIC-01..03 first, per D1)
  3. any literature board content that needs user-side input (e.g. specific papers to add to a SPINE that the agent did not include)

Do not push a recommendation on D3 in the closing summary. The decision was deliberately deferred per DEC-20260504-002.

## Files this handoff produces or modifies

Create:

- `decisions/DEC-20260504-001-composer-finalist-upgrade.md`
- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`
- `specs/SPEC-20260504-001-3r-composer.md`
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`
- `paradigm/TEACHER_AUDIENCE_PROFILE.md`
- `literature/INDEX.md`
- `literature/SPINE_CRITIC.md`
- `literature/SPINE_MEMORY.md`
- `literature/SPINE_PERMANENCE.md`
- `literature/SPINE_COMPOSER.md`
- `literature/CRITICAL_NOTES.md`
- `literature/PAPER_RELATED_WORK_SKELETON.md`
- `templates/demo_storyboard.md`
- `planning/WORK_RISK_REGISTER.md`
- `cycles/CYCLE-20260504-001.md`

Modify:

- `AGENT_MASTER_PROMPT.md`
- `WORKFLOW_STATUS.md`
- `RESEARCH_STATE.md`
- `INDEX.md`
- `README.md`
- `registry/decision_registry.md`
- `registry/research_unit_registry.md`
- `units/RESEARCH_UNIT_BANK.md`
- `specs/SPEC-20260503-001-geometry-critic.md`
- `specs/SPEC-20260503-002-executive-memory.md`
- `specs/SPEC-20260503-003-dynamic-object-permanence.md`

Total: 15 new files + 11 modified files.

## Out of scope for this session (do not do)

- pick a teacher demo target
- fill TEACHER_AUDIENCE_PROFILE content
- start any case card (CASE-* files); cycle 009 begins the case-card phase, not this session
- touch any KYKT app code
- reproduce, train, fine-tune, or download any checkpoint
- retro-renumber RESEARCH_STATE vs cycle log counters
- discard any non-finalist track (Cross-Modal, Active Perception remain alive at lower priority)
