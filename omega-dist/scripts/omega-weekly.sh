#!/bin/bash
# ø Weekly Omega Scan
# 周五 21:30 由 launchd 触发（me.marcyy.marcbrain.omega-weekly），也可手动运行。
# 用法: omega-weekly.sh [--dry-run]
#   --dry-run: 走完整链路（锁/状态流转/brief占位/通知）但不调用 claude、不 commit、不烧 token，结束后状态还原 idle。
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VAULT="🧠 Marc Brain 2"
OMEGA_DIR="$REPO_ROOT/$VAULT/_omega"
RUNTIME="$REPO_ROOT/.omega"
STATUS_FILE="$RUNTIME/status.json"
LAST_RUN_FILE="$RUNTIME/last-run.json"
LOCK_DIR="$RUNTIME/omega-weekly.lock"
LOG_FILE="$RUNTIME/logs/weekly.log"
WEEK_ID="$(date +%G-%V)"                       # ISO 年-周，如 2026-28
BRIEF_FILE="$OMEGA_DIR/inbox/weekly/${WEEK_ID}-omega-brief.md"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

mkdir -p "$RUNTIME/logs" "$OMEGA_DIR/logs" "$OMEGA_DIR/inbox/weekly"
cd "$REPO_ROOT" || exit 1

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG_FILE"; }

log_event() { # log_event <event> <detail>
  printf '{"ts":"%s","source":"omega-weekly.sh","event":"%s","detail":"%s"}\n' \
    "$(date -u +%FT%TZ)" "$1" "$2" >> "$OMEGA_DIR/logs/events.jsonl"
}

set_status() { # set_status <status> <message> [extra_key extra_value]...
  /usr/bin/python3 - "$STATUS_FILE" "$@" <<'PYEOF'
import json, sys
path = sys.argv[1]
try:
    with open(path) as f: data = json.load(f)
except Exception:
    data = {}
data["status"] = sys.argv[2]
data["message"] = sys.argv[3]
extras = sys.argv[4:]
for i in range(0, len(extras) - 1, 2):
    data[extras[i]] = extras[i + 1]
with open(path, "w") as f: json.dump(data, f, ensure_ascii=False, indent=2)
PYEOF
}

update_last_run() { # update_last_run <result>
  /usr/bin/python3 - "$LAST_RUN_FILE" "$1" <<'PYEOF'
import json, sys, datetime
path, result = sys.argv[1], sys.argv[2]
try:
    with open(path) as f: data = json.load(f)
except Exception:
    data = {"runs": 0}
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
data["last_attempt_at"] = now
data["last_result"] = result
data["runs"] = int(data.get("runs", 0)) + 1
if result == "success":
    data["last_success_at"] = now
with open(path, "w") as f: json.dump(data, f, ensure_ascii=False, indent=2)
PYEOF
}

fail() { # fail <detail>
  log "❌ $1"
  log_event "weekly_scan_error" "$1"
  set_status "error" "weekly scan 失败: $1"
  update_last_run "error"
  bash "$REPO_ROOT/scripts/omega-notify.sh" "ø 评估失败" "weekly scan 出错: $1（详见 .omega/logs/weekly.log）"
  rmdir "$LOCK_DIR" 2>/dev/null
  exit 1
}

# ── 锁：防重复运行 ────────────────────────────────────────────
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "已有实例在运行（${LOCK_DIR} 存在），退出"
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

# ── overdue 检测：电脑睡眠错过周五时，本次运行即补跑 ─────────
OVERDUE="$(/usr/bin/python3 - "$LAST_RUN_FILE" <<'PYEOF'
import json, sys, datetime
try:
    with open(sys.argv[1]) as f: last = json.load(f).get("last_success_at", "")
    if not last:
        print("first_run"); sys.exit()
    delta = datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(last)
    print("overdue" if delta.days >= 8 else "on_schedule")
except Exception:
    print("unknown")
