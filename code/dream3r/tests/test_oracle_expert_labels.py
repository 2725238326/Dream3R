"""Schema tests for Stage 3 oracle expert label helpers."""

from dream3r.scripts.build_oracle_expert_labels import (
    _pointmap_abs_rel,
    _select_sequences,
)

import torch


def test_pointmap_abs_rel_uses_valid_depth_mask():
    pred = torch.tensor([[[[0.0, 0.0, 2.0], [0.0, 0.0, 6.0]]]])
    target = torch.tensor([[[[0.0, 0.0, 1.0], [0.0, 0.0, 3.0]]]])
    mask = torch.tensor([[[True, False]]])

    assert _pointmap_abs_rel(pred, target, mask) == 1.0


def test_pointmap_abs_rel_can_align_median_depth_scale():
    pred = torch.tensor([[[[0.0, 0.0, 2.0], [0.0, 0.0, 4.0]]]])
    target = torch.tensor([[[[0.0, 0.0, 4.0], [0.0, 0.0, 8.0]]]])
    mask = torch.tensor([[[True, True]]])

    assert _pointmap_abs_rel(pred, target, mask, align_scale=True) == 0.0


def test_select_sequences_balances_top_regimes():
    regime_data = {
        "regime_order": [
            "indoor_static",
            "outdoor_static",
            "dynamic_scene",
            "sparse_view",
            "dense_sequential",
            "feed_forward_manyview",
        ],
        "labels": {
            "dense_a": [0, 0, 0, 0, 0.9, 0.1],
            "dense_b": [0, 0, 0, 0, 0.8, 0.2],
            "sparse_a": [0, 0, 0, 0.7, 0.2, 0.1],
        },
    }

    assert _select_sequences(regime_data, max_per_regime=1) == ["sparse_a", "dense_a"]
