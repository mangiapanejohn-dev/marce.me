#!/bin/bash
# 构建专属"ø 通知器"：克隆 terminal-notifier.app → 换 ø 图标/改名/改 bundle id → ad-hoc 重签名
# 产物: ~/Applications/omega-notifier.app（通知左侧小图标 = ø logo，App 名显示为 ø）
# 为什么需要它：macOS Big Sur+ 不允许 -appIcon 修改通知左侧图标，只能换发送方 App 本身的图标。
# 重跑安全（幂等）：每次全量重建。
set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGO="$REPO_ROOT/assets/omega-logo.png"
APP_DIR="$HOME/Applications"
APP="$APP_DIR/omega-notifier.app"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

[ -f "$LOGO" ] || { echo "❌ 找不到 logo: $LOGO"; exit 1; }
command -v terminal-notifier >/dev/null 2>&1 || { echo "❌ 请先 brew install terminal-notifier"; exit 1; }

# 1. 定位原版 terminal-notifier.app
SRC_APP="$(find -L "$(brew --prefix terminal-notifier)" -maxdepth 3 -name 'terminal-notifier.app' | head -1)"
[ -n "$SRC_APP" ] || { echo "❌ 找不到 terminal-notifier.app"; exit 1; }
echo "源: $SRC_APP"

# 2. logo → icns
ICONSET="$WORK/omega.iconset"
mkdir -p "$ICONSET"
for SZ in 16 32 128 256 512; do
  sips -z $SZ $SZ "$LOGO" --out "$ICONSET/icon_${SZ}x${SZ}.png" >/dev/null
  DBL=$((SZ * 2))
  sips -z $DBL $DBL "$LOGO" --out "$ICONSET/icon_${SZ}x${SZ}@2x.png" >/dev/null
done
iconutil -c icns "$ICONSET" -o "$WORK/omega.icns"
echo "icns 生成 ✅"

# 3. 克隆 + 换皮
mkdir -p "$APP_DIR"
rm -rf "$APP"
cp -R "$SRC_APP" "$APP"
PLIST="$APP/Contents/Info.plist"
ICON_NAME="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIconFile' "$PLIST" 2>/dev/null || echo Terminal.icns)"
case "$ICON_NAME" in *.icns) ;; *) ICON_NAME="$ICON_NAME.icns" ;; esac
cp "$WORK/omega.icns" "$APP/Contents/Resources/$ICON_NAME"
/usr/libexec/PlistBuddy -c 'Set :CFBundleIdentifier me.marcyy.omega-notifier' "$PLIST"
/usr/libexec/PlistBuddy -c 'Set :CFBundleName ø' "$PLIST"
/usr/libexec/PlistBuddy -c 'Add :CFBundleDisplayName string ø' "$PLIST" 2>/dev/null \
  || /usr/libexec/PlistBuddy -c 'Set :CFBundleDisplayName ø' "$PLIST"

# 4. ad-hoc 重签名（改过资源必须重签，否则拒绝运行）
codesign --force --deep --sign - "$APP"
echo "重签名 ✅"

# 5. 刷新图标缓存 + 冒烟
touch "$APP"
"$APP/Contents/MacOS/terminal-notifier" \
  -title "ø 通知器已就位" \
  -message "左边这个图标现在应该是 ø 了。去 系统设置→通知→ø 设为 提醒(Alerts)。" \
  -sound default -group "omega-weekly" -contentImage "$LOGO" || {
    echo "⚠️ 首次发送失败——若被 Gatekeeper 拦截，跑: xattr -dr com.apple.quarantine \"$APP\""; exit 1; }

echo "✅ 完成: $APP"
echo "→ 新 App 身份 = 新的通知设置项：系统设置→通知→ø → 样式选 提醒(Alerts)（需重新设一次）"
