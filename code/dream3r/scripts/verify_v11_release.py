"""Verify the Dream3R v1.1 usable domain-conditional model package."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_CODE_ROOT = Path(__file__).resolve().parents[2]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

from dream3r.release_v11 import (  # noqa: E402
    RELEASE_V11_CANDIDATE,
    RELEASE_V11_VERSION,
    build_dream3r_v11_release,
)


FROZEN_CORE = (
    "code/dream3r/model.py",
    "code/dream3r/anchor_bank.py",
    "code/dream3r/nsa_attention.py",
    "code/dream3r/bus.py",
    "code/dream3r/orchestrator.py",
    "code/dream3r/repair.py",
    "code/dream3r/modules.py",
    "code/dream3r/contracts.py",
    "code/dream3r/config.py",
)


def _find_repo_root(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / "release" / "ARTIFACTS.json").exists():
            return path
    raise RuntimeError("could not locate repo root from release/ARTIFACTS.json")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data


def _check_frozen_core(root: Path) -> list[str]:
    cmd = ["git", "diff", "--name-only", "--", *FROZEN_CORE]
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git frozen-core diff check failed: {proc.stderr.strip()}")
    changed = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if changed:
        raise AssertionError(f"frozen core changed: {changed}")
    return list(FROZEN_CORE)


def verify(root: Path, check_frozen_core: bool = True) -> dict[str, Any]:
    artifacts = _read_json(root / "release" / "ARTIFACTS.json")
    usable = artifacts.get("usable_model_v1_1")
    if not isinstance(usable, dict):
        raise AssertionError("release/ARTIFACTS.json missing usable_model_v1_1")
    if usable.get("version") != RELEASE_V11_VERSION:
        raise AssertionError(f"v1.1 version mismatch: {usable.get('version')}")
    if usable.get("candidate") != RELEASE_V11_CANDIDATE:
        raise AssertionError(f"v1.1 candidate mismatch: {usable.get('candidate')}")

    gate_rel = usable.get("unified_gate_artifact")
    if not gate_rel:
        raise AssertionError("usable_model_v1_1 missing unified_gate_artifact")
    gate = _read_json(root / gate_rel)
    if gate.get("status") != "pass" or gate.get("promotable_to_official") is not True:
        raise AssertionError("v1.1 unified gate is not pass/promotable")

    metrics = gate["metrics"]
    controls = gate["controls"]
    for name, passed in controls.items():
        if not passed:
            raise AssertionError(f"v1.1 control failed: {name}")

    model = build_dream3r_v11_release()
    meta = model.release_metadata()
    if meta["version"] != RELEASE_V11_VERSION:
        raise AssertionError(f"API version mismatch: {meta['version']}")
    if meta["release_candidate"] != RELEASE_V11_CANDIDATE:
        raise AssertionError(f"API candidate mismatch: {meta['release_candidate']}")
    if meta["selected_kitti_abs_rel"] != usable["kitti_abs_rel"]:
        raise AssertionError("KITTI metric mismatch between API and artifact manifest")
    if meta["selected_eth3d_abs_rel"] != usable["eth3d_abs_rel"]:
        raise AssertionError("ETH3D metric mismatch between API and artifact manifest")

    docs_checked = []
    for rel_path in (
        "release/USABLE_MODEL_V1_1.md",
        "release/ARTIFACTS.json",
        "release/ARCHITECTURE_STATUS.json",
        "ARCHITECTURE.md",
    ):
        path = root / rel_path
        if not path.exists():
            raise AssertionError(f"missing v1.1 doc: {rel_path}")
        docs_checked.append(rel_path)

    frozen = _check_frozen_core(root) if check_frozen_core else []
    return {
        "status": "pass",
        "version": RELEASE_V11_VERSION,
        "candidate": RELEASE_V11_CANDIDATE,
        "metrics": {
            "kitti_abs_rel": metrics["kitti_state_abs_rel"],
            "kitti_no_state_abs_rel": metrics["kitti_no_state_abs_rel"],
            "kitti_shuffle_abs_rel": metrics["kitti_shuffle_abs_rel"],
            "eth3d_abs_rel": metrics["eth3d_state_abs_rel"],
            "eth3d_no_state_abs_rel": metrics["eth3d_no_state_abs_rel"],
            "eth3d_shuffle_abs_rel": metrics["eth3d_shuffle_abs_rel"],
        },
        "api": {
            "builder": "dream3r.release_v11.build_dream3r_v11_release",
            "policy": meta["policy"],
            "expert_order": meta["expert_order"],
        },
        "docs_checked": docs_checked,
        "frozen_core_checked": frozen,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    parser.add_argument("--skip-frozen-core", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve() if args.root else _find_repo_root(Path(__file__).resolve())
    report = verify(root, check_frozen_core=not args.skip_frozen_core)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

