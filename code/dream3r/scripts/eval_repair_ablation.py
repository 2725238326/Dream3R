"""Evaluate Stage 4 repair rerouting on hard critic examples."""

import argparse
import json
from pathlib import Path
from typing import Dict

import torch

from dream3r.modules import Critic
from dream3r.scripts.train_critic_only import _critic_to_contract_action


def _load_critic(checkpoint: str, data: Dict[str, object]) -> Critic:
    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    cfg = ckpt["config"]
    state = ckpt["critic_state_dict"]
    critic = Critic(
        n_evidence=data["evidence"].shape[1],
        d_evidence=data["evidence"].shape[2],
        d_critic=cfg["d_critic"],
        n_heads=cfg["n_heads"],
        n_layers=cfg["n_layers"],
        geometric_conflict_scale=cfg.get("geometric_conflict_scale", 1.0),
        geometric_clean_bias=cfg.get("geometric_clean_bias", 0.0),
    )
    critic.load_state_dict(state)
    critic.eval()
    return critic


def _mean(values):
    return float(sum(values) / max(len(values), 1))


def evaluate_repair_ablation(
    data_path: str,
    critic_checkpoint: str,
    output: str,
) -> Dict[str, object]:
    data = torch.load(data_path, map_location="cpu", weights_only=False)
    critic = _load_critic(critic_checkpoint, data)

    with torch.no_grad():
        out = critic(
            data["evidence"].float(),
            cr1_mask=torch.ones(data["evidence"].shape[0]),
            pointmap_pair=data["pointmap_pair"].float(),
            confidence_pair=data["confidence_pair"].float(),
        )
        pred_action = _critic_to_contract_action(out["repair_logits"].argmax(dim=-1))

    rows = []
    for idx, meta in enumerate(data["meta"]):
        primary = float(meta["abs_rel"])
        alt = float(meta["alt_abs_rel"])
        action = int(pred_action[idx].item())
        if action == 3 and alt < primary:
            repaired = alt
            applied = "reroute_model"
        elif action == 4:
            repaired = primary
            applied = "test3r_offpath_verify"
        else:
            repaired = primary
            applied = "no_repair"
        improvement = (primary - repaired) / max(primary, 1e-8)
        rows.append({
            "sequence": meta["sequence"],
            "expert": meta["expert"],
            "regime_top": meta["regime_top"],
            "pred_action": action,
            "applied": applied,
            "without_repair_abs_rel": primary,
            "with_repair_abs_rel": repaired,
            "relative_improvement": improvement,
        })

    hard_rows = [row for row in rows if row["without_repair_abs_rel"] > data["summary"]["conflict_threshold"]]
    if not hard_rows:
        hard_rows = rows

    full = _mean([row["with_repair_abs_rel"] for row in hard_rows])
    repair_off = _mean([row["without_repair_abs_rel"] for row in hard_rows])
    both_off = repair_off
    best_improvement = max(row["relative_improvement"] for row in hard_rows)

    result = {
        "metric": data["summary"].get("metric", "abs_rel"),
        "n_examples": len(rows),
        "n_hard_examples": len(hard_rows),
        "metrics": {
            "full_pipeline_repair_on": full,
            "critic_on_repair_off": repair_off,
            "both_off": both_off,
        },
        "mean_relative_improvement_vs_repair_off": (repair_off - full) / max(repair_off, 1e-8),
        "best_example_relative_improvement": best_improvement,
        "rows": rows,
        "success": {
            "repair_beats_repair_off": full < repair_off,
            "one_example_gt_5pct": best_improvement > 0.05,
            "strict_chain_full_lt_repair_off_lt_both_off": full < repair_off < both_off,
        },
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_critic_data/critic_training_data.pt",
    )
    parser.add_argument(
        "--critic-checkpoint",
        default="/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_repair_ablation/results.json",
    )
    args = parser.parse_args()

    result = evaluate_repair_ablation(args.data, args.critic_checkpoint, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
