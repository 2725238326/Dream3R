"""Server-only real Fast3R checkpoint test for Stage 3."""

import os

import pytest
import torch

from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter


pytestmark = pytest.mark.gpu


def test_fast3r_real_checkpoint_forward_nonzero():
    if os.environ.get("DREAM3R_RUN_FAST3R_REAL") != "1":
        pytest.skip("set DREAM3R_RUN_FAST3R_REAL=1 on the server to run Fast3R")
    if not torch.cuda.is_available():
        pytest.skip("Fast3R real test requires CUDA")

    adapter = Fast3RAdapter()
    adapter.load_checkpoint()
    images = torch.rand(1, 2, 3, 224, 224, device="cuda")
    out = adapter.forward(images)

    assert adapter.is_loaded
    assert out.metadata["backend"] == "fast3r"
    assert out.pointmap.shape == (1, 2, 196, 3)
    assert out.confidence.shape == (1, 2, 196, 1)
    assert out.evidence_tokens.shape == (1, 2, 17, 32)
    assert torch.count_nonzero(out.pointmap).item() > 0
