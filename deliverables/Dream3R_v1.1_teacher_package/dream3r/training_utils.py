"""Shared metrics and dataset splitting utilities for cache-based training."""

from __future__ import annotations

import random
from typing import Dict, List

import torch


def pointmap_abs_rel(
    pred: torch.Tensor,
    target: torch.Tensor,
    mask: torch.Tensor,
    align_scale: bool = False,
) -> float:
    """Return mean absolute relative depth error on valid points."""

    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (target_depth.abs() > 1e-6)
    )
    if not bool(valid.any()):
        return float("inf")
    if align_scale:
        denominator = pred_depth[valid].median()
        denominator = torch.where(
            denominator.abs() > 1e-6,
            denominator,
            denominator.new_tensor(1e-6),
        )
        pred_depth = pred_depth * (target_depth[valid].median() / denominator)
    relative_error = (
        (pred_depth - target_depth).abs()
        / target_depth.abs().clamp_min(1e-6)
    )
    return float(relative_error[valid].mean().item())


def abs_rel_loss(
    pred: torch.Tensor,
    target: torch.Tensor,
    mask: torch.Tensor,
    align_scale: bool = True,
) -> torch.Tensor:
    """Differentiable absolute relative depth loss with optional scale alignment."""

    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (target_depth.abs() > 1e-6)
    )
    if not bool(valid.any()):
        return pred.sum() * 0.0
    if align_scale:
        with torch.no_grad():
            denominator = pred_depth[valid].detach().median()
            denominator = torch.where(
                denominator.abs() > 1e-6,
                denominator,
                denominator.new_tensor(1e-6),
            )
            scale = target_depth[valid].median() / denominator
        pred_depth = pred_depth * scale
    relative_error = (
        (pred_depth - target_depth).abs()
        / target_depth.abs().clamp_min(1e-6)
    )
    return relative_error[valid].mean()


def stratified_split(
    entries: List[Dict],
    seed: int,
    holdout_frac: float = 0.2,
) -> tuple[list[int], list[int]]:
    """Split indices by domain using a deterministic random seed."""

    by_domain: Dict[str, List[int]] = {}
    for index, entry in enumerate(entries):
        by_domain.setdefault(entry["domain"], []).append(index)
    rng = random.Random(seed)
    train_indices: list[int] = []
    test_indices: list[int] = []
    for indices in by_domain.values():
        shuffled = list(indices)
        rng.shuffle(shuffled)
        test_count = max(1, int(round(len(shuffled) * holdout_frac)))
        test_indices.extend(shuffled[:test_count])
        train_indices.extend(shuffled[test_count:])
    return sorted(train_indices), sorted(test_indices)
