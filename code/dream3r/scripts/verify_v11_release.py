"""Verify the Dream3R v1.1.0 official domain-conditional model package."""

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

import dream3r as dream3r_pkg  # noqa: E402
from dream3r.release_v11 import (  # noqa: E402
    RELEASE_V11_CANDIDATE,
    RELEASE_V11_VERSION,
    build_dream3r_v11_release,
)


EXPERIMENTAL_CORE_UNFREEZE = (
    "code/dream3r/model.py",
    "code/dream3r/modules.py",
    "code/dream3r/config.py",
)

STABLE_CORE = (
    "code/dream3r/anchor_bank.py",
    "code/dream3r/nsa_attention.py",
    "code/dream3r/bus.py",
    "code/dream3r/orchestrator.py",
    "code/dream3r/repair.py",
    "code/dream3r/contracts.py",
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


def _resolve_repo_path(root: Path, rel_path: str) -> Path | None:
    path = root / rel_path
    if path.exists():
        return path
    if rel_path.startswith("code/dream3r/"):
        package_rel = "dream3r/" + rel_path[len("code/dream3r/") :]
        package_path = root / package_rel
        if package_path.exists():
            return package_path
    return None


def _check_frozen_core(root: Path) -> list[str]:
    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if probe.returncode != 0:
        return []
    cmd = ["git", "diff", "--name-only", "--", *STABLE_CORE]
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(f"git stable-core diff check failed: {proc.stderr.strip()}")
    changed = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    if changed:
        raise AssertionError(f"stable core changed: {changed}")
    return list(STABLE_CORE)


def verify(root: Path, check_frozen_core: bool = True) -> dict[str, Any]:
    artifacts = _read_json(root / "release" / "ARTIFACTS.json")
    official = artifacts.get("official_release")
    if not isinstance(official, dict):
        raise AssertionError("release/ARTIFACTS.json missing official_release")
    if official.get("version") != RELEASE_V11_VERSION:
        raise AssertionError(f"official release version mismatch: {official.get('version')}")
    if official.get("candidate") != RELEASE_V11_CANDIDATE:
        raise AssertionError(
            f"official release candidate mismatch: {official.get('candidate')}"
        )
    effective = artifacts.get("current_effective_architecture")
    if not isinstance(effective, dict):
        raise AssertionError("release/ARTIFACTS.json missing current_effective_architecture")
    if effective.get("version") != RELEASE_V11_VERSION:
        raise AssertionError(f"effective architecture version mismatch: {effective.get('version')}")
    if effective.get("candidate") != RELEASE_V11_CANDIDATE:
        raise AssertionError(
            f"effective architecture candidate mismatch: {effective.get('candidate')}"
        )
    usable = artifacts.get("usable_model_v1_1")
    if not isinstance(usable, dict):
        raise AssertionError("release/ARTIFACTS.json missing usable_model_v1_1")
    if usable.get("version") != RELEASE_V11_VERSION:
        raise AssertionError(f"v1.1 version mismatch: {usable.get('version')}")
    if usable.get("candidate") != RELEASE_V11_CANDIDATE:
        raise AssertionError(f"v1.1 candidate mismatch: {usable.get('candidate')}")

    expected_package_version = (
        RELEASE_V11_VERSION[1:]
        if RELEASE_V11_VERSION.startswith("v")
        else RELEASE_V11_VERSION
    )
    package_version = getattr(dream3r_pkg, "__version__", None)
    if package_version != expected_package_version:
        raise AssertionError(
            f"dream3r.__version__ mismatch: {package_version} != {expected_package_version}"
        )

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
    if effective.get("kitti_abs_rel") != usable["kitti_abs_rel"]:
        raise AssertionError("KITTI metric mismatch between effective and usable manifests")
    if effective.get("eth3d_abs_rel") != usable["eth3d_abs_rel"]:
        raise AssertionError("ETH3D metric mismatch between effective and usable manifests")
    if official.get("kitti_abs_rel") != usable["kitti_abs_rel"]:
        raise AssertionError("KITTI metric mismatch between official and usable manifests")
    if official.get("eth3d_abs_rel") != usable["eth3d_abs_rel"]:
        raise AssertionError("ETH3D metric mismatch between official and usable manifests")
    expected_cache_demo = "code/dream3r/scripts/run_dream3r_v11_cache_demo.py"
    for name, section in (
        ("official_release", official),
        ("current_effective_architecture", effective),
        ("usable_model_v1_1", usable),
    ):
        if section.get("cache_demo_script") != expected_cache_demo:
            raise AssertionError(f"{name} missing v1.1 cache-demo script")
        cache_artifacts = section.get("cache_demo_artifacts")
        if not isinstance(cache_artifacts, list) or len(cache_artifacts) != 2:
            raise AssertionError(f"{name} missing v1.1 cache-demo artifacts")

    docs_checked = []
    for rel_path in (
        "release/OFFICIAL_VERSION.md",
        "release/EFFECTIVE_ARCHITECTURE_V1_1.md",
        "release/MODEL_CARD_V1_1.md",
        "release/ARCHITECTURE_DIAGRAM_V1_1.md",
        "release/AFTERNOON_DELIVERABLE_V1_1.md",
        "release/COMPLETE_MODEL_V1_1.md",
        "release/USABLE_MODEL_V1_1.md",
        "release/RUNBOOK.md",
        "release/PUBLISH_CHECKLIST.md",
        "release/REPRODUCE.md",
        "release/VERIFY_REPORT.md",
        "release/ARTIFACTS.json",
        "release/ARCHITECTURE_STATUS.json",
        "ARCHITECTURE.md",
        "TASK_SNAPSHOT.md",
        "INDEX.md",
        "README.md",
        "WORKFLOW_STATUS.md",
        "code/dream3r/scripts/run_dream3r_v11_demo.py",
        "code/dream3r/scripts/run_dream3r_v11_cache_demo.py",
        "code/dream3r/tests/test_v11_demo_script.py",
        "runs/release/v11_cache_demo/cache_demo_kitti.json",
        "runs/release/v11_cache_demo/cache_demo_eth3d.json",
        "planning/DREAM3R_CLEAN_ARCHITECTURE_MAP_20260608.md",
    ):
        if _resolve_repo_path(root, rel_path) is None:
            raise AssertionError(f"missing v1.1 doc: {rel_path}")
        docs_checked.append(rel_path)

    frozen = _check_frozen_core(root) if check_frozen_core else []
    stable_core_check_mode = (
        "skipped_by_flag"
        if not check_frozen_core
        else "git_diff"
        if frozen
        else "skipped_not_git_repo"
    )
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
            "package_version": package_version,
            "policy": meta["policy"],
            "expert_order": meta["expert_order"],
        },
        "docs_checked": docs_checked,
        "stable_core_checked": frozen,
        "stable_core_check_mode": stable_core_check_mode,
        "experimental_core_unfreeze_allowed": list(EXPERIMENTAL_CORE_UNFREEZE),
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
