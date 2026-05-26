"""Leave-one-out cross-validation for the Stage 5 S1 learned router.

For each held-out sequence, train the router on the remaining N-1 sequences and
predict the held-out expert. Aggregate the per-fold predictions into a single
LOO mean abs_rel and compare it against single-expert and oracle baselines.

This is the strongest cheap held-out check available on the 12-window KITTI
closure set: the held-out sample never contributes to training or to feature
normalization stats.
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.scripts.eval_router_ablation import evaluate_router_ablation
from dream3r.scripts.train_router_only import train_router_only


def evaluate_router_loo(
    regime_labels: str,
    oracle_labels: str,
    output: str,
    work_dir: str,
    epochs: int = 2000,
    lr: float = 0.05,
    batch_size: int = 12,
    d_routing: int = 32,
    feature_mode: str = "regime_stats",
    keep_fold_artifacts: bool = False,
    seed: int = 7,
) -> Dict[str, object]:
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    expert_order: List[str] = oracle_data["expert_order"]
    metrics = oracle_data["metrics"]
    sequences = sorted(
        seq for seq in oracle_data["labels"] if seq in regime_data["labels"]
    )
    if len(sequences) < 3:
        raise ValueError("LOO requires at least 3 sequences")

    work_path = Path(work_dir)
    work_path.mkdir(parents=True, exist_ok=True)

    per_fold: List[Dict[str, object]] = []
    learned_metric_sum = 0.0
    learned_routes: Dict[str, str] = {}
    correct_predictions = 0

    for idx, held_out in enumerate(sequences):
        train_set = [seq for seq in sequences if seq != held_out]
        fold_dir = work_path / f"fold_{idx:02d}_{held_out}"
        fold_ckpt_dir = fold_dir / "router"
        fold_eval = fold_dir / "eval.json"
        fold_dir.mkdir(parents=True, exist_ok=True)

        train_router_only(
            regime_labels=regime_labels,
            oracle_labels=oracle_labels,
            output_dir=str(fold_ckpt_dir),
            epochs=epochs,
            lr=lr,
            batch_size=batch_size,
            d_routing=d_routing,
            feature_mode=feature_mode,
            disable_critic_augmentation=True,
            sequence_filter=train_set,
            seed=seed,
        )
        fold_result = evaluate_router_ablation(
            regime_labels=regime_labels,
            oracle_labels=oracle_labels,
            router_checkpoint=str(fold_ckpt_dir / "latest.pt"),
            output=str(fold_eval),
            feature_mode=feature_mode,
            sequence_filter=[held_out],
        )

        predicted_expert = fold_result["routes"]["learned_router"][held_out]
        oracle_expert = fold_result["routes"]["oracle_router"][held_out]
        held_out_metric = float(metrics[held_out][predicted_expert])
        oracle_held_out = float(metrics[held_out][oracle_expert])
        learned_routes[held_out] = predicted_expert
        learned_metric_sum += held_out_metric
        if predicted_expert == oracle_expert:
            correct_predictions += 1

        per_fold.append({
            "held_out": held_out,
            "predicted_expert": predicted_expert,
            "oracle_expert": oracle_expert,
            "predicted_metric": held_out_metric,
            "oracle_metric": oracle_held_out,
            "feature_meta": fold_result["feature_meta"],
        })

        if not keep_fold_artifacts:
            shutil.rmtree(fold_ckpt_dir, ignore_errors=True)

    n = len(sequences)
    learned_loo_mean = learned_metric_sum / n
    oracle_loo_mean = sum(
        float(metrics[seq][expert_order[int(oracle_data["labels"][seq])]])
        for seq in sequences
    ) / n
    single_expert_means = {
        name: sum(float(metrics[seq][name]) for seq in sequences) / n
        for name in expert_order
    }
    best_single_expert = min(single_expert_means, key=single_expert_means.get)
    best_single_value = single_expert_means[best_single_expert]
    rel_improvement = (
        (best_single_value - learned_loo_mean) / best_single_value
        if best_single_value > 0
        else 0.0
    )
    learned_loo_expert_counts = {
        name: sum(1 for v in learned_routes.values() if v == name)
        for name in expert_order
    }

    result = {
        "metric": oracle_data.get("summary", {}).get("metric", "abs_rel"),
        "n_sequences": n,
        "n_folds": n,
        "expert_order": expert_order,
        "feature_mode": feature_mode,
        "seed": int(seed),
        "learned_loo_mean": learned_loo_mean,
        "oracle_loo_mean": oracle_loo_mean,
        "single_expert_means": single_expert_means,
        "best_single_expert": best_single_expert,
        "relative_improvement_vs_best_single": rel_improvement,
        "learned_loo_expert_counts": learned_loo_expert_counts,
        "loo_route_accuracy_vs_oracle": correct_predictions / n,
        "routes": {
            "learned_loo": learned_routes,
        },
        "per_fold": per_fold,
        "success": {
            "beats_best_single": learned_loo_mean < best_single_value,
            "improves_best_single_ge_5pct": rel_improvement >= 0.05,
            "loo_route_accuracy_ge_50pct": (correct_predictions / n) >= 0.5,
        },
    }

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--regime-labels", required=True)
    parser.add_argument("--oracle-labels", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--epochs", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=0.05)
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--d-routing", type=int, default=32)
    parser.add_argument(
        "--feature-mode",
        choices=["regime", "regime_stats", "regime_stats_robust"],
        default="regime_stats",
    )
    parser.add_argument("--keep-fold-artifacts", action="store_true")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    result = evaluate_router_loo(
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        output=args.output,
        work_dir=args.work_dir,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        d_routing=args.d_routing,
        feature_mode=args.feature_mode,
        keep_fold_artifacts=args.keep_fold_artifacts,
        seed=args.seed,
    )
    print(json.dumps({
        k: v for k, v in result.items()
        if k not in ("per_fold", "routes")
    }, indent=2))


if __name__ == "__main__":
    main()
