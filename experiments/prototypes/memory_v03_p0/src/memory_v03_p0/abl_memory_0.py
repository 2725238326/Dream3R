"""ABL-memory-0 fixture and logging validity gate."""

from __future__ import annotations

from pathlib import Path
import csv

from memory_v03_p0.config import P0Config
from memory_v03_p0.fixtures import FixtureBatch, generate_fixtures
from memory_v03_p0.io_utils import ensure_dir, write_json, write_jsonl
from memory_v03_p0.oracle_bus import (
    audit_variant_input_boundary,
    allowed_variant_inputs,
    validate_oracle_bus_tags,
)


def _shape_checks(batch: FixtureBatch) -> list[dict[str, object]]:
    expected = batch.config.expected_shapes()
    actual = {name: list(value.shape) for name, value in batch.tensors().items()}
    actual.update({f"bus.{name}": list(field["values"].shape) for name, field in batch.bus.items()})

    rows: list[dict[str, object]] = []
    for name, expected_shape in expected.items():
        actual_shape = actual.get(name)
        rows.append({
            "check": f"shape:{name}",
            "passed": actual_shape == expected_shape,
            "detail": {"expected": expected_shape, "actual": actual_shape},
        })
    return rows


def _reproducibility_checks(left: FixtureBatch, right: FixtureBatch) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for name in ("group_id", "is_dynamic", "is_corrupt", "expected_loop_id"):
        left_hash = left.manifest["raw_label_hashes"][name]
        right_hash = right.manifest["raw_label_hashes"][name]
        rows.append({
            "check": f"reproducible_label:{name}",
            "passed": left_hash == right_hash,
            "detail": {"left": left_hash, "right": right_hash},
        })
    for name in ("frame_tokens", "evidence_tokens", "point_tokens"):
        left_hash = left.manifest["tensor_hashes"][name]
        right_hash = right.manifest["tensor_hashes"][name]
        rows.append({
            "check": f"reproducible_tensor:{name}",
            "passed": left_hash == right_hash,
            "detail": {"left": left_hash, "right": right_hash},
        })
    return rows


def run_abl_memory_0(output_dir: Path | str, config: P0Config | None = None) -> dict[str, object]:
    output_path = ensure_dir(Path(output_dir))
    cfg = config or P0Config()
    batch = generate_fixtures(cfg)
    repeated = generate_fixtures(cfg)

    checks: list[dict[str, object]] = []
    checks.extend(_shape_checks(batch))
    checks.extend(_reproducibility_checks(batch, repeated))

    bus_errors = validate_oracle_bus_tags(batch.bus)
    checks.append({
        "check": "oracle_bus_tags",
        "passed": not bus_errors,
        "detail": {"errors": bus_errors},
    })

    input_audit = audit_variant_input_boundary(allowed_variant_inputs())
    checks.append({
        "check": "raw_label_exclusion",
        "passed": bool(input_audit["passed"]),
        "detail": input_audit,
    })

    checks.append({
        "check": "output_serialization_plan",
        "passed": True,
        "detail": {
            "required_outputs": [
                "fixtures_manifest.json",
                "write_log.jsonl",
                "metrics_abl_memory_0_8.csv",
                "summary_go_no_go.md",
                "evidence_boundary_update.md",
            ]
        },
    })

    passed = all(bool(row["passed"]) for row in checks)
    status = "pass" if passed else "fail"

    manifest = dict(batch.manifest)
    manifest["variant_input_audit"] = input_audit
    manifest["abl_memory_0_status"] = status

    write_json(output_path / "fixtures_manifest.json", manifest)

    log_rows = [
        {
            "abl_id": "ABL-memory-0",
            "event": "check",
            "check": row["check"],
            "passed": row["passed"],
            "detail": row["detail"],
        }
        for row in checks
    ]
    write_jsonl(output_path / "write_log.jsonl", log_rows)

    metric_path = output_path / "metrics_abl_memory_0_8.csv"
    with metric_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["abl_id", "status", "admissible", "metric_name", "metric_value", "notes"],
        )
        writer.writeheader()
        writer.writerow({
            "abl_id": "ABL-memory-0",
            "status": status,
            "admissible": str(passed).lower(),
            "metric_name": "validity_checks_passed",
            "metric_value": f"{sum(bool(row['passed']) for row in checks)}/{len(checks)}",
            "notes": "fixture/logging validity gate only",
        })
        for idx in range(1, 9):
            writer.writerow({
                "abl_id": f"ABL-memory-{idx}",
                "status": "not_run_scope_deferred",
                "admissible": "false",
                "metric_name": "not_applicable",
                "metric_value": "",
                "notes": "reserved for later cycles; no implementation or claim in cycle 031",
            })

    summary = _summary_markdown(status, checks)
    (output_path / "summary_go_no_go.md").write_text(summary, encoding="utf-8")

    evidence = _evidence_boundary_markdown(status)
    (output_path / "evidence_boundary_update.md").write_text(evidence, encoding="utf-8")

    return {
        "abl_id": "ABL-memory-0",
        "status": status,
        "passed": passed,
        "checks": checks,
        "output_dir": str(output_path),
    }


def _summary_markdown(status: str, checks: list[dict[str, object]]) -> str:
    lines = [
        "# ABL-memory-0 go/no-go summary",
        "",
        f"Status: {status}",
        "",
        "| Check | Passed |",
        "| --- | --- |",
    ]
    for row in checks:
        lines.append(f"| `{row['check']}` | {str(row['passed']).lower()} |")
    lines.extend([
        "",
        "Interpretation:",
        "",
        "- `pass` means the local P0 fixture/logging substrate is admissible for later ablation work.",
        "- It does not validate Memory v0.3 retrieval, recurrence, reconstruction, training, or paper claims.",
        "",
    ])
    return "\n".join(lines)


def _evidence_boundary_markdown(status: str) -> str:
    return "\n".join([
        "# Evidence boundary update",
        "",
        f"Cycle 031 `ABL-memory-0` status: {status}",
        "",
        "Locally demonstrated if status is `pass`:",
        "",
        "- deterministic P0 fixture generation",
        "- expected tensor shape contract",
        "- oracle-bus field tagging",
        "- raw fixture label exclusion from variant inputs",
        "- JSON, JSONL, CSV, and Markdown output serialization",
        "",
        "Still not demonstrated:",
        "",
        "- `ABL-memory-1..8` behavior",
        "- spatial retrieval quality",
        "- state-token recurrence quality",
        "- hybrid memory policy benefit",
        "- reconstruction quality",
        "- checkpoint or real model behavior",
        "- server integration",
        "- paper-level empirical evidence",
        "",
    ])
