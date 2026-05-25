"""End-to-end demo of Stage 5 S1 router + expert pipeline on KITTI."""

import argparse
import gc
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.composer_experts.spann3r_adapter import Spann3RAdapter
from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.scripts.build_oracle_expert_labels import (
    _pointmap_abs_rel,
    _resize_images,
)
from dream3r.scripts.eval_router_ablation import _load_router
from dream3r.scripts.train_router_only import _feature_tensor


EXPERT_CLASSES = {
    "fast3r": Fast3RAdapter,
    "mast3r": MASt3RAdapter,
    "spann3r": Spann3RAdapter,
}


def _load_adapter(name: str):
    adapter = EXPERT_CLASSES[name]()
    adapter.load_checkpoint()
    if not adapter.is_loaded:
        raise RuntimeError(f"{name} did not load real checkpoint")
    return adapter


def _select_demo_windows(oracle_data: Dict[str, object]) -> List[Tuple[str, str]]:
    targets = ["mast3r", "spann3r"]
    selections: List[Tuple[str, str]] = []
    for target in targets:
        candidates = [
            (seq, float(oracle_data["metrics"][seq][target]))
            for seq, name in oracle_data["oracle_expert"].items()
            if name == target and target in oracle_data["metrics"].get(seq, {})
        ]
        if not candidates:
            continue
        seq, _ = min(candidates, key=lambda kv: kv[1])
        selections.append((seq, target))
    return selections


def _sample_window(root: str, sequence: str, window_frames: int) -> Dict[str, torch.Tensor]:
    dataset = KITTILongSequenceDataset(
        root=root,
        sequence=sequence,
        sequence_length=window_frames,
        overlap=max(0, window_frames - 1),
        windows_per_sample=1,
        min_sequence_frames=window_frames,
        max_frames_per_sequence=32,
        max_sequences=0,
        n_patches=196,
        d_model=8,
    )
    if len(dataset) == 0:
        raise RuntimeError(f"no sample for sequence {sequence}")
    return dataset[0]


def _patch_colors(images: torch.Tensor, patch_grid: int) -> torch.Tensor:
    """images: [N, 3, H, W] in [0,1] -> [N, P, 3] uint8-range floats."""
    sampled = F.adaptive_avg_pool2d(images, (patch_grid, patch_grid))
    return (sampled.clamp(0, 1) * 255).permute(0, 2, 3, 1).reshape(images.shape[0], -1, 3)


def _save_pointmap_ply(points: torch.Tensor, mask: torch.Tensor,
                       colors: torch.Tensor, path: Path) -> int:
    """ASCII PLY. points: [P, 3], mask: [P] bool, colors: [P, 3] in 0..255."""
    mask_b = mask.bool().cpu()
    valid_idx = torch.nonzero(mask_b, as_tuple=False).squeeze(-1).tolist()
    pts = points.detach().cpu().numpy()
    cls = colors.detach().cpu().numpy().astype("uint8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(valid_idx)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for i in valid_idx:
            x, y, z = pts[i]
            r, g, b = cls[i]
            f.write(f"{x:.4f} {y:.4f} {z:.4f} {int(r)} {int(g)} {int(b)}\n")
    return len(valid_idx)


def _save_figure_pointmap(images: torch.Tensor, pred: torch.Tensor,
                          target: torch.Tensor, mask: torch.Tensor,
                          expert_name: str, out_path: Path,
                          align_scale: bool = True):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    n = images.shape[0]
    patch_grid = int(round(pred.shape[1] ** 0.5))
    pred_d = pred[..., 2].view(n, patch_grid, patch_grid).cpu().numpy()
    target_d = target[..., 2].view(n, patch_grid, patch_grid).cpu().numpy()
    mask_grid = mask.view(n, patch_grid, patch_grid).cpu().numpy().astype(bool)

    valid_all = mask_grid & np.isfinite(pred_d) & np.isfinite(target_d) & (np.abs(target_d) > 1e-6)
    if align_scale and valid_all.any():
        denom = float(np.median(pred_d[valid_all]))
        if abs(denom) > 1e-6:
            scale = float(np.median(target_d[valid_all])) / denom
            pred_d = pred_d * scale

    err = np.abs(pred_d - target_d)
    err[~valid_all] = 0.0

    fig, axes = plt.subplots(4, n, figsize=(2.5 * n, 9))
    if n == 1:
        axes = axes.reshape(4, 1)
    rgb = images.permute(0, 2, 3, 1).cpu().numpy()
    for i in range(n):
        axes[0, i].imshow(rgb[i])
        axes[0, i].set_title(f"frame {i}")
        axes[0, i].axis("off")
        axes[1, i].imshow(pred_d[i], cmap="viridis")
        axes[1, i].set_title(f"pred depth ({expert_name})")
        axes[1, i].axis("off")
        axes[2, i].imshow(target_d[i], cmap="viridis")
        axes[2, i].set_title("GT depth")
        axes[2, i].axis("off")
        axes[3, i].imshow(err[i], cmap="hot")
        axes[3, i].set_title("abs error")
        axes[3, i].axis("off")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=100)
    plt.close()


