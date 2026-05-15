@RTK.md

# HomePage - Claude Code 運作指南

## 文字管理規則（最重要）
- **禁止把 UI 文字硬編碼**
- 多語系管理: ja / en，分別在 src/i18n/ja.ts / src/i18n/en.ts 管理
- 新增文字時請先加到 ja.ts → 再在 en.ts 做翻譯

## Commit 規則
- 未新增或修改測試代碼的原始碼變更，不要 commit

## 提交前檢查（每次必做）
1. 橫向展開檢查 — 搜尋相同模式並完整處理
2. 安全檢查 — XSS、外部連結 rel 屬性、機密資訊
3. 效能檢查 — 未使用依賴、CSS 重複、打包大小
4. 部署檢查 — npx astro check → npm test → npm run build
