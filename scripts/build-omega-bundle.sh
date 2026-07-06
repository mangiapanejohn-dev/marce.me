#!/bin/bash
# 构建 ø / Omega 发布包：从活体源刷新 omega-dist/ → 打包 public/omega/{omega.tar.gz,omega.zip} → 写 VERSION
# ø 进化后发新版：跑本脚本 → git commit + push → Vercel 自动部署
# 源：全局 ~/.claude/skills|agents（skill 活体） + Marc-Brain-2 repo scripts/launchd/assets/README-OMEGA
set -eu

SITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRAIN_ROOT="$HOME/Desktop/🧠 Marc Brain 2"
DIST="$SITE_ROOT/omega-dist"
PUB="$SITE_ROOT/public/omega"
VERSION="$(date +%Y.%m.%d)"

[ -d "$BRAIN_ROOT/scripts" ] || { echo "❌ 找不到 Marc-Brain-2: $BRAIN_ROOT"; exit 1; }
[ -f "$HOME/.claude/skills/omega/SKILL.md" ] || { echo "❌ 找不到全局 omega skill"; exit 1; }

echo "── ① 刷新 omega-dist/（源 → 快照）──"
rm -rf "$DIST"
mkdir -p "$DIST/skills/omega" "$DIST/skills/omega-update" "$DIST/agents" "$DIST/scripts" "$DIST/launchd"

cp "$HOME/.claude/skills/omega/SKILL.md"        "$DIST/skills/omega/SKILL.md"
cp "$HOME/.claude/skills/omega-update/SKILL.md" "$DIST/skills/omega-update/SKILL.md"
cp "$HOME"/.claude/agents/omega-*.md            "$DIST/agents/"
for S in omega-weekly.sh omega-notify.sh omega-status.sh omega-remind.sh \
         install-omega-launchd.sh uninstall-omega-launchd.sh build-omega-notifier.sh; do
  cp "$BRAIN_ROOT/scripts/$S" "$DIST/scripts/$S"
done
cp "$BRAIN_ROOT/launchd/me.marcyy.marcbrain.omega-weekly.plist" "$DIST/launchd/"
cp "$BRAIN_ROOT/README-OMEGA.md"       "$DIST/README-OMEGA.md"
cp "$BRAIN_ROOT/.claude/settings.json" "$DIST/example-settings.json"
echo "$VERSION" > "$DIST/VERSION"

echo "── ② 纯净检查：绝不打包 _omega 数据 ──"
if grep -rl 'behavior_patterns\|deprecated_edges' "$DIST" >/dev/null 2>&1; then
  echo "❌ 疑似混入模型/图谱数据"; exit 1
fi
find "$DIST" -name '*.yaml' -o -name '*.jsonl' | grep -q . && { echo "❌ 混入 yaml/jsonl 数据文件"; exit 1; }
echo "纯净 ✅（仅 skill/agents/脚本/plist/README/示例配置）"

echo "── ③ 打包 ──"
mkdir -p "$PUB"
tar -czf "$PUB/omega.tar.gz" -C "$SITE_ROOT" omega-dist
( cd "$SITE_ROOT" && rm -f "$PUB/omega.zip" && zip -qr "$PUB/omega.zip" omega-dist )
echo "$VERSION" > "$PUB/VERSION"
cp "$BRAIN_ROOT/assets/omega-logo.png" "$PUB/omega-logo.png"

echo "✅ VERSION=$VERSION"
ls -la "$PUB"