# DEC-20260525-001 — Stage 4 Critic Closure

## Decision

Close Stage 4 as complete.

## Rationale

Stage 4 required the Critic and RepairExecutor to produce a real signal on KITTI, not just a logged or synthetic path.

The final server ablation meets the core closure gate provided for this handoff:

- `critic_changed_route_count`: 1
- `success.t4_3`: true
- `full_pipeline_repair_on`: 0.2108669020
- `critic_on_repair_off`: 0.2253848203
- `both_off`: 0.2253848203
- `best_example_relative_improvement`: 0.2488888968

The improvement is from actual `reroute_model` repair on `2011_09_26_drive_0051_sync_02`, where the full pipeline switches from Fast3R to MASt3R and reduces scale-aligned abs-rel from 0.2333236784 to 0.1752520055.

## Important Limitation

This closure does not claim a strict critic-only aggregate gain. On the hard-row aggregate, `critic_on_repair_off == both_off`. The evidence is:

- the critic signal changes at least one route (`critic_changed_route_count = 1`)
- repair changes output on real sequences (`repair_changed_output_count = 2`)
- full repair improves over both-off by 6.44139131% mean relative improvement
- at least one example improves by more than 5%

Those are sufficient for the stated Stage 4 gate in this handoff, but they are not sufficient for a SOTA or broad critic-only routing claim.

## Implementation Boundary

Changed:

- `modules.py`: `ComposerRouter` confidence gate now conditions on critic confidence, regime probabilities, and previous routed expert id; old confidence-gate checkpoint shapes are handled compatibly.
- `model.py`: main forward passes previous `routed_expert_id` into `ComposerRouter`. This was done only after explicit user authorization.
- `train_router_only.py`: retraining now includes zero-confidence and Stage 4 context-data supervision.
- `eval_repair_pipeline_ablation.py`: pipeline ablation passes previous expert id and evaluates the non-strict closure chain.
- `test_router_only_training.py`: tests cover previous-expert and zero-confidence behavior.

Not changed:

- `anchor_bank.py`
- `nsa_attention.py`
- `bus.py`

## Verification

Server focused tests:

```text
32 passed, 15 warnings
```

Router checkpoint:

```text
/hdd3/kykt26/checkpoints/router_only_v1/latest.pt
final_accuracy: 1.0
augmented_with_critic_confidence: true
context_n_examples: 12
zero_conf_context_accuracy_min: 0.9166666865
```

Pipeline ablation:

```text
/hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json
t4_3: true
critic_changed_route_count: 1
repair_changed_output_count: 2
```

## Follow-Up

Stage 5 should prioritize adding a third real expert before making broader routing-quality claims. The current two-expert Stage 4 result is a real closure artifact, but the next credibility jump is a >=3-expert Composer ablation on KITTI.
