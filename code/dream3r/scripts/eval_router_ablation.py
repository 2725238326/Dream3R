"""Evaluate Stage 3 learned router against single-expert baselines."""

import argparse
import json
import math
import random
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch

from dream3r.modules import ComposerRouter
from dream3r.scripts.train_router_only import _two_expert_registry


def _load_router(checkpoint: str, n_regimes: int) -> ComposerRouter:
    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    registry = _two_expert_registry()
    router = ComposerRouter(
        n_regimes=n_regimes,
        d_routing=ckpt["router_state_dict"]["regime_encoder.0.weight"].shape[0],
        cost_alpha=0.0,
        expert_registry=registry,
    )
    router.load_state_dict(ckpt["router_state_dict"])
    router.eval()
    return router


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
) -> Dict[str, object]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    expert_order = oracle_data["expert_order"]
    metrics = oracle_data["metrics"]
    sequences = sorted(seq for seq in oracle_data["labels"] if seq in regime_data["labels"])
    if not sequences:
        raise ValueError("no overlapping sequences to evaluate")

    router = _load_router(router_checkpoint, n_regimes=len(regime_data["regime_order"]))
    x = torch.tensor([regime_data["labels"][seq] for seq in sequences], dtype=torch.float32)
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
    fast3r_routes = {seq: "fast3r" for seq in sequences}
    mast3r_routes = {seq: "mast3r" for seq in sequences}
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

    metrics_out = {
        "learned_router": _mean_for_routes(metrics, learned_routes),
        "always_mast3r": _mean_for_routes(metrics, mast3r_routes),
        "always_fast3r": _mean_for_routes(metrics, fast3r_routes),
        "random_routing": _mean_for_routes(metrics, random_routes),
        "oracle_router": _mean_for_routes(metrics, oracle_routes),
    }
    result = {
        "metric": oracle_data.get("summary", {}).get("metric", "abs_rel"),
        "n_sequences": len(sequences),
        "expert_order": expert_order,
        "metrics": metrics_out,
        "routes": {
            "learned_router": learned_routes,
            "random_routing": random_routes,
            "oracle_router": oracle_routes,
        },
        "top_regimes": top_regimes,
        "route_regime_cramers_v": _cramers_v(regimes, learned_experts),
        "success": {
            "beats_mast3r": metrics_out["learned_router"] < metrics_out["always_mast3r"],
            "beats_fast3r": metrics_out["learned_router"] < metrics_out["always_fast3r"],
            "correlation_gt_0_3": _cramers_v(regimes, learned_experts) > 0.3,
        },
    }
    result["success"]["stage3"] = all(result["success"].values())

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
    args = parser.parse_args()

    result = evaluate_router_ablation(
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        router_checkpoint=args.router_checkpoint,
        output=args.output,
        random_seed=args.random_seed,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
