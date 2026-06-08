# Dream3R 中期报告写作风格说明

日期：2026-06-08

## 采用的论文叙述方式

本轮写作参考本地 3R 论文的常见表达结构，但不复制论文原句。DUSt3R、Fast3R、Spann3R、VGGT 和 Test3R 的引言基本遵循同一条线：先说明多视图三维重建是长期核心问题，再指出传统 SfM/MVS 级联流程的复杂性，然后引入 pointmap 或 feed-forward reconstruction 范式，最后落到一个具体瓶颈，例如 pairwise 输入、全局对齐、空间记忆、几何属性统一预测或测试时一致性。

Dream3R 的报告也应按这个方式写：先进入问题，不先喊口号；先解释已有方法解决了什么，再解释它们留下了什么空缺；最后把 Dream3R 收束为一个具体、可检验的阶段贡献。

## 当前应避免的口吻

以下表达容易显得像内部工程看板或 AI 总结，不适合放进中期报告正文：

```text
全链路闭环
赋能
保驾护航
核心抓手
系统性推进
全面优化
打造平台
模型安全边界
我们不能 claim
该模块作为后续可扩展抓手
不是 X，而是 Y
```

报告正文应改用更自然的学术表达，例如：

```text
本文研究的问题是……
该结果表明……
实验并不能说明……
因此，本阶段暂不将该分支纳入官方模型……
该设计聚焦于 proposal bank 上的状态条件化融合……
```

## Dream3R 当前推荐表述

推荐：

```text
Dream3R 当前是状态条件化 proposal-fusion 3R 模型。它将多个 3R teacher
的输出组织为 proposal bank，并利用 Dream state、候选冲突和场景域信息进行融合。
```

不推荐：

```text
Dream3R 已经是完整 proposal-free 3R foundation model。
Qwen 语义显著提升几何。
VGGT-Omega 就是 Dream3R 主体。
```

## 写作主线

中期报告正文应围绕以下顺序展开：

```text
传统 3R 流程复杂
-> DUSt3R/VGGT 等前馈式 3R 改变问题形式
-> 现有模型在不同场景域上分化
-> Dream3R 研究 proposal bank 上的状态条件化融合
-> v1.1.0 给出当前可运行模型包与 state/no-state/shuffle 对照
-> proposal-free、Qwen、Foundation3R 作为负结果或后续路线诚实保留
```

这个顺序比“我们做了哪些模块”的写法更像论文，也更容易解释当前模型的阶段性价值。
