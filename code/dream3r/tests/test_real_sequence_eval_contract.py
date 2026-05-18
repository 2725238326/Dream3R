"""Contract test for real-sequence evaluation orchestration."""

from unittest.mock import patch

import torch

from dream3r.evaluate_real_sequence import run_real_sequence_eval


class _FakeDataset:
    def __init__(self, *args, **kwargs):
        self.sample = {
            "features": torch.zeros(4, 196, 768),
            "pointmap_gt": torch.ones(4, 196, 3),
            "pointmap_mask": torch.ones(4, 196),
            "conflict_label": torch.tensor(0.0),
            "sequence_name": "fake_seq",
            "frame_ids": ["0000000000", "0000000001", "0000000002", "0000000003"],
        }

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        return self.sample


class _FakeRecurrence:
    backend = "fake_backend"
    backend_error = ""


class _FakeMemory:
    state_recurrence = _FakeRecurrence()


class _FakeModel:
    memory = _FakeMemory()

    def __init__(self, *args, **kwargs):
        pass

    def to(self, device):
        return self

    def eval(self):
        return self

    def __call__(self, x, **kwargs):
        device = x.device
        return {
            "pointmap": torch.zeros(1, 4, 196, 3, device=device),
            "conflict_score": torch.zeros(1, 1, device=device),
            "nsa_branch_weights": torch.tensor([[[0.2, 0.7, 0.1]]], device=device),
            "bank_occupancy": torch.tensor([12.0], device=device),
            "latent_drift_proxy": torch.tensor([0.3], device=device),
            "memory_retrieval_log": {
                "promoted_to_stable": torch.ones(1, device=device),
                "selected_3d_distances": torch.tensor([0.5], device=device),
                "geometry_bias_applied": torch.ones(1, device=device),
            },
            "critic_geometric_log": {
                "sampson_distance": torch.tensor([0.1], device=device),
                "covisible_inconsistency": torch.tensor([0.2], device=device),
                "depth_inconsistency": torch.tensor([0.3], device=device),
            },
            "recommended_action": torch.tensor([2], device=device),
            "routing_logits": torch.zeros(1, 5, device=device),
            "route_regret": torch.zeros(1, device=device),
            "latent_state_tokens": torch.zeros(1, 32, 128, device=device),
            "object_track_set": torch.zeros(1, 16, 128, device=device),
            "object_slot_poses": torch.zeros(1, 16, 7, device=device),
        }


def test_run_real_sequence_eval_contract_with_mocked_model():
    with patch("dream3r.evaluate_real_sequence.KITTIRectifiedSequenceDataset", _FakeDataset):
        with patch("dream3r.evaluate_real_sequence.Dream3R", _FakeModel):
            result = run_real_sequence_eval(
                data_root="/tmp/fake",
                max_windows=1,
                max_sequences=1,
                recurrence="mamba_hybrid",
                device_name="cpu",
            )

    assert result["dataset"] == "kitti_rectified"
    assert result["recurrence_backend"] == "fake_backend"
    assert result["window_count"] == 1
    assert result["metrics"]["n_samples"] == 1
    assert result["windows"][0]["sequence_name"] == "fake_seq"
    assert result["windows"][0]["nsa_branch_mean"]["selected"] == 0.7


if __name__ == "__main__":
    test_run_real_sequence_eval_contract_with_mocked_model()
    print("All real sequence evaluation contract tests passed.")
