"""Summarize Dream3R ver2.1 metric-refresh SCF sweeps."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


VARIANTS = ("state", "no_state", "shuffle_state")
DOMAINS = ("kitti", "eth3d")
METRICS = (
    "Ours_SCF",
    "rel_imp_vs_best_single_pp",
    "oracle_gap_pp",
    "patch_oracle_gap_pp",
    "Ours_temporal_delta_abs_rel",
    "Ours_scale_drift_proxy",
)
DISPLAY = {
    "state": "SCF + correct state",
    "no_state": "SCF - state",
    "shuffle_state": "SCF + shuffled state",
}


def _mean_std(values: list[float]) -> dict[str, float]:
    return {
        "mean": round(statistics.fmean(values), 4),
        "std": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0,
    }


def _load_result(root: Path, seed: int, variant: str) -> dict:
    path = root / f"seed_{seed}_{variant}" / "results.json"
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def summarize(root: Path, seeds: list[int]) -> dict:
    summary: dict[str, object] = {"root": str(root), "seeds": seeds, "variants": {}}
    variants = summary["variants"]
    assert isinstance(variants, dict)

    for variant in VARIANTS:
        loaded = [_load_result(root, seed, variant) for seed in seeds]
        by_domain = {}
        for domain in DOMAINS:
            by_domain[domain] = {
                metric: _mean_std([float(item["final_eval"][domain][metric]) for item in loaded])
                for metric in METRICS
            }
        variants[variant] = by_domain

    return summary


def _cell(summary: dict, variant: str, domain: str, metric: str) -> str:
    value = summary["variants"][variant][domain][metric]
    return f"{value['mean']:.4f} +/- {value['std']:.4f}"


def render_markdown(summary: dict) -> str:
    seeds = ", ".join(str(seed) for seed in summary["seeds"])
    lines = [
        "# Dream3R ver2.1 Metric Refresh Summary",
        "",
        f"Seeds: {seeds}",
        "",
        "## Accuracy and Oracle Gaps",
        "",
        "| variant | KITTI Ours | KITTI rel_imp | KITTI patch_gap | ETH3D Ours | ETH3D rel_imp | ETH3D patch_gap |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for variant in VARIANTS:
        lines.append(
            "| "
            + " | ".join(
                [
                    DISPLAY[variant],
                    _cell(summary, variant, "kitti", "Ours_SCF"),
                    _cell(summary, variant, "kitti", "rel_imp_vs_best_single_pp"),
                    _cell(summary, variant, "kitti", "patch_oracle_gap_pp"),
                    _cell(summary, variant, "eth3d", "Ours_SCF"),
                    _cell(summary, variant, "eth3d", "rel_imp_vs_best_single_pp"),
                    _cell(summary, variant, "eth3d", "patch_oracle_gap_pp"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Temporal and Scale Proxies",
            "",
            "| variant | KITTI temporal | KITTI scale | ETH3D temporal | ETH3D scale |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for variant in VARIANTS:
        lines.append(
            "| "
            + " | ".join(
                [
                    DISPLAY[variant],
                    _cell(summary, variant, "kitti", "Ours_temporal_delta_abs_rel"),
                    _cell(summary, variant, "kitti", "Ours_scale_drift_proxy"),
                    _cell(summary, variant, "eth3d", "Ours_temporal_delta_abs_rel"),
                    _cell(summary, variant, "eth3d", "Ours_scale_drift_proxy"),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("runs/stage6_fusion/ver21_metric_refresh"),
        help="Directory containing seed_<seed>_<variant>/results.json folders.",
    )
    parser.add_argument("--seeds", type=int, nargs="+", default=[7, 11, 13, 17])
    args = parser.parse_args()

    summary = summarize(args.root, args.seeds)
    args.root.mkdir(parents=True, exist_ok=True)
    (args.root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    markdown = render_markdown(summary)
    (args.root / "summary.md").write_text(markdown)
    print(markdown)


if __name__ == "__main__":
    main()
