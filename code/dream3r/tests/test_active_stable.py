"""Tests for W13 active/stable memory separation."""

import torch

from dream3r.anchor_bank import AnchorBank
from dream3r.config import DEFAULTS, config_to_model_args
from dream3r.modules import SpatialMemory


def test_stability_score_increments_for_persistent_entries():
    bank = AnchorBank(capacity=8, d_key=16, d_value=16)
    bank.reset(batch_size=1)
    bank.write(
        torch.randn(1, 2, 16),
        torch.randn(1, 2, 16),
        confidence=torch.ones(1, 2),
    )

    for _ in range(4):
        bank.tick()

    assert torch.all(bank.stability_score[0, :2] >= 4)
    assert bank.state_snapshot()["stability_score"].shape == (1, 8)


def test_stable_entries_survive_pruning():
    bank = AnchorBank(capacity=4, d_key=8, d_value=8, stability_prune_bonus=10.0)
    bank.reset(batch_size=1)
    stable_keys = torch.full((1, 2, 8), 0.25)
    stable_values = torch.full((1, 2, 8), 0.5)
    bank.write(stable_keys, stable_values, confidence=torch.ones(1, 2) * 0.1)
    for _ in range(5):
        bank.tick()

    bank.write(torch.randn(1, 2, 8), torch.randn(1, 2, 8), confidence=torch.ones(1, 2))
    pruned = bank.prune(keep_ratio=0.5)

    assert pruned.n_pruned == 2
    assert bank.valid[0, :2].all(), "older stable entries should survive prune"


def test_spatial_memory_promote_and_recall_from_stable():
    mem = SpatialMemory(
        d_model=32,
        n_state_tokens=4,
        bank_capacity=32,
        nsa_n_select_k=2,
        nsa_n_heads=2,
        sliding_window=2,
        active_to_stable_threshold=0.0,
        stable_recall_threshold=-1.0,
        stable_recall_strength=0.25,
    )
    state = mem.init_state(1, torch.device("cpu"))
    frame_tokens = torch.randn(1, 8, 768)
    evidence = torch.randn(1, 17 * 32)
    pointmap = torch.randn(1, 8, 3)

    out1 = mem(frame_tokens, evidence, state, t2_pointmap=pointmap)
    out2 = mem(frame_tokens, evidence, out1["latent_state_tokens"].detach(), t2_pointmap=pointmap)
    log = out2["memory_retrieval_log"]

    assert "active_state_confidence" in log
    assert "promoted_to_stable" in log
    assert log["promoted_to_stable"].any()
    assert log["stable_recall_activated"].any()
    assert mem.anchor_bank.stability_score.max().item() > 0


def test_active_stable_config_threads_to_model_args():
    cfg = dict(DEFAULTS)
    cfg["active_to_stable_threshold"] = 0.42
    cfg["stable_recall_strength"] = 0.33
    cfg["stability_prune_bonus"] = 2.5

    args = config_to_model_args(cfg)

    assert args["active_to_stable_threshold"] == 0.42
    assert args["stable_recall_strength"] == 0.33
    assert args["stability_prune_bonus"] == 2.5


if __name__ == "__main__":
    test_stability_score_increments_for_persistent_entries()
    test_stable_entries_survive_pruning()
    test_spatial_memory_promote_and_recall_from_stable()
    test_active_stable_config_threads_to_model_args()
    print("test_active_stable: OK")
