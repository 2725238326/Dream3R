from __future__ import annotations

import pytest
import torch

from dream3r.release_v11 import (
    ETH3D_EXPERT_ORDER,
    RELEASE_V11_CANDIDATE,
    RELEASE_V11_VERSION,
    Dream3RDomainConditionalConfig,
    Dream3RDomainConditionalRelease,
    build_dream3r_v11_release,
)


def test_v11_routes_kitti_to_release_candidate_branch() -> None:
    model = build_dream3r_v11_release()
    pointmaps = torch.randn(2, 3, 2, 4, 3)
    confidences = torch.rand(2, 3, 2, 4, 1)
    memory = torch.randn(2, 32)
    conflict = torch.randn(2, 1)

    out = model(pointmaps, confidences, memory, conflict, domain="kitti")

    assert out["final_pointmap"].shape == (2, 2, 4, 3)
    assert out["final_confidence"].shape == (2, 2, 4, 1)
    assert out["expert_weights"].shape == (2, 3, 2, 4)
    assert out["release_version"] == RELEASE_V11_VERSION
    assert out["domain_branch"] == "kitti_v1_0_rc1"


def test_v11_routes_eth3d_to_vggt_expanded_scf_branch() -> None:
    model = build_dream3r_v11_release()
    pointmaps = torch.randn(2, 4, 2, 4, 3)
    confidences = torch.rand(2, 4, 2, 4, 1)
    memory = torch.randn(2, 32)
    conflict = torch.randn(2, 1)

    out = model(pointmaps, confidences, memory, conflict, domain="eth3d")

    assert out["final_pointmap"].shape == (2, 2, 4, 3)
    assert out["final_confidence"].shape == (2, 2, 4, 1)
    assert out["expert_weights"].shape == (2, 4, 2, 4)
    assert out["release_version"] == RELEASE_V11_VERSION
    assert out["domain_branch"] == "eth3d_vggt_omega_scf"
    assert torch.allclose(out["expert_weights"].sum(dim=1), torch.ones(2, 2, 4), atol=1e-5)


def test_v11_metadata_records_policy_and_metrics() -> None:
    meta = build_dream3r_v11_release().release_metadata()

    assert meta["version"] == RELEASE_V11_VERSION
    assert meta["release_candidate"] == RELEASE_V11_CANDIDATE
    assert meta["metric_direction"] == "lower_is_better"
    assert meta["selected_kitti_abs_rel"] == 0.1448
    assert meta["selected_eth3d_abs_rel"] == 0.0570
    assert meta["expert_order"]["eth3d"] == list(ETH3D_EXPERT_ORDER)
    assert meta["controls"]["eth3d_state_abs_rel"] < meta["controls"]["eth3d_no_state_abs_rel"]
    assert meta["controls"]["eth3d_state_abs_rel"] < meta["controls"]["eth3d_shuffle_abs_rel"]


def test_v11_builder_accepts_cache_memory_dimension_override() -> None:
    model = build_dream3r_v11_release(d_memory=128)
    pointmaps = torch.randn(1, 3, 1, 3, 3)
    confidences = torch.rand(1, 3, 1, 3, 1)
    memory = torch.randn(1, 128)
    conflict = torch.randn(1, 1)

    out = model(pointmaps, confidences, memory, conflict, domain="kitti")

    assert out["final_pointmap"].shape == (1, 1, 3, 3)
    assert model.config.kitti.d_memory == 128
    assert model.config.eth3d_d_memory == 128


def test_v11_candidate_conflict_dampening_keeps_eth3d_contract() -> None:
    model = build_dream3r_v11_release(eth3d_conflict_dampening_strength=0.35)
    pointmaps = torch.randn(1, 4, 1, 3, 3)
    confidences = torch.rand(1, 4, 1, 3, 1)
    memory = torch.randn(1, 32)
    conflict = torch.ones(1, 1)

    out = model(pointmaps, confidences, memory, conflict, domain="eth3d")

    assert model.config.eth3d_conflict_dampening_strength == 0.35
    assert model.release_metadata()["config"]["eth3d_conflict_dampening_strength"] == 0.35
    assert out["final_pointmap"].shape == (1, 1, 3, 3)
    assert out["final_confidence"].shape == (1, 1, 3, 1)
    assert out["expert_weights"].shape == (1, 4, 1, 3)
    assert out["release_version"] == RELEASE_V11_VERSION
    assert out["domain_branch"] == "eth3d_vggt_omega_scf"


def test_v11_rejects_unsupported_domain_and_bad_config() -> None:
    model = build_dream3r_v11_release()
    pointmaps = torch.randn(1, 3, 1, 2, 3)
    confidences = torch.rand(1, 3, 1, 2, 1)

    with pytest.raises(ValueError, match="unsupported domain"):
        model(pointmaps, confidences, domain="nyu")

    with pytest.raises(ValueError, match="use_state=True"):
        Dream3RDomainConditionalRelease(
            Dream3RDomainConditionalConfig(eth3d_use_state=False)
        )

    with pytest.raises(ValueError, match="conflict_dampening_strength"):
        Dream3RDomainConditionalRelease(
            Dream3RDomainConditionalConfig(eth3d_conflict_dampening_strength=1.5)
        )


def test_v11_loads_eth3d_scf_checkpoint(tmp_path) -> None:
    model = build_dream3r_v11_release()
    ckpt = tmp_path / "eth3d_latest.pt"
    torch.save(
        {
            "head_state_dict": model.eth3d_head.state_dict(),
            "config": {
                "n_experts": 4,
                "d_memory": 32,
                "head_dim": 64,
                "hidden": 128,
                "use_state": True,
                "use_residual": False,
                "expert_order": list(ETH3D_EXPERT_ORDER),
            },
        },
        ckpt,
    )

    loaded = build_dream3r_v11_release(eth3d_checkpoint=ckpt)

    assert loaded.release_metadata()["version"] == RELEASE_V11_VERSION
    assert loaded.config.eth3d_n_experts == 4
    assert loaded.config.eth3d_expert_order == ETH3D_EXPERT_ORDER
