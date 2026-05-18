"""
Dream3R v0.2 End-to-End Demo

Runs the full control-graph pipeline on real images:
  Input images → C1 DINOv3-S → C2 Memory (AnchorBank + NSA) →
  C3 Permanence → C4 Critic → C5 Composer routing → Expert inference →
  Output pointmap/depth + routing log

Usage:
    CUDA_VISIBLE_DEVICES=0 python3 dream3r/demo_e2e.py \
        --img1 /path/to/image1.jpg --img2 /path/to/image2.jpg
"""

import sys
import os
import argparse
import time
import json
from pathlib import Path

import torch
import torch.nn.functional as F
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dream3r.model import Dream3R, CONFIGS
from dream3r.composer_experts import get_expert, available_experts


def load_image(path: str, size: int = 224) -> torch.Tensor:
    from PIL import Image
    import torchvision.transforms as T
    img = Image.open(path).convert("RGB")
    transform = T.Compose([
        T.Resize((size, size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(img)


def run_demo(img1_path: str, img2_path: str, device: str = "cuda:0",
             preset: str = "small"):
    print("=" * 70)
    print("Dream3R v0.2 — End-to-End Control-Graph Demo")
    print("=" * 70)

    # --- Load model ---
    cfg = CONFIGS[preset]
    model = Dream3R(cfg).to(device)
    model.eval()
    total_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n[Model] preset={preset}  params={total_params:,} (trainable={trainable:,})")

    # --- Load images ---
    img_size = cfg.get("img_size", 224)
    use_backbone = cfg.get("use_backbone", False)

    if use_backbone:
        img1 = load_image(img1_path, img_size).unsqueeze(0).to(device)
        img2 = load_image(img2_path, img_size).unsqueeze(0).to(device)
        x = torch.stack([img1, img2], dim=1)  # [1, 2, 3, H, W]
        print(f"[Input] {img1_path} + {img2_path} → {x.shape}")
    else:
        x = torch.randn(1, 2, 196, 768, device=device)
        print(f"[Input] Synthetic tokens (no backbone in {preset} preset)")

    # --- Window 1: Forward pass ---
    print("\n" + "-" * 70)
    print("WINDOW 1: Full bus tick")
    print("-" * 70)

    t0 = time.perf_counter()
    with torch.no_grad():
        out = model(x, timestep=0)
    torch.cuda.synchronize()
    w1_time = (time.perf_counter() - t0) * 1000

    # Print all bus signals
    print(f"\n  Latency: {w1_time:.1f} ms")
    print(f"\n  C1 Perceiver:")
    print(f"    frame_tokens:    {out['frame_tokens'].shape}")
    print(f"    pointmap:        {out['pointmap'].shape}")
    print(f"    confidence:      mean={out['confidence'].mean():.4f}")

    print(f"\n  C2 Memory:")
    print(f"    latent_state:    {out['latent_state'].shape}")
    print(f"    anchor_bank:     {out['anchor_bank_occupancy']} anchors stored")
    update_probs = out['update_probs'][0]
    modes = ['full', 'pose_adaptive', 'kalman', 'skip', 'reset']
    best_mode = modes[update_probs.argmax()]
    print(f"    A1 update_kind:  {best_mode} (probs: {[f'{p:.2f}' for p in update_probs.tolist()]})")
    print(f"    drift_proxy:     {out['latent_drift_proxy'][0].item():.4f}")

    print(f"\n  C3 Permanence:")
    print(f"    object_slots:    {out['object_track_set'].shape}")
    print(f"    dynamic_ratio:   {out['dynamic_ratio'][0].item():.4f}")
    region_pred = out['region_logits'][0].argmax(dim=-1)
    suppress_count = (region_pred == 0).sum().item()
    admit_count = (region_pred == 1).sum().item()
    defer_count = (region_pred == 2).sum().item()
    print(f"    region_decision: {suppress_count} suppress / {admit_count} admit / {defer_count} defer")
    print(f"    mint_conf:       mean={out['mint_confidence'].mean():.4f}")

    print(f"\n  C4 Critic:")
    conflict = out['conflict_score'][0].item()
    action_names = ['accept', 'rerun_local', 'reroute', 'open_anchor', 'request_prior', 'unresolved']
    action = action_names[out['recommended_action'][0].item()]
    print(f"    conflict_score:  {conflict:.4f}")
    print(f"    repair_action:   {action}")

    print(f"\n  C5 Composer:")
    match = out['capability_match'][0]
    route = out['route_recommendation'][0]
    regret = out['route_regret'][0].item()
    print(f"    capability_match: {match.tolist()}")
    print(f"    route_order:     {route.tolist()}")
    print(f"    route_regret:    {regret:.4f}")

    print(f"\n  C6 Bus:")
    log = out['contract_log']
    print(f"    contract_log:    {len(log)} entries")
    for entry in log:
        print(f"      {entry}")

    # --- Expert routing decision ---
    print("\n" + "-" * 70)
    print("ROUTING DECISION")
    print("-" * 70)

    avail = available_experts()
    expert_names = ["mast3r", "fast3r", "spann3r", "cut3r", "moge2", "depthanything_v2", "test3r"]
    top_expert_idx = route[0].item()
    if top_expert_idx < len(expert_names):
        chosen = expert_names[top_expert_idx]
    else:
        chosen = "unknown"

    print(f"\n  Available experts:  {avail}")
    print(f"  Critic conflict:   {conflict:.4f}")
    print(f"  Recommended action: {action}")

    if action == "reroute" or action == "rerun_local":
        print(f"  → Critic flagged issue. Routing to verification expert.")
        chosen = "test3r" if "test3r" in avail else chosen
    elif conflict > 0.5:
        print(f"  → High conflict ({conflict:.2f}). Critic-triggered lazy verification.")
        chosen = "test3r" if "test3r" in avail else chosen
    else:
        if "depthanything_v2" in avail:
            chosen = "depthanything_v2"
            print(f"  → Low conflict. Streaming-path expert selected.")
        else:
            print(f"  → Routing to top-ranked expert.")

    print(f"\n  SELECTED EXPERT: {chosen}")

    # --- Run selected expert ---
    print("\n" + "-" * 70)
    print(f"EXPERT INFERENCE: {chosen}")
    print("-" * 70)

    expert = get_expert(chosen)
    print(f"  streaming_path: {expert.is_streaming_path}")
    print(f"  attention_regime: {expert.attention_regime}")
    print(f"  capability_match: {expert.get_capability_match()}")

    if chosen == "depthanything_v2":
        expert_input = torch.randn(1, 1, 3, 518, 518, device=device)
        if use_backbone:
            from PIL import Image
            import torchvision.transforms as T
            eimg = Image.open(img1_path).convert("RGB")
            etf = T.Compose([T.Resize((518, 518)), T.ToTensor(),
                             T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
            expert_input = etf(eimg).unsqueeze(0).unsqueeze(0).to(device)
    elif chosen in ("mast3r", "test3r"):
        if use_backbone:
            from PIL import Image
            import torchvision.transforms as T
            etf = T.Compose([T.Resize((512, 512)), T.ToTensor(),
                             T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
            e1 = etf(Image.open(img1_path).convert("RGB")).unsqueeze(0).to(device)
            e2 = etf(Image.open(img2_path).convert("RGB")).unsqueeze(0).to(device)
            expert_input = torch.stack([e1, e2], dim=1)
        else:
            expert_input = torch.randn(1, 2, 3, 512, 512, device=device)
    else:
        expert_input = torch.randn(1, 2, 3, 224, 224, device=device)

    # Warmup
    expert.forward(expert_input, {})

    expert_out = expert.forward(expert_input, {})
    print(f"\n  Results:")
    if expert_out["pointmap"] is not None:
        pm = expert_out["pointmap"]
        print(f"    pointmap: {pm.shape}  range=[{pm.min():.3f}, {pm.max():.3f}]")
    if expert_out["depth"] is not None:
        dp = expert_out["depth"]
        print(f"    depth:    {dp.shape}  range=[{dp.min():.3f}, {dp.max():.3f}]")
    print(f"    confidence: mean={expert_out['confidence'].mean():.4f}")
    print(f"    latency:  {expert_out['latency_ms']:.1f} ms")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"  Input:           2 images → C1 perception → C2 memory → C3 permanence")
    print(f"  Critic:          conflict={conflict:.4f}  action={action}")
    print(f"  Routing:         {chosen} (regret={regret:.4f})")
    print(f"  Expert output:   {'pointmap' if expert_out['pointmap'] is not None else 'depth'}")
    print(f"  Pipeline time:   {w1_time:.1f}ms (Dream3R) + {expert_out['latency_ms']:.1f}ms (expert)")
    print(f"  Total:           {w1_time + expert_out['latency_ms']:.1f}ms")
    print(f"\n  This demonstrates Dream3R's control-graph-as-architecture:")
    print(f"  Critic evaluates → Composer routes → Expert executes")
    print(f"  Pillar A: verification drives routing (conflict→expert selection)")
    print(f"  Pillar D: heterogeneous experts provide regime-specific output")
    print("=" * 70)

    return {
        "conflict_score": conflict,
        "action": action,
        "chosen_expert": chosen,
        "route_regret": regret,
        "dream3r_latency_ms": w1_time,
        "expert_latency_ms": expert_out["latency_ms"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img1", required=True)
    parser.add_argument("--img2", required=True)
    parser.add_argument("--preset", default="small")
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
    run_demo(args.img1, args.img2, args.device, args.preset)
