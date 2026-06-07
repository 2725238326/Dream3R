"""Train the proposal-free Foundation3R decoder.

This trainer consumes Foundation3R dense teacher caches. It never reads
proposal pointmaps or expert confidences, and it keeps state/no-state/shuffle
controls explicit for later promotion gates.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.foundation3r_decoder import Foundation3RDecoder, Foundation3RVGGTFeatureDecoder
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.train_fusion_head import _abs_rel_loss, _stratified_split
from dream3r.scripts.train_scf_head import (
    _build_state_source,
    _scale_drift_proxy,
    _temporal_delta_abs_rel,
)


FORBIDDEN_ENTRY_KEYS = {
    "proposals",
    "proposal_pointmaps",
    "proposal_confidences",
    "expert_confidences",
    "expert_order",
    "teacher_model",
}

LOSS_PROFILES = {"auto", "hybrid", "teacher_only"}


def _load_caches(paths: List[str], d_memory_override: int = 0) -> Tuple[List[Dict], int]:
    entries: List[Dict] = []
    d_memory: Optional[int] = None
    for path in paths:
        blob = torch.load(path, map_location="cpu", weights_only=False)
        if blob.get("cache_type") != "foundation3r_dense_teacher":
            raise ValueError(f"{path} is not a Foundation3R dense teacher cache")
        if blob.get("proposal_inputs_used") is not False:
            raise ValueError(f"{path} does not declare proposal_inputs_used=false")
        if blob.get("teacher_used_at_inference") is not False:
            raise ValueError(f"{path} does not declare teacher_used_at_inference=false")
        if blob.get("proposal_fields_stripped") is not True:
            raise ValueError(f"{path} does not declare proposal_fields_stripped=true")
        for entry in blob["entries"]:
            leaked = sorted(FORBIDDEN_ENTRY_KEYS.intersection(entry))
            if leaked:
                raise ValueError(f"{path} entry leaks forbidden fields: {leaked}")
            for key in ("teacher_pointmap", "teacher_confidence", "teacher_valid_mask"):
                if key not in entry:
                    raise ValueError(f"{path} entry missing {key}")
            mc = entry.get("memory_context")
            if isinstance(mc, torch.Tensor) and d_memory is None:
                d_memory = int(mc.numel())
            entries.append(entry)
    if not entries:
        raise ValueError("empty Foundation3R cache list")
    if d_memory is None:
        d_memory = int(d_memory_override) if d_memory_override > 0 else 1
    return entries, d_memory


def _load_images(entry: Dict, image_size: int) -> torch.Tensor:
    images = entry.get("images")
    if isinstance(images, torch.Tensor):
        tensor = images.detach().float()
        if tensor.dim() != 4:
            raise ValueError(f"entry images must be [N,C,H,W], got {tuple(tensor.shape)}")
        return tensor

    frames = entry.get("frames") or []
    if not frames:
        raise ValueError(f"{entry.get('seq', '<unknown>')} has no images tensor or frames")
    try:
        from PIL import Image
    except Exception as exc:  # pragma: no cover - environment failure path
        raise RuntimeError("Pillow is required to load Foundation3R frame paths") from exc

    out: List[torch.Tensor] = []
    for frame in frames:
        path = Path(frame).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"image frame not found: {path}")
        img = Image.open(path).convert("RGB").resize((image_size, image_size))
        data = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
        data = data.view(image_size, image_size, 3).permute(2, 0, 1).float() / 255.0
        out.append(data)
    return torch.stack(out, dim=0)


def _stack(entry: Dict, device: torch.device, state_entry: Dict, image_size: int, input_mode: str):
    images = _load_images(entry, image_size).unsqueeze(0).to(device) if input_mode == "images" else None
    vggt_features = entry.get("vggt_patch_features")
    if input_mode == "vggt_features":
        if not isinstance(vggt_features, torch.Tensor):
            raise ValueError(f"{entry.get('seq', '<unknown>')} missing vggt_patch_features")
        vggt_features = vggt_features.unsqueeze(0).float().to(device)
    else:
        vggt_features = None
    mc = state_entry.get("memory_context")
    memory_context = mc.reshape(1, -1).to(device) if isinstance(mc, torch.Tensor) else None
    conflict_score = torch.tensor([[entry.get("conflict_score", 0.0)]], device=device)
    teacher = entry["teacher_pointmap"].unsqueeze(0).to(device)
    teacher_conf = entry["teacher_confidence"].unsqueeze(0).to(device)
    teacher_mask = entry["teacher_valid_mask"].unsqueeze(0).to(device)
    gt = entry.get("gt_pointmap")
    gt_mask = entry.get("gt_mask")
    gt = gt.unsqueeze(0).to(device) if isinstance(gt, torch.Tensor) else None
    gt_mask = gt_mask.unsqueeze(0).to(device) if isinstance(gt_mask, torch.Tensor) else None
    return images, vggt_features, memory_context, conflict_score, teacher, teacher_conf, teacher_mask, gt, gt_mask


def _infer_vggt_feature_dim(entries: List[Dict]) -> int:
    for entry in entries:
        feat = entry.get("vggt_patch_features")
        if isinstance(feat, torch.Tensor):
            return int(feat.shape[-1])
    return 0


def _forward_model(
    model: torch.nn.Module,
    images: Optional[torch.Tensor],
    vggt_features: Optional[torch.Tensor],
    memory_context: Optional[torch.Tensor],
    conflict_score: Optional[torch.Tensor],
    input_mode: str,
):
    if input_mode == "images":
        if images is None:
            raise ValueError("input_mode=images requires image tensors")
        return model(images, memory_context, conflict_score)
    if input_mode == "vggt_features":
        if vggt_features is None:
            raise ValueError("input_mode=vggt_features requires vggt_patch_features")
        return model(vggt_features, memory_context, conflict_score)
    raise ValueError(f"unsupported input_mode: {input_mode}")


def _masked_weighted_smooth_l1(
    pred: torch.Tensor,
    target: torch.Tensor,
    valid_mask: torch.Tensor,
    confidence: torch.Tensor,
) -> torch.Tensor:
    valid = valid_mask.bool().unsqueeze(-1).expand_as(pred)
    finite = valid & torch.isfinite(pred) & torch.isfinite(target)
    if not bool(finite.any()):
        return pred.new_tensor(0.0)
    per_value = F.smooth_l1_loss(pred, target.detach(), reduction="none")
    weights = confidence.detach().clamp_min(0.0).expand_as(pred)
    weights = torch.where(finite, weights, torch.zeros_like(weights))
    denom = weights.sum().clamp_min(1e-6)
    return (per_value * weights).sum() / denom


def _scale_normalize_pointmap(pointmap: torch.Tensor, valid_mask: torch.Tensor) -> torch.Tensor:
    """Normalize each sample by median absolute target depth.

    Evaluation is scale-aligned AbsRel, so the student should first learn a
    stable geometry shape instead of spending early capacity on VGGTΩ's metric
    scale. This keeps inference proposal-free and teacher-free.
    """
    out = pointmap.clone()
    for b in range(pointmap.shape[0]):
        valid = (
            valid_mask[b].bool()
            & torch.isfinite(pointmap[b, ..., 2])
            & (pointmap[b, ..., 2].abs() > 1e-6)
        )
        if bool(valid.any()):
            scale = pointmap[b, ..., 2][valid].abs().median().clamp_min(1e-6)
            out[b] = pointmap[b] / scale
    return out


def _masked_log_depth_l1(
    pred: torch.Tensor,
    target: torch.Tensor,
    valid_mask: torch.Tensor,
) -> torch.Tensor:
    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        valid_mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (pred_depth > 1e-6)
        & (target_depth.abs() > 1e-6)
    )
    if not bool(valid.any()):
        return pred.sum() * 0.0
    with torch.no_grad():
        pred_med = pred_depth[valid].median().clamp_min(1e-6)
        target_med = target_depth[valid].abs().median().clamp_min(1e-6)
    pred_norm = (pred_depth[valid] / pred_med).clamp_min(1e-6)
    target_norm = (target_depth[valid].abs() / target_med).clamp_min(1e-6)
    return F.l1_loss(torch.log(pred_norm), torch.log(target_norm))


def _foundation3r_supervision_loss(
    pred: torch.Tensor,
    teacher: torch.Tensor,
    teacher_conf: torch.Tensor,
    teacher_mask: torch.Tensor,
    gt: Optional[torch.Tensor],
    gt_mask: Optional[torch.Tensor],
    teacher_weight: float,
    gt_weight: float,
    depth_weight: float,
) -> torch.Tensor:
    teacher_target = _scale_normalize_pointmap(teacher, teacher_mask)
    loss = float(teacher_weight) * _masked_weighted_smooth_l1(
        pred,
        teacher_target,
        teacher_mask,
        teacher_conf,
    )
    if gt is not None and gt_mask is not None and gt_weight > 0:
        gt_target = _scale_normalize_pointmap(gt, gt_mask)
        loss = loss + float(gt_weight) * _abs_rel_loss(
            pred,
            gt_target,
            gt_mask,
            align_scale=True,
        )
    if depth_weight > 0:
        depth_target = gt if gt is not None else teacher
        depth_mask = gt_mask if gt_mask is not None else teacher_mask
        loss = loss + float(depth_weight) * _masked_log_depth_l1(
            pred,
            depth_target,
            depth_mask,
        )
    return loss


def _resolve_loss_weights(
    input_mode: str,
    loss_profile: str,
    teacher_weight: Optional[float],
    gt_weight: Optional[float],
    depth_weight: Optional[float],
) -> Tuple[float, float, float, str]:
    if loss_profile not in LOSS_PROFILES:
        raise ValueError(f"unsupported loss_profile: {loss_profile}")
    resolved_profile = loss_profile
    if resolved_profile == "auto":
        resolved_profile = "teacher_only" if input_mode == "vggt_features" else "hybrid"

    defaults = {
        "hybrid": (1.0, 1.0, 1.0),
        "teacher_only": (1.0, 0.0, 0.0),
    }[resolved_profile]
    tw = defaults[0] if teacher_weight is None else float(teacher_weight)
    gw = defaults[1] if gt_weight is None else float(gt_weight)
    dw = defaults[2] if depth_weight is None else float(depth_weight)
    return tw, gw, dw, resolved_profile


def _eval(
    entries: List[Dict],
    idxs: List[int],
    model: Foundation3RDecoder,
    state_entries: List[Dict],
    device: torch.device,
    image_size: int,
    input_mode: str,
) -> Dict[str, Dict[str, float]]:
    model.eval()
    sums: Dict[str, Dict[str, float]] = {}
    with torch.no_grad():
        for i in idxs:
            entry = entries[i]
            dom = entry["domain"]
            images, vggt_features, mc, cs, teacher, teacher_conf, teacher_mask, gt, gt_mask = _stack(
                entry, device, state_entries[i], image_size, input_mode
            )
            out = _forward_model(model, images, vggt_features, mc, cs, input_mode)
            s = sums.setdefault(dom, {
                "ours": 0.0,
                "teacher": 0.0,
                "temporal": 0.0,
                "scale": 0.0,
                "n": 0.0,
            })
            if gt is not None and gt_mask is not None:
                s["ours"] += _pointmap_abs_rel(out["final_pointmap"], gt, gt_mask, align_scale=True)
                s["teacher"] += _pointmap_abs_rel(teacher, gt, gt_mask, align_scale=True)
                s["temporal"] += _temporal_delta_abs_rel(out["final_pointmap"], gt, gt_mask)
                s["scale"] += _scale_drift_proxy(out["final_pointmap"], gt, gt_mask)
            else:
                teacher_loss = _masked_weighted_smooth_l1(
                    out["final_pointmap"],
                    teacher,
                    teacher_mask,
                    teacher_conf,
                )
                s["ours"] += float(teacher_loss.item())
                s["teacher"] += 0.0
            s["n"] += 1.0
    model.train()
    result: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1.0, s["n"])
        result[dom] = {
            "n": int(s["n"]),
            "Ours_Foundation3R": round(s["ours"] / n, 4),
            "Teacher_Dense": round(s["teacher"] / n, 4),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale"] / n, 4),
        }
    return result


def train(
    cache_paths: List[str],
    output_dir: str,
    seed: int = 7,
    epochs: int = 20,
    lr: float = 1e-3,
    holdout_frac: float = 0.2,
    image_size: int = 224,
    patch_size: int = 16,
    teacher_weight: Optional[float] = None,
    gt_weight: Optional[float] = None,
    depth_weight: Optional[float] = None,
    loss_profile: str = "auto",
    use_state: bool = True,
    shuffle_state: bool = False,
    model_dim: int = 128,
    state_dim: int = 64,
    hidden: int = 256,
    num_layers: int = 2,
    num_heads: int = 4,
    d_memory_override: int = 0,
    input_mode: str = "images",
    state_contrast_weight: float = 0.0,
    state_contrast_margin: float = 0.02,
) -> Dict:
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    entries, d_memory = _load_caches(cache_paths, d_memory_override=d_memory_override)
    if input_mode not in {"images", "vggt_features"}:
        raise ValueError(f"unsupported input_mode: {input_mode}")
    teacher_weight, gt_weight, depth_weight, resolved_loss_profile = _resolve_loss_weights(
        input_mode,
        loss_profile,
        teacher_weight,
        gt_weight,
        depth_weight,
    )
    d_vggt_feature = _infer_vggt_feature_dim(entries)
    if input_mode == "vggt_features" and d_vggt_feature <= 0:
        raise ValueError("input_mode=vggt_features requested but cache has no vggt_patch_features")
    state_entries = _build_state_source(entries, seed, shuffle_state)
    contrast_state_entries = _build_state_source(entries, seed + 1701, True)
    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    if input_mode == "vggt_features":
        model = Foundation3RVGGTFeatureDecoder(
            d_vggt_feature=d_vggt_feature,
            d_memory=d_memory,
            model_dim=model_dim,
            state_dim=state_dim,
            hidden=hidden,
            num_layers=num_layers,
            num_heads=num_heads,
            use_state=use_state,
        ).to(device)
    else:
        model = Foundation3RDecoder(
            d_memory=d_memory,
            patch_size=patch_size,
            model_dim=model_dim,
            state_dim=state_dim,
            hidden=hidden,
            num_layers=num_layers,
            num_heads=num_heads,
            use_state=use_state,
        ).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    print(
        f"loaded {len(entries)} entries, d_memory={d_memory}, "
        f"train={len(train_idx)} test={len(test_idx)}, use_state={use_state}, "
        f"shuffle_state={shuffle_state}, input_mode={input_mode}, "
        f"image_size={image_size}, patch_size={patch_size}, "
        f"loss_profile={resolved_loss_profile}, "
        f"teacher_weight={teacher_weight}, gt_weight={gt_weight}, depth_weight={depth_weight}, "
        f"state_contrast_weight={state_contrast_weight}, "
        f"state_contrast_margin={state_contrast_margin}, "
        f"proposal_inputs_used=false teacher_used_at_inference=false",
        flush=True,
    )

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        total, nb = 0.0, 0
        for i in order:
            images, vggt_features, mc, cs, teacher, teacher_conf, teacher_mask, gt, gt_mask = _stack(
                entries[i], device, state_entries[i], image_size, input_mode
            )
            out = _forward_model(model, images, vggt_features, mc, cs, input_mode)
            pos_loss = _foundation3r_supervision_loss(
                out["final_pointmap"],
                teacher,
                teacher_conf,
                teacher_mask,
                gt,
                gt_mask,
                teacher_weight,
                gt_weight,
                depth_weight,
            )
            loss = pos_loss
            if use_state and state_contrast_weight > 0:
                _, _, neg_mc, neg_cs, _, _, _, _, _ = _stack(
                    entries[i], device, contrast_state_entries[i], image_size, input_mode
                )
                neg_out = _forward_model(model, images, vggt_features, neg_mc, neg_cs, input_mode)
                neg_loss = _foundation3r_supervision_loss(
                    neg_out["final_pointmap"],
                    teacher,
                    teacher_conf,
                    teacher_mask,
                    gt,
                    gt_mask,
                    teacher_weight,
                    gt_weight,
                    depth_weight,
                )
                contrast = F.relu(pos_loss - neg_loss + float(state_contrast_margin))
                loss = loss + float(state_contrast_weight) * contrast
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss.detach())
            nb += 1
        losses.append(total / max(1, nb))
        if (epoch + 1) % 10 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, model, state_entries, device, image_size, input_mode)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_train_eval = _eval(entries, train_idx, model, state_entries, device, image_size, input_mode)
    final_eval = _eval(entries, test_idx, model, state_entries, device, image_size, input_mode)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    config = {
        "d_memory": d_memory,
        "image_size": image_size,
        "patch_size": patch_size,
        "input_mode": input_mode,
        "d_vggt_feature": d_vggt_feature if input_mode == "vggt_features" else None,
        "use_state": use_state,
        "shuffle_state": shuffle_state,
        "teacher_weight": teacher_weight,
        "gt_weight": gt_weight,
        "depth_weight": depth_weight,
        "loss_profile": resolved_loss_profile,
        "model_dim": model_dim,
        "state_dim": state_dim,
        "hidden": hidden,
        "num_layers": num_layers,
        "num_heads": num_heads,
        "state_modulation": "film_scale_shift_plus_additive_state",
        "state_contrast_weight": float(state_contrast_weight),
        "state_contrast_margin": float(state_contrast_margin),
        "proposal_inputs_used": False,
        "teacher_used_at_inference": False,
        "vggt_backbone_features_used": input_mode == "vggt_features",
        "scale_normalized_targets": True,
    }
    torch.save({
        "model_state_dict": model.state_dict(),
        "config": config,
        "loss_curve": losses,
        "final_train_eval": final_train_eval,
        "final_eval": final_eval,
    }, out_path / "latest.pt")
    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        **config,
        "final_train_loss": losses[-1] if losses else None,
        "final_train_eval": final_train_eval,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved Foundation3RDecoder + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--holdout-frac", type=float, default=0.2)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--patch-size", type=int, default=16)
    parser.add_argument("--teacher-weight", type=float, default=1.0)
    parser.add_argument("--gt-weight", type=float, default=None)
    parser.add_argument("--depth-weight", type=float, default=None)
    parser.add_argument("--loss-profile", choices=sorted(LOSS_PROFILES), default="auto")
    parser.add_argument("--model-dim", type=int, default=128)
    parser.add_argument("--state-dim", type=int, default=64)
    parser.add_argument("--hidden", type=int, default=256)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--d-memory", type=int, default=0)
    parser.add_argument("--input-mode", choices=["images", "vggt_features"], default="images")
    parser.add_argument("--state-contrast-weight", type=float, default=0.0)
    parser.add_argument("--state-contrast-margin", type=float, default=0.02)
    parser.add_argument("--no-state", action="store_true")
    parser.add_argument("--shuffle-state", action="store_true")
    args = parser.parse_args()
    train(
        args.cache,
        args.output_dir,
        seed=args.seed,
        epochs=args.epochs,
        lr=args.lr,
        holdout_frac=args.holdout_frac,
        image_size=args.image_size,
        patch_size=args.patch_size,
        teacher_weight=args.teacher_weight,
        gt_weight=args.gt_weight,
        depth_weight=args.depth_weight,
        loss_profile=args.loss_profile,
        use_state=not args.no_state,
        shuffle_state=args.shuffle_state,
        model_dim=args.model_dim,
        state_dim=args.state_dim,
        hidden=args.hidden,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        d_memory_override=args.d_memory,
        input_mode=args.input_mode,
        state_contrast_weight=args.state_contrast_weight,
        state_contrast_margin=args.state_contrast_margin,
    )


if __name__ == "__main__":
    main()
