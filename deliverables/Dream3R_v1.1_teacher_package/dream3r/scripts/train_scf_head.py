"""Train the state-conditioned multi-expert fusion head from proposal caches.

Loads all-expert proposal caches (``build_scf_cache``), trains ``SCFHead``
with a held-out scale-aligned abs_rel loss, and reports per domain:

    B_<expert>   per-expert baselines (always_fast3r / mast3r / spann3r)
    B_oracle     best-per-window lower bound (B4)
    B_patch_oracle  best-per-valid-point lower bound (diagnostic only)
    Ours_SCF     SCF convex fusion
    rel_imp_vs_best_single_pp   (best_single - ours) / best_single * 100
    oracle_gap_pp               (ours - oracle) / oracle * 100
    patch_oracle_gap_pp         (ours - patch_oracle) / patch_oracle * 100
    Ours_temporal_delta_abs_rel adjacent-frame depth-change error proxy
    Ours_scale_drift_proxy      per-frame median-scale drift proxy

Ablations are selected via flags: ``--no-state`` zeroes memory context;
``--shuffle-state`` feeds each window another window's memory context;
``--residual`` enables the gated residual correction on top of fusion.

The script also evaluates single-expert and oracle references using the same
per-domain split and AbsRel implementation as the fusion training pipeline.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch

from dream3r.scf_head import SCFHead
from dream3r.training_utils import (
    abs_rel_loss as _abs_rel_loss,
    pointmap_abs_rel as _pointmap_abs_rel,
    stratified_split as _stratified_split,
)


def _load_caches(paths: List[str]) -> Tuple[List[Dict], int, List[str]]:
    entries: List[Dict] = []
    d_memory: Optional[int] = None
    expert_order: Optional[List[str]] = None
    for p in paths:
        blob = torch.load(p, map_location="cpu", weights_only=False)
        entries.extend(blob["entries"])
        if blob.get("d_memory") is not None and d_memory is None:
            d_memory = int(blob["d_memory"])
        if expert_order is None:
            expert_order = list(blob["expert_order"])
        elif expert_order != list(blob["expert_order"]):
            raise ValueError(f"expert_order mismatch across caches: {expert_order} vs {blob['expert_order']}")
    if d_memory is None:
        raise ValueError("none of the caches recorded d_memory")
    return entries, d_memory, expert_order


def _build_state_source(entries: List[Dict], seed: int, shuffle_state: bool) -> List[Dict]:
    """Return per-entry state source; shuffled within domain for a negative control."""
    if not shuffle_state:
        return entries

    state_source = list(entries)
    rng = random.Random(seed + 1009)
    by_domain: Dict[str, List[int]] = {}
    for i, e in enumerate(entries):
        by_domain.setdefault(e["domain"], []).append(i)

    for idxs in by_domain.values():
        src = list(idxs)
        rng.shuffle(src)
        if len(src) > 1 and all(a == b for a, b in zip(idxs, src)):
            src = src[1:] + src[:1]
        for dst_i, src_i in zip(idxs, src):
            state_source[dst_i] = entries[src_i]
    return state_source


def _stack(entry: Dict, expert_order: List[str], device: torch.device,
           state_entry: Optional[Dict] = None):
    pms = torch.stack([entry["proposals"][n]["pointmap"] for n in expert_order], dim=0) \
        .unsqueeze(0).to(device)        # [1, E, N, P, 3]
    cfs = torch.stack([entry["proposals"][n]["confidence"] for n in expert_order], dim=0) \
        .unsqueeze(0).to(device)        # [1, E, N, P, 1]
    state_entry = state_entry or entry
    mc = state_entry["memory_context"].unsqueeze(0).to(device) \
        if state_entry["memory_context"] is not None else None
    cs = torch.tensor([[entry["conflict_score"]]], device=device)
    gt = entry["gt_pointmap"].unsqueeze(0).to(device)
    mask = entry["gt_mask"].unsqueeze(0).to(device)
    return pms, cfs, mc, cs, gt, mask


def _aligned_depth(pred: torch.Tensor, target: torch.Tensor,
                   mask: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return globally scale-aligned pred depth plus target depth and valid mask."""
    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (target_depth.abs() > 1e-6)
    )
    if bool(valid.any()):
        denom = pred_depth[valid].median()
        denom = torch.where(denom.abs() > 1e-6, denom, denom.new_tensor(1e-6))
        pred_depth = pred_depth * (target_depth[valid].median() / denom)
    return pred_depth, target_depth, valid


