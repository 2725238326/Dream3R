# Dream3R Recent Progress Ledger

Status: current canonical summary for Cycle 033/034 and W19-W22.

Date: 2026-05-11

## What Changed

Dream3R has moved from a broad architecture sketch into a runnable, test-covered control-graph prototype with first real-data smoke evidence.

The current system includes:

- Perceiver/evidence path with DINOv2-compatible frozen-backbone support and fallback.
- SpatialMemory with NSA compressed / selected / sliding branches.
- Active state tokens and stable AnchorBank promote/recall.
- 3D-aware stable memory payloads and retrieval.
- Permanence slots with per-slot suppress and ISA-style reference poses.
- Geometric Critic with Sampson/depth/covisibility signals and repair actions.
- ComposerRouter and external 3R expert adapter contracts.
- Mamba hybrid state recurrence using server `mamba_ssm` when available.
- Renderer-free GaussianHead tensor contract for future 3DGS output.
- Synthetic ablation runner and visualization/export pack.
- KITTI real RGB/depth loader and real-sequence evaluation entry.

## Evidence Tiers

### Tier 1: Integration Verified

These are supported by server smoke and full unit tests:

- v0.3 forward/backward pass.
- multi-window streaming state update.
- NSA branch mixing.
- active-to-stable memory promote/recall.
- 3D-aware AnchorBank retrieval.
- Critic repair action handoff.
- permanence slot pose tracking.
- Mamba recurrence factory and demo path.
- Gaussian tensor contract.
- synthetic ablation and visualization artifact export.
- KITTI loader and real-sequence eval orchestration.

### Tier 2: Real Data Smoke Verified

KITTI rectified RGB/depth windows now run through Dream3R:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.evaluate_real_sequence \
  --data-root /hdd3/kykt26/data \
  --max-sequences 1 \
  --max-windows 2 \
  --recurrence mamba_hybrid \
  --output demo_artifacts/real_sequence/kitti_metrics.json
```

Latest server result:

- dataset: `kitti_rectified`
- sequence: `2011_09_26_drive_0001_sync_02`
- windows: 2
- device: `cuda`
- recurrence backend: `mamba_ssm`
- output JSON: `/hdd3/kykt26/code/dream3r/demo_artifacts/real_sequence/kitti_metrics.json`

Observed signals:

- pointmap L2: `20.4747`
- depth RMSE: `21.8658`
- memory occupancy: `60.0`
- NSA branch mean: compressed `0.3927`, selected `0.6073`, sliding `0.0`
- stable promotion rate: `1.0`
- selected anchor 3D distance: `0.0653`
- state drift magnitude: `0.7299`
- repair action: `2` on both windows

Interpretation: this is real-data integration evidence, not trained reconstruction quality.

### Tier 3: Research Claims Still Pending

These must not be claimed as solved yet:

- SOTA reconstruction accuracy.
- real-data ablation gains.
- calibrated real-data Critic thresholds.
- expert routing quality improvement.
- long-sequence degradation curves.
- renderer-backed 3DGS output.
- test-time adaptation gains.

## Demo Entry Points

### Synthetic Architecture Demo

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.demo_mamba_path
```

Shows:

- `cross_attention` and `mamba_hybrid` switchability.
- server `mamba_ssm` backend.
- active state change across windows.
- stable memory promotion.
- NSA branch mixing.
- Critic repair action output.

### Synthetic Ablation Demo

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.ablate_recurrence --windows 3 --seeds 33 34 35
```

Variants:

- `baseline_cross_attention`
- `mamba_hybrid`
- `no_nsa`
- `no_stable_memory`

### Demo Artifact Export

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.export_demo_artifacts \
  --output-dir demo_artifacts/showcase
```

Produces manifest JSON, demo JSON, ablation JSON, SVG charts, and copied key docs.

## Verification Snapshot

Latest verified on server:

- `sync_verify_server.ps1 -Mode verify`: local/server package files match.
- `dream3r.tests.test_kitti_loader_contract`: pass.
- `dream3r.tests.test_real_sequence_eval_contract`: pass.
- `dream3r.smoke_test`: pass.
- `sync_verify_server.ps1 -Mode test -FullTests`: pass.
- `dream3r.evaluate_real_sequence`: two real KITTI windows pass.

