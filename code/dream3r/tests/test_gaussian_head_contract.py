"""Dependency-free W18 Gaussian tensor contract tests."""

import torch

from dream3r.gaussian_head import GaussianHead


def test_gaussian_head_outputs_shape_and_range_contract():
    torch.manual_seed(0)
    head = GaussianHead(d_input=8)
    tokens = torch.randn(2, 5, 8)
    means = torch.randn(2, 5, 3)
    confidence = torch.rand(2, 5, 1)
    source_anchor_ids = torch.tensor([[0, 1, 2, -1, -1],
                                      [4, 5, -1, -1, -1]])

    out = head(
        tokens,
        means,
        confidence=confidence,
        source_anchor_ids=source_anchor_ids,
    )

    assert out["means"].shape == (2, 5, 3)
    assert out["scales"].shape == (2, 5, 3)
    assert out["rotations"].shape == (2, 5, 4)
    assert out["colors"].shape == (2, 5, 3)
    assert out["opacity"].shape == (2, 5, 1)
    assert out["source_anchor_ids"].shape == (2, 5)

    assert torch.all(out["scales"] > 0)
    assert torch.all((out["colors"] >= 0) & (out["colors"] <= 1))
    assert torch.all((out["opacity"] >= 0) & (out["opacity"] <= 1))
    assert torch.allclose(
        out["rotations"].norm(dim=-1),
        torch.ones(2, 5),
        atol=1e-5,
    )
    assert torch.equal(out["source_anchor_ids"], source_anchor_ids)


def test_gaussian_head_defaults_to_transient_frame_gaussians():
    head = GaussianHead(d_input=4)
    out = head(torch.zeros(1, 3, 4), torch.zeros(1, 3, 3))

    assert out["source_anchor_ids"].tolist() == [[-1, -1, -1]]


if __name__ == "__main__":
    test_gaussian_head_outputs_shape_and_range_contract()
    test_gaussian_head_defaults_to_transient_frame_gaussians()
    print("All Gaussian head contract tests passed.")
