# Architecture Mechanism Intake

Last updated: 2026-05-02 (cycle 005)

Status: first-pass intake map; not a thesis decision.

Companion artifact:

```text
planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md
```

Use the companion file for the compact A1-A8 action set and proxy metric protocols.

## Purpose

This file prevents Dream from losing broad architecture and visual-method candidates while also preventing buzzword-driven research.

The mechanism pool also has writing value. Broad, well-organized intake helps Dream write a stronger paper by:

- showing the field is fragmented across memory, reasoning, dynamics, sensing, action, and rendering
- giving the related-work section a principled taxonomy instead of a flat paper list
- making novelty claims more defensible because each mechanism is placed against comparator pressure
- preserving high-writing-value mechanisms even when their first engineering path is not the cheapest
- creating a vocabulary for paper figures: failure modes, actions, evidence signals, and composition edges

Every new mechanism family must be translated through:

```text
Failure mode -> Mechanism -> Action -> Proxy metric -> Comparator -> Evidence level
```

Do not promote a mechanism to a branch unless it clearly addresses a 3R failure mode and has a plausible evidence path.

Do not discard a mechanism only because it is not immediately implementable. If it improves paper framing, comparator coverage, or a future evidence path, keep it as a writing / taxonomy asset with the correct evidence label.

## Comparator Completion Map

| Comparator group | Sources / models | Primary failure modes | What they already cover | Dream caution |
|---|---|---|---|---|
| Base pointmap / matching | DUSt3R, MASt3R, MASt3R-SfM | F3, F6 | pose-free pointmaps, dense matching, SfM-style alignment | not enough as a new thesis; use as baseline contracts |
| Many-view / sparse-view scale | Fast3R, MV-DUSt3R+ | F6, F3 | many-view forward pass, sparse-view RGB reconstruction, NVS support | strong composer inputs, not automatically architecture novelty |
| Spatial memory / global pointmap | Spann3R, Point3R | F1, F6 | spatial memory and explicit pointer memory for global pointmap / streaming geometry | Dream must not claim external memory itself as new |
| Stateful / streaming 3R | CUT3R, STream3R, LONG3R | F1 | persistent state, causal 3R, long-sequence memory and pruning | Dream novelty must be action governance, not generic statefulness |
| 2026 memory / cache frontier | LoGeR, Mem3R, PAS3R, FILT3R, LongStream, OVGGT | F1, F3 | hybrid memory, pose-adaptive update, Kalman-style filtering, gauge / cache / anchor handling | comparator pressure is high; action taxonomy must be precise |
| Dynamic / 4D 3R | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R | F2, F3 | dynamic pointmaps, temporal motion, training-free dynamic correction, ray/state ideas | Dream should target object permanence and memory policy, not only motion estimation |
| Critic / test-time reasoning | Test3R, TTT3R, CTRL-style critic-revision | F3, F1 | geometric consistency, test-time update, critic-revision analogy | critic must trigger a concrete action, not only diagnose |
| Visual asset / Gaussian output | Splatt3R, InstantSplat, NoPoSplat, 4DGS variants | F6, F2, demo | pose-free Gaussian or NVS output, teacher-visible artifacts | demo surface is valuable but not alone a thesis |
| Guided / cross-modal | EAG3R, Event-3DGS, G-CUT3R, depth / pose / calibration priors | F5, F2, F3 | event/RGB fusion and guided reconstruction priors | hardware/data burden and already-emerging event 3R framing |
| Active perception | NBV, active perception, NextBestSense-style systems, ActiveNeRF, FisherRF, ActiveSplat, ActiveGS | F4, F3 | view selection, information gain, sensing policy, Fisher-information view-gain | keep simulation/design-first; avoid robot-stack takeover |
| Visual priors (semantic / tracking) | DINOv2, SAM 2, CoTracker, SpatialTracker | F2, F3 | foundation features, promptable segmentation, joint 2D/3D point tracking | use as prior signals for A6/A7, not as geometry substitutes |
| Monocular metric-depth priors | Depth Anything V2, Depth Pro, Metric3D v2 | F3, F5 | monocular metric depth / joint depth-normal as arbitrated prior | paired with critic for A7 check_prior_conflict |
| Event-camera VO / cross-modal add-on | DEVO, EAG3R, Event-3DGS | F5, F2 | event-only pose/motion, event-augmented pointmap, event Gaussian Splatting | sensor scope can inflate engineering; keep as robustness branch |

## Architecture And Visual Mechanism Intake Table

