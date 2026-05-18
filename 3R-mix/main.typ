// DEPRECATED — Typst-era historical snapshot, no longer maintained.
// Current canonical manuscript is `main.tex` (LaTeX, ctexart + xelatex + unsrtnat).
// See README.md and NEW_CHAT_HANDOFF.md.

#import "review-template.typ": *

#show: review.with(
  title: "近期 3R 模型综述：表示、序列机制与应用证据",
  subtitle: "从 DUSt3R 式 pointmap 到 feed-forward visual geometry",
  authors: ("KYKT Dream",),
  date: "2026 年 5 月 12 日",
  abstract: [
    近期 3R / feed-forward 3D reconstruction 方法的核心变化，不是把传统 SfM/MVS 流程中的某一步替换成神经网络，而是把深度、相机、匹配、点云和时序状态重新组织为可学习的几何表示。DUSt3R 以 pointmap regression 为共同起点，MASt3R、Fast3R、VGGT、CUT3R、Spann3R、MonST3R、Test3R 和一批 Gaussian 输出方法分别沿匹配、多视角统一几何、长序列状态、动态场景、测试时一致性和可渲染资产方向扩展。本文不做跨论文 SOTA 排名，而按输入 regime、输出表示、时间机制、动态处理、测试时机制和应用证据来梳理这一谱系，并明确区分论文结论、代码状态、本地流程验证和应用可行性。
  ],
  keywords: [3R；feed-forward 3D reconstruction；pointmap；visual geometry；streaming reconstruction；dynamic reconstruction；Gaussian Splatting],
)

= 引言：3R 综述应回答什么问题

基于图像的三维重建长期依赖显式几何流程：特征提取、匹配、相机估计、三角化、多视图深度融合和全局优化。这个流程有清晰的中间变量，也便于工程调试；但在互联网图像、稀疏视角、动态视频和长序列场景中，匹配失败、尺度不稳、相机漂移和动态污染会逐级放大。近期 3R 方法的出现，正是对这种流程脆弱性的系统回应。

DUSt3R 将任意图像对直接回归为稠密 pointmap 和 confidence，并从中派生深度、匹配、相对相机和重建结果 @dust3r。这个表示把原来分散在多个模块中的几何变量收进同一输出空间，成为后续 3R 模型共享的语言。MASt3R 把 matching 放回 3D-grounded 表示中 @mast3r，Fast3R 和 MV-DUSt3R+ 处理多视角组织成本 @fast3r @mvdust3rplus，VGGT 同时预测 camera、depth、pointmap 和 tracks @vggt，CUT3R 和 Spann3R 把问题推进到连续观测和记忆 @cut3r @spann3r，MonST3R 等方法则尝试在运动存在时保持几何估计 @monst3r。

因此，本文不把近期工作写成“谁替代谁”的线性进步史，而是把它们组织为六个问题：第一，pointmap 表示如何重组传统几何任务；第二，多图输入如何从 pairwise pipeline 走向 many-view 或统一几何预测；第三，视频和动态场景如何破坏静态假设；第四，长序列中状态、记忆和缓存如何治理历史信息；第五，测试阶段如何做一致性学习、先验引导和错误缓解；第六，几何输出如何转为可查看、可记录、可复现的应用产物。

本文使用 Dream 长期调研中的经验作为方法论背景，而不是把 Dream3R 作为综述中心。具体做法是区分四类证据：论文中已经说明的机制，官方代码或 demo 的可用状态，本地流程是否跑通，以及重建质量是否在可比实验中得到支持。没有统一 benchmark、输入条件和许可证检查时，本文不把“流程可运行”写成“质量领先”。

= 材料来源与筛选边界

本文材料来自 arXiv、CVF/ECCV、项目主页、官方 GitHub，以及本地 `papers/` 中保存的 43 篇 PDF。当前正文已经对核心论文做了摘要层核验：DUSt3R 的无相机 pointmap regression，MASt3R 的 3D matching，Fast3R 的 many-view forward pass，VGGT 的 unified visual geometry，CUT3R 的 recurrent persistent state，Spann3R 的 external spatial memory，Test3R 的 triplet consistency prompt tuning，TTT3R 的 long-sequence memory update 等都来自本地 PDF 摘要或前言核对 @dust3r @mast3r @fast3r @vggt @cut3r @spann3r @test3r @ttt3r。

