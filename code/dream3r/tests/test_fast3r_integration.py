"""Optional server-side Fast3R adapter integration test.

Set DREAM3R_RUN_FAST3R_INTEGRATION=1 to load the real checkpoint.
"""

import os

import torch

from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.modules import ComposerRouter


def test_fast3r_adapter_contract_and_optional_real_load():
    adapter = Fast3RAdapter()
    images = torch.randn(1, 2, 3, 224, 224)

    if os.environ.get("DREAM3R_RUN_FAST3R_INTEGRATION") == "1":
        if not adapter.is_available():
            assert adapter.has_checkpoint_artifacts()
            try:
                adapter.load_checkpoint()
            except ImportError as exc:
                assert "missing dependency" in str(exc)
                return
        adapter.load_checkpoint()
        assert adapter.is_loaded
    else:
        assert not adapter.is_loaded

    out = adapter.forward(images)
    assert out.pointmap.shape == (1, 2, 196, 3)
    assert out.confidence.shape == (1, 2, 196, 1)
    assert out.evidence_tokens.shape == (1, 2, 17, 32)
    assert out.metadata["expert"] == "fast3r"
    assert out.metadata["backend"] in {"deterministic_fallback", "fast3r"}
    if adapter.is_loaded:
        assert out.metadata["backend"] == "fast3r"
        assert out.metadata["latency_ms"] > 0


def test_composer_dispatch_uses_loaded_fast3r_when_enabled():
    if os.environ.get("DREAM3R_RUN_FAST3R_INTEGRATION") != "1":
        return

    reg = ExpertRegistry()
    reg.register_all_defaults()
    fast3r = reg.get("fast3r")
    if not fast3r.is_available():
        assert fast3r.has_checkpoint_artifacts()
        return
    fast3r.load_checkpoint()

    router = ComposerRouter(n_regimes=6, d_routing=32, cost_alpha=0.0, expert_registry=reg)
    router.load_from_registry()
    fast3r_id = sorted(reg.names).index("fast3r")
    out = router.dispatch(fast3r_id, torch.randn(1, 2, 3, 224, 224))

    assert out is not None
    assert out.metadata["backend"] == "fast3r"
    assert out.metadata["adapter_is_loaded"] is True
    assert out.metadata["selected_expert_name"] == "fast3r"
    assert out.metadata["dispatch_latency_ms"] > 0


if __name__ == "__main__":
    test_fast3r_adapter_contract_and_optional_real_load()
    test_composer_dispatch_uses_loaded_fast3r_when_enabled()
    print("Fast3R adapter integration contract test passed.")
