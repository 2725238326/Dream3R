"""Train the Stage 3 ComposerRouter against oracle expert labels."""

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.config import load_config, save_config
from dream3r.modules import ComposerRouter


def _two_expert_registry() -> ExpertRegistry:
    registry = ExpertRegistry()
    registry.register_class("fast3r", Fast3RAdapter)
    registry.register_class("mast3r", MASt3RAdapter)
    return registry


def _load_examples(
    regime_labels: str,
    oracle_labels: str,
) -> Tuple[
    torch.Tensor,
    torch.Tensor,
    Optional[torch.Tensor],
    Optional[float],
    Optional[float],
    List[str],
    List[str],
]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    expert_order = oracle_data["expert_order"]

    sequences = [
        seq for seq in sorted(oracle_data["labels"])
        if seq in regime_data["labels"]
    ]
    if not sequences:
        raise ValueError("no overlapping sequences between regime and oracle labels")

    x = torch.tensor(
        [regime_data["labels"][seq] for seq in sequences],
        dtype=torch.float32,
    )
    y = torch.tensor(
        [int(oracle_data["labels"][seq]) for seq in sequences],
        dtype=torch.long,
    )

    # Optional critic-confidence augmentation: derive alt-expert labels and
    # eval-matched conf values from per-expert metrics, so that the router's
    # confidence_gate actually receives gradient during training.
    alt_y: Optional[torch.Tensor] = None
    conf_high_val: Optional[float] = None
    conf_low_val: Optional[float] = None
    metrics = oracle_data.get("metrics")
    if metrics and all(seq in metrics for seq in sequences):
        alt_labels: List[int] = []
        all_vals: List[float] = []
        for seq in sequences:
            seq_metrics = metrics[seq]
            ordered = sorted(
                expert_order,
                key=lambda name: seq_metrics.get(name, float("inf")),
            )
            alt_name = ordered[1] if len(ordered) >= 2 else ordered[0]
            alt_labels.append(expert_order.index(alt_name))
            all_vals.extend(
                float(seq_metrics[name]) for name in expert_order
                if name in seq_metrics
            )
        if alt_labels and all_vals:
            alt_y = torch.tensor(alt_labels, dtype=torch.long)
            # Match the eval-time transform from model.py forward:
            # critic_confidence = 1 - sigmoid(prev_conflict_score),
            # where prev_conflict_score is the critic's regression of abs_rel.
            min_val = min(all_vals)
            max_val = max(all_vals)
            conf_high_val = float(
                1.0 - torch.sigmoid(torch.tensor(min_val)).item()
            )
            conf_low_val = float(
                1.0 - torch.sigmoid(torch.tensor(max_val)).item()
            )
    return x, y, alt_y, conf_high_val, conf_low_val, sequences, expert_order


def _accuracy(logits: torch.Tensor, target: torch.Tensor) -> float:
    pred = logits.argmax(dim=-1)
    return float((pred == target).float().mean().item())


