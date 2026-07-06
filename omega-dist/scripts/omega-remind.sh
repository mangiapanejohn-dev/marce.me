#!/bin/bash
# Claude Code SessionStart 钩子：检查 ø 状态，有待办就在会话开头提醒。
# 只读 status.json，不弹系统通知、绝不自动运行 /omega——提醒 Marc，由 Marc 手动开始。
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATUS_FILE="$REPO_ROOT/.omega/status.json"
[ -f "$STATUS_FILE" ] || exit 0

STATUS="$(/usr/bin/python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('status',''))" "$STATUS_FILE" 2>/dev/null)"

case "$STATUS" in
  pending_dialogue)
    echo "ø has a pending weekly brief. Run /omega resume weekly to continue." ;;
  pending_update)
    echo "ø 有一份已达成的共识待合并。Run /omega-update to merge it." ;;
  error)
    echo "ø 上次运行出错（详见 .omega/logs/ 与 _omega/logs/events.jsonl）。" ;;
esac
exit 0
