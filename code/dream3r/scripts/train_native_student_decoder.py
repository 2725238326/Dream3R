"""Train Dream3R native student decoder from cached proposal banks.

This is the non-core execution gate for native decoder/distillation. It reuses
existing SCF caches, loads the DEC-019 StatePrior checkpoint as a frozen
teacher, applies proposal dropout during training, and reports the same
state-causality controls used by the bounded frozen-prior baseline.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn.functional as F

from dream3r.native_student_decoder import NativeStudentDecoder
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


def load_state_prior_checkpoint(
    student: NativeStudentDecoder,
    checkpoint_path: str,
    device: torch.device,
    freeze: bool = True,
) -> None:
    """Load DEC-019 StatePrior weights into the explicit teacher path."""

    ckpt = torch.load(checkpoint_path, map_location=device)
    student.state_prior.load_state_dict(ckpt["state_dict"])
    if freeze:
        student.freeze_state_prior()


def _masked_smooth_l1(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    valid = mask.bool().unsqueeze(-1).expand_as(pred)
    finite = valid & torch.isfinite(pred) & torch.isfinite(target)
    if not bool(finite.any()):
        return pred.new_tensor(0.0)
    return F.smooth_l1_loss(pred[finite], target.detach()[finite])


def _fallback_contamination_count(entries: List[Dict], expert_order: List[str]) -> int:
    count = 0
    for entry in entries:
        backends = entry.get("expert_backends") or {}
        for name in expert_order:
            value = backends.get(name)
            if value is not True:
                count += 1
    return count


def _eval(
    entries: List[Dict],
    idxs: List[int],
    student: NativeStudentDecoder,
    state_entries: List[Dict],
    expert_order: List[str],
    device: torch.device,
) -> Dict[str, Dict[str, float]]:
    student.eval()
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
            out = student(pms, cfs, mc, cs, proposal_dropout=0.0)
            ours = _pointmap_abs_rel(out["final_pointmap"], gt, mask, align_scale=True)
            teacher = _pointmap_abs_rel(out["teacher_pointmap"], gt, mask, align_scale=True)
            temporal = _temporal_delta_abs_rel(out["final_pointmap"], gt, mask)
            scale_drift = _scale_drift_proxy(out["final_pointmap"], gt, mask)
            teacher_temporal = _temporal_delta_abs_rel(out["teacher_pointmap"], gt, mask)
            teacher_scale = _scale_drift_proxy(out["teacher_pointmap"], gt, mask)
            residual = float(out["residual_delta"].norm(dim=-1).mean().item())
            entropy = float(
                -(
                    out["kept_prior_weights"].clamp_min(1e-8)
                    * out["kept_prior_weights"].clamp_min(1e-8).log()
                ).sum(dim=1).mean().item()
            )

            s = sums.setdefault(dom, {
                "per_expert": [0.0] * n_exp,
                "oracle": 0.0,
                "patch_oracle": 0.0,
                "ours": 0.0,
                "teacher": 0.0,
                "temporal": 0.0,
                "scale_drift": 0.0,
                "teacher_temporal": 0.0,
                "teacher_scale": 0.0,
                "residual": 0.0,
                "entropy": 0.0,
                "n": 0,
            })
            for k in range(n_exp):
                s["per_expert"][k] += per_expert[k]
            s["oracle"] += oracle
            s["patch_oracle"] += patch_oracle
            s["ours"] += ours
            s["teacher"] += teacher
            s["temporal"] += temporal
            s["scale_drift"] += scale_drift
            s["teacher_temporal"] += teacher_temporal
            s["teacher_scale"] += teacher_scale
            s["residual"] += residual
            s["entropy"] += entropy
            s["n"] += 1

    student.train()
    res: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1, s["n"])
        pe = [v / n for v in s["per_expert"]]
        oracle = s["oracle"] / n
        patch_oracle = s["patch_oracle"] / n
        ours = s["ours"] / n
        teacher = s["teacher"] / n
        best_single = min(pe)
        res[dom] = {
            "n": s["n"],
            **{f"B_{expert_order[k]}": round(pe[k], 4) for k in range(n_exp)},
            "B_oracle": round(oracle, 4),
            "B_patch_oracle": round(patch_oracle, 4),
            "Teacher_FrozenStatePrior": round(teacher, 4),
            "Ours_NativeStudent": round(ours, 4),
            "best_single": round(best_single, 4),
            "rel_imp_vs_best_single_pp": round((best_single - ours) / max(best_single, 1e-9) * 100, 2),
            "rel_imp_vs_teacher_pp": round((teacher - ours) / max(teacher, 1e-9) * 100, 2),
            "oracle_gap_pp": round((ours - oracle) / max(oracle, 1e-9) * 100, 2),
            "patch_oracle_gap_pp": round((ours - patch_oracle) / max(patch_oracle, 1e-9) * 100, 2),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale_drift"] / n, 4),
            "teacher_temporal_delta_abs_rel": round(s["teacher_temporal"] / n, 4),
            "teacher_scale_drift_proxy": round(s["teacher_scale"] / n, 4),
            "mean_residual_norm": round(s["residual"] / n, 6),
            "mean_prior_entropy": round(s["entropy"] / n, 4),
        }
    return res


def train(
    cache_paths: List[str],
    output_dir: str,
    state_prior_checkpoint: str,
    seed: int = 7,
    epochs: int = 50,
    lr: float = 5e-4,
    token_dim: int = 64,
    state_dim: int = 64,
    hidden: int = 128,
    num_layers: int = 2,
    num_heads: int = 4,
    prior_hidden: int = 128,
    residual_scale: float = 0.05,
    proposal_dropout: float = 0.35,
    distill_weight: float = 0.5,
    residual_l2_weight: float = 0.01,
    holdout_frac: float = 0.2,
    use_state: bool = True,
    shuffle_state: bool = False,
):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    entries, d_memory, expert_order = _load_caches(cache_paths)
    contamination = _fallback_contamination_count(entries, expert_order)
    if contamination:
        raise RuntimeError(f"fallback/stub proposal contamination detected: {contamination}")
    state_entries = _build_state_source(entries, seed, shuffle_state)
    n_exp = len(expert_order)
    print(
        f"loaded {len(entries)} entries, d_memory={d_memory}, experts={expert_order}, "
        f"fallback_contamination_count={contamination}",
        flush=True,
    )

    student = NativeStudentDecoder(
        n_experts=n_exp,
        d_memory=d_memory,
        token_dim=token_dim,
        state_dim=state_dim,
        hidden=hidden,
        num_layers=num_layers,
        num_heads=num_heads,
        use_state=use_state,
        prior_hidden=prior_hidden,
        residual_scale=residual_scale,
    ).to(device)
    load_state_prior_checkpoint(student, state_prior_checkpoint, device, freeze=True)
    print(
        f"loaded frozen StatePrior checkpoint={state_prior_checkpoint} "
        f"proposal_dropout={proposal_dropout} distill_weight={distill_weight}",
        flush=True,
    )

    opt = torch.optim.Adam((p for p in student.parameters() if p.requires_grad), lr=lr)
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
            out = student(pms, cfs, mc, cs, proposal_dropout=proposal_dropout)
            supervised = _abs_rel_loss(out["final_pointmap"], gt, mask, align_scale=True)
            distill = _masked_smooth_l1(out["final_pointmap"], out["teacher_pointmap"], mask)
            residual_l2 = out["residual_delta"].pow(2).mean()
            loss = supervised + distill_weight * distill + residual_l2_weight * residual_l2
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss)
            nb += 1
        losses.append(epoch_loss / max(1, nb))
        if (epoch + 1) % 10 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, student, state_entries, expert_order, device)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_eval = _eval(entries, test_idx, student, state_entries, expert_order, device)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "student_state_dict": student.state_dict(),
        "config": {
            "n_experts": n_exp,
            "d_memory": d_memory,
            "token_dim": token_dim,
            "state_dim": state_dim,
            "hidden": hidden,
            "num_layers": num_layers,
            "num_heads": num_heads,
            "use_state": use_state,
            "shuffle_state": shuffle_state,
            "prior_hidden": prior_hidden,
            "residual_scale": residual_scale,
            "proposal_dropout": proposal_dropout,
            "distill_weight": distill_weight,
            "residual_l2_weight": residual_l2_weight,
            "state_prior_checkpoint": state_prior_checkpoint,
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
        "state_prior_checkpoint": state_prior_checkpoint,
        "state_prior_frozen": True,
        "proposal_dropout": proposal_dropout,
        "distill_weight": distill_weight,
        "residual_l2_weight": residual_l2_weight,
        "residual_scale": residual_scale,
        "fallback_contamination_count": contamination,
        "final_train_loss": losses[-1] if losses else None,
        "loss_decrease_pct": (losses[0] - losses[-1]) / max(losses[0], 1e-9) * 100
        if len(losses) >= 2 else 0.0,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved NativeStudentDecoder + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", nargs="+", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--state-prior-checkpoint", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--lr", type=float, default=5e-4)
    ap.add_argument("--token-dim", type=int, default=64)
    ap.add_argument("--state-dim", type=int, default=64)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--num-layers", type=int, default=2)
    ap.add_argument("--num-heads", type=int, default=4)
    ap.add_argument("--prior-hidden", type=int, default=128)
    ap.add_argument("--residual-scale", type=float, default=0.05)
    ap.add_argument("--proposal-dropout", type=float, default=0.35)
    ap.add_argument("--distill-weight", type=float, default=0.5)
    ap.add_argument("--residual-l2-weight", type=float, default=0.01)
    ap.add_argument("--holdout-frac", type=float, default=0.2)
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--shuffle-state", action="store_true")
    a = ap.parse_args()
    train(
        a.cache,
        a.output_dir,
        a.state_prior_checkpoint,
        seed=a.seed,
        epochs=a.epochs,
        lr=a.lr,
        token_dim=a.token_dim,
        state_dim=a.state_dim,
        hidden=a.hidden,
        num_layers=a.num_layers,
        num_heads=a.num_heads,
        prior_hidden=a.prior_hidden,
        residual_scale=a.residual_scale,
        proposal_dropout=a.proposal_dropout,
        distill_weight=a.distill_weight,
        residual_l2_weight=a.residual_l2_weight,
        holdout_frac=a.holdout_frac,
        use_state=not a.no_state,
        shuffle_state=a.shuffle_state,
    )


if __name__ == "__main__":
    main()