def _save_figure_routing(regime_probs: List[float], regime_order: List[str],
                         router_logits: List[float], expert_order: List[str],
                         oracle_expert: str, router_expert: str,
                         out_path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(regime_order, regime_probs, color="steelblue")
    axes[0].set_title("regime probabilities (6D)")
    axes[0].set_ylim(0, 1)
    for label in axes[0].get_xticklabels():
        label.set_rotation(30)
        label.set_ha("right")

    bar_colors = ["#4caf50" if name == router_expert else "#90a4ae" for name in expert_order]
    bars = axes[1].bar(expert_order, router_logits, color=bar_colors)
    match = "MATCH" if router_expert == oracle_expert else "MISMATCH"
    axes[1].set_title(
        f"router logits  (router={router_expert}, oracle={oracle_expert}, {match})"
    )
    for bar, val in zip(bars, router_logits):
        axes[1].text(bar.get_x() + bar.get_width() / 2, val,
                     f"{val:.2f}", ha="center",
                     va="bottom" if val >= 0 else "top")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=100)
    plt.close()


def _save_figure_expert_compare(per_expert_metrics: Dict[str, float],
                                router_expert: str, oracle_expert: str,
                                out_path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    names = list(per_expert_metrics.keys())
    vals = [per_expert_metrics[n] for n in names]
    bar_colors = []
    for n in names:
        if n == router_expert and n == oracle_expert:
            bar_colors.append("#4caf50")
        elif n == router_expert:
            bar_colors.append("#fbc02d")
        elif n == oracle_expert:
            bar_colors.append("#42a5f5")
        else:
            bar_colors.append("#bdbdbd")
    bars = ax.bar(names, vals, color=bar_colors)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v,
                f"{v:.4f}", ha="center", va="bottom")
    ax.set_title(
        f"per-expert abs_rel  (router={router_expert}, oracle={oracle_expert})"
    )
    ax.set_ylabel("abs_rel")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=100)
    plt.close()


