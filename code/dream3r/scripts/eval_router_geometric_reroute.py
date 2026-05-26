"""Phase B+C: Geometric reroute closed-loop eval.

At inference, route via the trained joint router, then look up cached
geometric_log (sampson_distance / depth_inconsistency) for the router's
top-2 expert picks. If the top-1's geometric signal is materially worse
than the top-2's, reroute. Otherwise keep top-1.

This is the "Critic -> Router feedback" closed loop in the spirit of
Stage 4 -> Stage 5, but using deterministic geometric features instead
of the trained-Critic conflict head (which DEC-007 follow-up showed
does not generalize beyond the 12-seq KITTI training set).

Usage: provide a router checkpoint trained on joint KITTI+ETH3D windows
plus per-domain critic caches. Evaluate aggregate abs_rel:
  (a) without reroute
  (b) with geometric reroute (sampson margin tuned via CLI)
  (c) oracle upper bound (always pick best expert per window)
"""

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.modules import ComposerRouter
from dream3r.scripts.train_router_only import (
    STAT_FEATURE_KEYS,
    STAT_FEATURE_KEYS_ROBUST,
    _expert_registry,
)


def _features_from_meta(domain: str, x_row: torch.Tensor, meta: Dict[str, object],
                        per_domain_stats: Optional[Dict[str, Dict[str, List[float]]]]) -> torch.Tensor:
    """Apply per-domain stat normalization to a single row at eval time."""
    if per_domain_stats is None:
        return x_row
    if domain not in per_domain_stats:
        return x_row
    stats = per_domain_stats[domain]
    regime_width = int(meta["regime_width"])
    n_stats = len(STAT_FEATURE_KEYS_ROBUST)
    stat_slice = slice(regime_width, regime_width + n_stats)
    out = x_row.clone()
    mean = torch.tensor(stats["stat_mean"], dtype=torch.float32)
    std = torch.tensor(stats["stat_std"], dtype=torch.float32).clamp_min(1e-6)
    out[stat_slice] = (out[stat_slice] - mean) / std
    return out


def _load_joint_router(ckpt_path: str) -> Tuple[ComposerRouter, List[str], Dict[str, object]]:
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    summary = ckpt["summary"]
    expert_order = summary["expert_order"]
    feature_meta = summary["feature_meta"]
    n_regimes = int(feature_meta["regime_width"]) + \
                len(STAT_FEATURE_KEYS_ROBUST) + \
                int(feature_meta["domain_width"])
    registry = _expert_registry(expert_order)
    d_routing = int(ckpt["router_state_dict"]["regime_encoder.0.weight"].shape[0])
    router = ComposerRouter(
        n_regimes=n_regimes,
        d_routing=d_routing,
        cost_alpha=0.0,
        expert_registry=registry,
    )
    router.capability_cards.zero_()
    router.latency_costs.zero_()
    router.load_state_dict(ckpt["router_state_dict"])
    router.eval()
    return router, expert_order, feature_meta


def _build_x_for(domain: str, seq: str, regime_row: List[float], stats_row: Dict[str, float],
                 expert_order: List[str], feature_meta: Dict[str, object]) -> torch.Tensor:
    regime_vec = [float(v) for v in regime_row]
    stat_vec = [float(stats_row.get(k, 0.0)) for k in STAT_FEATURE_KEYS_ROBUST]
    domain_vec = [1.0, 0.0] if domain == "kitti" else [0.0, 1.0]
    x = torch.tensor(regime_vec + stat_vec + domain_vec, dtype=torch.float32)
    return _features_from_meta(domain, x, feature_meta, feature_meta.get("per_domain_stats"))


def _stats_for(regime_data: Dict[str, object], seq: str) -> Dict[str, float]:
    s = regime_data.get("stats") or regime_data.get("features") or {}
    return s.get(seq, {})