PYEOF
)"
log "开始 weekly scan（week=${WEEK_ID}, schedule=${OVERDUE}, dry_run=${DRY_RUN}）"
[ "$OVERDUE" = "overdue" ] && log_event "weekly_scan_overdue" "距上次成功超过8天，本次为补跑"

# ── 幂等：本周 brief 已存在则跳过 ────────────────────────────
if [ -f "$BRIEF_FILE" ] && [ "$DRY_RUN" -eq 0 ]; then
  log "本周 brief 已存在（${BRIEF_FILE}），跳过"
  exit 0
fi

set_status "running_weekly" "weekly scan 运行中（week ${WEEK_ID}）"
log_event "weekly_scan_started" "week=$WEEK_ID dry_run=$DRY_RUN"

if [ "$DRY_RUN" -eq 1 ]; then
  # 占位 brief 写到运行时目录，不污染 vault
  DRY_BRIEF="$RUNTIME/logs/${WEEK_ID}-omega-brief.dry-run.md"
  printf '# ø Weekly Brief (dry-run 占位)\n\nweek: %s\n生成于: %s\n\n真实运行时此文件会由 /omega weekly-scan 生成到 _omega/inbox/weekly/。\n' \
    "$WEEK_ID" "$(date '+%F %T')" > "$DRY_BRIEF"
  log "dry-run: 占位 brief → $DRY_BRIEF"
  bash "$REPO_ROOT/scripts/omega-notify.sh" "ø 评估完成 (dry-run)" "链路测试通过。真实运行将生成周报并等待 /omega resume weekly。"
  set_status "idle" "dry-run 完成（$(date '+%F %T')），状态已还原"
  log_event "weekly_scan_dry_run_ok" "week=$WEEK_ID"
  update_last_run "dry-run"
  log "dry-run 完成 ✅"
  exit 0
fi

# ── 真实运行：headless 调用 /omega weekly-scan ────────────────
export PATH="$HOME/.claude/local:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
CLAUDE_BIN="$(command -v claude || true)"
[ -z "$CLAUDE_BIN" ] && fail "找不到 claude CLI（PATH=${PATH}）"

log "调用: claude -p '/omega weekly-scan'（受 .claude/settings.json allowlist 约束）"
if ! "$CLAUDE_BIN" -p "/omega weekly-scan" --max-turns 60 >> "$LOG_FILE" 2>&1; then
  fail "claude -p 退出码非 0"
fi

# ── 验收：brief 必须真实生成 ─────────────────────────────────
[ -f "$BRIEF_FILE" ] || fail "claude 运行结束但未生成 $BRIEF_FILE"

set_status "pending_dialogue" "周报已生成，等待 /omega resume weekly" \
  "last_weekly_scan" "$(date '+%F %T')" \
  "latest_brief" "$VAULT/_omega/inbox/weekly/${WEEK_ID}-omega-brief.md"
log_event "weekly_scan_completed" "brief=${WEEK_ID}-omega-brief.md"
update_last_run "success"

# ── 提交 ø 记忆（.omega/ 已 gitignore；post-commit hook 自动 push）──
git add "$VAULT/_omega" && git commit -m "ø weekly scan: $WEEK_ID brief 生成" >> "$LOG_FILE" 2>&1 \
  || log "⚠️ git commit 失败或无变更（不影响 scan 结果）"

log "weekly scan 完成 ✅ brief=$BRIEF_FILE"
# 悬浮框显示 brief 摘要（提取"本周变化摘要"段前几行；提不到就用默认文案）
DIGEST="$(sed -n '/本周变化摘要/,/^## /p' "$BRIEF_FILE" 2>/dev/null | grep -v '^#' | grep -v '^[[:space:]]*$' | head -6)"
MSG="${DIGEST:-New reference path is ready.}

**运行 /omega resume weekly 开始进化对话**"
# 注意：dialog 模式会阻塞到 Marc 点击（常驻保证）；一切收尾已完成，挂在这里是安全的
bash "$REPO_ROOT/scripts/omega-notify.sh" "ø Weekly Scan complete" "$MSG" dialog
