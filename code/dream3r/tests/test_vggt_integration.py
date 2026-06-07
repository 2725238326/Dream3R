"""Integration tests for VGGT adapter and capability_card v2.2 schema."""

import pytest
import torch

from dream3r.scripts.stage_vggt_omega_admission import stage_vggt_omega_admission
from dream3r.scripts.smoke_vggt_omega_adapter import _flatten_confidence
from dream3r.scripts.eval_vggt_omega_oracle_admission import (
    _dense_conf_to_patch_confidence,
    _dense_depth_to_patch_pointmap,
    _expanded_entry,
    _summarize_rows,
)
from dream3r.composer_experts import ExpertRegistry, get_all_adapters
from dream3r.composer_experts.base_adapter import ExpertAdapter
from dream3r.composer_experts.vggt_adapter import VGGTAdapter
from dream3r.composer_experts.method_profiles import (
    REGIME_ORDER, FEATURE_ORDER, METHOD_PROFILES, MethodProfile,
)


class TestVGGTAdapter:
    """VGGT adapter unit tests."""

    def setup_method(self):
        self.adapter = VGGTAdapter()

    def test_name(self):
        assert self.adapter.name == "vggt"

    def test_capability_card_has_all_regimes(self):
        for regime in ExpertAdapter.REGIMES:
            assert regime in self.adapter.capability_card, f"Missing regime: {regime}"

    def test_capability_card_feed_forward_manyview_highest(self):
        card = self.adapter.capability_card
        assert card["feed_forward_manyview"] >= max(
            v for k, v in card.items() if k != "feed_forward_manyview"
        )

    def test_fallback_output_shape(self):
        B, N, H, W = 2, 4, 224, 224
        images = torch.randn(B, N, 3, H, W)
        out = self.adapter.forward(images)
        # Fallback uses patch tokens from backbone (patch_size=16 → 14×14=196)
        P = out.pointmap.shape[2]
        assert out.pointmap.shape == (B, N, P, 3)
        assert out.confidence.shape == (B, N, P, 1)
        assert out.evidence_tokens.shape[0] == B
        assert out.evidence_tokens.shape[1] == N

    def test_not_loaded_by_default(self):
        assert not self.adapter.is_loaded
        assert not self.adapter.is_available()

    def test_load_checkpoint_marks_loaded(self):
        self.adapter.load_checkpoint("/fake/path/vggt.pth")
        assert self.adapter.is_loaded
        assert self.adapter.is_available()

    def test_attention_regime(self):
        assert self.adapter.attention_regime == "full"

    def test_latency_estimate(self):
        assert self.adapter.latency_estimate_ms == 45.0


class TestCapabilityCardV22:
    """Tests for capability_card schema v2.2 upgrade."""

    def test_regime_order_has_feed_forward_manyview(self):
        assert "feed_forward_manyview" in REGIME_ORDER

    def test_regime_order_length_is_6(self):
        assert len(REGIME_ORDER) == 6

    def test_feature_order_has_feed_forward_geometry(self):
        assert "feed_forward_geometry" in FEATURE_ORDER

    def test_vggt_in_method_profiles(self):
        assert "vggt" in METHOD_PROFILES

    def test_vggt_profile_fields(self):
        p = METHOD_PROFILES["vggt"]
        assert isinstance(p, MethodProfile)
        assert p.family == "feed-forward visual geometry transformer"
        assert "feed_forward_manyview" in p.regime_scores
        assert p.regime_scores["feed_forward_manyview"] == 0.95

    def test_all_profiles_have_v22_regime_tensor_length(self):
        for name, profile in METHOD_PROFILES.items():
            t = profile.regime_tensor()
            assert t.shape[0] == 6, f"{name} regime_tensor has wrong length"


class TestRegistryWith8Experts:
    """Registry integration after VGGT addition."""

    def setup_method(self):
        self.registry = get_all_adapters()

    def test_registry_has_8_experts(self):
        assert len(self.registry.names) == 8

    def test_vggt_in_registry(self):
        assert "vggt" in self.registry.names

    def test_capability_matrix_shape(self):
        mat = self.registry.capability_matrix()
        # 8 experts × 6 regimes
        assert mat.shape == (8, 6)

    def test_vggt_adapter_instantiates(self):
        adapter = self.registry.get("vggt")
        assert isinstance(adapter, VGGTAdapter)

    def test_all_adapters_have_feed_forward_manyview_in_card(self):
        for name in self.registry.names:
            adapter = self.registry.get(name)
            # Only VGGT must have it > 0; others default to 0
            val = adapter.capability_card.get("feed_forward_manyview", 0.0)
            if name == "vggt":
                assert val > 0.5
            else:
                assert val >= 0.0  # others can be 0

    def test_adapter_status_reports_vggt(self):
        status = self.registry.adapter_status()
        assert "vggt" in status
        assert status["vggt"]["backend"] == "fallback"


