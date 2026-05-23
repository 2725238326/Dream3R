"""Contract tests for Stage 2 memory ablation evaluation."""

from pathlib import Path
from unittest.mock import patch

import torch

from dream3r.scripts.eval_memory_ablation import (
    _relative_improvement,
    run_memory_ablation,
)


class _FakeDataset:
    def __init__(self, *args, **kwargs):
        self.samples = []
        for idx in range(2):
            self.samples.append({
                "features": torch.zeros(1, 2, 3, 768),
                "pointmap_gt": torch.ones(1, 2, 3, 3),
                "pointmap_mask": torch.ones(1, 2, 3),
                "sequence_name": "fake_seq",
                "frame_ids": [[f"{idx:010d}", f"{idx + 1:010d}"]],
            })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


class _FakeModel:
    def __init__(self, *args, **kwargs):
        self.calls = 0

    def to(self, device):
        self.device = device
        return self

    def eval(self):
        return self

    def __call__(self, features, prev_memory_state=None, **kwargs):
        self.calls += 1
        value = 1.0 if prev_memory_state is None else 0.5
        device = features.device
        return {
            "pointmap": torch.full((1, 2, 3, 3), value, device=device),
            "latent_state_tokens": torch.full((1, 2, 4), value, device=device),
            "object_track_set": torch.zeros(1, 16, 128, device=device),
            "object_slot_poses": torch.zeros(1, 16, 7, device=device),
            "nsa_selected_indices": torch.zeros(1, 3, 2, dtype=torch.long, device=device),
            "latent_drift_proxy": torch.tensor([[value]], device=device),
            "bank_occupancy": torch.tensor([self.calls], dtype=torch.float32, device=device),
        }


def test_relative_improvement_handles_zero_baseline():
    assert _relative_improvement(0.0, 1.0) == 0.0
    assert _relative_improvement(10.0, 8.0) == 0.2


def test_run_memory_ablation_writes_table_and_plot(tmp_path: Path):
    with patch("dream3r.scripts.eval_memory_ablation.KITTILongSequenceDataset", _FakeDataset):
        with patch("dream3r.scripts.eval_memory_ablation.Dream3R", _FakeModel):
            with patch("dream3r.scripts.eval_memory_ablation._load_checkpoint", lambda *args: None):
                result = run_memory_ablation(
                    checkpoint="/tmp/fake.pt",
                    data_root="/tmp/fake",
                    output_dir=str(tmp_path),
                    max_windows=2,
                    max_sequences=1,
                    copy_overlap_memory=True,
                    device_name="cpu",
                )

    assert set(result["variants"]) == {"no_memory_reset", "memory_on"}
    assert "pointmap_drift" in result["relative_improvement"]
    assert result["copy_overlap_memory"] is True
    assert (tmp_path / "memory_ablation.json").exists()
    assert (tmp_path / "memory_ablation.csv").exists()
    assert (tmp_path / "memory_ablation.svg").exists()
