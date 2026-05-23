"""Train Stage 4 Critic on real expert KITTI conflict labels."""

import argparse
import json
import math
import time
from collections import Counter
from pathlib import Path
from typing import Dict

import torch
import torch.nn.functional as F

from dream3r.modules import Critic


def _contract_to_critic_target(actions: torch.Tensor) -> torch.Tensor:
    target = actions.clone()
    target = torch.where(actions == 3, torch.full_like(target, 2), target)
    return target


def _critic_to_contract_action(actions: torch.Tensor) -> torch.Tensor:
    mapped = torch.zeros_like(actions)
    mapped = torch.where(actions == 1, torch.ones_like(mapped), mapped)
    mapped = torch.where(actions == 2, torch.full_like(mapped, 3), mapped)
    mapped = torch.where(actions == 4, torch.full_like(mapped, 4), mapped)
    return mapped


def _pearson(x: torch.Tensor, y: torch.Tensor) -> float:
    x = x.float()
    y = y.float()
    vx = x - x.mean()
    vy = y - y.mean()
    denom = vx.norm() * vy.norm()
    if float(denom) <= 1e-8:
        return 0.0
    return float((vx * vy).sum().item() / denom.item())


def _baseline_action_accuracy(actions: torch.Tensor) -> float:
    return float((actions == 0).float().mean().item())


def train_critic_only(
    data_path: str,
    output_dir: str,
    epochs: int = 300,
    lr: float = 2e-3,
    d_critic: int = 64,
    n_heads: int = 4,
    n_layers: int = 2,
    action_weight: float = 0.5,
) -> Dict[str, object]:
    data = torch.load(data_path, map_location="cpu", weights_only=False)
    evidence = data["evidence"].float()
    pointmap_pair = data["pointmap_pair"].float()
    confidence_pair = data["confidence_pair"].float()
    abs_rel = data["abs_rel"].float()
    action = data["repair_action"].long()
    critic_target = _contract_to_critic_target(action)

    critic = Critic(
        n_evidence=evidence.shape[1],
        d_evidence=evidence.shape[2],
        d_critic=d_critic,
        n_heads=n_heads,
        n_layers=n_layers,
        geometric_conflict_scale=1.0,
        geometric_clean_bias=0.0,
    )
    optimizer = torch.optim.AdamW(critic.parameters(), lr=lr, weight_decay=1e-4)

    writer = None
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    try:
        from torch.utils.tensorboard import SummaryWriter
        writer = SummaryWriter(str(output_path / time.strftime("%Y%m%d-%H%M%S")))
    except ImportError:
        writer = None

    for epoch in range(epochs):
        out = critic(
            evidence,
            cr1_mask=torch.ones(evidence.shape[0]),
            pointmap_pair=pointmap_pair,
            confidence_pair=confidence_pair,
        )
        pred = out["conflict_score"].squeeze(-1)
        regression_loss = F.mse_loss(pred, abs_rel)
        action_loss = F.cross_entropy(out["repair_logits"], critic_target)
        loss = regression_loss + action_weight * action_loss

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

        if writer:
            writer.add_scalar("critic/loss", float(loss.item()), epoch)
            writer.add_scalar("critic/regression_loss", float(regression_loss.item()), epoch)
            writer.add_scalar("critic/action_loss", float(action_loss.item()), epoch)

    if writer:
        writer.close()

    critic.eval()
    with torch.no_grad():
        out = critic(
            evidence,
            cr1_mask=torch.ones(evidence.shape[0]),
            pointmap_pair=pointmap_pair,
            confidence_pair=confidence_pair,
        )
        conflict = out["conflict_score"].squeeze(-1)
        raw_action = out["repair_logits"].argmax(dim=-1)
        contract_action = _critic_to_contract_action(raw_action)
        action_accuracy = float((contract_action == action).float().mean().item())
        corr = _pearson(conflict, abs_rel)

    summary = {
        "n_examples": int(evidence.shape[0]),
        "conflict_abs_rel_corr": corr,
        "repair_action_accuracy": action_accuracy,
        "baseline_action0_accuracy": _baseline_action_accuracy(action),
        "target_action_counts": dict(Counter(str(int(x)) for x in action.tolist())),
        "pred_action_counts": dict(Counter(str(int(x)) for x in contract_action.tolist())),
        "success": {
            "corr_gt_0_5": corr > 0.5,
            "action_accuracy_gt_baseline": action_accuracy > _baseline_action_accuracy(action),
            "action_accuracy_gt_0_5": action_accuracy > 0.5,
        },
    }
    summary["success"]["t4_1"] = all(summary["success"].values())

    torch.save({
        "critic_state_dict": critic.state_dict(),
        "summary": summary,
        "config": {
            "d_critic": d_critic,
            "n_heads": n_heads,
            "n_layers": n_layers,
            "geometric_conflict_scale": 1.0,
            "geometric_clean_bias": 0.0,
        },
    }, output_path / "latest.pt")
    (output_path / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_critic_data/critic_training_data.pt",
    )
    parser.add_argument(
        "--output-dir",
        default="/hdd3/kykt26/checkpoints/critic_only_v1",
    )
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--d-critic", type=int, default=64)
    args = parser.parse_args()

    summary = train_critic_only(
        data_path=args.data,
        output_dir=args.output_dir,
        epochs=args.epochs,
        lr=args.lr,
        d_critic=args.d_critic,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
