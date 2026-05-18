# Planning addendum v0.3 — Checkpoint inventory for uninventoried experts

addendum_id:    PLANNING_ADDENDUM_V03_CHECKPOINT_INVENTORY
date:           2026-05-07
cycle:          023 (S2 deliverable; per DEC-20260507-003)
addresses:      RA-05 [HIGH] from Path C Agent B review (cycle 022)
parent_artifact: planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (cycle 020; NOT modified)
rule:           B-roadmap-F (no in-place modification; NEW addendum file)
source:         COMPOSER_CAPABILITY_DESCRIPTORS.md + paper-known checkpoint metadata

---

## Problem statement

Path C Agent B (cycle 022) identified that 3 of 7 expert checkpoints are "NOT yet
inventoried" in the IMPLEMENTATION_ROADMAP. Without confirmed checkpoint availability,
license status, and VRAM footprint, T-v02-EXPERT-4/5/6 tasks and ABL-v02-4 (Composer
best-of-N) are at risk of stalling the Tier 3+4 execution chain.

This addendum inventories the 3 uninventoried experts and the 4 already-known experts
for completeness.

## Checkpoint inventory

### Already inventoried (confirmed available)

| Expert | Checkpoint source | Params | Disk size (est.) | VRAM fp16 | License | Status |
|---|---|---|---|---|---|---|
| EXPERT-01 MASt3R | naver/mast3r (GitHub) | ~300M | ~1.2 GB | ~600 MB | CC BY-NC-SA 4.0 (non-commercial) | confirmed (cycle 015 Critic L3 pilot used MASt3R-adjacent infrastructure) |
| EXPERT-02 Fast3R | fast3r official (GitHub) | ~580M | ~2.3 GB | ~1.2 GB | Apache 2.0 | confirmed (paper-known; HuggingFace release) |
| EXPERT-03 Spann3R | hengyiwang/spann3r (GitHub) | ~250M | ~1.0 GB | ~500 MB | MIT | confirmed (paper-known; official release) |
| EXPERT-07 Test3R | test3r official (GitHub) | backbone + iteration | ~1.5 GB | ~800 MB (varies with iterations) | Apache 2.0 | confirmed (paper-known) |

Evidence label: paper-known for checkpoint source + params; engineering-judgment for
disk/VRAM estimates (based on published model sizes, not measured on dream3r server).

### Newly inventoried (this addendum)

| Expert | Checkpoint source | Params | Disk size (est.) | VRAM fp16 | License | Status | G_download gate |
|---|---|---|---|---|---|---|---|
| EXPERT-04 CUT3R | CUT3R official repo (GitHub; paper 2025) | ~300M | ~1.2 GB | ~600 MB | Apache 2.0 (paper-derived; verify at download) | **unverified** — paper lists official release; checkpoint URL needs confirmation at G_download time | required per F-002 |
| EXPERT-05 MoGe-2 | microsoft/MoGe (GitHub; Microsoft Research) | ~200M | ~800 MB | ~400 MB | MIT (paper states; verify at download) | **unverified** — Microsoft GitHub release paper-known; checkpoint availability needs confirmation at G_download time | required per F-002 |
| EXPERT-06 DepthAnything-V2 | depth-anything/Depth-Anything-V2 (GitHub + HuggingFace) | ~25M (Small) | ~100 MB (Small) | ~50 MB (Small) | Apache 2.0 | **likely available** — DepthAnything V2 is widely used; HuggingFace hub has multiple model sizes; Small is default for Dream3R v0.2 streaming budget | required per F-002 |

Evidence label: paper-derived for checkpoint source, params, and license (from published
papers and README files); engineering-judgment for disk/VRAM estimates; **unverified** for
actual download URL and checkpoint file integrity.

## Risk assessment per expert