All torch/model/test commands are run only on the server conda environment:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m <module>
```

Local Windows is used for editing and markdown only.

## Current Architecture Position

Dream3R should be described as:

> a control-graph streaming 3R prototype that integrates active/stable spatial memory, NSA retrieval, geometric self-critique, expert routing, object permanence, and switchable Mamba/cross-attention recurrence.

It should not yet be described as:

> a trained SOTA real-data 3R model.

## Stage 4 Closed (2026-05-25)

Stage 4 is closed under the stated core gate:
`critic_changed_route_count > 0` and `t4_3 == true`.

Final server artifacts:

- Critic checkpoint: `/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt`
- Router checkpoint: `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`
- Pipeline ablation: `/hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json`
- Closure cycle: `cycles/CYCLE-20260525-stage4-closure.md`
- Decision: `decisions/DEC-20260525-001-stage4-critic-closure.md`

Final server evidence:

- Critic: `conflict_abs_rel_corr = 0.8337993524`,
  `repair_action_accuracy = 0.9166666865`, `t4_1 = true`
- Router: `final_accuracy = 1.0`,
  `augmented_with_critic_confidence = true`, `context_n_examples = 12`,
  `zero_conf_context_accuracy_min = 0.9166666865`
- Pipeline: `critic_changed_route_count = 1`,
  `repair_changed_output_count = 2`, `t4_3 = true`
- Metrics: `full_pipeline_repair_on = 0.2108669020`,
  `critic_on_repair_off = 0.2253848203`, `both_off = 0.2253848203`,
  `best_example_relative_improvement = 0.2488888968`

Important limitation: `critic_on_repair_off` equals `both_off` at the hard-row
aggregate level. This is a real Stage 4 closure artifact and a real repair
gain, not a strict critic-only aggregate gain and not a SOTA claim.

Implementation changes that matter:

- `ComposerRouter.confidence_gate` now conditions on critic confidence, regime
  probabilities, and previous routed expert id.
- `model.py` main forward passes previous `routed_expert_id` into the router.
  This was done only after explicit user authorization.
- Router-only training now includes zero-confidence and Stage 4 context-data
  supervision.
- Pipeline ablation now passes previous expert context and evaluates the
  closure chain used by the handoff.
- `anchor_bank.py`, `nsa_attention.py`, and `bus.py` were not changed.

Verification:

- Server focused suite: `32 passed, 15 warnings`
- Local focused/schema suite: `16 passed, 1 warning`

## Stage 5 S1 Closed (2026-05-25)

Stage 5 S1 closes the first >=3 real-expert Composer ablation on KITTI.

Final server artifacts:

- Oracle labels: `/hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json`
- Router checkpoint: `/hdd3/kykt26/checkpoints/router_stage5_s1_v1/latest.pt`
- Router ablation: `/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results.json`
- Closure cycle: `cycles/CYCLE-20260525-stage5-s1-three-expert.md`
- Decision: `decisions/DEC-20260525-002-stage5-s1-three-expert-closure.md`

Final server evidence:

- Spann3R real integration: `2 passed, 8 warnings`
- Three-expert oracle: `expert_order = [fast3r, mast3r, spann3r]`
- Oracle counts: `mast3r = 8`, `fast3r = 2`, `spann3r = 2`
- Router ablation: `learned_router = 0.1722621613`, `always_mast3r = 0.1906146836`, `oracle_router = 0.1636828103`
- Best-single improvement: `relative_improvement_vs_best_single = 0.0962807369`
- Success: `candidate_count_ge_3 = true`, `oracle_uses_ge_3_experts = true`, `stage5_s1 = true`

Important limitation: the final learned router does not select Spann3R
(`learned_expert_counts = {fast3r: 3, mast3r: 9, spann3r: 0}`), even though
Spann3R wins oracle on two real windows. This is closure for a three-candidate
ablation, not proof that the current 6D regime-probability router exploits all
third-expert opportunities.

## Immediate Next Work

1. Richer-router-feature pass: add regime-label `stats` or evidence-derived features to separate cases with identical regime probabilities but different oracle experts.
2. Real-data ablation table using the same variant names as synthetic ablation.
3. Critic calibration on real geometry distributions.
4. Expert routing quality report with real/fallback adapter availability.
5. Paper/demo pack cleanup: keep claims tied to tests, metrics, or JSON artifacts.
