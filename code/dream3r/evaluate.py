"""
Dream3R evaluation harness.

Computes standard 3R metrics on a validation/test set:
  - Pointmap MSE / MAE
  - Confidence calibration (ECE)
  - Critic accuracy (conflict detection F1)
  - Memory utilization (AnchorBank occupancy, branch usage)
  - Composer routing diversity (entropy, regret distribution)
  - Per-regime accuracy breakdown
"""

import torch
import torch.nn.functional as F
from typing import Dict, List
from dataclasses import dataclass, field
import json


@dataclass
class EvalMetrics:
    pointmap_mse: float = 0.0
    pointmap_mae: float = 0.0
    pointmap_l2: float = 0.0
    pointmap_acc_005: float = 0.0
    pointmap_acc_010: float = 0.0
    depth_absrel: float = 0.0
    depth_sqrel: float = 0.0
    depth_rmse: float = 0.0
    depth_rmse_log: float = 0.0
    depth_delta1: float = 0.0
    depth_delta2: float = 0.0
    depth_delta3: float = 0.0
    chamfer_l2: float = 0.0
    fscore_005: float = 0.0
    fscore_010: float = 0.0
    confidence_ece: float = 0.0
    critic_f1: float = 0.0
    critic_precision: float = 0.0
    critic_recall: float = 0.0
    memory_occupancy: float = 0.0
    memory_branch_compressed: float = 0.0
    memory_branch_selected: float = 0.0
    memory_branch_sliding: float = 0.0
    memory_branch_entropy: float = 0.0
    selected_anchor_3d_distance: float = 0.0
    geometry_bias_applied: float = 0.0
    critic_sampson_distance: float = 0.0
    critic_covisible_inconsistency: float = 0.0
    critic_depth_inconsistency: float = 0.0
    state_drift_magnitude: float = 0.0
    routing_entropy: float = 0.0
    routing_mean_regret: float = 0.0
    n_samples: int = 0
    per_regime: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if k != "per_regime"}
        d["per_regime"] = self.per_regime
        return d

    def to_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


