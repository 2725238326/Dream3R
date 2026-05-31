"""Train/evaluate a Dream-state-only expert prior over cached proposals."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.train_fusion_head import _abs_rel_loss, _stratified_split
from dream3r.scripts.train_scf_head import (
    _build_state_source,
    _load_caches,
    _per_patch_oracle_abs_rel,
    _scale_drift_proxy,
    _stack,
    _temporal_delta_abs_rel,
)
from dream3r.state_prior_head import StatePriorHead


def _eval(
    entries: List[Dict],
    idxs: List[int],
    head: StatePriorHead,
    state_entries: List[Dict],
    expert_order: List[str],
    device: torch.device,
) -> Dict[str, Dict[str, float]]:
    head.eval()
    n_exp = len(expert_order)
    sums: Dict[str, Dict] = {}
    with torch.no_grad():
        for i in idxs:
            entry = entries[i]
            dom = entry["domain"]
            pms, cfs, mc, cs, gt, mask = _stack(entry, expert_order, device, state_entries[i])
            per_expert = [
                _pointmap_abs_rel(pms[:, k], gt, mask, align_scale=True)
                for k in range(n_exp)
            ]
            oracle = min(per_expert)
            patch_oracle = _per_patch_oracle_abs_rel(pms, gt, mask)
            out = head(pms, cfs, mc, cs)
            ours = _pointmap_abs_rel(out["final_pointmap"], gt, mask, align_scale=True)
            temporal = _temporal_delta_abs_rel(out["final_pointmap"], gt, mask)
            scale_drift = _scale_drift_proxy(out["final_pointmap"], gt, mask)
            entropy = float(
                -(
                    out["expert_weights"].clamp_min(1e-8)
                    * out["expert_weights"].clamp_min(1e-8).log()
                ).sum(dim=1).mean().item()
            )

            s = sums.setdefault(dom, {
                "per_expert": [0.0] * n_exp,
                "oracle": 0.0,
                "patch_oracle": 0.0,
                "ours": 0.0,
                "temporal": 0.0,
                "scale_drift": 0.0,
                "entropy": 0.0,
                "n": 0,
            })
            for k in range(n_exp):
                s["per_expert"][k] += per_expert[k]
            s["oracle"] += oracle
            s["patch_oracle"] += patch_oracle
            s["ours"] += ours
            s["temporal"] += temporal
            s["scale_drift"] += scale_drift
            s["entropy"] += entropy
            s["n"] += 1

    head.train()
    res: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1, s["n"])
        pe = [v / n for v in s["per_expert"]]
        oracle = s["oracle"] / n
        patch_oracle = s["patch_oracle"] / n
        ours = s["ours"] / n
        best_single = min(pe)
        res[dom] = {
            "n": s["n"],
            **{f"B_{expert_order[k]}": round(pe[k], 4) for k in range(n_exp)},
            "B_oracle": round(oracle, 4),
            "B_patch_oracle": round(patch_oracle, 4),
            "Ours_StatePrior": round(ours, 4),
            "best_single": round(best_single, 4),
            "rel_imp_vs_best_single_pp": round((best_single - ours) / max(best_single, 1e-9) * 100, 2),
            "oracle_gap_pp": round((ours - oracle) / max(oracle, 1e-9) * 100, 2),
            "patch_oracle_gap_pp": round((ours - patch_oracle) / max(patch_oracle, 1e-9) * 100, 2),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale_drift"] / n, 4),
            "mean_weight_entropy": round(s["entropy"] / n, 4),
        }
    return res


def train(
    cache_paths: List[str],
    output_dir: str,
    seed: int = 7,
    epochs: int = 300,
    lr: float = 1e-3,
    state_dim: int = 64,
    hidden: int = 128,
    holdout_frac: float = 0.2,
    use_state: bool = True,
    shuffle_state: bool = False,
):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    entries, d_memory, expert_order = _load_caches(cache_paths)
    state_entries = _build_state_source(entries, seed, shuffle_state)
    n_exp = len(expert_order)
    print(f"loaded {len(entries)} entries, d_memory={d_memory}, experts={expert_order}", flush=True)

    head = StatePriorHead(
        n_experts=n_exp,
        d_memory=d_memory,
        state_dim=state_dim,
        hidden=hidden,
        use_state=use_state,
    ).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=lr)

    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    print(
        f"split: train={len(train_idx)} test={len(test_idx)} "
        f"use_state={use_state} shuffle_state={shuffle_state} seed={seed}",
        flush=True,
    )

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        epoch_loss, nb = 0.0, 0
        for i in order:
            pms, cfs, mc, cs, gt, mask = _stack(entries[i], expert_order, device, state_entries[i])
            out = head(pms, cfs, mc, cs)
            loss = _abs_rel_loss(out["final_pointmap"], gt, mask, align_scale=True)
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss)
            nb += 1
        losses.append(epoch_loss / max(1, nb))
        if (epoch + 1) % 50 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, head, state_entries, expert_order, device)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_eval = _eval(entries, test_idx, head, state_entries, expert_order, device)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "state_dict": head.state_dict(),
        "config": {
            "n_experts": n_exp,
            "d_memory": d_memory,
            "state_dim": state_dim,
            "hidden": hidden,
            "use_state": use_state,
            "shuffle_state": shuffle_state,
        },
        "seed": seed,
        "final_eval": final_eval,
        "loss_curve": losses,
    }, out_path / "latest.pt")

    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "expert_order": expert_order,
        "use_state": use_state,
        "shuffle_state": shuffle_state,
        "final_train_loss": losses[-1] if losses else None,
        "loss_decrease_pct": (losses[0] - losses[-1]) / max(losses[0], 1e-9) * 100
        if len(losses) >= 2 else 0.0,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved StatePriorHead + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--state-dim", type=int, default=64)
    parser.add_argument("--hidden", type=int, default=128)
    parser.add_argument("--holdout-frac", type=float, default=0.2)
    parser.add_argument("--no-state", action="store_true")
    parser.add_argument("--shuffle-state", action="store_true")
    args = parser.parse_args()
    train(
        args.cache,
        args.output_dir,
        seed=args.seed,
        epochs=args.epochs,
        lr=args.lr,
        state_dim=args.state_dim,
        hidden=args.hidden,
        holdout_frac=args.holdout_frac,
        use_state=not args.no_state,
        shuffle_state=args.shuffle_state,
    )


if __name__ == "__main__":
    main()
