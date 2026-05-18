# 3R / feed-forward 3D reconstruction model inventory

Status: first-stage inventory for the Typst survey. This file records model roles,
source status, and writing boundaries before main-body prose is drafted.

Evidence labels used here:

- `paper-proven`: the claim is taken from the paper title, abstract, or the local Dream literature board.
- `registry-listed`: code/project status is copied from `E:\kykt\Dream\registry\source_registry.md` or `E:\kykt\Dream\units\REPRODUCTION_READINESS_MATRIX.md`; license and checkpoint details still need direct file-level verification before public or commercial use.
- `local-observed`: Dream-side notes report a local adapter, test, or smoke path. This does not imply reconstruction quality.
- `inferred`: review-level grouping or interpretation.
- `尚需确认`: the claim should not be used as a factual statement until the paper/repository has been read directly.

## 写作边界

- 本综述的中心是近期 3R / feed-forward 3D reconstruction 模型谱系，不把 Dream3R 写成中心模型。
- Dream 资料只作为方法论背景：证据分层、流程验证与质量判断分离、应用落地需要可复现产物。
- 不写“某模型整体领先”一类结论，除非正文引用原论文实验表或第三方评测；本清单阶段只记录模型定位。
- “代码可用”“权重可用”“demo 可跑”均按来源记录，不等同于本地质量验证。

## 谱系概览

| 分支 | 主要问题 | 代表模型 | 本综述中的处理方式 |
|---|---|---|---|
| 点图与匹配 | 不依赖完整相机标定，直接预测稠密 3D 表示和匹配线索 | DUSt3R, MASt3R, MASt3R-SfM | 作为 3R 范式起点和后续分支的共同语言 |
| 多视角规模化 | 多图输入时避免成对重建和昂贵全局对齐 | Fast3R, MV-DUSt3R+, VGGT, MapAnything | 讨论 batch/多视角/统一几何模型的不同取舍 |
| 深度与先验利用 | 单目深度、相机、位姿、场景先验如何进入 3R | Align3R, Pow3R, Depth Anything V2, Depth Pro, Metric3D v2 | 作为支撑先验和条件输入，不喧宾夺主 |
| 长序列状态与记忆 | 视频/长序列中的漂移、遗忘、缓存预算 | CUT3R, Spann3R, Point3R, STream3R, LONG3R, LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, LongStream | 区分 recurrent state、external memory、cache governance 和 filtering |
| 动态与 4D | 移动物体破坏静态几何假设 | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R | 区分动态 pointmap、训练自由修正、ray-based 动态抑制和 4D 输出 |
| 测试时验证/更新 | 推理阶段如何发现或缓解几何冲突 | Test3R, TTT3R, G-CUT3R, MASt3R-SfM | 区分一致性评分、测试时训练、先验引导和 SfM 后处理 |
| 可视化与资产输出 | 从几何预测走向可查看/可报告的结果 | Splatt3R, InstantSplat, NoPoSplat, 3DGS, 4DGS | 作为输出表示和应用路径，不等同于 3R 核心问题 |

## 基础点图与匹配线

| 模型 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| DUSt3R | 2023/2024 | 图像对或多视角，弱化相机先验 | pointmap、confidence，可导出深度/位姿/匹配 | `paper-proven`: pose-free dense pointmap regression 和 global alignment | 后续多视角仍可能依赖成对组合与全局对齐；非动态专用 | `registry-listed`: code/checkpoints/demo；P0 基础线 |
| MASt3R | 2024 | 图像对/多图匹配场景 | 3D-grounded matching、稀疏/稠密对应、pointmap | `paper-proven`: 在 DUSt3R 风格几何上增强匹配和 descriptor | 不应写成替代 DUSt3R；更适合匹配和 SfM 接口 | `registry-listed`: code/checkpoints/demo；Dream 有部分 adapter 记录，质量尚需确认 |
| MASt3R-SfM | 2024 | 无约束 SfM 图像集合 | 匹配、检索、全局 SfM 对齐结果 | `paper-proven`: 将 MASt3R 特征接入 SfM pipeline | 它是 SfM-stage refinement，不是 per-window Critic | `registry-listed`: MASt3R 生态代码；适合传统几何桥接 |

## 多视角规模化与统一几何模型

