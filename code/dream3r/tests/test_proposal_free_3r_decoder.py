from __future__ import annotations

import json
from pathlib import Path

import torch

from dream3r.proposal_free_3r_decoder import ProposalFree3RDecoder
from dream3r.scripts.build_proposal_free_teacher_cache import (
    build_proposal_free_teacher_cache,
)
from dream3r.scripts.train_proposal_free_3r import (
    _load_proposal_free_caches,
    train,
)


def test_proposal_free_decoder_has_no_proposal_inputs():
    model = ProposalFree3RDecoder(
        d_image=16,
        d_memory=8,
        model_dim=24,
        state_dim=12,
        hidden=32,
        num_layers=1,
        num_heads=4,
    )
    image_tokens = torch.randn(2, 3, 5, 16, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    out = model(image_tokens, memory, conflict)
    loss = out["final_pointmap"].pow(2).mean() + out["final_confidence"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 3, 5, 3)
    assert out["final_confidence"].shape == (2, 3, 5, 1)
    assert bool(out["proposal_inputs_used"].item()) is False
    assert image_tokens.grad is not None
    assert memory.grad is not None


def test_proposal_free_cache_loader_requires_image_tokens(tmp_path: Path):
    bad_cache = tmp_path / "bad.pt"
    torch.save({"d_image": 4, "d_memory": 3, "entries": [{"gt_mask": torch.ones(1)}]}, bad_cache)

    try:
        _load_proposal_free_caches([str(bad_cache)])
    except ValueError as exc:
        assert "image_tokens" in str(exc)
    else:
        raise AssertionError("expected missing image_tokens to fail")


def test_proposal_free_trainer_smoke_uses_no_proposals(tmp_path: Path):
    entries = []
    for i in range(6):
        entries.append({
            "seq": f"win_{i}",
            "domain": "kitti" if i < 4 else "eth3d",
            "image_tokens": torch.randn(2, 3, 8),
            "memory_context": torch.randn(5),
            "conflict_score": 0.1 * i,
            "gt_pointmap": torch.rand(2, 3, 3) + 0.1,
            "gt_mask": torch.ones(2, 3),
            # Deliberately poison proposals: trainer must not read them.
            "proposals": {"bad": {"pointmap": object()}},
        })
    cache = tmp_path / "cache.pt"
    torch.save({"d_image": 8, "d_memory": 5, "entries": entries}, cache)

    out = train(
        [str(cache)],
        str(tmp_path / "out"),
        seed=1,
        epochs=1,
        lr=1e-3,
        holdout_frac=0.34,
    )

    result = json.loads((tmp_path / "out" / "results.json").read_text(encoding="utf-8"))
    assert out["proposal_inputs_used"] is False
    assert result["proposal_inputs_used"] is False
    assert (tmp_path / "out" / "latest.pt").exists()


def test_teacher_cache_builder_strips_proposals_and_trainer_distills(tmp_path: Path):
    entries = []
    for i in range(6):
        gt = torch.rand(2, 3, 3) + 0.5
        entries.append({
            "seq": f"win_{i}",
            "domain": "kitti",
            "image_tokens": torch.randn(2, 3, 8),
            "memory_context": torch.randn(5),
            "conflict_score": 0.0,
            "gt_pointmap": gt,
            "gt_mask": torch.ones(2, 3),
            "proposals": {
                "good": {"pointmap": gt + 0.01, "confidence": torch.ones(2, 3, 1)},
                "bad": {"pointmap": gt + 1.0, "confidence": torch.ones(2, 3, 1)},
            },
        })
    source = tmp_path / "image_cache.pt"
    teacher_cache = tmp_path / "teacher_cache.pt"
    torch.save({
        "d_image": 8,
        "d_memory": 5,
        "expert_order": ["bad", "good"],
        "entries": entries,
    }, source)

    built = build_proposal_free_teacher_cache([str(source)], str(teacher_cache))
    saved = torch.load(teacher_cache, map_location="cpu", weights_only=False)

    assert built["proposal_fields_stripped"] is True
    assert "teacher_pointmap" in saved["entries"][0]
    assert "proposals" not in saved["entries"][0]
    assert saved["entries"][0]["teacher_name"] == "good"

    out = train(
        [str(teacher_cache)],
        str(tmp_path / "distill_out"),
        seed=1,
        epochs=1,
        lr=1e-3,
        holdout_frac=0.34,
        teacher_weight=0.5,
        teacher_absrel_weight=0.25,
        model_dim=32,
        hidden=48,
        num_layers=1,
    )

    assert out["teacher_weight"] == 0.5
    assert out["teacher_absrel_weight"] == 0.25
    assert out["model_dim"] == 32
    assert out["proposal_inputs_used"] is False
