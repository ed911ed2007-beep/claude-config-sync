---
name: ai-gateway 多模型 AI 平台專案
description: 用 Ollama + LiteLLM + Open WebUI 建立統一 AI 模型交換台，整合地端與雲端模型
type: project
---

## 專案目標
建立 `ai-gateway/` 目錄，以 LiteLLM 為代理層，統一管理以下模型：
- 地端：Ollama（gemma3:4b 已確認可用）
- 雲端：OpenAI GPT-4o、Google Gemini 2.0、Anthropic Claude

**Why:** 讓現有專案（尤其 rag_work_src_openai）只改一個 baseURL 就能自由切換任意模型，不被單一廠商鎖定。

**How to apply:** 下次繼續時，直接填 .env API Keys 然後 `docker compose up -d`。

## 進度狀態（2026-04-17）
- ✅ 架構規劃完成
- ✅ Ollama 正常（gemma3:4b 可用）
- ✅ Docker v27.4.0 正常
- ✅ `ai-gateway/` 目錄與四個核心設定檔已建立
- [ ] 尚未填入 API Keys（OpenAI / Gemini / Anthropic）
- [ ] 尚未執行 `docker compose up -d`
- [ ] 尚未執行 test_models.py 驗證

## 目錄結構（已建立）
```
ai-gateway/
├── .env.example       ✅ 已建
├── .env               ← 待填入 API keys
├── litellm_config.yaml ✅ 已建
├── docker-compose.yml  ✅ 已建
└── test_models.py      ✅ 已建
```

## 架構
```
Open WebUI (localhost:3000)
        │
        ▼
LiteLLM Proxy (localhost:8000)
        ├── ollama/gemma3:4b     → localhost:11434
        ├── openai/gpt-4o        → api.openai.com
        ├── gemini/gemini-2.0    → generativelanguage.googleapis.com
        └── anthropic/claude-*   → api.anthropic.com
```

## 下次繼續時的步驟
1. `cp .env.example .env`，填入 API Keys
2. `docker compose up -d`
3. `python test_models.py`
4. 開 http://localhost:3000 確認 Open WebUI

## 整合現有專案
rag_work_src_openai 只需改：
```javascript
baseURL: "http://localhost:8000/v1"
```