| 模型 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| Fast3R | 2025 | 多图集合，目标是大规模图像数 | 多视角 3D 重建结果 | `paper-proven`: 1000+ images in one forward pass 的 many-view 路线 | 不是流式模型；本地 Dream 记录有依赖阻塞 | `registry-listed`: code/checkpoint/demo；P1 scale baseline |
| MV-DUSt3R+ | 2024/2025 | sparse views，pose-free RGB | pointmap、pose/NVS 相关输出、Gaussian heads | `paper-proven`: multi-view decoder + cross-reference-view fusion；12/20-view examples checked | 论文与 README 代码状态需分开引用；环境约束需确认 | `repo-checked 2026-05-13`: code/checkpoints/Gradio；README lists CC BY-NC 4.0 |
| VGGT | 2025 | 多视角 feed-forward visual geometry | camera、depth、pointmap、tracks | `paper-proven`: unified feed-forward geometry prediction | 不宜写成“一步替代全部 3R”；仍需按输入 regime 比较 | `registry-listed`: Meta repo；Dream 记录为强 comparator，尚未做本地质量表 |
| MapAnything | 2025/2026 | 一张或多张图，允许可选 intrinsics/pose/depth/partial recon | metric scene geometry、camera、depth/ray map 等 | `paper-proven`: universal feed-forward metric 3D reconstruction | 其“通用性”需按论文实验和输入条件解释；不要泛化为所有应用可用 | PDF 已下载；代码/许可状态尚需确认 |

## 深度、视频一致性与可选先验

| 模型/先验 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| Align3R | 2024/2025 | 动态视频 + 单目深度线索 | aligned depth、camera pose 相关结果 | `paper-proven`: 用 DUSt3R 式对齐改善 monocular depth 的时序一致性 | 属于视频深度/对齐桥接，不是通用 3R 后继 | PDF 已下载；CVPR 2025 PDF/source 可用于正文引用 |
| Pow3R | 2025 | 无约束输入，可带 camera/scene/depth priors | 3D reconstruction | `paper-proven`: inference-time optional priors for reconstruction | 需要明确哪些先验是输入、哪些是模型内部能力 | PDF 已下载；代码状态尚需确认 |
| Depth Anything / V2 | 2024 | 单图深度估计 | relative 或 depth prediction | `paper-proven`: large-scale unlabeled data + robust monocular depth | 只作深度先验；不直接输出相机或多视角一致点图 | PDF 已下载；代码/权重常见，但正文须按官方源引用 |
| Depth Pro | 2024 | 单图 | metric depth、focal length 相关输出 | `paper-proven`: sharp monocular metric depth | 可作为 metric-scale prior，不能替代多视角重建 | PDF 已下载；应用可行性需实测 |
| Metric3D v2 | 2024 | 单图 | metric depth、surface normal | `paper-proven`: zero-shot metric depth and normal | 与 3R 的关系是先验/辅助监督 | PDF 已下载；应用可行性需实测 |
| DINOv2 / DINOv3 | 2023/2025 | 图像特征预训练 | dense visual features | `paper-proven`: self-supervised visual features | 不是 3R 模型；只作 backbone/feature prior | PDF 已下载；Dream 记录有 DINOv2 path，DINOv3 尚需专项确认 |

## 长序列状态、记忆与缓存

