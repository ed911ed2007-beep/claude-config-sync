#!/bin/bash
set -e

echo "=== 確認 Node.js ==="
if ! node --version 2>/dev/null; then
  echo "Node.js 尚未就緒，等待..."
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 5
    node --version 2>/dev/null && break
  done
fi
node --version
npm --version

echo "=== 安裝 Claude Code ==="
npm install -g @anthropic-ai/claude-code 2>&1 | tail -5

echo "=== 建立 .claude 目錄結構 ==="
mkdir -p /home/edward/.claude/agents
mkdir -p /home/edward/.claude/skills/ai-news-digest
mkdir -p /home/edward/.claude/skills/worklog

echo "=== 套用共用 settings ==="
cp /home/edward/claude-config/settings.json /home/edward/.claude/settings.json

echo "=== 套用 WSL 本機 settings ==="
cp /home/edward/claude-config/settings.local.template.wsl.json /home/edward/.claude/settings.local.json
sed -i 's/<wsl_user>/edward/g' /home/edward/.claude/settings.local.json

echo "=== 同步 CLAUDE.md / RTK.md ==="
cp /home/edward/claude-config/CLAUDE.md /home/edward/.claude/CLAUDE.md
cp /home/edward/claude-config/RTK.md /home/edward/.claude/RTK.md

echo "=== 同步 agents ==="
cp /home/edward/claude-config/agents/*.md /home/edward/.claude/agents/

echo "=== 同步 skills ==="
cp /home/edward/claude-config/skills/ai-news-digest/SKILL.md /home/edward/.claude/skills/ai-news-digest/
cp /home/edward/claude-config/skills/worklog/SKILL.md /home/edward/.claude/skills/worklog/

echo ""
echo "=== 安裝完成！驗證結果 ==="
echo "Claude Code 版本："
claude --version 2>/dev/null || echo "（需重開 terminal 才能使用 claude 指令）"
echo ""
echo ".claude 目錄內容："
ls -la /home/edward/.claude/
echo ""
echo "agents 數量："
ls /home/edward/.claude/agents/ | wc -l
echo ""
echo "settings.json 路徑檢查（不應出現 Company 或 edward.yg）："
grep -E "Company|edward\.yg|D:\\\\" /home/edward/.claude/settings.json && echo "警告：有硬編碼路徑！" || echo "✅ 通過：無硬編碼路徑"
echo ""
echo "settings.local.json wsl_user 替換確認："
grep "edward" /home/edward/.claude/settings.local.json | head -3
