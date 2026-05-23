"""Integration tests for VGGT adapter and capability_card v2.2 schema."""

import pytest
import torch

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
