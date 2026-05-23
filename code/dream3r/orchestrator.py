"""
Dream3R v0.4 orchestrator (pipeline).

Wraps an existing v0.3 Dream3R model and closes the architecture loops that
v0.3 only described as bus signals:

    Critic -> RepairExecutor -> rerun model.forward
    Critic -> Composer reroute hint -> dispatch alternate expert
    Composer -> dispatch real expert backend -> ExpertOutput -> final pointmap
    Permanence -> CR-2 -> Memory write gating (already in v0.3; preserved)
    Memory -> latent_drift_proxy + bank_occupancy -> Critic input (preserved)

It does not modify model.py. The v0.3 forward path stays runnable on its
own; the v0.4 pipeline is opt-in.

Test-friendly contract: the orchestrator works without any GPU and without
any expert checkpoint. When no real backend is available, the Composer's
fallback adapters generate deterministic outputs and backend_status is
tagged "fallback" (or "stub" for adapters whose forward delegates to the
shared image_fallback_output helper without any real backbone).
"""

from typing import Any, Dict, List, Optional

import torch
import torch.nn as nn

from dream3r.bus import EvidenceLabel
from dream3r.contracts import (
    ARCHITECTURE_VERSION,
    BACKEND_FALLBACK,
    BACKEND_REAL,
    BACKEND_STUB,
    REPAIR_ACTION_NAMES,
    ComposerDecision,
    CriticDecision,
    DispatchedExpertOutput,
    MemoryOutput,
    PerceptionOutput,
    PermanenceOutput,
    ReconstructionOutput,
)
from dream3r.composer_experts.base_adapter import ExpertOutput
from dream3r.repair import RepairExecutor


