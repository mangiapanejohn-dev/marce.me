#!/usr/bin/env bash
#
# Render every research figure from its Mermaid source into public/research/.
#
#   scripts/research/<name>.mmd  ->  public/research/<name>.svg
#                                    public/research/<name>-dark.svg
#
# The .mmd files carry no %%{init}%% block on purpose: the palette lives in
# theme-light.json / theme-dark.json, so one source renders both variants and a
# palette change is one edit rather than one per diagram. Backgrounds are
# transparent — the page ground shows through, in either theme.
#
# Embed the pair in a post or page with:
#
#   <img class="fig-light" src="/research/<name>.svg" alt="..." />
#   <img class="fig-dark"  src="/research/<name>-dark.svg" alt="" aria-hidden="true" />
#
# The swap rule lives in src/styles/global.css.
#
# Usage: scripts/render-figures.sh [name ...]     (no args = all)

set -euo pipefail

cd "$(dirname "$0")/.."

SRC_DIR="scripts/research"
OUT_DIR="public/research"
MMDC=(npx -y @mermaid-js/mermaid-cli@11)

mkdir -p "$OUT_DIR"

if [ $# -gt 0 ]; then
  sources=()
  for name in "$@"; do
    sources+=("$SRC_DIR/${name%.mmd}.mmd")
  done
else
  sources=("$SRC_DIR"/*.mmd)
fi

if [ ! -e "${sources[0]}" ]; then
  echo "no .mmd sources in $SRC_DIR" >&2
  exit 1
fi

for src in "${sources[@]}"; do
  name="$(basename "$src" .mmd)"

  if grep -q '%%{init' "$src"; then
    echo "$name: has its own %%{init}%% block — remove it, the theme comes from $SRC_DIR/theme-*.json" >&2
    exit 1
  fi

  for variant in light dark; do
    case "$variant" in
      light) out="$OUT_DIR/$name.svg" ;;
      dark) out="$OUT_DIR/$name-dark.svg" ;;
    esac

    "${MMDC[@]}" \
      --input "$src" \
      --output "$out" \
      --configFile "$SRC_DIR/theme-$variant.json" \
      --backgroundColor transparent \
      --quiet

    echo "$out"
  done
done
