import sys
import os

DREAM3R_EXPERTS = "/hdd3/kykt26/code/dream3r/dream3r/composer_experts"

# MASt3R adapter
mast3r = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

MAST3R_REPO = "/hdd3/kykt26/code/mast3r"
MAST3R_DUST3R = "/hdd3/kykt26/code/mast3r/dust3r"
MAST3R_CKPT = "/hdd3/kykt26/code/mast3r/checkpoints/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth"


class MASt3RAdapter(ExpertAdapter):
    expert_id = "mast3r"
    attention_regime = "full"
    is_streaming_path = True
    checkpoint_source = "naver/mast3r"
    license = "CC-BY-NC-SA-4.0"

    def __init__(self):
        self._model = None

    def _ensure_path(self):
        for p in [MAST3R_REPO, MAST3R_DUST3R]:
            if p not in sys.path:
                sys.path.insert(0, p)

    def _load_model(self, device="cpu"):
        if self._model is not None:
            return
        if not os.path.exists(MAST3R_CKPT):
            raise CheckpointNotFoundError(self.expert_id, MAST3R_CKPT)
        self._ensure_path()
        from mast3r.model import load_model
        self._model = load_model(MAST3R_CKPT, device, verbose=False)
        self._model.eval()
        for p in self._model.parameters():
            p.requires_grad = False

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        self._load_model(device)
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1

        if frames.dim() == 5 and N >= 2:
            img1 = frames[:, 0]
            img2 = frames[:, 1]
        else:
            img1 = frames[:, 0] if frames.dim() == 5 else frames
            img2 = img1

        H, W = img1.shape[-2], img1.shape[-1]
        shape = torch.tensor([[H, W]], device=device).expand(B, -1)
        view1 = {"img": img1, "true_shape": shape, "idx": torch.zeros(B, dtype=torch.long, device=device), "instance": ["0"] * B}
        view2 = {"img": img2, "true_shape": shape, "idx": torch.ones(B, dtype=torch.long, device=device), "instance": ["1"] * B}

        t0 = time.perf_counter()
        with torch.no_grad():
            pred1, pred2 = self._model(view1, view2)
        torch.cuda.synchronize()
        latency = (time.perf_counter() - t0) * 1000

        pts = pred1["pts3d"]
        conf = pred1["conf"].unsqueeze(-1) if "conf" in pred1 else torch.ones(*pts.shape[:-1], 1, device=device)

        return {
            "pointmap": pts.unsqueeze(1),
            "depth": None,
            "confidence": conf.unsqueeze(1),
            "expert_id": self.expert_id,
            "latency_ms": latency,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.85, "multi_view_scale": 0.7, "streaming": 0.5, "mono": 0.3, "dynamic": 0.6, "long_context": 0.5}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 80.0, "vram_mb": 600.0, "params_m": 688.6}

    def is_available(self) -> bool:
        return os.path.exists(MAST3R_CKPT)
'''

# Spann3R adapter
spann3r = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

SPANN3R_REPO = "/hdd3/kykt26/code/spann3r"
SPANN3R_CKPT = "/hdd3/kykt26/code/spann3r/checkpoints/spann3r.pth"


class Spann3RAdapter(ExpertAdapter):
    expert_id = "spann3r"
    attention_regime = "full"
    is_streaming_path = True
    checkpoint_source = "hengyiwang/spann3r"
    license = "MIT"

    def __init__(self):
        self._model = None

    def _load_model(self, device="cpu"):
        if self._model is not None:
            return
        if not os.path.exists(SPANN3R_CKPT):
            raise CheckpointNotFoundError(self.expert_id, SPANN3R_CKPT)
        if SPANN3R_REPO not in sys.path:
            sys.path.insert(0, SPANN3R_REPO)
        dust3r_path = os.path.join(SPANN3R_REPO, "dust3r")
        if dust3r_path not in sys.path:
            sys.path.insert(0, dust3r_path)
        croco_path = os.path.join(SPANN3R_REPO, "dust3r", "croco")
        if croco_path not in sys.path:
            sys.path.insert(0, croco_path)
        from spann3r.model import Spann3R
        self._model = Spann3R.from_pretrained(SPANN3R_CKPT)
        self._model.to(device).eval()
        for p in self._model.parameters():
            p.requires_grad = False

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1
        H, W = frames.shape[-2], frames.shape[-1]

        # Stub forward for now - Spann3R needs special streaming input format
        return {
            "pointmap": torch.zeros(B, N, H // 16, W // 16, 3, device=device),
            "depth": None,
            "confidence": torch.ones(B, N, H // 16, W // 16, 1, device=device) * 0.5,
            "expert_id": self.expert_id,
            "latency_ms": 0.0,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.6, "multi_view_scale": 0.55, "streaming": 0.85, "mono": 0.3, "dynamic": 0.4, "long_context": 0.8}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 60.0, "vram_mb": 500.0, "params_m": 250.0}

    def is_available(self) -> bool:
        return os.path.exists(SPANN3R_CKPT)
'''

# CUT3R adapter
cut3r = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

CUT3R_REPO = "/hdd3/kykt26/code/cut3r"
CUT3R_CKPT = "/hdd3/kykt26/code/cut3r/src/cut3r_512_dpt_4_64.pth"


