---
name: claw-lmstudio 整合專案
description: 讓 LM Studio 本地 LLM 驅動 claw-code Rust CLI agent，分 Phase A/B 進行
type: project
---

**目標：** 用 LM Studio（Qwen2.5-Coder-7B）取代 Claude API，驅動 claw-code agent harness

**Phase A（快速驗證）：** LiteLLM Proxy 中間層
- `ANTHROPIC_BASE_URL=http://localhost:4000`，零改程式碼
- litellm yaml 把 claude model alias 對應到 LM Studio openai/qwen2.5-coder-7b

**Phase B（正式整合）：** 直接改 Rust API 層
- 新增 `BackendMode` enum（Anthropic / OpenAiCompat）
- 新增 `openai_types.rs`、`openai_compat.rs`
- 修改 `client.rs` 支援雙後端切換

**Why:** EMBA 課程實作題目（中原大學 2nd/Sun），0426 上課要展示
**How to apply:** 下次繼續時先確認 checklist 完成度，從 Phase A 驗證開始

**計劃原檔：** `D:\Edward的資料夾\h.EMBA\中原大學\課程內容\2nd\Sun\0411\0426\claw-lmstudio-plan.md`
**備份：** `D:\Company\Users\edward.yg.APEXGRP\Claude-workspace\claw-lmstudio-plan.md`
**claw-code 原始碼：** `D:\Edward-Laptop\Downloads\claw-code-main\claw-code-main\`