def run_demo(
    root: str,
    regime_labels: str,
    oracle_labels: str,
    router_checkpoint: str,
    output_dir: str,
    expert_order: Optional[List[str]] = None,
    window_frames: int = 4,
    image_size: int = 224,
    align_scale: bool = True,
    feature_mode: str = "regime_stats",
) -> Dict[str, object]:
    expert_order = list(expert_order or ["fast3r", "mast3r", "spann3r"])
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    regime_order = regime_data.get("regime_order")

    if list(oracle_data["expert_order"]) != expert_order:
        raise ValueError(
            f"expert_order mismatch: oracle={oracle_data['expert_order']} "
            f"requested={expert_order}"
        )

    selections = _select_demo_windows(oracle_data)
    if len(selections) < 2:
        raise RuntimeError(
            f"need both MASt3R and Spann3R winning windows; got {selections}"
        )

    sequences = [seq for seq, _ in selections]

    ckpt_peek = torch.load(router_checkpoint, map_location="cpu", weights_only=False)
    ckpt_feature_meta = (ckpt_peek.get("summary") or {}).get("feature_meta") or {}
    frozen_stats: Optional[Dict[str, object]] = None
    if feature_mode == "regime_stats" and ckpt_feature_meta.get("stat_mean") is not None:
        frozen_stats = {
            "stat_mean": ckpt_feature_meta["stat_mean"],
            "stat_std": ckpt_feature_meta["stat_std"],
        }

    x, feature_meta = _feature_tensor(
        regime_data, sequences, feature_mode, frozen_stats=frozen_stats,
    )
    router, _ = _load_router(
        router_checkpoint,
        n_regimes=x.shape[1],
        expert_order=expert_order,
        expected_feature_mode=feature_mode,
    )
    with torch.no_grad():
        out = router(x)
        logits = out["routing_logits"]
        pred_ids = logits.argmax(dim=-1).tolist()
        probs = torch.softmax(logits, dim=-1).tolist()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    samples = [_sample_window(root, sequence, window_frames) for sequence, _ in selections]

    expert_outputs: Dict[str, List[torch.Tensor]] = {name: [] for name in expert_order}
    for name in expert_order:
        adapter = _load_adapter(name)
        for sample in samples:
            images = sample["images"][0].unsqueeze(0).to(device)
            images = _resize_images(images, image_size)
            with torch.no_grad():
                expert_out = adapter.forward(images)
            expert_outputs[name].append(expert_out.pointmap.detach().cpu())
        del adapter
        gc.collect()
        if device.type == "cuda":
            torch.cuda.empty_cache()

    demo_summary: Dict[str, object] = {
        "router_checkpoint": router_checkpoint,
        "oracle_labels": oracle_labels,
        "regime_labels": regime_labels,
        "expert_order": expert_order,
        "feature_mode": feature_mode,
        "feature_meta": feature_meta,
        "image_size": image_size,
        "window_frames": window_frames,
        "align_scale": bool(align_scale),
        "windows": [],
    }

    for w_idx, (sequence, oracle_expert) in enumerate(selections):
        sample = samples[w_idx]
        target = sample["pointmap_gt"][0].unsqueeze(0)         # [1, N, P, 3]
        mask = sample["pointmap_mask"][0].unsqueeze(0)         # [1, N, P]
        images_lo = _resize_images(
            sample["images"][0].unsqueeze(0).float(), image_size,
        ).cpu()                                                # [1, N, 3, S, S]
        router_expert = expert_order[pred_ids[w_idx]]

        per_expert_abs_rel: Dict[str, float] = {}
        for name in expert_order:
            pred = expert_outputs[name][w_idx]                  # [1, N, P, 3]
            per_expert_abs_rel[name] = _pointmap_abs_rel(
                pred, target, mask, align_scale=align_scale,
            )

        chosen_pred = expert_outputs[router_expert][w_idx][0]   # [N, P, 3]

        window_dir = output_root / f"window_{w_idx:02d}_{sequence}_oracle_{oracle_expert}"
        figures_dir = window_dir / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)

        _save_figure_pointmap(
            images_lo[0], chosen_pred, target[0], mask[0],
            router_expert, figures_dir / "fig1_pointmap.png",
            align_scale=align_scale,
        )
        router_logits = logits[w_idx].tolist()
        regime_probs = list(regime_data["labels"][sequence])
        _save_figure_routing(
            regime_probs, regime_order, router_logits, expert_order,
            oracle_expert, router_expert,
            figures_dir / "fig2_routing.png",
        )
        _save_figure_expert_compare(
            per_expert_abs_rel, router_expert, oracle_expert,
            figures_dir / "fig3_expert_compare.png",
        )

        patch_grid = int(round(chosen_pred.shape[1] ** 0.5))
        colors_per_frame = _patch_colors(images_lo[0], patch_grid)   # [N, P, 3]
        all_points = chosen_pred.reshape(-1, 3).clone()
        all_mask = mask[0].reshape(-1)
        target_flat = target[0].reshape(-1, 3)
        scale_align_mask = (
            all_mask.bool()
            & torch.isfinite(all_points[:, 2])
            & torch.isfinite(target_flat[:, 2])
            & (target_flat[:, 2].abs() > 1e-6)
        )
        if align_scale and bool(scale_align_mask.any()):
            denom = all_points[scale_align_mask, 2].median()
            denom = torch.where(denom.abs() > 1e-6, denom, denom.new_tensor(1e-6))
            scale = target_flat[scale_align_mask, 2].median() / denom
            all_points = all_points * float(scale.item())

        ply_path = window_dir / "pointmap_pred.ply"
        n_pts = _save_pointmap_ply(
            all_points, all_mask, colors_per_frame.reshape(-1, 3), ply_path,
        )

        window_summary = {
            "sequence": sequence,
            "oracle_expert": oracle_expert,
            "router_expert": router_expert,
            "router_match_oracle": router_expert == oracle_expert,
            "router_logits": router_logits,
            "router_probs": probs[w_idx],
            "regime_probs": regime_probs,
            "regime_order": regime_order,
            "per_expert_abs_rel": per_expert_abs_rel,
            "ply_path": str(ply_path),
            "ply_n_points": n_pts,
            "figures_dir": str(figures_dir),
        }
        (window_dir / "summary.json").write_text(
            json.dumps(window_summary, indent=2), encoding="utf-8",
        )
        demo_summary["windows"].append(window_summary)

    (output_root / "summary.json").write_text(
        json.dumps(demo_summary, indent=2), encoding="utf-8",
    )
    return demo_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--oracle-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json",
    )
    parser.add_argument(
        "--router-checkpoint",
        default="/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt",
    )
    parser.add_argument(
        "--output-dir",
        default="/hdd3/kykt26/code/dream3r/runs/demo_stage5_s1",
    )
    parser.add_argument(
        "--experts", nargs="+", default=["fast3r", "mast3r", "spann3r"],
    )
    parser.add_argument("--window-frames", type=int, default=4)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--align-scale", action="store_true")
    parser.add_argument(
        "--feature-mode",
        choices=["regime", "regime_stats"],
        default="regime_stats",
    )
    args = parser.parse_args()

    summary = run_demo(
        root=args.root,
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        router_checkpoint=args.router_checkpoint,
        output_dir=args.output_dir,
        expert_order=args.experts,
        window_frames=args.window_frames,
        image_size=args.image_size,
        align_scale=args.align_scale,
        feature_mode=args.feature_mode,
    )
    print(json.dumps({
        "windows": [
            {
                "sequence": w["sequence"],
                "oracle_expert": w["oracle_expert"],
                "router_expert": w["router_expert"],
                "router_match_oracle": w["router_match_oracle"],
                "per_expert_abs_rel": w["per_expert_abs_rel"],
                "ply_n_points": w["ply_n_points"],
            }
            for w in summary["windows"]
        ],
        "output_dir": str(Path(args.output_dir).resolve()),
    }, indent=2))


if __name__ == "__main__":
    main()
