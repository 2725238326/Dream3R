"""
Dream3R v0.4 architecture contract tests.

These tests assert that the V04Pipeline returns a structurally complete
ReconstructionOutput on a small fake image sequence, with all required
fields present and typed correctly. They do NOT require GPU, network, or
any real expert checkpoint.

Run with either pytest or directly:
    python tests/test_v04_architecture_contract.py
"""

import os
import sys

import torch

# Make ``dream3r`` importable when running this file directly from the
# tests/ folder.
HERE = os.path.dirname(os.path.abspath(__file__))
CODE_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_ROOT not in sys.path:
    sys.path.insert(0, CODE_ROOT)

from dream3r.contracts import (
    ARCHITECTURE_VERSION,
    REPAIR_ACTION_NAMES,
    ComposerDecision,
    CriticDecision,
    DispatchedExpertOutput,
    MemoryOutput,
    PerceptionOutput,
    PermanenceOutput,
    ReconstructionOutput,
)
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline


def _build_inputs(batch: int = 1, n_views: int = 3, n_evidence: int = 17,
                  d_model: int = 768, img_size: int = 64):
    feats = torch.randn(batch, n_views, n_evidence, d_model)
    imgs = torch.randn(batch, n_views, 3, img_size, img_size)
    return feats, imgs


def test_v04_pipeline_returns_typed_reconstruction_output():
    torch.manual_seed(0)
    model = build_dream3r("small")
    pipeline = build_v04_pipeline(model, max_repair_attempts=1)
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats, timestep=0)

    assert isinstance(out, ReconstructionOutput), type(out)
    assert out.architecture_version == ARCHITECTURE_VERSION


def test_v04_output_has_all_required_top_level_fields():
    torch.manual_seed(1)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()

    out = pipeline(images=imgs, features=feats)

    required = [
        "pointmap", "confidence", "dynamic_logits", "dynamic_mask_proxy",
        "dynamic_mask_final", "evidence", "selected_expert", "backend_status", "conflict_score",
        "memory_log", "route_log", "repair_action_log", "contract_log",
        "architecture_version",
    ]
    for name in required:
        assert hasattr(out, name), f"missing top-level field {name}"
        if name != "dynamic_mask_final":
            assert getattr(out, name) is not None, f"field {name} is None"


def test_v04_typed_submodule_contracts_present():
    torch.manual_seed(2)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    assert isinstance(out.perception, PerceptionOutput)
    assert isinstance(out.memory, MemoryOutput)
    assert isinstance(out.permanence, PermanenceOutput)
    assert isinstance(out.critic, CriticDecision)
    assert isinstance(out.composer, ComposerDecision)
    assert isinstance(out.expert, DispatchedExpertOutput)
    assert out.repair is not None


def test_perception_output_fields_and_backbone_status():
    torch.manual_seed(3)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    perc = out.perception
    assert perc.feature_tokens.dim() == 4
    assert perc.pointmap_proposal.shape[-1] == 3
    assert perc.confidence.shape[-1] == 1
    # 17 named evidence signals per Perceiver.EVIDENCE_SIGNALS
    assert len(perc.evidence_signals) == 17
    assert "pose_novelty" in perc.evidence_signals
    bs = perc.backbone_status
    for k in ["backbone_type", "is_loaded", "use_backbone", "backend"]:
        assert k in bs
    assert bs["backend"] in {"real", "fallback", "stub"}


def test_memory_output_includes_drift_occupancy_and_backend_status():
    torch.manual_seed(4)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    mem = out.memory
    assert mem.fused_context.shape[0] == feats.shape[0]
    assert mem.latent_drift_proxy.shape[-1] == 1
    assert torch.is_tensor(mem.bank_occupancy)
    # AnchorBank K=256 (small preset default).
    assert mem.memory_backend_status["bank_capacity"] == 256
    assert mem.memory_backend_status["state_recurrence_type"] in {
        "cross_attention", "mamba_hybrid"
    }
    assert mem.memory_backend_status["backend"] in {"real", "stub"}