def train_router_only(
    regime_labels: str,
    oracle_labels: str,
    output_dir: str,
    epochs: int = 100,
    lr: float = 1e-2,
    d_routing: int = 32,
    batch_size: int = 16,
    seed: int = 7,
) -> Dict[str, object]:
    torch.manual_seed(seed)
    (
        x, y, alt_y, conf_high_val, conf_low_val,
        sequences, expert_order,
    ) = _load_examples(regime_labels, oracle_labels)

    registry = _two_expert_registry()
    router_order = sorted(registry.names)
    if router_order != expert_order:
        raise ValueError(f"oracle expert_order {expert_order} != router order {router_order}")
    router = ComposerRouter(
        n_regimes=x.shape[1],
        d_routing=d_routing,
        cost_alpha=0.0,
        expert_registry=registry,
    )
    router.load_from_registry()
    router.capability_cards.zero_()
    router.latency_costs.zero_()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    writer = None
    try:
        from torch.utils.tensorboard import SummaryWriter
        writer = SummaryWriter(str(output_path / time.strftime("%Y%m%d-%H%M%S")))
    except ImportError:
        writer = None

    optimizer = torch.optim.AdamW(router.parameters(), lr=lr, weight_decay=1e-4)
    with torch.no_grad():
        initial_logits = router(x)["routing_logits"]
        initial_acc = _accuracy(initial_logits, y)

    augment = (
        alt_y is not None
        and conf_high_val is not None
        and conf_low_val is not None
    )

    n = x.shape[0]
    for epoch in range(epochs):
        perm_n = torch.randperm(n)
        perm_h = torch.randperm(n) if augment else None
        perm_l = torch.randperm(n) if augment else None
        total_loss = 0.0
        for start in range(0, n, batch_size):
            idx = perm_n[start:start + batch_size]
            out = router(x[idx])
            loss = F.cross_entropy(out["routing_logits"], y[idx])

            if augment:
                idx_h = perm_h[start:start + batch_size]
                conf_h = torch.full((idx_h.numel(), 1), conf_high_val)
                out_h = router(x[idx_h], critic_confidence=conf_h)
                loss_h = F.cross_entropy(out_h["routing_logits"], y[idx_h])

                idx_l = perm_l[start:start + batch_size]
                conf_l = torch.full((idx_l.numel(), 1), conf_low_val)
                out_l = router(x[idx_l], critic_confidence=conf_l)
                loss_l = F.cross_entropy(out_l["routing_logits"], alt_y[idx_l])

                loss = (loss + loss_h + loss_l) / 3.0

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item()) * idx.numel()

        with torch.no_grad():
            logits = router(x)["routing_logits"]
            acc = _accuracy(logits, y)
        avg_loss = total_loss / max(n, 1)
        if writer:
            writer.add_scalar("router/loss", avg_loss, epoch)
            writer.add_scalar("router/accuracy", acc, epoch)

    if writer:
        writer.close()

    with torch.no_grad():
        final_logits = router(x)["routing_logits"]
        final_acc = _accuracy(final_logits, y)
        predictions = final_logits.argmax(dim=-1).tolist()

    summary = {
        "n_examples": n,
        "expert_order": expert_order,
        "initial_accuracy": initial_acc,
        "final_accuracy": final_acc,
        "target_counts": dict(Counter(y.tolist())),
        "prediction_counts": dict(Counter(predictions)),
        "sequences": sequences,
        "augmented_with_critic_confidence": bool(augment),
        "conf_high_val": conf_high_val,
        "conf_low_val": conf_low_val,
    }
    if augment:
        with torch.no_grad():
            conf_h_eval = torch.full((n, 1), conf_high_val)
            conf_l_eval = torch.full((n, 1), conf_low_val)
            pred_high = router(x, critic_confidence=conf_h_eval)["routing_logits"].argmax(dim=-1)
            pred_low = router(x, critic_confidence=conf_l_eval)["routing_logits"].argmax(dim=-1)
        summary["high_conf_accuracy_vs_best"] = float((pred_high == y).float().mean().item())
        summary["low_conf_accuracy_vs_alt"] = float((pred_low == alt_y).float().mean().item())
        summary["low_conf_flip_rate_vs_no_conf"] = float(
            (pred_low != torch.tensor(predictions)).float().mean().item()
        )
    torch.save({
        "router_state_dict": router.state_dict(),
        "expert_order": expert_order,
        "summary": summary,
    }, output_path / "latest.pt")
    (output_path / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", default="router_only")
    parser.add_argument("--config", default=None)
    parser.add_argument("--regime-labels", default=None)
    parser.add_argument("--oracle-labels", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    cfg = load_config(path=args.config, preset=args.preset)
    if args.regime_labels:
        cfg["regime_labels_path"] = args.regime_labels
    if args.oracle_labels:
        cfg["oracle_labels_path"] = args.oracle_labels
    if args.output_dir:
        cfg["save_dir"] = args.output_dir
    if args.epochs:
        cfg["epochs"] = args.epochs
    if args.lr:
        cfg["lr"] = args.lr
    if args.batch_size:
        cfg["batch_size"] = args.batch_size

    out_dir = Path(cfg["save_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    save_config(cfg, str(out_dir / "config.yaml"))
    summary = train_router_only(
        regime_labels=cfg["regime_labels_path"],
        oracle_labels=cfg["oracle_labels_path"],
        output_dir=str(out_dir),
        epochs=cfg["epochs"],
        lr=cfg["lr"],
        d_routing=cfg.get("d_routing", 32),
        batch_size=cfg["batch_size"],
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