纳入标准按“是否直接改变 3R 问题设置”分层。直接 3R / pointmap / feed-forward geometry 方法构成正文主线；动态、长序列、测试时自适应和 prior-guided reconstruction 作为机制扩展；3DGS/4DGS 与 pose-free Gaussian 方法作为输出表示；Depth Anything、DINO、CoTracker、SpatialTracker、SAM 2 等作为支撑先验，不参与 3R 模型排名 @depth_anything @depth_anything_v2 @dinov2 @dinov3 @cotracker @spatialtracker @sam2。

#figure(
  thick-table(
    (1fr, 1.6fr, 2.3fr),
    [层级], [纳入对象], [本文中的角色],
    [核心 3R], [DUSt3R, MASt3R, MASt3R-SfM, Fast3R, MV-DUSt3R+, VGGT, MapAnything, Pow3R], [解释 pointmap、matching、many-view、unified geometry 和 optional priors 的主线。],
    [时间与动态扩展], [CUT3R, Spann3R, Point3R, STream3R, LONG3R, LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, LongStream, MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R], [解释状态、记忆、缓存、动态抑制和 4D pointmap 的机制差异。],
    [测试时与先验机制], [Test3R, TTT3R, G-CUT3R, MASt3R-SfM], [解释 consistency learning、memory update、prior-guided reconstruction 与 SfM alignment。],
    [输出与支撑先验], [Splatt3R, InstantSplat, NoPoSplat, 3DGS, 4DGS, Depth Anything, DINO, CoTracker, SAM 2], [说明可渲染输出、深度/特征/跟踪/分割先验，不作为核心 3R 排名。],
  ),
  caption: [本文的文献分层。粗线表格用于强调角色边界：分层不是论文价值排序，而是综述中的论证位置。],
)

= Pointmap：3R 谱系的共同表示

传统 SfM/MVS 把图像匹配、相机估计和三维点求解拆成显式阶段。DUSt3R 的变化在于，它不把相机标定和位姿估计放在输入前提中，而是把每个像素对应的 3D 点直接作为模型输出，再用 alignment 或下游几何操作恢复相机、深度和匹配 @dust3r。换言之，pointmap 不是简单的点云结果，而是一个中间几何接口。

这个接口有三点影响。第一，它允许模型在相机未知、视角稀疏或匹配困难时仍然给出稠密 3D 假设。第二，confidence 与 pointmap 共同输出，使后续一致性检查和失败区域标注有了入口。第三，它把后续扩展的焦点从“如何求出相机”转向“如何组织多个 pointmap、如何维持时序一致、如何处理动态和先验冲突”。

#figure(
  thick-table(
    (1.15fr, 1.15fr),
    [显式几何流程], [DUSt3R 式 pointmap 流程],
    [feature matching -> pose estimation -> triangulation -> MVS/depth fusion -> point cloud / mesh], [image pair or set -> transformer prediction -> pointmap + confidence -> alignment / matching / pose / depth / output],
    [优势：中间变量清晰，可解释性强。局限：早期匹配和相机误差会沿流程传播。], [优势：弱化相机先验，统一深度、匹配和重建。局限：多视角一致、长序列状态和动态场景仍需额外机制。],
  ),
  caption: [传统流程和 pointmap 流程的任务组织差异。右侧并不取消几何约束，而是把部分中间变量纳入可学习表示。],
)

MASt3R 说明 pointmap 不只服务于重建，也可以服务于 matching。它在 DUSt3R 式几何上加入 dense local features、matching loss 和 reciprocal matching，使 learned 3D features 更容易接入检索、匹配和 SfM pipeline @mast3r。MASt3R-SfM 进一步把这些特征与全局 SfM alignment 结合，说明 feed-forward 3R 与经典几何并非互斥，而是在真实系统中可能形成互补 @mast3r_sfm。

= 从图像对到多视角统一几何

