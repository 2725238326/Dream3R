"""Build the compact Dream3R v1.1 final evaluation pack.

The pack summarizes existing verified artifacts. It does not run a new
benchmark and must keep that boundary explicit in both JSON and Markdown.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_CODE_ROOT = Path(__file__).resolve().parents[2]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

from dream3r.release_v11 import RELEASE_V11_CANDIDATE, RELEASE_V11_VERSION  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("runs/release/v11_final_eval")
DEFAULT_TABLE_PATH = Path("release/FINAL_EVAL_TABLE_V1_1.md")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _require_path(root: Path, rel_path: str) -> Path:
    path = root / rel_path
    if not path.exists():
        raise FileNotFoundError(f"required artifact is missing: {rel_path}")
    return path


def _fallback_metrics(fallback_state: dict[str, Any]) -> dict[str, float]:
    final_eval = fallback_state["final_eval"]
    return {
        "kitti_abs_rel": float(final_eval["kitti"]["Ours_ProposalSetDecoder"]),
        "eth3d_abs_rel": float(final_eval["eth3d"]["Ours_ProposalSetDecoder"]),
    }


def _cache_demo_summary(cache_demo: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": cache_demo["status"],
        "domain": cache_demo["domain"],
        "demo_mode": cache_demo["demo_mode"],
        "entries_ran": int(cache_demo["entries_ran"]),
        "cache_entries_matched_domain": int(cache_demo["cache_entries_matched_domain"]),
        "cache_entries_total": int(cache_demo["cache_entries_total"]),
        "mean_abs_rel_vs_cache_gt": cache_demo["aggregate"]["mean_abs_rel_vs_cache_gt"],
        "expert_order": cache_demo["expert_order"],
        "claim_boundary": cache_demo["claim_boundary"],
    }


def _metric_row(
    *,
    domain: str,
    policy: str,
    state: float,
    no_state: float,
    shuffle: float,
    controls_pass: bool,
    source: str,
) -> str:
    return (
        f"| {domain} | {policy} | {state:.4f} | {no_state:.4f} | "
        f"{shuffle:.4f} | {'pass' if controls_pass else 'fail'} | `{source}` |"
    )


def _render_table(summary: dict[str, Any]) -> str:
    metrics = summary["official_v1_1"]["metrics"]
    controls = summary["official_v1_1"]["controls"]
    policy = summary["official_v1_1"]["policy"]
    fallback = summary["stable_fallback_v1_0"]["metrics"]
    cache = summary["runtime_cache_demo"]
    source = summary["source_json_paths"]
    attempt = summary.get("fusion_improvement_attempt")

    metric_rows = [
        _metric_row(
            domain="KITTI",
            policy=policy["kitti"],
            state=metrics["kitti_state_abs_rel"],
            no_state=metrics["kitti_no_state_abs_rel"],
            shuffle=metrics["kitti_shuffle_abs_rel"],
            controls_pass=controls["kitti_state_beats_no_state"]
            and controls["kitti_state_beats_shuffle"],
            source=source["unified_gate"],
        ),
        _metric_row(
            domain="ETH3D",
            policy=policy["eth3d"],
            state=metrics["eth3d_state_abs_rel"],
            no_state=metrics["eth3d_no_state_abs_rel"],
            shuffle=metrics["eth3d_shuffle_abs_rel"],
            controls_pass=controls["eth3d_state_beats_no_state"]
            and controls["eth3d_state_beats_shuffle"],
            source=source["unified_gate"],
        ),
    ]

    cache_rows = []
    for domain_key in ("kitti", "eth3d"):
        item = cache[domain_key]
        cache_rows.append(
            "| {domain} | {status} | {entries} | {matched}/{total} | {metric:.4f} | `{source}` |".format(
                domain=domain_key.upper(),
                status=item["status"],
                entries=item["entries_ran"],
                matched=item["cache_entries_matched_domain"],
                total=item["cache_entries_total"],
                metric=float(item["mean_abs_rel_vs_cache_gt"]),
                source=source[f"cache_demo_{domain_key}"],
            )
        )

    return "\n".join(
        [
            "# Dream3R v1.1.0 Final Evaluation Table",
            "",
            "Date: 2026-06-10",
            "",
            "This table summarizes existing verified release artifacts. It is not a new benchmark rerun.",
            "",
            "## Official v1.1.0 Metrics",
            "",
            "| Domain | Policy | Correct-state AbsRel | No-state AbsRel | Shuffle-state AbsRel | Controls | Source |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
            *metric_rows,
            "",
            "## Stable Fallback",
            "",
            "| Model | KITTI AbsRel | ETH3D AbsRel | Source |",
            "| --- | ---: | ---: | --- |",
            (
                "| v1.0-rc1 frozen StatePrior + bounded residual | "
                f"{fallback['kitti_abs_rel']:.4f} | {fallback['eth3d_abs_rel']:.4f} | "
                f"`{source['fallback_state']}` |"
            ),
            "",
            "## Runtime Cache Demo",
            "",
            "| Domain | Status | Entries run | Matched cache entries | Mean AbsRel vs cache GT | Source |",
            "| --- | --- | ---: | ---: | ---: | --- |",
            *cache_rows,
            "",
            *(
                [
                    "## Fusion Improvement Attempt",
                    "",
                    "| Candidate | Mechanism | Metric gate | Verdict | Source |",
                    "| --- | --- | --- | --- | --- |",
                    (
                        f"| {attempt['candidate_name']} | {attempt['mechanism']} | "
                        f"{attempt['metric_gate']['status']} | {attempt['verdict']} | "
                        f"`{source['conflict_dampening_attempt']}` |"
                    ),
                    "",
                ]
                if isinstance(attempt, dict)
                else []
            ),
            "## Claim Boundary",
            "",
            "- Safe claim: Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R release package.",
            "- Not claimed: proposal-free foundation 3R, image-only inference, Qwen geometry, universal SOTA, or long-sequence deployment.",
            "- Qwen, Foundation3R, proposal-free decoding, and v1.2-exp0 remain non-official unless future controls pass.",
            "",
        ]
    )


def build_final_eval_pack(
    *,
    root: Path,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    table_path: Path = DEFAULT_TABLE_PATH,
) -> dict[str, Any]:
    root = root.resolve()
    output_dir = output_dir if output_dir.is_absolute() else root / output_dir
    table_path = table_path if table_path.is_absolute() else root / table_path

    unified_gate_rel = (
        "runs/v22_admission/domain_conditional_teacher/"
        "unified_gate_candidate_with_kitti_no_state_server.json"
    )
    fallback_state_rel = (
        "runs/stage6_fusion/bounded_refine_sweep/"
        "frozen_prior_state_seed_7/results.json"
    )
    cache_kitti_rel = "runs/release/v11_cache_demo/cache_demo_kitti.json"
    cache_eth3d_rel = "runs/release/v11_cache_demo/cache_demo_eth3d.json"
    artifacts_rel = "release/ARTIFACTS.json"
    smoke_rel = "runs/release/v11_smoke/smoke_v11_release_model.json"
    attempt_rel = "runs/release/v11_final_eval/conflict_dampening_attempt.json"

    unified_gate = _read_json(_require_path(root, unified_gate_rel))
    artifacts = _read_json(_require_path(root, artifacts_rel))
    fallback_state = _read_json(_require_path(root, fallback_state_rel))
    cache_kitti = _read_json(_require_path(root, cache_kitti_rel))
    cache_eth3d = _read_json(_require_path(root, cache_eth3d_rel))
    smoke = _read_json(_require_path(root, smoke_rel))

    if unified_gate.get("status") != "pass":
        raise AssertionError("v1.1 unified gate must pass before building final eval pack")
    if unified_gate.get("promotable_to_official") is not True:
        raise AssertionError("v1.1 unified gate must be promotable before final eval pack")
    if artifacts.get("version") != RELEASE_V11_VERSION:
        raise AssertionError("release/ARTIFACTS.json version does not match v1.1")

    summary = {
        "status": "pass",
        "pack": "v11_final_eval",
        "version": RELEASE_V11_VERSION,
        "candidate": RELEASE_V11_CANDIDATE,
        "metric": "AbsRel",
        "metric_direction": "lower_is_better",
        "formal_benchmark_rerun": False,
        "benchmark_note": (
            "This pack consolidates the existing unified gate, fallback metrics, "
            "smoke report, and real-cache runtime demo. It does not rerun a "
            "formal benchmark."
        ),
        "official_v1_1": {
            "policy": unified_gate["policy"],
            "metrics": unified_gate["metrics"],
            "controls": unified_gate["controls"],
            "promotable_to_official": unified_gate["promotable_to_official"],
        },
        "stable_fallback_v1_0": {
            "version": "v1.0-rc1",
            "candidate": "frozen_state_prior_bounded_residual",
            "metrics": _fallback_metrics(fallback_state),
        },
        "runtime_cache_demo": {
            "kitti": _cache_demo_summary(cache_kitti),
            "eth3d": _cache_demo_summary(cache_eth3d),
        },
        "smoke": {
            "status": smoke["status"],
            "version": smoke["version"],
            "branches": smoke["branches"],
        },
        "source_json_paths": {
            "artifacts": artifacts_rel,
            "unified_gate": unified_gate_rel,
            "fallback_state": fallback_state_rel,
            "cache_demo_kitti": cache_kitti_rel,
            "cache_demo_eth3d": cache_eth3d_rel,
            "smoke": smoke_rel,
        },
        "claim_boundary": {
            "safe_claim": "state-conditioned proposal-fusion 3R release package",
            "not_claimed": [
                "formal benchmark rerun in this pack",
                "proposal-free foundation 3R",
                "image-only inference",
                "Qwen geometry backend",
                "universal SOTA",
                "long-sequence deployment",
            ],
        },
        "non_official_lanes": {
            "qwen": "diagnostic-only semantic/cache evidence",
            "foundation3r": "proposal-free research lane, not promotable",
            "proposal_free_decoder": "research scaffold, not official",
            "v1.2-exp0": "experimental core bridge, not official",
        },
    }

    attempt_path = root / attempt_rel
    if attempt_path.exists():
        summary["fusion_improvement_attempt"] = _read_json(attempt_path)
        summary["source_json_paths"]["conflict_dampening_attempt"] = attempt_rel

    summary_path = output_dir / "final_eval_summary.json"
    _write_json(summary_path, summary)
    table_path.parent.mkdir(parents=True, exist_ok=True)
    table_path.write_text(_render_table(summary), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--table-path", type=Path, default=DEFAULT_TABLE_PATH)
    args = parser.parse_args()

    summary = build_final_eval_pack(
        root=args.root,
        output_dir=args.output_dir,
        table_path=args.table_path,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
