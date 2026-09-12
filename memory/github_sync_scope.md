# GitHub 同步範圍

使用者於 2026-09-12 明確指定：說「sync github」、「同步 github」或「同步 GitHub 資料」時，預設同步以下三個儲存庫：

- `ed911ed2007-beep/claude-config-sync`：跨電腦 AI agents 共用設定、角色、技能與記憶。
- `ed911ed2007-beep/ai-collaboration-governance`：協作規則、任務、交接與驗證文件。
- `ed911ed2007-beep/mempalace`：共享記憶及其專案。

目的：同步不同電腦 AI agents 之間的差異，讓接手者有一致的設定、規則與記憶。

即使同一句話提到其他專案路徑，仍先同步上述三庫，再接續指定專案；不要把專案路徑誤認成要找其 GitHub remote。

同步時先確認工作樹與遠端差異，保留本機變更，檢閱後合併與推送。機器專用路徑與憑證不可盲目覆寫或上傳。Git repo 同步不等於所有執行中 agents、設定或 MemPalace 索引都已重新載入；回報須區分實際完成的範圍。
