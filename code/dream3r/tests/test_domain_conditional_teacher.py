from __future__ import annotations

import json
from pathlib import Path

from dream3r.scripts.eval_domain_conditional_teacher import evaluate_domain_conditional


def _write_result(path: Path, kitti: float, eth3d: float, key: str) -> Path:
    path.write_text(
        json.dumps(
            {
                "final_eval": {
                    "kitti": {key: kitti},
                    "eth3d": {key: eth3d},
                }
            }
        ),
        encoding="utf-8",
    )
    return path


def test_domain_conditional_teacher_reports_domain_controls(tmp_path: Path) -> None:
    bounded_state = _write_result(tmp_path / "bounded_state.json", 0.1448, 0.1475, "Ours_ProposalSetDecoder")
    bounded_shuffle = _write_result(tmp_path / "bounded_shuffle.json", 0.1521, 0.2467, "Ours_ProposalSetDecoder")
    vggt_state = _write_result(tmp_path / "vggt_state.json", 0.2296, 0.0570, "Ours_SCF")
    vggt_no_state = _write_result(tmp_path / "vggt_no_state.json", 0.1966, 0.0583, "Ours_SCF")
    vggt_shuffle = _write_result(tmp_path / "vggt_shuffle.json", 0.2180, 0.0598, "Ours_SCF")

    out = evaluate_domain_conditional(
        bounded_state,
        bounded_shuffle,
        vggt_state,
        vggt_no_state,
        vggt_shuffle,
        output=tmp_path / "candidate.json",
    )

    assert out["metrics"]["kitti_abs_rel"] == 0.1448
    assert out["metrics"]["eth3d_abs_rel"] == 0.057
    assert out["metrics"]["eth3d_relative_gain_vs_rc_pct"] == 61.36
    assert out["controls"]["kitti_bounded_state_beats_shuffle"]
    assert out["controls"]["eth3d_vggt_state_beats_no_state"]
    assert out["controls"]["eth3d_vggt_state_beats_shuffle"]
    assert out["passes_domainwise_controls"]
    assert not out["promotable_to_official"]
    assert (tmp_path / "candidate.json").exists()
