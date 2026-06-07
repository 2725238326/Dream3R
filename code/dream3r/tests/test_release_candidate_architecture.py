from __future__ import annotations

import torch
import pytest

from dream3r.release_candidate import (
    Dream3RReleaseCandidate,
    Dream3RReleaseConfig,
    RELEASE_CANDIDATE,
    RELEASE_VERSION,
    build_dream3r_release_candidate,
)


def test_release_candidate_forward_contract() -> None:
    model = build_dream3r_release_candidate(d_memory=8)
    pointmaps = torch.randn(2, 3, 2, 4, 3)
    confidences = torch.rand(2, 3, 2, 4, 1)
    memory = torch.randn(2, 8)
    conflict = torch.randn(2, 1)

    out = model(pointmaps, confidences, memory, conflict)

    assert out["final_pointmap"].shape == (2, 2, 4, 3)
    assert out["base_pointmap"].shape == (2, 2, 4, 3)
    assert out["residual_delta"].shape == (2, 2, 4, 3)
    assert out["final_confidence"].shape == (2, 2, 4, 1)
    assert out["expert_weights"].shape == (2, 3, 2, 4)
    assert torch.allclose(out["expert_weights"].sum(dim=1), torch.ones(2, 2, 4), atol=1e-5)


def test_release_candidate_metadata_is_versioned() -> None:
    model = build_dream3r_release_candidate(d_memory=8)
    meta = model.release_metadata()

    assert meta["version"] == RELEASE_VERSION
    assert meta["release_candidate"] == RELEASE_CANDIDATE
    assert meta["expert_order"] == ["fast3r", "mast3r", "spann3r"]
    assert meta["metric_direction"] == "lower_is_better"
    assert meta["selected_kitti_abs_rel"] == 0.1448
    assert meta["selected_eth3d_abs_rel"] == 0.1475


def test_release_candidate_rejects_non_official_config() -> None:
    with pytest.raises(ValueError, match="use_state=True"):
        Dream3RReleaseCandidate(Dream3RReleaseConfig(use_state=False))

    with pytest.raises(ValueError, match="bounded residual"):
        Dream3RReleaseCandidate(Dream3RReleaseConfig(residual_refine_scale=0.0))


def test_release_candidate_loads_checkpoint_config(tmp_path) -> None:
    model = build_dream3r_release_candidate(d_memory=8)
    ckpt = tmp_path / "latest.pt"
    torch.save(
        {
            "decoder_state_dict": model.decoder.state_dict(),
            "config": model.release_metadata()["config"],
        },
        ckpt,
    )

    loaded = build_dream3r_release_candidate(ckpt)

    assert loaded.release_metadata()["version"] == RELEASE_VERSION
    assert loaded.config.d_memory == 8
