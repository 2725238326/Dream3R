"""Train Dream3R-U1 image/state native student decoder.

Requires caches produced by ``build_image_state_student_cache.py`` because old
SCF caches do not contain image tokens. The trainer evaluates full-anchor,
one-teacher-only, no-proposal, no-state, and shuffle-state behavior through the
same cached proposal/GT metrics used by Stage 6.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.image_state_student_decoder import ImageStateStudentDecoder
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.train_fusion_head import _abs_rel_loss, _stratified_split
from dream3r.scripts.train_scf_head import (
    _build_state_source,
    _per_patch_oracle_abs_rel,
    _scale_drift_proxy,
    _temporal_delta_abs_rel,
)


def _load_image_caches(paths: List[str]) -> Tuple[List[Dict], int, int, List[str]]:
    entries: List[Dict] = []
    d_memory: Optional[int] = None
    d_image: Optional[int] = None
    expert_order: Optional[List[str]] = None
    for path in paths:
        blob = torch.load(path, map_location="cpu", weights_only=False)
        if blob.get("d_image") is None:
            raise ValueError(
                f"{path} has no d_image; rebuild with build_image_state_student_cache.py"
            )
        for entry in blob["entries"]:
            if "image_tokens" not in entry:
                raise ValueError(
                    f"{path} contains entries without image_tokens; not usable for U1"
                )
        entries.extend(blob["entries"])
        d_memory = int(blob["d_memory"]) if d_memory is None else d_memory
        d_image = int(blob["d_image"]) if d_image is None else d_image
        if expert_order is None:
            expert_order = list(blob["expert_order"])
        elif expert_order != list(blob["expert_order"]):
            raise ValueError(f"expert_order mismatch: {expert_order} vs {blob['expert_order']}")
    if d_memory is None or d_image is None or expert_order is None:
        raise ValueError("empty image-state cache list")
    return entries, d_memory, d_image, expert_order


def _stack(entry: Dict, expert_order: List[str], device: torch.device, state_entry: Dict):
    image_tokens = entry["image_tokens"].unsqueeze(0).to(device)
    pms = torch.stack([entry["proposals"][name]["pointmap"] for name in expert_order], dim=0) \
        .unsqueeze(0).to(device)
    cfs = torch.stack([entry["proposals"][name]["confidence"] for name in expert_order], dim=0) \
        .unsqueeze(0).to(device)
    mc = state_entry["memory_context"].unsqueeze(0).to(device) \
        if state_entry["memory_context"] is not None else None
    cs = torch.tensor([[entry["conflict_score"]]], device=device)
    gt = entry["gt_pointmap"].unsqueeze(0).to(device)
    mask = entry["gt_mask"].unsqueeze(0).to(device)
    return image_tokens, pms, cfs, mc, cs, gt, mask


def _fallback_contamination_count(entries: List[Dict], expert_order: List[str]) -> int:
    count = 0
    for entry in entries:
        backends = entry.get("expert_backends") or {}
        for name in expert_order:
            if backends.get(name) is not True:
                count += 1
    return count


def _masked_smooth_l1(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    valid = mask.bool().unsqueeze(-1).expand_as(pred)
    finite = valid & torch.isfinite(pred) & torch.isfinite(target)
    if not bool(finite.any()):
        return pred.new_tensor(0.0)
    return F.smooth_l1_loss(pred[finite], target.detach()[finite])


def _load_state_prior_checkpoint(model: ImageStateStudentDecoder, checkpoint_path: str, device: torch.device) -> None:
    ckpt = torch.load(checkpoint_path, map_location=device)
    model.state_prior.load_state_dict(ckpt["state_dict"])
    model.freeze_state_prior()


def _eval(
    entries: List[Dict],
    idxs: List[int],
    model: ImageStateStudentDecoder,
    state_entries: List[Dict],
    expert_order: List[str],
    device: torch.device,
) -> Dict[str, Dict[str, float]]:
    model.eval()
    n_exp = len(expert_order)
    sums: Dict[str, Dict] = {}
    with torch.no_grad():
        for i in idxs:
            entry = entries[i]
            dom = entry["domain"]
            image_tokens, pms, cfs, mc, cs, gt, mask = _stack(entry, expert_order, device, state_entries[i])
            per_expert = [
                _pointmap_abs_rel(pms[:, k], gt, mask, align_scale=True)
                for k in range(n_exp)
            ]
            oracle = min(per_expert)
            patch_oracle = _per_patch_oracle_abs_rel(pms, gt, mask)
            full = model(image_tokens, mc, cs, pms, cfs, proposal_dropout=0.0)
            no_prop = model(image_tokens, mc, cs, None, None, proposal_dropout=0.0)
            ours = _pointmap_abs_rel(full["final_pointmap"], gt, mask, align_scale=True)
            native = _pointmap_abs_rel(full["native_pointmap"], gt, mask, align_scale=True)
            no_proposal = _pointmap_abs_rel(no_prop["final_pointmap"], gt, mask, align_scale=True)
            temporal = _temporal_delta_abs_rel(full["final_pointmap"], gt, mask)
            scale = _scale_drift_proxy(full["final_pointmap"], gt, mask)
            s = sums.setdefault(dom, {
                "per_expert": [0.0] * n_exp,
                "oracle": 0.0,
                "patch_oracle": 0.0,
                "ours": 0.0,
                "native": 0.0,
                "no_proposal": 0.0,
                "temporal": 0.0,
                "scale": 0.0,
                "n": 0,
            })
            for k in range(n_exp):
                s["per_expert"][k] += per_expert[k]
            s["oracle"] += oracle
            s["patch_oracle"] += patch_oracle
            s["ours"] += ours
            s["native"] += native
            s["no_proposal"] += no_proposal
            s["temporal"] += temporal
            s["scale"] += scale
            s["n"] += 1
    model.train()
    result: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1, s["n"])
        pe = [v / n for v in s["per_expert"]]
        oracle = s["oracle"] / n
        patch_oracle = s["patch_oracle"] / n
        ours = s["ours"] / n
        best_single = min(pe)
        result[dom] = {
            "n": s["n"],
            **{f"B_{expert_order[k]}": round(pe[k], 4) for k in range(n_exp)},
            "B_oracle": round(oracle, 4),
            "B_patch_oracle": round(patch_oracle, 4),
            "Ours_ImageStateStudent": round(ours, 4),
            "Ours_NativeNoProposal": round(s["no_proposal"] / n, 4),
            "Ours_NativePointHead": round(s["native"] / n, 4),
            "best_single": round(best_single, 4),
            "rel_imp_vs_best_single_pp": round((best_single - ours) / max(best_single, 1e-9) * 100, 2),
            "oracle_gap_pp": round((ours - oracle) / max(oracle, 1e-9) * 100, 2),
            "patch_oracle_gap_pp": round((ours - patch_oracle) / max(patch_oracle, 1e-9) * 100, 2),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale"] / n, 4),
        }
    return result


def train(
    cache_paths: List[str],
    output_dir: str,
    state_prior_checkpoint: str,
    seed: int = 7,
    epochs: int = 50,
    lr: float = 5e-4,
    proposal_dropout: float = 0.5,
    distill_weight: float = 0.25,
    native_weight: float = 0.5,
    holdout_frac: float = 0.2,
    use_state: bool = True,
    shuffle_state: bool = False,
):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    entries, d_memory, d_image, expert_order = _load_image_caches(cache_paths)
    contamination = _fallback_contamination_count(entries, expert_order)
    if contamination:
        raise RuntimeError(f"fallback/stub proposal contamination detected: {contamination}")
    state_entries = _build_state_source(entries, seed, shuffle_state)
    print(
        f"loaded {len(entries)} entries, d_image={d_image}, d_memory={d_memory}, "
        f"experts={expert_order}, fallback_contamination_count={contamination}",
        flush=True,
    )

    model = ImageStateStudentDecoder(
        n_experts=len(expert_order),
        d_image=d_image,
        d_memory=d_memory,
        use_state=use_state,
    ).to(device)
    _load_state_prior_checkpoint(model, state_prior_checkpoint, device)
    opt = torch.optim.Adam((p for p in model.parameters() if p.requires_grad), lr=lr)

    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    print(
        f"split: train={len(train_idx)} test={len(test_idx)} "
        f"use_state={use_state} shuffle_state={shuffle_state}",
        flush=True,
    )

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        total, nb = 0.0, 0
        for i in order:
            image_tokens, pms, cfs, mc, cs, gt, mask = _stack(entries[i], expert_order, device, state_entries[i])
            out = model(image_tokens, mc, cs, pms, cfs, proposal_dropout=proposal_dropout)
            no_prop = model(image_tokens, mc, cs, None, None, proposal_dropout=0.0)
            loss = _abs_rel_loss(out["final_pointmap"], gt, mask, align_scale=True)
            loss = loss + native_weight * _abs_rel_loss(out["native_pointmap"], gt, mask, align_scale=True)
            loss = loss + distill_weight * _masked_smooth_l1(
                no_prop["final_pointmap"],
                out["anchor_pointmap"],
                mask,
            )
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss)
            nb += 1
        losses.append(total / max(1, nb))
        if (epoch + 1) % 10 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, model, state_entries, expert_order, device)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_eval = _eval(entries, test_idx, model, state_entries, expert_order, device)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "config": {
            "n_experts": len(expert_order),
            "d_image": d_image,
            "d_memory": d_memory,
            "use_state": use_state,
            "shuffle_state": shuffle_state,
            "proposal_dropout": proposal_dropout,
            "distill_weight": distill_weight,
            "native_weight": native_weight,
            "state_prior_checkpoint": state_prior_checkpoint,
        },
        "loss_curve": losses,
        "final_eval": final_eval,
    }, out_path / "latest.pt")
    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "expert_order": expert_order,
        "use_state": use_state,
        "shuffle_state": shuffle_state,
        "fallback_contamination_count": contamination,
        "proposal_dropout": proposal_dropout,
        "state_prior_checkpoint": state_prior_checkpoint,
        "final_train_loss": losses[-1] if losses else None,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved ImageStateStudentDecoder + results to {out_path}", flush=True)
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
    ap.add_argument("--proposal-dropout", type=float, default=0.5)
    ap.add_argument("--distill-weight", type=float, default=0.25)
    ap.add_argument("--native-weight", type=float, default=0.5)
    ap.add_argument("--holdout-frac", type=float, default=0.2)
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--shuffle-state", action="store_true")
    args = ap.parse_args()
    train(
        args.cache,
        args.output_dir,
        args.state_prior_checkpoint,
        seed=args.seed,
        epochs=args.epochs,
        lr=args.lr,
        proposal_dropout=args.proposal_dropout,
        distill_weight=args.distill_weight,
        native_weight=args.native_weight,
        holdout_frac=args.holdout_frac,
        use_state=not args.no_state,
        shuffle_state=args.shuffle_state,
    )


if __name__ == "__main__":
    main()
