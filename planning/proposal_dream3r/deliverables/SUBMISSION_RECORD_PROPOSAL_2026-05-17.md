# 开题报告提交记录 SUBMISSION_RECORD_PROPOSAL_2026-05-17

```yaml
submission_metadata:
  submission_date: 2026-05-17
  recipient: __<填入导师姓名 / 或学院/系联系人>__
  channel: __<email | IM(微信/钉钉) | school_portal | offline_print | other>__
  submitted_by: __<作者署名>__
  contact: __<邮箱>__

primary_deliverable:
  filename: proposal_external_v1_2026-05-17.pdf
  relative_path: Dream/planning/proposal_dream3r/deliverables/proposal_external_v1_2026-05-17.pdf
  pdf_sha256: 78078609F35CA69E6F8F86140B6938BB22F4EBF00FD72D3AB99E61A08414A09E
  pdf_sha256_computed_at: 2026-05-17 (PowerShell Get-FileHash -Algorithm SHA256; read-only operation, did not modify the PDF)
  page_count: __<填入实际页数>__
  word_count_approx: 15000
  section_count: 9
  compile_method: pandoc 3.9 + xelatex (MiKTeX) + SimSun CJK font
  compile_status: exit code 0; 6 missing-glyph warnings (↔ U+2194 in SimSun, cosmetic only)
  ref_pool: 44 (references.bib, shared with Track B survey; not all cited inline in current draft)
  figure_count: 0 (text-only advisor review copy; figures deferred to revision cycle if needed)

accompanying_documents:
  cover_note: SUBMISSION_PACKAGE_ADVISOR_PROPOSAL_2026-05-17.md   # 与 PDF 同包提交
  source_markdown: DRAFT_EXTERNAL_V1.md                           # 仅留档, 不随 PDF 外发

vocabulary_firewall_verification:
  scope: SUBMISSION_PACKAGE_ADVISOR_PROPOSAL_2026-05-17.md
  forbidden_pattern: "cycle|SPEC-|DEC-|CR-[0-9]|agent|skill|workflow|本地项目"
  grep_method: ripgrep case-insensitive
  last_verified: 2026-05-17
  result: 0 hits (clean)
  dream3r_firewall:
    forbidden_pattern: "Dream3R"
    grep_method: ripgrep case-insensitive
    last_verified: 2026-05-17
    result: 0 hits (clean)

submission_action:
  status: pending_user_action
  note: >
    实际提交动作 (email / IM / portal / offline_print) 由用户在 cycle 042 之后执行。
    用户完成提交后回填 recipient / channel / submitted_by / contact / submitted_at 字段。
  submitted_at: __<填入实际提交时间>__
```

---

## Checklist

- [x] PDF file generated and SHA256 computed
- [x] Cover note drafted (vocab-clean pending verification)
- [x] G3a vocab firewall grep on cover note: 0 hits
- [x] G3b Dream3R grep on cover note: 0 hits
- [ ] Page count filled in
- [ ] Recipient and channel filled in (user action)
- [ ] Actual submission executed (user action)
