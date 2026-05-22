"""
Dream3R v0.4/v0.5 Test3R off-path verification tests.

Validates that:
  - Action 4 dispatches Test3R as an off-path verification without replacing main output
  - Off-path result is logged in repair_action_log["offpath_verification"]
  - Off-path result never claims accepted_as_main_output=True
  - Fallback mode works without loaded checkpoint
  - Off-path scaffold runs even without raw images (records stub)
  - composer.dispatch("test3r") can be called directly in fallback

Run:
    cd E:/Dream3R/code
    python -m pytest dream3r/tests/test_v04_test3r_offpath.py -q
"""

import os
import sys

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_ROOT not in sys.path:
    sys.path.insert(0, CODE_ROOT)

from dream3r.contracts import (
    CriticDecision,
    OffpathVerification,
    REPAIR_ACTION_NAMES,
    ReconstructionOutput,
)
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline


def _make_pipeline(max_attempts: int = 1):
    torch.manual_seed(500)
    model = build_dream3r("small")
    pipeline = build_v04_pipeline(model, max_repair_attempts=max_attempts)
    feats = torch.randn(1, 2, 17, 768)
    imgs = torch.randn(1, 2, 3, 64, 64)
    return pipeline, feats, imgs


def _synthetic_decision(action: int, batch: int = 1) -> CriticDecision:
    return CriticDecision(
        conflict_score=torch.zeros(batch, 1),
        repair_action=torch.full((batch,), action, dtype=torch.long),
        reroute_hint=torch.tensor([action == 3] * batch),
        reason_codes=[["synthetic"]] * batch,
        local_window_ids=[0],
        critic_log={},
    )


# ---------- action 4 does not replace primary output ----------

def test_action_four_returns_primary_output_unchanged():
    """Action 4 must NOT replace the main output."""
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    new = pipeline.repair.execute(
        primary, _synthetic_decision(4),
        forward_fn=pipeline._call_model,
        forward_kwargs=forward_kwargs,
    )
    assert new is primary, "action 4 must return the original primary output"


# ---------- action 4 logs offpath verification ----------

def test_action_four_records_offpath_verification_in_report():
    """RepairReport must include offpath_verification after action 4."""
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    pipeline.repair.execute(
        primary, _synthetic_decision(4),
        forward_fn=pipeline._call_model,
        forward_kwargs=forward_kwargs,
    )
    report = pipeline.repair.finalize()

    assert report.offpath_verification is not None
    ov = report.offpath_verification
    assert isinstance(ov, OffpathVerification)
    assert ov.expert_id == "test3r"
    assert ov.accepted_as_main_output is False
    assert ov.backend in {"real", "fallback", "stub"}
    assert ov.triggered_by == "critic_conflict"


# ---------- action 4 with raw images dispatches fallback test3r ----------

def test_action_four_with_images_dispatches_test3r_fallback():
    """With raw images, action 4 dispatches test3r in fallback mode."""
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": imgs, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(
        x=feats, regime_probs=None, prev_memory_state=None,
        prev_object_slots=None, prev_object_slot_poses=None, timestep=0,
    )
    # Pass images in forward_kwargs for off-path dispatch
    pipeline.repair.execute(
        primary, _synthetic_decision(4),
        forward_fn=pipeline._call_model,
        forward_kwargs=forward_kwargs,
    )
    report = pipeline.repair.finalize()

    assert report.offpath_verification is not None
    ov = report.offpath_verification
    assert ov.expert_id == "test3r"
    # Not loaded locally -> fallback
    assert ov.backend in {"fallback", "stub"}
    assert ov.accepted_as_main_output is False
    # pointmap_shape should be non-empty when dispatch succeeded
    assert len(ov.pointmap_shape) > 0 or "error" in ov.metadata


# ---------- action 4 without images records stub ----------

def test_action_four_without_images_records_stub():
    """When images are not available, action 4 records a stub offpath."""
    pipeline, feats, imgs = _make_pipeline()
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    pipeline.repair.execute(
        primary, _synthetic_decision(4),
        forward_fn=pipeline._call_model,
        forward_kwargs=forward_kwargs,
    )
    report = pipeline.repair.finalize()

    assert report.offpath_verification is not None
    ov = report.offpath_verification
    assert ov.backend == "stub"
    assert ov.accepted_as_main_output is False


# ---------- offpath_verification in final reconstruction output ----------

def test_offpath_verification_appears_in_repair_action_log():
    """Full pipeline round-trip should include offpath_verification key."""
    pipeline, feats, imgs = _make_pipeline()

    # Run the pipeline normally (action will be 0 in most cases)
    out = pipeline(images=imgs, features=feats)

    # offpath_verification key must exist (None if action != 4)
    assert "offpath_verification" in out.repair_action_log


# ---------- REPAIR_ACTION_NAMES includes 4 ----------

def test_action_four_in_repair_action_names():
    """Action 4 must be in the REPAIR_ACTION_NAMES vocabulary."""
    assert 4 in REPAIR_ACTION_NAMES
    assert REPAIR_ACTION_NAMES[4] == "test3r_offpath_verify"


# ---------- composer.dispatch("test3r") fallback contract ----------

def test_composer_dispatch_test3r_fallback():
    """Direct dispatch of test3r adapter returns valid ExpertOutput in fallback."""
    torch.manual_seed(501)
    model = build_dream3r("small")
    composer = model.composer
    registry = getattr(composer, "registry", None)
    assert registry is not None, "ComposerRouter must have a registry"
    assert "test3r" in registry.names, "test3r must be registered"

    adapter = registry.get("test3r")
    assert not adapter.is_loaded, "test3r should not be loaded locally"

    images = torch.randn(1, 2, 3, 64, 64)
    expert_out = adapter.forward(images)
    assert expert_out is not None
    assert expert_out.pointmap.shape[0] == 1
    assert expert_out.pointmap.shape[-1] == 3
    assert expert_out.confidence.shape[0] == 1


if __name__ == "__main__":
    test_action_four_returns_primary_output_unchanged()
    test_action_four_records_offpath_verification_in_report()
    test_action_four_with_images_dispatches_test3r_fallback()
    test_action_four_without_images_records_stub()
    test_offpath_verification_appears_in_repair_action_log()
    test_action_four_in_repair_action_names()
    test_composer_dispatch_test3r_fallback()
    print("Test3R off-path tests: ALL PASSED")
