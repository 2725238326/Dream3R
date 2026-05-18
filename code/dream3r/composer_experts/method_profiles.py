"""Structured 3R method profiles used by Composer routing."""

from dataclasses import dataclass
from typing import Dict, List

import torch


REGIME_ORDER = [
    "indoor_static",
    "outdoor_static",
    "dynamic_scene",
    "sparse_view",
    "dense_sequential",
]

FEATURE_ORDER = [
    "pairwise_matching",
    "large_scale_context",
    "streaming_state",
    "spatial_memory",
    "monocular_metric_geometry",
    "monocular_relative_depth",
    "test_time_refinement",
    "low_latency",
    "dynamic_robustness",
    "sparse_view_robustness",
]


@dataclass(frozen=True)
class MethodProfile:
    name: str
    family: str
    implementation_status: str
    advantages: List[str]
    limitations: List[str]
    feature_scores: Dict[str, float]
    regime_scores: Dict[str, float]
    source_urls: List[str]

    def regime_tensor(self, regime_order: List[str] = None) -> torch.Tensor:
        order = regime_order or REGIME_ORDER
        return torch.tensor([self.regime_scores.get(key, 0.0) for key in order])

    def feature_tensor(self, feature_order: List[str] = None) -> torch.Tensor:
        order = feature_order or FEATURE_ORDER
        return torch.tensor([self.feature_scores.get(key, 0.0) for key in order])


