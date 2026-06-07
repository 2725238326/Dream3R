"""Stage and optionally run the VGGT-Omega admission gate.

This wrapper makes the DEC-026 one-window smoke resumable. It checks the
upstream repo, gated checkpoint, Hugging Face token state, and smoke image list,
then optionally downloads the checkpoint and invokes ``smoke_vggt_omega_adapter``.
It is intentionally non-core and writes a machine-readable status JSON for
blocked runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


SCHEMA_VERSION = "dream3r_vggt_omega_admission_stage_v1"
DEFAULT_REPO = "/hdd3/kykt26/externals/vggt-omega"
DEFAULT_CHECKPOINT = "/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt"
DEFAULT_HF_FILENAME = "vggt_omega_1b_512.pt"
DEFAULT_IMAGE_LIST = "runs/v22_admission/vggt_omega_smoke/images.txt"
DEFAULT_OUTPUT = "runs/v22_admission/vggt_omega_smoke/results.json"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _has_hf_token() -> bool:
    return bool(
        os.environ.get("HF_TOKEN")
        or os.environ.get("HUGGINGFACE_HUB_TOKEN")
        or Path.home().joinpath(".cache", "huggingface", "token").exists()
    )


def _download_checkpoint(
    checkpoint: Path,
    hf_repo: str,
    hf_filename: str,
) -> Dict[str, Any]:
    try:
        from huggingface_hub import hf_hub_download
    except Exception as exc:  # pragma: no cover - depends on server env
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: huggingface_hub unavailable: {exc}",
        }
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    try:
        downloaded = Path(hf_hub_download(
            repo_id=hf_repo,
            filename=hf_filename,
            local_dir=str(checkpoint.parent),
            local_dir_use_symlinks=False,
            token=os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN") or True,
        ))
        if checkpoint.exists() and checkpoint.resolve() != downloaded.resolve():
            checkpoint.unlink()
        if not checkpoint.exists():
            try:
                os.link(downloaded, checkpoint)
            except OSError:
                import shutil

                shutil.copy2(downloaded, checkpoint)
        return {"ok": True, "downloaded_path": str(downloaded)}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def stage_vggt_omega_admission(
    repo: str = DEFAULT_REPO,
    checkpoint: str = DEFAULT_CHECKPOINT,
    image_list: str = DEFAULT_IMAGE_LIST,
    output: str = DEFAULT_OUTPUT,
    hf_repo: str = "facebook/VGGT-Omega",
    hf_filename: str = DEFAULT_HF_FILENAME,
    download: bool = False,
    run_smoke: bool = False,
    device: str = "auto",
    image_resolution: int = 512,
    resize_mode: str = "balanced",
    env_python: Optional[str] = None,
) -> Dict[str, Any]:
    repo_path = Path(repo)
    checkpoint_path = Path(checkpoint)
    image_list_path = Path(image_list)
    output_path = Path(output)
    if not image_list_path.is_absolute():
        image_list_path = Path.cwd() / image_list_path
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    result: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "adapter": "vggt_omega",
        "repo": str(repo_path),
        "checkpoint": str(checkpoint_path),
        "image_list": str(image_list_path),
        "output": str(output_path),
        "hf_repo": hf_repo,
        "hf_filename": hf_filename,
        "download_requested": download,
        "run_smoke_requested": run_smoke,
        "hf_token_present": _has_hf_token(),
        "status": "blocked",
        "backend": "not_run",
        "failure_flags": [],
    }

    if not repo_path.exists():
        result["failure_flags"].append(f"repo_missing:{repo_path}")
    if not image_list_path.exists():
        result["failure_flags"].append(f"image_list_missing:{image_list_path}")

    if not checkpoint_path.exists() and download:
        if not result["hf_token_present"]:
            result["failure_flags"].append("hf_token_missing")
        else:
            dl = _download_checkpoint(checkpoint_path, hf_repo, hf_filename)
            result["download"] = dl
            if not dl["ok"]:
                result["failure_flags"].append("checkpoint_download_failed")

    if not checkpoint_path.exists():
        result["failure_flags"].append(f"checkpoint_missing:{checkpoint_path}")
    else:
        result["checkpoint_size"] = checkpoint_path.stat().st_size
        result["checkpoint_sha256"] = _sha256(checkpoint_path)

    if result["failure_flags"]:
        _write_json(output_path, result)
        return result

    if not run_smoke:
        result["status"] = "ready"
        result["backend"] = "checkpoint_staged"
        _write_json(output_path, result)
        return result

    python_exe = env_python or sys.executable
    command = [
        python_exe,
        "-m",
        "dream3r.scripts.smoke_vggt_omega_adapter",
        "--repo",
        str(repo_path),
        "--checkpoint",
        str(checkpoint_path),
        "--image-list",
        str(image_list_path),
        "--image-resolution",
        str(image_resolution),
        "--resize-mode",
        resize_mode,
        "--output",
        str(output_path),
        "--device",
        device,
    ]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    result["smoke_command"] = command
    result["smoke_returncode"] = completed.returncode
    result["smoke_output_tail"] = completed.stdout[-4000:]
    if completed.returncode != 0:
        result["failure_flags"].append("smoke_failed")
        _write_json(output_path.with_suffix(".stage.json"), result)
        return result
    smoke_result = json.loads(output_path.read_text(encoding="utf-8"))
    result["status"] = "admitted" if smoke_result.get("backend") == "real" else "blocked"
    result["backend"] = smoke_result.get("backend", "unknown")
    result["smoke_result"] = smoke_result
    _write_json(output_path.with_suffix(".stage.json"), result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--image-list", default=DEFAULT_IMAGE_LIST)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--hf-repo", default="facebook/VGGT-Omega")
    parser.add_argument("--hf-filename", default=DEFAULT_HF_FILENAME)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--run-smoke", action="store_true")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--image-resolution", type=int, default=512)
    parser.add_argument("--resize-mode", default="balanced")
    parser.add_argument("--env-python", default="")
    args = parser.parse_args()
    result = stage_vggt_omega_admission(
        repo=args.repo,
        checkpoint=args.checkpoint,
        image_list=args.image_list,
        output=args.output,
        hf_repo=args.hf_repo,
        hf_filename=args.hf_filename,
        download=args.download,
        run_smoke=args.run_smoke,
        device=args.device,
        image_resolution=args.image_resolution,
        resize_mode=args.resize_mode,
        env_python=args.env_python or None,
    )
    print(json.dumps({
        "schema_version": result["schema_version"],
        "status": result["status"],
        "backend": result["backend"],
        "failure_flags": result["failure_flags"],
        "checkpoint": result["checkpoint"],
        "output": result["output"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
