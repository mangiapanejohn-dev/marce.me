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

    # Preserve the spaces mermaid puts at tspan boundaries.
    #
    # With htmlLabels off, a wrapped label becomes <tspan>the</tspan><tspan> proposal</tspan> — the
    # space is there, and SVG's default xml:space="default" strips leading whitespace inside a
    # tspan, so it renders as "theproposal". Every renderer does this; it is the spec, not a bug in
    # one of them. `xml:space="preserve"` on the <text> keeps them.
    #
    # htmlLabels stays off on purpose: with it on the labels go inside <foreignObject>, which is not
    # rendered when an SVG is referenced from <img>, and every figure here is embedded that way.
    python3 - "$out" <<'PYFIX'
import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = re.sub(r'<text(?![^>]*xml:space)', '<text xml:space="preserve"', s)

# Give the root a real intrinsic size.
#
# mermaid writes width="100%" and puts the pixel cap only in an inline style. Referenced from
# <img> that leaves no usable intrinsic width, so the browser stretches the figure to the
# container and scales the type up with it — a 579px diagram rendered at 768px and shouting.
# width/height from the viewBox make <img> use the natural size; max-width:100% still shrinks it
# on a narrow screen.
NUM = r'[-+]?[0-9.]+'
m = re.match(r'<svg\b[^>]*>', s)
if m:
    root = m.group(0)
    vb = re.search(r'viewBox="\s*(%s)\s+(%s)\s+(%s)\s+(%s)\s*"' % (NUM, NUM, NUM, NUM), root)
    if vb:
        w, h = round(float(vb.group(3))), round(float(vb.group(4)))
        new_root = re.sub(r'\s(?:width|height)="[^"]*"', '', root)
        new_root = new_root.replace('<svg', '<svg width="%d" height="%d"' % (w, h), 1)
        s = new_root + s[m.end():]
open(p, "w", encoding="utf-8").write(s)
PYFIX

    echo "$out"
  done
done
