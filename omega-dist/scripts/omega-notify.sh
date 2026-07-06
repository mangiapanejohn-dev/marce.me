#!/bin/bash
# ø 通知：专属 ø 通知器优先（带 ø logo + -group 聚合），fallback terminal-notifier → osascript
# 用法: omega-notify.sh [标题] [内容] [dialog]
#   第三个参数传 dialog 时，额外弹一个 **常驻悬浮对话框**（不点按钮永不消失，
#   完全不依赖通知中心的 横幅/提醒 设置）——周五 weekly scan 成功时用它保证不被错过。
#
# ⚠️ 常驻要求（一次性手动设置，脚本无法代劳——macOS 只允许用户手动改）：
#   系统设置 → 通知 → terminal-notifier → 通知样式选 **"提醒(Alerts)"**。
#   横幅(Banners,默认)几秒自动消失；提醒(Alerts)常驻到手动关闭。
#   没装 terminal-notifier 时 fallback 到 osascript（App 显示为"脚本编辑器"，同理可设 Alerts）。
#   通知只是提示，不是事实源——真正的状态在 .omega/status.json，
#   SessionStart 钩子(omega-remind.sh)与 /omega 都会读它兜底。
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGO="$REPO_ROOT/assets/omega-logo.png"
# 专属 ø 通知器（左侧小图标=ø）：由 scripts/build-omega-notifier.sh 构建
OMEGA_NOTIFIER="$HOME/Applications/omega-notifier.app/Contents/MacOS/terminal-notifier"

TITLE="${1:-ø Weekly Scan complete}"
MESSAGE="${2:-New reference path is ready. Open Claude Code and run /omega resume weekly.}"
MODE="${3:-}"

if [ -x "$OMEGA_NOTIFIER" ]; then
  "$OMEGA_NOTIFIER" \
    -title "$TITLE" \
    -message "$MESSAGE" \
    -sound default \
    -group "omega-weekly" \
    -contentImage "$LOGO"
elif command -v terminal-notifier >/dev/null 2>&1; then
  if [ -f "$LOGO" ]; then
    terminal-notifier \
      -title "$TITLE" \
      -message "$MESSAGE" \
      -sound default \
      -group "omega-weekly" \
      -appIcon "$LOGO" \
      -contentImage "$LOGO"
  else
    terminal-notifier \
      -title "$TITLE" \
      -message "$MESSAGE" \
      -sound default \
      -group "omega-weekly"
  fi
elif command -v notify-send >/dev/null 2>&1; then
  # Linux（untested——ø 原生长在 macOS 上，此分支为发布版尽力适配）
  if [ -f "$LOGO" ]; then
    notify-send -i "$LOGO" "$TITLE" "$MESSAGE"
  else
    notify-send "$TITLE" "$MESSAGE"
  fi
else
  osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\""
fi

# ── 常驻对话框（dialog 模式）：前台阻塞直到点击，零系统设置依赖 ──
# ⚠️ 必须前台跑：后台(&)会在父进程/launchd job 退出时被连带杀掉，框就"自己消失"了。
#   脚本会停在这里等点击（这是特性）。
# 顺序：上面的系统通知先弹，2 秒后悬浮框再出现（带详细内容）。
# 关闭开关：若只想要系统通知（前提：系统设置→通知→ø 已设为"提醒"常驻），
#   运行 `touch .omega/notify-dialog-off` 即可跳过悬浮框；删除该文件恢复。
# 首选 swiftDialog（~/Applications/Dialog.app，右上角+置顶+PNG图标+markdown 内容），
# fallback 到 osascript display dialog（只能居中）。
if [ "$MODE" = "dialog" ] && [ ! -f "$REPO_ROOT/.omega/notify-dialog-off" ]; then
  sleep 2
  SWIFT_DIALOG="$HOME/Applications/Dialog.app/Contents/MacOS/Dialog"
  ICNS="$HOME/Applications/omega-notifier.app/Contents/Resources/Terminal.icns"
  if [ -x "$SWIFT_DIALOG" ]; then
    # 延迟激活兜底：headless 启动时窗口可能不到前台（--small/--timer 组合曾直接不渲染，勿加回）
    ( sleep 2; osascript -e 'tell application "Dialog" to activate' >/dev/null 2>&1 ) &
    "$SWIFT_DIALOG" \
      --title "$TITLE" \
      --message "$MESSAGE" \
      --icon "$LOGO" \
      --button1text "知道了" \
      --position topright \
      --ontop \
      --moveable \
      --width 420 --height 360 \
      >/dev/null 2>&1 || true
  elif [ -f "$ICNS" ]; then
    osascript -e "display dialog \"$MESSAGE\" with title \"$TITLE\" buttons {\"知道了\"} default button 1 with icon POSIX file \"$ICNS\" giving up after 86400" >/dev/null 2>&1 || true
  else
    osascript -e "display dialog \"$MESSAGE\" with title \"$TITLE\" buttons {\"知道了\"} default button 1 giving up after 86400" >/dev/null 2>&1 || true
  fi
fi
