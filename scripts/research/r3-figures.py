#!/usr/bin/env python3
"""Figures for "MØBIUS — What the Judge Was Shown, and What It Kept".

Hand-drawn SVG rather than Mermaid: these are data figures and fixed layouts, not flowcharts a
layout engine should place. One source, two palettes — the same light/dark pair convention as
scripts/render-figures.sh, so the post embeds them as `.fig-light` / `.fig-dark`.

Every number drawn here is re-derived in the post from the MØBIUS evidence directories it names.

    python3 scripts/research/r3-figures.py        # writes public/research/mobius-r3-*.svg
"""
from __future__ import annotations

import html
import os
import re

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "public", "research")

PALETTES = {
    "light": {
        "ink": "#262521", "soft": "#6b6a63", "line": "#4a4842", "faint": "#cfcabb",
        "card": "#f6f3ec", "fill": "#e7e3d7", "accent": "#c4623f", "accentfill": "#f4dfd3",
        "ok": "#3f6b4f", "okfill": "#dfe8dc", "warn": "#9a6a1f", "warnfill": "#f1e6cc",
        "bad": "#9b3a33", "badfill": "#f1d9d4", "blue": "#2f5d7a", "bluefill": "#dce6ee",
    },
    "dark": {
        "ink": "#edebe3", "soft": "#b9b7ad", "line": "#c9c6ba", "faint": "#55534b",
        "card": "#36352f", "fill": "#403f38", "accent": "#e08a6b", "accentfill": "#5a3d31",
        "ok": "#a9c9b1", "okfill": "#34423a", "warn": "#e2c38a", "warnfill": "#4a4131",
        "bad": "#eba59c", "badfill": "#4f3432", "blue": "#9cc3de", "bluefill": "#2f3f4a",
    },
}

SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
SERIF = "'STIX Two Math', 'Cambria Math', Georgia, 'Times New Roman', serif"


def fmt(s: str) -> str:
    """Escape, then turn x_{ab} / x_a and x^{ab} into sub/superscript tspans."""
    s = html.escape(s.replace("`", ""), quote=False)

    def sub(m):
        return f'<tspan baseline-shift="sub" font-size="72%">{m.group(1) or m.group(2)}</tspan>'

    def sup(m):
        return f'<tspan baseline-shift="super" font-size="72%">{m.group(1) or m.group(2)}</tspan>'

    s = re.sub(r"_\{([^}]*)\}|_([A-Za-z0-9*+−\-]+)", sub, s)
    s = re.sub(r"\^\{([^}]*)\}|\^([A-Za-z0-9*]+)", sup, s)
    return s


class Fig:
    def __init__(self, w: int, h: int, title: str, desc: str):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.items: list[str] = []

    def add(self, s: str):
        self.items.append(s)

    def text(self, x, y, s, size=12.5, color="ink", weight=400, anchor="start", family=SANS, italic=False):
        style = ' font-style="italic"' if italic else ""
        self.add(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}"'
            f' fill="{{{color}}}" text-anchor="{anchor}"{style}>{fmt(s)}</text>'
        )

    def lines(self, x, y, rows, size=12.5, color="ink", lh=None, **kw):
        lh = lh or size * 1.42
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, size=size, color=color, **kw)

    def rect(self, x, y, w, h, fill="card", stroke="line", sw=1, rx=8, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{{{fill}}}"'
            f' stroke="{{{stroke}}}" stroke-width="{sw}"{d}/>'
        )

    def line(self, x1, y1, x2, y2, color="line", sw=1.2, dash=None, arrow=False):
        if arrow:  # stop short of the box edge so the head is not drawn under it
            L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 or 1
            x2, y2 = round(x2 - 2 * (x2 - x1) / L, 1), round(y2 - 2 * (y2 - y1) / L, 1)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{{{color}}}" stroke-width="{sw}"{d}/>')
        if arrow:
            self.head(x1, y1, x2, y2, color)

    def head(self, fx, fy, tx, ty, color="line", size=7):
        """An explicit arrowhead at (tx, ty) pointing away from (fx, fy): no <marker>, so every renderer agrees."""
        L = ((tx - fx) ** 2 + (ty - fy) ** 2) ** 0.5 or 1
        ux, uy = (tx - fx) / L, (ty - fy) / L
        bx, by = tx - ux * size, ty - uy * size
        px, py = -uy * size * 0.5, ux * size * 0.5
        pts = f"{tx:.1f},{ty:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}"
        self.add(f'<polygon points="{pts}" fill="{{{color}}}"/>')

    def path(self, d, color="line", sw=1.2, dash=None, arrow=False, fill="none"):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        f = "none" if fill == "none" else f"{{{fill}}}"
        self.add(f'<path d="{d}" fill="{f}" stroke="{{{color}}}" stroke-width="{sw}"{dd}/>')
        if arrow:  # direction from the last control point to the end point
            nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", d)]
            self.head(nums[-4], nums[-3], nums[-2], nums[-1], color)

    def circle(self, cx, cy, r, fill="accent", stroke="accent", sw=1):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{{{fill}}}" stroke="{{{stroke}}}" stroke-width="{sw}"/>')

    def render(self, pal: dict) -> str:
        body = "\n".join(self.items)
        for k, v in pal.items():
            body = body.replace("{" + k + "}", v)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}"'
            f' role="img" aria-labelledby="t d">\n<title id="t">{html.escape(self.title)}</title>\n'
            f'<desc id="d">{html.escape(self.desc)}</desc>\n'
            f"{body}\n</svg>\n"
        )


