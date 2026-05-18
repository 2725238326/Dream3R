"""Optional server-side MASt3R adapter integration test.

Set DREAM3R_RUN_MAST3R_INTEGRATION=1 to load the real checkpoint.
Without the flag this verifies checkpoint discoverability and fallback shape
contract without paying the large model-load cost in the normal test suite.
"""

import os

import torch

from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.modules import ComposerRouter


def test_mast3r_adapter_contract_and_optional_real_load():
    adapter = MASt3RAdapter()
    images = torch.randn(1, 2, 3, 224, 224)

    if os.environ.get("DREAM3R_RUN_MAST3R_INTEGRATION") == "1":
        adapter.load_checkpoint()
        assert adapter.is_loaded
    else:
        assert not adapter.is_loaded

    out = adapter.forward(images)
    assert out.pointmap.shape == (1, 2, 196, 3)
    assert out.confidence.shape == (1, 2, 196, 1)
    assert out.evidence_tokens.shape == (1, 2, 17, 32)
    assert out.metadata["expert"] == "mast3r"
    assert out.metadata["backend"] in {"deterministic_fallback", "mast3r"}
    if adapter.is_loaded:
        assert out.metadata["backend"] == "mast3r"
        assert out.metadata["latency_ms"] > 0


def test_composer_dispatch_uses_loaded_mast3r_when_enabled():
    if os.environ.get("DREAM3R_RUN_MAST3R_INTEGRATION") != "1":
        return

    reg = ExpertRegistry()
    reg.register_all_defaults()
    mast3r = reg.get("mast3r")
    mast3r.load_checkpoint()

    router = ComposerRouter(n_regimes=5, d_routing=32, cost_alpha=0.0, expert_registry=reg)
    router.load_from_registry()
    mast3r_id = sorted(reg.names).index("mast3r")
    out = router.dispatch(mast3r_id, torch.randn(1, 2, 3, 224, 224))

    assert out is not None
    assert out.metadata["backend"] == "mast3r"
    assert out.metadata["adapter_is_loaded"] is True
    assert out.metadata["selected_expert_name"] == "mast3r"
    assert out.metadata["dispatch_latency_ms"] > 0


if __name__ == "__main__":
    test_mast3r_adapter_contract_and_optional_real_load()
    test_composer_dispatch_uses_loaded_mast3r_when_enabled()
    print("MASt3R adapter integration contract test passed.")
