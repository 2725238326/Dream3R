"""Phase A: Build per-(window, expert) Critic cache for Stage 5 S1 windows.

For each window in regime_labels and each expert in {fast3r, mast3r, spann3r}:
  1. Load images via KITTILongSequenceDataset.
  2. Run expert adapter -> pointmap, confidence, evidence_tokens.
  3. Build (pointmap_pair, confidence_pair, evidence) the same way
     build_critic_training_data.py does for Stage 4 training data.
  4. Forward trained Critic checkpoint -> conflict_score + repair_logits.
  5. Save per-(window, expert) JSON entry.

This mirrors Stage 4 closure's evaluation pipeline (eval_repair_pipeline_ablation.py)
exactly so the conflict_score distribution is the one the Critic was trained on.

Output JSON schema:

{
  "dataset": "kitti_long",
  "expert_order": ["fast3r", "mast3r", "spann3r"],
  "labels": {
    "<sequence_id>": {
      "<expert>": {
        "conflict_score_raw": float,
        "conflict_score_sigmoid": float,
        "repair_logits": [6 floats],
        "recommended_action_raw": int (0..5),
        "geometric_log": {sampson_distance, depth_inconsistency, ...}
      },
      ...
    },
    ...
  }
}
"""

import argparse
import gc
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.modules import Critic
from dream3r.scripts.build_oracle_expert_labels import (
    _load_adapter,
    _pointmap_abs_rel,
    _resize_images,
    _sequence_sample,
)


EXPERT_ORDER_DEFAULT = ["fast3r", "mast3r", "spann3r"]


def _load_trained_critic(ckpt_path: str, n_evidence: int, d_evidence: int) -> Critic:
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg = ckpt.get("config", {})
    critic = Critic(
        n_evidence=n_evidence,
        d_evidence=d_evidence,
        d_critic=int(cfg.get("d_critic", 64)),
        n_heads=int(cfg.get("n_heads", 4)),
        n_layers=int(cfg.get("n_layers", 2)),
        geometric_conflict_scale=float(cfg.get("geometric_conflict_scale", 1.0)),
        geometric_clean_bias=float(cfg.get("geometric_clean_bias", 0.0)),
    )
    critic.load_state_dict(ckpt["critic_state_dict"])
    critic.eval()
    return critic


