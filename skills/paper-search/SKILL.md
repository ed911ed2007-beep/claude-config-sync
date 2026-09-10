---
name: paper-search
description: Use when searching academic papers from arxiv or Semantic Scholar by topic and date range. Covers query construction, rate-limit handling, result parsing, and outputting a candidate list for user review.
---

# 學術論文搜尋 Skill

## 概覽

透過 arxiv API 搜尋論文候選清單，結果依日期排序，以結構化表格呈現供使用者選擇。

**核心原則**：直接查詢資料庫 API，不靠模型記憶生成論文資訊（防幻覺）。

---

## 搜尋流程

### 第一步：組合搜尋關鍵字

arxiv API 支援欄位限定與布林運算：

| 語法 | 說明 | 範例 |
|------|------|------|
| `ti:keyword` | 標題搜尋 | `ti:small+language+model` |
| `all:keyword` | 全文搜尋 | `all:SLM` |
| `+AND+` | 且 | `ti:SLM+AND+all:edge` |
| `+OR+` | 或 | `all:SLM+OR+all:phi` |

**SLM / 地端語言模型** 建議查詢組合：
```
all:small+language+model+AND+all:SLM
all:on-device+language+model
all:edge+inference+language+model
ti:SLM+AND+ti:deployment
```

### 第二步：呼叫 arxiv API（Python 版，支援指數退避）

**優先使用 Python 腳本**，PowerShell 缺乏原生重試機制且 IP 限速恢復較慢：

```python
# search_papers.py
import urllib.request
import xml.etree.ElementTree as ET
import time, sys

NS = "http://www.w3.org/2005/Atom"

def search_arxiv(query: str, max_results: int = 20, since: str = "2025-01-01") -> list[dict]:
    url = (
        f"https://export.arxiv.org/api/query"
        f"?search_query={query}"
        f"&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                root = ET.fromstring(resp.read())
            papers = []
            for entry in root.findall(f"{{{NS}}}entry"):
                date = entry.find(f"{{{NS}}}published").text[:10]
                if date < since:
                    continue
                arxiv_id = entry.find(f"{{{NS}}}id").text.split("/abs/")[-1]
                authors = [a.find(f"{{{NS}}}name").text
                           for a in entry.findall(f"{{{NS}}}author")[:2]]
                abstract = entry.find(f"{{{NS}}}summary").text.strip()[:200] + "..."
                papers.append({
                    "date": date,
                    "title": " ".join(entry.find(f"{{{NS}}}title").text.split()),
                    "authors": ", ".join(authors),
                    "id": arxiv_id,
                    "pdf": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                    "abstract": abstract,
                })
            return papers
        except Exception as e:
            wait = 15 * (2 ** attempt)   # 15s → 30s → 60s
            print(f"[警告] 第 {attempt+1} 次失敗：{e}，等待 {wait}s 後重試")
            time.sleep(wait)
    return []

queries = [
    "all:small+language+model+AND+all:SLM",
    "ti:small+language+model+AND+all:edge",
    "all:on-device+language+model",
    "all:on-premise+LLM",
]

seen, results = set(), []
for q in queries:
    print(f"搜尋中：{q}")
    for p in search_arxiv(q, max_results=15):
        if p["id"] not in seen:
            seen.add(p["id"])
            results.append(p)
    time.sleep(10)   # 查詢間隔

# 依日期排序，取最新 10 筆
results.sort(key=lambda x: x["date"], reverse=True)
for i, p in enumerate(results[:10], 1):
    print(f"\n[{i}] {p['date']} — {p['title']}")
    print(f"    作者: {p['authors']}")
    print(f"    ID:   {p['id']}")
    print(f"    PDF:  {p['pdf']}")
    print(f"    摘要: {p['abstract']}")
```

執行方式：
```powershell
python D:\Company\Users\edward.yg.APEXGRP\.claude\skills\paper-search\search_papers.py
```

### 第四步：輸出候選表格

```powershell
$i = 1
$candidates | ForEach-Object {
    Write-Host "[$i] $($_.Date) — $($_.Title)"
    Write-Host "    作者: $($_.Authors)"
    Write-Host "    ID:   $($_.ArxivID)"
    Write-Host "    PDF:  $($_.PDF)"
    Write-Host "    摘要: $($_.Abstract)"
    Write-Host ""
    $i++
}
```

---

## 常見問題排查

| 症狀 | 原因 | 處理方式 |
|------|------|----------|
| HTTP 429 | 請求過於頻繁 | 在每次查詢前 `Start-Sleep -Seconds 5` |
| 結果為空 | 關鍵字太嚴格 | 改用 `all:` 取代 `ti:`，或拆成單字 |
| XML 解析失敗 | API 回傳 HTML 錯誤頁 | 確認 URL 是否正確，印出 `$r.Content` 前 200 字元檢查 |
| 日期篩選無效 | arxiv API 不支援 server-side 日期過濾 | 用 `Where-Object` 在 client 端過濾 |

---

## 後續步驟

搜尋完成後，此 skill 輸出候選清單。後續可接：
- **citation-verify skill**（驗證論文真實存在）：逐筆開啟 `https://arxiv.org/abs/{ID}` 確認標題/作者匹配
- **paper-download skill**（依使用者選擇下載 PDF）