def save(name: str, fig: Fig):
    os.makedirs(OUT, exist_ok=True)
    for theme, pal in PALETTES.items():
        suffix = "" if theme == "light" else "-dark"
        with open(os.path.join(OUT, f"{name}{suffix}.svg"), "w", encoding="utf-8") as f:
            f.write(fig.render(pal))


# ---------------------------------------------------------------- A · timeline
def fig_timeline():
    rows = [
        ("6 Sep", "Last public post", ["V54–V56: what one binary can actually load."], "soft", False),
        ("6–8 Sep", "A world is declared, not discovered", ["ADR 0014–0019, Probes 1–6. A revision records what", "a provider did; the declared premise was inert."], "line", False),
        ("8–9 Sep", "Human decisions outlive their world", ["V59–V73. An approval is reused across a world", "change; V65 binds it to what it was granted over."], "line", False),
        ("10–12 Sep", "The approval line meets its neighbours", ["VB-1, VB-2, PP-1, OV-1; B1 ratified (approval =", "memoized decision keyed by its premise); K8 repaired."], "line", False),
        ("12–13 Sep", "An unattended mission reports success", ["S-M1/B: a moving world overwritten and called", "complete. ADR 0021–0026."], "line", False),
        ("13–15 Sep", "A real model in the loop (R1)", ["The proposer was blind. ADR 0027–0035; approval", "cells P6b: seven predictions, seven held."], "line", False),
        ("18 Sep", "Completion starts lying (R2)", ["Pilot: checker 0/6, runtime complete 5/6. ADR 0043", "judge: 0 false, and 0/6 completed at all."], "accent", True),
        ("18–19 Sep", "The judge is shown more (R3)", ["ADR 0044/0045, P3: 39 valid rows, 114 judgements,", "74 cannot-tell. P4: Boolean `expected` → no Brier."], "accent", True),
        ("18–19 Sep", "Claims killed; FTR kills itself", ["Approval line → prior art; write-set anticipation", "fails its threshold; FTR retired by its own criteria."], "bad", False),
        ("19 Sep", "This audit", ["The missing past is in the journal, out of view;", "1 unsupported `established`; certificates 0/11 closed."], "accent", True),
        ("now", "Open frontier", ["Which of history, decision basis, possible futures", "and proof obligations become runtime objects?"], "blue", True),
    ]
    W, top, step = 500, 44, 66
    H = top + step * len(rows) + 10
    f = Fig(W, H, "MØBIUS research timeline, 6 to 19 September 2026",
            "From the last public post to the current frontier: declared worlds, approvals bound to premises, "
            "the approval line reduced to prior art, real-model missions, the completion judge, R3, "
            "claims retired in review, and this audit.")
    f.text(16, 24, "6 Sep → 19 Sep 2026 · what happened between the two posts", size=12, color="soft", weight=600)
    x0 = 96
    f.line(x0, top, x0, top + step * (len(rows) - 1) + 8, color="faint", sw=2)
    for i, (d, t, desc, col, strong) in enumerate(rows):
        y = top + i * step
        f.text(x0 - 14, y + 5, d, size=11.5, color="soft", anchor="end", weight=600)
        f.circle(x0, y, 5.5 if strong else 4, fill=col if strong else "card", stroke=col, sw=2)
        f.text(x0 + 16, y + 5, t, size=13, weight=700, color="ink" if col != "bad" else "bad")
        f.lines(x0 + 16, y + 23, desc, size=11.5, color="soft", lh=15.5)
    save("mobius-r3-timeline", f)


