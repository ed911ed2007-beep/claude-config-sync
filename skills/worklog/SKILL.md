---
name: worklog
description: 工作日誌管理流程。Session 開始讀取待辦、Session 結束寫入摘要。當使用者說「收工/掰掰/bye/結束/下班」時自動觸發。
---

# 工作日誌 Skill

## 日誌位置
`D:\Company\Users\edward.yg.APEXGRP\Claude-workspace\daily-log\YYYY-MM-DD.md`

---

## Session 開始時（必做）

1. 列出 `Claude-workspace/daily-log/` 下所有 `.md`（排除 `_template.md`）
2. 讀取**最新**的日誌檔
3. 用繁體中文條列顯示：
   - 上次未完成的待辦（`- [ ]`）
   - 進行中的任務（`🔄`）
   - 建議今日優先處理的事項
4. 詢問使用者今天要從哪裡繼續

---

## Session 結束時

**觸發關鍵字**：`收工`、`掰掰`、`bye`、`結束工作`、`下班`、`關掉`、`結束`

### 步驟
1. 確認今天日期，決定檔案名 `YYYY-MM-DD.md`
2. 若當天日誌已存在 → **追加**本次 session 摘要到檔案末尾
3. 若當天日誌不存在 → 參照 `_template.md` 格式**新建**

### 摘要格式
```markdown
## 今日完成 ✅
- ✅ 【專案名】具體完成事項

## 進行中 🔄
- 🔄 【專案名】未完成的事項

## 待辦事項 📋
### 【專案名】
- [ ] 待辦項目（加 **B1/B2** 等優先標記）

## 明日優先事項 🎯
1. 最重要的一件事
2. 次要事項
```

### 格式規範
- 語言：繁體中文
- 待辦用 `- [ ]`，完成用 `- ✅`
- 每個任務標註所屬專案名稱（如 `【ai-news-digest】`）
- 寫完後告知使用者：「日誌已儲存到 `Claude-workspace/daily-log/YYYY-MM-DD.md`」

---

## 模板參考
`Claude-workspace/daily-log/_template.md`