| 模型 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| CUT3R | 2025 | continuous RGB sequence | online pointmaps / 3D perception state | `paper-proven`: persistent state tokens for continuous 3D perception | 不要把 recurrent state 写成外部可写空间记忆 | `registry-listed`: code/checkpoints/demo；Dream 有 state recurrence 借鉴 |
| Spann3R | 2024 | sequential / multi-view reconstruction | global pointmap prediction | `paper-proven`: spatial memory for 3D reconstruction | 是带 memory 的 3R 模型，不等同于 Mem3R/Point3R memory architecture | `registry-listed`: code；Dream 有部分 adapter 记录，质量尚需确认 |
| Point3R | 2025 | streaming dense reconstruction | spatial pointer memory + reconstruction | `paper-proven`: explicit spatial pointer memory | 与 Mem3R 的 hybrid memory 不同；不要混写 | `registry-listed`: code/checkpoint；P2 comparator |
| STream3R | 2025/2026 | sequential image stream | causal streaming 3D reconstruction | `paper-proven`: decoder-only/causal Transformer and stream session | 主要是 causal streaming architecture，不是无限外部记忆 | `registry-listed`: code/app/inference path；P2 comparator |
| LONG3R | 2025 | long sequence stream | 3D spatio-temporal memory | `paper-proven`: long-sequence streaming memory with gating/pruning | gate 是模型机制，不等同于外部 controller | PDF 已下载；project/code 状态需确认 |
| LoGeR | 2026 | long-context geometric reconstruction | local + global hybrid memory | `paper-proven`: TTT global memory + sliding-window local memory | 不等同于 Mem3R；混合轴不同 | PDF 已下载；project/code 状态需确认 |
| Mem3R | 2026 | streaming 3D reconstruction | hybrid memory, tracking + mapping decoupled | `paper-proven`: KV cache for tracking + map memory | 不等同于 OVGGT anchor cache 或 Point3R pointer memory | PDF 已下载；project/code 状态需确认 |
| OVGGT | 2026 | streaming visual geometry with fixed compute budget | compressed cache / protected dynamic anchors | `paper-proven`: O(1) constant-cost cache governance | 是 cache/anchor budget 机制，不是泛泛“记忆更强” | `source-checked 2026-05-13`: arXiv lists project/code links; repo license not read |
| PAS3R | 2026 | long monocular stream | pose-adaptive streaming state update | `paper-proven`: update gain depends on pose novelty | 不应写成 Mamba/SSM 路线 | `source-checked 2026-05-13`: arXiv page only; no stronger code claim |
| FILT3R | 2026 | streaming 3D reconstruction | latent state filtering | `paper-proven`: Kalman-style latent adaptive filter | 不是传统 SLAM graph Kalman filter | `source-checked 2026-05-13`: arXiv says code will be released |
| LongStream | 2026 | long sequence autoregressive visual geometry | streaming geometry with cache refresh | `paper-proven`: gauge-decoupled streaming and cache refresh | 与 STream3R/CUT3R 的状态范围需在正文区分 | `source-checked 2026-05-13`: arXiv lists project page; code/license not upgraded |

## 动态场景与 4D reconstruction

| 模型 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| MonST3R | 2024/2025 | dynamic video | per-frame geometry, dynamic masks/confidence | `paper-proven`: motion-aware geometry estimation | 不维护长期 object identity；不要写成 4D memory | `registry-listed`: code/demo；P1 dynamic comparator |
| POMATO | 2025 | dynamic 3D reconstruction | pointmap matching + temporal motion | `paper-proven`: pointmap matching with temporal motion | 与 D^2USt3R 机制不同，不能只归为“动态版 DUSt3R” | PDF 已下载；code/location 尚需确认 |
| D^2USt3R | 2025 | dynamic scenes | 4D pointmaps | `paper-proven`: dynamic-aware 4D pointmap extension | 4D 指时序点图，不是 4DGS asset | PDF 已下载；代码状态需确认 |
| Easi3R | 2025 | existing 3R output + dynamic regions | disentangled motion / dynamic correction | `paper-proven`: training-free adaptation from DUSt3R | 与 MonST3R 的训练式动态建模不同 | PDF 已下载；project/code 状态需确认 |
| RayMap3R | 2026 | streaming dynamic reconstruction | ray/image dual-branch dynamic suppression | `paper-proven`: training-free RayMap-based dynamic identification | ray representation 与 pointmap representation 的证据信号不同 | `source-checked 2026-05-13`: project page lists arXiv/code; local quality not verified |

## 测试时验证、修正和自适应

| 模型/机制 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| Test3R | 2025 | DUSt3R/MASt3R family outputs, image triplets | consistency signal / prompt tuning | `paper-proven`: test-time learning via cross-pair geometric consistency | 应区分为 triplet consistency / prompt tuning，不同于 TTT3R 的长序列 memory update | PDF 已下载；code listed，集成成本尚需确认 |
| TTT3R | 2025/2026 | CUT3R-style state / hard cases | updated state / reconstruction | `paper-proven`: 3D reconstruction as test-time training；20 FPS / 6 GB source-checked | 更新 internal state；计算和失败模式不同于 Test3R；吞吐数字需带条件引用 | `source-checked 2026-05-13`: project page + PDF front matter |
| G-CUT3R | 2025 | guided reconstruction with camera/depth priors | guided 3D reconstruction | `paper-proven`: camera and depth prior integration | 先验冲突检测属于 review/Dream inferred extension，不是论文直接结论 | PDF 已下载；代码状态未知 |
| MASt3R-SfM | 2024 | image collection | SfM-aligned reconstruction | `paper-proven`: matching + global SfM consistency | 可作为验证/修正参照，但不是轻量 per-window critic | 见基础线条目 |

## Gaussian / renderable output line

