# CYCLE 20260523 Stage 3 — Composer Router Real Routing

## Scope

Close Stage 3 by adding a second real expert, generating KITTI regime labels, training a supervised ComposerRouter, and running a multi-expert ablation.

## Changes

- Upgraded `Fast3RAdapter` to load the real Fast3R checkpoint already present on the server.
- Added `test_fast3r_real.py` and verified real Fast3R dispatch on GPU.
- Added `generate_regime_labels.py` for KITTI regime probabilities from sequence length, depth temporal change, and OXTS motion.
- Added empty-sequence filtering in regime label generation.
- Added `build_oracle_expert_labels.py` to compute real MASt3R/Fast3R oracle labels from KITTI pointmap abs-rel.
- Added `train_router_only.py` and `router_only` preset for supervised two-expert router training.
- Added `eval_router_ablation.py` for learned-router vs single-expert vs random routing evaluation.

## Verification

- T3.1 Fast3R real smoke:
  - `test_fast3r_real.py`: 1 passed on server GPU
  - `test_fast3r_integration.py`: 2 passed on server GPU
- T3.2 regime labels:
  - 246 valid KITTI sequences labeled
  - 1 empty sequence skipped
  - top distribution: outdoor_static 178, dense_sequential 59, sparse_view 6, dynamic_scene 3
- T3.3 router-only training:
  - scale-aligned oracle labels: MASt3R 6, Fast3R 2
  - router accuracy: 0.75 -> 1.00
  - checkpoint: `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`
- T3.4 ablation:
  - learned_router abs-rel: 0.1712338803
  - always_mast3r abs-rel: 0.2048148634
  - always_fast3r abs-rel: 0.2222443298
  - random_routing abs-rel: 0.2202285165
  - route/regime Cramer's V: 1.0
- Full test suites:
  - local: `219 passed, 2 skipped`
  - server: `217 passed, 2 skipped`

## Limitations

The ablation uses 8 sequence-level oracle samples and scale-aligned abs-rel. The first raw abs-rel oracle run selected MASt3R for every sampled sequence, which showed that raw scale conventions would block a meaningful router signal. The closure therefore evaluates routing quality after explicit per-window depth scale alignment.
