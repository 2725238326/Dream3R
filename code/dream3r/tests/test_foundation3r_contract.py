from __future__ import annotations

import json
from pathlib import Path

import torch

from dream3r.foundation3r_decoder import Foundation3RDecoder, Foundation3RVGGTFeatureDecoder
from dream3r.scripts.build_foundation3r_dense_teacher_cache import (
    FORBIDDEN_ENTRY_KEYS,
    build_foundation3r_dense_teacher_cache,
)


def test_foundation3r_forward_is_proposal_free():
    model = Foundation3RDecoder(
        d_memory=8,
        patch_size=4,
        model_dim=24,
        state_dim=12,
        hidden=32,
        num_layers=1,
        num_heads=4,
    )
    images = torch.randn(2, 3, 3, 16, 16, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    out = model(images, memory, conflict)
    loss = out["final_pointmap"].pow(2).mean() + out["final_confidence"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 3, 16, 3)
    assert out["final_confidence"].shape == (2, 3, 16, 1)
    assert bool((out["final_pointmap"][..., 2] > 0).all()) is True
    assert bool(out["proposal_inputs_used"].item()) is False
    assert bool(out["teacher_used_at_inference"].item()) is False
    assert images.grad is not None
    assert memory.grad is not None


def test_foundation3r_uses_patch_coordinates_on_flat_images():
    model = Foundation3RDecoder(
        d_memory=4,
        patch_size=4,
        model_dim=16,
        state_dim=8,
        hidden=24,
        num_layers=1,
        num_heads=4,
    )
    out = model(torch.zeros(1, 1, 3, 16, 16))

    first_patch = out["final_pointmap"][0, 0, 0]
    last_patch = out["final_pointmap"][0, 0, -1]
    assert not torch.allclose(first_patch, last_patch)


def test_foundation3r_vggt_feature_decoder_is_proposal_free():
    model = Foundation3RVGGTFeatureDecoder(
        d_vggt_feature=8,
        d_memory=4,
        model_dim=16,
        state_dim=8,
        hidden=24,
        num_layers=1,
        num_heads=4,
    )
    features = torch.randn(2, 3, 9, 8, requires_grad=True)
    memory = torch.randn(2, 4, requires_grad=True)

    out = model(features, memory, torch.zeros(2, 1))
    loss = out["final_pointmap"].mean() + out["final_confidence"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 3, 9, 3)
    assert out["final_confidence"].shape == (2, 3, 9, 1)
    assert bool(out["proposal_inputs_used"].item()) is False
    assert bool(out["teacher_used_at_inference"].item()) is False
    assert bool(out["vggt_backbone_features_used"].item()) is True
    assert features.grad is not None
    assert memory.grad is not None


def test_foundation3r_forward_rejects_proposal_kwargs():
    model = Foundation3RDecoder(d_memory=4, patch_size=4, model_dim=16, hidden=24, num_layers=1)
    images = torch.randn(1, 2, 3, 8, 8)
    proposals = torch.randn(1, 2, 4, 3)

    try:
        model(images, proposal_pointmaps=proposals)
    except TypeError as exc:
        assert "proposal_pointmaps" in str(exc)
    else:
        raise AssertionError("Foundation3RDecoder accepted proposal inputs")


def test_dense_teacher_cache_builder_strips_proposals_and_writes_report(tmp_path: Path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "schema_version": "test",
        "windows": [
            {
                "window_id": "kitti/w0",
                "dataset": "kitti",
                "sequence": "w0",
                "frames": ["a.jpg", "b.jpg"],
                "proposals": {"poison": "must not be copied"},
            }
        ],
    }), encoding="utf-8")
    state_cache = tmp_path / "state.pt"
    torch.save({
        "entries": [
            {
                "seq": "w0",
                "domain": "kitti",
                "memory_context": torch.randn(6),
                "conflict_score": 0.25,
                "gt_pointmap": torch.rand(2, 9, 3),
                "gt_mask": torch.ones(2, 9),
                "proposals": {"bad": {"pointmap": object()}},
            }
        ]
    }, state_cache)
    output = tmp_path / "foundation_cache.pt"

    result = build_foundation3r_dense_teacher_cache(
        window_manifest=str(manifest),
        output=str(output),
        backend="mock",
        state_caches=[str(state_cache)],
        n_patches=9,
        include_vggt_features=True,
        vggt_feature_dim=8,
    )

    saved = torch.load(output, map_location="cpu", weights_only=False)
    report = json.loads(output.with_suffix(".json").read_text(encoding="utf-8"))
    entry = saved["entries"][0]

    assert result["schema_version"] == "dream3r_foundation3r_dense_teacher_cache_v1"
    assert result["proposal_inputs_used"] is False
    assert result["teacher_used_at_inference"] is False
    assert result["vggt_features_included"] is True
    assert result["proposal_fields_stripped"] is True
    assert report["n_windows"] == 1
    assert entry["teacher_pointmap"].shape == (2, 9, 3)
    assert entry["teacher_confidence"].shape == (2, 9, 1)
    assert entry["teacher_valid_mask"].shape == (2, 9)
    assert entry["vggt_patch_features"].shape == (2, 9, 8)
    assert entry["vggt_feature_source"] == "vggt_omega_aggregator_final_patch_tokens_chunkmean"
    assert entry["memory_context"].shape == (6,)
    assert entry["gt_pointmap"].shape == (2, 9, 3)
    assert not any(key in entry for key in FORBIDDEN_ENTRY_KEYS)