def build_critic_cache(
    root: str,
    regime_labels: str,
    oracle_labels: str,
    output: str,
    critic_checkpoint: str,
    expert_order: List[str],
    window_frames: int = 4,
    max_frames_per_sequence: int = 32,
    image_size: int = 224,
    n_patches: int = 196,
    align_scale: bool = True,
) -> Dict[str, object]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))
    sequences = sorted(
        seq for seq in oracle_data["labels"]
        if seq in regime_data["labels"]
    )
    if not sequences:
        raise ValueError("no sequence overlap between regime_labels and oracle_labels")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Phase A cache build ===", flush=True)
    print(f"  n_sequences: {len(sequences)}", flush=True)
    print(f"  experts: {expert_order}", flush=True)
    print(f"  device: {device}", flush=True)
    print(f"  critic_ckpt: {critic_checkpoint}", flush=True)

    # Discover evidence dims via one dummy adapter forward.
    # The expert adapter outputs evidence_tokens of shape [B, T, n_evidence, d_evidence];
    # build_critic_training_data does .mean(dim=1) -> [B, n_evidence, d_evidence].
    sample0 = _sequence_sample(
        root, sequences[0], window_frames, max_frames_per_sequence, n_patches,
    )
    if sample0 is None:
        raise RuntimeError(f"first sequence {sequences[0]} returned no sample")
    probe_adapter = _load_adapter(expert_order[0])
    imgs0 = _resize_images(sample0["images"][0].unsqueeze(0).to(device), image_size)
    with torch.no_grad():
        probe_out = probe_adapter.forward(imgs0)
    n_evidence = probe_out.evidence_tokens.shape[-2]
    d_evidence = probe_out.evidence_tokens.shape[-1]
    print(f"  n_evidence={n_evidence}, d_evidence={d_evidence}", flush=True)
    del probe_adapter, probe_out
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()

    critic = _load_trained_critic(critic_checkpoint, n_evidence, d_evidence).to(device)

    # Pre-load each adapter once; iterate sequences inside.
    adapters = {name: _load_adapter(name) for name in expert_order}

    labels: Dict[str, Dict[str, Dict[str, object]]] = {}
    summary_rows: List[Dict[str, object]] = []
    t_start = time.time()
    for s_idx, seq in enumerate(sequences):
        sample = _sequence_sample(
            root, seq, window_frames, max_frames_per_sequence, n_patches,
        )
        if sample is None:
            print(f"  [{s_idx+1}/{len(sequences)}] {seq}: SKIP (no sample)", flush=True)
            continue
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)
        target_mean = target.mean(dim=1)  # [B, P, 3]
        target_conf = mask.float().mean(dim=1, keepdim=False).unsqueeze(-1)  # [B, P, 1]

        labels[seq] = {}
        for expert_name in expert_order:
            with torch.no_grad():
                out = adapters[expert_name].forward(images)
            abs_rel = _pointmap_abs_rel(out.pointmap, target, mask, align_scale)
            pointmap_mean = out.pointmap.mean(dim=1)
            confidence_mean = out.confidence.mean(dim=1)
            evidence_pool = out.evidence_tokens.mean(dim=1)  # [B, n_evidence, d_evidence]

            pointmap_pair = torch.stack(
                [pointmap_mean.squeeze(0), target_mean.squeeze(0)], dim=0
            ).unsqueeze(0)  # [1, 2, P, 3]
            confidence_pair = torch.stack(
                [confidence_mean.squeeze(0), target_conf.squeeze(0)], dim=0
            ).unsqueeze(0)  # [1, 2, P, 1]

            with torch.no_grad():
                critic_out = critic(
                    evidence_pool.float(),
                    cr1_mask=torch.ones(1, device=device),
                    pointmap_pair=pointmap_pair.float(),
                    confidence_pair=confidence_pair.float(),
                )
            conflict_raw = float(critic_out["conflict_score"].flatten()[0].item())
            repair_logits = critic_out["repair_logits"].flatten().tolist()
            recommended = int(torch.argmax(critic_out["repair_logits"], dim=-1).item())
            geo = critic_out.get("geometric_consistency_log", {}) or {}
            geo_log = {
                k: float(v.flatten()[0].item()) if hasattr(v, "flatten") else float(v)
                for k, v in geo.items()
            }

            labels[seq][expert_name] = {
                "abs_rel": float(abs_rel),
                "conflict_score_raw": conflict_raw,
                "conflict_score_sigmoid": float(torch.sigmoid(torch.tensor(conflict_raw)).item()),
                "repair_logits": [float(x) for x in repair_logits],
                "recommended_action_raw": recommended,
                "geometric_log": geo_log,
            }
            summary_rows.append({
                "sequence": seq,
                "expert": expert_name,
                "abs_rel": float(abs_rel),
                "conflict_sigmoid": labels[seq][expert_name]["conflict_score_sigmoid"],
                "recommended_action": recommended,
            })

        elapsed = time.time() - t_start
        eta = elapsed / (s_idx + 1) * (len(sequences) - s_idx - 1)
        print(f"  [{s_idx+1}/{len(sequences)}] {seq}: 3 experts ok | "
              f"elapsed={elapsed:.1f}s eta={eta:.1f}s", flush=True)

    result = {
        "dataset": Path(regime_labels).stem,
        "expert_order": expert_order,
        "n_sequences": len(labels),
        "metric": "scale_aligned_abs_rel" if align_scale else "raw_abs_rel",
        "critic_checkpoint": critic_checkpoint,
        "labels": labels,
        "summary_rows": summary_rows,
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved cache to {output_path}", flush=True)

    # Sanity stats
    all_conf = [r["conflict_sigmoid"] for r in summary_rows]
    if all_conf:
        import statistics
        print(f"\n=== Sanity ({len(all_conf)} (window, expert) entries) ===", flush=True)
        print(f"  conflict_sigmoid: mean={statistics.mean(all_conf):.4f} "
              f"std={statistics.stdev(all_conf):.4f} "
              f"min={min(all_conf):.4f} max={max(all_conf):.4f}", flush=True)
        action_counts: Dict[int, int] = {}
        for r in summary_rows:
            action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1
        print(f"  recommended_action counts: {action_counts}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument("--regime-labels", required=True)
    parser.add_argument("--oracle-labels", required=True,
                        help="Per-(window, expert) oracle JSON; defines window set")
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--critic-checkpoint",
        default="/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt",
    )
    parser.add_argument("--experts", nargs="+", default=EXPERT_ORDER_DEFAULT)
    parser.add_argument("--window-frames", type=int, default=4)
    parser.add_argument("--max-frames-per-sequence", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--n-patches", type=int, default=196)
    parser.add_argument("--no-align-scale", action="store_true")
    args = parser.parse_args()

    build_critic_cache(
        root=args.root,
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        output=args.output,
        critic_checkpoint=args.critic_checkpoint,
        expert_order=args.experts,
        window_frames=args.window_frames,
        max_frames_per_sequence=args.max_frames_per_sequence,
        image_size=args.image_size,
        n_patches=args.n_patches,
        align_scale=not args.no_align_scale,
    )


if __name__ == "__main__":
    main()
