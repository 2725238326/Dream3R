"""Phase A: ETH3D 50w geometric cache for closed-loop reroute.

Mirrors build_critic_cache.py but uses ETH3DLongSequenceDataset with
--dense-gt (laser scan GT) so the geometric_log is computed against
dense ground truth.

Note: we still load the trained Critic to call its forward (which
emits geometric_consistency_log as a side effect). The conflict_score
head is known not to generalize beyond the 12-seq KITTI training set
(DEC-007 follow-up), but the geometric_consistency_log values come
from a deterministic computation that does not depend on Critic
weights. We use those geometric values, not the conflict head.
"""

import argparse
import gc
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES
from dream3r.modules import Critic
from dream3r.scripts.build_critic_cache import _load_trained_critic
from dream3r.scripts.build_oracle_expert_labels import (
    _load_adapter,
    _pointmap_abs_rel,
    _resize_images,
)


EXPERT_ORDER_DEFAULT = ["fast3r", "mast3r", "spann3r"]


def build_critic_cache_eth3d(
    root: str,
    regime_labels: str,
    oracle_labels: str,
    output: str,
    critic_checkpoint: str,
    expert_order: List[str],
    sequence_length: int = 4,
    image_size: int = 224,
    n_patches: int = 196,
    max_windows_per_scene: int = 25,
    dense_gt: bool = True,
    align_scale: bool = True,
) -> Dict[str, object]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    oracle_data = json.loads(Path(oracle_labels).read_text(encoding="utf-8"))

    sequences = sorted(
        seq for seq in oracle_data["labels"]
        if seq in regime_data["labels"]
    )
    if not sequences:
        raise ValueError("no overlap between regime/oracle sequences")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Phase A ETH3D cache build (dense_gt={dense_gt}) ===", flush=True)
    print(f"  n_sequences: {len(sequences)}", flush=True)
    print(f"  experts: {expert_order}", flush=True)
    print(f"  device: {device}", flush=True)

    dataset = ETH3DLongSequenceDataset(
        root=root,
        sequence_length=sequence_length,
        max_windows_per_scene=max_windows_per_scene,
        image_size=image_size,
        n_patches=n_patches,
        scenes=SCENES,
        dense_gt=dense_gt,
    )
    sample_index = {
        dataset[i]["sequence_name"]: i
        for i in range(len(dataset))
    }

    # Probe evidence dims via one expert + one sample
    probe_seq = sequences[0]
    probe_idx = sample_index.get(probe_seq)
    if probe_idx is None:
        raise RuntimeError(f"first sequence {probe_seq} not found in dataset")
    probe_sample = dataset[probe_idx]
    probe_imgs = _resize_images(probe_sample["images"][0].unsqueeze(0).to(device), image_size)
    probe_adapter = _load_adapter(expert_order[0])
    with torch.no_grad():
        probe_out = probe_adapter.forward(probe_imgs)
    n_evidence = probe_out.evidence_tokens.shape[-2]
    d_evidence = probe_out.evidence_tokens.shape[-1]
    print(f"  n_evidence={n_evidence}, d_evidence={d_evidence}", flush=True)
    del probe_adapter, probe_out
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()

    critic = _load_trained_critic(critic_checkpoint, n_evidence, d_evidence).to(device)
    adapters = {name: _load_adapter(name) for name in expert_order}

    labels: Dict[str, Dict[str, Dict[str, object]]] = {}
    summary_rows: List[Dict[str, object]] = []
    t_start = time.time()
    for s_idx, seq in enumerate(sequences):
        idx = sample_index.get(seq)
        if idx is None:
            print(f"  [{s_idx+1}/{len(sequences)}] {seq}: SKIP", flush=True)
            continue
        sample = dataset[idx]
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)
        target_mean = target.mean(dim=1)
        target_conf = mask.float().mean(dim=1, keepdim=False).unsqueeze(-1)

        labels[seq] = {}
        for expert_name in expert_order:
            with torch.no_grad():
                out = adapters[expert_name].forward(images)
            abs_rel = _pointmap_abs_rel(out.pointmap, target, mask, align_scale)
            pointmap_mean = out.pointmap.mean(dim=1)
            confidence_mean = out.confidence.mean(dim=1)
            evidence_pool = out.evidence_tokens.mean(dim=1)

            pointmap_pair = torch.stack(
                [pointmap_mean.squeeze(0), target_mean.squeeze(0)], dim=0
            ).unsqueeze(0)
            confidence_pair = torch.stack(
                [confidence_mean.squeeze(0), target_conf.squeeze(0)], dim=0
            ).unsqueeze(0)

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
        "dataset": "eth3d_low_res_many_view",
        "expert_order": expert_order,
        "n_sequences": len(labels),
        "metric": "scale_aligned_abs_rel" if align_scale else "raw_abs_rel",
        "gt_source": "dense_scan" if dense_gt else "sfm_sparse",
        "critic_checkpoint": critic_checkpoint,
        "labels": labels,
        "summary_rows": summary_rows,
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved cache to {output_path}", flush=True)

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
    parser.add_argument("--oracle-labels", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--critic-checkpoint",
        default="/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt",
    )
    parser.add_argument("--experts", nargs="+", default=EXPERT_ORDER_DEFAULT)
    parser.add_argument("--sequence-length", type=int, default=4)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--n-patches", type=int, default=196)
    parser.add_argument("--max-windows-per-scene", type=int, default=25)
    parser.add_argument("--no-dense-gt", action="store_true")
    parser.add_argument("--no-align-scale", action="store_true")
    args = parser.parse_args()

    build_critic_cache_eth3d(
        root=args.root,
        regime_labels=args.regime_labels,
        oracle_labels=args.oracle_labels,
        output=args.output,
        critic_checkpoint=args.critic_checkpoint,
        expert_order=args.experts,
        sequence_length=args.sequence_length,
        image_size=args.image_size,
        n_patches=args.n_patches,
        max_windows_per_scene=args.max_windows_per_scene,
        dense_gt=not args.no_dense_gt,
        align_scale=not args.no_align_scale,
    )


if __name__ == "__main__":
    main()
