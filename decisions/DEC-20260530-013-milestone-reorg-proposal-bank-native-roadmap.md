# DEC-20260530-013 — Reorganize Dream3R as a model roadmap, not a loose fusion script

decision_id: DEC-20260530-013
date: 2026-05-30
scope: Dream3R post-midterm milestone reorganization
status: accepted for planning and next-task routing; implementation remains gated

## Context

DEC-011 and DEC-012 make the immediate evidence clear:

- hard expert selection is not the Dream3R model;
- bounded SCF over real Fast3R / MASt3R / Spann3R proposals works;
- correct state beats no-state and shuffled-state, but temporal/scale
  behavior is not yet solved.

The remaining risk is narrative and execution drift: treating Dream3R as a
bag of external 3R models plus a small head. That is not enough. Dream3R must
be organized as a staged 3R model roadmap.

## Decision

Dream3R is now organized as:

```text
Dream3R = proposal encoders + Dream state + state-conditioned reconstruction decoder
```

The near-term model family is:

```text
v2.0 Proposal-bank Dream3R
  real Fast3R / MASt3R / Spann3R proposals
  + current Dream state
  + bounded SCF decoder

v2.2 Expanded proposal-bank Dream3R
  v2.0 core bank
  + admitted high-complementarity candidates:
    VGGT-Omega, CUT3R, MonST3R
  + candidate-aware state-conditioned reconstruction decoder

v2.3 Trained-state Dream3R
  frozen proposal bank
  + trained state projection / Critic calibration
  + temporal / scale objectives

v3.0 Native Dream3R
  proposal bank becomes teacher;
  Dream3R learns a native reconstruction decoder that can run with partial or
  dropped external proposals.
```

## Expert-bank decision

Keep the current proven real bank:

| expert | role |
| --- | --- |
| MASt3R | static/pairwise high-quality matching proposal |
| Fast3R | many-view fast feed-forward proposal |
| Spann3R | memory-like/global-coordinate proposal |

Prioritize only three next candidate families:

| candidate | why it is worth admission | immediate status |
| --- | --- | --- |
| VGGT-Omega | upgraded VGGT-family visual-geometry foundation; preferred over vanilla VGGT for v2.2 admission if its real backend can be deployed | admission probe first; checkpoint/run gated |
| CUT3R | persistent-state continuous 3D perception; directly aligned with Dream3R's original state-memory thesis | admission probe first; checkpoint/run gated |
| MonST3R | dynamic-scene pointmap proposal; fills the current dynamic/Permanence gap | admission probe first; checkpoint/run gated |

Do not prioritize these as immediate proposal experts:

| candidate | reason |
| --- | --- |
| Test3R / TTT3R | use as slow verifier/refinement or teacher, not default proposal |
| DepthAnything / MoGe / Depth Pro / Metric3D | useful monocular priors, but not enough as core 3R proposals |
| vanilla VGGT | keep as baseline / schema ancestor; superseded by VGGT-Omega as first v2.2 admission target |
| STream3R / InfiniteVGGT / SwiftVGGT / RobustVGGT | important streaming/VGGT-family comparators; use as design pressure and later candidates after v2.2 |
| OVGGT | memory/cache comparator for constant-budget cache compression; not the same as VGGT-Omega |
| 3DGS / Splatt3R family | output/rendering target, not the next reconstruction core |

## Reconstruction-decoder decision

The next Dream3R-owned component should be a **State-Conditioned
Reconstruction Decoder**, not another hard router:

```text
proposal tokens
+ proposal confidence
+ expert identity / cost / backend
+ Memory / Anchor / NSA state
+ Permanence / Critic reliability
-> bounded fusion weights
-> final pointmap + confidence + diagnostics
```

SCFHead is the v0 decoder. The next implementation should be non-core and
proposal-cache based before any frozen-core edit:

1. frozen-state projection / Critic calibration;
2. proposal-set transformer decoder;
3. temporal/scale objective;
4. native decoder distillation only after the previous gates pass.

## External-source checkpoint

Checked on 2026-05-30:

- VGGT: https://github.com/facebookresearch/vggt and
  https://arxiv.org/abs/2503.11651
- VGGT-Omega: https://vggt-omega.github.io/ and
  https://github.com/facebookresearch/vggt-omega
- CUT3R: https://cut3r.github.io/ and https://github.com/CUT3R/CUT3R
- Fast3R: CVPR 2025 paper at
  https://openaccess.thecvf.com/content/CVPR2025/papers/Yang_Fast3R_Towards_3D_Reconstruction_of_1000_Images_in_One_Forward_CVPR_2025_paper.pdf
- Spann3R: https://arxiv.org/abs/2408.16061 and
  https://github.com/HengyiWang/spann3r
- MonST3R: https://arxiv.org/abs/2410.03825 and
  https://monst3r-project.github.io/files/monst3r_paper.pdf
- STream3R: https://arxiv.org/abs/2508.10893
- InfiniteVGGT: https://arxiv.org/abs/2601.02281

These sources are used for routing and candidate admission only. No new
checkpoint download, install, or benchmark is authorized by this DEC.

## Rejected alternatives

- Add every available 3R model into the bank: too slow and makes causality
  unreadable.
- Go back to hard routing: already demoted by DEC-009/011.
- Claim Dream3R is better than VGGT-Omega/CUT3R/STream3R globally:
  unsupported.
- Jump directly to native decoder training: premature without proposal-bank
  teacher evidence and state-training gates.

## Next executable task

Start with a **non-core v2.2 admission plan**:

1. define adapter/cache contracts for VGGT-Omega, CUT3R, MonST3R;
2. define admission metrics against the current SCF bank;
3. implement no checkpoint download or server run until a separate DEC
   authorizes it.
