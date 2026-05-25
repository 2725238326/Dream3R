# DEC-20260525-005 - Deferred Cross-Dataset Stage 5 S1 Validation

## Status

Deferred. Stage 5 S1 closes at DEC-20260525-003 (59-window KITTI expanded).
Cross-dataset validation is recorded as future work, not implemented.

## Context

After Stage 5 S1 expanded closure (DEC-20260525-003) produced 78% LOO route
accuracy on 59 KITTI windows, the natural next step was cross-dataset
evidence. ETH3D Low-res many-view was the proposed target because the five
training scenes mix indoor/outdoor with metric depth ground truth, which
matches the existing KITTI long-window oracle interface.

On 2026-05-25 we attempted to bring ETH3D onto the server:

- Server `curl https://www.eth3d.net/...` timed out (TCP unreachable). Same
  symptom as `ping eth3d.net` 100% loss and `ping github.com` 100% loss.
  The server is in China (BUAA) and only reaches Baidu and PyPI mirrors
  reliably.
- User offered to download locally then scp to server. After inspecting
  eth3d.net file sizes (High-res multi-view bulk ~7 GB; Low-res many-view
  five-scene total ~250-350 MB), user declined: both local download
  bandwidth and upload-to-server bandwidth are constrained.

## Decision

Defer cross-dataset validation. Close Stage 5 S1 at the 59-window KITTI
expanded closure (DEC-20260525-003) as the final headline evidence for
this stage.

## Rationale

### 1. Network is the binding constraint, not engineering

The pending code work (ETH3D dataloader, oracle build parameterization,
cross-domain eval) is straightforward and could be written in hours. None
of it yields a closure number without ETH3D data on the server. Writing
the code without data would be speculative work, not validated evidence.

### 2. The current closure evidence is already honest and bounded

DEC-20260525-003 claims:

- 7.60% relative improvement over best single expert on 59-window
  closure set
- 78% LOO route accuracy held-out (vs 33% chance on 3-class)
- 2.23% relative abs_rel improvement held-out (below 5% gate)
- Explicit non-claims: not SOTA, not cross-dataset

This is a defensible in-domain generalization claim. The remaining
cross-domain ask is strictly stretch, not part of the S1 closure bar.

### 3. Project goal is demo, not unified architecture or SOTA

`mainwork.md §0` reads "default goal: working demo (option 2)... not SOTA,
every number real." Cross-dataset evidence is not required for the demo
bar. It would be required for option 1 (conference) or option 4
(proposal-grade cross-domain claim), neither of which is the active goal.

### 4. Time budget

User asked for closure on 2026-05-25 evening. Even a minimal one-scene
ETH3D path is 3-5 hours server-side after data arrives (dataloader,
oracle build, router transfer eval). The deferral keeps the closure on
the requested timeline.

## What is preserved for future pickup

When the trigger fires, the future agent should be able to start without
re-deriving the plan:

- **Target dataset**: ETH3D Low-res many-view training set (5 scenes:
  delivery_area, electro, forest, playground, terrains).
- **Required upload path**:
  `/hdd3/kykt26/data/eth3d/low_res_many_view/training/<scene>/`
- **Files needed per scene**: `<scene>_dslr_undistorted.7z` (images) +
  `<scene>_dslr_depth.7z` (depth ground truth). Total ~250-350 MB.
- **Code work pending**:
  - `code/dream3r/data/eth3d_long.py`: mirror `KITTILongSequenceDataset`
    interface (return dict with images, depth_gt, valid_mask,
    pointmap_gt, pointmap_mask, intrinsics, camera_poses, regime,
    conflict_label, repair_label, region_label).
  - `code/dream3r/scripts/build_oracle_expert_labels.py`: parameterize
    dataset factory so the same oracle build script handles KITTI and
    ETH3D without code duplication.
  - `code/dream3r/scripts/eval_cross_domain_router.py`: load the
    Stage 5 S1 expanded checkpoint
    (`/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt`),
    forward on ETH3D windows, report (a) route distribution shift vs
    KITTI, (b) abs_rel relative to per-window oracle on ETH3D, (c)
    relative improvement vs ETH3D best-single-expert.
- **Evaluation questions**:
  1. Does the 59-window KITTI router maintain meaningful route accuracy
     when evaluated on ETH3D windows, or does the regime->expert mapping
     shift entirely with the domain?
  2. Is "best single expert" on ETH3D the same as on KITTI (MASt3R), or
     does the dominant expert change? A different dominant expert
     would itself be cross-dataset evidence even if the router degrades.
- **Risk register**:
  - ETH3D regime distribution may not overlap KITTI's regime set
    (indoor static scenes vs outdoor driving). The router input depends
    on regime probabilities, so a non-overlapping regime support is
    itself a finding.
  - Expert checkpoints (MASt3R, Spann3R, Fast3R) were trained mostly on
    outdoor and DUSt3R-style data; their relative ranking on ETH3D
    indoor scenes is an open empirical question.

## Trigger conditions

Pick this back up when ANY of the following becomes true:

1. **Network access**: Server gains stable access to eth3d.net or a
   Chinese academic mirror hosting ETH3D Low-res many-view.
2. **User bandwidth**: User has the local download + upload bandwidth
   for ~300 MB of Low-res many-view archives.
3. **Goal shift**: Project goal moves from demo to conference paper or
   to a cross-dataset claim that requires this evidence.

Until one of these fires, the Stage 5 S1 closure rests on DEC-20260525-003
alone, with cross-dataset explicitly listed as future work.

## Boundary

This decision changes nothing in code. Server artifacts, checkpoints,
docs, and tests from DEC-20260525-001 through DEC-20260525-004 remain
authoritative.
