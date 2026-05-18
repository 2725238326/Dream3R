"""Tests for 3R evaluation metrics."""

import torch

from dream3r.evaluate import Evaluator, compute_3d_metrics, compute_depth_metrics


def test_depth_metrics_perfect_prediction():
    depth = torch.tensor([[1.0, 2.0, 4.0]])
    metrics = compute_depth_metrics(depth, depth)

    assert metrics["absrel"] == 0.0
    assert metrics["sqrel"] == 0.0
    assert metrics["rmse"] == 0.0
    assert metrics["rmse_log"] == 0.0
    assert metrics["delta1"] == 1.0
    assert metrics["delta2"] == 1.0
    assert metrics["delta3"] == 1.0


def test_3d_metrics_perfect_prediction():
    points = torch.tensor([[[0.0, 0.0, 1.0],
                            [1.0, 0.0, 2.0]]])
    chamfer, f005, f010 = compute_3d_metrics(points, points)

    assert chamfer == 0.0
    assert f005 == 1.0
    assert f010 == 1.0


def test_evaluator_accumulates_geometry_and_architecture_metrics():
    pointmap = torch.tensor([[[0.0, 0.0, 1.0],
                              [0.1, 0.0, 2.0]]])
    branch_weights = torch.tensor([[[0.5, 0.5, 0.0],
                                    [0.5, 0.5, 0.0]]])
    outputs = {
        "pointmap": pointmap,
        "nsa_branch_weights": branch_weights,
        "memory_retrieval_log": {
            "selected_3d_distances": torch.tensor([[[0.2, 0.3]]]),
            "geometry_bias_applied": torch.tensor(1.0),
        },
        "critic_geometric_log": {
            "sampson_distance": torch.tensor([0.2]),
            "covisible_inconsistency": torch.tensor([0.1]),
            "depth_inconsistency": torch.tensor([0.3]),
        },
        "latent_drift_proxy": torch.tensor([[0.4]]),
        "bank_occupancy": torch.tensor([0.25]),
        "routing_logits": torch.tensor([[2.0, 0.0, -1.0]]),
    }
    targets = {"pointmap": pointmap}

    evaluator = Evaluator()
    evaluator.update(outputs, targets)
    metrics = evaluator.compute()

    assert metrics.pointmap_mse == 0.0
    assert metrics.pointmap_l2 == 0.0
    assert metrics.depth_delta1 == 1.0
    assert metrics.chamfer_l2 == 0.0
    assert metrics.memory_branch_selected == 0.5
    assert metrics.memory_branch_entropy > 0.0
    assert metrics.selected_anchor_3d_distance == 0.25
    assert metrics.geometry_bias_applied == 1.0
    assert abs(metrics.critic_sampson_distance - 0.2) < 1e-6
    assert abs(metrics.critic_covisible_inconsistency - 0.1) < 1e-6
    assert abs(metrics.critic_depth_inconsistency - 0.3) < 1e-6
    assert abs(metrics.state_drift_magnitude - 0.4) < 1e-6


if __name__ == "__main__":
    test_depth_metrics_perfect_prediction()
    test_3d_metrics_perfect_prediction()
    test_evaluator_accumulates_geometry_and_architecture_metrics()
    print("All evaluation metric tests passed.")
