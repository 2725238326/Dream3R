"""Train the Stage 3 ComposerRouter against oracle expert labels."""

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

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


def _load_examples(regime_labels: str, oracle_labels: str) -> Tuple[torch.Tensor, torch.Tensor, List[str], List[str]]:
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
    return x, y, sequences, expert_order


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
    x, y, sequences, expert_order = _load_examples(regime_labels, oracle_labels)

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

    n = x.shape[0]
    for epoch in range(epochs):
        perm = torch.randperm(n)
        total_loss = 0.0
        for start in range(0, n, batch_size):
            idx = perm[start:start + batch_size]
            out = router(x[idx])
            loss = F.cross_entropy(out["routing_logits"], y[idx])
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
    }
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
