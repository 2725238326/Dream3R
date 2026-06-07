from __future__ import annotations

import json
from pathlib import Path

from dream3r.scripts.verify_v11_release import verify


def test_verify_v11_release_passes_repo_root():
    report = verify(Path(".").resolve(), check_frozen_core=False)

    assert report["status"] == "pass"
    assert report["version"] == "v1.1-rc1"
    assert report["candidate"] == "domain_conditional_vggt_teacher"
    assert report["metrics"]["kitti_abs_rel"] == 0.1448
    assert report["metrics"]["eth3d_abs_rel"] == 0.0570
    json.dumps(report)