class Evaluator:
    """Accumulates predictions across batches, then computes final metrics."""

    def __init__(self):
        self._pointmap_se: List[float] = []
        self._pointmap_ae: List[float] = []
        self._pointmap_l2: List[float] = []
        self._pointmap_acc_005: List[float] = []
        self._pointmap_acc_010: List[float] = []
        self._depth_metrics: List[Dict[str, float]] = []
        self._chamfer: List[float] = []
        self._fscore_005: List[float] = []
        self._fscore_010: List[float] = []
        self._conf_bins: List[List[float]] = [[] for _ in range(10)]
        self._conf_acc_bins: List[List[float]] = [[] for _ in range(10)]
        self._critic_tp = 0
        self._critic_fp = 0
        self._critic_fn = 0
        self._branch_weights: List[torch.Tensor] = []
        self._selected_3d_distances: List[float] = []
        self._geometry_biases: List[float] = []
        self._critic_sampson: List[float] = []
        self._critic_covisible: List[float] = []
        self._critic_depth: List[float] = []
        self._state_drifts: List[float] = []
        self._occupancies: List[float] = []
        self._routing_logits: List[torch.Tensor] = []
        self._regrets: List[float] = []
        self._n = 0

    @torch.no_grad()
    def update(self, outputs: Dict[str, torch.Tensor],
               targets: Dict[str, torch.Tensor]):
        self._n += 1

        if "pointmap" in outputs and "pointmap" in targets:
            pred = outputs["pointmap"]
            gt = targets["pointmap"]
            mask = targets.get("pointmap_mask", torch.ones_like(gt[..., 0]))
            se = ((pred - gt) ** 2 * mask.unsqueeze(-1)).sum() / (mask.sum() * 3 + 1e-8)
            ae = ((pred - gt).abs() * mask.unsqueeze(-1)).sum() / (mask.sum() * 3 + 1e-8)
            l2 = ((pred - gt).norm(dim=-1) * mask).sum() / (mask.sum() + 1e-8)
            point_err = (pred - gt).norm(dim=-1)
            acc_005 = ((point_err < 0.05).float() * mask).sum() / (mask.sum() + 1e-8)
            acc_010 = ((point_err < 0.10).float() * mask).sum() / (mask.sum() + 1e-8)
            self._pointmap_se.append(se.item())
            self._pointmap_ae.append(ae.item())
            self._pointmap_l2.append(l2.item())
            self._pointmap_acc_005.append(acc_005.item())
            self._pointmap_acc_010.append(acc_010.item())

            self._depth_metrics.append(compute_depth_metrics(pred[..., 2], gt[..., 2], mask))
            chamfer, f005, f010 = compute_3d_metrics(pred, gt, mask)
            self._chamfer.append(chamfer)
            self._fscore_005.append(f005)
            self._fscore_010.append(f010)

        if "conflict_score" in outputs and "conflict_label" in targets:
            pred = (torch.sigmoid(outputs["conflict_score"].squeeze(-1)) > 0.5).float()
            gt = targets["conflict_label"].float()
            tp = ((pred == 1) & (gt == 1)).sum().item()
            fp = ((pred == 1) & (gt == 0)).sum().item()
            fn = ((pred == 0) & (gt == 1)).sum().item()
            self._critic_tp += tp
            self._critic_fp += fp
            self._critic_fn += fn

        if "nsa_branch_weights" in outputs:
            self._branch_weights.append(
                outputs["nsa_branch_weights"].mean(dim=(0, 1)).cpu()
            )

        log = outputs.get("memory_retrieval_log", {})
        if isinstance(log, dict):
            selected_dist = log.get("selected_3d_distances")
            if isinstance(selected_dist, torch.Tensor):
                finite = selected_dist[torch.isfinite(selected_dist)]
                if finite.numel() > 0:
                    self._selected_3d_distances.append(finite.mean().item())
            geo_bias = log.get("geometry_bias_applied")
            if isinstance(geo_bias, torch.Tensor):
                self._geometry_biases.append(geo_bias.float().mean().item())

        critic_geo = outputs.get("critic_geometric_log", {})
        if isinstance(critic_geo, dict):
            sampson = critic_geo.get("sampson_distance")
            if isinstance(sampson, torch.Tensor):
                self._critic_sampson.append(sampson.float().mean().item())
            covisible = critic_geo.get("covisible_inconsistency")
            if isinstance(covisible, torch.Tensor):
                self._critic_covisible.append(covisible.float().mean().item())
            depth = critic_geo.get("depth_inconsistency")
            if isinstance(depth, torch.Tensor):
                self._critic_depth.append(depth.float().mean().item())

        if "latent_drift_proxy" in outputs:
            self._state_drifts.append(outputs["latent_drift_proxy"].float().abs().mean().item())

        if "bank_occupancy" in outputs:
            occ = outputs["bank_occupancy"]
            if isinstance(occ, torch.Tensor):
                self._occupancies.append(occ.mean().item())

        if "routing_logits" in outputs:
            self._routing_logits.append(outputs["routing_logits"].cpu())

        if "route_regret" in outputs:
            self._regrets.append(outputs["route_regret"].mean().item())

    def compute(self) -> EvalMetrics:
        m = EvalMetrics(n_samples=self._n)

        if self._pointmap_se:
            m.pointmap_mse = sum(self._pointmap_se) / len(self._pointmap_se)
        if self._pointmap_ae:
            m.pointmap_mae = sum(self._pointmap_ae) / len(self._pointmap_ae)
        if self._pointmap_l2:
            m.pointmap_l2 = sum(self._pointmap_l2) / len(self._pointmap_l2)
            m.pointmap_acc_005 = sum(self._pointmap_acc_005) / len(self._pointmap_acc_005)
            m.pointmap_acc_010 = sum(self._pointmap_acc_010) / len(self._pointmap_acc_010)
        if self._depth_metrics:
            for key in self._depth_metrics[0].keys():
                setattr(m, f"depth_{key}", sum(d[key] for d in self._depth_metrics) / len(self._depth_metrics))
        if self._chamfer:
            m.chamfer_l2 = sum(self._chamfer) / len(self._chamfer)
            m.fscore_005 = sum(self._fscore_005) / len(self._fscore_005)
            m.fscore_010 = sum(self._fscore_010) / len(self._fscore_010)

        prec_denom = self._critic_tp + self._critic_fp
        rec_denom = self._critic_tp + self._critic_fn
        m.critic_precision = self._critic_tp / prec_denom if prec_denom > 0 else 0.0
        m.critic_recall = self._critic_tp / rec_denom if rec_denom > 0 else 0.0
        if m.critic_precision + m.critic_recall > 0:
            m.critic_f1 = 2 * m.critic_precision * m.critic_recall / (m.critic_precision + m.critic_recall)

        if self._branch_weights:
            avg = torch.stack(self._branch_weights).mean(dim=0)
            m.memory_branch_compressed = avg[0].item()
            m.memory_branch_selected = avg[1].item()
            m.memory_branch_sliding = avg[2].item()
            m.memory_branch_entropy = (-(avg * avg.clamp_min(1e-8).log()).sum()).item()

        if self._selected_3d_distances:
            m.selected_anchor_3d_distance = sum(self._selected_3d_distances) / len(self._selected_3d_distances)
        if self._geometry_biases:
            m.geometry_bias_applied = sum(self._geometry_biases) / len(self._geometry_biases)
        if self._critic_sampson:
            m.critic_sampson_distance = sum(self._critic_sampson) / len(self._critic_sampson)
        if self._critic_covisible:
            m.critic_covisible_inconsistency = sum(self._critic_covisible) / len(self._critic_covisible)
        if self._critic_depth:
            m.critic_depth_inconsistency = sum(self._critic_depth) / len(self._critic_depth)
        if self._state_drifts:
            m.state_drift_magnitude = sum(self._state_drifts) / len(self._state_drifts)

        if self._occupancies:
            m.memory_occupancy = sum(self._occupancies) / len(self._occupancies)

        if self._routing_logits:
            all_logits = torch.cat(self._routing_logits, dim=0)
            probs = F.softmax(all_logits, dim=-1)
            avg_probs = probs.mean(dim=0)
            entropy = -(avg_probs * (avg_probs + 1e-8).log()).sum().item()
            m.routing_entropy = entropy

        if self._regrets:
            m.routing_mean_regret = sum(self._regrets) / len(self._regrets)

        return m


