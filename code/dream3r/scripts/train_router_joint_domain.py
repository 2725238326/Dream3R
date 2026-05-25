"""Joint KITTI+ETH3D router training with a 2D domain-id feature.

Concatenates KITTI 59w + ETH3D 50w (109 examples). Feature vector per
example:

  [6 regime probs] + [4 robust stats normalized over joint set] + [2 domain]

Domain id is `[1, 0]` for KITTI examples and `[0, 1]` for ETH3D examples.

The four "robust" stats (frame_count, depth_mean, valid_ratio,
depth_temporal_change) are normalized with mean/std computed over the
joint 109-example set so that the domain-id one-hot is the only
explicit domain signal at training time.

A fold-restricted training mode (``--sequence-filter-file``) is provided
for LOO eval.
"""

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.config import load_config, save_config
from dream3r.modules import ComposerRouter
from dream3r.scripts.train_router_only import (
    STAT_FEATURE_KEYS_ROBUST,
    _expert_registry,
    _accuracy,
)


def _load_joint_examples(
    kitti_regime: str,
    kitti_oracle: str,
    eth3d_regime: str,
    eth3d_oracle: str,
    sequence_filter: Optional[List[str]] = None,
    frozen_stats: Optional[Dict[str, object]] = None,
    per_domain_norm: bool = False,
    frozen_per_domain_stats: Optional[Dict[str, Dict[str, object]]] = None,
) -> Tuple[torch.Tensor, torch.Tensor, List[str], List[str], List[str], Dict[str, object]]:
    """Return joint (x, y, sequences, domain_ids, expert_order, feature_meta).

    Both KITTI and ETH3D oracles must share the same `expert_order`.

    When ``per_domain_norm`` is True, the 4 robust stats are normalized
    per domain (KITTI rows use KITTI's own mean/std; ETH3D rows use
    ETH3D's). At fold-eval time, pass ``frozen_per_domain_stats =
    {"kitti": {...}, "eth3d": {...}}`` to use the training-fold stats.
    """
    k_reg = json.loads(Path(kitti_regime).read_text(encoding="utf-8"))
    k_ora = json.loads(Path(kitti_oracle).read_text(encoding="utf-8"))
    e_reg = json.loads(Path(eth3d_regime).read_text(encoding="utf-8"))
    e_ora = json.loads(Path(eth3d_oracle).read_text(encoding="utf-8"))

    if k_ora["expert_order"] != e_ora["expert_order"]:
        raise ValueError(
            f"expert_order mismatch: kitti={k_ora['expert_order']}, "
            f"eth3d={e_ora['expert_order']}"
        )
    expert_order = k_ora["expert_order"]

    def _stats_dict(reg: Dict[str, object]) -> Dict[str, Dict[str, float]]:
        s = reg.get("stats")
        if not isinstance(s, dict):
            s = reg.get("features")
        if not isinstance(s, dict):
            raise ValueError("regime data missing stats/features")
        return s

    k_stats = _stats_dict(k_reg)
    e_stats = _stats_dict(e_reg)

    rows: List[List[float]] = []
    labels: List[int] = []
    seqs: List[str] = []
    domains: List[str] = []

    def _push(domain: str, regime_data, oracle_data, stats_data):
        for seq in sorted(oracle_data["labels"]):
            if seq not in regime_data["labels"]:
                continue
            if seq not in stats_data:
                continue
            if sequence_filter is not None and seq not in sequence_filter:
                continue
            regime_vec = [float(v) for v in regime_data["labels"][seq]]
            stat_vec = [
                float(stats_data[seq].get(key, 0.0))
                for key in STAT_FEATURE_KEYS_ROBUST
            ]
            domain_vec = [1.0, 0.0] if domain == "kitti" else [0.0, 1.0]
            rows.append(regime_vec + stat_vec + domain_vec)
            labels.append(int(oracle_data["labels"][seq]))
            seqs.append(seq)
            domains.append(domain)

    _push("kitti", k_reg, k_ora, k_stats)
    _push("eth3d", e_reg, e_ora, e_stats)
    if not rows:
        raise ValueError("no joint examples assembled")

    raw = torch.tensor(rows, dtype=torch.float32)
    regime_width = len(rows[0]) - len(STAT_FEATURE_KEYS_ROBUST) - 2
    stat_slice = slice(regime_width, regime_width + len(STAT_FEATURE_KEYS_ROBUST))
    stats = raw[:, stat_slice]
    domain_tensor = torch.tensor(
        [0 if d == "kitti" else 1 for d in domains], dtype=torch.long
    )

    if per_domain_norm:
        # Per-domain mean/std: KITTI rows normalized by KITTI stats, ETH3D
        # rows by ETH3D stats. At eval time, frozen_per_domain_stats holds
        # both domains' frozen mean/std from the training fold.
        per_domain_meta: Dict[str, Dict[str, List[float]]] = {}
        for domain_idx, domain_name in enumerate(("kitti", "eth3d")):
            mask = domain_tensor == domain_idx
            if mask.sum() == 0:
                # No rows for this domain in the current call (e.g., LOO
                # eval on a single held-out KITTI sample). Skip — frozen
                # stats for the absent domain still recorded if passed.
                if frozen_per_domain_stats is not None and domain_name in frozen_per_domain_stats:
                    fs = frozen_per_domain_stats[domain_name]
                    per_domain_meta[domain_name] = {
                        "stat_mean": list(fs["stat_mean"]),
                        "stat_std": list(fs["stat_std"]),
                    }
                continue
            sub = stats[mask]
            if frozen_per_domain_stats is not None and domain_name in frozen_per_domain_stats:
                fs = frozen_per_domain_stats[domain_name]
                d_mean = torch.tensor(fs["stat_mean"], dtype=torch.float32).unsqueeze(0)
                d_std = torch.tensor(fs["stat_std"], dtype=torch.float32).unsqueeze(0).clamp_min(1e-6)
            else:
                d_mean = sub.mean(dim=0, keepdim=True)
                d_std = sub.std(dim=0, keepdim=True, unbiased=False).clamp_min(1e-6)
            stats[mask] = (sub - d_mean) / d_std
            per_domain_meta[domain_name] = {
                "stat_mean": [float(v) for v in d_mean.squeeze(0).tolist()],
                "stat_std": [float(v) for v in d_std.squeeze(0).tolist()],
            }
        raw[:, stat_slice] = stats
        stats_frozen = frozen_per_domain_stats is not None
        feature_mode_name = "regime_stats_robust_joint_per_domain"
        feature_meta = {
            "feature_mode": feature_mode_name,
            "regime_width": int(regime_width),
            "stat_keys": list(STAT_FEATURE_KEYS_ROBUST),
            "per_domain_stats": per_domain_meta,
            "stats_frozen": stats_frozen,
            "domain_width": 2,
            "domain_order": ["kitti", "eth3d"],
        }
    else:
        if frozen_stats is not None:
            mean = torch.tensor(frozen_stats["stat_mean"], dtype=torch.float32).unsqueeze(0)
            std = torch.tensor(frozen_stats["stat_std"], dtype=torch.float32).unsqueeze(0).clamp_min(1e-6)
            stats_frozen = True
        else:
            mean = stats.mean(dim=0, keepdim=True)
            std = stats.std(dim=0, keepdim=True, unbiased=False).clamp_min(1e-6)
            stats_frozen = False
        raw[:, stat_slice] = (stats - mean) / std

        feature_meta = {
            "feature_mode": "regime_stats_robust_joint",
            "regime_width": int(regime_width),
            "stat_keys": list(STAT_FEATURE_KEYS_ROBUST),
            "stat_mean": [float(v) for v in mean.squeeze(0).tolist()],
            "stat_std": [float(v) for v in std.squeeze(0).tolist()],
            "stats_frozen": stats_frozen,
            "domain_width": 2,
            "domain_order": ["kitti", "eth3d"],
        }
    y = torch.tensor(labels, dtype=torch.long)
    return raw, y, seqs, domains, expert_order, feature_meta