class V04Pipeline(nn.Module):
    """v0.4 closed-loop pipeline around a v0.3 Dream3R model.

    Args:
        model:                Dream3R instance (any preset; v01 or v03).
        max_repair_attempts:  forwarded to RepairExecutor.
    """

    def __init__(self, model: nn.Module, max_repair_attempts: int = 1):
        super().__init__()
        self.model = model
        self.repair = RepairExecutor(model, max_repair_attempts=max_repair_attempts)
        self.architecture_version = ARCHITECTURE_VERSION

    # ------------------------------------------------------------------
    # Top-level forward
    # ------------------------------------------------------------------

    def forward(self,
                images: Optional[torch.Tensor] = None,
                features: Optional[torch.Tensor] = None,
                regime_probs: Optional[torch.Tensor] = None,
                prev_memory_state: Optional[torch.Tensor] = None,
                prev_object_slots: Optional[torch.Tensor] = None,
                prev_object_slot_poses: Optional[torch.Tensor] = None,
                timestep: int = 0,
                ) -> ReconstructionOutput:
        """One v0.4 closed-loop tick.

        Either ``images`` (raw [B,N,3,H,W]) or ``features`` (pre-extracted
        [B,N,P,D]) must be provided. Both can be passed together: features
        are used by the inner model.forward (skipping the backbone), while
        images are kept for expert adapter dispatch.
        """
        if images is None and features is None:
            raise ValueError("V04Pipeline.forward requires either images or features")

        # Decide what tensor to feed the underlying model.
        model_input = features if features is not None else images

        forward_kwargs: Dict[str, Any] = {
            "x": model_input,
            "regime_probs": regime_probs,
            "prev_memory_state": prev_memory_state,
            "prev_object_slots": prev_object_slots,
            "prev_object_slot_poses": prev_object_slot_poses,
            "timestep": timestep,
        }

        self.repair.begin_call()

        # 1) Primary forward.
        primary = self._call_model(**forward_kwargs)

        # 2) Build a typed Critic decision from the primary forward so the
        #    repair executor sees a stable contract instead of a raw dict.
        critic_decision = self._build_critic_decision(primary, timestep)

        # 3) Repair: may rerun model.forward; returns either primary or a
        #    new forward dict. action=3 (reroute) does not rerun model.
        raw = self.repair.execute(primary, critic_decision,
                                  forward_fn=self._call_model,
                                  forward_kwargs=forward_kwargs)

        # If the rerun produced a new forward dict, refresh critic decision
        # so downstream contracts reflect the corrected pipeline state.
        if raw is not primary:
            critic_decision = self._build_critic_decision(raw, timestep)

        # 4) Build the rest of the typed contracts.
        perception = self._build_perception(raw)
        memory = self._build_memory(raw)
        permanence = self._build_permanence(raw)
        composer = self._build_composer(raw, reroute_hint=self.repair._reroute_hint)

        # 5) Expert dispatch — real, fallback, or stub. Falls back to
        #    perception's pointmap if dispatch yields nothing.
        expert = self._dispatch_expert(composer, images, features, raw)

        # 6) Assemble the final ReconstructionOutput.
        return self._assemble_output(
            raw=raw,
            perception=perception,
            memory=memory,
            permanence=permanence,
            critic=critic_decision,
            composer=composer,
            expert=expert,
        )

    # ------------------------------------------------------------------
    # Internal: model.forward bound to fixed kwargs
    # ------------------------------------------------------------------

    def _call_model(self, **kwargs) -> Dict[str, torch.Tensor]:
        return self.model(
            kwargs["x"],
            regime_probs=kwargs.get("regime_probs"),
            prev_memory_state=kwargs.get("prev_memory_state"),
            prev_object_slots=kwargs.get("prev_object_slots"),
            prev_object_slot_poses=kwargs.get("prev_object_slot_poses"),
            timestep=kwargs.get("timestep", 0),
        )

    # ------------------------------------------------------------------
    # Contract builders
    # ------------------------------------------------------------------

    def _build_perception(self, raw: Dict[str, torch.Tensor]) -> PerceptionOutput:
        perceiver = getattr(self.model, "perceiver", None)
        backbone_status: Dict[str, Any] = {}
        if perceiver is not None:
            backbone = getattr(perceiver, "backbone", None)
            backbone_type = getattr(perceiver, "backbone_type", "unknown")
            load_error = getattr(perceiver, "backbone_load_error", None)
            is_loaded = backbone is not None
            if is_loaded:
                backend = BACKEND_REAL
            elif getattr(perceiver, "use_backbone", False):
                backend = BACKEND_FALLBACK
            else:
                backend = BACKEND_STUB
            backbone_status = {
                "backbone_type": backbone_type,
                "is_loaded": is_loaded,
                "use_backbone": bool(getattr(perceiver, "use_backbone", False)),
                "backbone_load_error": load_error,
                "backend": backend,
            }

        return PerceptionOutput(
            feature_tokens=raw["frame_tokens"],
            pointmap_proposal=raw["pointmap"],
            confidence=raw["confidence"],
            evidence_signals=dict(raw.get("evidence_named", {})),
            backbone_status=backbone_status,
        )

    def _build_memory(self, raw: Dict[str, torch.Tensor]) -> MemoryOutput:
        retrieval_log = dict(raw.get("memory_retrieval_log", {}))
        memory_module = getattr(self.model, "memory", None)
        anchor_bank = getattr(memory_module, "anchor_bank", None)
        bank_capacity = getattr(anchor_bank, "capacity", None)
        memory_backend_status = {
            "state_recurrence_type": getattr(memory_module, "state_recurrence_type", "unknown"),
            "memory_use_nsa": bool(getattr(memory_module, "memory_use_nsa", False)),
            "enable_stable_memory": bool(getattr(memory_module, "enable_stable_memory", False)),
            "bank_capacity": bank_capacity,
            "backend": BACKEND_REAL if memory_module is not None else BACKEND_STUB,
        }

        selected_anchor_stats: Dict[str, Any] = {}
        if "nsa_branch_weights" in raw:
            selected_anchor_stats["branch_weights_mean"] = raw["nsa_branch_weights"].detach().mean(dim=(0, 1))
        if "selected_anchor_3d_distance" in retrieval_log:
            selected_anchor_stats["selected_anchor_3d_distance"] = retrieval_log["selected_anchor_3d_distance"]
        if "selected_3d_distances" in retrieval_log and retrieval_log["selected_3d_distances"] is not None:
            selected_anchor_stats["selected_3d_distances_mean"] = (
                retrieval_log["selected_3d_distances"].float().mean()
            )
        if "effective_top_k" in retrieval_log:
            selected_anchor_stats["effective_top_k"] = retrieval_log["effective_top_k"]

        bank_occupancy = raw.get("bank_occupancy")
        if bank_occupancy is None:
            bank_occupancy = torch.zeros(raw["pointmap"].shape[0])

        return MemoryOutput(
            fused_context=raw["latent_state"],
            latent_drift_proxy=raw["latent_drift_proxy"],
            bank_occupancy=bank_occupancy,
            selected_anchor_stats=selected_anchor_stats,
            retrieval_log=retrieval_log,
            memory_backend_status=memory_backend_status,
        )

    def _build_permanence(self, raw: Dict[str, torch.Tensor]) -> PermanenceOutput:
        region_logits = raw["region_logits"]
        dynamic_mask_proxy = raw.get("dynamic_mask_proxy")
        if dynamic_mask_proxy is None:
            dynamic_mask_proxy = (region_logits.argmax(dim=-1) != 0)
        dynamic_mask_final = raw.get("dynamic_mask_final")
        stable_promotion_log = {
            "mint_confidence": raw.get("mint_confidence"),
            "slot_match_indices": raw.get("slot_match_indices"),
            "slot_match_scores": raw.get("slot_match_scores"),
            "cr2_suppress_source": raw.get("cr2_suppress_source"),
        }
        return PermanenceOutput(
            dynamic_logits=region_logits,
            dynamic_mask_proxy=dynamic_mask_proxy,
            dynamic_mask_final=dynamic_mask_final,
            dynamic_ratio=raw["dynamic_ratio"],
            suppress_static_write=raw["suppress_static_write"],
            object_track_set=raw["object_track_set"],
            stable_promotion_log=stable_promotion_log,
        )

    def _build_critic_decision(self, raw: Dict[str, torch.Tensor],
                               timestep: int) -> CriticDecision:
        recommended = raw["recommended_action"].long()
        conflict = raw["conflict_score"]

        # Map the v0.3 Critic's 6-way head onto the v0.4/v0.5 contract:
        # 0=no, 1=local, 2=reroute, 4=Test3R off-path.
        v04_action = torch.zeros_like(recommended)
        v04_action = torch.where(recommended == 1, torch.ones_like(recommended), v04_action)
        v04_action = torch.where(recommended == 2,
                                 torch.full_like(recommended, 3), v04_action)
        v04_action = torch.where(recommended == 4,
                                 torch.full_like(recommended, 4), v04_action)

        # Escalate local rerun to window rerun when the conflict signal is
        # severe (sigmoid > 0.85). This keeps cascading repair bounded by
        # max_repair_attempts in the executor.
        sigmoid_conflict = torch.sigmoid(conflict).squeeze(-1)
        severe = sigmoid_conflict > 0.85
        v04_action = torch.where((v04_action == 1) & severe,
                                 torch.full_like(v04_action, 2), v04_action)

        reroute_hint = v04_action == 3

        reasons: List[List[str]] = []
        for b in range(v04_action.shape[0]):
            code = int(v04_action[b].item())
            entry = [REPAIR_ACTION_NAMES.get(code, "unknown")]
            entry.append(f"sigmoid_conflict={sigmoid_conflict[b].item():.3f}")
            if severe[b]:
                entry.append("severe_conflict_escalated_to_window_rerun")
            reasons.append(entry)

        critic_log = {
            "repair_logits": raw.get("repair_logits"),
            "raw_recommended_action": raw["recommended_action"],
            "geometric_consistency_log": raw.get("critic_geometric_log"),
        }
        return CriticDecision(
            conflict_score=conflict,
            repair_action=v04_action,
            reroute_hint=reroute_hint,
            reason_codes=reasons,
            local_window_ids=[int(timestep)],
            critic_log=critic_log,
        )

    def _build_composer(self, raw: Dict[str, torch.Tensor],
                        reroute_hint: bool) -> ComposerDecision:
        selected_expert = raw.get("selected_expert")
        route_rec = raw.get("route_recommendation")
        routing_logits = raw.get("routing_logits")
        cost_adj = raw.get("cost_adjusted_scores")
        capability_match = raw["capability_match"]
        route_regret = raw["route_regret"]

        if selected_expert is None and route_rec is not None:
            selected_expert = route_rec[:, 0].long()
        if route_rec is None:
            # v01 Composer path returns sorted indices in route_recommendation
            # too; keep it None-safe.
            route_rec = torch.zeros(raw["pointmap"].shape[0], 1, dtype=torch.long)
        if routing_logits is None:
            routing_logits = torch.zeros(route_rec.shape[0], route_rec.shape[1])
        if cost_adj is None:
            cost_adj = routing_logits.clone()

        reroute_applied = False
        if reroute_hint and route_rec.shape[1] >= 2 and selected_expert is not None:
            alt = route_rec[:, 1].long()
            selected_expert = torch.where(
                torch.ones_like(selected_expert, dtype=torch.bool),
                alt, selected_expert,
            )
            reroute_applied = True

        registry = getattr(self.model.composer, "registry", None)
        if registry is not None:
            adapter_status = registry.adapter_status()
        else:
            adapter_status = {}
        backend_status = {
            "n_experts": route_rec.shape[1] if route_rec is not None else 0,
            "registry_attached": registry is not None,
            "adapter_status": adapter_status,
            "reroute_hint": bool(reroute_hint),
            "reroute_applied": reroute_applied,
        }
        return ComposerDecision(
            selected_expert=selected_expert,
            routing_logits=routing_logits,
            cost_adjusted_scores=cost_adj,
            route_recommendation=route_rec,
            capability_match=capability_match,
            route_regret=route_regret,
            reroute_applied=reroute_applied,
            backend_status=backend_status,
        )

    # ------------------------------------------------------------------
    # Expert dispatch
    # ------------------------------------------------------------------

    def _dispatch_expert(self,
                        composer: ComposerDecision,
                        images: Optional[torch.Tensor],
                        features: Optional[torch.Tensor],
                        raw: Dict[str, torch.Tensor],
                        ) -> DispatchedExpertOutput:
        registry = getattr(self.model.composer, "registry", None)
        names = sorted(registry.names) if registry is not None else []
        if composer.selected_expert is None or registry is None or not names:
            return self._fallback_expert_output(raw, reason="composer_no_dispatch")

        expert_id = int(composer.selected_expert[0].item())
        if expert_id < 0 or expert_id >= len(names):
            return self._fallback_expert_output(raw, reason="expert_id_out_of_range")

        expert_name = names[expert_id]

        # Adapters need raw images (5-D). When the user only passed features,
        # we cannot dispatch a real backend; fall back to a perception-derived
        # ExpertOutput so the final pipeline still has pointmap/confidence
        # tagged with a stub backend.
        if images is None or images.dim() != 5:
            return self._stub_expert_output(raw, expert_name,
                                            note="no_raw_images_for_dispatch")

        try:
            expert_out: Optional[ExpertOutput] = self.model.composer.dispatch(
                expert_id, images,
                context={
                    "regime_probs": raw.get("regime_card"),
                    "critic_confidence": raw.get("conflict_score"),
                },
            )
        except Exception as exc:  # noqa: BLE001 — never let dispatch crash the pipeline
            return self._stub_expert_output(raw, expert_name,
                                            note=f"dispatch_raised:{type(exc).__name__}")

        if expert_out is None:
            return self._stub_expert_output(raw, expert_name,
                                            note="dispatch_returned_none")

        adapter = registry.get(expert_name)
        is_loaded = bool(getattr(adapter, "is_loaded", False))
        is_available = bool(getattr(adapter, "is_available", lambda: False)())
        load_error = getattr(adapter, "load_error", None)
        backend = BACKEND_REAL if is_loaded else (
            BACKEND_FALLBACK if expert_out.metadata.get("backend") == "deterministic_fallback"
            else BACKEND_STUB
        )
        backend_status = {
            "expert_name": expert_name,
            "is_loaded": is_loaded,
            "is_available": is_available,
            "load_error": load_error,
            "backend": backend,
            "attention_regime": getattr(adapter, "attention_regime", "unknown"),
            "latency_estimate_ms": getattr(adapter, "latency_estimate_ms", 0.0),
            "dispatch_latency_ms": expert_out.metadata.get("dispatch_latency_ms"),
        }
        return DispatchedExpertOutput(
            pointmap=expert_out.pointmap,
            confidence=expert_out.confidence,
            evidence_tokens=expert_out.evidence_tokens,
            expert_name=expert_name,
            backend_status=backend_status,
            metadata=dict(expert_out.metadata),
        )

    def _fallback_expert_output(self, raw: Dict[str, torch.Tensor],
                                reason: str) -> DispatchedExpertOutput:
        return DispatchedExpertOutput(
            pointmap=raw["pointmap"],
            confidence=raw["confidence"],
            evidence_tokens=raw["evidence_tokens"],
            expert_name="<perception_proxy>",
            backend_status={
                "expert_name": "<perception_proxy>",
                "is_loaded": False,
                "is_available": False,
                "backend": BACKEND_STUB,
                "load_error": None,
                "reason": reason,
            },
            metadata={"backend": "perception_proxy", "reason": reason},
        )

    def _stub_expert_output(self, raw: Dict[str, torch.Tensor],
                            expert_name: str, note: str) -> DispatchedExpertOutput:
        return DispatchedExpertOutput(
            pointmap=raw["pointmap"],
            confidence=raw["confidence"],
            evidence_tokens=raw["evidence_tokens"],
            expert_name=expert_name,
            backend_status={
                "expert_name": expert_name,
                "is_loaded": False,
                "is_available": False,
                "backend": BACKEND_STUB,
                "note": note,
            },
            metadata={"backend": "stub", "note": note},
        )

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    def _assemble_output(self,
                        raw: Dict[str, torch.Tensor],
                        perception: PerceptionOutput,
                        memory: MemoryOutput,
                        permanence: PermanenceOutput,
                        critic: CriticDecision,
                        composer: ComposerDecision,
                        expert: DispatchedExpertOutput,
                        ) -> ReconstructionOutput:
        repair_report = self.repair.finalize()

        route_log = {
            "selected_expert_id": composer.selected_expert,
            "route_recommendation": composer.route_recommendation,
            "route_regret": composer.route_regret,
            "reroute_applied": composer.reroute_applied,
            "reroute_hint": critic.reroute_hint,
            "backend_status": composer.backend_status,
            "expert_backend_status": expert.backend_status,
        }
        offpath_dict = None
        if repair_report.offpath_verification is not None:
            ov = repair_report.offpath_verification
            offpath_dict = {
                "expert_id": ov.expert_id,
                "backend": ov.backend,
                "triggered_by": ov.triggered_by,
                "pointmap_shape": ov.pointmap_shape,
                "confidence_mean": ov.confidence_mean,
                "accepted_as_main_output": ov.accepted_as_main_output,
                "metadata": ov.metadata,
            }

        repair_action_log = {
            "final_action": repair_report.final_action,
            "final_action_name": repair_report.final_action_name,
            "n_attempts": repair_report.n_attempts,
            "max_attempts": repair_report.max_attempts,
            "reroute_hint": repair_report.reroute_hint,
            "capped": repair_report.capped,
            "attempts": [
                {
                    "attempt_index": a.attempt_index,
                    "action_code": a.action_code,
                    "action_name": a.action_name,
                    "reason": a.reason,
                    "triggered_by_critic": a.triggered_by_critic,
                    "succeeded": a.succeeded,
                    "note": a.note,
                }
                for a in repair_report.attempts
            ],
            "implemented_actions": list(REPAIR_ACTION_NAMES.keys()),
            "offpath_verification": offpath_dict,
        }

        memory_log = {
            "latent_drift_proxy": memory.latent_drift_proxy,
            "bank_occupancy": memory.bank_occupancy,
            "selected_anchor_stats": memory.selected_anchor_stats,
            "memory_backend_status": memory.memory_backend_status,
            "retrieval_log": memory.retrieval_log,
        }

        backend_status = {
            "architecture_version": ARCHITECTURE_VERSION,
            "perception": perception.backbone_status,
            "memory": memory.memory_backend_status,
            "permanence": {"backend": BACKEND_REAL},
            "critic": {"backend": BACKEND_REAL},
            "composer": composer.backend_status,
            "expert": expert.backend_status,
        }

        return ReconstructionOutput(
            pointmap=expert.pointmap,
            confidence=expert.confidence,
            dynamic_logits=permanence.dynamic_logits,
            dynamic_mask_proxy=permanence.dynamic_mask_proxy,
            dynamic_mask_final=permanence.dynamic_mask_final,
            evidence=expert.evidence_tokens,
            selected_expert=composer.selected_expert,
            backend_status=backend_status,
            conflict_score=critic.conflict_score,
            memory_log=memory_log,
            route_log=route_log,
            repair_action_log=repair_action_log,
            contract_log=list(raw.get("contract_log", [])),
            architecture_version=ARCHITECTURE_VERSION,
            perception=perception,
            memory=memory,
            permanence=permanence,
            critic=critic,
            composer=composer,
            expert=expert,
            repair=repair_report,
            next_memory_state=raw.get("latent_state_tokens", raw.get("latent_state")),
            next_object_slots=raw.get("object_track_set"),
            next_object_slot_poses=raw.get("object_slot_poses"),
        )


def build_v04_pipeline(model: nn.Module,
                       max_repair_attempts: int = 1) -> V04Pipeline:
    """Convenience constructor mirroring build_dream3r."""
    return V04Pipeline(model, max_repair_attempts=max_repair_attempts)