def _per_patch_oracle_abs_rel(proposals: torch.Tensor, target: torch.Tensor,
                              mask: torch.Tensor) -> float:
    """Best expert per valid point after each expert's global scale alignment."""
    rel_maps: List[torch.Tensor] = []
    valid_any: Optional[torch.Tensor] = None
    for k in range(proposals.shape[1]):
        pred_depth, target_depth, valid = _aligned_depth(proposals[:, k], target, mask)
        rel = (pred_depth - target_depth).abs() / target_depth.abs().clamp_min(1e-6)
        rel = torch.where(valid, rel, torch.full_like(rel, float("inf")))
        rel_maps.append(rel)
        valid_any = valid if valid_any is None else (valid_any | valid)
    if valid_any is None or not bool(valid_any.any()):
        return float("inf")
    best = torch.stack(rel_maps, dim=0).min(dim=0).values
    finite = valid_any & torch.isfinite(best)
    if not bool(finite.any()):
        return float("inf")
    return float(best[finite].mean().item())


def _temporal_delta_abs_rel(pred: torch.Tensor, target: torch.Tensor,
                            mask: torch.Tensor) -> float:
    """Adjacent-frame depth-change error; lower is more temporally coherent."""
    pred_depth, target_depth, valid = _aligned_depth(pred, target, mask)
    if pred_depth.shape[1] < 2:
        return 0.0
    pair_valid = valid[:, 1:] & valid[:, :-1]
    if not bool(pair_valid.any()):
        return float("inf")
    pred_delta = pred_depth[:, 1:] - pred_depth[:, :-1]
    target_delta = target_depth[:, 1:] - target_depth[:, :-1]
    denom = target_depth[:, 1:].abs().clamp_min(1e-6)
    rel = (pred_delta - target_delta).abs() / denom
    return float(rel[pair_valid].mean().item())


def _scale_drift_proxy(pred: torch.Tensor, target: torch.Tensor,
                       mask: torch.Tensor) -> float:
    """Stddev of per-frame log scale ratios; lower means less scale drift."""
    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (pred_depth.abs() > 1e-6)
        & (target_depth.abs() > 1e-6)
    )
    values: List[torch.Tensor] = []
    for b in range(pred_depth.shape[0]):
        frame_logs: List[torch.Tensor] = []
        for n in range(pred_depth.shape[1]):
            v = valid[b, n]
            if bool(v.any()):
                denom = pred_depth[b, n][v].median()
                denom = torch.where(denom.abs() > 1e-6, denom, denom.new_tensor(1e-6))
                scale = target_depth[b, n][v].median() / denom
                frame_logs.append(torch.log(scale.abs().clamp_min(1e-6)))
        if len(frame_logs) >= 2:
            logs = torch.stack(frame_logs)
            values.append(logs.std(unbiased=False))
    if not values:
        return 0.0
    return float(torch.stack(values).mean().item())


