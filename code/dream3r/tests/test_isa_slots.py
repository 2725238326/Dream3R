"""Tests for W16 ISA per-slot reference frames."""

import torch

from dream3r.model import build_dream3r
from dream3r.modules import Permanence


def test_permanence_returns_slot_poses():
    torch.manual_seed(0)
    perm = Permanence(d_input=16, d_slot=8, n_slots=3, n_iters=1)
    features = torch.randn(2, 5, 16)
    positions = torch.randn(2, 5, 3)

    out = perm(features, input_positions=positions)

    assert out["object_slot_poses"].shape == (2, 3, 7)
    assert torch.allclose(out["object_slot_poses"][..., 3], torch.ones(2, 3))
    assert torch.allclose(out["object_slot_poses"][..., 4:], torch.zeros(2, 3, 3))


def test_slot_pose_translation_tracks_apparent_motion():
    torch.manual_seed(0)
    perm = Permanence(d_input=8, d_slot=8, n_slots=2, n_iters=1)
    features = torch.ones(1, 6, 8)
    base_positions = torch.tensor([[[0.0, 0.0, 1.0],
                                    [0.1, 0.0, 1.0],
                                    [0.0, 0.1, 1.0],
                                    [0.1, 0.1, 1.0],
                                    [0.05, 0.0, 1.0],
                                    [0.0, 0.05, 1.0]]])

    out0 = perm(features, input_positions=base_positions)
    out1 = perm(
        features,
        prev_slots=out0["object_track_set"],
        input_positions=base_positions + torch.tensor([0.5, 0.0, 0.0]),
        prev_slot_poses=out0["object_slot_poses"],
    )
    out2 = perm(
        features,
        prev_slots=out1["object_track_set"],
        input_positions=base_positions + torch.tensor([1.0, 0.0, 0.0]),
        prev_slot_poses=out1["object_slot_poses"],
    )

    x0 = out0["object_slot_poses"][..., 0].mean()
    x1 = out1["object_slot_poses"][..., 0].mean()
    x2 = out2["object_slot_poses"][..., 0].mean()
    assert x0 < x1 < x2


def test_multi_window_slot_poses_follow_synthetic_camera_motion():
    torch.manual_seed(0)
    perm = Permanence(d_input=8, d_slot=8, n_slots=3, n_iters=1)
    features = torch.ones(1, 9, 8)
    base_positions = torch.tensor([[
        [0.0, 0.0, 1.0],
        [0.1, 0.0, 1.0],
        [0.2, 0.0, 1.0],
        [0.0, 0.1, 1.0],
        [0.1, 0.1, 1.0],
        [0.2, 0.1, 1.0],
        [0.0, 0.2, 1.0],
        [0.1, 0.2, 1.0],
        [0.2, 0.2, 1.0],
    ]])

    prev_slots = None
    prev_poses = None
    pose_means = []
    for step in range(6):
        shift = torch.tensor([0.2 * step, -0.05 * step, 0.0])
        out = perm(
            features,
            prev_slots=prev_slots,
            input_positions=base_positions + shift,
            prev_slot_poses=prev_poses,
        )
        pose_means.append(out["object_slot_poses"][..., :3].mean(dim=1))
        prev_slots = out["object_track_set"]
        prev_poses = out["object_slot_poses"]

    pose_means = torch.stack(pose_means, dim=0).squeeze(1)
    x_deltas = pose_means[1:, 0] - pose_means[:-1, 0]
    y_deltas = pose_means[1:, 1] - pose_means[:-1, 1]

    assert torch.all(x_deltas > 0.05)
    assert torch.all(y_deltas < -0.01)
    assert pose_means[-1, 0] - pose_means[0, 0] > 0.5
    assert pose_means[-1, 1] - pose_means[0, 1] < -0.1


def test_pose_aware_matching_overrides_wrong_feature_match():
    prev_slots = torch.eye(2).view(1, 2, 2)
    current_slots = prev_slots[:, [1, 0], :]
    prev_poses = torch.tensor([[[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                [10.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]]])
    current_poses = torch.tensor([[[0.1, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                   [9.9, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]]])

    baseline_idx, _ = Permanence.match_slots(current_slots, prev_slots)
    pose_idx, _ = Permanence.match_slots(
        current_slots, prev_slots, current_poses, prev_poses, pose_weight=4.0
    )

    assert baseline_idx.tolist() == [[1, 0]]
    assert pose_idx.tolist() == [[0, 1]]


def test_pose_aware_matching_beats_feature_only_when_identity_is_unreliable():
    prev_slots = torch.eye(3).view(1, 3, 3)
    current_slots = prev_slots[:, [1, 0, 2], :] * 0.7 + prev_slots * 0.3
    prev_poses = torch.tensor([[[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                [4.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                [8.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]]])
    current_poses = torch.tensor([[[0.1, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                   [4.1, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                                   [7.9, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]]])

    feature_idx, _ = Permanence.match_slots(current_slots, prev_slots)
    pose_idx, _ = Permanence.match_slots(
        current_slots, prev_slots, current_poses, prev_poses, pose_weight=6.0
    )

    feature_pose_distance = (
        current_poses[0, :, :3] - prev_poses[0, feature_idx[0], :3]
    ).norm(dim=-1).mean()
    pose_distance = (
        current_poses[0, :, :3] - prev_poses[0, pose_idx[0], :3]
    ).norm(dim=-1).mean()

    assert feature_idx.tolist() == [[1, 0, 2]]
    assert pose_idx.tolist() == [[0, 1, 2]]
    assert pose_distance < feature_pose_distance


def test_model_carries_slot_poses_across_windows():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    x = torch.randn(1, 4, 16, 768)

    with torch.no_grad():
        out0 = model(x, timestep=0)
        out1 = model(
            x,
            prev_memory_state=out0["latent_state_tokens"],
            prev_object_slots=out0["object_track_set"],
            prev_object_slot_poses=out0["object_slot_poses"],
            timestep=1,
        )

    assert out0["object_slot_poses"].shape[-1] == 7
    assert out1["slot_match_indices"].shape == (1, 16)


if __name__ == "__main__":
    test_permanence_returns_slot_poses()
    test_slot_pose_translation_tracks_apparent_motion()
    test_multi_window_slot_poses_follow_synthetic_camera_motion()
    test_pose_aware_matching_overrides_wrong_feature_match()
    test_pose_aware_matching_beats_feature_only_when_identity_is_unreliable()
    test_model_carries_slot_poses_across_windows()
    print("All ISA slot tests passed.")