# ---------------------------------------------------------------- B · runtime
def fig_runtime():
    W, H = 500, 760
    f = Fig(W, H, "The MØBIUS runtime as it stands at f9b27dd",
            "Model and cognition propose intents, looks and judgements through the model port. The runtime "
            "loop owns authority, routing, world and version binding, observation, execution, verification, "
            "evidence and completion, and the journal. Effects reach the world through environment providers.")
    # model
    f.rect(20, 16, 460, 86, fill="bluefill", stroke="blue")
    f.text(36, 40, "Model / cognition  ·  advisory, never authoritative", size=13, weight=700, color="blue")
    f.lines(36, 62, ["proposer (intent-source) · look (observation-source)",
                     "criterion judge (criterion-judge, ADR 0043) · Claude CLI / OpenAI transports"],
            size=11.5, color="ink", lh=17)
    f.line(250, 108, 250, 132, arrow=True)
    f.rect(120, 132, 260, 50, fill="card")
    f.text(250, 153, "ActionIntent", size=13, weight=700, anchor="middle")
    f.text(250, 171, "desiredEffect · expected · satisfies · parameters", size=11, color="soft", anchor="middle")
    f.line(250, 182, 250, 206, arrow=True)
    # runtime
    f.rect(20, 206, 460, 432, fill="card", stroke="accent", sw=1.6, rx=10)
    f.text(36, 230, "Runtime  ·  runtime-core/loop.ts, owns every consequential decision", size=13, weight=700, color="accent")
    comps = [
        ("authority", "AuthorityGate · approval revalidation · occurrence binding (K8)"),
        ("routing", "reflex + compiler: intent → ActionIR; arguments may route (ADR 0030/0033)"),
        ("world / version", "declared world (ADR 0014) · per-provider revision · basis, stale-basis"),
        ("observation", "one gated door; the runtime looks where the model did not (ADR 0041)"),
        ("execution", "MEP transport → provider session; receipts carry identity"),
        ("verification", "comparator over `expected` · paths.ts resolvePath (dotted, no search)"),
        ("evidence", "#evidenceByCriterion · judge sees binding ∪ run view (ADR 0045)"),
        ("completion", "goal.completed records the binding's evidence only"),
        ("journal", "append-only events; a run re-opens over the journal (ADR 0013)"),
    ]
    y = 256
    for name, d in comps:
        hot = name in ("evidence", "completion")
        f.rect(34, y, 432, 38, fill="accentfill" if hot else "fill", stroke="accent" if hot else "faint", rx=6)
        f.text(46, y + 16, name, size=12, weight=700, color="accent" if hot else "ink")
        f.text(46, y + 31, d, size=10.8, color="soft", family=SANS)
        y += 42
    f.line(250, 638, 250, 662, arrow=True)
    f.rect(20, 662, 460, 80, fill="okfill", stroke="ok")
    f.text(36, 686, "World", size=13, weight=700, color="ok")
    f.lines(36, 706, ["filesystem provider (anchor) · repository provider (witness, asked, never anchored)",
                      "human: asked through mobiusd / the TUI; an answer re-opens the run"], size=11, color="ink", lh=17)
    save("mobius-r3-runtime", f)