def _eval(entries: List[Dict], idxs: List[int], head: SCFHead,
          state_entries: List[Dict],
          expert_order: List[str], device: torch.device) -> Dict[str, Dict[str, float]]:
    head.eval()
    n_exp = len(expert_order)
    sums: Dict[str, Dict] = {}
    with torch.no_grad():
        for i in idxs:
            e = entries[i]
            dom = e["domain"]
            pms, cfs, mc, cs, gt, mask = _stack(e, expert_order, device, state_entries[i])
            per_expert = [_pointmap_abs_rel(pms[:, k], gt, mask, align_scale=True)
                          for k in range(n_exp)]
            oracle = min(per_expert)
            patch_oracle = _per_patch_oracle_abs_rel(pms, gt, mask)
            out = head(pms, cfs, mc, cs)
            ours = _pointmap_abs_rel(out["final_pointmap"], gt, mask, align_scale=True)
            temporal = _temporal_delta_abs_rel(out["final_pointmap"], gt, mask)
            scale_drift = _scale_drift_proxy(out["final_pointmap"], gt, mask)
            s = sums.setdefault(dom, {
                "per_expert": [0.0] * n_exp,
                "oracle": 0.0,
                "patch_oracle": 0.0,
                "ours": 0.0,
                "temporal": 0.0,
                "scale_drift": 0.0,
                "n": 0,
            })
            for k in range(n_exp):
                s["per_expert"][k] += per_expert[k]
            s["oracle"] += oracle
            s["patch_oracle"] += patch_oracle
            s["ours"] += ours
            s["temporal"] += temporal
            s["scale_drift"] += scale_drift
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
            "Ours_SCF": round(ours, 4),
            "best_single": round(best_single, 4),
            "rel_imp_vs_best_single_pp": round((best_single - ours) / max(best_single, 1e-9) * 100, 2),
            "oracle_gap_pp": round((ours - oracle) / max(oracle, 1e-9) * 100, 2),
            "patch_oracle_gap_pp": round((ours - patch_oracle) / max(patch_oracle, 1e-9) * 100, 2),
            "Ours_temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "Ours_scale_drift_proxy": round(s["scale_drift"] / n, 4),
        }
    return res


def train(cache_paths: List[str], output_dir: str, seed: int = 7, epochs: int = 300,
          lr: float = 1e-3, head_dim: int = 64, hidden: int = 128,
          holdout_frac: float = 0.2, use_state: bool = True, use_residual: bool = False,
          shuffle_state: bool = False):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    entries, d_memory, expert_order = _load_caches(cache_paths)
    state_entries = _build_state_source(entries, seed, shuffle_state)
    n_exp = len(expert_order)
    print(f"loaded {len(entries)} entries, d_memory={d_memory}, experts={expert_order}", flush=True)

    head = SCFHead(n_experts=n_exp, d_memory=d_memory, head_dim=head_dim, hidden=hidden,
                   use_state=use_state, use_residual=use_residual).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=lr)

    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    print(f"split: train={len(train_idx)} test={len(test_idx)} "
          f"use_state={use_state} shuffle_state={shuffle_state} "
          f"use_residual={use_residual} (seed={seed})", flush=True)

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        epoch_loss, nb = 0.0, 0
        for i in order:
            e = entries[i]
            pms, cfs, mc, cs, gt, mask = _stack(e, expert_order, device, state_entries[i])
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
        "head_state_dict": head.state_dict(),
        "config": {"n_experts": n_exp, "d_memory": d_memory, "head_dim": head_dim,
                   "hidden": hidden, "use_state": use_state,
                   "use_residual": use_residual, "shuffle_state": shuffle_state},
        "seed": seed, "final_eval": final_eval, "loss_curve": losses,
    }, out_path / "latest.pt")

    result = {
        "seed": seed, "epochs": epochs, "n_train": len(train_idx), "n_test": len(test_idx),
        "expert_order": expert_order, "use_state": use_state,
        "shuffle_state": shuffle_state, "use_residual": use_residual,
        "final_train_loss": losses[-1] if losses else None,
        "loss_decrease_pct": (losses[0] - losses[-1]) / max(losses[0], 1e-9) * 100 if len(losses) >= 2 else 0.0,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved SCF head + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", nargs="+", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--head-dim", type=int, default=64)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--holdout-frac", type=float, default=0.2)
    ap.add_argument("--no-state", action="store_true", help="ablation: zero memory context")
    ap.add_argument("--shuffle-state", action="store_true",
                    help="ablation: feed same-domain memory context from a different window")
    ap.add_argument("--residual", action="store_true", help="ablation: enable gated residual")
    a = ap.parse_args()
    train(a.cache, a.output_dir, a.seed, a.epochs, a.lr, a.head_dim, a.hidden,
          a.holdout_frac, use_state=not a.no_state, use_residual=a.residual,
          shuffle_state=a.shuffle_state)


if __name__ == "__main__":
    main()