def evaluate_geometric_reroute(
    router_checkpoint: str,
    kitti_regime: str,
    kitti_oracle: str,
    kitti_critic_cache: str,
    eth3d_regime: str,
    eth3d_oracle: str,
    eth3d_critic_cache: str,
    geometric_signal: str = "sampson_distance",
    margin: float = 0.02,
    output: str = "",
) -> Dict[str, object]:
    router, expert_order, feature_meta = _load_joint_router(router_checkpoint)
    k_reg = json.loads(Path(kitti_regime).read_text(encoding="utf-8"))
    k_ora = json.loads(Path(kitti_oracle).read_text(encoding="utf-8"))
    e_reg = json.loads(Path(eth3d_regime).read_text(encoding="utf-8"))
    e_ora = json.loads(Path(eth3d_oracle).read_text(encoding="utf-8"))
    k_crit = json.loads(Path(kitti_critic_cache).read_text(encoding="utf-8"))
    e_crit = json.loads(Path(eth3d_critic_cache).read_text(encoding="utf-8"))

    per_domain: Dict[str, Dict[str, List[float]]] = {
        "kitti": {"router_only": [], "reroute": [], "oracle": [], "best_single": {}},
        "eth3d": {"router_only": [], "reroute": [], "oracle": [], "best_single": {}},
    }
    per_window: List[Dict[str, object]] = []
    reroute_counts = {"kitti": 0, "eth3d": 0}

    for domain, regime_data, oracle_data, crit_cache in (
        ("kitti", k_reg, k_ora, k_crit),
        ("eth3d", e_reg, e_ora, e_crit),
    ):
        seqs = sorted(
            seq for seq in oracle_data["labels"]
            if seq in regime_data["labels"] and seq in crit_cache["labels"]
        )
        single_sums = {name: 0.0 for name in expert_order}
        n = len(seqs)
        for seq in seqs:
            regime_row = regime_data["labels"][seq]
            stats_row = _stats_for(regime_data, seq)
            x = _build_x_for(domain, seq, regime_row, stats_row, expert_order, feature_meta)
            with torch.no_grad():
                out = router(x.unsqueeze(0))
                logits = out["routing_logits"][0]
                ranking = logits.argsort(descending=True).tolist()
            top1 = expert_order[ranking[0]]
            top2 = expert_order[ranking[1]]
            metrics_seq = oracle_data["metrics"][seq]
            crit_seq = crit_cache["labels"][seq]
            geo_top1 = float(crit_seq[top1]["geometric_log"][geometric_signal])
            geo_top2 = float(crit_seq[top2]["geometric_log"][geometric_signal])
            router_pick = top1
            reroute_pick = top1
            applied_reroute = False
            if geo_top1 > geo_top2 + margin:
                reroute_pick = top2
                applied_reroute = True
                reroute_counts[domain] += 1
            router_metric = float(metrics_seq[router_pick])
            reroute_metric = float(metrics_seq[reroute_pick])
            oracle_pick = expert_order[int(oracle_data["labels"][seq])]
            oracle_metric = float(metrics_seq[oracle_pick])
            per_domain[domain]["router_only"].append(router_metric)
            per_domain[domain]["reroute"].append(reroute_metric)
            per_domain[domain]["oracle"].append(oracle_metric)
            for name in expert_order:
                single_sums[name] += float(metrics_seq[name])
            per_window.append({
                "domain": domain, "sequence": seq,
                "router_pick": router_pick, "reroute_pick": reroute_pick,
                "oracle_pick": oracle_pick,
                "router_metric": router_metric,
                "reroute_metric": reroute_metric,
                "oracle_metric": oracle_metric,
                f"{geometric_signal}_top1": geo_top1,
                f"{geometric_signal}_top2": geo_top2,
                "applied_reroute": applied_reroute,
            })
        per_domain[domain]["best_single"] = {
            name: single_sums[name] / n if n > 0 else 0.0
            for name in expert_order
        }
        per_domain[domain]["n"] = n

    summary: Dict[str, object] = {
        "router_checkpoint": router_checkpoint,
        "geometric_signal": geometric_signal,
        "margin": margin,
        "expert_order": expert_order,
        "per_domain": {},
        "per_window": per_window,
    }
    for domain in ("kitti", "eth3d"):
        n = per_domain[domain]["n"]
        if n == 0:
            continue
        router_mean = sum(per_domain[domain]["router_only"]) / n
        reroute_mean = sum(per_domain[domain]["reroute"]) / n
        oracle_mean = sum(per_domain[domain]["oracle"]) / n
        best_single_means = per_domain[domain]["best_single"]
        best_name = min(best_single_means, key=best_single_means.get)
        best_value = best_single_means[best_name]
        def _rel_imp(value: float) -> float:
            return (best_value - value) / best_value if best_value > 0 else 0.0
        summary["per_domain"][domain] = {
            "n_sequences": n,
            "router_only_mean": router_mean,
            "reroute_mean": reroute_mean,
            "oracle_mean": oracle_mean,
            "best_single_means": best_single_means,
            "best_single_expert": best_name,
            "router_only_rel_imp": _rel_imp(router_mean),
            "reroute_rel_imp": _rel_imp(reroute_mean),
            "oracle_rel_imp": _rel_imp(oracle_mean),
            "reroute_minus_router": reroute_mean - router_mean,
            "n_reroute_applied": reroute_counts[domain],
        }

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--router-checkpoint", required=True)
    parser.add_argument("--kitti-regime", required=True)
    parser.add_argument("--kitti-oracle", required=True)
    parser.add_argument("--kitti-critic-cache", required=True)
    parser.add_argument("--eth3d-regime", required=True)
    parser.add_argument("--eth3d-oracle", required=True)
    parser.add_argument("--eth3d-critic-cache", required=True)
    parser.add_argument(
        "--geometric-signal",
        choices=["sampson_distance", "depth_inconsistency", "confidence_disagreement", "covisible_inconsistency"],
        default="sampson_distance",
    )
    parser.add_argument("--margin", type=float, default=0.02)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    summary = evaluate_geometric_reroute(
        router_checkpoint=args.router_checkpoint,
        kitti_regime=args.kitti_regime,
        kitti_oracle=args.kitti_oracle,
        kitti_critic_cache=args.kitti_critic_cache,
        eth3d_regime=args.eth3d_regime,
        eth3d_oracle=args.eth3d_oracle,
        eth3d_critic_cache=args.eth3d_critic_cache,
        geometric_signal=args.geometric_signal,
        margin=args.margin,
        output=args.output,
    )
    out = {k: v for k, v in summary.items() if k != "per_window"}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
