"""
Dream3R v0.3 training script.

Supports:
  - DDP multi-GPU (2-3 cards, CUDA_VISIBLE_DEVICES to pick)
  - Mixed precision (torch.amp)
  - Checkpoint save/resume
  - TensorBoard logging with per-bus-signal traces
  - Gradient clipping
  - Multi-stage LR schedule (warmup -> partial unfreeze -> full cosine)
  - Synthetic or DTU dataset
  - v0.3 loss terms (retrieval, routing, drift_consistency)

Usage:
    # Single GPU
    python -m dream3r.train --preset small --gpus 0

    # 2-GPU DDP
    torchrun --nproc_per_node=2 -m dream3r.train --preset small --gpus 0,1

    # Resume from checkpoint
    torchrun --nproc_per_node=2 -m dream3r.train --resume checkpoints/latest.pt
"""

import os
import sys
import argparse
import time
import math
from pathlib import Path

import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

try:
    from tqdm.auto import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from dream3r.config import load_config, save_config, config_to_model_args
from dream3r.model import Dream3R
from dream3r.losses import Dream3RLoss
from dream3r.data.synthetic import SyntheticSequenceDataset, DTUDataset


# ---------------------------------------------------------------------------
# DDP utilities
# ---------------------------------------------------------------------------

def setup_ddp(rank: int, world_size: int, backend: str = "nccl"):
    dist.init_process_group(backend, rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)


def cleanup_ddp():
    if dist.is_initialized():
        dist.destroy_process_group()


def is_main_process() -> bool:
    return not dist.is_initialized() or dist.get_rank() == 0


# ---------------------------------------------------------------------------
# Checkpoint I/O
# ---------------------------------------------------------------------------

def save_checkpoint(model: nn.Module, optimizer, scaler, epoch: int,
                    step: int, cfg: dict, path: str):
    state = {
        "epoch": epoch,
        "step": step,
        "cfg": cfg,
        "model": model.module.state_dict() if hasattr(model, "module") else model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "scaler": scaler.state_dict() if scaler else None,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, path)


def load_checkpoint(path: str, model: nn.Module, optimizer=None, scaler=None):
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    m = model.module if hasattr(model, "module") else model
    m.load_state_dict(ckpt["model"])
    if optimizer and "optimizer" in ckpt:
        optimizer.load_state_dict(ckpt["optimizer"])
    if scaler and ckpt.get("scaler"):
        scaler.load_state_dict(ckpt["scaler"])
    return ckpt.get("epoch", 0), ckpt.get("step", 0)


# ---------------------------------------------------------------------------
# Multi-stage LR scheduler
# ---------------------------------------------------------------------------

