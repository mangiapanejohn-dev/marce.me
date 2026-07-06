#!/bin/bash
# ø / Omega installer — Marc's personal meta-cognition layer for Claude Code
#   macOS : full install (skills + agents + Friday launchd + persistent notifications)
#   Linux : best-effort (skills + agents + cron + notify-send)  [untested — feedback welcome]
#   Windows: use install.ps1 instead (skills + agents only)
# Usage:  curl -fsSL https://marcyy.me/omega/install.sh | bash
# Env  :  OMEGA_DIR=<where scripts land, default ~/omega>   OMEGA_BASE_URL=<override download host>
set -eu

BASE_URL="${OMEGA_BASE_URL:-https://marcyy.me/omega}"
OMEGA_DIR="${OMEGA_DIR:-$HOME/omega}"
CLAUDE_DIR="$HOME/.claude"
OS="$(uname -s)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

say()  { printf '%s\n' "$*"; }
ask()  { # ask <prompt> — returns 0 for yes; auto-no when no usable tty (piped install stays non-interactive-safe)
  { printf '%s [y/N] ' "$1" > /dev/tty; } 2>/dev/null || return 1
  { read -r REPLY < /dev/tty; } 2>/dev/null || return 1
  case "$REPLY" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

say ""
say "  ø / Omega — symbiotic meta-cognition layer for Claude Code"
say "  /omega thinks with Marc. /omega-update grows the Brain. Friday keeps ø alive."
say ""
case "$OS" in
  Darwin) say "  Detected macOS — full install available." ;;
  Linux)  say "  Detected Linux — best-effort install [untested — feedback welcome]." ;;
  *)      say "  Unsupported OS: $OS (on Windows, use: irm ${BASE_URL}/install.ps1 | iex)"; exit 1 ;;
esac

say ""
say "── ① Downloading bundle ($(curl -fsSL "$BASE_URL/VERSION" 2>/dev/null || echo unknown)) ──"
curl -fsSL "$BASE_URL/omega.tar.gz" -o "$TMP/omega.tar.gz"
tar -xzf "$TMP/omega.tar.gz" -C "$TMP"
SRC="$TMP/omega-dist"
[ -f "$SRC/skills/omega/SKILL.md" ] || { say "❌ bundle looks broken"; exit 1; }

say "── ② Installing skills + agents into ~/.claude ──"
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"
for SK in omega omega-update; do
  if [ -d "$CLAUDE_DIR/skills/$SK" ]; then
    rm -rf "$CLAUDE_DIR/skills/$SK.bak"
    mv "$CLAUDE_DIR/skills/$SK" "$CLAUDE_DIR/skills/$SK.bak"
    say "  existing skill '$SK' backed up to $SK.bak"
  fi
  cp -R "$SRC/skills/$SK" "$CLAUDE_DIR/skills/$SK"
done
cp "$SRC"/agents/omega-*.md "$CLAUDE_DIR/agents/"
say "  skills: /omega /omega-update   agents: 7x omega-* council"

say "── ③ Installing scripts to ${OMEGA_DIR} ──"
mkdir -p "$OMEGA_DIR"
cp -R "$SRC/scripts" "$SRC/launchd" "$OMEGA_DIR/"
cp "$SRC/README-OMEGA.md" "$SRC/example-settings.json" "$SRC/VERSION" "$OMEGA_DIR/"
chmod +x "$OMEGA_DIR/scripts/"*.sh

say "── ④ Weekly automation (Friday 21:30) ──"
if [ "$OS" = "Darwin" ]; then
  if ask "  Install launchd agent for the Friday scan now?"; then
    bash "$OMEGA_DIR/scripts/install-omega-launchd.sh" || say "  ⚠️ launchd install failed — run it manually later"
  else
    say "  skipped — install later with: bash ${OMEGA_DIR}/scripts/install-omega-launchd.sh"
  fi
  say "  optional persistent notifications: brew install terminal-notifier && bash ${OMEGA_DIR}/scripts/build-omega-notifier.sh"
  say "  then: System Settings → Notifications → ø → set style to Alerts"
else
  CRON_LINE="30 21 * * 5 /bin/bash \"$OMEGA_DIR/scripts/omega-weekly.sh\""
  if ask "  Add a Friday 21:30 crontab entry?"; then
    ( crontab -l 2>/dev/null | grep -v omega-weekly ; echo "$CRON_LINE" ) | crontab -
    say "  crontab added [untested on Linux — feedback welcome]"
  else
    say "  skipped — add later with: crontab -e  →  $CRON_LINE"
  fi
fi

say ""
say "✅ ø installed."
say "   NOTE: this is Marc's personal system shared as-is — the /omega skill assumes"
say "   his knowledge-base layout (an Obsidian vault named 'Marc Brain'). Read"
say "   ${OMEGA_DIR}/README-OMEGA.md and adapt paths/structure to your own brain."
say "   Try:  /omega        (in Claude Code)"
say "   Undo: rm -rf ~/.claude/skills/omega ~/.claude/skills/omega-update ~/.claude/agents/omega-*.md ${OMEGA_DIR}"