METHOD_PROFILES: Dict[str, MethodProfile] = {
    "mast3r": MethodProfile(
        name="mast3r",
        family="3D-grounded image matching",
        implementation_status="checkpoint_available",
        advantages=[
            "dense 3D-grounded local matching",
            "strong static-scene pairwise geometry",
            "fast reciprocal matching path for image pairs",
        ],
        limitations=[
            "pair-centric unless wrapped by a global mapper",
            "less suited to persistent streaming state by itself",
        ],
        feature_scores={
            "pairwise_matching": 0.95,
            "sparse_view_robustness": 0.75,
            "low_latency": 0.45,
            "dynamic_robustness": 0.25,
        },
        regime_scores={
            "indoor_static": 0.92,
            "outdoor_static": 0.86,
            "dynamic_scene": 0.30,
            "sparse_view": 0.72,
            "dense_sequential": 0.55,
        },
        source_urls=["https://arxiv.org/abs/2406.09756"],
    ),
    "fast3r": MethodProfile(
        name="fast3r",
        family="large-scale feed-forward 3D reconstruction",
        implementation_status="checkpoint_available",
        advantages=[
            "many-image reconstruction in one forward pass",
            "reduced sequential error accumulation",
            "strong latency profile for large image sets",
        ],
        limitations=[
            "less specialized for pairwise precision matching",
            "requires batching many views to expose its main advantage",
        ],
        feature_scores={
            "large_scale_context": 0.95,
            "low_latency": 0.85,
            "dense_sequential": 0.85,
            "pairwise_matching": 0.45,
        },
        regime_scores={
            "indoor_static": 0.72,
            "outdoor_static": 0.76,
            "dynamic_scene": 0.45,
            "sparse_view": 0.58,
            "dense_sequential": 0.88,
        },
        source_urls=["https://arxiv.org/abs/2501.13928"],
    ),
    "spann3r": MethodProfile(
        name="spann3r",
        family="spatial-memory 3D reconstruction",
        implementation_status="checkpoint_available",
        advantages=[
            "external spatial memory for image collections",
            "ordered or unordered dense reconstruction",
            "natural conceptual match for Dream3R AnchorBank",
        ],
        limitations=[
            "memory quality depends on retrieval policy",
            "does not directly solve expert cost routing",
        ],
        feature_scores={
            "spatial_memory": 0.95,
            "large_scale_context": 0.70,
            "dense_sequential": 0.82,
            "sparse_view_robustness": 0.62,
        },
        regime_scores={
            "indoor_static": 0.78,
            "outdoor_static": 0.78,
            "dynamic_scene": 0.50,
            "sparse_view": 0.65,
            "dense_sequential": 0.92,
        },
        source_urls=["https://arxiv.org/abs/2408.16061"],
    ),
    "cut3r": MethodProfile(
        name="cut3r",
        family="continuous stateful 3D reconstruction",
        implementation_status="stub",
        advantages=[
            "persistent state for continuous perception",
            "streaming-friendly pointmap updates",
            "can infer unseen regions from virtual probes",
        ],
        limitations=[
            "state drift needs explicit critic or memory control",
            "quality depends on recurrence stability",
        ],
        feature_scores={
            "streaming_state": 0.95,
            "dynamic_robustness": 0.70,
            "large_scale_context": 0.70,
            "low_latency": 0.55,
        },
        regime_scores={
            "indoor_static": 0.76,
            "outdoor_static": 0.76,
            "dynamic_scene": 0.78,
            "sparse_view": 0.60,
            "dense_sequential": 0.86,
        },
        source_urls=["https://arxiv.org/abs/2501.12387"],
    ),
    "moge2": MethodProfile(
        name="moge2",
        family="monocular metric geometry",
        implementation_status="stub",
        advantages=[
            "single-image metric pointmap prior",
            "sharp open-domain geometry",
            "useful fallback when multiview overlap is weak",
        ],
        limitations=[
            "monocular estimates need multiview consistency checks",
            "temporal identity is not its native objective",
        ],
        feature_scores={
            "monocular_metric_geometry": 0.95,
            "sparse_view_robustness": 0.85,
            "low_latency": 0.60,
            "pairwise_matching": 0.10,
        },
        regime_scores={
            "indoor_static": 0.70,
            "outdoor_static": 0.72,
            "dynamic_scene": 0.48,
            "sparse_view": 0.92,
            "dense_sequential": 0.52,
        },
        source_urls=["https://arxiv.org/abs/2507.02546"],
    ),
    "depthanything": MethodProfile(
        name="depthanything",
        family="monocular relative depth foundation model",
        implementation_status="stub",
        advantages=[
            "robust monocular depth prior",
            "very low latency relative to 3R backbones",
            "good regularizer for weak geometry regions",
        ],
        limitations=[
            "relative depth is not full multiview reconstruction",
            "raw per-frame depth can flicker without temporal filtering",
        ],
        feature_scores={
            "monocular_relative_depth": 0.95,
            "low_latency": 0.95,
            "sparse_view_robustness": 0.72,
            "pairwise_matching": 0.05,
        },
        regime_scores={
            "indoor_static": 0.62,
            "outdoor_static": 0.66,
            "dynamic_scene": 0.55,
            "sparse_view": 0.82,
            "dense_sequential": 0.45,
        },
        source_urls=["https://arxiv.org/abs/2406.09414"],
    ),
    "test3r": MethodProfile(
        name="test3r",
        family="test-time 3D reconstruction refinement",
        implementation_status="stub",
        advantages=[
            "test-time self-supervised consistency refinement",
            "strong verification expert for ambiguous geometry",
            "fits critic-triggered off-path repair",
        ],
        limitations=[
            "high latency",
            "best used selectively rather than every frame",
        ],
        feature_scores={
            "test_time_refinement": 0.95,
            "dynamic_robustness": 0.60,
            "low_latency": 0.05,
            "sparse_view_robustness": 0.65,
        },
        regime_scores={
            "indoor_static": 0.65,
            "outdoor_static": 0.66,
            "dynamic_scene": 0.62,
            "sparse_view": 0.70,
            "dense_sequential": 0.58,
        },
        source_urls=["https://arxiv.org/abs/2506.13750"],
    ),
}


def get_method_profile(name: str) -> MethodProfile:
    return METHOD_PROFILES[name]