class CUT3RAdapter(ExpertAdapter):
    expert_id = "cut3r"
    attention_regime = "full"
    is_streaming_path = True
    checkpoint_source = "CUT3R-official"
    license = "Apache-2.0"

    def __init__(self):
        self._model = None

    def _load_model(self, device="cpu"):
        if self._model is not None:
            return
        if not os.path.exists(CUT3R_CKPT):
            raise CheckpointNotFoundError(self.expert_id, CUT3R_CKPT)
        # CUT3R loading is complex; stub for now
        self._model = "loaded"

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1
        H, W = frames.shape[-2], frames.shape[-1]

        return {
            "pointmap": torch.zeros(B, N, H // 16, W // 16, 3, device=device),
            "depth": None,
            "confidence": torch.ones(B, N, H // 16, W // 16, 1, device=device) * 0.5,
            "expert_id": self.expert_id,
            "latency_ms": 0.0,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.7, "multi_view_scale": 0.55, "streaming": 0.9, "mono": 0.4, "dynamic": 0.4, "long_context": 0.8}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 50.0, "vram_mb": 600.0, "params_m": 300.0}

    def is_available(self) -> bool:
        return os.path.exists(CUT3R_CKPT)
'''

# Fast3R adapter
fast3r = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

FAST3R_REPO = "/hdd3/kykt26/code/fast3r"
FAST3R_CKPT_DIR = "/hdd3/kykt26/models/fast3r/Fast3R_ViT_Large_512"


class Fast3RAdapter(ExpertAdapter):
    expert_id = "fast3r"
    attention_regime = "full"
    is_streaming_path = True
    checkpoint_source = "fast3r-official"
    license = "Apache-2.0"

    def __init__(self):
        self._model = None

    def _load_model(self, device="cpu"):
        if self._model is not None:
            return
        ckpt_file = os.path.join(FAST3R_CKPT_DIR, "model.safetensors")
        if not os.path.exists(ckpt_file):
            raise CheckpointNotFoundError(self.expert_id, ckpt_file)
        # Fast3R loading needs its own import path; stub for now
        self._model = "loaded"

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1
        H, W = frames.shape[-2], frames.shape[-1]

        return {
            "pointmap": torch.zeros(B, N, H // 16, W // 16, 3, device=device),
            "depth": None,
            "confidence": torch.ones(B, N, H // 16, W // 16, 1, device=device) * 0.5,
            "expert_id": self.expert_id,
            "latency_ms": 0.0,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.8, "multi_view_scale": 0.9, "streaming": 0.3, "mono": 0.4, "dynamic": 0.3, "long_context": 0.5}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 100.0, "vram_mb": 1200.0, "params_m": 580.0}

    def is_available(self) -> bool:
        return os.path.exists(os.path.join(FAST3R_CKPT_DIR, "model.safetensors"))
'''

# Test3R adapter (no checkpoint yet)
test3r = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

TEST3R_REPO = "/hdd3/kykt26/code/Test3R"
TEST3R_CKPT = "/hdd3/kykt26/models/test3r/test3r.pth"


class Test3RAdapter(ExpertAdapter):
    expert_id = "test3r"
    attention_regime = "full"
    is_streaming_path = False  # OFF streaming path; lazy invocation only
    checkpoint_source = "test3r-official"
    license = "Apache-2.0"

    def __init__(self):
        self._model = None

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1
        H, W = frames.shape[-2], frames.shape[-1]

        return {
            "pointmap": torch.zeros(B, N, H // 16, W // 16, 3, device=device),
            "depth": None,
            "confidence": torch.ones(B, N, H // 16, W // 16, 1, device=device) * 0.5,
            "expert_id": self.expert_id,
            "latency_ms": 0.0,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.7, "multi_view_scale": 0.5, "streaming": 0.3, "mono": 0.3, "dynamic": 0.3, "long_context": 0.5}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 200.0, "vram_mb": 800.0, "params_m": 300.0}

    def is_available(self) -> bool:
        return os.path.exists(TEST3R_CKPT) or os.path.exists(TEST3R_REPO)
'''

# MoGe-2 adapter (no checkpoint yet)
moge2 = '''import sys
import os
import torch
import time
from typing import Dict, Any
from .base import ExpertAdapter, CheckpointNotFoundError

MOGE2_CKPT = "/hdd3/kykt26/models/moge2/moge2.pth"


class MoGe2Adapter(ExpertAdapter):
    expert_id = "moge2"
    attention_regime = "full"
    is_streaming_path = True
    checkpoint_source = "microsoft/MoGe"
    license = "MIT"

    def __init__(self):
        self._model = None

    def forward(self, frames: torch.Tensor, bus_signals: Dict[str, Any], **kwargs) -> Dict[str, torch.Tensor]:
        device = frames.device
        B = frames.shape[0]
        N = frames.shape[1] if frames.dim() == 5 else 1
        H, W = frames.shape[-2], frames.shape[-1]

        return {
            "pointmap": torch.zeros(B, N, H // 16, W // 16, 3, device=device),
            "depth": None,
            "confidence": torch.ones(B, N, H // 16, W // 16, 1, device=device) * 0.5,
            "expert_id": self.expert_id,
            "latency_ms": 0.0,
        }

    def get_capability_match(self) -> Dict[str, float]:
        return {"pair_quality": 0.3, "multi_view_scale": 0.2, "streaming": 0.4, "mono": 0.95, "dynamic": 0.5, "long_context": 0.2}

    def get_latency_estimate(self) -> Dict[str, float]:
        return {"forward_ms": 75.0, "vram_mb": 400.0, "params_m": 200.0}

    def is_available(self) -> bool:
        return os.path.exists(MOGE2_CKPT)
'''

adapters = {
    "mast3r_adapter.py": mast3r,
    "spann3r_adapter.py": spann3r,
    "cut3r_adapter.py": cut3r,
    "fast3r_adapter.py": fast3r,
    "test3r_adapter.py": test3r,
    "moge2_adapter.py": moge2,
}

for fname, content in adapters.items():
    path = os.path.join(sys.argv[1], fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"  {fname}: {len(content.splitlines())} lines")

print("ALL 6 ADAPTERS WRITTEN")
