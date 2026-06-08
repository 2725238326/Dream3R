# Dream3R 中期报告 PPT 页纲与讲稿骨架

日期：2026-06-08  
建议页数：20 页  
建议时长：15-20 分钟

## PPT 总体叙事

PPT 采用论文式答辩线，围绕问题、方法、证据和后续实验展开：

```text
为什么 3R 还需要新架构？
-> 现有 DUSt3R/VGGT 系列解决了什么，又留下什么？
-> Dream3R 当前到底是什么模型？
-> v1.1.0 做到了什么？
-> 指标和对照说明了什么？
-> 哪些路线没有成功？
-> 后续怎么优化到论文级模型？
```

核心一句话：

```text
Dream3R v1.1.0 聚焦于前馈式 3R proposal bank 上的状态条件化融合：多个 3R teacher 产生候选几何，Dream state 与场景域信息参与融合决策。
```

## Slide 1. 封面

标题：

```text
面向前馈式三维重建的状态条件化 Proposal-Fusion 模型与验证平台
```

副标题：

```text
Dream3R 中期报告
```

讲稿：

```text
本次汇报主要介绍开题之后的阶段性工作，包括当前实际完成的模型、实验结果、未成功路线以及后续优化计划。
```

## Slide 2. 开题目标回顾

画面：四格表格。

| 开题目标 | 中期对应工作 |
| --- | --- |
| 长序列状态 | Dream state / memory context |
| 几何校验 | state/no-state/shuffle controls |
| 多模型组合 | proposal bank + teacher fusion |
| 统一实验平台 | release docs + verifier + cache demo |

讲稿：

```text
开题阶段提出的目标可以概括为四点：状态、校验、多模型组合和实验平台。中期阶段的工作围绕这四点展开，但最终收束到一个更具体的模型形态：状态条件化 proposal-fusion。
```

## Slide 3. 研究背景：3R 从级联流程走向前馈式模型

画面：左侧 SfM/MVS pipeline，右侧 DUSt3R/VGGT feed-forward。

要点：

```text
传统流程：features -> matching -> pose -> BA -> dense reconstruction
前馈式 3R：images -> pointmaps / cameras / depth
```

讲稿：

```text
传统三维重建依赖多个级联步骤。DUSt3R 之后，pointmap regression 让未知相机条件下的重建可以用前馈网络表达。VGGT 进一步展示了直接预测相机、点图、深度和轨迹的可能性。
```

## Slide 4. 现有 3R 模型的分化

画面：方法族矩阵。

| 方法 | 主要贡献 | 暴露的问题 |
| --- | --- | --- |
| DUSt3R | pose-free pointmap | pairwise + alignment |
| MASt3R | 3D-grounded matching | 下游组合仍复杂 |
| Fast3R | many-view forward | 大规模训练和域泛化 |
| Spann3R | spatial memory | 记忆更新策略 |
| VGGT | unified geometry prediction | 域表现存在差异 |
| Test3R | test-time consistency | 需要测试时优化 |

讲稿：

```text
这些工作说明 3R 已经进入模型分化阶段。不同模型有不同强项，研究重点从单一 backbone 设计扩展到不同场景下的模型选择、融合和验证。
```

## Slide 5. Dream3R 的问题定位

标题：

```text
从“单模型重建”转向“状态条件化候选几何融合”
```

画面：一句问题定义。

```text
Given multiple 3R proposal teachers, how can a system use state and scene evidence to fuse the right geometry proposal?
```

讲稿：

```text
Dream3R 当前研究的问题是 proposal bank 上的状态条件化融合。VGGT-Omega、v1.0-rc1 和其他 teachers 提供候选几何，Dream3R 负责把这些候选放入可检验的状态融合协议。
```

## Slide 6. 架构演化路线

画面：时间轴。

```text
开题候选架构
-> SCF / proposal bank
-> v1.0-rc1 stable fallback
-> v1.1.0 domain-conditional proposal-fusion
-> v1.2-exp0 experimental core bridge
```

讲稿：

```text
中期阶段完成了架构收束。可用模型固定到 v1.1.0，失败或不成熟分支保留为后续研究线。
```

## Slide 7. Dream3R v1.1.0 总览

画面：核心流程图。

```text
input images
-> 3R proposal teachers
-> proposal bank + confidence
-> Dream state / conflict score
-> domain policy
-> fused pointmap + confidence
```

讲稿：

```text
v1.1.0 的输入由多个 3R teacher 的几何提议构成。Dream state 和 conflict score 参与融合，domain policy 决定使用 KITTI 或 ETH3D 分支。
```

## Slide 8. KITTI 分支

标题：

```text
KITTI: 保留 v1.0-rc1 stable fallback
```

要点：

```text
bounded StatePrior + residual refinement
AbsRel = 0.1448
比 VGGT-expanded KITTI 分支更稳
```

讲稿：

```text
KITTI 上我们没有强行使用 VGGT-Omega。实验显示稳定 fallback 更可靠，因此 v1.1.0 在 KITTI 分支保留 v1.0-rc1。
```

## Slide 9. ETH3D 分支

标题：

```text
ETH3D: 引入 VGGT-Omega-expanded SCF
```

要点：

```text
VGGT-Omega oracle admission 在 ETH3D 上增益明显
ETH3D AbsRel 从 fallback 0.1475 到 v1.1 0.0570
```

讲稿：

```text
VGGT-Omega 在 ETH3D 分支中作为强 teacher 使用。它在 ETH3D-like 场景中给出更强几何提议，因此被纳入 domain-conditional fusion。
```