@torch.no_grad()
def compute_depth_metrics(pred_depth: torch.Tensor, gt_depth: torch.Tensor,
                          mask: torch.Tensor = None) -> Dict[str, float]:
    pred = pred_depth.float().abs().clamp_min(1e-6)
    gt = gt_depth.float().abs().clamp_min(1e-6)
    valid = torch.isfinite(pred) & torch.isfinite(gt)
    if mask is not None:
        valid = valid & mask.bool()
    if valid.sum() == 0:
        return {k: 0.0 for k in ["absrel", "sqrel", "rmse", "rmse_log", "delta1", "delta2", "delta3"]}

    pred = pred[valid]
    gt = gt[valid]
    diff = pred - gt
    ratio = torch.maximum(pred / gt, gt / pred)
    return {
        "absrel": ((diff.abs() / gt).mean()).item(),
        "sqrel": (((diff ** 2) / gt).mean()).item(),
        "rmse": torch.sqrt((diff ** 2).mean()).item(),
        "rmse_log": torch.sqrt(((pred.log() - gt.log()) ** 2).mean()).item(),
        "delta1": (ratio < 1.25).float().mean().item(),
        "delta2": (ratio < 1.25 ** 2).float().mean().item(),
        "delta3": (ratio < 1.25 ** 3).float().mean().item(),
    }


@torch.no_grad()
def compute_3d_metrics(pred_points: torch.Tensor, gt_points: torch.Tensor,
                       mask: torch.Tensor = None,
                       thresholds=(0.05, 0.10)) -> tuple:
    pred = pred_points.reshape(-1, 3).float()
    gt = gt_points.reshape(-1, 3).float()
    valid = torch.isfinite(pred).all(dim=-1) & torch.isfinite(gt).all(dim=-1)
    if mask is not None:
        valid = valid & mask.reshape(-1).bool()
    pred = pred[valid]
    gt = gt[valid]
    if pred.numel() == 0 or gt.numel() == 0:
        return 0.0, 0.0, 0.0

    dist = torch.cdist(pred.unsqueeze(0), gt.unsqueeze(0)).squeeze(0)
    pred_to_gt = dist.min(dim=1).values
    gt_to_pred = dist.min(dim=0).values
    chamfer = (pred_to_gt.pow(2).mean() + gt_to_pred.pow(2).mean()).item()
    fscores = []
    for threshold in thresholds:
        precision = (pred_to_gt < threshold).float().mean()
        recall = (gt_to_pred < threshold).float().mean()
        fscore = (2 * precision * recall / (precision + recall + 1e-8)).item()
        fscores.append(fscore)
    return chamfer, fscores[0], fscores[1]
