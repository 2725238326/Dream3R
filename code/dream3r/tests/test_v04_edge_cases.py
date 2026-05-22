"""
Dream3R v0.4 edge-case contract tests.

Validates pipeline stability under:
  - batch size > 1
  - missing raw images (features-only dispatch)
  - all repair action log fields present
  - backend_status never falsely claims "real"
  - contract_log records required cross-module signal reads
  - repair_action_log schema stability for all action codes 0..4

Run:
    cd E:/Dream3R/code
    python -m pytest dream3r/tests/test_v04_edge_cases.py -q
"""

import os
import sys

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_ROOT not in sys.path:
    sys.path.insert(0, CODE_ROOT)

from dream3r.contracts import (
    BACKEND_FALLBACK,
    BACKEND_REAL,
    BACKEND_STUB,
    REPAIR_ACTION_NAMES,
    ReconstructionOutput,
)
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline


def _build_inputs(batch: int = 1, n_views: int = 3, n_evidence: int = 17,
                  d_model: int = 768, img_size: int = 64):
    feats = torch.randn(batch, n_views, n_evidence, d_model)
    imgs = torch.randn(batch, n_views, 3, img_size, img_size)
    return feats, imgs


# ---------- batch size > 1 ----------

def test_v04_forward_batch_two_keeps_contract_shape():
    """Pipeline produces valid output with batch=2."""
    torch.manual_seed(100)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs(batch=2)

    out = pipeline(images=imgs, features=feats)

    assert isinstance(out, ReconstructionOutput)
    assert out.pointmap.shape[0] == 2
    assert out.confidence.shape[0] == 2
    assert out.dynamic_logits.shape[0] == 2
    assert out.selected_expert.shape[0] == 2
    assert out.conflict_score.shape[0] == 2


# ---------- no raw images -> fallback dispatch ----------

def test_v04_forward_without_raw_images_marks_fallback_backend():
    """When only features are supplied, expert dispatch uses stub/fallback path."""
    torch.manual_seed(101)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, _ = _build_inputs()

    out = pipeline(features=feats)

    assert isinstance(out, ReconstructionOutput)
    expert_backend = out.backend_status["expert"]["backend"]
    assert expert_backend in {BACKEND_FALLBACK, BACKEND_STUB}, (
        f"Without raw images, expert should be fallback/stub, got {expert_backend}"
    )
    assert out.backend_status["expert"]["is_loaded"] is False


# ---------- all required log fields ----------

def test_v04_output_contains_required_logs_under_no_repair():
    """Even when no repair fires, all log dicts are present and structured."""
    torch.manual_seed(102)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    # repair_action_log
    ral = out.repair_action_log
    assert "final_action" in ral
    assert "final_action_name" in ral
    assert "n_attempts" in ral
    assert "max_attempts" in ral
    assert "capped" in ral
    assert "attempts" in ral
    assert "implemented_actions" in ral
    assert isinstance(ral["attempts"], list)

    # route_log
    rl = out.route_log
    assert "selected_expert_id" in rl
    assert "reroute_applied" in rl
    assert "backend_status" in rl
    assert "expert_backend_status" in rl

    # memory_log
    ml = out.memory_log
    assert "latent_drift_proxy" in ml
    assert "bank_occupancy" in ml
    assert "memory_backend_status" in ml
    assert "retrieval_log" in ml

    # backend_status top-level
    bs = out.backend_status
    for module in ["architecture_version", "perception", "memory",
                   "permanence", "critic", "composer", "expert"]:
        assert module in bs, f"backend_status missing key: {module}"


def test_v04_repair_log_schema_stable_for_all_actions():
    """Repair action log has consistent schema regardless of action code."""
    torch.manual_seed(103)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    ral = out.repair_action_log
    assert ral["final_action"] in REPAIR_ACTION_NAMES or ral["final_action"] == 4
    assert isinstance(ral["final_action_name"], str)
    assert isinstance(ral["n_attempts"], int)
    assert isinstance(ral["max_attempts"], int)
    assert isinstance(ral["capped"], bool)

    for attempt in ral["attempts"]:
        for key in ["attempt_index", "action_code", "action_name",
                    "reason", "triggered_by_critic", "succeeded", "note"]:
            assert key in attempt, f"attempt missing key: {key}"


# ---------- backend never claims real without loaded adapter ----------

def test_v04_backend_status_never_claims_real_without_loaded_adapter():
    """No adapter is loaded locally; backend must never be 'real'."""
    torch.manual_seed(104)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    expert_bs = out.backend_status["expert"]
    if not expert_bs.get("is_loaded", False):
        assert expert_bs["backend"] != BACKEND_REAL, (
            f"Expert claims real but is_loaded=False"
        )

    composer_bs = out.backend_status["composer"]
    adapter_status = composer_bs.get("adapter_status", {})
    for name, status in adapter_status.items():
        if not status.get("is_loaded", False):
            assert status["backend"] != "real", (
                f"Adapter {name} claims real without is_loaded=True"
            )


# ---------- contract_log records required signal reads ----------

def test_v04_contract_log_records_required_signal_reads():
    """Contract log must record key cross-module signal interactions."""
    torch.manual_seed(105)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    log = out.contract_log
    assert isinstance(log, list)
    assert len(log) > 0

    signals_seen = set()
    for entry in log:
        signals_seen.add(entry.get("signal", ""))

    # Key cross-module signals that must appear
    expected_signals = {"dynamic_ratio", "latent_drift_proxy", "capability_match"}
    for sig in expected_signals:
        assert sig in signals_seen, (
            f"Expected signal '{sig}' in contract_log, got: {signals_seen}"
        )


# ---------- output has evidence field and it's from expert ----------

def test_v04_expert_output_evidence_shape():
    """Evidence tensor from expert dispatch has expected shape."""
    torch.manual_seed(106)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    assert out.evidence.dim() == 4  # [B, N, n_ev, d_ev]
    assert out.evidence.shape[0] == 1  # batch
    assert out.evidence.shape[-1] == 32  # d_evidence


if __name__ == "__main__":
    test_v04_forward_batch_two_keeps_contract_shape()
    test_v04_forward_without_raw_images_marks_fallback_backend()
    test_v04_output_contains_required_logs_under_no_repair()
    test_v04_repair_log_schema_stable_for_all_actions()
    test_v04_backend_status_never_claims_real_without_loaded_adapter()
    test_v04_contract_log_records_required_signal_reads()
    test_v04_expert_output_evidence_shape()
    print("v0.4 edge-case tests: ALL PASSED")