# ---------------------------------------------------------------- C · state vs transition evidence
def fig_state_vs_transition():
    W, H = 500, 482
    f = Fig(W, H, "Post-state evidence against transition evidence",
            "Left: with only the post-state, a judge sees archive.txt holding 'the note' and notes.txt absent, "
            "and cannot tell whether that was notes.txt's former content. Right: a pre-state digest, the move, "
            "and the post-state digest let the relation be checked mechanically.")
    f.text(20, 26, "POST STATE ONLY", size=12.5, weight=800, color="bad")
    f.rect(20, 38, 460, 124, fill="badfill", stroke="bad")
    f.lines(38, 64, ["archive.txt  =  \"the note\"", "notes.txt    absent"], size=12.5, family=MONO, lh=20)
    f.lines(38, 118, ["criterion: archive.txt holds the former content of notes.txt",
                      "former content of notes.txt = ?   → not in the evidence",
                      "verdict that is justified:  cannot-tell"], size=11.5, color="ink", lh=18)
    f.text(20, 188, "PRE  →  ACTION  →  POST   (a transition witness)", size=12.5, weight=800, color="ok")
    f.rect(20, 200, 460, 270, fill="okfill", stroke="ok")
    boxes = [("pre   W_t", "notes.txt  digest 6862e4…", 220), ("action A_t", "fs.move(notes.txt → archive.txt)", 284),
             ("post  W_{t+1}", "archive.txt digest 6862e4… · notes.txt absent", 348)]
    for lab, v, yy in boxes:
        f.rect(38, yy, 424, 44, fill="card", stroke="faint", rx=6)
        f.text(50, yy + 18, lab, size=11.5, weight=700, color="soft")
        f.text(50, yy + 35, v, size=12, family=MONO)
    f.line(250, 264, 250, 284, arrow=True)
    f.line(250, 328, 250, 348, arrow=True)
    f.text(38, 414, "relation R_t:  digest(notes_{pre}) = digest(archive_{post})", size=12, weight=700, family=SANS)
    f.text(38, 434, "∧ exists(notes_{post}) = false   ⇒   the criterion is entailed", size=12, family=SANS)
    f.text(38, 456, "In R3 P3 every such pre-state was in the journal — just not in the judge's view.", size=10.8, color="soft", italic=True)
    save("mobius-r3-state-vs-transition", f)


# ---------------------------------------------------------------- D · two histories
def fig_two_histories():
    W, H = 500, 430
    f = Fig(W, H, "Two histories with the same post-state and opposite criterion truth",
            "History A: notes.txt held 'the note' and was moved to archive.txt; the criterion is true. History B: "
            "notes.txt held something else, was deleted, and archive.txt was written with 'the note'; the criterion "
            "is false. The post-state evidence is identical in both.")
    for i, (name, pre, act, truth, col, fill) in enumerate([
        ("History A", "notes_{pre} = \"the note\"", "fs.move(notes → archive)", "C true", "ok", "okfill"),
        ("History B", "notes_{pre} = \"something else\"", "delete notes; write archive", "C false", "bad", "badfill"),
    ]):
        x = 20 + i * 240
        f.rect(x, 16, 220, 214, fill=fill, stroke=col)
        f.text(x + 14, 40, name, size=13, weight=800, color=col)
        f.rect(x + 12, 52, 196, 40, fill="card", stroke="faint", rx=6)
        f.text(x + 22, 77, pre, size=11.5, family=MONO)
        f.line(x + 110, 92, x + 110, 112, arrow=True)
        f.text(x + 110, 128, act, size=11, color="soft", anchor="middle")
        f.line(x + 110, 134, x + 110, 150, arrow=True)
        f.rect(x + 12, 150, 196, 40, fill="card", stroke="faint", rx=6)
        f.text(x + 22, 168, "archive_{post} = \"the note\"", size=11.5, family=MONO)
        f.text(x + 22, 184, "notes_{post}: absent", size=11.5, family=MONO)
        f.text(x + 110, 216, truth, size=13, weight=800, color=col, anchor="middle")
        f.path(f"M{x + 110},230 C{x + 110},262 250,262 250,286", arrow=True)
    f.rect(70, 286, 360, 58, fill="accentfill", stroke="accent")
    f.text(250, 310, "same post evidence  E_{post}(h_A) = E_{post}(h_B)", size=12.5, weight=700, anchor="middle", color="accent")
    f.text(250, 330, "different criterion truth  C(h_A) ≠ C(h_B)", size=12.5, weight=700, anchor="middle", color="accent")
    f.text(250, 372, "so no judge can soundly answer `established` from E_{post} alone:", size=11.5, anchor="middle", color="soft")
    f.text(250, 396, "E_{post} ⊭ C", size=16, weight=700, anchor="middle", family=SERIF)
    save("mobius-r3-two-histories", f)


