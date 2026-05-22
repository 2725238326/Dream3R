"""Contract test for real-data ablation orchestration."""

from unittest.mock import patch

from dream3r.ablate_real_sequence import run_real_sequence_ablation


def _fake_real_eval(
    data_root,
    max_windows,
    max_sequences,
    recurrence,
    device_name,
    config_overrides,
):
    memory_use_nsa = config_overrides["memory_use_nsa"]
    enable_stable_memory = config_overrides["enable_stable_memory"]
    selected = 0.7 if memory_use_nsa else 0.0
    return {
        "dataset": "kitti_rectified",
        "data_root": data_root,
        "device": device_name,
        "recurrence_type": recurrence,
        "recurrence_backend": "fake_backend",
        "recurrence_backend_error": "",
        "memory_use_nsa": memory_use_nsa,
        "enable_stable_memory": enable_stable_memory,
        "window_count": max_windows,
        "metrics": {
            "pointmap_l2": 1.25,
            "depth_rmse": 2.5,
            "n_samples": max_windows,
        },
        "windows": [
            {
                "elapsed_ms": 10.0,
                "bank_occupancy": 4.0,
                "latent_drift_proxy": 0.2,
                "stable_promotion_rate": 1.0 if enable_stable_memory else 0.0,
                "selected_anchor_3d_distance": 0.3,
                "conflict_score_mean": 0.4,
                "nsa_branch_mean": {
                    "compressed": 0.3,
                    "selected": selected,
                    "sliding": 0.0,
                },
            }
        ],
    }


def test_run_real_sequence_ablation_collects_four_variants():
    with patch("dream3r.ablate_real_sequence.run_real_sequence_eval", _fake_real_eval):
        result = run_real_sequence_ablation(
            data_root="/tmp/fake",
            max_windows=1,
            max_sequences=1,
            device_name="cpu",
        )

    assert set(result["variants"]) == {
        "baseline_cross_attention",
        "mamba_hybrid",
        "no_nsa",
        "no_stable_memory",
    }
    assert result["variants"]["no_nsa"]["config"]["memory_use_nsa"] is False
    assert result["variants"]["no_nsa"]["summary"]["nsa_branch_mean"]["selected"] == 0.0
    assert result["variants"]["no_stable_memory"]["config"]["enable_stable_memory"] is False
    assert result["variants"]["mamba_hybrid"]["summary"]["pointmap_l2"] == 1.25


if __name__ == "__main__":
    test_run_real_sequence_ablation_collects_four_variants()
    print("All real-data ablation contract tests passed.")
