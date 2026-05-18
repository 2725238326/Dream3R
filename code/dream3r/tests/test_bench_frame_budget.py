"""Tests for frame-budget architecture metric profiling."""

import io
from contextlib import redirect_stdout

import torch

from dream3r.bench_frame_budget import (
    collect_architecture_metrics,
    print_report,
    profile_model,
)


class FakeProfileModel:
    def __init__(self):
        self.profile = False
        self.calls = 0

    def eval(self):
        return self

    def __call__(self, x, regime, prev_memory_state=None,
                 prev_object_slots=None, timestep=0):
        self.calls += 1
        batch = x.shape[0]
        return {
            "timings": {
                "perceiver_ms": 1.0 + 0.1 * timestep,
                "memory_ms": 2.0 + 0.1 * timestep,
            },
            "latent_state_tokens": torch.ones(batch, 2, 4),
            "object_track_set": torch.ones(batch, 3, 4),
            "bank_occupancy": torch.tensor([0.25] * batch),
            "nsa_branch_weights": torch.tensor([[[0.5, 0.5, 0.0],
                                                  [0.5, 0.5, 0.0]]]).repeat(batch, 1, 1),
            "memory_retrieval_log": {
                "selected_3d_distances": torch.tensor([[[0.1, 0.2]]]).repeat(batch, 1, 1),
                "geometry_bias_applied": torch.tensor(1.0),
                "branch_active_mask": torch.tensor([[[True, True, False],
                                                      [True, True, False]]]).repeat(batch, 1, 1),
            },
            "latent_drift_proxy": torch.tensor([[0.3]]).repeat(batch, 1),
            "routing_logits": torch.tensor([[2.0, 0.0, -1.0]]).repeat(batch, 1),
        }


def test_collect_architecture_metrics_from_forward_output():
    metrics = {}
    out = FakeProfileModel()(torch.zeros(1, 1, 1, 1), torch.zeros(1, 3))

    collect_architecture_metrics(out, metrics)

    assert metrics["bank_occupancy"][0] == 0.25
    assert metrics["branch_selected"][0] == 0.5
    assert metrics["active_branch_count"][0] == 2.0
    assert abs(metrics["selected_anchor_3d_distance"][0] - 0.15) < 1e-6
    assert metrics["geometry_bias_applied"][0] == 1.0
    assert abs(metrics["state_drift_magnitude"][0] - 0.3) < 1e-6
    assert metrics["routing_entropy"][0] > 0.0


def test_profile_model_returns_architecture_and_memory_sections():
    model = FakeProfileModel()
    x = torch.zeros(1, 1, 1, 1)
    regime = torch.zeros(1, 3)

    results = profile_model(model, x, regime, n_windows=3, warmup=1)

    assert "total" in results
    assert "architecture" in results
    assert "memory" in results
    assert results["architecture"]["bank_occupancy"] == 0.25
    assert results["architecture"]["active_branch_count"] == 2.0
    assert results["memory"]["peak_allocated_mb"] == 0.0


def test_print_report_includes_architecture_and_memory():
    results = {
        "memory_ms": {"p50": 2.0, "p95": 2.0, "p99": 2.0, "mean": 2.0, "min": 2.0, "max": 2.0},
        "total": {"p50": 4.0, "p95": 4.0, "p99": 4.0, "mean": 4.0, "min": 4.0, "max": 4.0},
        "architecture": {"bank_occupancy": 0.25, "branch_entropy": 0.69},
        "memory": {"peak_allocated_mb": 0.0, "peak_reserved_mb": 0.0},
    }
    buf = io.StringIO()

    with redirect_stdout(buf):
        print_report(results)
    text = buf.getvalue()

    assert "Architecture metrics" in text
    assert "bank_occupancy" in text
    assert "peak_allocated_mb" in text


if __name__ == "__main__":
    test_collect_architecture_metrics_from_forward_output()
    test_profile_model_returns_architecture_and_memory_sections()
    test_print_report_includes_architecture_and_memory()
    print("All frame budget profiler tests passed.")