def train_router_joint(
    kitti_regime: str,
    kitti_oracle: str,
    eth3d_regime: str,
    eth3d_oracle: str,
    output_dir: str,
    epochs: int = 2000,
    lr: float = 0.05,
    batch_size: int = 32,
    d_routing: int = 32,
    seed: int = 7,
    sequence_filter: Optional[List[str]] = None,
    per_domain_norm: bool = False,
) -> Dict[str, object]:
    torch.manual_seed(seed)
    x, y, seqs, domains, expert_order, feature_meta = _load_joint_examples(
        kitti_regime, kitti_oracle, eth3d_regime, eth3d_oracle,
        sequence_filter=sequence_filter,
        per_domain_norm=per_domain_norm,
    )
    registry = _expert_registry(expert_order)
    router = ComposerRouter(
        n_regimes=x.shape[1],
        d_routing=d_routing,
        cost_alpha=0.0,
        expert_registry=registry,
    )
    router.capability_cards.zero_()
    router.latency_costs.zero_()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    optimizer = torch.optim.AdamW(router.parameters(), lr=lr, weight_decay=1e-4)
    with torch.no_grad():
        initial_acc = _accuracy(router(x)["routing_logits"], y)

    n = x.shape[0]
    for epoch in range(epochs):
        perm = torch.randperm(n)
        for start in range(0, n, batch_size):
            idx = perm[start:start + batch_size]
            out = router(x[idx])
            loss = F.cross_entropy(out["routing_logits"], y[idx])
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

    with torch.no_grad():
        final_logits = router(x)["routing_logits"]
        final_acc = _accuracy(final_logits, y)
        predictions = final_logits.argmax(dim=-1).tolist()

    # Per-domain closure accuracy
    per_domain_acc: Dict[str, float] = {}
    per_domain_counts: Dict[str, Dict[str, int]] = {}
    for domain in set(domains):
        mask = [i for i, d in enumerate(domains) if d == domain]
        if not mask:
            continue
        d_preds = [predictions[i] for i in mask]
        d_targets = [int(y[i].item()) for i in mask]
        per_domain_acc[domain] = float(
            sum(int(p == t) for p, t in zip(d_preds, d_targets)) / len(mask)
        )
        per_domain_counts[domain] = {
            "target": dict(Counter(d_targets)),
            "predicted": dict(Counter(d_preds)),
        }

    summary = {
        "n_examples": n,
        "expert_order": expert_order,
        "initial_accuracy": initial_acc,
        "final_accuracy": final_acc,
        "target_counts": dict(Counter(y.tolist())),
        "prediction_counts": dict(Counter(predictions)),
        "sequences": seqs,
        "domains": domains,
        "per_domain_accuracy": per_domain_acc,
        "per_domain_counts": per_domain_counts,
        "feature_mode": feature_meta["feature_mode"],
        "feature_meta": feature_meta,
        "per_domain_norm": bool(per_domain_norm),
    }
    torch.save({
        "router_state_dict": router.state_dict(),
        "expert_order": expert_order,
        "summary": summary,
    }, output_path / "latest.pt")
    (output_path / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", default="router_only")
    parser.add_argument("--kitti-regime", required=True)
    parser.add_argument("--kitti-oracle", required=True)
    parser.add_argument("--eth3d-regime", required=True)
    parser.add_argument("--eth3d-oracle", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--epochs", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=0.05)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--d-routing", type=int, default=32)
    parser.add_argument("--per-domain-norm", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = train_router_joint(
        kitti_regime=args.kitti_regime,
        kitti_oracle=args.kitti_oracle,
        eth3d_regime=args.eth3d_regime,
        eth3d_oracle=args.eth3d_oracle,
        output_dir=str(out_dir),
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        d_routing=args.d_routing,
        per_domain_norm=args.per_domain_norm,
    )
    print(json.dumps({
        k: v for k, v in summary.items()
        if k not in ("sequences", "domains")
    }, indent=2))


if __name__ == "__main__":
    main()
