# CYCLE-20260525-stage4-router-regime-aware-gate

cycle_id: CYCLE-20260525-stage4-router-regime-aware-gate
date: 2026-05-25
stage: 4 (Critic + Repair) — partial, code-side fix only
status: code-fix-locally-verified; server retrain + pipeline ablation rerun pending
predecessors: CYCLE-20260523-stage3, DEC-20260523-006

---

## Objective

Unblock Stage 4 closure. The pre-existing pipeline ablation showed:

- `full_pipeline_repair_on` = 0.2108669020
- `critic_on_repair_off` = 0.2253848203
- `both_off` = 0.2253848203
- `critic_changed_route_count` = 0
- `t4_3` = false

The two `critic_*_repair_off` numbers being identical proved the critic's confidence signal had **no effect on routing**. Stage 4 cannot close while the critic-on path is indistinguishable from the both-off path.

This cycle is the upstream code fix for that finding. It does not yet retrain on the server or rerun the pipeline ablation.

## Diagnosis

`ComposerRouter.confidence_gate` was a single global linear layer:

```python
self.confidence_gate = nn.Linear(1, d_routing)
```

It is the only place `critic_confidence` enters the router. Two separate problems were found in this layer:

1. **It is not trained.** `train_router_only.py` only fed `regime_probs` into the router; `critic_confidence` was never passed during training. The gate stayed at random init and produced negligible offsets at eval time. Stage 3 closure used this script and never exercised this signal.

2. **Even after training, this layer cannot represent the supervision Stage 4 wants.** When dense-regime samples (oracle = expert A) and sparse-regime samples (oracle = expert B) are in the same low-conf batch, they want the gate to push routing in **opposite directions** in routing-head space. With a single shared `(d_routing, 1)` weight matrix and a constant scalar conf input, the per-sample gradients on `confidence_gate.weight` cancel exactly. The gate cannot learn per-regime flips.

This was confirmed by an isolated reproduction: with regime + routing_head trained to convergence and the gate frozen-then-trained on `(conf_high → y, conf_low → alt_y)` pairs, `loss_l ≈ 71` but `||confidence_gate.weight.grad|| ≈ 8.5e-10` and `||confidence_gate.bias.grad|| = 0.0`. The gradient is structurally cancelled, not numerically small.

Several attempted training tricks (heavier `loss_l` weight, `weight_decay=0` on the gate, two-stage training with frozen regime/head, an input-shift trick to centre the conf band, switching to SGD) all failed for the same root cause: the architecture cannot express the target function.

User-approved fix: upgrade the gate to be **regime-aware**.

## Implementation

### Code changes

`code/dream3r/modules.py`, `ComposerRouter`:

```python
# old
self.confidence_gate = nn.Linear(1, d_routing)

# new
self.confidence_gate = nn.Sequential(
    nn.Linear(1 + n_regimes, d_routing),
    nn.GELU(),
    nn.Linear(d_routing, d_routing),
)
```

`forward` now feeds the concatenation:

```python
if critic_confidence is not None:
    gate_dtype = self.confidence_gate[0].weight.dtype
    conf_in = critic_confidence.to(gate_dtype)
    regime_in = regime_probs.to(gate_dtype)
    gate_input = torch.cat([conf_in, regime_in], dim=-1)
    conf_mod = self.confidence_gate(gate_input)
    regime_embed = regime_embed + conf_mod.to(regime_embed.dtype)
```

`load_state_dict` was extended with a backward-compatibility branch: if a checkpoint contains `confidence_gate.weight` of shape `(d_routing, 1)`, the legacy keys are dropped and the new MLP keeps its random init. Legacy production checkpoints had this layer untrained anyway, so the migration is semantically equivalent.

`code/dream3r/scripts/train_router_only.py`:

- Removed the conf-shift / two-stage / `_absorb_conf_shift` logic and debug prints.
- Restored a single-stage joint training step combining `loss_n / loss_h / loss_l` with equal weights. Per-regime gradients no longer cancel because the gate input now contains regime information, so the simpler loop converges.

