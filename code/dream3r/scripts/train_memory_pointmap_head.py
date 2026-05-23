"""Train the external memory-conditioned pointmap residual head."""

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple

import torch
import torch.nn.functional as F

from dream3r.config import config_to_model_args, load_config
from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.memory_pointmap_head import MemoryPointmapResidualHead
from dream3r.model import Dream3R


def _load_model(checkpoint: str, device: torch.device) -> Dream3R:
    cfg = load_config(preset="memory_only")
    model = Dream3R(config_to_model_args(cfg)).to(device)
    ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
    state = ckpt.get("model", ckpt)
    current = model.state_dict()
    compatible = {
        key: value for key, value in state.items()
        if key in current and current[key].shape == value.shape
    }
    model.load_state_dict(compatible, strict=False)
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    return model


def _dataset(data_root: str, max_sequences: int, max_frames: int) -> KITTILongSequenceDataset:
    cfg = load_config(preset="memory_only")
    return KITTILongSequenceDataset(
        root=data_root,
        sequence_length=cfg.get("kitti_window_frames", 8),
        overlap=cfg.get("kitti_window_overlap", 4),
        windows_per_sample=1,
        min_sequence_frames=cfg.get("kitti_min_sequence_frames", 50),
        max_frames_per_sequence=max_frames,
        max_sequences=max_sequences,
        n_patches=196,
        d_model=cfg.get("d_model", 768),
        n_regimes=cfg.get("n_regimes", 6),
        n_slots=cfg.get("n_slots", 16),
    )


def _pointmap_loss(pred: torch.Tensor, gt: torch.Tensor,
                   mask: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
    valid = mask.float().unsqueeze(-1)
    mse = ((pred - gt) ** 2 * valid).sum() / (valid.sum() * 3 + 1e-8)
    pred_depth = pred[..., 2]
    gt_depth = gt[..., 2]
    depth_valid = (mask > 0) & torch.isfinite(gt_depth) & (gt_depth > 1e-6)
    if depth_valid.any():
        abs_rel = ((pred_depth[depth_valid] - gt_depth[depth_valid]).abs() / gt_depth[depth_valid]).mean()
    else:
        abs_rel = torch.zeros((), device=pred.device)
    return mse + 0.1 * abs_rel, {"mse": mse.detach(), "abs_rel": abs_rel.detach()}


def _run_epoch(model: Dream3R,
               head: MemoryPointmapResidualHead,
               dataset: KITTILongSequenceDataset,
               indices,
               device: torch.device,
               optimizer=None,
               overlap_frames: int = 4) -> Dict[str, float]:
    train = optimizer is not None
    head.train(train)
    prev_memory = None
    prev_slots = None
    prev_slot_poses = None
    prev_corrected = None
    totals = {"loss": 0.0, "mse": 0.0, "abs_rel": 0.0}

    for count, idx in enumerate(indices, start=1):
        sample = dataset[idx]
        features = sample["features"][0].unsqueeze(0).to(device)
        gt = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(
                features,
                prev_memory_state=prev_memory,
                prev_object_slots=prev_slots,
                prev_object_slot_poses=prev_slot_poses,
                timestep=idx,
            )
            raw_pointmap = outputs["pointmap"].detach()
            latent = outputs["latent_state_tokens"].detach()

        corrected, _ = head(
            raw_pointmap,
            latent,
            prev_pointmap=prev_corrected,
            overlap_frames=overlap_frames,
        )
        loss, parts = _pointmap_loss(corrected, gt, mask)
        if prev_corrected is not None and overlap_frames > 0:
            overlap = min(overlap_frames, corrected.shape[1], prev_corrected.shape[1])
            overlap_loss = F.mse_loss(corrected[:, :overlap], prev_corrected[:, -overlap:].detach())
            loss = loss + 0.1 * overlap_loss
        if train:
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

        totals["loss"] += float(loss.detach().item())
        totals["mse"] += float(parts["mse"].item())
        totals["abs_rel"] += float(parts["abs_rel"].item())

        prev_memory = latent
        prev_slots = outputs.get("object_track_set")
        prev_slot_poses = outputs.get("object_slot_poses")
        prev_corrected = corrected.detach()

    denom = max(len(indices), 1)
    return {key: value / denom for key, value in totals.items()}


def train_memory_pointmap_head(
    memory_checkpoint: str = "/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt",
    output: str = "/hdd3/kykt26/checkpoints/memory_pointmap_head_v1/latest.pt",
    data_root: str = "/hdd3/kykt26/data",
    epochs: int = 8,
    train_windows: int = 40,
    val_windows: int = 20,
    max_sequences: int = 4,
    max_frames: int = 100,
    lr: float = 1e-3,
    overlap_frames: int = 4,
    device_name: str = "auto",
) -> Dict[str, object]:
    device = torch.device(
        "cuda" if device_name == "auto" and torch.cuda.is_available()
        else "cpu" if device_name == "auto"
        else device_name
    )
    dataset = _dataset(data_root, max_sequences=max_sequences, max_frames=max_frames)
    needed = train_windows + val_windows
    if len(dataset) < needed:
        raise RuntimeError(f"Need {needed} windows, found {len(dataset)}")

    model = _load_model(memory_checkpoint, device)
    head = MemoryPointmapResidualHead().to(device)
    optimizer = torch.optim.AdamW(head.parameters(), lr=lr, weight_decay=1e-4)
    train_indices = list(range(train_windows))
    val_indices = list(range(train_windows, train_windows + val_windows))
    history = []

    for epoch in range(epochs):
        train_metrics = _run_epoch(
            model, head, dataset, train_indices, device, optimizer, overlap_frames
        )
        with torch.no_grad():
            val_metrics = _run_epoch(
                model, head, dataset, val_indices, device, None, overlap_frames
            )
        row = {"epoch": epoch + 1, "train": train_metrics, "val": val_metrics}
        history.append(row)
        print(json.dumps(row), flush=True)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "head": head.state_dict(),
        "history": history,
        "memory_checkpoint": memory_checkpoint,
        "config": {
            "epochs": epochs,
            "train_windows": train_windows,
            "val_windows": val_windows,
            "max_sequences": max_sequences,
            "max_frames": max_frames,
            "lr": lr,
            "overlap_frames": overlap_frames,
        },
    }, output_path)
    return {"output": str(output_path), "history": history}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-checkpoint", default="/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt")
    parser.add_argument("--output", default="/hdd3/kykt26/checkpoints/memory_pointmap_head_v1/latest.pt")
    parser.add_argument("--data-root", default="/hdd3/kykt26/data")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--train-windows", type=int, default=40)
    parser.add_argument("--val-windows", type=int, default=20)
    parser.add_argument("--max-sequences", type=int, default=4)
    parser.add_argument("--max-frames", type=int, default=100)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--overlap-frames", type=int, default=4)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()

    result = train_memory_pointmap_head(
        memory_checkpoint=args.memory_checkpoint,
        output=args.output,
        data_root=args.data_root,
        epochs=args.epochs,
        train_windows=args.train_windows,
        val_windows=args.val_windows,
        max_sequences=args.max_sequences,
        max_frames=args.max_frames,
        lr=args.lr,
        overlap_frames=args.overlap_frames,
        device_name=args.device,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