| 模型/表示 | 年份 | 输入假设 | 输出表示 | 核心机制 | 局限/注意 | 应用状态 |
|---|---:|---|---|---|---|---|
| 3D Gaussian Splatting | 2023 | posed images / SfM initialization in original setup | anisotropic 3D Gaussians | `paper-proven`: real-time radiance field rendering | 是渲染表示，不是 pose-free 3R 本身 | PDF 已下载；作为输出表示背景 |
| 4D Gaussian Splatting / 4DGS | 2023/2024 | dynamic scene video | dynamic Gaussian representation | `paper-proven`: dynamic novel-view rendering | 与 4D pointmap 不同；不要混同动态重建与资产渲染 | PDF 已下载；作为应用/可视化背景 |
| Splatt3R | 2024 | uncalibrated image pairs | 3D Gaussian splats | `paper-proven`: MASt3R-based pose-free Gaussian prediction | 许可和依赖约束需要正文注明；demo 可见不等于质量领先 | `registry-listed`: code/checkpoint/Gradio；P0 visual demo |
| InstantSplat | 2024 | sparse-view / pose-free images | 3D Gaussians | `paper-proven`: dense stereo prior + 3DGS | 依赖链重；应用可行性需按本地环境验证 | `registry-listed`: code/scripts；P0/P1 visual |
| NoPoSplat | 2024/2025 | sparse unposed multi-view images | 3D Gaussians | `paper-proven`: feed-forward unposed sparse-view Gaussian reconstruction | 没有 first-pass Gradio path 的本地记录；不能写成最易部署 | `registry-listed`: MIT/checkpoints noted in Dream matrix;需复核 |

## 支撑先验

| 先验 | 年份 | 主要用途 | 与 3R 的关系 | 注意事项 |
|---|---:|---|---|---|
| CoTracker | 2023 | long video point tracking | 动态/身份一致性先验 | 2D tracking prior，不直接提供 3D 重建 |
| SpatialTracker | 2024 | tracking pixels in 3D space | 3D-aware motion prior | V2 线索需另行核对；正文优先引用已下载论文 |
| SAM 2 | 2024 | image/video segmentation | 动态区域、mask prior | 只作为辅助先验；避免把 segmentation 写成几何验证 |
| DINOv2/v3 | 2023/2025 | dense visual feature prior | backbone / matching / depth prior | 不是 3R 方法；性能判断要引用原论文或具体实验 |
| Depth Anything / V2, Depth Pro, Metric3D v2 | 2024 | monocular depth / metric geometry | 作为 3R 的条件输入、初始化或一致性检查 | 单帧深度质量不等于多视角一致性 |

## 章节结构记录

1. 引言：说明 3R 的范式变化、综述范围和证据边界。
2. 从传统几何流程到 pointmap 表示：解释 SfM/MVS 的中间变量和 DUSt3R 的重新组织。
3. DUSt3R 及匹配增强分支：DUSt3R、MASt3R、MASt3R-SfM。
4. 多视角规模化与统一视觉几何模型：Fast3R、MV-DUSt3R+、VGGT、MapAnything、Pow3R。
5. 视频深度、动态场景和 4D 重建：Align3R、MonST3R、POMATO、D^2USt3R、Easi3R、RayMap3R。
6. 长序列重建中的状态、记忆和缓存机制：CUT3R、Spann3R、Point3R、STream3R、LONG3R、LoGeR、Mem3R、OVGGT、PAS3R、FILT3R、LongStream。
7. 测试时验证、修正和自适应：Test3R、TTT3R、G-CUT3R、MASt3R-SfM。
8. 面向应用的输出表示：point cloud、depth、confidence、mesh、3DGS/4DGS、Splatt3R、InstantSplat、NoPoSplat。
9. 方法比较表：输入假设、输出表示、是否需要相机、动态/长序列能力、代码/权重状态、应用落地难度。
10. 图示和应用路径：图像/视频输入到可查看重建结果、质量检查、报告和 KYKT 集成。
11. 经验总结与开放问题：以证据分层和失败模式为中心，避免把 Dream 经验写成模型结论。

## 待确认清单

- 逐篇读取 PDF 后再写性能/benchmark 结论；当前仅完成元数据、摘要和本地资料的第一轮核对。
- 代码许可证、权重许可证、demo 成熟度需从官方仓库文件直接确认。
- 对 VGGT、MapAnything、MV-DUSt3R+ 等统一/多视角模型的比较需要引用原论文实验表或第三方评测。
- 对 2026 年模型（LoGeR、Mem3R、OVGGT、PAS3R、FILT3R、LongStream、RayMap3R）已推进到来源级状态；仍需在复用代码/权重前逐仓库读 license 和 checkpoint terms。
