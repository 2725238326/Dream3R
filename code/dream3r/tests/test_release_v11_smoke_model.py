from __future__ import annotations

import json

from dream3r.scripts.smoke_v11_release_model import run_smoke


def test_v11_release_smoke_writes_both_domain_branches(tmp_path):
    output = tmp_path / "smoke.json"

    report = run_smoke(output=output, seed=11, batch=1, views=1, patches=3)

    assert report["status"] == "pass"
    assert report["version"] == "v1.1.0"
    assert report["branches"]["kitti"]["domain_branch"] == "kitti_v1_0_rc1"
    assert report["branches"]["eth3d"]["domain_branch"] == "eth3d_vggt_omega_scf"
    assert report["branches"]["kitti"]["final_pointmap_shape"] == [1, 1, 3, 3]
    assert report["branches"]["eth3d"]["final_pointmap_shape"] == [1, 1, 3, 3]
    assert output.exists()
    json.loads(output.read_text(encoding="utf-8"))
