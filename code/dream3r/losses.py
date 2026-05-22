"""
Dream3R training losses.

v0.1 losses: pointmap, critic_p1, critic_p5, memory_p2, permanence_p4, action_entropy
v0.3 additions: retrieval (anti-collapse), routing (expert utilization), drift_consistency
v0.4 additions: geometric_consistency, retrieval_quality, state_drift_regularization
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict


class Dream3RLoss(nn.Module):
    """
    L_total = weighted sum of per-module losses.
    Each loss maps to a proxy metric from the ablation plan.
    """

    def __init__(self, weights: Dict[str, float] = None):
        super().__init__()
        self.w = weights or {
            "pointmap": 1.0,
            "critic_p1": 0.5,
            "critic_p5": 0.3,
            "memory_p2": 0.3,
            "memory_p3": 0.2,
            "permanence_p4": 0.5,
            "action_entropy": 0.1,
            "retrieval": 0.1,
            "retrieval_quality": 0.05,
            "routing": 0.05,
            "geometric_consistency": 0.05,
            "sampson_distance": 0.05,
            "covisibility_consistency": 0.05,
            "drift_consistency": 0.1,
            "state_drift_regularization": 0.01,
        }

    @staticmethod
    def sampson_distance_loss(pointmap_pair: torch.Tensor,
                              confidence_pair: torch.Tensor = None) -> torch.Tensor:
        from dream3r.modules import Critic
        return Critic.compute_geometric_consistency(
            pointmap_pair, confidence_pair
        )["sampson_distance"].mean()

    @staticmethod
    def covisibility_consistency_loss(pointmap_pair: torch.Tensor,
                                      confidence_pair: torch.Tensor = None) -> torch.Tensor:
        from dream3r.modules import Critic
        log = Critic.compute_geometric_consistency(pointmap_pair, confidence_pair)
        return (log["covisible_inconsistency"] + log["confidence_disagreement"]).mean()

    def forward(self, outputs: Dict[str, torch.Tensor],
                targets: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        losses = {}
        total = torch.tensor(0.0, device=next(iter(outputs.values())).device)

        # L_pointmap: standard 3R pointmap regression
        if "pointmap" in targets:
            pred = outputs["pointmap"]
            gt = targets["pointmap"]
            mask = targets.get("pointmap_mask", torch.ones_like(gt[..., 0]))
            l = ((pred - gt) ** 2 * mask.unsqueeze(-1)).sum() / (mask.sum() * 3 + 1e-8)
            losses["pointmap"] = l
            total = total + self.w["pointmap"] * l

        # L_geometric_consistency: preserve inter-window 3D displacement on overlap.
        if (
            "pointmap" in outputs and "prev_pointmap" in outputs
            and "pointmap" in targets and "prev_pointmap" in targets
        ):
            pred = outputs["pointmap"]
            pred_prev = outputs["prev_pointmap"]
            gt = targets["pointmap"]
            gt_prev = targets["prev_pointmap"]
            mask = targets.get("pointmap_mask", torch.ones_like(gt[..., 0]))
            prev_mask = targets.get("prev_pointmap_mask", mask)
            overlap = mask * prev_mask
            pred_delta = pred - pred_prev
            gt_delta = gt - gt_prev
            l_geo = (((pred_delta - gt_delta) ** 2) * overlap.unsqueeze(-1)).sum() / (
                overlap.sum() * 3 + 1e-8
            )
            losses["geometric_consistency"] = l_geo
            total = total + self.w.get("geometric_consistency", 0.05) * l_geo

        critic_geo_log = outputs.get("critic_geometric_log", {})
        if isinstance(critic_geo_log, dict):
            sampson = critic_geo_log.get("sampson_distance")
            if isinstance(sampson, torch.Tensor):
                losses["sampson_distance"] = sampson.float().mean()
                total = total + self.w.get("sampson_distance", 0.05) * losses["sampson_distance"]
            covis = critic_geo_log.get("covisible_inconsistency")
            conf_dis = critic_geo_log.get("confidence_disagreement")
            if isinstance(covis, torch.Tensor):
                l_covis = covis.float().mean()
                if isinstance(conf_dis, torch.Tensor):
                    l_covis = l_covis + conf_dis.float().mean()
                losses["covisibility_consistency"] = l_covis
                total = total + self.w.get("covisibility_consistency", 0.05) * l_covis

        # L_critic_P1: conflict detection (binary CE on conflict_score)
        if "conflict_label" in targets:
            pred = outputs["conflict_score"].squeeze(-1)
            gt = targets["conflict_label"].float()
            l = F.binary_cross_entropy_with_logits(pred, gt)
            losses["critic_p1"] = l
            total = total + self.w["critic_p1"] * l

        # L_critic_P5: repair action (CE on repair_logits)
        if "repair_label" in targets:
            pred = outputs["repair_logits"]
            pred = pred.clamp(min=-60000, max=60000)
            gt = targets["repair_label"].long()
            l = F.cross_entropy(pred, gt)
            losses["critic_p5"] = l
            total = total + self.w["critic_p5"] * l

        # L_memory_P2: anchor retention (encourage high scores on important anchors)
        if "anchor_importance_label" in targets:
            pred = outputs.get("update_kind")
            if pred is not None:
                gt = targets["anchor_importance_label"]
                l = F.cross_entropy(pred, gt.long())
                losses["memory_p2"] = l
                total = total + self.w["memory_p2"] * l

        # L_permanence_P4: dynamic pollution (CE on region classifier)
        if "region_label" in targets:
            pred = outputs["region_logits"]
            gt = targets["region_label"].long()
            B, S, C = pred.shape
            l = F.cross_entropy(pred.reshape(B * S, C), gt.reshape(B * S))
            losses["permanence_p4"] = l
            total = total + self.w["permanence_p4"] * l

        # L_action_entropy: encourage non-degenerate action distributions
        for key in ["update_kind", "repair_logits", "region_logits"]:
            if key in outputs:
                logits = outputs[key]
                if logits.dim() == 3:
                    logits = logits.reshape(-1, logits.shape[-1])
                probs = F.softmax(logits, dim=-1)
                entropy = -(probs * (probs + 1e-8).log()).sum(dim=-1).mean()
                losses[f"entropy_{key}"] = entropy
                total = total + self.w["action_entropy"] * (-entropy)

        # L_retrieval: encourage diverse AnchorBank usage (anti-collapse)
        if "nsa_branch_weights" in outputs:
            bw = outputs["nsa_branch_weights"]
            branch_usage = bw.mean(dim=(0, 1))
            target_uniform = torch.ones_like(branch_usage) / branch_usage.shape[0]
            l_ret = F.kl_div(
                branch_usage.clamp_min(1e-8).log(),
                target_uniform,
                reduction="batchmean",
            )
            losses["retrieval"] = l_ret
            total = total + self.w.get("retrieval", 0.1) * l_ret

        # L_retrieval_quality: prefer useful retrieved anchors, measured by high
        # selected similarity scores and low 3D anchor distance when available.
        log = outputs.get("memory_retrieval_log", {})
        if isinstance(log, dict):
            terms = []
            selected_scores = log.get("selected_scores_after_bias")
            if isinstance(selected_scores, torch.Tensor) and selected_scores.numel() > 0:
                finite_scores = selected_scores.float()[torch.isfinite(selected_scores)]
                if finite_scores.numel() > 0:
                    terms.append(F.softplus(-finite_scores.clamp(-50.0, 50.0)).mean())
            selected_distances = log.get("selected_3d_distances")
            if isinstance(selected_distances, torch.Tensor) and selected_distances.numel() > 0:
                finite = selected_distances.float()[torch.isfinite(selected_distances)]
                if finite.numel() > 0:
                    terms.append(finite.mean())
            if terms:
                l_quality = torch.stack(terms).mean()
                losses["retrieval_quality"] = l_quality
                total = total + self.w.get("retrieval_quality", 0.05) * l_quality

        # L_routing: expert utilization balance
        if "routing_logits" in outputs:
            route_probs = F.softmax(outputs["routing_logits"], dim=-1)
            avg_route = route_probs.mean(dim=0)
            target_uniform = torch.ones_like(avg_route) / avg_route.shape[0]
            l_route = F.kl_div(
                avg_route.clamp_min(1e-8).log(),
                target_uniform,
                reduction="batchmean",
            )
            losses["routing"] = l_route
            total = total + self.w.get("routing", 0.05) * l_route

        # L_drift_consistency: latent drift should correlate with scene change
        if "latent_drift_proxy" in outputs and "pointmap_change" in targets:
            drift = outputs["latent_drift_proxy"].squeeze(-1)
            change = targets["pointmap_change"]
            l_drift = F.mse_loss(torch.sigmoid(drift), change.clamp(0, 1))
            losses["drift_consistency"] = l_drift
            total = total + self.w.get("drift_consistency", 0.1) * l_drift

        # L_state_drift_regularization: keep recurrent memory updates bounded.
        if "latent_drift_proxy" in outputs:
            drift = outputs["latent_drift_proxy"].float()
            l_state = drift.pow(2).mean()
            losses["state_drift_regularization"] = l_state
            total = total + self.w.get("state_drift_regularization", 0.01) * l_state

        losses["total"] = total
        return losses
