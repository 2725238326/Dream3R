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
from dream3r.composer_experts.spann3r_adapter import Spann3RAdapter
from dream3r.config import load_config, save_config
from dream3r.modules import ComposerRouter


STAT_FEATURE_KEYS = [
    "frame_count",
    "depth_mean",
    "valid_ratio",
    "depth_temporal_change",
    "oxts_available",
    "mean_speed",
    "speed_std",
]

EXPERT_CLASSES = {
    "fast3r": Fast3RAdapter,
    "mast3r": MASt3RAdapter,
    "spann3r": Spann3RAdapter,
}


def _expert_registry(expert_order: List[str]) -> ExpertRegistry:
    registry = ExpertRegistry()
    unknown = [name for name in expert_order if name not in EXPERT_CLASSES]
    if unknown:
        raise ValueError(f"unsupported experts: {unknown}")
    for name in expert_order:
        registry.register_class(name, EXPERT_CLASSES[name])
    return registry


def _two_expert_registry() -> ExpertRegistry:
    return _expert_registry(["fast3r", "mast3r"])


def _load_examples(
    regime_labels: str,
    oracle_labels: str,
    feature_mode: str = "regime",
) -> Tuple[
    torch.Tensor,
    torch.Tensor,
    Optional[torch.Tensor],
    Optional[float],
    Optional[float],
    Optional[float],
    List[str],
    List[str],
    Dict[str, object],
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

    x, feature_meta = _feature_tensor(regime_data, sequences, feature_mode)
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
    conf_threshold_val: Optional[float] = None
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
            conflict_threshold = float(
                oracle_data.get("summary", {}).get("conflict_threshold", 0.20)
            )
            conf_threshold_val = float(
                1.0 - torch.sigmoid(torch.tensor(conflict_threshold)).item()
            )
    return (
        x, y, alt_y, conf_high_val, conf_low_val, conf_threshold_val,
        sequences, expert_order, feature_meta,
    )


def _feature_tensor(
    regime_data: Dict[str, object],
    sequences: List[str],
    feature_mode: str = "regime",
) -> Tuple[torch.Tensor, Dict[str, object]]:
    regime_x = torch.tensor(
        [regime_data["labels"][seq] for seq in sequences],
        dtype=torch.float32,
    )
    if feature_mode == "regime":
        return regime_x, {
            "feature_mode": feature_mode,
            "regime_width": int(regime_x.shape[1]),
            "stat_keys": [],
        }
    if feature_mode != "regime_stats":
        raise ValueError(f"unsupported feature_mode: {feature_mode}")

    stats_source = "stats"
    stats_data = regime_data.get("stats")
    if not isinstance(stats_data, dict):
        stats_source = "features"
        stats_data = regime_data.get("features")
    if not isinstance(stats_data, dict):
        raise ValueError(
            "feature_mode=regime_stats requires regime label stats/features"
        )
    rows = []
    for seq in sequences:
        if seq not in stats_data:
            raise ValueError(f"missing stats for sequence: {seq}")
        rows.append([float(stats_data[seq].get(key, 0.0)) for key in STAT_FEATURE_KEYS])
    stats = torch.tensor(rows, dtype=torch.float32)
    mean = stats.mean(dim=0, keepdim=True)
    std = stats.std(dim=0, keepdim=True, unbiased=False).clamp_min(1e-6)
    norm_stats = (stats - mean) / std
    x = torch.cat([regime_x, norm_stats], dim=-1)
    return x, {
        "feature_mode": feature_mode,
        "regime_width": int(regime_x.shape[1]),
        "stat_source": stats_source,
        "stat_keys": list(STAT_FEATURE_KEYS),
        "stat_mean": [float(v) for v in mean.squeeze(0).tolist()],
        "stat_std": [float(v) for v in std.squeeze(0).tolist()],
    }


def _load_context_examples(
    regime_labels: str,
    context_data: Optional[str],
    expert_order: List[str],
    feature_mode: str = "regime",
) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]:
    if not context_data:
        return None, None
    data_path = Path(context_data)
    if not data_path.exists():
        return None, None
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    data = torch.load(data_path, map_location="cpu", weights_only=False)
    if list(data["summary"]["expert_order"]) != expert_order:
        raise ValueError("context data expert_order does not match oracle labels")

    order: List[str] = []
    grouped: Dict[str, Dict[str, float]] = {}
    for meta in data["meta"]:
        seq = str(meta["sequence"])
        expert = str(meta["expert"])
        if seq not in grouped:
            order.append(seq)
            grouped[seq] = {}
        grouped[seq][expert] = float(meta["abs_rel"])

    sequences = [
        seq for seq in order
        if seq in regime_data["labels"]
        and all(name in grouped[seq] for name in expert_order)
    ]
    if not sequences:
        return None, None

    x_ctx, _ = _feature_tensor(regime_data, sequences, feature_mode)
    y_ctx = torch.tensor(
        [
            expert_order.index(min(expert_order, key=lambda name: grouped[seq][name]))
            for seq in sequences
        ],
        dtype=torch.long,
    )
    return x_ctx, y_ctx


