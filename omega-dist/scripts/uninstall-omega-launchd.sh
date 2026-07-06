#!/bin/bash
# 卸载 ø 周五自动扫描的 LaunchAgent
set -eu

LABEL="me.marcyy.marcbrain.omega-weekly"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null && echo "已停止 $LABEL" || echo "$LABEL 未在运行"
[ -f "$TARGET" ] && rm "$TARGET" && echo "已删除 $TARGET" || echo "$TARGET 不存在"
echo "✅ 卸载完成（repo 内模板保留，可随时重装）"
