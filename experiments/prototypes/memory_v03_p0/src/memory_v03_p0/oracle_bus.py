"""Oracle-bus contract for P0 synthetic fixtures."""

from __future__ import annotations

from collections.abc import Mapping


ORACLE_BUS_TAG = "oracle_bus"

ORACLE_BUS_FIELDS = (
    "dynamic_ratio",
    "conflict_score",
    "permanence_score",
    "expected_future_use",
    "reset_mask",
)

FORBIDDEN_VARIANT_INPUTS = (
    "group_id",
    "is_dynamic",
    "is_corrupt",
    "expected_loop_id",
    "future_use_label",
)


def allowed_variant_inputs() -> tuple[str, ...]:
    return (
        "frame_tokens",
        "evidence_tokens",
        "point_tokens",
        *(f"bus.{field}" for field in ORACLE_BUS_FIELDS),
    )


def validate_oracle_bus_tags(bus: Mapping[str, Mapping[str, object]]) -> list[str]:
    errors: list[str] = []
    missing = sorted(set(ORACLE_BUS_FIELDS) - set(bus.keys()))
    extra = sorted(set(bus.keys()) - set(ORACLE_BUS_FIELDS))
    if missing:
        errors.append(f"missing oracle-bus fields: {missing}")
    if extra:
        errors.append(f"unexpected oracle-bus fields: {extra}")

    for name in ORACLE_BUS_FIELDS:
        if name not in bus:
            continue
        field = bus[name]
        if field.get("tag") != ORACLE_BUS_TAG:
            errors.append(f"{name} has tag {field.get('tag')!r}, expected {ORACLE_BUS_TAG!r}")
        if "values" not in field:
            errors.append(f"{name} has no values")
    return errors


def audit_variant_input_boundary(inputs: tuple[str, ...] | list[str]) -> dict[str, object]:
    input_set = set(inputs)
    forbidden_present = sorted(input_set.intersection(FORBIDDEN_VARIANT_INPUTS))
    missing_allowed = sorted(set(allowed_variant_inputs()) - input_set)
    return {
        "allowed_inputs": list(allowed_variant_inputs()),
        "actual_inputs": list(inputs),
        "forbidden_inputs": list(FORBIDDEN_VARIANT_INPUTS),
        "forbidden_present": forbidden_present,
        "missing_allowed": missing_allowed,
        "passed": not forbidden_present and not missing_allowed,
    }
