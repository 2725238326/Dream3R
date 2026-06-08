from __future__ import annotations

import json

import pytest
import torch

from dream3r.scripts.run_dream3r_v11_cache_demo import run_cache_demo
from dream3r.scripts.run_dream3r_v11_demo import run_demo


def _assert_demo_report(report, *, domain: str, branch: str, experts: int) -> None:
    assert report["status"] == "pass"
    assert report["version"] == "v1.1.0"
    assert report["domain"] == domain
    assert report["domain_branch"] == branch
    assert report["demo_mode"] == "synthetic_proposal_bank_runtime"
    assert report["official_api"] == "dream3r.release_v11.build_dream3r_v11_release"
    assert report["input_contract"]["proposal_pointmaps_shape"] == [1, experts, 1, 3, 3]
    assert report["output_contract"]["final_pointmap_shape"] == [1, 1, 3, 3]
    assert report["output_contract"]["expert_weights_shape"] == [1, experts, 1, 3]
    assert 0.999 <= report["output_contract"]["expert_weight_sum_min"] <= 1.001
    assert 0.999 <= report["output_contract"]["expert_weight_sum_max"] <= 1.001
    assert report["selected_metrics"]["metric_direction"] == "lower_is_better"
    assert "proposal-free foundation 3R" in report["claim_boundary"]["not_claimed"]


def test_v11_demo_writes_kitti_json(tmp_path):
    output = tmp_path / "demo_kitti.json"

    report = run_demo(domain="kitti", output=output, seed=13, batch=1, views=1, patches=3)

    _assert_demo_report(report, domain="kitti", branch="kitti_v1_0_rc1", experts=3)
    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8"))["domain"] == "kitti"


def test_v11_demo_writes_eth3d_json(tmp_path):
    output = tmp_path / "demo_eth3d.json"

    report = run_demo(domain="eth3d", output=output, seed=13, batch=1, views=1, patches=3)

    _assert_demo_report(report, domain="eth3d", branch="eth3d_vggt_omega_scf", experts=4)
    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8"))["domain"] == "eth3d"


def _write_mock_cache(path, *, domain: str, expert_order: list[str]) -> None:
    torch.manual_seed(3)
    views, patches = 1, 3
    proposals = {}
    gt = torch.randn(views, patches, 3)
    for name in expert_order:
        proposals[name] = {
            "pointmap": gt + 0.01 * torch.randn(views, patches, 3),
            "confidence": torch.rand(views, patches, 1),
        }
    torch.save(
        {
            "entries": [
                {
                    "domain": domain,
                    "sequence": f"{domain}_mock",
                    "window_id": 0,
                    "proposals": proposals,
                    "memory_context": torch.randn(32),
                    "conflict_score": 0.25,
                    "gt_pointmap": gt,
                    "gt_mask": torch.ones(views, patches, dtype=torch.bool),
                }
            ],
            "d_memory": 32,
            "expert_order": expert_order,
        },
        path,
    )


def test_v11_cache_demo_runs_kitti_mock_cache(tmp_path):
    cache = tmp_path / "kitti_cache.pt"
    output = tmp_path / "cache_demo_kitti.json"
    _write_mock_cache(cache, domain="kitti", expert_order=["fast3r", "mast3r", "spann3r"])

    report = run_cache_demo(
        domain="kitti",
        cache_paths=[cache],
        output=output,
        max_entries=1,
        device_name="cpu",
    )

    assert report["status"] == "pass"
    assert report["demo_mode"] == "proposal_cache_runtime"
    assert report["domain"] == "kitti"
    assert report["expert_order"] == ["fast3r", "mast3r", "spann3r"]
    assert report["items"][0]["output"]["domain_branch"] == "kitti_v1_0_rc1"
    assert report["items"][0]["output"]["final_pointmap_shape"] == [1, 1, 3, 3]
    assert report["aggregate"]["mean_abs_rel_vs_cache_gt"] is not None
    assert json.loads(output.read_text(encoding="utf-8"))["domain"] == "kitti"


def test_v11_cache_demo_runs_eth3d_mock_cache(tmp_path):
    cache = tmp_path / "eth3d_cache.pt"
    output = tmp_path / "cache_demo_eth3d.json"
    _write_mock_cache(
        cache,
        domain="eth3d",
        expert_order=["fast3r", "mast3r", "spann3r", "vggt_omega"],
    )

    report = run_cache_demo(
        domain="eth3d",
        cache_paths=[cache],
        output=output,
        max_entries=1,
        device_name="cpu",
    )

    assert report["status"] == "pass"
    assert report["domain"] == "eth3d"
    assert report["expert_order"] == ["fast3r", "mast3r", "spann3r", "vggt_omega"]
    assert report["items"][0]["output"]["domain_branch"] == "eth3d_vggt_omega_scf"
    assert report["items"][0]["output"]["expert_weights_shape"] == [1, 4, 1, 3]
    assert json.loads(output.read_text(encoding="utf-8"))["domain"] == "eth3d"


def test_v11_cache_demo_rejects_wrong_expert_order(tmp_path):
    cache = tmp_path / "bad_cache.pt"
    _write_mock_cache(
        cache,
        domain="kitti",
        expert_order=["fast3r", "mast3r", "spann3r", "vggt_omega"],
    )

    with pytest.raises(ValueError, match="requires expert_order"):
        run_cache_demo(domain="kitti", cache_paths=[cache], device_name="cpu")
