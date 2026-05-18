"""Command-line entry point for local P0 ablation gates."""

from __future__ import annotations

from pathlib import Path
import argparse
import json

from memory_v03_p0.abl_memory_0 import run_abl_memory_0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Memory v0.3 P0 gates.")
    parser.add_argument("--abl", default="ABL-memory-0", choices=["ABL-memory-0"])
    parser.add_argument("--output", default="outputs", type=Path)
    args = parser.parse_args(argv)

    result = run_abl_memory_0(args.output)
    print(json.dumps({
        "abl_id": result["abl_id"],
        "status": result["status"],
        "output_dir": result["output_dir"],
    }, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
