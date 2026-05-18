"""Create dependency-free SVG charts from Dream3R ablation JSON."""

import argparse
import json
from pathlib import Path


def _bar_svg(title: str, values: dict[str, float], ylabel: str) -> str:
    width = 760
    height = 360
    margin_left = 150
    margin_right = 40
    margin_top = 56
    margin_bottom = 62
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    max_value = max(max(values.values()), 1e-8)
    bar_gap = 18
    bar_h = max(20, (plot_h - bar_gap * (len(values) - 1)) / max(len(values), 1))

    rows = []
    for idx, (name, value) in enumerate(values.items()):
        y = margin_top + idx * (bar_h + bar_gap)
        bar_w = plot_w * (value / max_value)
        rows.append(
            f'<text x="12" y="{y + bar_h * 0.65:.1f}" font-size="14" '
            f'font-family="Arial">{name}</text>'
        )
        rows.append(
            f'<rect x="{margin_left}" y="{y:.1f}" width="{bar_w:.1f}" '
            f'height="{bar_h:.1f}" fill="#3267b1" rx="3" />'
        )
        rows.append(
            f'<text x="{margin_left + bar_w + 8:.1f}" y="{y + bar_h * 0.65:.1f}" '
            f'font-size="13" font-family="Arial">{value:.4f}</text>'
        )

    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial" font-weight="700">{title}</text>',
        f'<text x="{margin_left}" y="{height - 18}" font-size="13" font-family="Arial">{ylabel}</text>',
        f'<line x1="{margin_left}" y1="{margin_top - 8}" x2="{margin_left}" y2="{height - margin_bottom + 8}" stroke="#999" />',
        *rows,
        '</svg>',
    ])


def _stacked_nsa_svg(values: dict[str, dict[str, float]]) -> str:
    width = 820
    height = 380
    margin_left = 160
    margin_top = 58
    bar_w = 520
    bar_h = 34
    gap = 28
    colors = {
        "compressed": "#3267b1",
        "selected": "#2a9d70",
        "sliding": "#d9822b",
    }
    rows = []
    for idx, (name, branches) in enumerate(values.items()):
        y = margin_top + idx * (bar_h + gap)
        x = margin_left
        rows.append(
            f'<text x="12" y="{y + bar_h * 0.65:.1f}" font-size="14" font-family="Arial">{name}</text>'
        )
        for branch in ["compressed", "selected", "sliding"]:
            value = branches.get(branch, 0.0)
            seg_w = bar_w * value
            rows.append(
                f'<rect x="{x:.1f}" y="{y}" width="{seg_w:.1f}" height="{bar_h}" '
                f'fill="{colors[branch]}" />'
            )
            if seg_w > 44:
                rows.append(
                    f'<text x="{x + seg_w / 2:.1f}" y="{y + bar_h * 0.65:.1f}" '
                    f'text-anchor="middle" font-size="12" font-family="Arial" fill="white">{value:.2f}</text>'
                )
            x += seg_w

    legend = []
    lx = margin_left
    for branch in ["compressed", "selected", "sliding"]:
        legend.extend([
            f'<rect x="{lx}" y="{height - 42}" width="16" height="16" fill="{colors[branch]}" />',
            f'<text x="{lx + 22}" y="{height - 29}" font-size="13" font-family="Arial">{branch}</text>',
        ])
        lx += 140

    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial" font-weight="700">NSA Branch Mix</text>',
        *rows,
        *legend,
        '</svg>',
    ])


def create_visuals(input_path: Path, output_dir: Path) -> dict[str, Path]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    variants = data["variants"]
    summaries = {name: payload["summary"] for name, payload in variants.items()}

    charts = {
        "elapsed_ms.svg": _bar_svg(
            "Mean Runtime", {k: v["elapsed_ms_mean"] for k, v in summaries.items()}, "milliseconds, lower is better"
        ),
        "state_delta.svg": _bar_svg(
            "State Delta", {k: v["state_delta_mean_abs"] for k, v in summaries.items()}, "mean absolute delta"
        ),
        "latent_drift.svg": _bar_svg(
            "Latent Drift", {k: v["latent_drift_mean_abs"] for k, v in summaries.items()}, "mean absolute drift"
        ),
        "stable_promotion.svg": _bar_svg(
            "Stable Promotion Rate", {k: v["stable_promotion_rate"] for k, v in summaries.items()}, "rate"
        ),
        "nsa_branch_mix.svg": _stacked_nsa_svg(
            {k: v["nsa_branch_mean"] for k, v in summaries.items()}
        ),
    }

    written = {}
    for filename, svg in charts.items():
        path = output_dir / filename
        path.write_text(svg + "\n", encoding="utf-8")
        written[filename] = path

    summary_md = output_dir / "summary.md"
    lines = [
        "# Ablation Visualization Summary",
        "",
        f"Source: `{input_path}`",
        "",
        "| Variant | Backend | Runtime ms | State delta | Latent drift | Stable promotion |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, summary in summaries.items():
        lines.append(
            f"| `{name}` | `{summary['backend']}` | {summary['elapsed_ms_mean']} | "
            f"{summary['state_delta_mean_abs']} | {summary['latent_drift_mean_abs']} | "
            f"{summary['stable_promotion_rate']} |"
        )
    lines.extend([
        "",
        "Charts:",
        "",
        "- `elapsed_ms.svg`",
        "- `state_delta.svg`",
        "- `latent_drift.svg`",
        "- `stable_promotion.svg`",
        "- `nsa_branch_mix.svg`",
    ])
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    written["summary.md"] = summary_md
    return written


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json")
    parser.add_argument("--out-dir", default="demo_artifacts/ablation")
    args = parser.parse_args()

    written = create_visuals(Path(args.input_json), Path(args.out_dir))
    for name, path in written.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
