# 训练与 checkpoint 说明

## 训练输入

训练脚本读取预先生成的 PyTorch proposal cache。cache 至少应包含：

- `entries`：样本列表；每个样本包含数据域、专家点图、专家置信度、真值点图、有效掩码和 memory context。
- `expert_order`：专家名称列表，顺序必须与 cache 内张量一致。
- `d_memory`：memory context 维度。

cache 生成依赖第三方专家模型及其权重，本交付包不包含这些模型和数据。

## 训练入口

查看参数：

```bash
python -m dream3r.scripts.train_scf_head --help
python -m dream3r.scripts.train_proposal_set_decoder --help
```

典型流程是先准备一个或多个 cache，再按数据域划分训练和验证集合，运行状态、无状态和乱序状态三个控制实验。正式选择必须以正确状态优于两个控制组为前提。

## checkpoint 格式

KITTI 分支：

```python
{
    "decoder_state_dict": decoder.state_dict(),
    "config": {...}
}
```

ETH3D 分支：

```python
{
    "head_state_dict": head.state_dict(),
    "config": {
        "n_experts": 4,
        "d_memory": 32,
        "head_dim": 64,
        "hidden": 128,
        "use_state": True,
        "use_residual": False,
        "expert_order": ["fast3r", "mast3r", "spann3r", "vggt_omega"]
    }
}
```

加载方式：

```python
from dream3r import build_dream3r_v11_release

model = build_dream3r_v11_release(
    kitti_checkpoint="checkpoints/kitti.pt",
    eth3d_checkpoint="checkpoints/eth3d.pt",
).eval()
```

测试套件包含两个分支联合保存、加载和前向传播的回归测试。
