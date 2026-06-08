"""Verify the Dream3R v1.0-rc1 release package.

This is a read-only consistency gate. It does not train models or touch GPU
state; it checks the local mirrored artifacts, release docs, selected metrics,
state-causality control, and frozen-core edit policy.
"""

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

from dream3r.release_candidate import (
    RELEASE_CANDIDATE,
    RELEASE_VERSION,
    build_dream3r_release_candidate,
)

EXPECTED_RC = RELEASE_CANDIDATE
EXPECTED_VERSION = RELEASE_VERSION
METRIC_TOL = 5e-5

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


def _check_close(name: str, actual: float, expected: float) -> None:
    if abs(float(actual) - float(expected)) > METRIC_TOL:
        raise AssertionError(f"{name}: expected {expected}, got {actual}")


def _metric(result: dict[str, Any], domain: str) -> float:
    return float(result["final_eval"][domain]["Ours_ProposalSetDecoder"])


def _check_docs(root: Path, artifact_manifest: dict[str, Any]) -> list[str]:
    checked: list[str] = []
    for label, rel_path in artifact_manifest["release_docs"].items():
        path = root / rel_path
        if not path.exists():
            raise AssertionError(f"missing release doc {label}: {rel_path}")
        checked.append(rel_path)
    return checked


def _check_local_artifacts(root: Path, artifact_manifest: dict[str, Any]) -> list[str]:
    checked: list[str] = []
    for label, rel_path in artifact_manifest["local_mirrors"].items():
        path = root / rel_path
        if not path.exists():
            server_path = artifact_manifest.get("server_artifacts", {}).get(label)
            if server_path:
                path = Path(server_path)
        if not path.exists():
            raise AssertionError(f"missing local mirror {label}: {rel_path}")
        _read_json(path)
        checked.append(str(path if path.is_absolute() else rel_path))
    return checked


def _check_selected_metrics(root: Path, artifact_manifest: dict[str, Any]) -> dict[str, float]:
    selected = artifact_manifest["selected_metrics"]
    state = _read_json(root / artifact_manifest["local_mirrors"]["bounded_state"])
    shuffle = _read_json(root / artifact_manifest["local_mirrors"]["bounded_shuffle"])

    kitti = _metric(state, "kitti")
    eth3d = _metric(state, "eth3d")
    shuffle_kitti = _metric(shuffle, "kitti")
    shuffle_eth3d = _metric(shuffle, "eth3d")

    _check_close("kitti_abs_rel", kitti, selected["kitti_abs_rel"])
    _check_close("eth3d_abs_rel", eth3d, selected["eth3d_abs_rel"])
    _check_close("shuffle_kitti_abs_rel", shuffle_kitti, selected["shuffle_kitti_abs_rel"])
    _check_close("shuffle_eth3d_abs_rel", shuffle_eth3d, selected["shuffle_eth3d_abs_rel"])

    if not (kitti < shuffle_kitti and eth3d < shuffle_eth3d):
        raise AssertionError(
            "state-causality check failed: correct-state must beat shuffle-state "
            f"on both domains, got {kitti}/{eth3d} vs {shuffle_kitti}/{shuffle_eth3d}"
        )

    return {
        "kitti_abs_rel": kitti,
        "eth3d_abs_rel": eth3d,
        "shuffle_kitti_abs_rel": shuffle_kitti,
        "shuffle_eth3d_abs_rel": shuffle_eth3d,
    }


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


def _check_official_api() -> dict[str, Any]:
    model = build_dream3r_release_candidate(d_memory=8)
    meta = model.release_metadata()
    if meta["version"] != EXPECTED_VERSION:
        raise AssertionError(f"official API version mismatch: {meta['version']}")
    if meta["release_candidate"] != EXPECTED_RC:
        raise AssertionError(
            f"official API release candidate mismatch: {meta['release_candidate']}"
        )
    if meta["expert_order"] != ["fast3r", "mast3r", "spann3r"]:
        raise AssertionError(f"official API expert order mismatch: {meta['expert_order']}")
    return {
        "version": meta["version"],
        "release_candidate": meta["release_candidate"],
        "expert_order": meta["expert_order"],
    }


def verify(root: Path, check_frozen_core: bool = True) -> dict[str, Any]:
    artifacts_path = root / "release" / "ARTIFACTS.json"
    artifacts = _read_json(artifacts_path)
    fallback = artifacts.get("stable_fallback_v1_0")
    if not isinstance(fallback, dict):
        fallback = artifacts

    if fallback.get("release_candidate") != EXPECTED_RC:
        raise AssertionError(
            f"release_candidate expected {EXPECTED_RC}, got {fallback.get('release_candidate')}"
        )
    if fallback.get("version") != EXPECTED_VERSION:
        raise AssertionError(f"version expected {EXPECTED_VERSION}, got {fallback.get('version')}")

    docs = _check_docs(root, artifacts)
    mirrors = _check_local_artifacts(root, artifacts)
    metrics_manifest = dict(artifacts)
    metrics_manifest["selected_metrics"] = fallback.get(
        "selected_metrics",
        artifacts.get("selected_metrics"),
    )
    metrics = _check_selected_metrics(root, metrics_manifest)
    frozen = _check_frozen_core(root) if check_frozen_core else []
    stable_core_check_mode = (
        "skipped_by_flag"
        if not check_frozen_core
        else "git_diff"
        if frozen
        else "skipped_not_git_repo"
    )
    official_api = _check_official_api()

    return {
        "status": "pass",
        "version": EXPECTED_VERSION,
        "release_candidate": EXPECTED_RC,
        "metrics": metrics,
        "docs_checked": docs,
        "local_mirrors_checked": mirrors,
        "stable_core_checked": frozen,
        "stable_core_check_mode": stable_core_check_mode,
        "experimental_core_unfreeze_allowed": list(EXPERIMENTAL_CORE_UNFREEZE),
        "official_api": official_api,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="repository root")
    parser.add_argument(
        "--skip-frozen-core",
        action="store_true",
        help="skip git diff check for frozen core files",
    )
    args = parser.parse_args()

    root = args.root.resolve() if args.root else _find_repo_root(Path(__file__).resolve())
    report = verify(root, check_frozen_core=not args.skip_frozen_core)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
