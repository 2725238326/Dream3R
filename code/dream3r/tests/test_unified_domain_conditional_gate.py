from __future__ import annotations

import json
from pathlib import Path

from dream3r.scripts.eval_unified_domain_conditional_gate import (
    evaluate_unified_domain_conditional_gate,
)


def _write(path: Path, domain: str, key: str, value: float) -> Path:
    path.write_text(
        json.dumps({"final_eval": {domain: {key: value}}}),
        encoding="utf-8",
    )
    return path


def test_unified_gate_blocks_when_kitti_no_state_is_missing(tmp_path: Path) -> None:
    out = evaluate_unified_domain_conditional_gate(
        kitti_state=_write(tmp_path / "ks.json", "kitti", "Ours_ProposalSetDecoder", 0.1448),
        kitti_shuffle=_write(tmp_path / "ksh.json", "kitti", "Ours_ProposalSetDecoder", 0.1521),
        eth3d_state=_write(tmp_path / "es.json", "eth3d", "Ours_SCF", 0.0570),
        eth3d_no_state=_write(tmp_path / "en.json", "eth3d", "Ours_SCF", 0.0583),
        eth3d_shuffle=_write(tmp_path / "esh.json", "eth3d", "Ours_SCF", 0.0598),
    )

    assert out["status"] == "blocked"
    assert "kitti_no_state" in out["promotion_blockers"]
    assert not out["promotable_to_official"]


def test_unified_gate_passes_when_all_controls_separate(tmp_path: Path) -> None:
    out = evaluate_unified_domain_conditional_gate(
        kitti_state=_write(tmp_path / "ks.json", "kitti", "Ours_ProposalSetDecoder", 0.1448),
        kitti_no_state=_write(tmp_path / "kn.json", "kitti", "Ours_ProposalSetDecoder", 0.1550),
        kitti_shuffle=_write(tmp_path / "ksh.json", "kitti", "Ours_ProposalSetDecoder", 0.1521),
        eth3d_state=_write(tmp_path / "es.json", "eth3d", "Ours_SCF", 0.0570),
        eth3d_no_state=_write(tmp_path / "en.json", "eth3d", "Ours_SCF", 0.0583),
        eth3d_shuffle=_write(tmp_path / "esh.json", "eth3d", "Ours_SCF", 0.0598),
        output=tmp_path / "gate.json",
    )

    assert out["status"] == "pass"
    assert out["promotion_blockers"] == []
    assert out["promotable_to_official"]
    assert (tmp_path / "gate.json").exists()


def test_unified_gate_reads_flat_local_mirror_for_results_path(tmp_path: Path) -> None:
    cache_root = tmp_path / "cache"
    cache_root.mkdir()
    _write(cache_root / "scf_state_seed7_results.json", "eth3d", "Ours_SCF", 0.0570)

    out = evaluate_unified_domain_conditional_gate(
        kitti_state=_write(tmp_path / "ks.json", "kitti", "Ours_ProposalSetDecoder", 0.1448),
        kitti_no_state=_write(tmp_path / "kn.json", "kitti", "Ours_ProposalSetDecoder", 0.1550),
        kitti_shuffle=_write(tmp_path / "ksh.json", "kitti", "Ours_ProposalSetDecoder", 0.1521),
        eth3d_state=cache_root / "scf_state_seed7" / "results.json",
        eth3d_no_state=_write(tmp_path / "en.json", "eth3d", "Ours_SCF", 0.0583),
        eth3d_shuffle=_write(tmp_path / "esh.json", "eth3d", "Ours_SCF", 0.0598),
    )

    assert out["status"] == "pass"
    assert out["metrics"]["eth3d_state_abs_rel"] == 0.0570
