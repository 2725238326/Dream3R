"""Tests for W12 3D-aware AnchorBank retrieval."""

import torch

from dream3r.anchor_bank import AnchorBank


def test_3d_position_encoding_shape_and_finiteness():
    points = torch.randn(2, 4, 3)
    enc = AnchorBank.encode_3d_position(points, num_frequencies=5)
    assert enc.shape == (2, 4, 30)
    assert torch.isfinite(enc).all()


def test_spatial_retrieval_prefers_nearest_3d_anchor_when_latent_ties():
    bank = AnchorBank(capacity=4, d_key=4, d_value=4, spatial_bias_alpha=3.0)
    bank.reset(batch_size=1)

    keys = torch.zeros(1, 2, 4)
    values = torch.tensor([[[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0]]])
    points = torch.tensor([[[0.0, 0.0, 0.0],
                            [10.0, 0.0, 0.0]]])
    bank.write(keys, values, points3d_mean=points, source_patch_ids=torch.tensor([[0, 1]]))

    queries = torch.zeros(1, 1, 4)
    query_points = torch.tensor([[[9.8, 0.0, 0.0]]])
    result = bank.read(
        queries, top_k=1, query_points3d=query_points,
        spatial_retrieval_mode="latent_plus_3d",
    )

    assert result.indices.item() == 1
    assert torch.equal(result.points3d_mean[0, 0, 0], points[0, 1])


def test_latent_only_mode_matches_legacy_read():
    torch.manual_seed(0)
    bank = AnchorBank(capacity=8, d_key=8, d_value=8)
    bank.reset(batch_size=1)
    bank.write(
        torch.randn(1, 4, 8), torch.randn(1, 4, 8),
        points3d_mean=torch.randn(1, 4, 3),
    )

    queries = torch.randn(1, 3, 8)
    query_points = torch.randn(1, 3, 3)
    legacy = bank.read(queries, top_k=2, spatial_retrieval_mode="latent_only")
    explicit = bank.read(
        queries, top_k=2, query_points3d=query_points,
        spatial_retrieval_mode="latent_only",
    )

    assert torch.equal(legacy.indices, explicit.indices)
    assert torch.allclose(legacy.scores, explicit.scores)


if __name__ == "__main__":
    test_3d_position_encoding_shape_and_finiteness()
    test_spatial_retrieval_prefers_nearest_3d_anchor_when_latent_ties()
    test_latent_only_mode_matches_legacy_read()
    print("All 3D retrieval tests passed.")
