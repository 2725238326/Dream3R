# Work Risk Register

Last updated: 2026-05-16 (cycle 036; v1.2 additive — 3 Dream3R proposal dual-draft cross-spec risk rows appended; v1.1 + v1 substance unchanged)

Status: consolidated risk view across the four finalist specs and the cross-spec contract.

## Purpose

Each finalist spec already has its own `Risks` section. This register aggregates them and adds the cross-SPEC risks that no single spec can own (annotation budget overflow across four parallel case-card passes, signal contract drift, numbering reconciliation, teacher audience uncertainty, etc.).

This file is an aggregator. It does **not** duplicate per-spec risk prose. It links to each SPEC's `Risks` section.

## Reading Rule

- Per-SPEC risks: read the SPEC's own Risks section.
- Cross-SPEC risks: read this file.
- Triggers and current-status columns are updated when state changes; the register does not silently age.

## Per-SPEC Risk Pointers

| SPEC | Risks section pointer | Last reviewed |
|---|---|---|
| SPEC-20260503-001 Geometry Critic | `specs/SPEC-20260503-001-geometry-critic.md` Risks section | 2026-05-04 (cycle 008.5; budget edits applied) |
| SPEC-20260503-002 Executive Memory | `specs/SPEC-20260503-002-executive-memory.md` Risks section | 2026-05-04 (cycle 008.5; budget edits applied) |
| SPEC-20260503-003 Dynamic Object Permanence | `specs/SPEC-20260503-003-dynamic-object-permanence.md` Risks section | 2026-05-04 (cycle 008.5; budget edits applied) |
| SPEC-20260504-001 3R Composer | `specs/SPEC-20260504-001-3r-composer.md` Risks section | 2026-05-04 (cycle 008.5; new spec) |

## Cross-SPEC Risk Table