| Mechanism family | 3R translation | Failure modes | Candidate actions | Proxy metrics | Comparators / anchors | Evidence level now | Promotion condition |
|---|---|---|---|---|---|---|---|
| Sparse attention | retrieve only high-value views, frames, keypoints, anchors, or map cells | F1, F3, F6 | request_global_context; retrieve_sparse_keyframes; keep_sliding_window_context | anchor retention; loop consistency; compute-quality tradeoff; route regret | LoGeR, Mem3R, LongStream, OVGGT, Spann3R | inferred from source mechanisms | promote if retrieval policy beats fixed window or fixed cache in proxy |
| Linear attention | cheap long-context mixing for long video or many-view input | F1, F6 | update_state; compress_context; request_global_context | memory growth; runtime budget; drift-risk proxy | MLLA / MILA, Kimi Linear, RAM-Net, Mamba-2, STream3R | architecture-transfer inferred | promote only if geometry-specific gate or sparse retrieval is defined |
| SSM / Mamba-like state | input-conditioned state propagation and forgetting | F1 | weak_latent_update; strong_latent_update; route_scan; reset_state | update frequency; drift-risk proxy; locality preservation | Mamba, Mamba-2, VMamba, Vision Mamba, MambaOut, CUT3R, PAS3R | paper-proven mechanisms; 3R benefit unknown | promote if route/update policy is geometry-conditioned, not generic Mamba |
| Attention residual / hidden-state reuse | preserve valuable previous representations across layers, chunks, or revisits | F1, F3 | protect_anchor; reuse_hidden_state; request_global_context | anchor retention; early-frame recall; conflict reduction | EfficientViM, Kimi Linear, Infini-attention, OVGGT, LongStream | inferred / partially speculative | promote if residual state maps to geometry anchors or loop candidates |
| KDA-like finite-state memory | fine-grained state gating with selective full-attention escape | F1, F6 | update_state; retrieve_sparse_keyframes; evict_cache_token | action entropy; compute-quality tradeoff; route regret | Kimi Linear, linear-attention memory work, LoGeR / Mem3R as 3R comparators | speculative for 3R | promote after design memo compares against Mamba, causal attention, and fixed cache |
| RL / policy learning | learn action policy over verify, revise, reroute, or view acquisition | F3, F4, F6 | allocate_compute; revise_hypothesis; reroute_model; request_new_view | route regret; uncertainty reduction; view gain; revision success | CTRL, active perception, NBV systems | architecture-transfer inferred | promote only after non-RL proxy policy establishes reward signals |
| Active perception / planning | choose next view or sensing action to reduce 3R uncertainty | F4, F3, F5 | request_new_view; request_sensing_mode; revisit_region | uncertainty reduction; view gain; blind-spot reduction | NBV, NextBestSense-style systems | speculative for Dream 3R | promote through mock simulation before robotics or simulator work |
| Continual learning / test-time adaptation | update narrow adapter/state path under geometry evidence | F1, F3, F5 | open_adapter_update_budget; weak_update; strong_update | conflict reduction; forgetting risk; adaptation budget | TTT3R, SEAL, continual learner work | inferred; performance unknown | promote only if actual state/adapter update is defined and forgetting is measured |
| New visual backbones / foundation features | provide stronger image features, semantics, robustness, or correspondence priors | F3, F5, F6 | add_feature_prior; reroute_model; verify_geometry | matching conflict; low-texture robustness; route regret | MASt3R features, MambaVision, Vision Mamba, segmentation / foundation models | broad paper-proven, 3R role inferred | promote only when tied to a concrete geometric failure signal |
| Segmentation / tracking / optical flow / VOS | separate dynamic actors, preserve identity, and improve motion reasoning | F2, F3 | split_dynamic_static; preserve_object_identity; reject_dynamic_update | dynamic pollution; object identity consistency; static-map stability | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R | inferred from dynamic 3R and vision sources | promote if object permanence is measurable, not just mask quality |
| Gaussian / neural rendering / 4D representation | turn geometry into teacher-visible asset and represent dynamic scene state | F2, F6, demo | generate_visual_asset; initialize_4d_state; split_dynamic_static | demo clarity; asset consistency; dynamic identity consistency | Splatt3R, InstantSplat, NoPoSplat, 4DGS variants | paper/code-observed per source map | promote as evidence/demo layer unless it changes the 3R mechanism |
| Event / depth / IMU / LiDAR / guided priors | add sensor evidence when RGB-only geometry is fragile | F5, F2, F3 | add_sensor_prior; check_prior_conflict; route_to_guided_mode | blur robustness; prior conflict detection; geometry consistency | EAG3R, Event-3DGS, G-CUT3R, guided 3R | paper-proven mechanisms; Dream policy inferred | promote if policy decides when to trust or reject priors |
| VLM / semantic failure classification | classify scene regimes or failure causes using language/semantic priors | F3, F6 | classify_failure_mode; reroute_model; explain_report | failure-label accuracy; route regret; demo clarity | VLM reasoning work, composer evidence reports | speculative for 3R | promote only as support signal, not geometry substitute |

