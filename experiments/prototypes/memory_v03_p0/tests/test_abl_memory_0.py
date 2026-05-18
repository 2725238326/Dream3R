from __future__ import annotations

import csv
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_v03_p0.abl_memory_0 import run_abl_memory_0
from memory_v03_p0.config import P0Config
from memory_v03_p0.fixtures import generate_fixtures


def test_fixture_shapes_and_reproducible_hashes() -> None:
    config = P0Config()
    first = generate_fixtures(config)
    second = generate_fixtures(config)

    for name, expected_shape in config.expected_shapes().items():
        if name.startswith("bus."):
            actual_shape = list(first.bus[name.split(".", 1)[1]]["values"].shape)
        else:
            actual_shape = list(first.tensors()[name].shape)
        assert actual_shape == expected_shape

    assert first.manifest["raw_label_hashes"] == second.manifest["raw_label_hashes"]
    assert first.manifest["tensor_hashes"] == second.manifest["tensor_hashes"]


def test_run_abl_memory_0_outputs(tmp_path: Path) -> None:
    result = run_abl_memory_0(tmp_path)
    assert result["status"] == "pass"

    expected_files = {
        "fixtures_manifest.json",
        "write_log.jsonl",
        "metrics_abl_memory_0_8.csv",
        "summary_go_no_go.md",
        "evidence_boundary_update.md",
    }
    assert expected_files.issubset({path.name for path in tmp_path.iterdir()})

    manifest = json.loads((tmp_path / "fixtures_manifest.json").read_text(encoding="utf-8"))
    assert manifest["abl_memory_0_status"] == "pass"
    assert manifest["variant_input_audit"]["passed"] is True
    assert manifest["variant_input_audit"]["forbidden_present"] == []
    assert all(field["tag"] == "oracle_bus" for field in manifest["oracle_bus"].values())

    with (tmp_path / "metrics_abl_memory_0_8.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["abl_id"] == "ABL-memory-0"
    assert rows[0]["status"] == "pass"
    assert rows[1]["abl_id"] == "ABL-memory-1"
    assert rows[1]["status"] == "not_run_scope_deferred"


if __name__ == "__main__":
    test_fixture_shapes_and_reproducible_hashes()
    with tempfile.TemporaryDirectory() as temp_dir:
        test_run_abl_memory_0_outputs(Path(temp_dir))
