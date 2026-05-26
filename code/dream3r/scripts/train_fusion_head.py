"""Stage 6 fusion head — cache builder + trainer + held-out eval.

Three modes:

- ``--build-cache``: run ``V04Pipeline.forward()`` per window on a dataset
  and save ``(expert_pointmap, expert_confidence, memory_context,
  conflict_score, gt_pointmap, gt_mask)`` to a ``.pt`` cache file. Done
  once per (dataset, preset).
- default (training): load caches, train head with held-out abs_rel
  loss, save best checkpoint + per-window predictions.
- ``--eval-only``: load checkpoint, evaluate on the same held-out split,
  report baseline (``expert.pointmap``) vs head (``refined``) deltas.

Reused utilities:

- ``_pointmap_abs_rel`` from ``build_oracle_expert_labels.py``
- ``_resize_images`` from same
- window iteration patterns from ``build_critic_cache.py`` and
  ``build_critic_cache_eth3d.py``

This script never touches v0.3/v0.5 core. The only model-side dependency
is ``V04PipelineWithFusion`` (subclass, also a new file).
"""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES
from dream3r.fusion_head import Stage6FusionHead
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline
from dream3r.scripts.build_oracle_expert_labels import (
    _pointmap_abs_rel,
    _resize_images,
)


# ---------------------------------------------------------------------------
# Cache build
# ---------------------------------------------------------------------------


def _iter_kitti_windows(root: str, regime_labels: str, window_frames: int):
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    sequences = sorted(regime_data["labels"].keys())
    for seq in sequences:
        ds = KITTILongSequenceDataset(
            root=root,
            sequence=seq,
            sequence_length=window_frames,
            overlap=max(0, window_frames - 1),
            windows_per_sample=1,
            min_sequence_frames=window_frames,
            max_frames_per_sequence=32,
            max_sequences=0,
            n_patches=196,
            d_model=8,
        )
        if len(ds) == 0:
            continue
        sample = ds[0]
        yield seq, sample


def _iter_eth3d_windows(root: str, regime_labels: str, window_frames: int):
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    regime_sequences = list(regime_data["labels"].keys())
    rl_scenes = list(regime_data.get("scenes") or SCENES)
    rl_seq_len = int(regime_data.get("sequence_length", window_frames))
    rl_img_size = int(regime_data.get("image_size", 224))
    rl_n_patches = int(regime_data.get("n_patches", 196))
    rl_max_per_scene = int(regime_data.get("max_windows_per_scene", 10))
    dataset = ETH3DLongSequenceDataset(
        root=root,
        sequence_length=rl_seq_len,
        max_windows_per_scene=rl_max_per_scene,
        image_size=rl_img_size,
        n_patches=rl_n_patches,
        scenes=rl_scenes,
        dense_gt=True,
    )
    sample_index = {s["sequence_name"]: idx for idx, s in enumerate(dataset.samples)}
    for seq in regime_sequences:
        idx = sample_index.get(seq)
        if idx is None:
            continue
        yield seq, dataset[idx]


