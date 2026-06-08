# Dream3R 中期后优化思路

日期：2026-06-08  
状态：中期报告/PPT 配套执行稿

## 总体判断

当前 Dream3R v1.1.0 已经能作为中期可交付模型包使用，但它离“论文级完整模型”还差三类工作：

```text
1. 证据更完整：当前有 v1.1 指标、状态对照和真实 cache demo；完整 benchmark rerun 仍需补齐。
2. 融合更可解释：当前知道 ETH3D 需要 VGGT-Omega，KITTI 走 stable fallback，但 teacher contribution 还需要系统消融。
3. proposal-free 还未成立：Foundation3R 有训练入口和 cache，但当前结果不足以替代 proposal bank。
```

因此后续优化应减少泛泛“加模块”的路线，先把 v1.1.0 做成论文级证据，再开一个受控的 v1.2 或 Foundation3R redesign。

## 优化线 A：把 v1.1.0 做成论文级实验系统

目标：保留当前官方模型身份，把证据从“可运行 release package”推进到“可写论文的正式实验”。

### A1. 固定数据协议

需要补齐：

```text
KITTI:
  固定窗口采样规则
  train/val/test 或 smoke/formal split 区分
  窗口数量从当前 gate 级别扩大到正式报告级别

ETH3D:
  固定场景划分
  区分 VGGT-Omega admission windows 和 final evaluation windows
  避免同一批窗口既调参又报告最终结论
```

产出：

```text
reports/midterm/tables/dataset_protocol.md
runs/release/v11_formal_eval/
```

### A2. 重复状态因果性控制

每个正式结果至少同时报告：

```text
correct-state
no-state
shuffle-state
```

并补充：

```text
mean / std over seeds or splits
paired difference
failure windows
```

这样可以把“状态有效”从单次 gate 结果变成更稳的实验结论。

### A3. Teacher contribution ablation

当前需要回答的问题是：

```text
哪个 teacher 在哪个域有用？
VGGT-Omega 为什么只进 ETH3D 分支？
KITTI 为什么保留 v1.0-rc1 fallback？
移除某个 teacher 后指标怎么变化？
```

建议表格：

| Ablation | KITTI AbsRel | ETH3D AbsRel | 解释 |
| --- | ---: | ---: | --- |
| full v1.1.0 | 0.1448 | 0.0570 | 当前官方 |
| no Dream state | 0.1553 | 0.0583 | 状态移除 |
| shuffle Dream state | 0.1521 | 0.0598 | 状态打乱 |
| no VGGT-Omega ETH3D branch | 待跑 | 待跑 | 验证 VGGT-Omega 贡献 |
| KITTI force VGGT branch | 已知不优，应正式记录 | 待补 | 解释 domain policy |

## 优化线 B：融合模型本身的下一步

目标：在不破坏 v1.1.0 fallback 的前提下，尝试更强的 v1.2。

### B1. Confidence calibration

当前 proposal confidence 主要作为融合输入。下一步应校准不同 teacher 的 confidence，使不同模型的置信度可比较。

可做：

```text
per-teacher temperature calibration
confidence-to-error reliability plot
ECE-like calibration metric for pointmap/depth error
```

预期收益：减少错误 teacher 在某些域中过度影响 fusion。

### B2. Conflict-aware residual

当前 residual refinement 已经证明 bounded route 有效，但还可以让 residual 显式依赖 teacher conflict：

```text
low conflict:
  保守融合，减少改动

high conflict:
  允许状态 prior 或 stronger teacher 介入
```

必须保留 gate：

```text
correct-state < no-state
correct-state < shuffle-state
KITTI 不低于 v1.0 fallback
ETH3D 不低于 v1.1 official
```

### B3. 从 hard domain policy 到 soft domain policy

v1.1.0 现在是硬分支：

```text
KITTI -> v1.0-rc1
ETH3D -> VGGT-Omega-expanded SCF
```

论文里可以先这样报告，但后续模型优化应尝试 soft policy：

```text
domain embedding
scene statistics
teacher conflict vector
state quality vector
```

输出从固定 domain label 扩展为 teacher/fusion weights。

风险：soft policy 容易过拟合当前小规模窗口，所以必须和 shuffle-state、held-out split 一起跑。

## 优化线 C：proposal-free Foundation3R 重设计

当前 proposal-free 分支保留为研究线。它已经具备代码入口，主要瓶颈集中在表示和监督强度。

下一轮必须改三件事：

```text
1. 输入表示：从浅层 image tokens 转向 VGGT/DINO/MASt3R dense features。
2. 监督目标：在 pointmap L1 之外加入 scale-normalized depth/pointmap、confidence mask 和 geometry consistency。
3. 数据规模：先构建更稳定 dense teacher cache，再跑明确 train/held-out。
```

成功门槛：

```text
student 接近 dense teacher target
correct-state 优于 no-state 和 shuffle-state
无 proposal leakage
推理时不读取 proposal pointmaps
```

只有这四条同时成立，Foundation3R 才能重新进入“独立 3R”讨论。

## 中期后优先级

| 优先级 | 工作 | 原因 |
| --- | --- | --- |
| P0 | 做中期报告/PPT | 先完成阶段交付 |
| P1 | v1.1 formal eval + ablation | 这是最接近论文结果的路线 |
| P2 | confidence calibration / conflict residual | 小改动，容易验证 |
| P3 | soft domain policy | 有潜力，但需防过拟合 |
| P4 | Foundation3R redesign | 长线，不适合抢中期交付 |

结论：中期答辩应把 v1.1.0 作为当前模型，把上述优化路线作为后续计划。Foundation3R 在 PPT 中作为后续研究线呈现。