`code/dream3r/tests/test_router_only_training.py`:

- Augmented training test now runs at `epochs=500, lr=0.05` (down from the failing `2000, 0.1` we tried under the old gate).
- Asserts `summary["high_conf_accuracy_vs_best"] >= 0.75`, `summary["low_conf_flip_rate_vs_no_conf"] > 0.0`, plus a reload + per-sequence flip check.

### Files changed

- `code/dream3r/modules.py` — `ComposerRouter.__init__`, `forward`, new `load_state_dict`
- `code/dream3r/scripts/train_router_only.py` — joint training, augmented losses
- `code/dream3r/tests/test_router_only_training.py` — augmented training test

No other modules touched. `model.py` main forward, `bus.py`, `anchor_bank.py`, `nsa_attention.py` untouched.

## Verification

### Local — done

```text
python -m pytest tests/ --ignore=tests/test_eval.py -q
==> 227 passed, 2 skipped, 70 warnings
```

Notable focused subset:

- `tests/test_router_only_training.py` — 3 passed (preset, accuracy, regime-aware low-conf flip)
- `tests/test_router_ablation_eval.py` — passed
- `tests/test_repair_pipeline_ablation_eval.py` — passed
- `tests/test_repair_ablation_eval.py` — passed
- `tests/test_spatial_memory.py` — 12 passed (includes `test_composer_router_*`)
- `tests/test_v04_test3r_offpath.py` — 7 passed
- `tests/test_sequence_training.py`, `test_training_convergence.py`, `test_state_recurrence_factory.py` — passed

Direct probe of the trained gate on the new test data:

```
pred no-conf:    [0, 0, 1, 1]
pred conf-high:  [0, 0, 1, 1]   # matches oracle y
pred conf-low:   [1, 1, 0, 0]   # flips per-regime to alt_y
```

This is the per-regime flip behaviour the old global gate could not produce.

### Server — pending

Not run yet in this cycle. Required to actually close Stage 4:

1. `scp` the three modified files to `/hdd3/kykt26/code/dream3r/dream3r/`.
2. Retrain `router_only_v1` on the server using the new training loop.
3. Rerun `scripts/eval_repair_pipeline_ablation.py` against the retrained checkpoint.
4. Confirm `critic_changed_route_count > 0` and `t4_3 = true`.
5. Then write the Stage 4 closure DEC.

## Limitations and Honest Notes

- The local proof uses 4 synthetic sequences and a 6-regime softmax. It demonstrates that the new gate **can** learn per-regime flips. It does not demonstrate that the existing critic on KITTI will produce conf bands that actually trigger the gate at eval time. That part is what the server pipeline ablation rerun will verify.
- `confidence_gate` is now a `nn.Sequential`, so any code that introspected `confidence_gate.weight` directly (only `_debug_router.py`, which has been deleted) would break. The new path is `confidence_gate[0].weight` and `confidence_gate[2].weight`.
- The `load_state_dict` migration silently drops legacy gate keys. This is correct for production checkpoints (gate was untrained), but if any future pipeline tries to load a *trained* legacy gate it will silently lose those weights. We accept this because no such checkpoint exists.
- Stage 4 closure success criteria (T4.3) require **real KITTI hard-sequence evidence**, not the synthetic supervision used for unit tests. The handoff prompt covers what server work remains.

## Files Changed

- `code/dream3r/modules.py`
- `code/dream3r/scripts/train_router_only.py`
- `code/dream3r/tests/test_router_only_training.py`

Deleted (temporary diagnostic, never committed):

- `code/dream3r/_debug_router.py`

## Conclusion

The architectural blocker for Stage 4 (`critic_changed_route_count = 0`) has a verified upstream fix locally. Stage 4 itself is not yet closed; closure requires the server retrain + pipeline ablation rerun listed above. The handoff prompt for the next agent picks up from that point.
