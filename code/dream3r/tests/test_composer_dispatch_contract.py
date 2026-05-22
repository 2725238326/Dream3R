"""
Dream3R v0.4 Composer dispatch contract tests.

Asserts that the Composer ACTUALLY dispatches to one of the seven expert
adapters and the resulting ExpertOutput is what lands in
ReconstructionOutput.pointmap (not just a per-frame perception proposal).
Also verifies the reroute-hint path picks a different expert.
"""

import os
import sys

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_ROOT not in sys.path:
    sys.path.insert(0, CODE_ROOT)

from dream3r.contracts import CriticDecision
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline


def _build():
    torch.manual_seed(42)
    model = build_dream3r("small")
    pipeline = build_v04_pipeline(model, max_repair_attempts=1)
    feats = torch.randn(1, 3, 17, 768)
    imgs = torch.randn(1, 3, 3, 64, 64)
    return pipeline, feats, imgs


def test_dispatch_returns_one_of_seven_known_experts():
    pipeline, feats, imgs = _build()
    out = pipeline(images=imgs, features=feats)
    seven = {"mast3r", "fast3r", "spann3r", "cut3r", "moge2",
             "depthanything", "test3r"}
    assert out.expert.expert_name in seven, out.expert.expert_name


def test_expert_output_replaces_perception_pointmap_in_final_output():
    pipeline, feats, imgs = _build()
    out = pipeline(images=imgs, features=feats)
    # Perception proposal P-dim equals 17 (feature_tokens P axis); expert
    # adapters produce a 14*14 = 196 patch pointmap. Final pointmap must
    # match the expert.
    assert out.expert.pointmap.shape[-2] == 196
    assert out.pointmap.shape == out.expert.pointmap.shape
    assert out.evidence.shape == out.expert.evidence_tokens.shape


def test_backend_status_includes_real_or_fallback_or_stub_labels():
    pipeline, feats, imgs = _build()
    out = pipeline(images=imgs, features=feats)
    expert_bs = out.backend_status["expert"]
    assert expert_bs["backend"] in {"real", "fallback", "stub"}
    # Without checkpoints, the adapter is_loaded must be False and the
    # backend must be honestly labeled (no false "real" claim).
    if not expert_bs["is_loaded"]:
        assert expert_bs["backend"] != "real"


def test_reroute_hint_changes_selected_expert():
    pipeline, feats, imgs = _build()
    # Force the critic decision to action=3 so the orchestrator applies
    # the reroute.
    pipeline.repair.begin_call()
    forward_kwargs = {
        "x": feats, "regime_probs": None, "prev_memory_state": None,
        "prev_object_slots": None, "prev_object_slot_poses": None,
        "timestep": 0,
    }
    primary = pipeline._call_model(**forward_kwargs)
    base_composer = pipeline._build_composer(primary, reroute_hint=False)
    primary_expert = int(base_composer.selected_expert[0].item())

    # Build the rerouted composer decision the way the live pipeline would.
    decision = CriticDecision(
        conflict_score=primary["conflict_score"],
        repair_action=torch.tensor([3]),
        reroute_hint=torch.tensor([True]),
        reason_codes=[["forced_action_3"]],
        local_window_ids=[0],
        critic_log={},
    )
    pipeline.repair.execute(primary, decision,
                            forward_fn=pipeline._call_model,
                            forward_kwargs=forward_kwargs)
    rerouted = pipeline._build_composer(primary,
                                        reroute_hint=pipeline.repair._reroute_hint)
    rerouted_expert = int(rerouted.selected_expert[0].item())

    assert rerouted.reroute_applied is True
    if base_composer.route_recommendation.shape[1] >= 2:
        # When at least two experts are ranked, reroute MUST pick the
        # second-best, which (unless there is a tie) differs from primary.
        assert rerouted_expert != primary_expert, (
            primary_expert, rerouted_expert,
            base_composer.route_recommendation.tolist(),
        )


def test_dispatch_handles_no_image_input_gracefully():
    pipeline, feats, imgs = _build()
    out = pipeline(features=feats)
    # Without raw images we cannot run a real adapter forward; the
    # orchestrator returns a stub-labeled ExpertOutput backed by perception.
    assert out.expert.backend_status["backend"] == "stub"
    assert "note" in out.expert.backend_status


def test_route_log_records_reroute_state():
    pipeline, feats, imgs = _build()
    out = pipeline(images=imgs, features=feats)
    route = out.route_log
    for key in ["selected_expert_id", "route_recommendation",
                "route_regret", "reroute_applied", "reroute_hint",
                "backend_status", "expert_backend_status"]:
        assert key in route


def test_seven_expert_registry_is_attached():
    pipeline, feats, imgs = _build()
    composer_bs = pipeline._build_composer(
        pipeline._call_model(
            x=feats, regime_probs=None, prev_memory_state=None,
            prev_object_slots=None, prev_object_slot_poses=None, timestep=0,
        ),
        reroute_hint=False,
    ).backend_status
    assert composer_bs["registry_attached"] is True
    assert len(composer_bs["adapter_status"]) == 7


if __name__ == "__main__":
    test_dispatch_returns_one_of_seven_known_experts()
    test_expert_output_replaces_perception_pointmap_in_final_output()
    test_backend_status_includes_real_or_fallback_or_stub_labels()
    test_reroute_hint_changes_selected_expert()
    test_dispatch_handles_no_image_input_gracefully()
    test_route_log_records_reroute_state()
    test_seven_expert_registry_is_attached()
    print("Composer dispatch contract tests: PASS")
