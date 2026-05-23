"""Schema tests for the Stage 1 real smoke script helpers."""

import torch

from dream3r.scripts.smoke_real_e2e import _depth_abs_rel, _parse_pair


def test_parse_pair():
    assert _parse_pair("0,1") == (0, 1)


def test_depth_abs_rel():
    pred = torch.tensor([[2.0, 4.0]])
    target = torch.tensor([[1.0, 4.0]])
    mask = torch.tensor([[True, True]])
    assert _depth_abs_rel(pred, target, mask) == 0.5
