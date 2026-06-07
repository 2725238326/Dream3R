"""Train the proposal-free Dream3R native decoder.

This trainer consumes image-state caches only for image tokens, Dream state,
conflict score, and GT pointmaps. It does not feed proposal pointmaps or expert
confidences into the model.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.proposal_free_3r_decoder import ProposalFree3RDecoder
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.train_fusion_head import _abs_rel_loss, _stratified_split
from dream3r.scripts.train_scf_head import (
    _build_state_source,
    _scale_drift_proxy,
    _temporal_delta_abs_rel,
)


def _load_proposal_free_caches(paths: List[str]) -> Tuple[List[Dict], int, int]:
    entries: List[Dict] = []
    d_memory: Optional[int] = None
    d_image: Optional[int] = None
    for path in paths:
        blob = torch.load(path, map_location="cpu", weights_only=False)
        if blob.get("d_image") is None:
            raise ValueError(f"{path} has no d_image; rebuild image-state cache first")
        for entry in blob["entries"]:
            for key in ("image_tokens", "gt_pointmap", "gt_mask"):
                if key not in entry:
                    raise ValueError(f"{path} entry missing {key}")
        entries.extend(blob["entries"])
        d_memory = int(blob["d_memory"]) if d_memory is None else d_memory
        d_image = int(blob["d_image"]) if d_image is None else d_image
    if d_memory is None or d_image is None:
        raise ValueError("empty proposal-free cache list")
    return entries, d_memory, d_image


def _stack_free(entry: Dict, device: torch.device, state_entry: Dict):
    image_tokens = entry["image_tokens"].unsqueeze(0).to(device)
    mc = (
        state_entry["memory_context"].unsqueeze(0).to(device)
        if state_entry["memory_context"] is not None
        else None
    )
    cs = torch.tensor([[entry.get("conflict_score", 0.0)]], device=device)
    gt = entry["gt_pointmap"].unsqueeze(0).to(device)
    mask = entry["gt_mask"].unsqueeze(0).to(device)
    return image_tokens, mc, cs, gt, mask


def _teacher_pointmap(entry: Dict, device: torch.device) -> Optional[torch.Tensor]:
    teacher = entry.get("teacher_pointmap")
    if teacher is None:
        return None
    return teacher.unsqueeze(0).to(device)


def _masked_smooth_l1(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    valid = mask.bool().unsqueeze(-1).expand_as(pred)
    finite = valid & torch.isfinite(pred) & torch.isfinite(target)
    if not bool(finite.any()):
        return pred.new_tensor(0.0)
    return F.smooth_l1_loss(pred[finite], target.detach()[finite])


def _eval(
    entries: List[Dict],
    idxs: List[int],
    model: ProposalFree3RDecoder,
    state_entries: List[Dict],
    device: torch.device,
) -> Dict[str, Dict[str, float]]:
    model.eval()
    sums: Dict[str, Dict[str, float]] = {}
    with torch.no_grad():
        for i in idxs:
            entry = entries[i]
            dom = entry["domain"]
            image_tokens, mc, cs, gt, mask = _stack_free(entry, device, state_entries[i])
            out = model(image_tokens, mc, cs)
            abs_rel = _pointmap_abs_rel(out["final_pointmap"], gt, mask, align_scale=True)
            teacher = _teacher_pointmap(entry, device)
            teacher_abs_rel = (
                _pointmap_abs_rel(teacher, gt, mask, align_scale=True)
                if teacher is not None
                else None
            )
            temporal = _temporal_delta_abs_rel(out["final_pointmap"], gt, mask)
            scale = _scale_drift_proxy(out["final_pointmap"], gt, mask)
            s = sums.setdefault(dom, {
                "ours": 0.0,
                "teacher": 0.0,
                "teacher_n": 0.0,
                "temporal": 0.0,
                "scale": 0.0,
                "n": 0.0,
            })
            s["ours"] += abs_rel
            if teacher_abs_rel is not None:
                s["teacher"] += teacher_abs_rel
                s["teacher_n"] += 1.0
            s["temporal"] += temporal
            s["scale"] += scale
            s["n"] += 1.0
    model.train()
    result: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1.0, s["n"])
        result[dom] = {
            "n": int(s["n"]),
            "Ours_ProposalFree3R": round(s["ours"] / n, 4),
            "Teacher_OfflineTarget": (
                round(s["teacher"] / max(1.0, s["teacher_n"]), 4)
                if s["teacher_n"] > 0
                else None
            ),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale"] / n, 4),
        }
    return result


def train(
    cache_paths: List[str],
    output_dir: str,
    seed: int = 7,
    epochs: int = 50,
    lr: float = 5e-4,
    holdout_frac: float = 0.2,
    use_state: bool = True,
    shuffle_state: bool = False,
    teacher_weight: float = 0.0,
    teacher_absrel_weight: float = 0.0,
    model_dim: int = 128,
    state_dim: int = 64,
    hidden: int = 128,
    num_layers: int = 2,
    num_heads: int = 4,
):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    entries, d_memory, d_image = _load_proposal_free_caches(cache_paths)
    state_entries = _build_state_source(entries, seed, shuffle_state)
    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    model = ProposalFree3RDecoder(
        d_image=d_image,
        d_memory=d_memory,
        use_state=use_state,
        model_dim=model_dim,
        state_dim=state_dim,
        hidden=hidden,
        num_layers=num_layers,
        num_heads=num_heads,
    ).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    print(
        f"loaded {len(entries)} entries, d_image={d_image}, d_memory={d_memory}, "
        f"train={len(train_idx)} test={len(test_idx)}, use_state={use_state}, "
        f"shuffle_state={shuffle_state}, teacher_weight={teacher_weight}, "
        f"teacher_absrel_weight={teacher_absrel_weight}, model_dim={model_dim}, "
        f"num_layers={num_layers}, hidden={hidden}, "
        f"proposal_inputs_used=false",
        flush=True,
    )

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        total, nb = 0.0, 0
        for i in order:
            image_tokens, mc, cs, gt, mask = _stack_free(entries[i], device, state_entries[i])
            out = model(image_tokens, mc, cs)
            loss = _abs_rel_loss(out["final_pointmap"], gt, mask, align_scale=True)
            teacher = _teacher_pointmap(entries[i], device)
            if teacher is not None and teacher_weight > 0:
                loss = loss + float(teacher_weight) * _masked_smooth_l1(
                    out["final_pointmap"],
                    teacher,
                    mask,
                )
            if teacher is not None and teacher_absrel_weight > 0:
                loss = loss + float(teacher_absrel_weight) * _abs_rel_loss(
                    out["final_pointmap"],
                    teacher,
                    mask,
                    align_scale=True,
                )
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss.detach())
            nb += 1
        losses.append(total / max(1, nb))
        if (epoch + 1) % 10 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, model, state_entries, device)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_eval = _eval(entries, test_idx, model, state_entries, device)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "config": {
            "d_image": d_image,
            "d_memory": d_memory,
            "use_state": use_state,
            "shuffle_state": shuffle_state,
            "teacher_weight": teacher_weight,
            "teacher_absrel_weight": teacher_absrel_weight,
            "model_dim": model_dim,
            "state_dim": state_dim,
            "hidden": hidden,
            "num_layers": num_layers,
            "num_heads": num_heads,
            "proposal_inputs_used": False,
        },
        "loss_curve": losses,
        "final_eval": final_eval,
    }, out_path / "latest.pt")
    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "use_state": use_state,
        "shuffle_state": shuffle_state,
        "teacher_weight": teacher_weight,
        "teacher_absrel_weight": teacher_absrel_weight,
        "model_dim": model_dim,
        "state_dim": state_dim,
        "hidden": hidden,
        "num_layers": num_layers,
        "num_heads": num_heads,
        "proposal_inputs_used": False,
        "final_train_loss": losses[-1] if losses else None,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved ProposalFree3RDecoder + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", nargs="+", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--lr", type=float, default=5e-4)
    ap.add_argument("--holdout-frac", type=float, default=0.2)
    ap.add_argument("--teacher-weight", type=float, default=0.0)
    ap.add_argument("--teacher-absrel-weight", type=float, default=0.0)
    ap.add_argument("--model-dim", type=int, default=128)
    ap.add_argument("--state-dim", type=int, default=64)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--num-layers", type=int, default=2)
    ap.add_argument("--num-heads", type=int, default=4)
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--shuffle-state", action="store_true")
    args = ap.parse_args()
    train(
        args.cache,
        args.output_dir,
        seed=args.seed,
        epochs=args.epochs,
        lr=args.lr,
        holdout_frac=args.holdout_frac,
        use_state=not args.no_state,
        shuffle_state=args.shuffle_state,
        teacher_weight=args.teacher_weight,
        teacher_absrel_weight=args.teacher_absrel_weight,
        model_dim=args.model_dim,
        state_dim=args.state_dim,
        hidden=args.hidden,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
    )


if __name__ == "__main__":
    main()
