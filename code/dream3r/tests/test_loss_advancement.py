"""Tests for advanced Dream3R loss terms."""

import torch

from dream3r.losses import Dream3RLoss


def _loss_fn():
    return Dream3RLoss(weights={
        "pointmap": 1.0,
        "critic_p1": 0.0,
        "critic_p5": 0.0,
        "memory_p2": 0.0,
        "memory_p3": 0.0,
        "permanence_p4": 0.0,
        "action_entropy": 0.0,
        "retrieval": 0.1,
        "retrieval_quality": 0.1,
        "routing": 0.1,
        "geometric_consistency": 0.1,
        "drift_consistency": 0.0,
        "state_drift_regularization": 0.1,
    })


def test_advanced_loss_terms_are_finite():
    outputs = {
        "pointmap": torch.tensor([[[0.1, 0.0, 1.0],
                                   [1.0, 0.0, 2.0]]], requires_grad=True),
        "prev_pointmap": torch.tensor([[[0.0, 0.0, 1.0],
                                        [0.9, 0.0, 2.0]]]),
        "nsa_branch_weights": torch.tensor([[[0.5, 0.5, 0.0],
                                             [0.4, 0.6, 0.0]]]),
        "routing_logits": torch.tensor([[0.0, 1.0, -1.0]]),
        "memory_retrieval_log": {
            "selected_scores_after_bias": torch.tensor([[[2.0, 1.0]]]),
            "selected_3d_distances": torch.tensor([[[0.1, 0.2]]]),
        },
        "latent_drift_proxy": torch.tensor([[0.2]]),
    }
    targets = {
        "pointmap": torch.tensor([[[0.1, 0.0, 1.0],
                                   [1.0, 0.0, 2.0]]]),
        "prev_pointmap": torch.tensor([[[0.0, 0.0, 1.0],
                                        [0.9, 0.0, 2.0]]]),
    }

    losses = _loss_fn()(outputs, targets)

    for key in [
        "total", "geometric_consistency", "retrieval_quality",
        "routing", "retrieval", "state_drift_regularization",
    ]:
        assert key in losses
        assert torch.isfinite(losses[key])


def test_routing_loss_penalizes_single_expert_collapse():
    loss_fn = _loss_fn()
    common = {
        "pointmap": torch.zeros(1, 1, 3),
        "nsa_branch_weights": torch.full((1, 1, 3), 1.0 / 3.0),
    }
    targets = {"pointmap": torch.zeros(1, 1, 3)}

    collapsed = {**common, "routing_logits": torch.tensor([[10.0, -10.0, -10.0]])}
    balanced = {**common, "routing_logits": torch.zeros(1, 3)}

    assert loss_fn(collapsed, targets)["routing"] > loss_fn(balanced, targets)["routing"]


def test_retrieval_quality_rewards_near_high_score_anchors():
    loss_fn = _loss_fn()
    common = {
        "pointmap": torch.zeros(1, 1, 3),
        "nsa_branch_weights": torch.full((1, 1, 3), 1.0 / 3.0),
        "routing_logits": torch.zeros(1, 3),
    }
    targets = {"pointmap": torch.zeros(1, 1, 3)}
    good = {
        **common,
        "memory_retrieval_log": {
            "selected_scores_after_bias": torch.tensor([[[4.0, 3.0]]]),
            "selected_3d_distances": torch.tensor([[[0.05, 0.10]]]),
        },
    }
    bad = {
        **common,
        "memory_retrieval_log": {
            "selected_scores_after_bias": torch.tensor([[[-3.0, -4.0]]]),
            "selected_3d_distances": torch.tensor([[[1.5, 2.0]]]),
        },
    }

    assert loss_fn(good, targets)["retrieval_quality"] < loss_fn(bad, targets)["retrieval_quality"]


if __name__ == "__main__":
    test_advanced_loss_terms_are_finite()
    test_routing_loss_penalizes_single_expert_collapse()
    test_retrieval_quality_rewards_near_high_score_anchors()
    print("All advanced loss tests passed.")
