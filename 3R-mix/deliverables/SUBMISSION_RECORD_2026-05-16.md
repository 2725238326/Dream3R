# 综述提交记录 SUBMISSION_RECORD_2026-05-16

```yaml
submission_metadata:
  submission_date: 2026-05-16
  recipient: __<填入导师姓名 / 或学院/系联系人>__
  channel: __<email | IM(微信/钉钉) | school_portal | offline_print | other>__
  submitted_by: __<作者署名>__
  contact: __<邮箱>__

primary_deliverable:
  filename: 3r_survey_stage_final_2026-05-15_natural.pdf
  relative_path: Dream/3R-mix/deliverables/3r_survey_stage_final_2026-05-15_natural.pdf
  pdf_sha256: A0763DB7AB7A1E8E1427D4DCC8CB62BC15F94F3F2D915AD0BFBB235CC99C64B0
  pdf_sha256_computed_at: 2026-05-16 (PowerShell Get-FileHash -Algorithm SHA256; read-only operation, did not modify the PDF)
  page_count: 18
  ref_count: 44
  figure_count: 6
  figure_breakdown: 4 TikZ self-drawn + 2 paper Fig.1 composites
  table_count: 5
  table_format: booktabs
  compile_status: 0 errors / 0 warnings (ctexart + xelatex + unsrtnat)
  time_window_covered: 2024-01 ~ 2026-05

accompanying_documents:
  cover_note: SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md   # 与 PDF 同包提交
  internal_meta: RELATION_TO_TRACK_A_2026-05-16.md       # 不与 PDF 同包，内部留档

vocabulary_firewall_verification:
  scope: SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md
  forbidden_pattern: Dream|Dream3R|KYKT|agent|skill|workflow|本地项目|cycle|SPEC-|DEC-|CR-
  grep_method: ripgrep case-insensitive
  last_verified: 2026-05-16
  result: 0 hits (clean)
  manuscript_firewall: 同方法 grep on main.tex 历史上多次 0 hits（见 work_log）；本次提交未修改 main.tex 故沿用既有验证

publication_route:
  selected: route C (arXiv self-archiving, no venue submission)
  rationale: 时效优先 + 综述工作的核心价值在于把握 2026 年中节点的方法分布
  date_locked: 2026-05-14 (manuscript wound down to this route)

post_submission_actions_pending:
  - 用户实际执行提交动作（email / 上传 / 当面）
  - 提交完成后回填 recipient + channel + submitted_by + contact 字段（pdf_sha256 已于 2026-05-16 预填）
  - 提交后等待导师 / 学校反馈；如有实质性内容反馈则启动新的修订 cycle

audit_chain:
  predecessor: 2026-05-15 prose naturalization pass (10 paragraphs rewritten)
  predecessor_artifact: 3r_survey_stage_final_2026-05-15_natural.pdf
  current_artifact: this file + SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md
  successor: pending advisor feedback (out of cycle scope)
```

---

## 提交动作 checklist（用户执行时填写）

- [x] 计算 PDF SHA256 并回填到上方 `pdf_sha256` 字段（已于 2026-05-16 预填，SHA256 = A0763DB7AB7A1E8E1427D4DCC8CB62BC15F94F3F2D915AD0BFBB235CC99C64B0）
  - PowerShell 命令：`Get-FileHash -Algorithm SHA256 .\3r_survey_stage_final_2026-05-15_natural.pdf`
  - 如重新生成 PDF 需重算并替换上方 SHA256
- [ ] 决定提交渠道（email / IM / portal / offline），回填到 `channel` 字段
- [ ] 填写导师姓名 / 学院联系人到 `recipient` 字段
- [ ] 填写作者署名 + 邮箱到 `submitted_by` + `contact` 字段
- [ ] 准备提交邮件 / 信件正文（可复用 `SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` §六请求审阅事项 段落）
- [ ] 附件：PDF + cover note
- [ ] 实际发送 / 上传 / 当面交付
- [ ] 在本文件追加 "submitted_at: YYYY-MM-DD HH:MM" 字段（提交完成时间）
- [ ] 在本文件追加 "ack_received: yes/no" 字段（导师确认收到）

---

## 备注

- `RELATION_TO_TRACK_A_2026-05-16.md` 不与 PDF 同包提交。它是项目内部留档，说明本综述与主线研究的关系；提交给导师的材料仅包含 PDF + cover note 两件。
- 本提交记录文件本身保存在 `Dream/3R-mix/deliverables/` 目录下，作为提交动作的审计锚点；不主动提交给导师。
