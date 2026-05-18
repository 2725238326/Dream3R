"""Tests for W15 geometric Critic signals."""

import torch

from dream3r.losses import Dream3RLoss
from dream3r.model import Dream3R, build_dream3r
from dream3r.modules import Critic


def _critic():
    critic = Critic(
        n_evidence=2, d_evidence=4, d_critic=16, n_heads=2, n_layers=1,
        geometric_conflict_scale=24.0, geometric_clean_bias=-2.0,
    )
    for p in critic.parameters():
        p.data.zero_()
    return critic


def test_sampson_distance_zero_for_perfect_consistency():
    pointmap = torch.tensor([[[0.0, 0.0, 1.0],
                              [1.0, 0.0, 2.0],
                              [0.0, 1.0, 3.0]]])
    pair = torch.stack([pointmap, pointmap], dim=1)
    loss = Dream3RLoss.sampson_distance_loss(pair, torch.ones(1, 2, 3, 1))

    assert torch.allclose(loss, torch.tensor(0.0), atol=1e-7)


def test_critic_conflict_rises_for_shifted_pointmap_pair():
    critic = _critic()
    base = torch.tensor([[[0.0, 0.0, 1.0],
                          [1.0, 0.0, 1.0],
                          [0.0, 1.0, 1.0]]])
    consistent = torch.stack([base, base], dim=1)
    shifted = torch.stack([base, base + torch.tensor([0.75, 0.0, 0.0])], dim=1)
    evidence = torch.zeros(1, 2, 4)
    confidence = torch.ones(1, 2, 3, 1)

    out_ok = critic(evidence, pointmap_pair=consistent, confidence_pair=confidence)
    out_bad = critic(evidence, pointmap_pair=shifted, confidence_pair=confidence)

    assert out_ok["conflict_score"].item() < -1.5
    assert out_bad["conflict_score"].item() > out_ok["conflict_score"].item() + 2.0
    assert out_bad["geometric_consistency_log"]["sampson_distance"].item() > 0.1


def test_covisibility_loss_detects_confidence_disagreement():
    pointmap = torch.zeros(1, 2, 4, 3)
    good_conf = torch.ones(1, 2, 4, 1)
    bad_conf = good_conf.clone()
    bad_conf[:, 1, :, :] = 0.0

    good = Dream3RLoss.covisibility_consistency_loss(pointmap, good_conf)
    bad = Dream3RLoss.covisibility_consistency_loss(pointmap, bad_conf)

    assert good.item() == 0.0
    assert bad.item() > good.item()


def test_model_exposes_geometric_critic_log():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    with torch.no_grad():
        out = model(torch.randn(1, 4, 16, 768), timestep=0)

    log = out["critic_geometric_log"]
    assert "sampson_distance" in log
    assert "covisible_inconsistency" in log
    assert torch.isfinite(log["sampson_distance"]).all()


def test_geometric_critic_config_threads_to_model():
    model = Dream3R({
        "version": "v03",
        "use_backbone": False,
        "critic_geometric_conflict_scale": 3.5,
        "critic_geometric_clean_bias": -1.25,
    })

    assert model.critic.geometric_conflict_scale == 3.5
    assert model.critic.geometric_clean_bias == -1.25


if __name__ == "__main__":
    test_sampson_distance_zero_for_perfect_consistency()
    test_critic_conflict_rises_for_shifted_pointmap_pair()
    test_covisibility_loss_detects_confidence_disagreement()
    test_model_exposes_geometric_critic_log()
    test_geometric_critic_config_threads_to_model()
    print("All geometric Critic tests passed.")
