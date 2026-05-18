"""Tests for W11 frozen DINO-style Perceiver backbone."""

import torch
import torch.nn as nn

from dream3r.config import load_config, config_to_model_args
from dream3r.model import Dream3R
from dream3r.modules import Perceiver


class FakeDINO(nn.Module):
    def __init__(self, d_out=768, n_tokens=256):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(1))
        self.d_out = d_out
        self.n_tokens = n_tokens

    def forward(self, x):
        base = x.mean(dim=(1, 2, 3), keepdim=False).view(x.shape[0], 1, 1)
        tokens = torch.ones(x.shape[0], self.n_tokens, self.d_out, device=x.device)
        return tokens * base * self.weight


def _with_fake_hub(fn):
    original = torch.hub.load
    torch.hub.load = lambda *args, **kwargs: FakeDINO()
    try:
        return fn()
    finally:
        torch.hub.load = original


def test_dinov2_backbone_shapes_and_freeze():
    def run():
        model = Perceiver(use_backbone=True, backbone_type="dinov2_vitb14", backbone_freeze=True)
        assert model.backbone is not None
        assert not any(param.requires_grad for param in model.backbone.parameters())

        out = model(torch.randn(1, 2, 3, 224, 224))
        assert out["t1"].shape == (1, 2, 256, 768)
        assert out["t2_pointmap"].shape == (1, 2, 256, 3)
        assert out["t3_evidence"].shape == (1, 2, 17, 32)
        assert out["backbone_load_error"] is None
    _with_fake_hub(run)


def test_frozen_backbone_has_no_grads_but_heads_train():
    def run():
        model = Perceiver(use_backbone=True, backbone_type="dinov2_vitb14", backbone_freeze=True)
        out = model(torch.randn(1, 1, 3, 224, 224))
        loss = out["t2_pointmap"].mean() + out["t3_evidence"].mean()
        loss.backward()

        assert all(param.grad is None for param in model.backbone.parameters())
        head_grads = [param.grad for param in model.pointmap_head.parameters() if param.requires_grad]
        evidence_grads = [param.grad for param in model.evidence_projectors.parameters() if param.requires_grad]
        assert any(grad is not None for grad in head_grads)
        assert any(grad is not None for grad in evidence_grads)
    _with_fake_hub(run)


def test_backbone_config_reaches_dream3r():
    def run():
        cfg = load_config(preset="small_vit", overrides={"gpus": "0"})
        args = config_to_model_args(cfg)
        assert args["backbone_type"] == "dinov2_vitb14"
        assert args["backbone_freeze"] is True

        model = Dream3R(args)
        assert model.perceiver.backbone_type == "dinov2_vitb14"
        assert model.perceiver.backbone is not None
    _with_fake_hub(run)


if __name__ == "__main__":
    test_dinov2_backbone_shapes_and_freeze()
    test_frozen_backbone_has_no_grads_but_heads_train()
    test_backbone_config_reaches_dream3r()
    print("All DINOv2 backbone tests passed.")
