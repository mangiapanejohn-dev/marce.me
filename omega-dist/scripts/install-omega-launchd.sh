#!/bin/bash
# 安装 ø 周五自动扫描的 LaunchAgent
# 用法: install-omega-launchd.sh [--dry-run]
set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL="me.marcyy.marcbrain.omega-weekly"
TEMPLATE="$REPO_ROOT/launchd/$LABEL.plist"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

[ -f "$TEMPLATE" ] || { echo "❌ 模板不存在: $TEMPLATE"; exit 1; }

RENDERED="$(sed -e "s|__REPO_ROOT__|$REPO_ROOT|g" -e "s|__HOME__|$HOME|g" "$TEMPLATE")"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "── dry-run：将安装到 $TARGET ──"
  echo "$RENDERED"
  echo "── dry-run：随后执行 launchctl bootstrap gui/$(id -u) $TARGET ──"
  exit 0
fi

mkdir -p "$HOME/Library/LaunchAgents" "$REPO_ROOT/.omega/logs"

# 已装则先卸载旧的（幂等）
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  echo "已存在旧的 ${LABEL}，先卸载"
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
fi

echo "$RENDERED" > "$TARGET"
plutil -lint "$TARGET"
launchctl bootstrap "gui/$(id -u)" "$TARGET"

echo "✅ 已安装并启用: ${LABEL}（每周五 21:30）"
launchctl print "gui/$(id -u)/$LABEL" | grep -E "state|program" | head -5 || true
echo "验证: launchctl list | grep $LABEL"
echo "卸载: bash scripts/uninstall-omega-launchd.sh"
