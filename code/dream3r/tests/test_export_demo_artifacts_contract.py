"""Contract test for demo artifact manifest creation helpers."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from dream3r.export_demo_artifacts import export_showcase


def test_export_showcase_writes_manifest_with_mocked_runs():
    demo_payload = {
        "device": "cuda",
        "variants": [
            {
                "recurrence_type": "cross_attention",
                "backend": "StateTokenRecurrence",
                "elapsed_ms_3_windows": 1.0,
                "state_delta_mean_abs": 0.5,
                "stable_promotion_rate": 1.0,
            },
            {
                "recurrence_type": "mamba_hybrid",
                "backend": "mamba_ssm",
                "elapsed_ms_3_windows": 0.8,
                "state_delta_mean_abs": 0.3,
                "stable_promotion_rate": 1.0,
            },
        ],
    }
    ablation_payload = {
        "variants": {
            "baseline_cross_attention": {
                "summary": {
                    "backend": "StateTokenRecurrence",
                    "elapsed_ms_mean": 1.0,
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
        },
    }

    def fake_run(module, args):
        if module == "dream3r.demo_mamba_path":
            return json.dumps(demo_payload)
        if module == "dream3r.ablate_recurrence":
            output = Path(args[args.index("--output") + 1])
            output.write_text(json.dumps(ablation_payload), encoding="utf-8")
            return json.dumps(ablation_payload)
        raise AssertionError(module)

    with tempfile.TemporaryDirectory() as tmp:
        with patch("dream3r.export_demo_artifacts._run_module", side_effect=fake_run):
            manifest = export_showcase(Path(tmp), windows=3, seeds=[33])

        assert manifest["demo_summary"]["device"] == "cuda"
        assert manifest["demo_summary"]["variants"]["mamba_hybrid"]["backend"] == "mamba_ssm"
        assert (Path(tmp) / "manifest.json").exists()
        assert (Path(tmp) / "README.md").exists()
        assert (Path(tmp) / "charts" / "summary.md").exists()


if __name__ == "__main__":
    test_export_showcase_writes_manifest_with_mocked_runs()
    print("All export demo artifact tests passed.")
