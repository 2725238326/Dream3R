# SPEC-20260530-003 — Dream3R reconstruction-decoder roadmap

status: accepted roadmap; implementation gated
date: 2026-05-30
depends_on: DEC-20260530-011, DEC-20260530-012, DEC-20260530-013

## Purpose

This spec reorganizes Dream3R from "expert selection plus fusion scripts" into
a staged 3R model:

```text
images -> proposal encoders -> Dream state -> reconstruction decoder -> pointmap
```

The goal is to keep the original architecture's Memory / Anchor / NSA /
Permanence / Critic / Composer intent, while fixing the old failure mode where
the final output collapsed to one selected external expert.

## Model definition

Dream3R owns the reconstruction decision:

```text
Input:
  images
  optional camera/meta hints

Proposal encoders:
  expert_i(images) -> pointmap_i, confidence_i, method_state_i

Dream state:
  Memory / AnchorBank / NSA / Permanence / Critic / Composer prior

Reconstruction decoder:
  proposal set + Dream state -> final pointmap, confidence, diagnostics
```

The external 3R models are **proposal encoders**, not the whole Dream3R model.
The Dream3R-owned model component is the state-conditioned reconstruction
decoder plus the state machinery that conditions it.

## Expert bank

### Accepted core bank

| expert | role in Dream3R | current evidence |
| --- | --- | --- |
| MASt3R | high-quality static/pairwise matching proposal | real proposal in SCF bank |
| Fast3R | many-view fast proposal | real proposal in SCF bank |
| Spann3R | memory-like/global-coordinate proposal | real proposal in SCF bank |

### Next admission candidates

| candidate | admission purpose | expected complement |
| --- | --- | --- |
| VGGT-Omega | upgraded VGGT-family global feed-forward geometry foundation | camera/depth/point/track-rich proposal distinct from the current three |
| CUT3R | persistent-state proposal | tests whether an external state model improves Dream3R's state-conditioned decoder |
| MonST3R | dynamic-scene pointmap proposal | gives Permanence/Critic a real dynamic proposal to arbitrate |

Vanilla VGGT remains a baseline / schema ancestor. OVGGT is a separate
memory/cache comparator and is not interchangeable with VGGT-Omega.

### Later comparators

| candidate | use later as |
| --- | --- |
| STream3R | causal streaming baseline / teacher |
| InfiniteVGGT | endless-stream VGGT-family baseline / teacher |
| SwiftVGGT / RobustVGGT | efficiency / outlier-view robustness pressure on VGGT admission |
| OVGGT | constant-budget cache / dynamic-anchor memory comparator |
| Test3R / TTT3R | slow verifier or teacher for repair, not default proposal |
| monocular metric-depth models | scale/depth priors, not complete 3R proposal bank members by default |

## Decoder stages

### Decoder v0 — SCFHead

Current implementation:

```text
pointmaps/confidences from 3 real experts
+ memory.fused_context
+ critic.conflict_score
+ optional composer prior
-> convex weights
-> final pointmap
```

Status: positive midterm prototype.

Limit: state is useful but not yet trained as geometry state.

### Decoder v1 — Frozen-state projection

Train only non-core heads:

```text
memory.fused_context
+ critic/confidence features
-> state projection / reliability calibration
-> SCF weights
```

Pass condition:

```text
trained projection > current state > no-state / shuffled-state
```

and temporal/scale proxies must not degrade.

### Decoder v2 — Proposal-set transformer

Replace per-expert MLP weighting with a small proposal-set decoder:

```text
proposal tokens:
  expert_id, cost, backend, pointmap patch, confidence, local scale

state tokens:
  memory context, anchor summary, NSA summary, permanence summary, critic reliability

decoder:
  cross-attend proposal tokens to state tokens
  predict bounded weights and uncertainty
```

This remains non-core if trained from proposal caches.

Pass condition:

```text
beats SCFHead on abs_rel and patch_oracle_gap_pp
without worsening temporal_delta / scale_drift
```

### Decoder v3 — Native Dream3R distillation

Use the expanded proposal bank as teacher:

```text
proposal-bank oracle / SCF weights / patch oracle
-> train Dream3R native decoder with proposal dropout
```

The point of v3 is to reduce reliance on running every external model at
inference while preserving the learned state-conditioned behavior.

## Admission protocol for new experts

A new expert is admitted only if it passes all gates:

1. **contract gate**: adapter emits pointmap/confidence/backend metadata;
2. **cache gate**: cache can store outputs alongside existing SCF entries;
3. **real-backend gate**: fallback entries are excluded from result tables;
4. **complementarity gate**: candidate improves oracle or patch-oracle ceiling
   on at least one regime;
5. **decoder gate**: candidate improves Dream3R output after state-conditioned
   fusion, not just its own standalone score.

If a candidate improves standalone quality but not Dream3R output, it remains
a comparator or optional proposal, not a main architecture step.

## Immediate implementation boundary

Allowed without core edits:

- admission plan and adapter contract docs;
- cache schema extension outside frozen core;
- non-core proposal-set decoder prototype;
- evaluation scripts over cached proposals.

Gated:

- checkpoint download;
- server benchmark longer than small admission smoke;
- edits to frozen core files;
- native decoder training inside core modules.