pairwise pointmap 为 3R 提供了基础接口，但图像数量增加后，成对组合和全局对齐会成为主要成本。Fast3R 正是针对这一问题提出 many-view forward pass，试图绕开大量 pairwise prediction 和 iterative alignment @fast3r。MV-DUSt3R+ 则面向稀疏多视角，强调 single-stage scene reconstruction from sparse views，并通过跨参考视角的信息融合减轻参考视角选择带来的不稳定 @mvdust3rplus。

VGGT 和 MapAnything 代表了更统一的方向。VGGT 把 camera parameters、depth maps、point maps 和 point tracks 放入一个 feed-forward visual geometry 模型 @vggt；MapAnything 则允许输入图像以及可选 intrinsics、poses、depth 或 partial reconstructions，并输出 metric scene geometry 和 cameras @mapanything。它们共同说明，近期 3R 已经从“预测一个重建结果”扩展到“同时预测多个视觉几何变量”。

Pow3R 对这个趋势给出另一个角度：许多应用并非完全无先验，camera、scene、dense/sparse depth 等信息可能部分存在 @pow3r。合理使用这些先验可以降低重建难度，但先验错误会引入新的失败模式。因此，prior-aware 3R 不能只写成“使用更多信息”，还应写清先验来源、可信度和冲突处理。

#figure(
  thick-table(
    (1.1fr, 1.25fr, 1.35fr, 1.65fr),
    [问题], [代表模型], [核心输出], [综述判断],
    [图像对几何], [DUSt3R, MASt3R], [pointmap, confidence, matches], [3R 表示起点；MASt3R 侧重 matching。],
    [稀疏/多视角], [Fast3R, MV-DUSt3R+], [multi-view reconstruction], [从 pairwise 成本转向 many-view 或 single-stage 组织。],
    [统一视觉几何], [VGGT, MapAnything], [camera, depth, pointmap, tracks, metric geometry], [把多个 3D 视觉变量放入同一 feed-forward 框架。],
    [可选先验], [Pow3R, G-CUT3R], [prior-guided reconstruction], [需要同时记录先验收益和先验冲突。],
  ),
  caption: [从图像对到统一视觉几何的主线。粗线分组强调输入条件和输出表示，而不是按模型名排序。],
)

= 动态场景与 4D：静态 pointmap 的边界

视频输入首先引入时间一致性问题。Align3R 把单目深度估计和 DUSt3R 式对齐联系起来，用于动态视频中的 aligned monocular depth @align3r。Depth Anything、Depth Anything V2、Depth Pro 和 Metric3D v2 提供了强单帧深度或 metric depth 先验 @depth_anything @depth_anything_v2 @depth_pro @metric3dv2，但单帧深度强并不等于跨帧 3D 一致性强。这里需要区分 depth prior 和 3R reconstruction。

动态场景的核心难点在于，运动物体会破坏“静态场景 + 相机运动”的假设。MonST3R 通过动态数据 fine-tuning，把 pointmap 表示推进到 presence of motion 场景 @monst3r。POMATO 将 pointmap matching 与 temporal motion 结合 @pomato；D^2USt3R 输出 static-dynamic aligned 4D pointmaps @d2ust3r；Easi3R 通过推理时 attention adaptation 做 training-free motion disentanglement @easi3r；RayMap3R 则利用 RayMap/image 分支差异识别并抑制动态区域对 streaming memory 的干扰 @raymap3r。

这些方法不应被写成一个“动态版 DUSt3R”集合。MonST3R 偏动态训练，POMATO 偏 matching 与 motion，D^2USt3R 偏 4D pointmap，Easi3R 偏 training-free attention adaptation，RayMap3R 偏 inference-time dynamic suppression。它们都处理动态，但机制、输出和应用代价不同。

#figure(
  thick-table(
    (1fr, 1.45fr, 1.35fr, 1.65fr),
    [方法], [动态机制], [输出], [边界],
    [MonST3R], [动态数据 fine-tuning + per-timestep geometry], [geometry, masks, confidence], [motion-aware geometry，不等于长期物体身份记忆。],
    [POMATO], [pointmap matching + temporal motion], [dynamic reconstruction cues], [强调 matching 与 motion。],
    [D^2USt3R], [static-dynamic aligned pointmaps], [4D pointmaps], [4D pointmap 不是 4DGS 资产。],
    [Easi3R], [training-free attention adaptation], [motion disentanglement, 4D dense point map], [动态修正机制，不作为本文中心。],
    [RayMap3R], [RayMap/image contrast + dynamic suppression], [dynamic-aware streaming reconstruction], [适合讨论动态区域对 memory update 的影响。],
  ),
  caption: [动态 3R 机制对照。表格只比较机制和输出，不形成性能排名。],
)