# ---------------------------------------------------------------- E · judge distribution
def fig_judge():
    W, H = 500, 560
    f = Fig(W, H, "R3 P3 judge verdicts and what the cannot-tell verdicts were missing",
            "114 judgements: R2 103 (19 established, 20 not-established, 64 cannot-tell), R1 11 (1 established, "
            "10 cannot-tell). Of 74 cannot-tell: 40 cite only a missing prior state, 5 cite a missing prior state "
            "and an unread current resource, 28 cite only an unread current resource, 1 is a judge timeout.")
    f.text(20, 26, "Verdicts, R3 P3 at f9b27dd (every row valid)", size=12.5, weight=700)
    cols = {"est": ("ok", "established"), "not": ("warn", "not-established"), "ct": ("accent", "cannot-tell")}
    data = [("R2 · 103", [19, 20, 64]), ("R1 · 11", [1, 0, 10]), ("all · 114", [20, 20, 74])]
    bx, bw = 100, 360
    for i, (lab, vals) in enumerate(data):
        y = 46 + i * 44
        f.text(bx - 10, y + 18, lab, size=11.5, anchor="end", weight=600, color="soft")
        tot = sum(vals); x = bx
        for v, key in zip(vals, ["est", "not", "ct"]):
            if v == 0:
                continue
            w = bw * v / tot
            c = cols[key][0]
            f.rect(round(x, 1), y, round(w, 1), 26, fill=c + "fill" if c != "accent" else "accentfill", stroke=c, rx=3)
            if w > 22:
                f.text(round(x + w / 2, 1), y + 17.5, str(v), size=11.5, weight=700, anchor="middle", color=c)
            x += w
    ly = 190
    for j, key in enumerate(["est", "not", "ct"]):
        c, name = cols[key]
        f.rect(100 + j * 125, ly - 10, 12, 12, fill=c + "fill" if c != "accent" else "accentfill", stroke=c, rx=2)
        f.text(118 + j * 125, ly, name, size=11, color="soft")
    f.line(20, 214, 480, 214, color="faint")
    f.text(20, 240, "What the 74 cannot-tell reasons say is missing (hand-coded)", size=12.5, weight=700)
    parts = [(40, "prior state only", "accent"), (5, "both", "warn"), (28, "an unread current resource", "blue"), (1, "judge timeout", "soft")]
    x = 20; y = 256; bw2 = 460
    for v, lab, c in parts:
        w = bw2 * v / 74
        fl = {"accent": "accentfill", "warn": "warnfill", "blue": "bluefill", "soft": "fill"}[c]
        f.rect(round(x, 1), y, round(w, 1), 30, fill=fl, stroke=c, rx=3)
        if w > 18:
            f.text(round(x + w / 2, 1), y + 20, str(v), size=12, weight=700, anchor="middle", color=c)
        x += w
    f.lines(20, 306, ["prior state only 40 · both 5 · current resource only 28 · judge timeout 1",
                      "assign the 5 mixed cases by primary barrier and this reads 43 / 30 / 1"], size=11, color="soft", lh=16)
    f.line(20, 346, 480, 346, color="faint")
    f.text(20, 372, "Share of each task's cannot-tell that cites a missing prior state", size=12.5, weight=700)
    tasks = [("T4 rename", 10, 10), ("R2-3 spec edit", 20, 22), ("R2-6 split", 15, 27), ("R2-2, R2-4, R2-5", 0, 15)]
    for i, (lab, a, n) in enumerate(tasks):
        y = 390 + i * 36
        f.text(128, y + 16, lab, size=11.5, anchor="end", color="soft", weight=600)
        f.rect(138, y, 260, 22, fill="fill", stroke="faint", rx=3)
        if a:
            f.rect(138, y, round(260 * a / n, 1), 22, fill="accentfill", stroke="accent", rx=3)
        f.text(408, y + 16, f"{a} / {n}", size=11.5, weight=700)
    f.text(20, 540, "Three unrelated task shapes; the other three tasks' misses are all current-state reads.", size=10.8, color="soft", italic=True)
    save("mobius-r3-judge", f)


