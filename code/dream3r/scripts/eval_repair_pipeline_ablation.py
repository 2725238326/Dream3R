"""Evaluate Stage 4 repair as a sequence-level pipeline ablation.

This differs from eval_repair_ablation.py: critic-on/repair-off carries the
previous tick's critic signal into the next route decision, matching the
existing Dream3R bus/composer contract, but never executes RepairExecutor.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch

from dream3r.scripts.eval_repair_ablation import _load_critic
from dream3r.scripts.eval_router_ablation import _load_router
from dream3r.scripts.train_critic_only import _critic_to_contract_action


def _mean(values: List[float]) -> float:
    return float(sum(values) / max(len(values), 1))


def _group_by_sequence(data: Dict[str, object]) -> Tuple[List[str], Dict[str, Dict[str, dict]]]:
    order: List[str] = []
    grouped: Dict[str, Dict[str, dict]] = {}
    for idx, meta in enumerate(data["meta"]):
        seq = str(meta["sequence"])
        expert = str(meta["expert"])
        if seq not in grouped:
            order.append(seq)
            grouped[seq] = {}
        grouped[seq][expert] = dict(meta) | {"idx": idx}
    return order, grouped


def _route(
    router,
    regime_probs: torch.Tensor,
    expert_order: List[str],
    prev_conflict_score: Optional[float],
    prev_raw_action: Optional[int],
    prev_expert_id: Optional[int],
) -> Tuple[List[int], str, str]:
    kwargs = {}
    if prev_conflict_score is not None:
        critic_confidence = 1.0 - torch.sigmoid(
            torch.tensor([[prev_conflict_score]], dtype=torch.float32)
        )
        # Dream3R.forward uses previous raw recommended_action==2 to zero the
        # Composer confidence budget. Contract action 3 maps from raw action 2.
        if prev_raw_action == 2:
            critic_confidence = torch.zeros_like(critic_confidence)
        kwargs["critic_confidence"] = critic_confidence
        if prev_expert_id is not None:
            kwargs["previous_expert_id"] = torch.tensor(
                [[prev_expert_id]], dtype=torch.long,
            )

    with torch.no_grad():
        out = router(regime_probs, **kwargs)
    route_ids = [int(x) for x in out["route_recommendation"][0].tolist()]
    primary = expert_order[route_ids[0]]
    alternate = expert_order[route_ids[1]] if len(route_ids) > 1 else primary
    return route_ids, primary, alternate


def _metric(grouped: Dict[str, Dict[str, dict]], sequence: str, expert: str) -> float:
    return float(grouped[sequence][expert]["abs_rel"])


def evaluate_repair_pipeline_ablation(
    data_path: str,
    regime_labels: str,
    critic_checkpoint: str,
    router_checkpoint: str,
    output: str,
) -> Dict[str, object]:
    data = torch.load(data_path, map_location="cpu", weights_only=False)
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    expert_order = list(data["summary"]["expert_order"])
    sequence_order, grouped = _group_by_sequence(data)
    sequences = [
        seq for seq in sequence_order
        if seq in regime_data["labels"] and all(name in grouped[seq] for name in expert_order)
    ]
    if not sequences:
        raise ValueError("no sequence has regime labels and all expert metrics")

    critic = _load_critic(critic_checkpoint, data)
    with torch.no_grad():
        critic_out = critic(
            data["evidence"].float(),
            cr1_mask=torch.ones(data["evidence"].shape[0]),
            pointmap_pair=data["pointmap_pair"].float(),
            confidence_pair=data["confidence_pair"].float(),
        )
    conflict_score = critic_out["conflict_score"].squeeze(-1)
    raw_action = critic_out["repair_logits"].argmax(dim=-1)
    contract_action = _critic_to_contract_action(raw_action)

    router, _ = _load_router(router_checkpoint, n_regimes=len(regime_data["regime_order"]))

    rows = []
    prev_critic_conflict: Optional[float] = None
    prev_critic_raw_action: Optional[int] = None
    prev_critic_expert_id: Optional[int] = None
    prev_full_conflict: Optional[float] = None
    prev_full_raw_action: Optional[int] = None
    prev_full_expert_id: Optional[int] = None

    for sequence in sequences:
        regime = torch.tensor([regime_data["labels"][sequence]], dtype=torch.float32)

        both_route, both_expert, _ = _route(
            router, regime, expert_order, None, None, None,
        )
        both_abs_rel = _metric(grouped, sequence, both_expert)

        critic_route, critic_expert, _ = _route(
            router, regime, expert_order,
            prev_critic_conflict, prev_critic_raw_action, prev_critic_expert_id,
        )
        critic_abs_rel = _metric(grouped, sequence, critic_expert)

        full_route, full_primary, full_alternate = _route(
            router, regime, expert_order,
            prev_full_conflict, prev_full_raw_action, prev_full_expert_id,
        )
        full_primary_idx = int(grouped[sequence][full_primary]["idx"])
        full_action = int(contract_action[full_primary_idx].item())
        full_raw = int(raw_action[full_primary_idx].item())
        if full_action == 3:
            full_expert = full_alternate
            applied = "reroute_model"
        elif full_action == 4:
            full_expert = full_primary
            applied = "test3r_offpath_verify"
        else:
            full_expert = full_primary
            applied = "no_repair"
        full_abs_rel = _metric(grouped, sequence, full_expert)

        critic_idx = int(grouped[sequence][critic_expert]["idx"])
        prev_critic_conflict = float(conflict_score[critic_idx].item())
        prev_critic_raw_action = int(raw_action[critic_idx].item())
        prev_critic_expert_id = expert_order.index(critic_expert)
        prev_full_conflict = float(conflict_score[full_primary_idx].item())
        prev_full_raw_action = full_raw
        prev_full_expert_id = expert_order.index(full_primary)

        rows.append({
            "sequence": sequence,
            "regime_top": grouped[sequence][both_expert].get("regime_top"),
            "both_off_route": both_route,
            "critic_on_repair_off_route": critic_route,
            "full_pipeline_route": full_route,
            "both_off_expert": both_expert,
            "critic_on_repair_off_expert": critic_expert,
            "full_pipeline_primary_expert": full_primary,
            "full_pipeline_expert": full_expert,
            "full_pipeline_action": full_action,
            "full_pipeline_applied": applied,
            "both_off_abs_rel": both_abs_rel,
            "critic_on_repair_off_abs_rel": critic_abs_rel,
            "full_pipeline_abs_rel": full_abs_rel,
            "critic_changed_route": critic_route != both_route,
            "repair_changed_output": full_expert != full_primary,
        })

    threshold = float(data["summary"].get("conflict_threshold", 0.20))
    hard_rows = [row for row in rows if row["both_off_abs_rel"] > threshold]
    if not hard_rows:
        hard_rows = rows

    full = _mean([row["full_pipeline_abs_rel"] for row in hard_rows])
    critic_off = _mean([row["critic_on_repair_off_abs_rel"] for row in hard_rows])
    both_off = _mean([row["both_off_abs_rel"] for row in hard_rows])
    best_improvement = max(
        (row["both_off_abs_rel"] - row["full_pipeline_abs_rel"])
        / max(row["both_off_abs_rel"], 1e-8)
        for row in hard_rows
    )

    result = {
        "metric": data["summary"].get("metric", "abs_rel"),
        "n_sequences": len(rows),
        "n_hard_sequences": len(hard_rows),
        "metrics": {
            "full_pipeline_repair_on": full,
            "critic_on_repair_off": critic_off,
            "both_off": both_off,
        },
        "mean_relative_improvement_vs_both_off": (both_off - full) / max(both_off, 1e-8),
        "best_example_relative_improvement": best_improvement,
        "critic_changed_route_count": sum(1 for row in rows if row["critic_changed_route"]),
        "repair_changed_output_count": sum(1 for row in rows if row["repair_changed_output"]),
        "rows": rows,
        "success": {
            "chain_full_le_critic_off_le_both_off": (
                full <= critic_off <= both_off
                and (full < critic_off or critic_off < both_off)
            ),
            "one_example_gt_5pct": best_improvement > 0.05,
        },
    }
    result["success"]["t4_3"] = all(result["success"].values())

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_critic_data/critic_training_data.pt",
    )
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--critic-checkpoint",
        default="/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt",
    )
    parser.add_argument(
        "--router-checkpoint",
        default="/hdd3/kykt26/checkpoints/router_only_v1/latest.pt",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json",
    )
    args = parser.parse_args()

    result = evaluate_repair_pipeline_ablation(
        data_path=args.data,
        regime_labels=args.regime_labels,
        critic_checkpoint=args.critic_checkpoint,
        router_checkpoint=args.router_checkpoint,
        output=args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