## Shared Action Taxonomy Draft

This draft has been compacted into A1-A8 in:

```text
planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md
```

Keep the detailed draft below as vocabulary support.

| Action | Meaning | Main failure modes | Minimum proxy metric | Branches using it |
|---|---|---|---|---|
| `weak_latent_update` | update state conservatively when evidence is redundant or uncertain | F1 | update frequency; drift-risk proxy | Memory, Continual |
| `strong_latent_update` | overwrite or strongly update state when geometry novelty is high and reliable | F1 | novelty-response score; anchor retention | Memory |
| `kalman_filter_update` | update state with uncertainty-aware gain | F1, F3 | predicted variance reduction; conflict reduction | Memory, Critic |
| `write_spatial_pointer` | add external map / pointer memory entry | F1, F6 | memory growth versus reuse; later retrieval usefulness | Memory, Composer |
| `merge_spatial_pointer` | merge duplicate or overlapping spatial memory entries | F1 | memory compression; overlap consistency | Memory |
| `protect_anchor` | preserve keyframe, gauge, or cache token critical for scale / frame | F1 | anchor retention; loop consistency | Memory |
| `evict_cache_token` | remove low-value cache/context token | F1, F6 | cache budget; quality drop | Memory, Composer |
| `request_global_context` | retrieve sparse/global views, memory, or high-value keyframes | F1, F3 | route regret; conflict reduction | Memory, Composer |
| `verify_geometry` | run critic or consistency check | F3 | conflict detection precision/recall | Critic, Composer |
| `revise_hypothesis` | locally retry, optimize, or choose alternate hypothesis | F3 | revision success; compute cost | Critic |
| `reroute_model` | choose another model or pipeline by failure mode/regime | F3, F6 | route regret; capability-card accuracy | Composer, Critic |
| `split_dynamic_static` | route static and dynamic evidence to different states | F2 | dynamic pollution; static-map stability | Dynamic, Memory |
| `preserve_object_identity` | maintain object state across time | F2 | identity consistency; object uncertainty | Dynamic |
| `reject_dynamic_update` | prevent dynamic region from updating static map | F2 | dynamic pollution reduction | Dynamic, Memory |
| `add_sensor_prior` | inject event/depth/pose/calibration/IMU/LiDAR prior | F5 | robustness under blur/low light; conflict detection | Cross-modal |
| `check_prior_conflict` | detect contradiction between RGB geometry and external prior | F5, F3 | prior conflict detection | Cross-modal, Critic |
| `open_adapter_update_budget` | allow constrained test-time adapter/state update | F1, F3, F5 | conflict reduction versus forgetting risk | Continual, Critic |
| `request_new_view` | ask for a new camera view/action | F4 | uncertainty reduction; view gain | Active |
| `request_sensing_mode` | choose event/depth/guided mode instead of RGB-only | F4, F5 | sensing-mode gain; hardware burden | Active, Cross-modal |
| `generate_visual_asset` | produce Gaussian/NVS/4D asset as evidence surface | F6, demo | demo clarity; artifact consistency | Composer, Dynamic |

## Proxy Metric Bank Draft

| Metric | Definition | Applies to | Minimum evidence without reproduction |
|---|---|---|---|
| conflict detection | whether a critic flags inconsistent pointmap/pose/confidence evidence | F3 | annotate public examples or KYKT metadata; no model run required |
| anchor retention | whether important keyframes / gauges / cache anchors are kept | F1 | simulate policy over frame/chunk metadata |
| memory growth | how fast external memory or cache grows under a policy | F1, F6 | count writes/evictions in proxy timeline |
| dynamic pollution | how often dynamic regions would update static memory | F2 | label dynamic/static regions at taxonomy level |
| object identity consistency | whether a dynamic object remains linked across time | F2 | manual/public-output annotation |
| route regret | whether composer chose a suboptimal model or action for a sample regime | F6, F3 | capability matrix comparison |
| action entropy | whether a policy uses diverse meaningful actions instead of one default | all | proxy action logs over synthetic/sample scenarios |
| uncertainty reduction | whether action reduces predicted unknown or inconsistent regions | F4, F3 | mock uncertainty map or design simulation |
| compute-quality tradeoff | whether extra context/compute is spent only on hard cases | F1, F3, F6 | cost model plus action trigger counts |
| demo clarity | whether the mechanism can be shown as a timeline/report/object split | all | storyboard review; not evidence of performance |

## Near-Term Use

Use this file to update:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md`
- `planning/BRANCH_COMPARISON_MATRIX.md`
- `sources/FRONTIER_SOURCE_MAP.md`
- `units/RESEARCH_UNIT_BANK.md`

Do not use this file to justify reproduction, checkpoint downloads, model training, or frontend implementation without user approval.