def test_stage_vggt_omega_admission_blocks_without_checkpoint_or_token(tmp_path, monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.delenv("HUGGINGFACE_HUB_TOKEN", raising=False)
    repo = tmp_path / "repo"
    repo.mkdir()
    image_list = tmp_path / "images.txt"
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"fake")
    image_list.write_text(str(image), encoding="utf-8")
    output = tmp_path / "stage.json"

    result = stage_vggt_omega_admission(
        repo=str(repo),
        checkpoint=str(tmp_path / "missing" / "model.pt"),
        image_list=str(image_list),
        output=str(output),
        download=False,
        run_smoke=False,
    )

    assert output.exists()
    assert result["status"] == "blocked"
    assert result["backend"] == "not_run"
    assert any(flag.startswith("checkpoint_missing:") for flag in result["failure_flags"])


def test_stage_vggt_omega_admission_ready_with_existing_checkpoint(tmp_path, monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.delenv("HUGGINGFACE_HUB_TOKEN", raising=False)
    repo = tmp_path / "repo"
    repo.mkdir()
    image_list = tmp_path / "images.txt"
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"fake")
    image_list.write_text(str(image), encoding="utf-8")
    checkpoint = tmp_path / "checkpoint" / "model.pt"
    checkpoint.parent.mkdir()
    checkpoint.write_bytes(b"not-a-real-checkpoint-for-stage-only")
    output = tmp_path / "stage.json"

    result = stage_vggt_omega_admission(
        repo=str(repo),
        checkpoint=str(checkpoint),
        image_list=str(image_list),
        output=str(output),
        download=False,
        run_smoke=False,
    )

    assert result["status"] == "ready"
    assert result["backend"] == "checkpoint_staged"
    assert result["checkpoint_size"] == checkpoint.stat().st_size
    assert "checkpoint_sha256" in result


def test_vggt_omega_confidence_accepts_batched_frame_tensor():
    conf = torch.ones(1, 2, 4, 5)

    flattened = _flatten_confidence(conf, n_frames=2)

    assert flattened.shape == (2, 20, 1)


def test_vggt_omega_dense_depth_downsamples_to_patch_pointmap():
    depth = torch.arange(2 * 8 * 8, dtype=torch.float32).reshape(2, 8, 8)

    pointmap = _dense_depth_to_patch_pointmap(depth, n_patches=16)

    assert pointmap.shape == (2, 16, 3)
    assert torch.all(pointmap[..., :2] == 0)
    assert torch.isfinite(pointmap[..., 2]).all()


def test_vggt_omega_dense_conf_downsamples_to_patch_confidence():
    conf = torch.ones(1, 2, 8, 8)

    patch_conf = _dense_conf_to_patch_confidence(conf, n_patches=16)

    assert patch_conf.shape == (2, 16, 1)
    assert torch.allclose(patch_conf, torch.ones_like(patch_conf))


def test_vggt_omega_expanded_entry_adds_real_backend():
    base = {
        "seq": "seq0",
        "domain": "kitti",
        "proposals": {
            "fast3r": {"pointmap": torch.zeros(2, 3, 3), "confidence": torch.ones(2, 3, 1)},
        },
        "expert_backends": {"fast3r": True},
        "memory_context": torch.zeros(4),
        "conflict_score": 0.25,
        "composer_prior": torch.zeros(1),
        "gt_pointmap": torch.zeros(2, 3, 3),
        "gt_mask": torch.ones(2, 3),
    }

    entry = _expanded_entry(
        base,
        ["fast3r"],
        vggt_pointmap=torch.ones(1, 2, 3, 3),
        vggt_confidence=torch.ones(1, 2, 3, 1),
    )

    assert entry["expert_order"] == ["fast3r", "vggt_omega"]
    assert entry["expert_backends"]["vggt_omega"] is True
    assert entry["proposals"]["vggt_omega"]["pointmap"].shape == (2, 3, 3)


def test_vggt_omega_admission_summary_counts_oracle_gain():
    rows = [
        {
            "old_oracle": 0.20,
            "new_oracle": 0.15,
            "old_best_expert": "mast3r",
            "new_best_expert": "vggt_omega",
            "metrics": {"vggt_omega": 0.15},
        },
        {
            "old_oracle": 0.10,
            "new_oracle": 0.10,
            "old_best_expert": "fast3r",
            "new_best_expert": "fast3r",
            "metrics": {"vggt_omega": 0.30},
        },
    ]

    summary = _summarize_rows(rows, ["fast3r", "mast3r", "spann3r"])

    assert summary["n"] == 2
    assert summary["vggt_omega_wins"] == 1
    assert summary["oracle_gain_abs_rel"] > 0