## Slide 10. 主结果表

| 模型 | KITTI AbsRel | ETH3D AbsRel |
| --- | ---: | ---: |
| v1.0-rc1 fallback | 0.1448 | 0.1475 |
| v1.1.0 official | 0.1448 | 0.0570 |

脚注：

```text
AbsRel 越小越好。
```

讲稿：

```text
当前官方结果是 KITTI 0.1448，ETH3D 0.0570。KITTI 保持稳定，ETH3D 通过 VGGT-Omega branch 获得明显下降。
```

## Slide 11. 状态因果性对照

| 数据域 | Correct state | No state | Shuffle state |
| --- | ---: | ---: | ---: |
| KITTI | 0.1448 | 0.1553 | 0.1521 |
| ETH3D | 0.0570 | 0.0583 | 0.0598 |

讲稿：

```text
这是本阶段最重要的对照。如果正确状态不优于无状态和乱序状态，Dream state 的作用就只能停留在结构假设。当前两个域 correct-state 都最好。
```

## Slide 12. 真实 proposal-cache runtime demo

画面：文件和验证链。

```text
run_dream3r_v11_cache_demo.py
-> cache_demo_kitti.json
-> cache_demo_eth3d.json
```

讲稿：

```text
除了合成 demo，我们还补了真实 cache runtime demo。它读取已有 SCF/VGGT-Omega 缓存，检查 expert 顺序和 d_memory 适配。这个证据说明模型包能运行真实缓存；其性质是 runtime contract verification。
```

## Slide 13. 没有纳入官方模型的分支

| 分支 | 当前结论 |
| --- | --- |
| Qwen3-VL semantic controller | diagnostic-only，当前无几何增益 |
| Foundation3R proposal-free | 有训练入口，当前指标不足 |
| NativeStudent/ImageStateStudent | 结构有效，指标不足 |
| v1.2-exp0 core bridge | experimental，保留实验分支 |

讲稿：

```text
这些结果解释了当前模型选择 proposal-fusion 的依据。Qwen、Foundation3R 和 v1.2-exp0 都保留为后续研究线，但当前答辩只报告它们已经通过的证据。
```

## Slide 14. 当前模型定位

画面：三句话。

```text
对象：前馈式 3R proposal bank
信号：Dream state、候选冲突、场景域
输出：domain-conditional fused pointmap
```

讲稿：

```text
这一页给出当前模型定位。Dream3R v1.1.0 的贡献在 proposal bank 之上的状态条件化融合和验证链路；proposal-free Foundation3R 作为后续研究线保留。
```

## Slide 15. 后续优化思路一：v1.1 做成论文级实验

要点：

```text
固定 KITTI/ETH3D 数据协议
扩大窗口数量
多 seed / split
补充 runtime / VRAM / failure case
```

讲稿：

```text
下一步优先把 v1.1.0 的证据补到论文级。这样能把当前 release package 变成可外部审阅的实验系统。
```

## Slide 16. 后续优化思路二：融合模型优化

要点：

```text
confidence calibration
teacher contribution ablation
conflict-aware residual
soft domain policy
```

讲稿：

```text
模型层面可以继续优化融合策略。重点是让系统知道哪个 teacher 在什么域可靠，并用消融控制模块数量。
```

## Slide 17. 后续优化思路三：proposal-free 重设计

要点：

```text
使用更强视觉表示
dense teacher target
scale-normalized loss
严格 proposal leakage audit
```

讲稿：

```text
proposal-free 路线暂列后续研究线。后续如果要重启，需要改变表示和监督方式，先证明 student 接近 teacher target，再讨论 foundation model。
```

## Slide 18. 平台与复现链路

画面：release docs + verifier + artifacts。

```text
OFFICIAL_VERSION
EFFECTIVE_ARCHITECTURE
MODEL_CARD
VERIFY_REPORT
ARTIFACTS
verifier / smoke / demo / cache-demo
```

讲稿：

```text
除结果表外，当前工作已经形成固定入口、验证脚本、artifact manifest 和服务器运行证据，后续复现实验可以接着这条链路推进。
```

## Slide 19. 当前不足

要点：

```text
仍依赖 proposal teachers
domain policy 仍窄
real-cache demo 属于 runtime contract 证据
更长序列和动态场景尚未验证
Qwen 语义未提升几何
```

讲稿：

```text
这些不足需要主动说明。它们也是后续工作的来源，可以自然导向下一阶段实验计划。
```

## Slide 20. 总结

三句话：

```text
1. Dream3R v1.1.0 已形成可运行官方模型包。
2. 当前贡献是状态条件化 proposal-fusion 与可验证状态对照。
3. 后续重点是正式评测、融合优化和 proposal-free 重设计。
```

讲稿：

```text
总结来说，本阶段已经从开题架构设想推进到 v1.1.0 可运行模型包。当前模型有明确指标、状态对照和复现链路。后续会先把 v1.1 证据做完整，再推进更激进的 proposal-free 方向。
```

## 制作建议

PPT 视觉上只需要三类图：

```text
1. pipeline 对比图：传统 SfM/MVS vs feed-forward 3R。
2. Dream3R v1.1 架构图：proposal teachers -> proposal bank -> state/domain fusion。
3. 三张表：主结果、状态对照、失败分支/后续优化。
```

视觉上保持克制。中期答辩最重要的是老师能在 5 分钟内听懂：

```text
Dream3R 是什么
模块如何服务模型问题
当前指标是多少
Qwen/Foundation3R 的实验结论
下一步怎么优化
```
