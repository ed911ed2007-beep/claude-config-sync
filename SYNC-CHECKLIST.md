# Claude Config Sync — 上傳 / 下載前檢點表

每次 `git push`（上傳）或 `git pull`（下載）前執行。

---

## 上傳前（Push）

### 1. 敏感資料
- [ ] `settings.json` 無 API key / token / password
- [ ] 無 `.env`、`*.key`、`*credential*` 等敏感檔被意外 staged
- [ ] `.gitignore` 仍涵蓋 `*.env`、`*.key`、`*secret*`、`*credential*`

```powershell
# 快速掃描
git diff --cached --name-only
git status
grep -r "api_key\s*=" skills/ --include="*.py"
```

### 2. Skills 完整性
- [ ] 每個 skill 的 `SKILL.md` 有 `name:` 與 `description:` frontmatter
- [ ] Python 工具腳本中所有 `open()` 均有 `encoding='utf-8'`（防 cp950）

```powershell
# frontmatter 檢查
foreach ($f in Get-ChildItem skills\*\SKILL.md) {
    $ok = (Select-String "^name:" $f) -and (Select-String "^description:" $f)
    Write-Host "$($f.FullName) | OK=$ok"
}
# encoding 檢查
Select-String 'open\(' skills\*\*.py -Recurse | Where-Object { $_ -notmatch 'encoding' }
```

### 3. Git 狀態
- [ ] `git status` 確認 staged 檔案符合預期
- [ ] commit message 清楚描述變更內容

---

## 下載後（Pull）

### 1. 路徑調整（跨機器）
- [ ] `claude/settings.json` 的 hooks 路徑已從公司路徑改為本機路徑
  - 公司：`D:\\Company\\Users\\edward.yg.APEXGRP\\`
  - 筆電：確認實際路徑後替換
- [ ] `claude/installed_plugins.json` 的 `installPath` 已調整

### 2. 套用到本機
- [ ] `claude/CLAUDE.md` → `~\.claude\CLAUDE.md`
- [ ] `claude/RTK.md` → `~\.claude\RTK.md`
- [ ] `claude/settings.json` → `~\.claude\settings.json`（路徑修改後）
- [ ] `skills/*` → `~\.claude\skills\`（直接複製或 symlink）
- [ ] `memory/*.md` → `~\.claude\projects\<機器名>\memory\`
- [ ] `agents/*.md` → `~\.claude\agents\`（若支援）

### 3. 安裝驗證
- [ ] 在 Claude Code 輸入 `/skills` 確認新 skill 已載入
- [ ] 執行 `rtk --version` 確認 RTK 正常

---

## 歷史記錄

| 日期 | 方向 | 執行人 | 結果 |
|------|------|--------|------|
| 2026-05-19 | Push | Claude Code (公司) | ✅ 3 skills 推上（bpm-form-manual, hv-analysis, paper-search） |
