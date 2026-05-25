"""Evaluate Stage 3 learned router against single-expert baselines."""

import argparse
import json
import math
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch

from dream3r.modules import ComposerRouter
from dream3r.scripts.train_router_only import _expert_registry, _feature_tensor


def _load_router(checkpoint: str, n_regimes: int,
                 expert_order: List[str] | None = None,
                 expected_feature_mode: Optional[str] = None,
                 ) -> Tuple[ComposerRouter, Dict[str, object]]:
    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    order = expert_order or ckpt.get("expert_order") or ckpt.get("summary", {}).get("expert_order")
    if order is None:
        order = ["fast3r", "mast3r"]
    summary = ckpt.get("summary") or {}
    ckpt_feature_meta = summary.get("feature_meta") or {}
    ckpt_feature_mode = ckpt_feature_meta.get("feature_mode") or summary.get("feature_mode")
    if (
        expected_feature_mode is not None
        and ckpt_feature_mode is not None
        and expected_feature_mode != ckpt_feature_mode
    ):
        raise ValueError(
            f"feature_mode mismatch: checkpoint trained with '{ckpt_feature_mode}' "
            f"but eval requested '{expected_feature_mode}'"
        )
    registry = _expert_registry(list(order))
    router = ComposerRouter(
        n_regimes=n_regimes,
        d_routing=ckpt["router_state_dict"]["regime_encoder.0.weight"].shape[0],
        cost_alpha=0.0,
        expert_registry=registry,
    )
    router.load_state_dict(ckpt["router_state_dict"])
    router.eval()
    return router, ckpt_feature_meta


def _mean_for_routes(metrics: Dict[str, Dict[str, float]],
                     routes: Dict[str, str]) -> float:
    values = [metrics[seq][expert] for seq, expert in routes.items()]
    return float(sum(values) / max(len(values), 1))


def _cramers_v(regimes: List[str], experts: List[str]) -> float:
    if len(regimes) != len(experts) or not regimes:
        return 0.0
    regime_ids = {name: idx for idx, name in enumerate(sorted(set(regimes)))}
    expert_ids = {name: idx for idx, name in enumerate(sorted(set(experts)))}
    table = np.zeros((len(regime_ids), len(expert_ids)), dtype=np.float64)
    for regime, expert in zip(regimes, experts):
        table[regime_ids[regime], expert_ids[expert]] += 1.0

    n = table.sum()
    if n <= 0 or min(table.shape) <= 1:
        return 0.0
    expected = np.outer(table.sum(axis=1), table.sum(axis=0)) / n
    valid = expected > 0
    chi2 = ((table[valid] - expected[valid]) ** 2 / expected[valid]).sum()
    denom = n * (min(table.shape) - 1)
    return float(math.sqrt(chi2 / denom)) if denom > 0 else 0.0


