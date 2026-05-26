"""Phase 0 sanity: verify DINOv3 backbone is REAL and Critic produces meaningful conflict_score.

Loads one real KITTI window, runs V04Pipeline.forward, prints backbone backend +
critic outputs. If backbone is fallback/stub, the rest of the closed-loop plan
won't produce useful signal.
"""

import argparse
import json
import sys
from pathlib import Path

import torch

from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", default="small_real",
                        help="Dream3R preset; small_real uses DINOv3 ONNX backbone")
    parser.add_argument("--sequence", default=None,
                        help="Optional KITTI sequence name (else first available)")
    parser.add_argument("--max-windows", type=int, default=2)
    parser.add_argument("--output", default="/tmp/phase0_sanity.json")
    args = parser.parse_args()

    print(f"=== Phase 0 sanity (preset={args.preset}) ===", flush=True)

    print("Building Dream3R + V04Pipeline ...", flush=True)
    model = build_dream3r(args.preset)
    model.eval()
    pipeline = build_v04_pipeline(model, max_repair_attempts=1)

    print(f"Loading KITTI window (sequence={args.sequence or 'first'}) ...", flush=True)
    ds = KITTILongSequenceDataset(
        sequence=args.sequence,
        sequence_length=4,
        overlap=2,
        windows_per_sample=1,
        max_sequences=1 if args.sequence is None else 0,
        min_sequence_frames=4,
        max_frames_per_sequence=20,
    )
    if len(ds) == 0:
        print("ERROR: no KITTI windows found", flush=True)
        sys.exit(1)

    sample = ds[0]
    images = sample["images"]  # [W, T, 3, H, W]
    print(f"  sequence: {sample['sequence_name']}, images shape: {tuple(images.shape)}", flush=True)

    results = {"preset": args.preset, "sequence": sample["sequence_name"], "windows": []}

    n_run = min(args.max_windows, images.shape[0])
    with torch.no_grad():
        for w_idx in range(n_run):
            print(f"\n--- window {w_idx} forward ---", flush=True)
            window_imgs = images[w_idx:w_idx+1]  # [1, T, 3, H, W]
            out = pipeline(images=window_imgs, timestep=w_idx)

            # backbone_status lives on PerceptionOutput
            backbone_status = {}
            if hasattr(out, "perception") and out.perception is not None:
                backbone_status = dict(out.perception.backbone_status) if out.perception.backbone_status else {}

            conflict_score = float(out.conflict_score.flatten()[0].item()) \
                if out.conflict_score is not None else None
            critic = out.critic
            entry = {
                "window_idx": w_idx,
                "backbone_status": backbone_status,
                "conflict_score_raw": conflict_score,
                "conflict_score_sigmoid": float(torch.sigmoid(torch.tensor(conflict_score)).item())
                    if conflict_score is not None else None,
                "recommended_action": int(critic.repair_action.flatten()[0].item())
                    if critic is not None else None,
                "selected_expert": int(out.selected_expert.flatten()[0].item())
                    if out.selected_expert is not None else None,
            }
            if critic is not None and critic.critic_log:
                geo = critic.critic_log.get("geometric_consistency_log", {})
                entry["geometric_log"] = {
                    k: float(v.flatten()[0].item()) if hasattr(v, "flatten") else v
                    for k, v in geo.items()
                } if geo else {}

            results["windows"].append(entry)
            print(json.dumps(entry, indent=2), flush=True)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved to {args.output}", flush=True)

    # Verdict
    if results["windows"]:
        backbone = results["windows"][0]["backbone_status"]
        backend = backbone.get("backend", "unknown")
        is_loaded = backbone.get("is_loaded", False)
        print(f"\n=== VERDICT ===", flush=True)
        print(f"  backbone backend: {backend} (is_loaded={is_loaded})", flush=True)
        if backend == "real":
            print("  PHASE 0 PASS — DINOv3 real, proceed to Phase A.", flush=True)
        elif backend == "fallback":
            print("  PHASE 0 WARN — backbone in fallback mode; conflict_score may be noise.", flush=True)
            print("  Recommendation: investigate backbone load error before Phase A.", flush=True)
        else:
            print("  PHASE 0 FAIL — backbone stub; cache will not have meaningful signal.", flush=True)


if __name__ == "__main__":
    main()