```text
EXPERT-04 CUT3R:
  Risk level: MEDIUM.
  The CUT3R paper (2025) reports an official GitHub release. However,
  some 2025 3R papers have delayed or partial checkpoint releases.
  Mitigation: G_download DEC must include a "verify checkpoint exists
  and loads" step before authorizing T-v02-EXPERT-4.
  Fallback if unavailable: Spann3R (EXPERT-03) covers a similar
  streaming regime; route_regret analysis with 6 experts instead of 7.

EXPERT-05 MoGe-2:
  Risk level: LOW-MEDIUM.
  Microsoft Research releases are generally well-maintained. MoGe-2
  (the "v2" of MoGe) has a published GitHub repo. The main risk is
  that the model may be large (ViT-L based, ~200M) and may require
  a specific weight format (safetensors vs .pth). TITAN RTX 24GB
  can handle 200M fp16 alongside other loaded models, but VRAM
  scheduling needs attention if multiple experts are loaded simultaneously.
  Mitigation: lazy loading per expert (only load when routing policy
  selects); shared backbone if applicable.

EXPERT-06 DepthAnything-V2:
  Risk level: LOW.
  DepthAnything V2 is one of the most widely used mono depth models;
  HuggingFace has official checkpoints for -S/-B/-L sizes. The Small
  variant (~25M) is negligible in VRAM. License is Apache 2.0.
  Mitigation: none needed; straightforward download.
```

## VRAM budget analysis (all 7 experts loaded simultaneously)

```text
NOT recommended to load all 7 simultaneously. TITAN RTX 24GB budget:

  DINOv3-S backbone (C1):     ~50 MB
  C2 Memory + NSA:            ~300 MB (inferred)
  C3 Permanence:              ~200 MB (inferred)
  C4 Critic:                  ~100 MB (inferred)
  Subtotal (core architecture): ~650 MB

  All 7 experts loaded:
    MASt3R:         ~600 MB
    Fast3R:         ~1200 MB
    Spann3R:        ~500 MB
    CUT3R:          ~600 MB
    MoGe-2:         ~400 MB
    DepthAnything:  ~50 MB
    Test3R:         ~800 MB
    Subtotal (experts): ~4150 MB

  Total (core + all experts): ~4800 MB (~4.7 GB)
  Remaining VRAM for activations, optimizer states: ~19 GB
  Verdict: fits in TITAN RTX 24GB for inference-only streaming.

  For training (optimizer states + gradients):
  Only subset of experts are trainable (adapters only; expert
  backbones frozen). Core architecture training (C1-C6): needs
  ~8-12 GB for gradients + optimizer. Still fits with lazy
  expert loading. See T-v02-F for training VRAM analysis.
```

Evidence label: engineering-judgment. All numbers are estimates from published
param counts + standard fp16 conversion. Actual VRAM depends on batch size,
sequence length, and CUDA memory allocator behavior. Promotion to measured
requires bench_frame_budget.py execution under a separate DEC.

## Pre-execution checklist addition for T-v02-EXPERT-4, -5, -6

Per RA-05, the following checklist items should be added to the pre-execution
review checklists of T-v02-EXPERT-4, T-v02-EXPERT-5, and T-v02-EXPERT-6 in
a future IMPLEMENTATION_ROADMAP v0.3 addendum:

```text
[ ] Verify checkpoint URL is accessible (wget/curl test; no 404).
[ ] Verify downloaded checkpoint loads without error (torch.load +
    model.load_state_dict; verify key match).
[ ] Verify checkpoint license is compatible with project use
    (non-commercial MASt3R precedent: acknowledged in COMPOSER
    descriptors; other experts must be Apache/MIT/similar).
[ ] Verify VRAM footprint matches estimate in this inventory
    (within 20% tolerance).
[ ] Verify checkpoint is stored under /hdd3/kykt26/ per lab rules
    (not in home directory).
```

## Version history

```text
v1  2026-05-07  cycle 023. Addresses RA-05 from Path C Agent B.
                Checkpoint inventory for EXPERT-04 CUT3R, EXPERT-05
                MoGe-2, EXPERT-06 DepthAnything-V2. VRAM budget
                analysis. Pre-execution checklist additions proposed.
```
