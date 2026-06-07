from __future__ import annotations

import json
from pathlib import Path

import torch

from dream3r.scripts.train_foundation3r import (
    _load_caches,
    _masked_log_depth_l1,
    _resolve_loss_weights,
    _scale_normalize_pointmap,
    train,
)


def _entry(i: int):
    gt = torch.rand(2, 4, 3) + 0.5
    return {
        "window_id": f"w{i}",
        "seq": f"w{i}",
        "domain": "kitti" if i < 4 else "eth3d",
        "frames": [f"fake_{i}_0.jpg", f"fake_{i}_1.jpg"],
        "images": torch.rand(2, 3, 8, 8),
        "vggt_patch_features": torch.rand(2, 4, 6),
        "teacher_backend": "mock",
        "teacher_pointmap": gt + 0.01,
        "teacher_confidence": torch.ones(2, 4, 1),
        "teacher_valid_mask": torch.ones(2, 4, dtype=torch.bool),
        "memory_context": torch.randn(5),
        "conflict_score": 0.1 * i,
        "gt_pointmap": gt,
        "gt_mask": torch.ones(2, 4),
    }


def test_foundation3r_cache_loader_rejects_proposal_leak(tmp_path: Path):
    cache = tmp_path / "bad.pt"
    entry = _entry(0)
    entry["proposals"] = {"bad": {"pointmap": object()}}
    torch.save({
        "cache_type": "foundation3r_dense_teacher",
        "proposal_inputs_used": False,
        "teacher_used_at_inference": False,
        "proposal_fields_stripped": True,
        "entries": [entry],
    }, cache)

    try:
        _load_caches([str(cache)])
    except ValueError as exc:
        assert "forbidden" in str(exc) or "leaks" in str(exc)
    else:
        raise AssertionError("expected proposal leak to fail")


def test_train_foundation3r_smoke_uses_no_proposals(tmp_path: Path):
    entries = [_entry(i) for i in range(8)]
    cache = tmp_path / "cache.pt"
    torch.save({
        "cache_type": "foundation3r_dense_teacher",
        "proposal_inputs_used": False,
        "teacher_used_at_inference": False,
        "proposal_fields_stripped": True,
        "entries": entries,
    }, cache)

    out = train(
        [str(cache)],
        str(tmp_path / "out"),
        seed=1,
        epochs=1,
        lr=1e-3,
        holdout_frac=0.25,
        image_size=8,
        patch_size=4,
        model_dim=16,
        state_dim=8,
        hidden=24,
        num_layers=1,
        num_heads=4,
    )

    result = json.loads((tmp_path / "out" / "results.json").read_text(encoding="utf-8"))
    assert out["proposal_inputs_used"] is False
    assert out["teacher_used_at_inference"] is False
    assert result["proposal_inputs_used"] is False
    assert result["teacher_used_at_inference"] is False
    assert result["scale_normalized_targets"] is True
    assert result["loss_profile"] == "hybrid"
    assert result["gt_weight"] == 1.0
    assert result["depth_weight"] == 1.0
    assert "final_train_eval" in result
    assert (tmp_path / "out" / "latest.pt").exists()


def test_train_foundation3r_vggt_feature_mode_uses_no_proposals(tmp_path: Path):
    entries = [_entry(i) for i in range(8)]
    cache = tmp_path / "cache.pt"
    torch.save({
        "cache_type": "foundation3r_dense_teacher",
        "proposal_inputs_used": False,
        "teacher_used_at_inference": False,
        "proposal_fields_stripped": True,
        "vggt_features_included": True,
        "vggt_feature_dim": 6,
        "entries": entries,
    }, cache)

    out = train(
        [str(cache)],
        str(tmp_path / "out_vggt"),
        seed=1,
        epochs=1,
        lr=1e-3,
        holdout_frac=0.25,
        image_size=8,
        patch_size=4,
        input_mode="vggt_features",
        model_dim=16,
        state_dim=8,
        hidden=24,
        num_layers=1,
        num_heads=4,
    )

    result = json.loads((tmp_path / "out_vggt" / "results.json").read_text(encoding="utf-8"))
    assert out["proposal_inputs_used"] is False
    assert out["teacher_used_at_inference"] is False
    assert result["input_mode"] == "vggt_features"
    assert result["d_vggt_feature"] == 6
    assert result["vggt_backbone_features_used"] is True
    assert result["loss_profile"] == "teacher_only"
    assert result["teacher_weight"] == 1.0
    assert result["gt_weight"] == 0.0
    assert result["depth_weight"] == 0.0


def test_vggt_loss_profile_allows_explicit_weight_override():
    assert _resolve_loss_weights("vggt_features", "auto", None, None, None) == (
        1.0,
        0.0,
        0.0,
        "teacher_only",
    )
    assert _resolve_loss_weights("vggt_features", "auto", None, 0.5, 0.25) == (
        1.0,
        0.5,
        0.25,
        "teacher_only",
    )


def test_scale_normalize_pointmap_uses_median_depth():
    pointmap = torch.tensor([[[[2.0, 0.0, 2.0], [4.0, 0.0, 4.0], [8.0, 0.0, 8.0]]]])
    mask = torch.tensor([[[True, True, True]]])

    out = _scale_normalize_pointmap(pointmap, mask)

    assert torch.allclose(out[..., 2], torch.tensor([[[0.5, 1.0, 2.0]]]))


def test_log_depth_loss_is_scale_invariant():
    pred = torch.tensor([[[[0.0, 0.0, 2.0], [0.0, 0.0, 4.0]]]])
    target = torch.tensor([[[[0.0, 0.0, 4.0], [0.0, 0.0, 8.0]]]])
    mask = torch.tensor([[[True, True]]])

    loss = _masked_log_depth_l1(pred, target, mask)

    assert float(loss.item()) < 1e-6