def build_cache(
    dataset_name: str,
    root: str,
    regime_labels: str,
    output: str,
    preset: str = "small_real",
    window_frames: int = 4,
    image_size: int = 224,
):
    """One pass of V04Pipeline.forward() per window; saves head inputs + GT."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Stage 6 cache build ({dataset_name}, preset={preset}) ===", flush=True)
    print(f"  device: {device}", flush=True)

    model = build_dream3r(preset)
    model.eval()
    pipeline = build_v04_pipeline(model, max_repair_attempts=1).to(device)

    if dataset_name == "kitti_long":
        iterator = _iter_kitti_windows(root, regime_labels, window_frames)
    elif dataset_name == "eth3d_long":
        iterator = _iter_eth3d_windows(root, regime_labels, window_frames)
    else:
        raise ValueError(f"unknown dataset: {dataset_name}")

    entries: List[Dict] = []
    d_memory: Optional[int] = None
    t_start = time.time()
    for idx, (seq, sample) in enumerate(iterator):
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0)         # [1, N, P, 3]
        mask = sample["pointmap_mask"][0].unsqueeze(0)         # [1, N, P]

        with torch.no_grad():
            out = pipeline(images=images, timestep=0)

        expert = out.expert
        memory = out.memory
        critic = out.critic
        if expert is None or memory is None or critic is None:
            print(f"  [{idx+1}] {seq}: SKIP (missing contracts)", flush=True)
            continue

        memory_context = memory.fused_context.detach().cpu().squeeze(0) \
            if memory.fused_context is not None else None
        if memory_context is not None and d_memory is None:
            d_memory = int(memory_context.shape[-1])

        entry = {
            "seq": seq,
            "expert_name": expert.expert_name,
            "expert_pointmap": expert.pointmap.detach().cpu().squeeze(0),     # [N, P, 3]
            "expert_confidence": expert.confidence.detach().cpu().squeeze(0), # [N, P, 1]
            "memory_context": memory_context,                                   # [D_mem]
            "conflict_score": float(critic.conflict_score.flatten()[0].item()),
            "gt_pointmap": target.squeeze(0).cpu(),                             # [N, P, 3]
            "gt_mask": mask.squeeze(0).cpu(),                                   # [N, P]
        }
        entries.append(entry)
        elapsed = time.time() - t_start
        print(f"  [{idx+1}] {seq}: ok (elapsed={elapsed:.1f}s)", flush=True)

    blob = {
        "dataset": dataset_name,
        "preset": preset,
        "n_windows": len(entries),
        "d_memory": d_memory,
        "entries": entries,
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(blob, output_path)
    print(f"\nSaved cache to {output_path}", flush=True)
    print(f"  n_windows: {len(entries)}, d_memory: {d_memory}", flush=True)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------


def _abs_rel_loss(pred: torch.Tensor, target: torch.Tensor,
                  mask: torch.Tensor, align_scale: bool = True) -> torch.Tensor:
    """Differentiable scale-aligned abs_rel; scale factor is detached so the
    head cannot game by shrinking predictions."""
    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (target_depth.abs() > 1e-6)
    )
    if not bool(valid.any()):
        return pred.sum() * 0.0
    if align_scale:
        with torch.no_grad():
            denom = pred_depth[valid].detach().median()
            denom = torch.where(denom.abs() > 1e-6, denom, denom.new_tensor(1e-6))
            scale = target_depth[valid].median() / denom
        pred_depth = pred_depth * scale
    rel = (pred_depth - target_depth).abs() / target_depth.abs().clamp_min(1e-6)
    return rel[valid].mean()


def _load_caches(paths: List[str]) -> Tuple[List[Dict], int]:
    entries: List[Dict] = []
    d_memory: Optional[int] = None
    for p in paths:
        blob = torch.load(p, map_location="cpu", weights_only=False)
        for e in blob["entries"]:
            e = dict(e)
            e["domain"] = "kitti" if blob["dataset"] == "kitti_long" else "eth3d"
            entries.append(e)
        if blob.get("d_memory") is not None:
            if d_memory is None:
                d_memory = int(blob["d_memory"])
            elif d_memory != int(blob["d_memory"]):
                raise ValueError(
                    f"d_memory mismatch across caches: {d_memory} vs {blob['d_memory']}"
                )
    if d_memory is None:
        raise ValueError("none of the caches recorded d_memory")
    return entries, d_memory


def _stratified_split(entries: List[Dict], seed: int, holdout_frac: float = 0.2):
    """Per-domain 80/20 split with given seed."""
    by_domain: Dict[str, List[int]] = {}
    for i, e in enumerate(entries):
        by_domain.setdefault(e["domain"], []).append(i)
    rng = random.Random(seed)
    train_idx, test_idx = [], []
    for dom, idxs in by_domain.items():
        rng.shuffle(idxs)
        n_test = max(1, int(round(len(idxs) * holdout_frac)))
        test_idx.extend(idxs[:n_test])
        train_idx.extend(idxs[n_test:])
    return sorted(train_idx), sorted(test_idx)


def _eval_split(entries: List[Dict], indices: List[int], head: Stage6FusionHead,
                device: torch.device) -> Dict[str, Dict[str, float]]:
    """Return per-domain abs_rel for baseline (expert.pointmap) vs head."""
    head.eval()
    sums: Dict[str, Dict[str, float]] = {}
    counts: Dict[str, int] = {}
    with torch.no_grad():
        for i in indices:
            e = entries[i]
            ep = e["expert_pointmap"].unsqueeze(0).to(device)
            ec = e["expert_confidence"].unsqueeze(0).to(device)
            mc = e["memory_context"].unsqueeze(0).to(device) \
                if e["memory_context"] is not None else None
            cs = torch.tensor([[e["conflict_score"]]], device=device)
            gt = e["gt_pointmap"].unsqueeze(0).to(device)
            mask = e["gt_mask"].unsqueeze(0).to(device)

            base_abs_rel = _pointmap_abs_rel(ep, gt, mask, align_scale=True)
            refined = head(ep, ec, mc, cs)
            head_abs_rel = _pointmap_abs_rel(refined, gt, mask, align_scale=True)

            d = e["domain"]
            sums.setdefault(d, {"baseline": 0.0, "head": 0.0})
            sums[d]["baseline"] += float(base_abs_rel)
            sums[d]["head"] += float(head_abs_rel)
            counts[d] = counts.get(d, 0) + 1
    head.train()
    means: Dict[str, Dict[str, float]] = {}
    for d in sums:
        n = max(1, counts[d])
        means[d] = {
            "baseline_mean_abs_rel": sums[d]["baseline"] / n,
            "head_mean_abs_rel": sums[d]["head"] / n,
            "delta_pp": (sums[d]["baseline"] - sums[d]["head"]) / max(sums[d]["baseline"], 1e-9) * 100,
            "n_windows": int(n),
        }
    return means


def train_fusion_head(
    cache_paths: List[str],
    output_dir: str,
    seed: int = 7,
    epochs: int = 300,
    lr: float = 1e-3,
    head_dim: int = 64,
    hidden: int = 128,
    holdout_frac: float = 0.2,
) -> Dict[str, object]:
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    entries, d_memory = _load_caches(cache_paths)
    print(f"loaded {len(entries)} cache entries, d_memory={d_memory}", flush=True)

    head = Stage6FusionHead(d_memory=d_memory, head_dim=head_dim, hidden=hidden).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=lr)

    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    print(f"split: train={len(train_idx)} test={len(test_idx)} (seed={seed})", flush=True)

    losses: List[float] = []
    best_delta_kitti = -1e9
    best_delta_eth3d = -1e9

    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        epoch_loss = 0.0
        n = 0
        for i in order:
            e = entries[i]
            ep = e["expert_pointmap"].unsqueeze(0).to(device)
            ec = e["expert_confidence"].unsqueeze(0).to(device)
            mc = e["memory_context"].unsqueeze(0).to(device) \
                if e["memory_context"] is not None else None
            cs = torch.tensor([[e["conflict_score"]]], device=device)
            gt = e["gt_pointmap"].unsqueeze(0).to(device)
            mask = e["gt_mask"].unsqueeze(0).to(device)

            refined = head(ep, ec, mc, cs)
            loss = _abs_rel_loss(refined, gt, mask, align_scale=True)
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss)
            n += 1
        epoch_loss /= max(1, n)
        losses.append(epoch_loss)
        if (epoch + 1) % 20 == 0 or epoch == 0:
            ev = _eval_split(entries, test_idx, head, device)
            print(
                f"epoch {epoch+1:4d}  loss={epoch_loss:.5f}  "
                f"K[base={ev.get('kitti', {}).get('baseline_mean_abs_rel', float('nan')):.4f} "
                f"head={ev.get('kitti', {}).get('head_mean_abs_rel', float('nan')):.4f} "
                f"Δ={ev.get('kitti', {}).get('delta_pp', float('nan')):+.2f}pp]  "
                f"E[base={ev.get('eth3d', {}).get('baseline_mean_abs_rel', float('nan')):.4f} "
                f"head={ev.get('eth3d', {}).get('head_mean_abs_rel', float('nan')):.4f} "
                f"Δ={ev.get('eth3d', {}).get('delta_pp', float('nan')):+.2f}pp]",
                flush=True,
            )

    final_eval = _eval_split(entries, test_idx, head, device)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "head_state_dict": head.state_dict(),
        "config": {
            "d_memory": d_memory,
            "head_dim": head_dim,
            "hidden": hidden,
        },
        "seed": seed,
        "epochs": epochs,
        "lr": lr,
        "train_indices": train_idx,
        "test_indices": test_idx,
        "loss_curve": losses,
        "final_eval": final_eval,
    }, output_path / "latest.pt")

    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "d_memory": d_memory,
        "final_train_loss": losses[-1] if losses else None,
        "loss_decrease_pct": (losses[0] - losses[-1]) / max(losses[0], 1e-9) * 100 if len(losses) >= 2 else 0.0,
        "final_eval": final_eval,
    }
    (output_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved head + results to {output_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode")

    p_cache = sub.add_parser("build-cache", help="run V04Pipeline per window, save head inputs + GT")
    p_cache.add_argument("--dataset", choices=["kitti_long", "eth3d_long"], required=True)
    p_cache.add_argument("--root", default="/hdd3/kykt26/data")
    p_cache.add_argument("--regime-labels", required=True)
    p_cache.add_argument("--output", required=True)
    p_cache.add_argument("--preset", default="small_real")
    p_cache.add_argument("--window-frames", type=int, default=4)
    p_cache.add_argument("--image-size", type=int, default=224)

    p_train = sub.add_parser("train", help="train head on cached inputs")
    p_train.add_argument("--cache", nargs="+", required=True)
    p_train.add_argument("--output-dir", required=True)
    p_train.add_argument("--seed", type=int, default=7)
    p_train.add_argument("--epochs", type=int, default=300)
    p_train.add_argument("--lr", type=float, default=1e-3)
    p_train.add_argument("--head-dim", type=int, default=64)
    p_train.add_argument("--hidden", type=int, default=128)
    p_train.add_argument("--holdout-frac", type=float, default=0.2)

    args = parser.parse_args()
    if args.mode == "build-cache":
        build_cache(
            dataset_name=args.dataset,
            root=args.root,
            regime_labels=args.regime_labels,
            output=args.output,
            preset=args.preset,
            window_frames=args.window_frames,
            image_size=args.image_size,
        )
    elif args.mode == "train":
        train_fusion_head(
            cache_paths=args.cache,
            output_dir=args.output_dir,
            seed=args.seed,
            epochs=args.epochs,
            lr=args.lr,
            head_dim=args.head_dim,
            hidden=args.hidden,
            holdout_frac=args.holdout_frac,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
