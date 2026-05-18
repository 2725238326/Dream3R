"""Shared contracts reserved for later P0 ablation implementations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VariantContract:
    abl_id: str
    implemented: bool
    claim_boundary: str


RESERVED_CONTRACTS: tuple[VariantContract, ...] = tuple(
    VariantContract(
        abl_id=f"ABL-memory-{idx}",
        implemented=False,
        claim_boundary="reserved; not implemented or claimed in cycle 031",
    )
    for idx in range(1, 9)
)
