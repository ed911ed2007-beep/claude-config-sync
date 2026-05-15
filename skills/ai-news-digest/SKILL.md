---
name: ai-news-digest
description: ai-news-digest 專案的執行、除錯、修改流程。當使用者要跑 pipeline、修 bug、加功能時使用。
---

# ai-news-digest 專案 Skill

## 專案位置
`D:\Company\Users\edward.yg.APEXGRP\ai-news-digest\`

## 執行 Pipeline

**正確執行方式**（必須加 `-X utf8`，否則 cp950 會炸）：
```powershell
cd D:\Company\Users\edward.yg.APEXGRP\ai-news-digest
python -X utf8 src/main.py
```

> B1 根本修法：在 `src/main.py` 最頂端加 `sys.stdout.reconfigure(encoding='utf-8')`，
> 或讓 Task Scheduler 用環境變數 `PYTHONIOENCODING=utf-8` 呼叫，就不用依賴手動 `-X utf8`。

## 修改程式碼的注意事項

1. **所有 `open()` 必須加 `encoding='utf-8'`**
   ```python
   # 錯誤
   with open(path) as f:
   # 正確
   with open(path, encoding='utf-8') as f:
   ```

2. **API Key 不得出現在程式碼中** — 只從 `settings.json` 讀取，`settings.json` 必須在 `.gitignore`

3. **字串替換不得靜默失敗** — 用 `str.replace()` 前先確認目標字串存在，或用 assert 驗證結果有改變

## 重要檔案
| 檔案 | 用途 |
|------|------|
| `src/main.py` | Pipeline 入口 |
| `settings.json` | API key、設定（勿 commit） |
| `data/wiki/` | Wiki 輸出（勿 commit） |
| `data/rag/manual-overrides.json` | 手動覆寫 |

## 常見錯誤排查

| 症狀 | 原因 | 解法 |
|------|------|------|
| `UnicodeEncodeError: cp950` | stdout 未設定 utf-8 | 加 `-X utf8` 或 `PYTHONIOENCODING=utf-8` |
| entity 頁面沒更新 | `_upsert_entity_page` 找不到錨點字串 | 加錯誤拋出，不要靜默跳過 |
| Haiku 分類降級 | 正常，模型自動 fallback | 忽略 |
| Token 超出預算 | 中文 token 估算用 `len(s)//2`，應改 `len(s.encode('utf-8'))//3` | 修 budget 計算 |

## 完成修改後的自我確認清單
- [ ] 新增/修改的 `open()` 都有 `encoding='utf-8'`
- [ ] 沒有 hardcode API key
- [ ] 錯誤處理不是靜默跳過
- [ ] 在 `ai-news-digest/` 目錄下跑 `python -X utf8 src/main.py` 驗證可執行