# ---------------------------------------------------------------- F · certificate closure
def fig_certificate():
    W, H = 500, 470
    f = Fig(W, H, "The judge's decision basis against the completion certificate",
            "The judge is shown the binding's evidence plus the run's view; it answers established; goal.completed "
            "stores only the binding's evidence. In T4 repetition 3 the judge used a read of archive.txt and a "
            "listing of the root; the certificate keeps the read. Across R3 P3, 0 of 11 judge-bound criteria in "
            "completed runs had a certificate containing the judge's basis.")
    f.rect(20, 16, 460, 118, fill="bluefill", stroke="blue")
    f.text(36, 40, "What the judge was shown   J_i = E_{binding} ∪ E_{runView}", size=12.5, weight=700, color="blue")
    f.rect(36, 54, 204, 64, fill="card", stroke="faint", rx=6)
    f.lines(46, 74, ["E_{binding}", "obs-5: read archive.txt", "\"the note\\n\""], size=11, lh=15)
    f.rect(252, 54, 212, 64, fill="card", stroke="faint", rx=6)
    f.lines(262, 74, ["E_{runView}", "obs-4: listing of .", "notes.txt absent"], size=11, lh=15)
    f.line(250, 134, 250, 160, arrow=True)
    f.rect(150, 160, 200, 40, fill="okfill", stroke="ok")
    f.text(250, 185, "verdict: established", size=12.5, weight=700, anchor="middle", color="ok")
    f.line(250, 200, 250, 226, arrow=True)
    f.rect(20, 226, 460, 96, fill="accentfill", stroke="accent")
    f.text(36, 250, "What goal.completed keeps   C_i = E_{binding}", size=12.5, weight=700, color="accent")
    f.rect(36, 262, 204, 44, fill="card", stroke="faint", rx=6)
    f.lines(46, 280, ["obs-5: read archive.txt", "(nothing says notes.txt is gone)"], size=11, lh=15)
    f.rect(252, 262, 212, 44, fill="fill", stroke="faint", rx=6, dash="4 3")
    f.text(262, 289, "obs-4 — not kept", size=11, color="soft", italic=True)
    f.text(250, 352, "J_i ⊈ C_i", size=18, weight=700, anchor="middle", family=SERIF)
    f.lines(20, 384, ["R3 P3: 11 judge-bound criteria in completed runs; J ⊆ C in 0 of 11.",
                      "In 8 of the 11 the omitted evidence carries part of what the judge's own reason cites.",
                      "The journal's criterion.judged event still names J — the gap is in the certificate,",
                      "not in the log."], size=11.2, color="soft", lh=17)
    save("mobius-r3-certificate", f)


# ---------------------------------------------------------------- G · FTR loop
def fig_ftr():
    W, H = 500, 800
    f = Fig(W, H, "FTR as a candidate closed loop",
            "Reality and history feed a versioned world W_t. The FTR state holds possible futures, disagreement, "
            "future evidence requirements, risk, proof-failure probability and calibration. It informs a runtime "
            "meta-decision among act, observe, test, ask, fork, replan, preserve and wait. The action changes the "
            "world; forecasts resolve as satisfied, violated or void; calibration updates; a new FTR state follows.")
    cx = 210
    def node(y, h, title, sub=None, fill="card", stroke="line", tcol="ink"):
        f.rect(cx - 150, y, 300, h, fill=fill, stroke=stroke)
        f.text(cx, y + (22 if sub else h / 2 + 5), title, size=12.5, weight=700, anchor="middle", color=tcol)
        if sub:
            f.lines(cx, y + 40, sub, size=11, color="soft", lh=15, anchor="middle")
    node(14, 40, "Reality / history  H_t")
    f.line(cx, 54, cx, 74, arrow=True)
    node(74, 40, "Versioned world  W_t")
    f.line(cx, 114, cx, 134, arrow=True)
    f.rect(cx - 170, 134, 340, 196, fill="accentfill", stroke="accent", sw=1.6, rx=10)
    f.text(cx, 158, "FTR state  F_t   (candidate, not validated)", size=12.5, weight=800, anchor="middle", color="accent")
    comps = [("possible futures", "P_t(τ)"), ("disagreement", "D_t, H_t"), ("future evidence", "Ω*_t"),
             ("proof failure", "P_t^{proof}"), ("risk", "R_t(a)"), ("calibration", "Γ_t")]
    for i, (a, b) in enumerate(comps):
        y = 172 + i * 25
        f.text(cx - 140, y + 12, a, size=11.5, color="ink")
        f.text(cx + 140, y + 12, b, size=12, color="accent", anchor="end", family=SERIF, italic=True)
    f.line(cx, 330, cx, 352, arrow=True)
    node(352, 64, "Runtime meta-decision  x*_t", ["act · observe · test · ask", "fork · replan · preserve · wait"], fill="bluefill", stroke="blue", tcol="blue")
    f.line(cx, 416, cx, 436, arrow=True)
    node(436, 40, "Action  A_t")
    f.line(cx, 476, cx, 496, arrow=True)
    node(496, 40, "World transition  (O_{t+1}, W_{t+1})")
    f.line(cx, 536, cx, 556, arrow=True)
    node(556, 58, "Forecast resolution", ["satisfied · violated · void"])
    f.line(cx, 614, cx, 634, arrow=True)
    node(634, 40, "Calibration  Γ_{t+1}")
    f.line(cx, 674, cx, 694, arrow=True)
    node(694, 40, "New FTR state  F_{t+1}", fill="accentfill", stroke="accent", tcol="accent")
    # loop back
    f.path(f"M{cx + 150},714 C{cx + 250},714 {cx + 250},232 {cx + 172},232", arrow=True, dash="5 4")
    f.text(cx + 262, 470, "↺", size=20, color="soft", anchor="middle")
    f.text(20, 770, "Only the Boolean expectation layer exists in code today; nothing here is implemented as FTR.", size=10.8, color="soft", italic=True)
    save("mobius-r3-ftr-loop", f)


