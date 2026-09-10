---
name: bpm-form-manual
description: Build and update BPM operation-manual decks for the three core forms, enforce Traditional Chinese UTF-8 safety, and create date-stamped backups. Use when users request manual PPT generation, style alignment with reference PPTs, garbled-text diagnosis, or reproducible backup packaging.
---

# BPM Form Manual

## Workflow

1. Resolve source paths under `Documents/BPM/115/專案1`.
2. Confirm the three target forms and two style reference PPT files exist.
3. Generate or update the manual PPT with UTF-8 safe file writing.
4. Validate Chinese text by checking slide XML text nodes in the exported PPTX zip.
5. Create a date-stamped backup folder and copy all deliverables.
6. Summarize outputs with absolute paths and verification results.

## Required Inputs

- Form XML files:
  - `Form_(夆)外訓申請表_*.xml`
  - `Form_(夆)外訓心得報告書_*.xml`
  - `Form_(夆)國內派註地津貼_交通補助申請單_*.xml`
- Style references:
  - `20230705-行政文書作業無紙化管理.pptx`
  - `20230807-BPM訓練-請假+加班(精簡版).pptx`

## UTF-8 Guardrails

- Write scripts/files with explicit UTF-8 encoding.
- Avoid shell stdin pipelines for Chinese-heavy content generation.
- After PPT export, unzip and inspect `ppt/slides/slide*.xml` text nodes.
- If text appears as `?` or mojibake, regenerate from UTF-8 script files.

## Backup Standard

- Backup folder name: `backup_YYYY-MM-DD`.
- Include:
  - final PPTX
  - style baseline notes
  - generation script
  - config/json inputs
  - optional verification log
- Keep previous backups untouched.

## Resources

- Use `scripts/create_backup.ps1` for reproducible date-stamped backup creation.
- Use `references/verification-checklist.md` before final handoff.