class MultiStageScheduler:
    """
    3-stage LR schedule with actual parameter freeze/unfreeze:
      Stage 1 (warmup):  linear ramp, only heads trainable (backbone frozen)
      Stage 2 (partial):  constant lr, backbone partially unfrozen
      Stage 3 (full):     cosine decay, all parameters unfrozen
    """

    def __init__(self, optimizer, cfg: dict, model: nn.Module = None):
        self.optimizer = optimizer
        self.model = model
        self.warmup = cfg.get("warmup_epochs", 5)
        self.total = cfg.get("epochs", 100)
        self.base_lr = cfg.get("lr", 1e-4)
        self.stage2_start = self.warmup
        self.stage3_start = self.warmup + (self.total - self.warmup) // 3
        self._current_stage = None

    def step(self, epoch: int) -> float:
        if epoch < self.warmup:
            lr = self.base_lr * (epoch + 1) / self.warmup
        elif epoch < self.stage3_start:
            lr = self.base_lr
        else:
            progress = (epoch - self.stage3_start) / max(1, self.total - self.stage3_start)
            lr = self.base_lr * 0.5 * (1 + math.cos(math.pi * progress))
        for pg in self.optimizer.param_groups:
            pg["lr"] = lr

        stage = self.get_stage(epoch)
        if stage != self._current_stage:
            self._apply_freeze(stage)
            self._current_stage = stage

        return lr

    def _apply_freeze(self, stage: str):
        if self.model is None:
            return
        m = self.model.module if hasattr(self.model, "module") else self.model

        if stage == "warmup":
            if hasattr(m, "perceiver") and hasattr(m.perceiver, "backbone"):
                if m.perceiver.backbone is not None:
                    for p in m.perceiver.backbone.parameters():
                        p.requires_grad = False
        elif stage == "partial_unfreeze":
            if hasattr(m, "perceiver") and hasattr(m.perceiver, "backbone"):
                if m.perceiver.backbone is not None:
                    layers = list(m.perceiver.backbone.parameters())
                    n_unfreeze = max(1, len(layers) // 3)
                    for p in layers[-n_unfreeze:]:
                        p.requires_grad = True
        elif stage == "full_unfreeze":
            for p in m.parameters():
                p.requires_grad = True

    def get_stage(self, epoch: int) -> str:
        if epoch < self.warmup:
            return "warmup"
        elif epoch < self.stage3_start:
            return "partial_unfreeze"
        return "full_unfreeze"


# ---------------------------------------------------------------------------
# Dataset builders
# ---------------------------------------------------------------------------

def build_datasets(cfg: dict):
    if cfg.get("dataset", "synthetic") == "dtu":
        train_ds = DTUDataset(cfg.get("data_root", "/hdd3/kykt26/data/dtu"), "train")
        val_ds = DTUDataset(cfg.get("data_root", "/hdd3/kykt26/data/dtu"), "val")
    else:
        train_ds = SyntheticSequenceDataset(
            n_sequences=cfg.get("n_train_sequences", 500),
            n_frames=cfg.get("n_frames_per_window", 4),
            n_slots=cfg.get("n_slots", 16),
            n_regimes=cfg.get("n_regimes", 5),
            d_model=cfg.get("d_model", 768),
            sequence_length=cfg.get("sequence_length", 3),
            seed=42,
        )
        val_ds = SyntheticSequenceDataset(
            n_sequences=cfg.get("n_val_sequences", 50),
            n_frames=cfg.get("n_frames_per_window", 4),
            n_slots=cfg.get("n_slots", 16),
            n_regimes=cfg.get("n_regimes", 5),
            d_model=cfg.get("d_model", 768),
            sequence_length=cfg.get("sequence_length", 3),
            seed=1337,
        )
    return train_ds, val_ds


def collate_synthetic(batch):
    keys = batch[0].keys()
    return {k: torch.stack([b[k] for b in batch]) for k in keys}


def _window_value(value: torch.Tensor, t: int, sequence_length: int) -> torch.Tensor:
    if sequence_length > 1 and value.dim() >= 2:
        return value[:, t]
    return value


def _make_targets(batch: dict, device: torch.device, t: int,
                  sequence_length: int) -> dict:
    targets = {
        "pointmap": _window_value(batch["pointmap_gt"].to(device, non_blocking=True), t, sequence_length),
        "conflict_label": _window_value(batch["conflict_label"].to(device, non_blocking=True), t, sequence_length),
        "repair_label": _window_value(batch["repair_label"].to(device, non_blocking=True), t, sequence_length),
        "region_label": _window_value(batch["region_label"].to(device, non_blocking=True), t, sequence_length),
    }
    if "pointmap_change" in batch:
        targets["pointmap_change"] = _window_value(
            batch["pointmap_change"].to(device, non_blocking=True), t, sequence_length
        )
    if sequence_length > 1 and t > 0 and "pointmap_gt" in batch:
        pointmaps = batch["pointmap_gt"].to(device, non_blocking=True)
        targets["prev_pointmap"] = pointmaps[:, t - 1]
    if sequence_length > 1 and t > 0 and "pointmap_mask" in batch:
        masks = batch["pointmap_mask"].to(device, non_blocking=True)
        targets["prev_pointmap_mask"] = masks[:, t - 1]
    return targets


def _forward_sequence(model: nn.Module, batch: dict, loss_fn: nn.Module,
                      device: torch.device, tbptt_detach_every: int = 1):
    x = batch["features"].to(device, non_blocking=True)
    regime = batch["regime"].to(device, non_blocking=True)
    sequence_length = x.shape[1] if x.dim() == 5 else 1

    prev_state = None
    prev_slots = None
    total_loss = None
    last_outputs = None
    loss_sums = {}
    prev_pointmap_pred = None

    for t in range(sequence_length):
        x_t = x[:, t] if sequence_length > 1 else x
        regime_t = regime[:, t] if sequence_length > 1 and regime.dim() == 3 else regime
        targets_t = _make_targets(batch, device, t, sequence_length)

        outputs = model(
            x_t, regime_t,
            prev_memory_state=prev_state,
            prev_object_slots=prev_slots,
            timestep=t,
        )
        if prev_pointmap_pred is not None:
            outputs["prev_pointmap"] = prev_pointmap_pred.detach()
        losses = loss_fn(outputs, targets_t)
        total_loss = losses["total"] if total_loss is None else total_loss + losses["total"]

        for key, value in losses.items():
            if isinstance(value, torch.Tensor):
                loss_sums[key] = loss_sums.get(key, 0.0) + value.detach()

        prev_state = outputs.get("latent_state_tokens", outputs.get("latent_state"))
        prev_slots = outputs.get("object_track_set")
        if tbptt_detach_every > 0 and (t + 1) % tbptt_detach_every == 0:
            if prev_state is not None:
                prev_state = prev_state.detach()
            if prev_slots is not None:
                prev_slots = prev_slots.detach()
        prev_pointmap_pred = outputs["pointmap"]
        last_outputs = outputs

    loss_avg = {
        key: value / sequence_length
        for key, value in loss_sums.items()
    }
    loss_avg["total"] = total_loss / sequence_length
    return last_outputs, loss_avg


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------

def train(cfg: dict):
    local_rank = int(os.environ.get("LOCAL_RANK", 0))
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    is_ddp = world_size > 1

    if is_ddp:
        setup_ddp(local_rank, world_size, cfg["dist_backend"])

    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_device(device)

    model_cfg = config_to_model_args(cfg)
    model = Dream3R(model_cfg).to(device)
    if is_ddp:
        model = DDP(model, device_ids=[local_rank], find_unused_parameters=True)

    if cfg.get("gradient_checkpointing", False):
        raw = model.module if hasattr(model, "module") else model
        raw.enable_gradient_checkpointing(True)

    if is_main_process():
        n_params = sum(p.numel() for p in model.parameters())
        version = cfg.get("version", "v03")
        print(f"Dream3R [{version}]: {n_params:,} params | {world_size} GPU(s) | AMP={cfg['amp']}")

    loss_fn = Dream3RLoss(weights={
        "pointmap": cfg["w_pointmap"],
        "critic_p1": cfg["w_critic_p1"],
        "critic_p5": cfg["w_critic_p5"],
        "memory_p2": cfg["w_memory_p2"],
        "memory_p3": cfg["w_memory_p3"],
        "permanence_p4": cfg["w_permanence_p4"],
        "action_entropy": cfg["w_action_entropy"],
        "retrieval": cfg.get("w_retrieval", 0.1),
        "retrieval_quality": cfg.get("w_retrieval_quality", 0.05),
        "routing": cfg.get("w_routing", 0.05),
        "geometric_consistency": cfg.get("w_geometric_consistency", 0.05),
        "sampson_distance": cfg.get("w_sampson_distance", 0.05),
        "covisibility_consistency": cfg.get("w_covisibility_consistency", 0.05),
        "drift_consistency": cfg.get("w_drift_consistency", 0.1),
        "state_drift_regularization": cfg.get("w_state_drift_regularization", 0.01),
    }).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg["lr"], weight_decay=cfg["weight_decay"],
    )
    scheduler = MultiStageScheduler(optimizer, cfg, model=model)
    use_amp = cfg["amp"] and device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda") if use_amp else None

    train_ds, val_ds = build_datasets(cfg)
    sampler = DistributedSampler(train_ds) if is_ddp else None
    train_loader = DataLoader(
        train_ds, batch_size=cfg["batch_size"],
        sampler=sampler, shuffle=(sampler is None),
        num_workers=cfg["num_workers"], pin_memory=True,
        drop_last=True, collate_fn=collate_synthetic,
    )
    val_loader = DataLoader(
        val_ds, batch_size=cfg["batch_size"], shuffle=False,
        num_workers=cfg["num_workers"], pin_memory=True,
        collate_fn=collate_synthetic,
    )

    writer = None
    if is_main_process():
        try:
            from torch.utils.tensorboard import SummaryWriter
            log_dir = Path(cfg["log_dir"]) / time.strftime("%Y%m%d-%H%M%S")
            writer = SummaryWriter(str(log_dir))
            save_config(cfg, str(log_dir / "config.yaml"))
            print(f"Logging to {log_dir}")
        except ImportError:
            try:
                from tensorboardX import SummaryWriter
                log_dir = Path(cfg["log_dir"]) / time.strftime("%Y%m%d-%H%M%S")
                writer = SummaryWriter(str(log_dir))
                save_config(cfg, str(log_dir / "config.yaml"))
            except ImportError:
                print("No TensorBoard writer available, skipping logging")

    start_epoch, global_step = 0, 0
    resume_path = cfg.get("resume")
    if resume_path and Path(resume_path).exists():
        start_epoch, global_step = load_checkpoint(resume_path, model, optimizer, scaler)
        if is_main_process():
            print(f"Resumed from {resume_path} (epoch {start_epoch}, step {global_step})")

    use_tqdm = HAS_TQDM and is_main_process()
    epoch_iter = range(start_epoch, cfg["epochs"])
    if use_tqdm:
        epoch_iter = tqdm(epoch_iter, desc="Epochs", position=0,
                          unit="ep", dynamic_ncols=True)

    for epoch in epoch_iter:
        if sampler:
            sampler.set_epoch(epoch)

        lr = scheduler.step(epoch)
        stage = scheduler.get_stage(epoch)

        model.train()
        epoch_loss = 0.0
        t0 = time.time()

        if use_tqdm:
            step_iter = tqdm(
                enumerate(train_loader),
                total=len(train_loader),
                desc=f"  ep{epoch+1:02d}/{cfg['epochs']} [{stage}]",
                position=1, leave=False, unit="batch",
                dynamic_ncols=True, mininterval=0.5,
            )
        else:
            step_iter = enumerate(train_loader)

        for batch_idx, batch in step_iter:
            optimizer.zero_grad(set_to_none=True)
            tbptt = cfg.get("tbptt_detach_every", 1)

            if use_amp:
                with torch.amp.autocast("cuda"):
                    outputs, losses = _forward_sequence(model, batch, loss_fn, device, tbptt)
                scaler.scale(losses["total"]).backward()
                scaler.unscale_(optimizer)
                nn.utils.clip_grad_norm_(model.parameters(), cfg["grad_clip"])
                scaler.step(optimizer)
                scaler.update()
            else:
                outputs, losses = _forward_sequence(model, batch, loss_fn, device, tbptt)
                losses["total"].backward()
                nn.utils.clip_grad_norm_(model.parameters(), cfg["grad_clip"])
                optimizer.step()

            loss_val = losses["total"].item()
            epoch_loss += loss_val
            global_step += 1

            if use_tqdm:
                postfix = {"loss": f"{loss_val:.3f}", "lr": f"{lr:.1e}"}
                if "pointmap" in losses:
                    postfix["pm"] = f"{losses['pointmap'].item():.3f}"
                if "critic_p1" in losses:
                    postfix["c1"] = f"{losses['critic_p1'].item():.3f}"
                step_iter.set_postfix(postfix)

            if is_main_process() and global_step % cfg["log_every"] == 0:
                if writer:
                    for k, v in losses.items():
                        if isinstance(v, torch.Tensor):
                            writer.add_scalar(f"loss/{k}", v.item(), global_step)
                    if "update_probs" in outputs:
                        probs = outputs["update_probs"].detach().mean(0)
                        modes = ["full", "pose_adpt", "kalman", "skip", "reset"]
                        for i, name in enumerate(modes):
                            writer.add_scalar(f"a1_mode/{name}", probs[i].item(), global_step)
                    if "nsa_branch_weights" in outputs:
                        bw = outputs["nsa_branch_weights"].detach().mean(dim=(0, 1))
                        for i, name in enumerate(["compressed", "selected", "sliding"]):
                            writer.add_scalar(f"memory/branch_{name}", bw[i].item(), global_step)
                    if "bank_occupancy" in outputs:
                        occ = outputs["bank_occupancy"]
                        if isinstance(occ, torch.Tensor):
                            writer.add_scalar("memory/bank_occupancy", occ.mean().item(), global_step)
                    if "route_regret" in outputs:
                        writer.add_scalar("composer/route_regret",
                                          outputs["route_regret"].mean().item(), global_step)
                    writer.add_scalar("train/lr", lr, global_step)

        if use_tqdm:
            step_iter.close()

        dt = time.time() - t0
        avg = epoch_loss / max(len(train_loader), 1)

        if is_main_process():
            msg = (f"  epoch {epoch+1:3d}/{cfg['epochs']}  loss={avg:.4f}  "
                   f"lr={lr:.2e}  stage={stage}  time={dt:.1f}s")
            if use_tqdm:
                tqdm.write(msg)
                epoch_iter.set_postfix(loss=f"{avg:.3f}", stage=stage)
            else:
                print(msg, flush=True)

            if writer:
                writer.add_scalar("epoch/loss", avg, epoch)

            if (epoch + 1) % cfg.get("eval_every_epoch", 5) == 0:
                model.eval()
                val_loss = 0.0
                n_val = 0
                with torch.no_grad():
                    for batch in val_loader:
                        outputs, losses = _forward_sequence(
                            model, batch, loss_fn, device,
                            cfg.get("tbptt_detach_every", 1),
                        )
                        val_loss += losses["total"].item()
                        n_val += 1
                avg_val = val_loss / max(n_val, 1)
                print(f"    val_loss={avg_val:.4f}")
                if writer:
                    writer.add_scalar("val/loss", avg_val, epoch)

            if (epoch + 1) % cfg["save_every_epoch"] == 0:
                path = Path(cfg["save_dir"]) / f"epoch_{epoch+1:04d}.pt"
                save_checkpoint(model, optimizer, scaler, epoch + 1, global_step, cfg, str(path))
                print(f"    saved {path}")

    if is_main_process():
        path = Path(cfg["save_dir"]) / "latest.pt"
        save_checkpoint(model, optimizer, scaler, cfg["epochs"], global_step, cfg, str(path))
        print(f"Training done. Final checkpoint: {path}")
        if writer:
            writer.close()

    cleanup_ddp()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Dream3R v0.3 training")
    parser.add_argument("--preset", default="small", help="Config preset name")
    parser.add_argument("--config", default=None, help="Path to YAML config")
    parser.add_argument("--resume", default=None, help="Path to checkpoint")
    parser.add_argument("--gpus", default=None, help="GPU ids (e.g. 0,1)")
    parser.add_argument("--dataset", default=None, help="Dataset: synthetic/dtu")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch_size", type=int, default=None)
    parser.add_argument("--lr", type=float, default=None)
    args = parser.parse_args()

    overrides = {}
    if args.resume:
        overrides["resume"] = args.resume
    if args.gpus:
        overrides["gpus"] = args.gpus
    if args.dataset:
        overrides["dataset"] = args.dataset
    if args.epochs:
        overrides["epochs"] = args.epochs
    if args.batch_size:
        overrides["batch_size"] = args.batch_size
    if args.lr:
        overrides["lr"] = args.lr

    cfg = load_config(path=args.config, preset=args.preset, overrides=overrides)

    if "WORLD_SIZE" not in os.environ:
        gpu_list = cfg["gpus"].split(",")
        os.environ["CUDA_VISIBLE_DEVICES"] = cfg["gpus"]
        if len(gpu_list) == 1:
            train(cfg)
        else:
            print(f"Use torchrun for multi-GPU: torchrun --nproc_per_node={len(gpu_list)} -m dream3r.train")
            sys.exit(1)
    else:
        train(cfg)


if __name__ == "__main__":
    main()
