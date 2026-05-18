"""Deterministic synthetic fixtures for Memory v0.3 P0."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any

import numpy as np

from memory_v03_p0.config import P0Config
from memory_v03_p0.oracle_bus import ORACLE_BUS_TAG


@dataclass(frozen=True)
class FixtureBatch:
    config: P0Config
    frame_tokens: np.ndarray
    evidence_tokens: np.ndarray
    point_tokens: np.ndarray
    group_id: np.ndarray
    is_dynamic: np.ndarray
    is_corrupt: np.ndarray
    expected_loop_id: np.ndarray
    bus: dict[str, dict[str, Any]]
    manifest: dict[str, Any]

    def tensors(self) -> dict[str, np.ndarray]:
        return {
            "frame_tokens": self.frame_tokens,
            "evidence_tokens": self.evidence_tokens,
            "point_tokens": self.point_tokens,
            "group_id": self.group_id,
            "is_dynamic": self.is_dynamic,
            "is_corrupt": self.is_corrupt,
            "expected_loop_id": self.expected_loop_id,
        }


def array_digest(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    header = f"{contiguous.shape}|{contiguous.dtype}".encode("utf-8")
    return sha256(header + contiguous.tobytes()).hexdigest()


def _bus_field(name: str, values: np.ndarray, source: str) -> dict[str, Any]:
    return {
        "tag": ORACLE_BUS_TAG,
        "source": source,
        "shape": list(values.shape),
        "dtype": str(values.dtype),
        "hash": array_digest(values),
        "values": values,
    }


def _compact_bus_manifest(bus: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    compact: dict[str, dict[str, Any]] = {}
    for name, field in bus.items():
        compact[name] = {
            "tag": field["tag"],
            "source": field["source"],
            "shape": field["shape"],
            "dtype": field["dtype"],
            "hash": field["hash"],
        }
    return compact


def generate_fixtures(config: P0Config | None = None) -> FixtureBatch:
    cfg = config or P0Config()
    rng_tokens = np.random.default_rng(cfg.seeds[0])
    rng_noise = np.random.default_rng(cfg.seeds[1])
    rng_flags = np.random.default_rng(cfg.seeds[2])

    b, t, p, e, d, g = (
        cfg.batch_size,
        cfg.frames,
        cfg.patch_tokens,
        cfg.evidence_tokens,
        cfg.token_dim,
        cfg.groups,
    )

    prototypes = rng_tokens.normal(size=(g, d)).astype(np.float32)
    prototypes /= np.linalg.norm(prototypes, axis=1, keepdims=True).clip(min=1e-6)

    patch_groups = (np.arange(p, dtype=np.int32) % g)[None, None, :]
    group_id = np.broadcast_to(patch_groups, (b, t, p)).copy()

    expected_loop_id = np.full((b, t), -1, dtype=np.int32)
    for frame_idx in range(cfg.loop_offset, t):
        expected_loop_id[:, frame_idx] = frame_idx - cfg.loop_offset

    time = np.arange(t, dtype=np.float32)
    paired_time = np.where(time >= cfg.loop_offset, time - cfg.loop_offset, time)
    phase = np.sin((paired_time / max(cfg.loop_offset - 1, 1)) * np.pi).astype(np.float32)
    drift_direction = rng_tokens.normal(size=(d,)).astype(np.float32)
    drift_direction /= np.linalg.norm(drift_direction).clip(min=1e-6)
    drift = (0.08 * phase[:, None] * drift_direction[None, :]).astype(np.float32)

    frame_tokens = prototypes[group_id] + drift[None, :, None, :]
    frame_tokens += rng_noise.normal(scale=0.015, size=(b, t, p, d)).astype(np.float32)

    dynamic_hot_frames = np.isin(np.arange(t), [3, 4, 9, 10])[None, :, None]
    dynamic_probability = np.where(dynamic_hot_frames, 0.42, 0.08)
    is_dynamic = rng_flags.random(size=(b, t, p)) < dynamic_probability

    corrupt_hot_frames = np.isin(np.arange(t), [5, 11])[None, :, None]
    corrupt_probability = np.where(corrupt_hot_frames, 0.38, 0.04)
    is_corrupt = rng_flags.random(size=(b, t, p)) < corrupt_probability

    point_tokens = frame_tokens + rng_noise.normal(scale=0.005, size=(b, t, p, d)).astype(np.float32)

    evidence_tokens = np.empty((b, t, e, d), dtype=np.float32)
    for evidence_idx in range(e):
        mask = group_id == (evidence_idx % g)
        counts = mask.sum(axis=2).clip(min=1)[:, :, None]
        evidence_tokens[:, :, evidence_idx, :] = (frame_tokens * mask[:, :, :, None]).sum(axis=2) / counts

    dynamic_ratio = is_dynamic.mean(axis=2).astype(np.float32)
    conflict_score = is_corrupt.mean(axis=2).astype(np.float32)
    permanence_score = np.clip(1.0 - (0.7 * dynamic_ratio) - (0.2 * conflict_score), 0.0, 1.0).astype(np.float32)
    expected_future_use = (np.arange(t)[None, :] < cfg.loop_offset).astype(np.float32)
    expected_future_use = np.broadcast_to(expected_future_use, (b, t)).copy()
    reset_mask = ((conflict_score > 0.35) | (np.arange(t)[None, :] == 0)).astype(np.int32)

    bus = {
        "dynamic_ratio": _bus_field("dynamic_ratio", dynamic_ratio, "fixture_metadata"),
        "conflict_score": _bus_field("conflict_score", conflict_score, "fixture_metadata"),
        "permanence_score": _bus_field("permanence_score", permanence_score, "fixture_metadata"),
        "expected_future_use": _bus_field("expected_future_use", expected_future_use, "fixture_metadata"),
        "reset_mask": _bus_field("reset_mask", reset_mask, "fixture_metadata"),
    }

    hashes = {name: array_digest(value) for name, value in {
        "frame_tokens": frame_tokens,
        "evidence_tokens": evidence_tokens,
        "point_tokens": point_tokens,
    }.items()}
    label_hashes = {name: array_digest(value) for name, value in {
        "group_id": group_id,
        "is_dynamic": is_dynamic,
        "is_corrupt": is_corrupt,
        "expected_loop_id": expected_loop_id,
    }.items()}

    manifest = {
        "prototype": "memory_v03_p0",
        "cycle": "031",
        "abl_gate": "ABL-memory-0",
        "config": cfg.to_dict(),
        "expected_shapes": cfg.expected_shapes(),
        "tensor_hashes": hashes,
        "raw_label_hashes": label_hashes,
        "oracle_bus": _compact_bus_manifest(bus),
        "raw_label_policy": {
            "construction_and_audit_only": [
                "group_id",
                "is_dynamic",
                "is_corrupt",
                "expected_loop_id",
            ],
            "forbidden_as_variant_inputs": True,
        },
    }

    return FixtureBatch(
        config=cfg,
        frame_tokens=frame_tokens,
        evidence_tokens=evidence_tokens,
        point_tokens=point_tokens,
        group_id=group_id,
        is_dynamic=is_dynamic,
        is_corrupt=is_corrupt,
        expected_loop_id=expected_loop_id,
        bus=bus,
        manifest=manifest,
    )
