#!/bin/bash
# ƒ installer — 14 style modes for Claude Code (pure prompts, no scripts, no dependencies)
# Usage:  curl -fsSL https://marcyy.me/ƒ/install.sh | bash
# Env  :  SKILLS_BASE_URL=<override download host>   CLAUDE_HOME=<override ~/.claude>
set -eu

BASE_URL="${SKILLS_BASE_URL:-https://marcyy.me/ƒ}"
CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PERSISTENT="godmode artifacts eli5 ghost brief nocode silent ooda step"
ONESHOT="devil roast matrix why steal"
SKILLS="$PERSISTENT $ONESHOT"

say() { printf '%s\n' "$*"; }

say ""
say "  ƒ — 14 style modes for Claude Code"
say "  9 persistent modes + 5 one-shot analyses. One SKILL.md each, zero dependencies."
say ""

say "── ① Downloading bundle ($(curl -fsSL "$BASE_URL/VERSION" 2>/dev/null || echo unknown)) ──"
curl -fsSL "$BASE_URL/skills.tar.gz" -o "$TMP/skills.tar.gz"
tar -xzf "$TMP/skills.tar.gz" -C "$TMP"
SRC="$TMP/skills-dist"
[ -f "$SRC/skills/godmode/SKILL.md" ] || { say "❌ bundle looks broken"; exit 1; }

say "── ② Installing into $CLAUDE_DIR/skills ──"
mkdir -p "$CLAUDE_DIR/skills"
BACKED_UP=""
for SK in $SKILLS; do
  [ -f "$SRC/skills/$SK/SKILL.md" ] || { say "❌ missing '$SK' in bundle"; exit 1; }
  if [ -d "$CLAUDE_DIR/skills/$SK" ]; then
    rm -rf "$CLAUDE_DIR/skills/$SK.bak"
    mv "$CLAUDE_DIR/skills/$SK" "$CLAUDE_DIR/skills/$SK.bak"
    BACKED_UP="$BACKED_UP $SK"
  fi
  cp -R "$SRC/skills/$SK" "$CLAUDE_DIR/skills/$SK"
done
cp "$SRC/README-SKILLS.md" "$CLAUDE_DIR/skills/README-SKILLS.md"
[ -z "$BACKED_UP" ] || say "  existing skills backed up to <name>.bak:$BACKED_UP"

say ""
say "✅ ƒ installed — 14 modes."
say ""
say "   persistent · /godmode  /artifacts  /eli5   /ghost  /brief"
say "                /nocode   /silent     /ooda   /step"
say "   one-shot   · /devil    /roast      /matrix /why    /steal"
say ""
say "   /xxx           turn the mode on for the rest of the session"
say "   /xxx [thing]   apply it once, without entering the mode"
say "   modes stack — say \"关闭 xxx\" / \"turn off xxx\" to drop one"
say ""
say "   Reference: $CLAUDE_DIR/skills/README-SKILLS.md"
say "   Undo: rm -rf $CLAUDE_DIR/skills/{$(echo $SKILLS | tr ' ' ',')}"
