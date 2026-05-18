# 3R-mix survey

LaTeX 中文综述：近期 3R / feed-forward 3D reconstruction 模型的表示、序列机制与应用证据。

## 当前交付

- 推荐版本：`deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`（18 A4 页，44 条参考文献，6 张图，5 张表；2026-05-15 prose naturalization 轮次产出，在 2026-05-14 quality 版基础上重写正文以去掉 LLM 套话和工作流词汇）。
- 主稿：`main.tex`（`ctexart` + `xelatex` + `unsrtnat`）。
- 参考文献：`references.bib`（44 条，全部在正文显式引用）。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex  build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

输出位置：`build/main.pdf`。MiKTeX 在 Windows 11 Home China 上会打印 "running on an unsupported version of Windows" 警告，PDF 正常生成；如换为 TeXLive 可消除该警告。

## 目录约定

- `papers/`、`build/`、`guidance_skills/` 已在 `.gitignore` 中排除；不要把生成 PDF 或第三方论文 PDF 提交进版本控制。
- 任何新增论文截图都需要逐篇确认复用许可证。当前已确认：DUSt3R / VGGT / MonST3R / CUT3R。

## 历史与开发说明

- 阶段终稿已收口；当前规划为 arXiv-only 自存档，不投递期刊或会议。
- 早期 Typst 路线（`main.typ`、`review-template.typ`、`bib.yaml`、`GENERATION_PROMPT.md`）保留为历史快照，不再维护。
- 完整状态、细粒度修改记录与发布前检查清单：`NEW_CHAT_HANDOFF.md`、`notes/work_log.md`。
