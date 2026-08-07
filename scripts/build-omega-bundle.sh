#!/bin/bash
# 构建 ø / Omega 发布包：从活体源刷新 omega-dist/ → 打包 public/omega/{omega.tar.gz,omega.zip} → 写 VERSION
# ø 进化后发新版：跑本脚本 → git commit + push → Vercel 自动部署
# 源：全局 ~/.claude/skills|agents（skill 活体） + Marc-Brain-2 repo scripts/launchd/assets/README-OMEGA
set -eu

SITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRAIN_ROOT="$HOME/Desktop/🧠 Marc Brain 2"
DIST="$SITE_ROOT/omega-dist"
PUB="$SITE_ROOT/public/ø"
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

echo "── ④ 同步 ASCII 镜像 public/omega/（Windows 用）──"
# Windows 控制台传统代码页会把粘贴进去的 ø 吃掉，PowerShell 5.1 又会把无 charset
# 的响应按 latin-1 解码搞坏脚本里的非 ASCII 字节 —— 所以 Windows 全链路只能走 ASCII。
PUB_ASCII="$SITE_ROOT/public/omega"
mkdir -p "$PUB_ASCII"
for F in omega.tar.gz omega.zip VERSION install.ps1 install.sh; do
  cp "$PUB/$F" "$PUB_ASCII/$F"
done
if LC_ALL=C grep -q '[^ -~	]' "$PUB/install.ps1"; then
  echo "❌ install.ps1 含非 ASCII 字符，Windows 上会被 latin-1 解码搞坏"; exit 1
fi
echo "ASCII 镜像同步完成 ✅"

echo "✅ VERSION=$VERSION"
ls -la "$PUB" "$PUB_ASCII"