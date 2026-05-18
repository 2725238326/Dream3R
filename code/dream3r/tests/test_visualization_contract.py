"""Tests for dependency-free ablation visualization artifacts."""

import json
import tempfile
from pathlib import Path

from dream3r.visualize_ablation import create_visuals


def test_visualize_ablation_writes_svg_and_summary():
    payload = {
        "variants": {
            "baseline_cross_attention": {
                "summary": {
                    "backend": "StateTokenRecurrence",
                    "elapsed_ms_mean": 10.0,
                    "state_delta_mean_abs": 0.5,
                    "latent_drift_mean_abs": 0.2,
                    "stable_promotion_rate": 1.0,
                    "nsa_branch_mean": {
                        "compressed": 0.1,
                        "selected": 0.8,
                        "sliding": 0.1,
                    },
                },
            },
            "mamba_hybrid": {
                "summary": {
                    "backend": "mamba_ssm",
                    "elapsed_ms_mean": 8.0,
                    "state_delta_mean_abs": 0.3,
                    "latent_drift_mean_abs": 0.1,
                    "stable_promotion_rate": 1.0,
                    "nsa_branch_mean": {
                        "compressed": 0.2,
                        "selected": 0.7,
                        "sliding": 0.1,
                    },
                },
            },
        },
    }

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "ablation.json"
        out_dir = root / "charts"
        source.write_text(json.dumps(payload), encoding="utf-8")

        written = create_visuals(source, out_dir)

        assert "elapsed_ms.svg" in written
        assert "nsa_branch_mix.svg" in written
        assert "summary.md" in written
        assert "<svg" in written["elapsed_ms.svg"].read_text(encoding="utf-8")
        assert "mamba_hybrid" in written["summary.md"].read_text(encoding="utf-8")


if __name__ == "__main__":
    test_visualize_ablation_writes_svg_and_summary()
    print("All visualization contract tests passed.")
