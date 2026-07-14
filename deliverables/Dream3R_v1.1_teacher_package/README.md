# Dream3R v1.1.0 代码交付包

本目录包含 Dream3R 当前正式版本的核心推理、cache 训练入口、回归测试和接口文档。交付内容聚焦于状态条件化的多专家三维重建融合模块，不包含研究过程记录、废弃实验、缓存、日志或中间结果。

## 模型结构

- KITTI 分支：3 个专家（Fast3R、MASt3R、Spann3R）的状态先验加权与有界残差融合。
- ETH3D 分支：在上述专家基础上加入 VGGT-Omega，使用状态条件融合（SCF）。
- 输入：各专家生成的点图、置信度、Dream 状态向量及可选冲突分数。
- 输出：融合点图、融合置信度和专家权重。

当前发布版本为 `v1.1.0`。已记录的 AbsRel 为 KITTI `0.1448`、ETH3D `0.0570`；这些数值来自项目既有评测，不由本包中的随机输入演示重新计算。

## 环境

建议使用 Python 3.10 或更高版本：

```bash
python -m pip install -r requirements.txt
```

## 快速验证

在本目录执行：

```bash
python -m pytest
python -m dream3r.scripts.smoke_release --output smoke_result.json
python -m dream3r.scripts.run_demo --domain kitti --output demo_kitti.json
python -m dream3r.scripts.run_demo --domain eth3d --output demo_eth3d.json
```

测试和演示使用随机生成、形状符合接口约定的 proposal tensors，用于验证代码结构与前向传播。

## 使用示例

```python
import torch
from dream3r import build_dream3r_v11_release

model = build_dream3r_v11_release(d_memory=32).eval()
pointmaps = torch.randn(1, 3, 2, 64, 3)
confidences = torch.rand(1, 3, 2, 64, 1)
memory = torch.randn(1, 32)

with torch.inference_mode():
    result = model(pointmaps, confidences, memory, domain="kitti")

print(result["final_pointmap"].shape)
```

ETH3D 分支的专家数为 4；其余张量格式不变。

## 文件说明

- `dream3r/release_v11.py`：v1.1.0 统一入口与双域路由。
- `dream3r/release_candidate.py`：KITTI 发布分支。
- `dream3r/proposal_set_decoder.py`：状态条件 proposal 融合解码器。
- `dream3r/scf_head.py`：ETH3D 状态条件融合头。
- `dream3r/state_prior_head.py`：状态先验权重模块。
- `dream3r/scripts/`：演示、运行时自检及 proposal-cache 训练入口。
- `tests/`：正式发布接口回归测试。
- `MODEL_CARD.md`：模型能力、张量契约与限制。
- `TRAINING.md`：训练 cache 与 checkpoint 格式。
- `ENVIRONMENT.md`：依赖范围和最终验证环境。

## 交付边界

本包不包含数据集、第三方专家模型、训练缓存或 checkpoint。完整图像推理需要先由 Fast3R、MASt3R、Spann3R 和 VGGT-Omega 生成符合接口约定的 proposal tensors，再交给本模型融合。无 checkpoint 时，构建函数会初始化相同结构的模型，适用于接口测试，不代表训练后指标。
