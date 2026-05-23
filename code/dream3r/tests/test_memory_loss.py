"""Tests for Stage 2 memory-specific losses."""

import torch

from dream3r.losses import Dream3RLoss


def _loss_fn():
    return Dream3RLoss(weights={
        "pointmap": 0.0,
        "critic_p1": 0.0,
        "critic_p5": 0.0,
        "memory_p2": 0.0,
        "memory_p3": 0.0,
        "permanence_p4": 0.0,
        "action_entropy": 0.0,
        "retrieval": 0.0,
        "retrieval_quality": 0.0,
        "routing": 0.0,
        "geometric_consistency": 0.0,
        "cross_window_pointmap": 1.0,
        "drift_consistency": 0.0,
        "state_drift_regularization": 0.0,
        "memory_consistency": 1.0,
        "anchor_reuse": 1.0,
    })


def test_cross_window_pointmap_loss_penalizes_wrong_delta():
    loss_fn = _loss_fn()
    prev = torch.zeros(1, 2, 3)
    gt = torch.tensor([[[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]]])
    mask = torch.ones(1, 2)
    targets = {
        "pointmap": gt,
        "prev_pointmap": prev,
        "pointmap_mask": mask,
        "prev_pointmap_mask": mask,
    }

    good = {"pointmap": gt.clone(), "prev_pointmap": prev.clone()}
    bad = {"pointmap": torch.zeros_like(gt), "prev_pointmap": prev.clone()}

    assert loss_fn(good, targets)["cross_window_pointmap"] == 0
    assert loss_fn(bad, targets)["cross_window_pointmap"] > 0


def test_memory_consistency_relaxes_when_scene_changes():
    loss_fn = _loss_fn()
    current = torch.ones(2, 3, 4)
    previous = torch.zeros(2, 3, 4)
    outputs = {
        "latent_state_tokens": current,
        "prev_latent_state_tokens": previous,
    }

    low_change = loss_fn(outputs, {"pointmap_change": torch.tensor([0.0, 0.0])})
    high_change = loss_fn(outputs, {"pointmap_change": torch.tensor([1.0, 1.0])})

    assert low_change["memory_consistency"] > high_change["memory_consistency"]
    assert high_change["memory_consistency"] == 0


def test_anchor_reuse_prefers_reused_indices_and_selected_branch():
    loss_fn = _loss_fn()
    previous_idx = torch.tensor([[[0, 1], [2, 3]]])
    good = {
        "nsa_branch_weights": torch.tensor([[[0.1, 0.8, 0.1], [0.1, 0.8, 0.1]]]),
        "nsa_selected_indices": previous_idx.clone(),
        "prev_nsa_selected_indices": previous_idx,
    }
    bad = {
        "nsa_branch_weights": torch.tensor([[[0.8, 0.1, 0.1], [0.8, 0.1, 0.1]]]),
        "nsa_selected_indices": torch.tensor([[[4, 5], [6, 7]]]),
        "prev_nsa_selected_indices": previous_idx,
    }

    targets = {}
    good_loss = loss_fn(good, targets)["anchor_reuse"]
    bad_loss = loss_fn(bad, targets)["anchor_reuse"]

    assert good_loss < bad_loss
    assert torch.isfinite(good_loss)
    assert torch.isfinite(bad_loss)