= 长序列：状态、记忆与缓存治理

长序列 3R 的问题不是简单“处理更多帧”。如果历史信息压缩过强，模型会遗忘早期几何；如果历史信息无限增长，计算和显存会失控；如果动态物体被写入静态记忆，后续地图会被污染。因此，长序列方法的关键在于状态、记忆和缓存的治理。

CUT3R 以 persistent recurrent state 支持连续 3D perception @cut3r。这种 state 是压缩的 latent state，不是可以任意写入和空间查询的数据库。Spann3R 使用 external spatial memory 预测全局 pointmap @spann3r，Point3R 进一步引入 explicit spatial pointer memory @point3r。STream3R 和 LongStream 将 sequential reconstruction 放进 causal / autoregressive framework，并关注 session、cache refresh 或 gauge-decoupled streaming @stream3r @longstream。

LONG3R、LoGeR 和 Mem3R 把长上下文问题拆得更细。LONG3R 强调 memory gating、pruning 和 3D spatio-temporal memory @long3r；LoGeR 使用 hybrid memory，把 parametric TTT memory 与 sliding-window attention 结合 @loger；Mem3R 把 tracking 和 mapping memory 解耦 @mem3r。OVGGT、PAS3R、FILT3R 则分别从 constant-cost cache、pose-adaptive update 和 Kalman-style latent filtering 的角度治理状态更新 @ovggt @pas3r @filt3r。

#figure(
  thick-table(
    (1.2fr, 1.75fr, 2fr),
    [机制类型], [代表方法], [要点],
    [Recurrent state], [CUT3R, STream3R], [状态随观测更新，计算线性或近似线性；不等同于空间数据库。],
    [Spatial / pointer memory], [Spann3R, Point3R], [按空间或指针保存历史几何，需要讨论写入、查询和遗忘。],
    [Hybrid memory], [LONG3R, LoGeR, Mem3R], [本地/全局、tracking/mapping、parametric/non-parametric 轴线不同。],
    [Cache / update / filtering], [OVGGT, PAS3R, FILT3R, LongStream], [关注固定预算、更新增益、滤波和长程漂移。],
  ),
  caption: [长序列 3R 的四类状态机制。粗线边框强调这些术语不可互换。],
)

= 测试时机制：一致性、更新与先验引导

测试阶段的机制可以分为三类。第一类是一致性学习。Test3R 使用图像三元组生成共享参考图像下的两组重建，并通过 prompt tuning 最大化 cross-pair geometric consistency @test3r。它不是简单的评分器，而是 test-time consistency learning。

第二类是状态更新。TTT3R 从 long-sequence recurrent memory update 的角度讨论 test-time training，使用 observation-memory alignment confidence 推导更新率 @ttt3r。它和 Test3R 都发生在测试阶段，但一个偏局部 triplet consistency，一个偏长序列 memory update。

第三类是先验引导。G-CUT3R 让 CUT3R 接收 depth、camera calibration 或 camera positions 等辅助信息 @gcut3r；MASt3R-SfM 则通过 learned matching、retrieval 和 global SfM alignment 提供更传统的全局一致性路径 @mast3r_sfm。对应用系统来说，这三类机制可以互补，但需要记录额外计算、先验错误和更新失败的风险。

= 输出表示与应用证据

3R 论文中的输出不等于应用产物。应用端需要可查看、可比较、可记录的结果：深度图、点云、confidence map、相机轨迹、失败区域、mesh、Gaussian、新视角渲染和报告表格。Pointmap 是中间几何表示，不能直接替代这些产物。

