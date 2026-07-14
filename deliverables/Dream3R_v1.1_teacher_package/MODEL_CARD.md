# Dream3R v1.1.0 模型卡

## 任务

Dream3R 对多个前馈三维重建专家产生的点图进行状态条件融合。模型接收 proposal pointmaps、对应置信度和 Dream memory context，输出融合点图、融合置信度与逐点专家权重。

## 正式策略

| 数据域 | 专家顺序 | 融合结构 | 已记录 AbsRel |
| --- | --- | --- | ---: |
| KITTI | Fast3R、MASt3R、Spann3R | 冻结状态先验与有界残差融合 | 0.1448 |
| ETH3D | Fast3R、MASt3R、Spann3R、VGGT-Omega | 无残差状态条件融合（SCF） | 0.0570 |

指标方向为越低越好。上述数值来自既有实验记录，当前交付包不包含数据集、专家模型权重或正式 checkpoint，因此不能仅依靠本包重新得到这些数值。

## 输入契约

- `proposal_pointmaps`：`[B, E, N, P, 3]`
- `proposal_confidences`：`[B, E, N, P, 1]`
- `memory_context`：`[B, D]`
- `conflict_score`：可选 `[B, 1]`
- `domain`：`kitti` 或 `eth3d`

其中 `E` 在 KITTI 为 3，在 ETH3D 为 4；专家顺序必须与上表一致。

## 输出契约

- `final_pointmap`：`[B, N, P, 3]`
- `final_confidence`：`[B, N, P, 1]`
- `expert_weights`：`[B, E, N, P]`，沿专家维归一化
- `domain_branch` 与 `release_version`：运行分支及版本信息

## 适用范围与限制

- 本模型是 proposal-fusion 模型，不是直接从图像生成三维结果的完整视觉基础模型。
- 随机初始化模式只用于接口测试；正式推理需要加载匹配的训练 checkpoint。
- 输入 proposal 的质量、尺度和专家顺序会直接影响输出。
- 当前正式策略只锁定 KITTI 与 ETH3D，未验证其他数据域。
