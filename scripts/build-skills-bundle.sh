#!/bin/bash
# 构建 ƒ / style modes 发布包：从活体源刷新 skills-dist/ → 打包 public/ƒ/{skills.tar.gz,skills.zip} → 写 VERSION
# 改了任何一个模式发新版：跑本脚本 → git commit + push → Vercel 自动部署
# 源：全局 ~/.claude/skills/<name>/SKILL.md（活体）
set -eu

SITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_ROOT="$HOME/.claude/skills"
DIST="$SITE_ROOT/skills-dist"
PUB="$SITE_ROOT/public/ƒ"
# ASCII mirror. Windows consoles on a legacy code page mangle a pasted "ƒ", and
# PowerShell 5.1 latin-1-decodes any non-ASCII byte in a fetched script, so the
# whole Windows path (typed URL, script body, downloads) must stay ASCII-only.
PUB_ASCII="$SITE_ROOT/public/f"
VERSION="$(date +%Y.%m.%d)"

# 显式白名单 —— 绝不扫目录，否则以后新建的个人 skill 会被自动打进公开包
PERSISTENT="godmode artifacts eli5 ghost brief nocode silent ooda step"
ONESHOT="devil roast matrix why steal"
SKILLS="$PERSISTENT $ONESHOT"
EXPECTED=14

echo "── ① 刷新 skills-dist/（活体源 → 快照）──"
rm -rf "$DIST"
mkdir -p "$DIST/skills"
for S in $SKILLS; do
  [ -f "$SRC_ROOT/$S/SKILL.md" ] || { echo "❌ 找不到活体 skill: $SRC_ROOT/$S/SKILL.md"; exit 1; }
  mkdir -p "$DIST/skills/$S"
  cp "$SRC_ROOT/$S/SKILL.md" "$DIST/skills/$S/SKILL.md"
done
cp "$SITE_ROOT/scripts/README-SKILLS.md" "$DIST/README-SKILLS.md"
echo "$VERSION" > "$DIST/VERSION"
echo "已快照 $(echo $SKILLS | wc -w | tr -d ' ') 个"

echo "── ② 纯净检查 ──"
COUNT="$(find "$DIST/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[ "$COUNT" = "$EXPECTED" ] || { echo "❌ 目录数 $COUNT ≠ 期望 $EXPECTED"; exit 1; }

# 每个 skill 目录里只允许有 SKILL.md
STRAY="$(find "$DIST/skills" -type f ! -name SKILL.md)"
[ -z "$STRAY" ] || { echo "❌ 混入非 SKILL.md 文件:"; echo "$STRAY"; exit 1; }

# 个人信息：绝对家目录路径、Brain vault、桌面路径
if grep -rlE "/Users/|${HOME}|Marc Brain|Desktop/" "$DIST/skills" >/dev/null 2>&1; then
  echo "❌ 疑似混入个人路径:"; grep -rlE "/Users/|${HOME}|Marc Brain|Desktop/" "$DIST/skills"; exit 1
fi

# 疑似密钥
if grep -rlE "sk-[A-Za-z0-9]|api[_-]?key[[:space:]]*[=:]|token[[:space:]]*=" "$DIST/skills" >/dev/null 2>&1; then
  echo "❌ 疑似混入密钥:"; grep -rlE "sk-[A-Za-z0-9]|api[_-]?key[[:space:]]*[=:]|token[[:space:]]*=" "$DIST/skills"; exit 1
fi

# frontmatter 完整性：name 必须与目录名一致
for S in $SKILLS; do
  NAME="$(awk -F': *' '/^name:/{print $2; exit}' "$DIST/skills/$S/SKILL.md")"
  [ "$NAME" = "$S" ] || { echo "❌ $S/SKILL.md 的 name 是 '$NAME'，与目录名不符"; exit 1; }
done
echo "纯净 ✅（$EXPECTED 个目录 · 各一个 SKILL.md · 无个人路径 · 无密钥 · name 与目录名一致）"

echo "── ③ 打包 ──"
mkdir -p "$PUB"
tar -czf "$PUB/skills.tar.gz" -C "$SITE_ROOT" skills-dist
( cd "$SITE_ROOT" && rm -f "$PUB/skills.zip" && zip -qr "$PUB/skills.zip" skills-dist )
echo "$VERSION" > "$PUB/VERSION"

echo "── ④ 同步 ASCII 镜像 public/f/（Windows 用）──"
mkdir -p "$PUB_ASCII"
for F in skills.tar.gz skills.zip VERSION install.ps1 install.sh; do
  cp "$PUB/$F" "$PUB_ASCII/$F"
done
# 安装器必须是纯 ASCII，否则 PowerShell 会把 BaseUrl 解码成乱码
for F in "$PUB/install.ps1" "$PUB_ASCII/install.ps1"; do
  if LC_ALL=C grep -q '[^ -~	]' "$F"; then
    echo "❌ $F 含非 ASCII 字符，Windows 上会被 latin-1 解码搞坏"; exit 1
  fi
done
echo "ASCII 镜像同步完成 ✅"

echo "✅ VERSION=$VERSION"
ls -la "$PUB" "$PUB_ASCII"
