"""
Dream3R expert adapter registry and factory.

Usage:
    from dream3r.composer_experts import ExpertRegistry, get_all_adapters
    registry = ExpertRegistry()
    registry.register_all_defaults()
    adapter = registry.get("mast3r")
"""

from typing import Dict, List, Optional, Type
import torch

from .base_adapter import ExpertAdapter, ExpertOutput
from .method_profiles import FEATURE_ORDER, METHOD_PROFILES, MethodProfile


class ExpertRegistry:
    """Central registry for expert adapters."""

    def __init__(self):
        self._adapters: Dict[str, ExpertAdapter] = {}
        self._classes: Dict[str, Type[ExpertAdapter]] = {}

    def register_class(self, name: str, cls: Type[ExpertAdapter]):
        self._classes[name] = cls

    def instantiate(self, name: str, **kwargs) -> ExpertAdapter:
        if name not in self._classes:
            raise KeyError(f"Unknown expert: {name}. Available: {list(self._classes.keys())}")
        adapter = self._classes[name](**kwargs)
        self._adapters[name] = adapter
        return adapter

    def get(self, name: str) -> ExpertAdapter:
        if name not in self._adapters:
            return self.instantiate(name)
        return self._adapters[name]

    def register_all_defaults(self):
        from .mast3r_adapter import MASt3RAdapter
        from .fast3r_adapter import Fast3RAdapter
        from .spann3r_adapter import Spann3RAdapter
        from .cut3r_adapter import CUT3RAdapter
        from .moge2_adapter import MoGe2Adapter
        from .depthanything_adapter import DepthAnythingAdapter
        from .test3r_adapter import Test3RAdapter

        for cls in [MASt3RAdapter, Fast3RAdapter, Spann3RAdapter,
                    CUT3RAdapter, MoGe2Adapter, DepthAnythingAdapter,
                    Test3RAdapter]:
            self.register_class(cls.name, cls)

    @property
    def names(self) -> List[str]:
        return list(self._classes.keys())

    def capability_matrix(self, regime_order: Optional[list] = None) -> torch.Tensor:
        order = regime_order or ExpertAdapter.REGIMES
        rows = []
        for name in sorted(self._classes.keys()):
            profile = METHOD_PROFILES.get(name)
            if profile is not None:
                rows.append(profile.regime_tensor(order))
            else:
                adapter = self.get(name)
                rows.append(adapter.capability_tensor(order))
        return torch.stack(rows)

    def method_profile(self, name: str) -> MethodProfile:
        if name not in METHOD_PROFILES:
            raise KeyError(f"No method profile for expert: {name}")
        return METHOD_PROFILES[name]

    def method_profiles(self) -> Dict[str, MethodProfile]:
        return {
            name: METHOD_PROFILES[name]
            for name in sorted(self._classes.keys())
            if name in METHOD_PROFILES
        }

    def feature_matrix(self, feature_order: Optional[list] = None) -> torch.Tensor:
        order = feature_order or FEATURE_ORDER
        rows = []
        for name in sorted(self._classes.keys()):
            profile = METHOD_PROFILES.get(name)
            if profile is None:
                rows.append(torch.zeros(len(order)))
            else:
                rows.append(profile.feature_tensor(order))
        return torch.stack(rows)

    def advantage_summary(self) -> Dict[str, List[str]]:
        return {
            name: profile.advantages
            for name, profile in self.method_profiles().items()
        }

    def adapter_status(self) -> Dict[str, Dict[str, object]]:
        status = {}
        for name in sorted(self._classes.keys()):
            adapter = self.get(name)
            is_available = (
                adapter.is_available()
                if hasattr(adapter, "is_available")
                else False
            )
            status[name] = {
                "is_loaded": bool(adapter.is_loaded),
                "is_available": bool(is_available),
                "has_checkpoint_artifacts": bool(
                    adapter.has_checkpoint_artifacts()
                    if hasattr(adapter, "has_checkpoint_artifacts")
                    else is_available
                ),
                "load_error": getattr(adapter, "load_error", None),
                "backend": "real" if adapter.is_loaded else "fallback",
                "attention_regime": adapter.attention_regime,
                "latency_estimate_ms": adapter.latency_estimate_ms,
            }
        return status

    def latency_vector(self) -> torch.Tensor:
        return torch.tensor([
            self.get(n).latency_estimate_ms
            for n in sorted(self._classes.keys())
        ])


def get_all_adapters() -> ExpertRegistry:
    reg = ExpertRegistry()
    reg.register_all_defaults()
    return reg
