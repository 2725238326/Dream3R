"""Small synthetic ablation for Dream3R memory and recurrence paths."""

import argparse
import json
import time
from pathlib import Path
from statistics import mean

import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.model import Dream3R


def _run_once(variant: dict, seed: int, windows: int, device: torch.device) -> dict:
    cfg = load_config(overrides={
        "state_recurrence_type": variant["state_recurrence_type"],
        "memory_use_nsa": variant["memory_use_nsa"],
        "enable_stable_memory": variant["enable_stable_memory"],
        "use_backbone": False,
        "batch_size": 1,
        "active_to_stable_threshold": 0.0,
    })
    model = Dream3R(config_to_model_args(cfg)).to(device)
    model.eval()

    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    prev_memory = None
    prev_slots = None
    prev_slot_poses = None
    outputs = []

    start = time.perf_counter()
    with torch.no_grad():
        for step in range(windows):
            x = torch.randn(1, 4, 16, 768, generator=generator, device=device)
            out = model(
                x,
                prev_memory_state=prev_memory,
                prev_object_slots=prev_slots,
                prev_object_slot_poses=prev_slot_poses,
                timestep=step,
            )
            outputs.append(out)
            prev_memory = out["latent_state_tokens"]
            prev_slots = out["object_track_set"]
            prev_slot_poses = out["object_slot_poses"]
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    first = outputs[0]
    last = outputs[-1]
    branch_weights = last["nsa_branch_weights"].float().mean(dim=(0, 1)).detach().cpu()
    promoted = last["memory_retrieval_log"]["promoted_to_stable"].float().mean().item()
    state_delta = (
        last["latent_state_tokens"] - first["latent_state_tokens"]
    ).abs().mean().item()
    recurrence = model.memory.state_recurrence

    return {
        "seed": seed,
        "elapsed_ms": elapsed_ms,
        "backend": getattr(recurrence, "backend", recurrence.__class__.__name__),
        "backend_error": getattr(recurrence, "backend_error", ""),
        "state_recurrence_type": variant["state_recurrence_type"],
        "memory_use_nsa": variant["memory_use_nsa"],
        "enable_stable_memory": variant["enable_stable_memory"],
        "state_delta_mean_abs": state_delta,
        "latent_drift_mean_abs": last["latent_drift_proxy"].float().abs().mean().item(),
        "stable_promotion_rate": promoted,
        "conflict_score_mean": last["conflict_score"].float().mean().item(),
        "nsa_compressed": branch_weights[0].item(),
        "nsa_selected": branch_weights[1].item(),
        "nsa_sliding": branch_weights[2].item(),
        "recommended_action": last["recommended_action"].detach().cpu().tolist(),
    }


def _summarize(rows: list[dict]) -> dict:
    return {
        "backend": rows[-1]["backend"],
        "backend_error": rows[-1]["backend_error"],
        "elapsed_ms_mean": round(mean(r["elapsed_ms"] for r in rows), 3),
        "state_delta_mean_abs": round(mean(r["state_delta_mean_abs"] for r in rows), 6),
        "latent_drift_mean_abs": round(mean(r["latent_drift_mean_abs"] for r in rows), 6),
        "stable_promotion_rate": round(mean(r["stable_promotion_rate"] for r in rows), 6),
        "conflict_score_mean": round(mean(r["conflict_score_mean"] for r in rows), 6),
        "nsa_branch_mean": {
            "compressed": round(mean(r["nsa_compressed"] for r in rows), 6),
            "selected": round(mean(r["nsa_selected"] for r in rows), 6),
            "sliding": round(mean(r["nsa_sliding"] for r in rows), 6),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", type=int, default=3)
    parser.add_argument("--seeds", type=int, nargs="+", default=[33, 34, 35])
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = {
        "device": str(device),
        "windows": args.windows,
        "seeds": args.seeds,
        "variants": {},
    }
    variants = [
        {
            "name": "baseline_cross_attention",
            "state_recurrence_type": "cross_attention",
            "memory_use_nsa": True,
            "enable_stable_memory": True,
        },
        {
            "name": "mamba_hybrid",
            "state_recurrence_type": "mamba_hybrid",
            "memory_use_nsa": True,
            "enable_stable_memory": True,
        },
        {
            "name": "no_nsa",
            "state_recurrence_type": "mamba_hybrid",
            "memory_use_nsa": False,
            "enable_stable_memory": True,
        },
        {
            "name": "no_stable_memory",
            "state_recurrence_type": "mamba_hybrid",
            "memory_use_nsa": True,
            "enable_stable_memory": False,
        },
    ]
    for variant in variants:
        rows = [
            _run_once(variant, seed, args.windows, device)
            for seed in args.seeds
        ]
        result["variants"][variant["name"]] = {
            "summary": _summarize(rows),
            "runs": rows,
        }

    text = json.dumps(result, indent=2)
    print(text)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