3D Gaussian Splatting 提供了实时可渲染表示 @gaussian_splatting_3d，4DGS 和 4D-Rotor-GS 扩展到动态场景渲染 @gaussian_splatting_4d @rotor_4dgs。Splatt3R、InstantSplat 和 NoPoSplat 则把 pose-free 或 sparse-view 3R 前端与 Gaussian 输出连接起来 @splatt3r @instantsplat @noposplat。它们对演示和应用很重要，但可视化吸引力不能自动转化为几何质量结论；许可证、权重、依赖、输入视角和本地复现状态必须单独记录。

#figure(
  thick-table(
    (1.2fr, 1.55fr, 1.7fr, 1.6fr),
    [输出目标], [代表方法], [可见产物], [证据要求],
    [几何中间量], [DUSt3R, VGGT, CUT3R], [pointmap, depth, camera, tracks], [需要 confidence、一致性和输入条件记录。],
    [动态几何], [MonST3R, D^2USt3R, RayMap3R], [dynamic mask, 4D pointmap, dynamic-aware reconstruction], [需要区分静态/动态区域和时序漂移。],
    [测试时修正], [Test3R, TTT3R, G-CUT3R], [consistency signal, updated state, guided reconstruction], [需要记录额外计算、更新规则和先验来源。],
    [可渲染资产], [Splatt3R, InstantSplat, NoPoSplat, 3DGS, 4DGS], [Gaussian, NVS, 4D preview], [需要许可证、依赖、视角条件和失败样本。],
  ),
  caption: [从 3R 输出到应用证据的转换。表中“证据要求”用于防止把 demo 效果写成质量裁决。],
)

= 支撑先验：不要喧宾夺主

Depth Anything / V2、Depth Pro 和 Metric3D v2 能提供强深度或 metric geometry 先验 @depth_anything @depth_anything_v2 @depth_pro @metric3dv2；DINOv2 / DINOv3 能提供 robust visual features @dinov2 @dinov3；CoTracker、SpatialTracker 和 SAM 2 能提供点跟踪、3D-aware tracking 和视频分割线索 @cotracker @spatialtracker @sam2。这些先验对动态区域识别、匹配、尺度约束和失败分析有价值，但它们不是 3R 模型本身。本文把它们放在条件输入、辅助特征或外部证据的位置。

= 讨论：3R 综述的关键判断

第一，模型比较必须先看 input regime。图像对、稀疏多视角、many-view、streaming video、dynamic video 和 asset output 是不同问题。第二，输出表示必须分开：pointmap、depth、camera、tracks、memory state、mesh 和 Gaussian 不能混作一个指标。第三，时间机制必须拆开：recurrent state、spatial memory、hybrid memory、KV/cache、pose-adaptive update 和 Kalman-style filtering 不是同义词。第四，应用判断必须独立于论文指标：代码、权重、许可证、依赖、推理时间、失败区域和报告产物都需要单独记录。

从这个角度看，近期 3R 方向还没有一个可以覆盖所有输入的单一答案。更稳妥的路线是建立 regime-aware 模型卡：先判断输入条件，再选择模型族，随后用 confidence、一致性、动态区域、先验冲突和失败样本记录结果。这样的框架不替代论文实验，但能减少应用端把模型误用到不匹配场景的风险。

= 局限与结论

本文是一篇叙述性综述，不是带完整检索式、排除记录和统计图的 PRISMA systematic review。本文覆盖 DUSt3R、MASt3R、Fast3R、VGGT、MapAnything、CUT3R、Spann3R、MonST3R、Test3R、Gaussian 输出和若干 2026 年长序列方法，但不能声称穷尽所有相关论文。所有性能、SOTA、代码可用性和应用可行性判断，都应回到原论文实验、官方仓库、许可证和本地复现记录中逐项确认。

总体而言，DUSt3R 之后的 3R 谱系已经从单一 pointmap reconstruction 扩展为多分支生态：matching 分支强化 correspondence，多视角分支追求统一视觉几何，动态分支处理 motion 对静态假设的破坏，长序列分支治理状态和记忆，测试时分支引入一致性学习和先验引导，Gaussian 分支把几何结果推向可渲染资产。理解这一领域的关键，不是寻找一个绝对最强模型，而是理解不同方法的输入假设、输出表示和失败边界。

#pagebreak(weak: true)
= 参考文献
#bibliography("bib.yaml", style: "american-psychological-association", title: none)
