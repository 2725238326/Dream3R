"""Configuration for the Memory v0.3 P0 local fixture substrate."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class P0Config:
    """Default tensor sizes from the Memory v0.3 P0 prototype plan."""

    batch_size: int = 2
    frames: int = 12
    patch_tokens: int = 64
    evidence_tokens: int = 8
    token_dim: int = 128
    state_tokens: int = 32
    memory_max: int = 256
    window: int = 4
    retrieval_k: int = 8
    groups: int = 4
    seeds: tuple[int, int, int] = (20260508, 20260509, 20260510)

    @property
    def loop_offset(self) -> int:
        return self.frames // 2

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["seeds"] = list(self.seeds)
        data["loop_offset"] = self.loop_offset
        return data

    def expected_shapes(self) -> dict[str, list[int]]:
        b = self.batch_size
        t = self.frames
        p = self.patch_tokens
        e = self.evidence_tokens
        d = self.token_dim
        return {
            "frame_tokens": [b, t, p, d],
            "evidence_tokens": [b, t, e, d],
            "point_tokens": [b, t, p, d],
            "group_id": [b, t, p],
            "is_dynamic": [b, t, p],
            "is_corrupt": [b, t, p],
            "expected_loop_id": [b, t],
            "bus.dynamic_ratio": [b, t],
            "bus.conflict_score": [b, t],
            "bus.permanence_score": [b, t],
            "bus.expected_future_use": [b, t],
            "bus.reset_mask": [b, t],
        }
