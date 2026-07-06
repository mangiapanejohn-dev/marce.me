#!/bin/bash
# 打印 ø 当前状态（人话版）。status.json 缺失时按默认值重建。
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATUS_FILE="$REPO_ROOT/.omega/status.json"

if [ ! -f "$STATUS_FILE" ]; then
  mkdir -p "$REPO_ROOT/.omega/logs"
  cat > "$STATUS_FILE" <<'EOF'
{
  "status": "idle",
  "last_weekly_scan": "",
  "latest_brief": "",
  "latest_pending_update": "",
  "last_synced_at": "",
  "message": "status.json 缺失，已自动重建"
}
EOF
  echo "⚠️  status.json 不存在，已重建为 idle"
fi

get() { /usr/bin/python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get(sys.argv[2],''))" "$STATUS_FILE" "$1"; }

STATUS="$(get status)"
echo "ø 状态: $STATUS"
echo "  上次 weekly scan : $(get last_weekly_scan)"
echo "  最新 brief       : $(get latest_brief)"
echo "  待合并 update    : $(get latest_pending_update)"
echo "  上次落库         : $(get last_synced_at)"
echo "  说明             : $(get message)"

case "$STATUS" in
  pending_dialogue) echo "→ 下一步: 在 Claude Code 输入 /omega resume weekly" ;;
  pending_update)   echo "→ 下一步: 在 Claude Code 输入 /omega-update" ;;
  error)            echo "→ 查看 .omega/logs/ 与 _omega/logs/events.jsonl" ;;
esac
