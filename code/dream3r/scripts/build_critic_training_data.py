"""Build Stage 4 critic training data from real expert KITTI outputs."""

import argparse
import json
from pathlib import Path
from typing import Dict, List

import torch

from dream3r.modules import Critic
from dream3r.scripts.build_oracle_expert_labels import (
    EXPERT_ORDER,
    _evaluate_expert,
    _load_adapter,
    _pointmap_abs_rel,
    _resize_images,
    _select_sequences,
    _sequence_sample,
    _top_regime,
)


def _action_for(abs_rel: float, alt_abs_rel: float,
                conflict_threshold: float, reroute_margin: float) -> int:
    if abs_rel <= conflict_threshold:
        return 0
    if alt_abs_rel + reroute_margin < abs_rel:
        return 3
    return 4


def build_critic_training_data(
    root: str,
    regime_labels: str,
    output: str,
    max_per_regime: int = 3,
    window_frames: int = 4,
    max_frames_per_sequence: int = 32,
    image_size: int = 224,
    n_patches: int = 196,
    conflict_threshold: float = 0.20,
    reroute_margin: float = 0.01,
    align_scale: bool = True,
) -> Dict[str, object]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    sequences = _select_sequences(regime_data, max_per_regime=max_per_regime)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    metric_by_expert = {
        name: _evaluate_expert(
            name, root, sequences, window_frames, max_frames_per_sequence,
            image_size, n_patches, align_scale, device,
        )
        for name in EXPERT_ORDER
    }

    tensors = {
        "evidence": [],
        "pointmap_pair": [],
        "confidence_pair": [],
        "abs_rel": [],
        "conflict_label": [],
        "repair_action": [],
    }
    meta: List[Dict[str, object]] = []

    adapters = {name: _load_adapter(name) for name in EXPERT_ORDER}
    for seq in sequences:
        sample = _sequence_sample(
            root, seq, window_frames, max_frames_per_sequence, n_patches,
        )
        if sample is None:
            continue
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)
        target_mean = target.mean(dim=1)
        target_conf = mask.float().mean(dim=1, keepdim=False).unsqueeze(-1)

        for expert_name in EXPERT_ORDER:
            alt_name = next(name for name in EXPERT_ORDER if name != expert_name)
            with torch.no_grad():
                out = adapters[expert_name].forward(images)
            abs_rel = _pointmap_abs_rel(out.pointmap, target, mask, align_scale)
            alt_abs_rel = metric_by_expert[alt_name][seq]
            action = _action_for(
                abs_rel, alt_abs_rel, conflict_threshold, reroute_margin,
            )

            pointmap_mean = out.pointmap.mean(dim=1)
            confidence_mean = out.confidence.mean(dim=1)
            tensors["evidence"].append(out.evidence_tokens.mean(dim=1).squeeze(0).cpu())
            tensors["pointmap_pair"].append(
                torch.stack([pointmap_mean.squeeze(0), target_mean.squeeze(0)], dim=0).cpu()
            )
            tensors["confidence_pair"].append(
                torch.stack([confidence_mean.squeeze(0), target_conf.squeeze(0)], dim=0).cpu()
            )
            tensors["abs_rel"].append(torch.tensor(abs_rel, dtype=torch.float32))
            tensors["conflict_label"].append(
                torch.tensor(float(abs_rel > conflict_threshold), dtype=torch.float32)
            )
            tensors["repair_action"].append(torch.tensor(action, dtype=torch.long))
            meta.append({
                "sequence": seq,
                "expert": expert_name,
                "alt_expert": alt_name,
                "abs_rel": abs_rel,
                "alt_abs_rel": alt_abs_rel,
                "repair_action": action,
                "regime_top": _top_regime(
                    regime_data["labels"][seq],
                    regime_data["regime_order"],
                ),
            })

    data = {
        key: torch.stack(values)
        for key, values in tensors.items()
    }
    data["meta"] = meta
    data["summary"] = {
        "n_examples": len(meta),
        "n_sequences": len(sequences),
        "expert_order": EXPERT_ORDER,
        "metric": "scale_aligned_abs_rel" if align_scale else "raw_abs_rel",
        "conflict_threshold": conflict_threshold,
        "reroute_margin": reroute_margin,
    }

    # Keep the geometric feature calculation exercised at build time.
    Critic.compute_geometric_consistency(data["pointmap_pair"], data["confidence_pair"])

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(data, output_path)
    (output_path.with_suffix(".summary.json")).write_text(
        json.dumps(data["summary"] | {"meta": meta}, indent=2),
        encoding="utf-8",
    )
    return data["summary"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_critic_data/critic_training_data.pt",
    )
    parser.add_argument("--max-per-regime", type=int, default=3)
    parser.add_argument("--window-frames", type=int, default=4)
    parser.add_argument("--max-frames-per-sequence", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--conflict-threshold", type=float, default=0.20)
    parser.add_argument("--reroute-margin", type=float, default=0.01)
    parser.add_argument("--raw-scale", action="store_true")
    args = parser.parse_args()

    summary = build_critic_training_data(
        root=args.root,
        regime_labels=args.regime_labels,
        output=args.output,
        max_per_regime=args.max_per_regime,
        window_frames=args.window_frames,
        max_frames_per_sequence=args.max_frames_per_sequence,
        image_size=args.image_size,
        conflict_threshold=args.conflict_threshold,
        reroute_margin=args.reroute_margin,
        align_scale=not args.raw_scale,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
