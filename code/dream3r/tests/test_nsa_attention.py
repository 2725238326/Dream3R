"""Unit tests for NSA attention module."""

import torch
from dream3r.nsa_attention import NSAAttention, NSABranch


def test_nsa_branch_shapes():
    branch = NSABranch(d_model=64, n_heads=4)
    q = torch.randn(2, 10, 64)
    k = torch.randn(2, 20, 64)
    v = torch.randn(2, 20, 64)
    out = branch(q, k, v)
    assert out.shape == (2, 10, 64), f"Expected (2,10,64), got {out.shape}"


def test_nsa_branch_with_mask():
    branch = NSABranch(d_model=64, n_heads=4)
    q = torch.randn(2, 5, 64)
    k = torch.randn(2, 8, 64)
    v = torch.randn(2, 8, 64)
    mask = torch.ones(2, 5, 8, dtype=torch.bool)
    mask[:, :, 6:] = False
    out = branch(q, k, v, mask=mask)
    assert out.shape == (2, 5, 64)


def test_nsa_full_forward():
    nsa = NSAAttention(d_model=64, n_compress=8, n_select_k=4, n_heads=4)
    B, Q, M, W = 2, 16, 32, 12
    query = torch.randn(B, Q, 64)
    compressed = torch.randn(B, 8, 64)
    bank_k = torch.randn(B, M, 64)
    bank_v = torch.randn(B, M, 64)
    sliding = torch.randn(B, W, 64)

    result = nsa(query, compressed, bank_k, bank_v, sliding)
    assert result["output"].shape == (B, Q, 64)
    assert result["branch_weights"].shape == (B, Q, 3)
    assert result["selected_indices"].shape == (B, Q, 4)
    assert result["retrieval_log"]["effective_top_k"] == 4

    weights_sum = result["branch_weights"].sum(dim=-1)
    assert torch.allclose(weights_sum, torch.ones_like(weights_sum), atol=1e-5)
    assert (result["branch_weights"] == 0).sum(dim=-1).min() == 1
    assert result["retrieval_log"]["branch_active_mask"].shape == (B, Q, 3)


def test_nsa_with_bank_mask():
    nsa = NSAAttention(d_model=64, n_compress=4, n_select_k=3, n_heads=2)
    B, Q, M = 1, 4, 10
    query = torch.randn(B, Q, 64)
    compressed = torch.randn(B, 4, 64)
    bank_k = torch.randn(B, M, 64)
    bank_v = torch.randn(B, M, 64)
    sliding = torch.randn(B, 6, 64)
    mask = torch.ones(B, M, dtype=torch.bool)
    mask[0, 7:] = False

    result = nsa(query, compressed, bank_k, bank_v, sliding, bank_mask=mask)
    assert result["output"].shape == (B, Q, 64)
    assert result["selected_indices"].max() < 10


def test_nsa_gradient_flow():
    nsa = NSAAttention(d_model=32, n_compress=4, n_select_k=2, n_heads=2)
    query = torch.randn(1, 4, 32, requires_grad=True)
    compressed = torch.randn(1, 4, 32)
    bank_k = torch.randn(1, 8, 32)
    bank_v = torch.randn(1, 8, 32)
    sliding = torch.randn(1, 4, 32)

    result = nsa(query, compressed, bank_k, bank_v, sliding)
    loss = result["output"].sum()
    loss.backward()
    assert query.grad is not None
    assert not torch.isnan(query.grad).any()


def test_nsa_cr3_confidence_and_permanence_bias_log():
    nsa = NSAAttention(d_model=16, n_compress=2, n_select_k=2, n_heads=2)
    with torch.no_grad():
        nsa.confidence_bias_strength.fill_(1.5)

    query = torch.zeros(1, 1, 16)
    compressed = torch.zeros(1, 2, 16)
    bank_k = torch.zeros(1, 4, 16)
    bank_v = torch.randn(1, 4, 16)
    sliding = torch.zeros(1, 2, 16)
    permanence_bias = torch.tensor([[0.0, 0.0, 3.0, 4.0]])

    result = nsa(
        query, compressed, bank_k, bank_v, sliding,
        critic_confidence=torch.tensor([[0.25]]),
        permanence_bias=permanence_bias,
        dynamic_top_k=3,
    )

    log = result["retrieval_log"]
    assert result["selected_indices"].shape == (1, 1, 3)
    assert log["effective_top_k"] == 3
    assert log["confidence_bias_applied"].item() > 0
    assert log["permanence_bias_applied"].item() > 0
    assert 3 in result["selected_indices"][0, 0].tolist()
    assert log["selected_scores_after_bias"].max() > log["selected_scores_before_bias"].max()


def test_nsa_geometry_bias_prefers_nearby_3d_anchors():
    nsa = NSAAttention(d_model=16, n_compress=2, n_select_k=1, n_heads=2)
    query = torch.zeros(1, 1, 16)
    compressed = torch.zeros(1, 2, 16)
    bank_k = torch.zeros(1, 4, 16)
    bank_v = torch.randn(1, 4, 16)
    sliding = torch.zeros(1, 2, 16)
    query_points = torch.tensor([[[0.0, 0.0, 0.0]]])
    bank_points = torch.tensor([[[0.1, 0.0, 0.0],
                                 [10.0, 0.0, 0.0],
                                 [20.0, 0.0, 0.0],
                                 [30.0, 0.0, 0.0]]])

    result = nsa(
        query, compressed, bank_k, bank_v, sliding,
        query_points3d=query_points,
        bank_points3d=bank_points,
    )
    log = result["retrieval_log"]

    assert result["selected_indices"].item() == 0
    assert log["geometry_bias_applied"].item() > 0
    assert log["selected_3d_distances"].shape == (1, 1, 1)
    assert log["selected_scores_after_bias"].item() > -0.1


if __name__ == "__main__":
    test_nsa_branch_shapes()
    test_nsa_branch_with_mask()
    test_nsa_full_forward()
    test_nsa_with_bank_mask()
    test_nsa_gradient_flow()
    test_nsa_cr3_confidence_and_permanence_bias_log()
    test_nsa_geometry_bias_prefers_nearby_3d_anchors()
    print("All NSA attention tests passed.")
