"""Cross-domain transfer eval: KITTI-trained router on ETH3D windows.

Loads the Stage 5 S1 expanded router checkpoint and evaluates it against the
ETH3D oracle. Reuses `evaluate_router_ablation` for the core arithmetic and
adds cross-domain reporting fields: route distribution shift vs the KITTI
training oracle, ETH3D best-single-expert vs KITTI, route accuracy comparison.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

from dream3r.scripts.eval_router_ablation import evaluate_router_ablation


def _route_counts(routes: Dict[str, str], expert_order: List[str]) -> Dict[str, int]:
    counts = {name: 0 for name in expert_order}
    for expert in routes.values():
        if expert in counts:
            counts[expert] += 1
    return counts


def evaluate_cross_domain(
    regime_labels: str,
    oracle_labels: str,
    router_checkpoint: str,
    output: str,
    kitti_oracle_labels: Optional[str] = None,
    feature_mode: str = "regime_stats",
) -> Dict[str, object]:
    base = evaluate_router_ablation(
        regime_labels=regime_labels,
        oracle_labels=oracle_labels,
        router_checkpoint=router_checkpoint,
        output=output,
        feature_mode=feature_mode,
    )

    expert_order = base["expert_order"]
    learned_routes = base["routes"]["learned_router"]
    oracle_routes = base["routes"]["oracle_router"]

    learned_counts = _route_counts(learned_routes, expert_order)
    oracle_counts = _route_counts(oracle_routes, expert_order)

    eth3d_route_accuracy = sum(
        1 for seq in oracle_routes
        if learned_routes.get(seq) == oracle_routes[seq]
    ) / max(len(oracle_routes), 1)

    cross_domain: Dict[str, object] = {
        "eth3d_n_sequences": base["n_sequences"],
        "eth3d_learned_router_counts": learned_counts,
        "eth3d_oracle_router_counts": oracle_counts,
        "eth3d_route_accuracy_vs_oracle": float(eth3d_route_accuracy),
        "eth3d_best_single_expert": base["best_single_expert"],
        "eth3d_relative_improvement_vs_best_single": float(
            base["relative_improvement_vs_best_single"]
        ),
    }

    if kitti_oracle_labels:
        kitti_data = json.loads(Path(kitti_oracle_labels).read_text(encoding="utf-8"))
        kitti_oracle_counts = dict(kitti_data.get("summary", {}).get("oracle_counts", {}))
        kitti_metrics = kitti_data.get("metrics") or {}
        kitti_singles: Dict[str, float] = {}
        for name in expert_order:
            vals = [
                float(m[name]) for m in kitti_metrics.values()
                if name in m and m[name] != float("inf")
            ]
            kitti_singles[name] = sum(vals) / len(vals) if vals else float("inf")
        kitti_best = (
            min(kitti_singles, key=kitti_singles.get) if kitti_singles else None
        )
        cross_domain["kitti_oracle_counts"] = kitti_oracle_counts
        cross_domain["kitti_per_expert_mean_abs_rel"] = kitti_singles
        cross_domain["kitti_best_single_expert"] = kitti_best
        cross_domain["best_single_shifted_kitti_to_eth3d"] = (
            kitti_best != base["best_single_expert"]
        )

    base["cross_domain"] = cross_domain

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(base, indent=2), encoding="utf-8")
    return base


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--oracle-labels",
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json",
    )
    parser.add_argument(
        "--router-checkpoint",
        default="/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_router/results.json",
    )
    parser.add_argument(
        "--kitti-oracle-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json",
    )
    parser.add_argument(
        "--feature-mode",
        choices=["regime", "regime_stats", "regime_stats_robust"],
        default="regime_stats",
    )
    args = parser.parse_args()

    result = evaluate_cross_domain(
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        router_checkpoint=args.router_checkpoint,
        output=args.output,
        kitti_oracle_labels=args.kitti_oracle_labels,
        feature_mode=args.feature_mode,
    )
    print(json.dumps({
        "n_sequences": result["n_sequences"],
        "metrics": result["metrics"],
        "best_single_expert": result["best_single_expert"],
        "relative_improvement_vs_best_single": result["relative_improvement_vs_best_single"],
        "learned_expert_counts": result["learned_expert_counts"],
        "oracle_expert_counts": result["oracle_expert_counts"],
        "cross_domain": result["cross_domain"],
    }, indent=2))


if __name__ == "__main__":
    main()
