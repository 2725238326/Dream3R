"""Runnable W17 demo for the Mamba-hybrid state path."""

import json
import time

import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.model import Dream3R


def _run_variant(recurrence_type: str, device: torch.device) -> dict:
    cfg = load_config(overrides={
        "state_recurrence_type": recurrence_type,
        "use_backbone": False,
        "batch_size": 1,
        "active_to_stable_threshold": 0.0,
    })
    model = Dream3R(config_to_model_args(cfg)).to(device)
    model.eval()

    generator = torch.Generator(device=device)
    generator.manual_seed(33)
    prev_memory = None
    prev_slots = None
    prev_slot_poses = None
    outputs = []

    start = time.perf_counter()
    with torch.no_grad():
        for step in range(3):
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

    last = outputs[-1]
    branch_weights = last["nsa_branch_weights"].float().mean(dim=(0, 1)).detach().cpu()
    promoted = last["memory_retrieval_log"]["promoted_to_stable"].float().mean().item()
    state_delta = (
        outputs[-1]["latent_state_tokens"] - outputs[0]["latent_state_tokens"]
    ).abs().mean().item()
    recurrence = model.memory.state_recurrence

    return {
        "recurrence_type": recurrence_type,
        "backend": getattr(recurrence, "backend", recurrence.__class__.__name__),
        "backend_error": getattr(recurrence, "backend_error", ""),
        "elapsed_ms_3_windows": round(elapsed_ms, 2),
        "latent_state_tokens": list(last["latent_state_tokens"].shape),
        "state_delta_mean_abs": round(state_delta, 6),
        "stable_promotion_rate": round(promoted, 6),
        "nsa_branch_mean": {
            "compressed": round(branch_weights[0].item(), 6),
            "selected": round(branch_weights[1].item(), 6),
            "sliding": round(branch_weights[2].item(), 6),
        },
        "conflict_score_mean": round(last["conflict_score"].float().mean().item(), 6),
        "recommended_action": last["recommended_action"].detach().cpu().tolist(),
    }


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = {
        "device": str(device),
        "variants": [
            _run_variant("cross_attention", device),
            _run_variant("mamba_hybrid", device),
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
