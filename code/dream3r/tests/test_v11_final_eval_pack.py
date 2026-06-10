from __future__ import annotations

import json
from pathlib import Path

from dream3r.scripts.build_v11_final_eval_pack import build_final_eval_pack


def test_build_v11_final_eval_pack_writes_summary_and_table(tmp_path):
    summary = build_final_eval_pack(
        root=Path(".").resolve(),
        output_dir=tmp_path / "eval",
        table_path=tmp_path / "FINAL_EVAL_TABLE_V1_1.md",
    )

    summary_path = tmp_path / "eval" / "final_eval_summary.json"
    table_path = tmp_path / "FINAL_EVAL_TABLE_V1_1.md"

    assert summary["status"] == "pass"
    assert summary["version"] == "v1.1.0"
    assert summary["candidate"] == "domain_conditional_vggt_teacher"
    assert summary["formal_benchmark_rerun"] is False
    assert summary["official_v1_1"]["metrics"]["kitti_state_abs_rel"] == 0.1448
    assert summary["official_v1_1"]["metrics"]["eth3d_state_abs_rel"] == 0.057
    assert summary["stable_fallback_v1_0"]["metrics"]["eth3d_abs_rel"] == 0.1475
    assert summary_path.exists()
    assert table_path.exists()

    written = json.loads(summary_path.read_text(encoding="utf-8"))
    assert written["source_json_paths"]["unified_gate"].endswith(
        "unified_gate_candidate_with_kitti_no_state_server.json"
    )
    table = table_path.read_text(encoding="utf-8")
    assert "not a new benchmark rerun" in table
    assert "Qwen" in table
