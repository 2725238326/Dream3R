"""Per-domain LOO for the joint KITTI+ETH3D router.

For each held-out sequence (across 109 joint examples), train a fresh
joint router on the remaining N-1, predict the held-out expert, and
aggregate route accuracy per domain. Supports ``--max-folds`` to
subsample folds when wall time is tight.
"""

import argparse
import json
import random
import shutil
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.scripts.train_router_joint_domain import (
    _load_joint_examples,
    train_router_joint,
)


def evaluate_joint_loo(
    kitti_regime: str,
    kitti_oracle: str,
    eth3d_regime: str,
    eth3d_oracle: str,
    output: str,
    work_dir: str,
    epochs: int = 2000,
    lr: float = 0.05,
    batch_size: int = 108,
    d_routing: int = 32,
    max_folds: int = 0,
    seed: int = 7,
    keep_fold_artifacts: bool = False,
    per_domain_norm: bool = False,
) -> Dict[str, object]:
    # Build the full joint set once just to get the sequence/domain ordering
    # and the per-window oracle expert; per-fold training uses sequence_filter.
    x_full, y_full, seqs, domains, expert_order, _ = _load_joint_examples(
        kitti_regime, kitti_oracle, eth3d_regime, eth3d_oracle,
        per_domain_norm=per_domain_norm,
    )
    n = len(seqs)
    if n < 3:
        raise ValueError("joint LOO requires at least 3 sequences")

    # Per-sequence oracle metric tables (so we can compute LOO abs_rel cheaply)
    k_ora = json.loads(Path(kitti_oracle).read_text(encoding="utf-8"))
    e_ora = json.loads(Path(eth3d_oracle).read_text(encoding="utf-8"))
    metrics: Dict[str, Dict[str, float]] = {}
    metrics.update(k_ora["metrics"])
    metrics.update(e_ora["metrics"])

    work_path = Path(work_dir)
    work_path.mkdir(parents=True, exist_ok=True)

    fold_indices = list(range(n))
    if max_folds > 0 and max_folds < n:
        rng = random.Random(seed)
        # Stratified by domain so subsample preserves domain balance
        kitti_idx = [i for i, d in enumerate(domains) if d == "kitti"]
        eth3d_idx = [i for i, d in enumerate(domains) if d == "eth3d"]
        n_kitti = round(max_folds * len(kitti_idx) / n)
        n_eth3d = max_folds - n_kitti
        rng.shuffle(kitti_idx)
        rng.shuffle(eth3d_idx)
        fold_indices = sorted(kitti_idx[:n_kitti] + eth3d_idx[:n_eth3d])

    per_fold: List[Dict[str, object]] = []
    correct_per_domain: Dict[str, int] = {"kitti": 0, "eth3d": 0}
    total_per_domain: Dict[str, int] = {"kitti": 0, "eth3d": 0}
    learned_metric_sum_per_domain: Dict[str, float] = {"kitti": 0.0, "eth3d": 0.0}
    oracle_metric_sum_per_domain: Dict[str, float] = {"kitti": 0.0, "eth3d": 0.0}

    for fold_pos, idx in enumerate(fold_indices):
        held_out_seq = seqs[idx]
        held_out_domain = domains[idx]
        train_seqs = [seqs[i] for i in range(n) if i != idx]

        fold_dir = work_path / f"fold_{fold_pos:03d}_{held_out_domain}_{held_out_seq}"
        fold_ckpt_dir = fold_dir / "router"
        fold_ckpt_dir.mkdir(parents=True, exist_ok=True)

        train_router_joint(
            kitti_regime=kitti_regime,
            kitti_oracle=kitti_oracle,
            eth3d_regime=eth3d_regime,
            eth3d_oracle=eth3d_oracle,
            output_dir=str(fold_ckpt_dir),
            epochs=epochs,
            lr=lr,
            batch_size=batch_size,
            d_routing=d_routing,
            sequence_filter=train_seqs,
            per_domain_norm=per_domain_norm,
        )

        ckpt = torch.load(
            fold_ckpt_dir / "latest.pt", map_location="cpu", weights_only=False
        )
        fold_feature_meta = ckpt["summary"]["feature_meta"]
        if per_domain_norm:
            frozen_per_domain_stats = fold_feature_meta["per_domain_stats"]
            x_held, y_held, seqs_held, domains_held, _, _ = _load_joint_examples(
                kitti_regime, kitti_oracle, eth3d_regime, eth3d_oracle,
                sequence_filter=[held_out_seq],
                per_domain_norm=True,
                frozen_per_domain_stats=frozen_per_domain_stats,
            )
        else:
            frozen_stats = {
                "stat_mean": fold_feature_meta["stat_mean"],
                "stat_std": fold_feature_meta["stat_std"],
            }
            x_held, y_held, seqs_held, domains_held, _, _ = _load_joint_examples(
                kitti_regime, kitti_oracle, eth3d_regime, eth3d_oracle,
                sequence_filter=[held_out_seq],
                frozen_stats=frozen_stats,
            )
        # Re-instantiate router and load state for inference
        from dream3r.modules import ComposerRouter
        from dream3r.scripts.train_router_only import _expert_registry as _reg

        d_in = x_held.shape[1]
        router = ComposerRouter(
            n_regimes=d_in,
            d_routing=ckpt["router_state_dict"]["regime_encoder.0.weight"].shape[0],
            cost_alpha=0.0,
            expert_registry=_reg(expert_order),
        )
        router.load_state_dict(ckpt["router_state_dict"])
        router.eval()
        with torch.no_grad():
            pred_id = int(router(x_held)["routing_logits"].argmax(dim=-1).item())
        predicted_expert = expert_order[pred_id]
        oracle_expert = expert_order[int(y_held.item())]
        held_out_metric = float(metrics[held_out_seq][predicted_expert])
        oracle_held_metric = float(metrics[held_out_seq][oracle_expert])

        correct = int(predicted_expert == oracle_expert)
        correct_per_domain[held_out_domain] += correct
        total_per_domain[held_out_domain] += 1
        learned_metric_sum_per_domain[held_out_domain] += held_out_metric
        oracle_metric_sum_per_domain[held_out_domain] += oracle_held_metric

        per_fold.append({
            "held_out": held_out_seq,
            "domain": held_out_domain,
            "predicted_expert": predicted_expert,
            "oracle_expert": oracle_expert,
            "predicted_metric": held_out_metric,
            "oracle_metric": oracle_held_metric,
        })

        if not keep_fold_artifacts:
            shutil.rmtree(fold_ckpt_dir, ignore_errors=True)

    def _safe_div(num: float, den: int) -> float:
        return float(num / den) if den > 0 else 0.0

    per_domain_route_acc = {
        d: _safe_div(correct_per_domain[d], total_per_domain[d])
        for d in ("kitti", "eth3d")
    }
    per_domain_learned_mean = {
        d: _safe_div(learned_metric_sum_per_domain[d], total_per_domain[d])
        for d in ("kitti", "eth3d")
    }
    per_domain_oracle_mean = {
        d: _safe_div(oracle_metric_sum_per_domain[d], total_per_domain[d])
        for d in ("kitti", "eth3d")
    }

    # Best-single per domain (from oracle metric tables) — for relative improvement
    def _best_single(metrics_subset: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for name in expert_order:
            vals = [float(m[name]) for m in metrics_subset.values() if name in m]
            out[name] = sum(vals) / len(vals) if vals else float("inf")
        return out

    k_singles = _best_single(k_ora["metrics"])
    e_singles = _best_single(e_ora["metrics"])
    k_best = min(k_singles, key=k_singles.get)
    e_best = min(e_singles, key=e_singles.get)

    per_domain_rel_improvement = {
        "kitti": (
            (k_singles[k_best] - per_domain_learned_mean["kitti"]) / k_singles[k_best]
            if k_singles[k_best] > 0 and total_per_domain["kitti"] > 0
            else 0.0
        ),
        "eth3d": (
            (e_singles[e_best] - per_domain_learned_mean["eth3d"]) / e_singles[e_best]
            if e_singles[e_best] > 0 and total_per_domain["eth3d"] > 0
            else 0.0
        ),
    }

    result = {
        "n_total_examples": n,
        "n_folds_run": len(fold_indices),
        "subsampled": len(fold_indices) < n,
        "per_domain_norm": bool(per_domain_norm),
        "expert_order": expert_order,
        "per_domain_loo_route_accuracy": per_domain_route_acc,
        "per_domain_loo_learned_mean": per_domain_learned_mean,
        "per_domain_loo_oracle_mean": per_domain_oracle_mean,
        "per_domain_best_single_expert": {"kitti": k_best, "eth3d": e_best},
        "per_domain_best_single_mean": {
            "kitti": k_singles[k_best],
            "eth3d": e_singles[e_best],
        },
        "per_domain_rel_improvement_vs_best_single": per_domain_rel_improvement,
        "per_domain_fold_counts": total_per_domain,
        "per_fold": per_fold,
        "success": {
            "kitti_loo_route_acc_gt_33pct": per_domain_route_acc["kitti"] > 1.0 / 3.0,
            "eth3d_loo_route_acc_gt_33pct": per_domain_route_acc["eth3d"] > 1.0 / 3.0,
            "both_domains_above_chance": (
                per_domain_route_acc["kitti"] > 1.0 / 3.0
                and per_domain_route_acc["eth3d"] > 1.0 / 3.0
            ),
        },
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kitti-regime", required=True)
    parser.add_argument("--kitti-oracle", required=True)
    parser.add_argument("--eth3d-regime", required=True)
    parser.add_argument("--eth3d-oracle", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--epochs", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=0.05)
    parser.add_argument("--batch-size", type=int, default=108)
    parser.add_argument("--d-routing", type=int, default=32)
    parser.add_argument("--max-folds", type=int, default=0)
    parser.add_argument("--keep-fold-artifacts", action="store_true")
    parser.add_argument("--per-domain-norm", action="store_true")
    args = parser.parse_args()

    result = evaluate_joint_loo(
        kitti_regime=args.kitti_regime,
        kitti_oracle=args.kitti_oracle,
        eth3d_regime=args.eth3d_regime,
        eth3d_oracle=args.eth3d_oracle,
        output=args.output,
        work_dir=args.work_dir,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        d_routing=args.d_routing,
        max_folds=args.max_folds,
        keep_fold_artifacts=args.keep_fold_artifacts,
        per_domain_norm=args.per_domain_norm,
    )
    print(json.dumps({
        k: v for k, v in result.items() if k != "per_fold"
    }, indent=2))


if __name__ == "__main__":
    main()
