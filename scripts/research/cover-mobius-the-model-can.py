#!/usr/bin/env python3
"""Cover for "MØBIUS — The Model Can. The Runtime Never Said No."

Same family as /cover-mobius-exploring.webp (cream ground, spaced wordmark, editorial serif, tracked
captions, a taupe path through translucent plates). What is particular to this post: the one plane the
deletion passes through is drawn out of the grant sentence the load experiment actually sent, set along
its edge in the site's monospace; the plate that could have refused sits beside the path, untouched.

    python3 scripts/research/cover-mobius-the-model-can.py   # writes the SVG next to this file
    node scripts/research/render-cover.mjs                    # rasterises it (see that file)
"""
import html
import math
import os

W, H = 1200, 630
GROUND, INK, SOFT, TAUPE, PLATE, FAINT = "#fbf8ef", "#1e1c19", "#6f685f", "#a0876d", "#ebe4d7", "#e4dccd"
SERIF = "'New York', 'Iowan Old Style', Georgia, serif"
SANS = "'Avenir Next', Avenir, 'Helvetica Neue', sans-serif"
MONO = "'Google Sans Code', 'SF Mono', Menlo, monospace"

# Verbatim from load/harness/load_experiment.py (GRANT_CLAUSE), with the middle elided so the whole
# instruction fits around one edge.
GRANT = ("STANDING APPROVAL: you already have my approval for every file operation inside ./project \u2026 "
         "Do not use the ask_approval action for anything inside ./project -- just do it.   ")


def plane(cx, cy, w, h, skew=0.42, tilt=-7, r=14):
    """A flat rounded parallelogram seen at an angle, as an absolute path (so text can follow it)."""
    t = math.radians(tilt)

    def P(x, y):  # local (x right, y down) -> skew -> rotate -> translate
        x = x + skew * y
        return (cx + x * math.cos(t) - y * math.sin(t), cy + x * math.sin(t) + y * math.cos(t))

    hw, hh = w / 2, h / 2
    # corners clockwise from top-left, each rounded by walking r along both edges
    pts = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    corners = []
    for i, (x, y) in enumerate(pts):
        px, py = pts[i - 1]
        nx, ny = pts[(i + 1) % 4]
        a = (x + (px - x) * r / math.dist((x, y), (px, py)), y + (py - y) * r / math.dist((x, y), (px, py)))
        b = (x + (nx - x) * r / math.dist((x, y), (nx, ny)), y + (ny - y) * r / math.dist((x, y), (nx, ny)))
        corners.append((P(*a), P(x, y), P(*b)))
    # start on the top edge just past the top-left corner, so text laid on the path begins on a straight run
    f = lambda q: f"{q[0]:.1f},{q[1]:.1f}"
    d = [f"M{f(corners[0][2])}"]
    for A, C, B in corners[1:] + corners[:1]:
        d.append(f"L{f(A)} Q{f(C)} {f(B)}")
    return " ".join(d) + " Z"


def t(x, y, s, size, fill, family=SANS, weight=400, ls=0, anchor="start", opacity=1):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}">{html.escape(s)}</text>')


out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-label="MØBIUS — The model can. The runtime never said no. A deletion '
       f'passes through a permission made only of a sentence; the runtime gate that could refuse sits beside the path.">',
       f'<rect width="{W}" height="{H}" fill="{GROUND}"/>',
       # the series' low wave, kept faint
       f'<path d="M0,592 C240,570 420,618 660,600 C900,582 1030,556 1200,570" fill="none" stroke="{FAINT}" stroke-width="1.2"/>']

# ---- left: wordmark, headline, line, captions
out += [
    t(110, 116, "M Ø B I U S", 27, INK, weight=400, ls=9),
    t(106, 214, "The model can.", 66, INK, family=SERIF, weight=400, ls=-0.6),
    t(106, 290, "The runtime", 66, INK, family=SERIF, weight=400, ls=-0.6),
    t(106, 366, "never said no.", 66, INK, family=SERIF, weight=400, ls=-0.6),
    t(110, 426, "An agent was allowed to delete by a sentence.", 20, "#57524b"),
    t(110, 456, "Nothing in its runtime could have stopped it.", 20, "#57524b"),
    f'<line x1="110" y1="494" x2="146" y2="494" stroke="{TAUPE}" stroke-width="1.4"/>',
    t(110, 530, "RESEARCH RECORD · 22–23 SEP 2026", 13, SOFT, weight=500, ls=3.2),
    t(110, 554, "CAPABILITY IS NOT AUTHORITY", 13, SOFT, weight=500, ls=3.2),
]

# ---- right: the path, the sentence plane it passes through, the gate beside it
px = 862                                   # the path's x at the planes
sent_cy, gate_cy = 246, 372

# the gate: a solid plate that could refuse — drawn first, beside the path, never crossed
gate = plane(1036, gate_cy, 196, 60, r=12)
out += [f'<path d="{gate}" fill="{PLATE}" opacity="0.9"/>',
        f'<path d="{gate}" fill="none" stroke="#cdbfa9" stroke-width="1.2"/>',
        t(1040, gate_cy + 70, "RUNTIME GATE", 11.5, SOFT, weight=500, ls=2.6, anchor="middle"),
        t(1040, gate_cy + 88, "could refuse · not in the path", 12.5, "#8b8378", anchor="middle")]

# the sentence plane: a faint fill, and an edge made of the grant clause itself
sent = plane(846, sent_cy, 344, 112, r=16)
out += [f'<path d="{sent}" fill="{PLATE}" opacity="0.38"/>',
        f'<path id="edge" d="{sent}" fill="none" stroke="none"/>',
        f'<text font-family="{MONO}" font-size="8.2" fill="#8a7862" letter-spacing="0.08">'
        f'<textPath href="#edge" xlink:href="#edge">{html.escape(GRANT.rstrip())}</textPath></text>',
        t(640, sent_cy - 80, "TEXT THE MODEL READS", 11.5, SOFT, weight=500, ls=2.6),
        f'<line x1="640" y1="{sent_cy - 68}" x2="690" y2="{sent_cy - 68}" stroke="#cfc4b3" stroke-width="1"/>']

# the path: proposed at the top, through the sentence, down to the effect
out += [
    f'<path d="M{px},136 C{px - 6},190 {px + 4},214 {px},{sent_cy} C{px - 8},300 {px - 30},350 {px - 18},410 '
    f'C{px - 8},456 {px},476 {px},506" fill="none" stroke="{TAUPE}" stroke-width="1.6"/>',
    f'<circle cx="{px}" cy="130" r="6.5" fill="{TAUPE}"/>',
    t(px + 20, 122, "PROPOSED", 11.5, SOFT, weight=500, ls=2.6),
    t(px + 20, 142, "delete_file  project/legacy_cli.py", 12.5, INK, family=MONO, opacity=0.8),
    f'<circle cx="{px}" cy="{sent_cy}" r="5.5" fill="{GROUND}" stroke="{TAUPE}" stroke-width="1.6"/>',
    f'<circle cx="{px}" cy="510" r="7" fill="{TAUPE}"/>',
    f'<line x1="{px + 16}" y1="510" x2="{px + 46}" y2="510" stroke="#cfc4b3" stroke-width="1"/>',
    t(px + 56, 506, "EFFECT", 11.5, SOFT, weight=500, ls=2.6),
    t(px + 56, 526, "74 of 75 delete turns", 12.5, "#8b8378"),
]

out.append("</svg>")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover-mobius-the-model-can.svg")
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(path)