def _accuracy(logits: torch.Tensor, target: torch.Tensor) -> float:
    pred = logits.argmax(dim=-1)
    return float((pred == target).float().mean().item())


def _class_weights(
    target: torch.Tensor, n_classes: int, balance_alpha: float = 0.0,
) -> torch.Tensor:
    if balance_alpha <= 0.0:
        return torch.ones(n_classes, dtype=torch.float32)
    counts = torch.bincount(target, minlength=n_classes).float()
    weights = torch.ones(n_classes, dtype=torch.float32)
    present = counts > 0
    base = counts[present].sum() / (present.sum() * counts[present])
    weights[present] = base.pow(balance_alpha)
    return weights


def train_router_only(
    regime_labels: str,
    oracle_labels: str,
    output_dir: str,
    context_data: Optional[str] = None,
    epochs: int = 100,
    lr: float = 1e-2,
    d_routing: int = 32,
    batch_size: int = 16,
    seed: int = 7,
    class_balance_alpha: float = 0.0,
    disable_critic_augmentation: bool = False,
    feature_mode: str = "regime",
) -> Dict[str, object]:
    torch.manual_seed(seed)
    (
        x, y, alt_y, conf_high_val, conf_low_val, conf_threshold_val,
        sequences, expert_order, feature_meta,
    ) = _load_examples(regime_labels, oracle_labels, feature_mode=feature_mode)
    if disable_critic_augmentation:
        alt_y = None
        conf_high_val = None
        conf_low_val = None
        conf_threshold_val = None

    registry = _expert_registry(expert_order)
    router_order = sorted(registry.names)
    if router_order != expert_order:
        raise ValueError(f"oracle expert_order {expert_order} != router order {router_order}")
    router = ComposerRouter(
        n_regimes=x.shape[1],
        d_routing=d_routing,
        cost_alpha=0.0,
        expert_registry=registry,
    )
    if feature_meta["feature_mode"] == "regime":
        router.load_from_registry()
    router.capability_cards.zero_()
    router.latency_costs.zero_()
    x_ctx, y_ctx = _load_context_examples(
        regime_labels, context_data, expert_order, feature_mode=feature_mode,
    )
    class_weights = _class_weights(
        y, len(expert_order), balance_alpha=class_balance_alpha,
    )
    context_class_weights = (
        _class_weights(y_ctx, len(expert_order), balance_alpha=class_balance_alpha)
        if y_ctx is not None
        else class_weights
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    writer = None
    try:
        from torch.utils.tensorboard import SummaryWriter
        writer = SummaryWriter(str(output_path / time.strftime("%Y%m%d-%H%M%S")))
    except ImportError:
        writer = None

    augment = (
        alt_y is not None
        and conf_high_val is not None
        and conf_low_val is not None
        and conf_threshold_val is not None
    )
    dynamic_idx = torch.empty(0, dtype=torch.long)
    if augment:
        regime_width = int(feature_meta["regime_width"])
        dynamic_idx = torch.tensor(
            [
                idx for idx, probs in enumerate(x)
                if int(probs[:regime_width].argmax().item()) == 2
            ],
            dtype=torch.long,
        )

    optimizer = torch.optim.AdamW(router.parameters(), lr=lr, weight_decay=1e-4)
    with torch.no_grad():
        initial_logits = router(x)["routing_logits"]
        initial_acc = _accuracy(initial_logits, y)

    # Joint training: regime_encoder + routing_head + confidence_gate are
    # trained together. In augmented mode each step combines
    #   loss_n = CE(router(x),               y)        # no-conf path
    #   loss_h = CE(router(x, conf=conf_h),  y)        # high-conf reinforces oracle
    #   loss_l = CE(router(x, conf=conf_l),  alt_y)    # low-conf flips to alt expert
    #   loss_t = CE(router(x_dyn, conf=conf_threshold), alt_y_dyn)
    #            # near-threshold dynamic conflicts should explore the alternate
    # The regime-aware MLP gate (modules.ComposerRouter) lets per-regime
    # gradients separate, so we no longer need a two-stage schedule or a
    # conf-input shift trick.
    n = x.shape[0]
    for epoch in range(epochs):
        perm_n = torch.randperm(n)
        perm_h = torch.randperm(n) if augment else None
        perm_l = torch.randperm(n) if augment else None
        total_loss = 0.0
        for start in range(0, n, batch_size):
            idx = perm_n[start:start + batch_size]
            out = router(x[idx])
            loss = F.cross_entropy(
                out["routing_logits"], y[idx], weight=class_weights,
            )

            if augment:
                idx_h = perm_h[start:start + batch_size]
                conf_h = torch.full((idx_h.numel(), 1), conf_high_val)
                out_h = router(x[idx_h], critic_confidence=conf_h)
                loss_h = F.cross_entropy(
                    out_h["routing_logits"], y[idx_h], weight=class_weights,
                )

                idx_l = perm_l[start:start + batch_size]
                conf_l = torch.full((idx_l.numel(), 1), conf_low_val)
                out_l = router(x[idx_l], critic_confidence=conf_l)
                loss_l = F.cross_entropy(
                    out_l["routing_logits"], alt_y[idx_l], weight=class_weights,
                )
                out_l_prev_best = router(
                    x[idx_l],
                    critic_confidence=conf_l,
                    previous_expert_id=y[idx_l],
                )
                loss_l_prev_best = F.cross_entropy(
                    out_l_prev_best["routing_logits"], alt_y[idx_l],
                    weight=class_weights,
                )
                out_l_prev_alt = router(
                    x[idx_l],
                    critic_confidence=conf_l,
                    previous_expert_id=alt_y[idx_l],
                )
                loss_l_prev_alt = F.cross_entropy(
                    out_l_prev_alt["routing_logits"], y[idx_l],
                    weight=class_weights,
                )
                conf_z = torch.zeros((idx_l.numel(), 1))
                out_z_prev_best = router(
                    x[idx_l],
                    critic_confidence=conf_z,
                    previous_expert_id=y[idx_l],
                )
                loss_z_prev_best = F.cross_entropy(
                    out_z_prev_best["routing_logits"], alt_y[idx_l],
                    weight=class_weights,
                )
                out_z_prev_alt = router(
                    x[idx_l],
                    critic_confidence=conf_z,
                    previous_expert_id=alt_y[idx_l],
                )
                loss_z_prev_alt = F.cross_entropy(
                    out_z_prev_alt["routing_logits"], y[idx_l],
                    weight=class_weights,
                )

                loss = (
                    loss + loss_h + loss_l
                    + loss_l_prev_best + loss_l_prev_alt
                    + loss_z_prev_best + loss_z_prev_alt
                ) / 7.0
                if dynamic_idx.numel() > 0:
                    conf_t = torch.full((dynamic_idx.numel(), 1), conf_threshold_val)
                    out_t_prev_best = router(
                        x[dynamic_idx],
                        critic_confidence=conf_t,
                        previous_expert_id=y[dynamic_idx],
                    )
                    loss_t_prev_best = F.cross_entropy(
                        out_t_prev_best["routing_logits"], alt_y[dynamic_idx],
                        weight=class_weights,
                    )
                    out_t_prev_alt = router(
                        x[dynamic_idx],
                        critic_confidence=conf_t,
                        previous_expert_id=alt_y[dynamic_idx],
                    )
                    loss_t_prev_alt = F.cross_entropy(
                        out_t_prev_alt["routing_logits"], y[dynamic_idx],
                        weight=class_weights,
                    )
                    loss = (loss + loss_t_prev_best + loss_t_prev_alt) / 3.0
                if x_ctx is not None and y_ctx is not None:
                    context_losses = []
                    conf_values = [
                        torch.full((x_ctx.shape[0], 1), conf_low_val),
                        torch.full((x_ctx.shape[0], 1), conf_threshold_val),
                        torch.zeros((x_ctx.shape[0], 1)),
                    ]
                    for conf_ctx in conf_values:
                        for prev_id in range(len(expert_order)):
                            prev_ctx = torch.full(
                                (x_ctx.shape[0], 1), prev_id, dtype=torch.long,
                            )
                            out_ctx = router(
                                x_ctx,
                                critic_confidence=conf_ctx,
                                previous_expert_id=prev_ctx,
                            )
                            context_losses.append(
                                F.cross_entropy(
                                    out_ctx["routing_logits"], y_ctx,
                                    weight=context_class_weights,
                                )
                            )
                    context_loss = sum(context_losses) / len(context_losses)
                    loss = 0.25 * loss + 0.75 * context_loss

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
        "conf_threshold_val": conf_threshold_val,
        "context_n_examples": 0 if x_ctx is None else int(x_ctx.shape[0]),
        "feature_mode": feature_mode,
        "feature_meta": feature_meta,
        "class_balance_alpha": class_balance_alpha,
        "class_weights": [float(v) for v in class_weights.tolist()],
        "critic_augmentation_disabled": bool(disable_critic_augmentation),
    }
    if augment:
        with torch.no_grad():
            conf_h_eval = torch.full((n, 1), conf_high_val)
            conf_l_eval = torch.full((n, 1), conf_low_val)
            pred_high = router(x, critic_confidence=conf_h_eval)["routing_logits"].argmax(dim=-1)
            pred_low = router(x, critic_confidence=conf_l_eval)["routing_logits"].argmax(dim=-1)
            pred_low_prev_best = router(
                x,
                critic_confidence=conf_l_eval,
                previous_expert_id=y,
            )["routing_logits"].argmax(dim=-1)
            pred_low_prev_alt = router(
                x,
                critic_confidence=conf_l_eval,
                previous_expert_id=alt_y,
            )["routing_logits"].argmax(dim=-1)
            conf_z_eval = torch.zeros((n, 1))
            pred_zero_prev_best = router(
                x,
                critic_confidence=conf_z_eval,
                previous_expert_id=y,
            )["routing_logits"].argmax(dim=-1)
            pred_zero_prev_alt = router(
                x,
                critic_confidence=conf_z_eval,
                previous_expert_id=alt_y,
            )["routing_logits"].argmax(dim=-1)
            if dynamic_idx.numel() > 0:
                conf_t_eval = torch.full((dynamic_idx.numel(), 1), conf_threshold_val)
                pred_threshold_dyn_prev_best = router(
                    x[dynamic_idx],
                    critic_confidence=conf_t_eval,
                    previous_expert_id=y[dynamic_idx],
                )["routing_logits"].argmax(dim=-1)
                pred_threshold_dyn_prev_alt = router(
                    x[dynamic_idx],
                    critic_confidence=conf_t_eval,
                    previous_expert_id=alt_y[dynamic_idx],
                )["routing_logits"].argmax(dim=-1)
                no_conf_dyn = torch.tensor(predictions)[dynamic_idx]
            else:
                pred_threshold_dyn_prev_best = torch.empty(0, dtype=torch.long)
                pred_threshold_dyn_prev_alt = torch.empty(0, dtype=torch.long)
                no_conf_dyn = torch.empty(0, dtype=torch.long)
        summary["high_conf_accuracy_vs_best"] = float((pred_high == y).float().mean().item())
        summary["low_conf_accuracy_vs_alt"] = float((pred_low == alt_y).float().mean().item())
        summary["low_conf_flip_rate_vs_no_conf"] = float(
            (pred_low != torch.tensor(predictions)).float().mean().item()
        )
        summary["low_conf_avoid_prev_best_accuracy"] = float(
            (pred_low_prev_best == alt_y).float().mean().item()
        )
        summary["low_conf_avoid_prev_alt_accuracy"] = float(
            (pred_low_prev_alt == y).float().mean().item()
        )
        summary["zero_conf_avoid_prev_best_accuracy"] = float(
            (pred_zero_prev_best == alt_y).float().mean().item()
        )
        summary["zero_conf_avoid_prev_alt_accuracy"] = float(
            (pred_zero_prev_alt == y).float().mean().item()
        )
        summary["threshold_dynamic_flip_rate_vs_no_conf"] = float(
            (pred_threshold_dyn_prev_best != no_conf_dyn).float().mean().item()
        ) if dynamic_idx.numel() > 0 else 0.0
        summary["threshold_dynamic_avoid_prev_best_accuracy"] = float(
            (pred_threshold_dyn_prev_best == alt_y[dynamic_idx]).float().mean().item()
        ) if dynamic_idx.numel() > 0 else 0.0
        summary["threshold_dynamic_avoid_prev_alt_accuracy"] = float(
            (pred_threshold_dyn_prev_alt == y[dynamic_idx]).float().mean().item()
        ) if dynamic_idx.numel() > 0 else 0.0
        if x_ctx is not None and y_ctx is not None:
            with torch.no_grad():
                context_accs: Dict[str, List[float]] = {}
                for name, value in [
                    ("low", conf_low_val),
                    ("threshold", conf_threshold_val),
                    ("zero", 0.0),
                ]:
                    conf_ctx_eval = torch.full((x_ctx.shape[0], 1), value)
                    context_accs[name] = []
                    for prev_id in range(len(expert_order)):
                        prev_ctx = torch.full(
                            (x_ctx.shape[0], 1), prev_id, dtype=torch.long,
                        )
                        pred_ctx = router(
                            x_ctx,
                            critic_confidence=conf_ctx_eval,
                            previous_expert_id=prev_ctx,
                        )["routing_logits"].argmax(dim=-1)
                        context_accs[name].append(
                            float((pred_ctx == y_ctx).float().mean().item())
                        )
            for name, accs in context_accs.items():
                summary[f"{name}_conf_context_accuracy_min"] = min(accs)
                summary[f"{name}_conf_context_accuracy_mean"] = float(
                    sum(accs) / len(accs)
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
    parser.add_argument("--context-data", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--class-balance-alpha", type=float, default=0.0)
    parser.add_argument("--disable-critic-augmentation", action="store_true")
    parser.add_argument(
        "--feature-mode",
        choices=["regime", "regime_stats"],
        default="regime",
    )
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
        context_data=args.context_data,
        epochs=cfg["epochs"],
        lr=cfg["lr"],
        d_routing=cfg.get("d_routing", 32),
        batch_size=cfg["batch_size"],
        class_balance_alpha=args.class_balance_alpha,
        disable_critic_augmentation=args.disable_critic_augmentation,
        feature_mode=args.feature_mode,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