def evaluate_router_ablation(
    regime_labels: str,
    oracle_labels: str,
    router_checkpoint: str,
    output: str,
    random_seed: int = 7,
    feature_mode: str = "regime",
    sequence_filter: Optional[List[str]] = None,
) -> Dict[str, object]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    expert_order = oracle_data["expert_order"]
    metrics = oracle_data["metrics"]
    sequences = sorted(seq for seq in oracle_data["labels"] if seq in regime_data["labels"])
    if sequence_filter is not None:
        filter_set = set(sequence_filter)
        sequences = [seq for seq in sequences if seq in filter_set]
    if not sequences:
        raise ValueError("no overlapping sequences to evaluate")

    ckpt_peek = torch.load(router_checkpoint, map_location="cpu", weights_only=False)
    ckpt_feature_meta = (ckpt_peek.get("summary") or {}).get("feature_meta") or {}
    frozen_stats: Optional[Dict[str, object]] = None
    if feature_mode == "regime_stats" and ckpt_feature_meta.get("stat_mean") is not None:
        frozen_stats = {
            "stat_mean": ckpt_feature_meta["stat_mean"],
            "stat_std": ckpt_feature_meta["stat_std"],
        }

    x, feature_meta = _feature_tensor(
        regime_data, sequences, feature_mode, frozen_stats=frozen_stats,
    )
    router, _ = _load_router(
        router_checkpoint,
        n_regimes=x.shape[1],
        expert_order=expert_order,
        expected_feature_mode=feature_mode,
    )
    with torch.no_grad():
        pred_ids = router(x)["routing_logits"].argmax(dim=-1).tolist()
    learned_routes = {
        seq: expert_order[pred_id]
        for seq, pred_id in zip(sequences, pred_ids)
    }

    rng = random.Random(random_seed)
    random_routes = {
        seq: expert_order[rng.randrange(len(expert_order))]
        for seq in sequences
    }
    oracle_routes = {
        seq: expert_order[int(oracle_data["labels"][seq])]
        for seq in sequences
    }

    top_regimes = {
        seq: oracle_data.get("regime_top", {}).get(seq)
        or regime_data["regime_order"][int(np.argmax(regime_data["labels"][seq]))]
        for seq in sequences
    }
    regimes = [top_regimes[seq] for seq in sequences]
    learned_experts = [learned_routes[seq] for seq in sequences]
    oracle_experts = [oracle_routes[seq] for seq in sequences]
    learned_expert_counts = {
        name: learned_experts.count(name)
        for name in expert_order
    }
    oracle_expert_counts = {
        name: oracle_experts.count(name)
        for name in expert_order
    }

    metrics_out = {
        "learned_router": _mean_for_routes(metrics, learned_routes),
        "random_routing": _mean_for_routes(metrics, random_routes),
        "oracle_router": _mean_for_routes(metrics, oracle_routes),
    }
    single_expert_means = {}
    for name in expert_order:
        routes = {seq: name for seq in sequences}
        value = _mean_for_routes(metrics, routes)
        single_expert_means[name] = value
        metrics_out[f"always_{name}"] = value
    best_single_expert = min(single_expert_means, key=single_expert_means.get)
    best_single_value = single_expert_means[best_single_expert]
    learned_value = metrics_out["learned_router"]
    rel_improvement = (
        (best_single_value - learned_value) / best_single_value
        if best_single_value > 0
        else 0.0
    )
    regime_route_v = _cramers_v(regimes, learned_experts)
    success = {
        f"beats_{name}": learned_value < value
        for name, value in single_expert_means.items()
    }
    success.update({
        "candidate_count_ge_3": len(expert_order) >= 3,
        "oracle_uses_ge_3_experts": sum(v > 0 for v in oracle_expert_counts.values()) >= 3,
        "learned_uses_ge_3_experts": sum(v > 0 for v in learned_expert_counts.values()) >= 3,
        "beats_best_single": learned_value < best_single_value,
        "improves_best_single_ge_5pct": rel_improvement >= 0.05,
        "correlation_gt_0_3": regime_route_v > 0.3,
    })
    result = {
        "metric": oracle_data.get("summary", {}).get("metric", "abs_rel"),
        "n_sequences": len(sequences),
        "expert_order": expert_order,
        "feature_mode": feature_mode,
        "feature_meta": feature_meta,
        "learned_expert_counts": learned_expert_counts,
        "oracle_expert_counts": oracle_expert_counts,
        "metrics": metrics_out,
        "best_single_expert": best_single_expert,
        "relative_improvement_vs_best_single": float(rel_improvement),
        "routes": {
            "learned_router": learned_routes,
            "random_routing": random_routes,
            "oracle_router": oracle_routes,
        },
        "top_regimes": top_regimes,
        "route_regime_cramers_v": regime_route_v,
        "success": success,
    }
    result["success"]["stage3"] = (
        result["success"].get("beats_fast3r", False)
        and result["success"].get("beats_mast3r", False)
        and result["success"]["correlation_gt_0_3"]
    )
    result["success"]["stage5_s1"] = (
        len(expert_order) >= 3
        and result["success"]["oracle_uses_ge_3_experts"]
        and result["success"]["improves_best_single_ge_5pct"]
        and result["success"]["correlation_gt_0_3"]
    )

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--oracle-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_oracle_labels/oracle_expert_labels.json",
    )
    parser.add_argument(
        "--router-checkpoint",
        default="/hdd3/kykt26/checkpoints/router_only_v1/latest.pt",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_router_ablation/results.json",
    )
    parser.add_argument("--random-seed", type=int, default=7)
    parser.add_argument(
        "--feature-mode",
        choices=["regime", "regime_stats"],
        default="regime",
    )
    args = parser.parse_args()

    result = evaluate_router_ablation(
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        router_checkpoint=args.router_checkpoint,
        output=args.output,
        random_seed=args.random_seed,
        feature_mode=args.feature_mode,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
