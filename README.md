# Claude Code 設定同步

兩台電腦（公司 / 筆電）的 Claude Code 設定同步 repo。

## 目錄結構

```
claude/
  CLAUDE.md              <- 工作流程指令（最重要）
  RTK.md                 <- Token 工具設定
  settings.json          <- Claude Code 行為設定（含 hooks）
  installed_plugins.json <- 已安裝的 plugins

memory/
  MEMORY.md              <- 記憶索引
  user_profile.md
  project_*.md

context/
  about-me.md            <- 個人設定
  lessons-learned.md
```

## 同步流程

### 推送（修改後）
```bash
cd Claude-workspace/claude-config-sync
git add .
git commit -m "sync: 更新設定"
git push
```

### 拉取（另一台電腦）
```bash
git pull
```
然後手動複製需要的檔案到對應位置（見下方）。

## 套用到本機的路徑對應

| repo 檔案 | 套用到（公司電腦） | 套用到（筆電，路徑請自行確認） |
|-----------|-----------------|-------------------------------|
| `claude/CLAUDE.md` | `D:\Company\Users\edward.yg.APEXGRP\.claude\CLAUDE.md` | `~\.claude\CLAUDE.md` |
| `claude/RTK.md` | `D:\Company\Users\edward.yg.APEXGRP\.claude\RTK.md` | `~\.claude\RTK.md` |
| `claude/settings.json` | `D:\Company\Users\edward.yg.APEXGRP\.claude\settings.json` | 需修改路徑後再套用 |
| `claude/installed_plugins.json` | `.claude\plugins\installed_plugins.json` | 需修改 installPath 後套用 |
| `memory/*.md` | `.claude\projects\<機器名>\memory\` | 同左（路徑不同） |
| `context/*.md` | `_context\` | `_context\` |

## 注意事項

### settings.json 路徑問題
settings.json 內的 hooks 有硬寫路徑，筆電套用前需修改：
- 把 `D:\\Company\\Users\\edward.yg.APEXGRP\\` 換成筆電的實際路徑

### installed_plugins.json 路徑問題
`installPath` 也是硬寫的，筆電套用前需修改 installPath。
建議筆電直接用 Claude Code 重新安裝 plugin（`/install-plugin superpowers`），不要直接複製。

### memory/ 套用路徑
公司電腦的 memory 路徑含機器名稱：
`D:\Company\Users\edward.yg.APEXGRP\.claude\projects\D--Company-Users-edward-yg-APEXGRP\memory\`

筆電的路徑會不同，需確認後再套用。