# ---------------------------------------------------------------- H · status map
def fig_status():
    groups = [
        ("MEASURED", "blue", ["cannot-tell dominated by missing prior state (3 task shapes)",
                              "unsupported establishment: 1 clear case in 20",
                              "certificate closure: 0 of 11",
                              "layered determinism 0.923 / 0.795 (n = 3, one commit)"]),
        ("OPEN", "accent", ["future information requirement Ω* (outlives FTR)",
                            "rollout disagreement as a signal",
                            "anticipatory evidence preservation", "proof-failure prediction",
                            "open-provider addressability"]),
        ("KILLED", "bad", ["FTR, strong form — killed under its own criteria",
                                          "pre-write write-set anticipation from reads (median 0.25)",
                                          "\"reuse costs nothing\" (OV-1)", "\"provenance link is load-bearing\" (PP-1)",
                                          "lease as approval validity (VB-1)"]),
        ("RETIRED · PRIOR ART", "soft", ["future prediction as novelty (predictive RV)",
                                         "approval capture/revalidation (CommitGuard, PlanFence, S-Bus)",
                                         "false success (Advani 2026)", "transition witness as a new primitive",
                                         "append-only replay; per-action approval gate"]),
        ("NOT YET EVALUABLE", "warn", ["Boolean `expected` → Brier / resolution",
                                       "\"0 false completions\" (0 opportunities)",
                                       "does content variance change outcomes (39/39 pass)"]),
    ]
    W = 500
    H = 20 + sum(34 + 19 * len(g[2]) + 14 for g in groups)
    f = Fig(W, H, "Research status map, 19 September 2026",
            "Measured, open, killed by experiment, retired as prior art, and not yet evaluable — the items the "
            "post discusses, grouped by status.")
    y = 14
    for name, c, items in groups:
        h = 30 + 19 * len(items)
        fill = {"blue": "bluefill", "accent": "accentfill", "bad": "badfill", "soft": "fill", "warn": "warnfill"}[c]
        f.rect(20, y, 460, h, fill=fill, stroke=c)
        f.text(34, y + 21, name, size=12, weight=800, color=c)
        for i, it in enumerate(items):
            f.text(46, y + 42 + i * 19, "· " + it, size=11.5)
        y += h + 14
    save("mobius-r3-status", f)


if __name__ == "__main__":
    fig_timeline(); fig_runtime(); fig_state_vs_transition(); fig_two_histories()
    fig_judge(); fig_certificate(); fig_ftr(); fig_status()
    print("wrote", sorted(n for n in os.listdir(OUT) if n.startswith("mobius-r3-")))