def test_permanence_output_has_dynamic_mask_proxy_and_suppress_handoff():
    torch.manual_seed(5)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    perm = out.permanence
    assert perm.dynamic_logits.shape[-1] == 3
    assert perm.dynamic_mask_proxy.dtype == torch.bool
    assert perm.dynamic_mask_final is None or perm.dynamic_mask_final.dtype == torch.bool
    assert perm.dynamic_ratio.shape[-1] == 1
    assert perm.suppress_static_write.shape[0] == feats.shape[0]
    assert perm.object_track_set.dim() == 3
    assert perm.stable_promotion_log["cr2_suppress_source"] == "dynamic_mask_proxy"


def test_critic_decision_uses_v04_action_codes():
    torch.manual_seed(6)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    critic = out.critic
    assert critic.conflict_score.shape[0] == feats.shape[0]
    for code in critic.repair_action.tolist():
        assert code in REPAIR_ACTION_NAMES, code
    assert critic.reroute_hint.dtype == torch.bool


def test_composer_decision_carries_selected_expert_and_route_log():
    torch.manual_seed(7)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    comp = out.composer
    assert comp.selected_expert.shape[0] == feats.shape[0]
    assert comp.route_recommendation.dim() == 2
    assert comp.backend_status["n_experts"] >= 1
    assert "adapter_status" in comp.backend_status


def test_final_pointmap_is_from_expert_dispatch_and_backend_is_labeled():
    torch.manual_seed(8)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)

    # Expert adapters produce a 14x14 = 196 patch pointmap in fallback mode;
    # this differs from the perception's pointmap_proposal which has
    # P = n_evidence patches. Asserting on the final pointmap therefore
    # confirms the expert dispatch result is what landed in ReconstructionOutput.
    assert out.pointmap.shape[-1] == 3
    assert out.pointmap.shape[-2] == 196  # adapter patch grid 14*14
    assert out.evidence.shape[-2:] == (17, 32)

    expert_status = out.backend_status["expert"]
    assert expert_status["backend"] in {"real", "fallback", "stub"}
    # Locally we never have real backends, so the assertion holds; on the
    # server with real checkpoints the value will switch to "real".


def test_contract_log_records_cross_module_reads():
    torch.manual_seed(9)
    pipeline = build_v04_pipeline(build_dream3r("small"))
    feats, imgs = _build_inputs()
    out = pipeline(images=imgs, features=feats)
    assert isinstance(out.contract_log, list)
    assert len(out.contract_log) > 0
    sample = out.contract_log[0]
    for key in ["signal", "producer", "consumer", "t"]:
        assert key in sample


def test_pipeline_state_carry_over_for_next_window():
    torch.manual_seed(10)
    model = build_dream3r("small")
    pipeline = build_v04_pipeline(model)
    feats, imgs = _build_inputs()

    out1 = pipeline(images=imgs, features=feats, timestep=0)
    out2 = pipeline(
        images=imgs, features=feats,
        prev_memory_state=out1.next_memory_state,
        prev_object_slots=out1.next_object_slots,
        prev_object_slot_poses=out1.next_object_slot_poses,
        timestep=1,
    )
    # Second tick must still produce a valid reconstruction and update the
    # contract log.
    assert isinstance(out2, ReconstructionOutput)
    assert len(out2.contract_log) > 0


if __name__ == "__main__":
    test_v04_pipeline_returns_typed_reconstruction_output()
    test_v04_output_has_all_required_top_level_fields()
    test_v04_typed_submodule_contracts_present()
    test_perception_output_fields_and_backbone_status()
    test_memory_output_includes_drift_occupancy_and_backend_status()
    test_permanence_output_has_dynamic_mask_proxy_and_suppress_handoff()
    test_critic_decision_uses_v04_action_codes()
    test_composer_decision_carries_selected_expert_and_route_log()
    test_final_pointmap_is_from_expert_dispatch_and_backend_is_labeled()
    test_contract_log_records_cross_module_reads()
    test_pipeline_state_carry_over_for_next_window()
    print("v0.4 architecture contract tests: PASS")
