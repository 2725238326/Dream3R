"""Tests for the Stage 1 DINOv3-B ONNX backbone path."""

import numpy as np
import pytest
import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.model import CONFIGS, Dream3R
from dream3r.modules import Perceiver


class FakeONNXInput:
    name = "pixel_values"


class FakeONNXSession:
    def __init__(self, *args, **kwargs):
        pass

    def get_inputs(self):
        return [FakeONNXInput()]

    def run(self, *_args):
        pixel_values = _args[1]["pixel_values"]
        batch = pixel_values.shape[0]
        tokens = np.ones((batch, 201, 768), dtype=np.float32)
        pooled = np.ones((batch, 768), dtype=np.float32)
        return [tokens, pooled]


def _patch_onnxruntime(monkeypatch):
    ort = pytest.importorskip("onnxruntime")
    monkeypatch.setattr(ort, "get_available_providers", lambda: ["CPUExecutionProvider"])
    monkeypatch.setattr(ort, "InferenceSession", FakeONNXSession)


def test_dinov3_onnx_backbone_shapes_and_freeze(monkeypatch):
    _patch_onnxruntime(monkeypatch)
    model = Perceiver(
        use_backbone=True,
        backbone_type="dinov3_vitb16_onnx",
        backbone_freeze=True,
        backbone_checkpoint_path="fake.onnx",
    )

    assert model.backbone is not None
    assert all(param.requires_grad is False for param in model.backbone.parameters())

    out = model(torch.randn(1, 4, 3, 224, 224))
    assert out["t1"].shape == (1, 4, 196, 768)
    assert out["t2_pointmap"].shape == (1, 4, 196, 3)
    assert out["t3_evidence"].shape == (1, 4, 17, 32)
    assert out["backbone_load_error"] is None


def test_small_real_config_reaches_dream3r(monkeypatch):
    _patch_onnxruntime(monkeypatch)
    cfg = load_config(preset="small_real", overrides={"backbone_checkpoint_path": "fake.onnx"})
    args = config_to_model_args(cfg)

    assert args["backbone_type"] == "dinov3_vitb16_onnx"
    assert args["backbone_freeze"] is True
    assert CONFIGS["small_real"]["backbone_type"] == "dinov3_vitb16_onnx"

    model = Dream3R(args)
    assert model.perceiver.backbone_type == "dinov3_vitb16_onnx"
    assert model.perceiver.backbone is not None
