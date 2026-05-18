"""Tests for CR-3 retrieval policy wiring."""

import torch

from dream3r.bus import EvidenceLabel, MemoryBus
from dream3r.model import build_dream3r
from dream3r.nsa_attention import NSAAttention


def test_cr3_uses_previous_conflict_to_scale_top_k():
    bus = MemoryBus()
    bus.publish("conflict_score", torch.tensor([[2.0]]), EvidenceLabel.INFERRED,
                "critic", timestep=0)
    bus.reset()

    assert bus.gate_cr3(base_k=8) > 8
    assert bus.cr3_retrieval_bias() is not None


def test_cr3_low_conflict_does_not_apply_retrieval_bias():
    bus = MemoryBus()
    bus.publish("conflict_score", torch.tensor([[-20.0]]), EvidenceLabel.INFERRED,
                "critic", timestep=0)
    bus.reset()

    assert bus.gate_cr3(base_k=8) == 8
    confidence = bus.cr3_retrieval_bias()
    assert confidence is not None
    assert torch.allclose(confidence, torch.ones_like(confidence), atol=1e-5)


def test_permanence_bias_prefers_stable_bank_entries():
    nsa = NSAAttention(d_model=16, n_compress=2, n_select_k=2, n_heads=2)
    query = torch.zeros(1, 1, 16)
    compressed = torch.zeros(1, 2, 16)
    bank_k = torch.zeros(1, 4, 16)
    bank_v = torch.randn(1, 4, 16)
    sliding = torch.zeros(1, 2, 16)

    result = nsa(
        query, compressed, bank_k, bank_v, sliding,
        permanence_bias=torch.tensor([[0.0, 0.0, 2.0, 3.0]]),
    )

    selected = result["selected_indices"][0, 0].tolist()
    assert 3 in selected
    assert result["retrieval_log"]["permanence_bias_applied"].item() > 0


def test_model_exposes_cr3_retrieval_log_from_previous_conflict():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()

    model.bus.publish("conflict_score", torch.tensor([[2.0]]), EvidenceLabel.INFERRED,
                      "critic", timestep=0)

    x = torch.randn(1, 4, 16, 768)
    with torch.no_grad():
        out = model(x, timestep=1)

    log = out["memory_retrieval_log"]
    assert log["effective_top_k"] > 8
    assert log["confidence_bias_applied"].item() > 0
    assert "selected_scores_before_bias" in log
    assert "selected_scores_after_bias" in log


if __name__ == "__main__":
    test_cr3_uses_previous_conflict_to_scale_top_k()
    test_cr3_low_conflict_does_not_apply_retrieval_bias()
    test_permanence_bias_prefers_stable_bank_entries()
    test_model_exposes_cr3_retrieval_log_from_previous_conflict()
    print("All CR-3 policy tests passed.")
