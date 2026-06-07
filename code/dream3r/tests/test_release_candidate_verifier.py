from __future__ import annotations

from pathlib import Path

from dream3r.scripts.verify_release_candidate import _find_repo_root, verify


def test_release_candidate_package_verifies_without_git_check() -> None:
    repo_root = _find_repo_root(Path(__file__).resolve())
    report = verify(repo_root, check_frozen_core=False)

    assert report["status"] == "pass"
    assert report["version"] == "v1.0-rc1"
    assert report["release_candidate"] == "frozen_state_prior_bounded_residual"
    assert report["metrics"]["kitti_abs_rel"] == 0.1448
    assert report["metrics"]["eth3d_abs_rel"] == 0.1475
    assert report["metrics"]["kitti_abs_rel"] < report["metrics"]["shuffle_kitti_abs_rel"]
    assert report["metrics"]["eth3d_abs_rel"] < report["metrics"]["shuffle_eth3d_abs_rel"]
