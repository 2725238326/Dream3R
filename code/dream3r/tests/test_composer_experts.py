"""Unit tests for composer expert adapters."""

import torch
from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.base_adapter import ExpertAdapter


def test_registry_registration():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    assert len(reg.names) == 7
    expected = {"mast3r", "fast3r", "spann3r", "cut3r", "moge2", "depthanything", "test3r"}
    assert set(reg.names) == expected


def test_capability_matrix():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    matrix = reg.capability_matrix()
    assert matrix.shape == (7, 5)
    assert (matrix >= 0).all() and (matrix <= 1).all()


def test_method_profiles_extract_3r_advantages():
    reg = ExpertRegistry()
    reg.register_all_defaults()

    profiles = reg.method_profiles()
    assert set(profiles) == set(reg.names)
    assert "dense 3D-grounded local matching" in profiles["mast3r"].advantages
    assert "persistent state for continuous perception" in profiles["cut3r"].advantages
    assert "external spatial memory for image collections" in profiles["spann3r"].advantages

    feature_matrix = reg.feature_matrix()
    assert feature_matrix.shape[0] == 7
    assert feature_matrix.shape[1] >= 8
    assert feature_matrix.max() <= 1
    assert feature_matrix.min() >= 0

    summary = reg.advantage_summary()
    assert "fast3r" in summary
    assert len(summary["fast3r"]) >= 2


def test_adapter_status_reports_backend_availability():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    status = reg.adapter_status()

    assert set(status) == set(reg.names)
    assert "is_loaded" in status["mast3r"]
    assert "is_available" in status["mast3r"]
    assert "has_checkpoint_artifacts" in status["mast3r"]
    assert "load_error" in status["mast3r"]
    assert status["mast3r"]["backend"] in {"real", "fallback"}


def test_latency_vector():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    latency = reg.latency_vector()
    assert latency.shape == (7,)
    assert (latency > 0).all()

    fastest = reg.get("depthanything")
    assert fastest.latency_estimate_ms < 20

    slowest = reg.get("test3r")
    assert slowest.latency_estimate_ms > 100


def test_adapter_forward():
    reg = ExpertRegistry()
    reg.register_all_defaults()

    for name in reg.names:
        adapter = reg.get(name)
        images = torch.randn(2, 4, 3, 224, 224)
        out = adapter.forward(images)
        assert out.pointmap.shape == (2, 4, 196, 3), f"{name} pointmap shape wrong"
        assert out.confidence.shape == (2, 4, 196, 1), f"{name} confidence shape wrong"
        assert out.evidence_tokens.shape == (2, 4, 17, 32), f"{name} evidence shape wrong"
        assert "expert" in out.metadata


def test_mast3r_fallback_is_deterministic_and_marked():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    adapter = reg.get("mast3r")
    images = torch.randn(1, 2, 3, 224, 224)

    out1 = adapter.forward(images)
    out2 = adapter.forward(images)

    assert torch.allclose(out1.pointmap, out2.pointmap)
    assert torch.allclose(out1.confidence, out2.confidence)
    assert out1.metadata["backend"] in {"deterministic_fallback", "mast3r"}
    if not adapter.is_loaded:
        assert out1.metadata["is_loaded"] is False


def test_all_fallback_adapters_are_deterministic():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    images = torch.randn(1, 3, 3, 224, 224)

    for name in reg.names:
        adapter = reg.get(name)
        if adapter.is_loaded:
            continue
        out1 = adapter.forward(images)
        out2 = adapter.forward(images)
        assert torch.allclose(out1.pointmap, out2.pointmap), name
        assert torch.allclose(out1.confidence, out2.confidence), name
        assert torch.allclose(out1.evidence_tokens, out2.evidence_tokens), name
        assert out1.metadata["backend"] == "deterministic_fallback"


def test_capability_tensor():
    reg = ExpertRegistry()
    reg.register_all_defaults()

    adapter = reg.get("mast3r")
    ct = adapter.capability_tensor()
    assert ct.shape == (5,)
    assert ct.sum() > 0


def test_cut3r_state_tokens():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    adapter = reg.get("cut3r")
    out = adapter.forward(torch.randn(1, 2, 3, 224, 224))
    assert "state_tokens" in out.metadata
    assert out.metadata["state_tokens"].shape[1] == 32


if __name__ == "__main__":
    test_registry_registration()
    test_capability_matrix()
    test_method_profiles_extract_3r_advantages()
    test_adapter_status_reports_backend_availability()
    test_latency_vector()
    test_adapter_forward()
    test_mast3r_fallback_is_deterministic_and_marked()
    test_all_fallback_adapters_are_deterministic()
    test_capability_tensor()
    test_cut3r_state_tokens()
    print("All composer expert tests passed.")