| Risk | Source SPEC | Trigger | Current status | Owner |
|---|---|---|---|---|
| Annotation budget overflow across four parallel case-card passes | all four | aggregate cycle 009 annotation effort exceeds (4 specs * 3 case cards * 90-120 minutes) ceiling | open; cycle 009 not yet started | Dream agent + user gate (user must authorize rescue allocation if hit) |
| Cross-spec signal contract drift | Critic + Memory + Permanence + Composer | a case card consumes a contract signal whose semantics differ from the producer's published definition | open; v1 contract not yet exercised; cycle 009 case cards are first test | Dream agent (records new contract version) |
| Critic A5 reroute_model depends on Composer capability_match before Composer case cards land | Critic + Composer | Critic case cards in cycle 009 (D1 = Critic first) read a Composer signal whose evidence label is `inferred` and unverified | open; mitigated by per-card evidence-label propagation (CR-5) | Dream agent (must record evidence label in Critic case card) |
| Memory honor of Permanence suppress_static_write fails | Memory + Permanence | Memory's A2 ignores or partially honors a Permanence suppress flag | open; mitigated by CR-2 logged-refusal rule | Dream agent (must surface to Advisor on refusal) |
| Numbering reconciliation: RESEARCH_STATE running counter (Cycle 010) vs cycle log running counter (cycle 008) | RESEARCH_STATE + cycle log | future cycle reads diverge and a reader picks one as authoritative | accepted divergence per cycle 008 documentation; no rename allowed without dedicated cycle | Dream agent (must not silently fix) |
| Teacher audience uncertainty blocks D3 | demo storyboard template + DEC-20260504-002 | user has not populated `paradigm/TEACHER_AUDIENCE_PROFILE.md` when D3 is asked | open; expected; mitigated by explicit deferral | user (must populate to unblock) |
| Single-finalist drift via case-card prioritization order | DEC-20260504-002 | Critic case cards land first (per D1) and the agent describes Critic as "leading" rather than "executing first" | open; mitigated by explicit cycle-log reminder and DEC-20260504-002 | Dream agent (must keep D1 = execution order, not preference) |
| Capability card staleness | Composer | a comparator paper publishes a new regime claim mid-cycle | open; mitigated by version stamp on each capability_card | Dream agent (must update via cycle log, not silently) |
| Composer demo is text-heavy compared to Permanence visual demo | Composer + (when D3 is unblocked) | demo target choice biases toward visual finalist | open; mitigated by pairing Composer with Critic timeline panel | user gate via D3 |
| Cycle 009 four-parallel-track scope creep | all four | one finalist's case cards expand and crowd out others | open; mitigated by per-card 90-120 min cap and per-spec fail-fast thresholds | Dream agent (must surface overrun before silent re-allocation) |
| Honest-evidence drift on cross-domain analogs (MoE for Composer; CTRL for Critic) | Composer + Critic | a case card cites MoE / CTRL as a 3R comparator rather than as a cross-domain analog | open; mitigated by `literature/CRITICAL_NOTES.md` deconfusion entries and SPINE files | Dream agent (must keep label `inferred` for cross-domain borrows) |
| Composer retire-to-support outcome conflicts with DEC-20260504-001 finalist authorization | Composer | Composer hits its fail-fast (zero spread) and retires to support layer | acceptable per Composer SPEC fail_fast_threshold; not a contract violation; documented retirement does not require re-authorization | Dream agent (records via decision memo, not silent edit) |
| 4DGS / asset axis bleed into Permanence | Permanence | demo or case-card pressure pulls 4DGS asset rendering back in | mitigated by SPEC-003 explicit out-of-scope clause; agent must refuse and surface to user | Dream agent (must refuse; user gate) |
| R-OOD-1: OOD detection path absent in C4 Critic | SPEC-20260506-004 v0.2 §C4 Critic + Dream3R v0.3 mainline | a real-data window from outside the training distribution (indoor + urban KITTI/ScanNet) silently passes Critic acceptance with confidence_drop unflagged; Composer routes to wrong expert because route_regret_estimate stays low | open; surfaced 2026-05-15 by survey-driven optimization proposal §4 P0-4; mitigated only by `planning/CRITIC_CALIBRATION_PLAN_V1.md` A6 mode in the calibration plan (plan-only, execution gated) | Dream agent (must not promote OOD detection to v0.4 finalist without DEC; per DEC-20260504-002 no-all-in) |
| R-EXT-PRIOR-1: External prior vs geometry conflict unmodeled in CR-1..CR-6 | CROSS_SPEC_SIGNAL_CONTRACT v2.1 + Composer SPEC-20260504-001 | a future C5 Composer prior-adapter (Depth Pro / Metric3Dv2 / SAM2 / DINO / CoTracker / SpatialTracker) emits a prior that conflicts with C2 Memory pointmap or C4 Critic conflict_score; no CR rule defines resolution priority | open; surfaced 2026-05-15 by survey-driven optimization proposal §4 P1-4 + §5 C2 "CR-7 候选: external_prior_conflict"; mitigated only if v0.4 spec delta B3 (input extension axis) lands a contract upgrade to v2.2 | Dream agent (must not silently introduce prior-adapter without v0.4 spec delta + DEC; contract version bump non-trivial) |
| R-4DGS-LIC-1: 4DGS asset license chain undocumented in W18 GaussianHead | SPEC-20260506-004 v0.2 §C-output (placeholder) + W18 GaussianHead tensor contract | a downstream renderer consumer (W27 gated) inherits W18 tensor output and reuses a Gaussian splatting renderer with viral / restricted license (e.g., Splatt3R / InstantSplat lineage); license incompatibility surfaces only at integration | open; surfaced 2026-05-15 by survey-driven optimization proposal §4 P1-2 + §5 B2; W18 currently labels tensor contract only, no license metadata; mitigated by W27 renderer remaining gated per `code/dream3r/NEXT_PHASE_ROADMAP.md` | Dream agent (must not promote W27 from gated to draft without per-renderer license review DEC; user gate on any 4DGS asset publication) |
| R-INPUT-EXT-1: Input extension axis (pose / sparse depth / video timestamp) first-class absent | SPEC-20260506-004 v0.2 §C1 Perceiver + §C5 Composer | a comparator point with G-CUT3R / Pow3R / MASt3R-SfM / Splatt3R-style first-class prior input becomes the benchmark Dream3R must beat; Dream3R cannot enter the comparison because it only accepts images + sequence | open; surfaced 2026-05-15 by survey-driven optimization proposal §3 (input extension bonus axis) + §4 P1-3 + `planning/SOTA_MATRIX_V2.md` §6.5; mitigated only if v0.4 spec delta B3 lands `input_priors` tensor channel | Dream agent (must not silently extend C1 / C5 input contract without v0.4 spec delta + DEC; impacts C1 + C5 + CR contract simultaneously) |
| R-PROP-VOCAB-1: 外部稿 Dream-vocabulary leakage | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` (cycle 036+) | grep on external draft returns any hit on `Dream\|Dream3R\|KYKT\|agent\|skill\|workflow\|本地项目\|cycle\|SPEC-\|DEC-\|CR-` during double-draft editing window; risk increases with each cycle that touches `proposal_dream3r/` | open; surfaced 2026-05-16 by cycle 036 dual-draft kickoff; mitigated by `planning/proposal_dream3r/STYLE_CONTRACT.md` §2 vocab substitution table + §3 sync rule + per-sync grep verification; cycle 036 close passed verification with 0 hits on full pattern; cycle 037+ inherits the same gate | Dream agent (must run grep before each cycle close that touches `proposal_dream3r/`) |
| R-PROP-CLAIM-1: 开题报告 over-claim 候选架构 X 为最终方案 | `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` + `DRAFT_INTERNAL_V1.md` | any of `证明.{0,10}优于` / `最佳.{0,5}架构` / `最终.{0,5}架构` / `X 解决了` / `Dream3R 解决了` patterns appear in claim-bearing prose; risk increases as §3 / §6 (research questions + expected outcomes) are drafted in cycle 039 | open; surfaced 2026-05-16 by cycle 036 dual-draft kickoff; mitigated by `STYLE_CONTRACT.md` §5 candidate-not-final 句式对比表 + per-cycle grep verification on draft §1-§N as they land; cycle 036 close passed verification with 0 hits on both internal and external §1 | Dream agent + cycle reviewer (must apply §5 句式表 + verify before each draft section close) |
| R-PROP-SYNC-1: 双稿语义漂移 | `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` vs `DRAFT_EXTERNAL_V1.md` | internal-vs-external §X 对同一研究问题的描述出现实质性差异 (新增 example / 删除 claim / 不同 metric 数值); risk increases as sections drafted out of order or external draft edited standalone in violation of `STYLE_CONTRACT.md` §3 规则 3 | open; surfaced 2026-05-16 by cycle 036 dual-draft kickoff; mitigated by `STYLE_CONTRACT.md` §3 sync rule (internal-is-master + 周期性 external 快照 + §6 sync log) + 外部稿 standalone 编辑限制 | Dream agent (must run sync + append sync log entry at end of any cycle that edits `proposal_dream3r/` drafts) |

## Trigger Conditions In Detail

### Annotation budget overflow

The aggregate worst case is 4 specs × 3 case cards × 120 minutes = **24 hours of human annotation** in cycle 009. Realistic median is ~2/3 of that (~16 hours) given Critic's actual labeling load is below ceiling. If aggregate exceeds 16 hours mid-cycle, surface to the user before re-allocating. Per DEC-20260504-002, no agent-side preference selection.

### Contract drift

The cross-spec signal contract `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v1 has six conflict resolution rules. Each cycle 009 case card must list which signals it consumed and the producer's evidence label at consumption time. If two case cards interpret the same signal differently, the contract must be revised (new version), not silently patched.

### Numbering reconciliation

`RESEARCH_STATE.md` uses sequential per-section headers (Cycle 010 entry covers what cycle 008 cycle log calls cycle 008). This divergence is documented in `cycles/CYCLE-20260503-002.md` "Running counter" note. No retro-renumbering without a dedicated cycle, per Discipline rule 3 (Surgical Edits).

### Teacher audience uncertainty

`paradigm/TEACHER_AUDIENCE_PROFILE.md` is a placeholder file. While empty, D3 stays deferred. The agent must not invent values.

## Current Status Summary

- Cycle 008.5 is closing; cycle 009 has not started.
- All risks above are **open** in the sense that cycle 009 has not yet exercised them.
- No risk has triggered yet; this register's value is to make triggers visible *when* they happen rather than after.

## Companion Files

- `paradigm/RESEARCH_CODE_DISCIPLINE.md` — rules 3 and 5 govern this register's behavior
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` — defines the signal-drift risk
- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` — defines the no-all-in posture risk
- each finalist SPEC's Risks section — primary source for per-SPEC risk prose
- `cycles/CYCLE-20260504-001.md` — closing entry that lists which risks were updated this cycle
