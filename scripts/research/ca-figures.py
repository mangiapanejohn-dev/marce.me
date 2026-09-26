#!/usr/bin/env python3
"""Figures for "MØBIUS — The Model Can. The Runtime Never Said No."

Same conventions as r3-figures.py and rl-figures.py (whose drawing helpers and palettes this imports):
hand-placed SVG, one source, a light and a dark file, embedded as `.fig-light` / `.fig-dark`.

Figures 1 and 2 are redraws of the research lead's two rasters (kept in the evidence bundle as
`pilot/figures/pilot_differential.research-lead.png` and `load/figures/load_experiment.research-lead.png`):
same panels and the same numbers, recomputed here from the bundle's raw rows rather than copied from
the images. Figure 3 places each rule the post measures by where it was held.

    python3 scripts/research/ca-figures.py      # writes public/research/mobius-ca-*.svg
"""
from __future__ import annotations

import collections
import csv
import glob
import importlib.util
import json
import os
import re

from scipy.stats import beta

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("r3figs", os.path.join(HERE, "r3-figures.py"))
r3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r3)
Fig, save, SANS, MONO, SERIF = r3.Fig, r3.save, r3.SANS, r3.MONO, r3.SERIF


def lit(s: str) -> str:
    """Keep a literal underscore (an identifier) from being drawn as a subscript by r3's fmt()."""
    return s.replace("_", "_\u2060")

BUNDLE = os.path.join(HERE, "..", "..", "public", "research", "evidence", "2026-09-26")


def cp(k, n):
    lo = 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(0.975, k + 1, n - k))
    return lo, hi


def load_rows():
    rows = []
    for f in sorted(glob.glob(os.path.join(BUNDLE, "load", "rows", "rows_*.jsonl"))):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                r["m"] = "opus" if "opus" in r["model"] else "haiku"
                rows.append(r)
    return rows


# ---------------------------------------------------------------- 1 · pilot
def fig_pilot():
    rs = list(csv.DictReader(open(os.path.join(BUNDLE, "pilot", "pilot_paired_turns_v2.csv"))))
    opp = collections.Counter()
    bak = collections.defaultdict(lambda: [0, 0])
    auth = collections.defaultdict(lambda: [0, 0])
    asks = collections.Counter()
    for r in rs:
        t = int(r["turn"])
        if r["arm"] == "GRANT":
            opp[t] += int(r["bak_opportunities"])
            bak[t][0] += int(r["bak_complied"])
            bak[t][1] += int(r["bak_opportunities"])
            auth[t][0] += int(r["auth_opportunity"]) - int(r["auth_violations"])
            auth[t][1] += int(r["auth_opportunity"])
        else:
            asks[t] += int(r["n_asks"])

    W, H = 720, 470
    f = Fig(W, H, "Pilot: neither constraint decayed over 10 turns; without the grant, asks came only on delete turns",
            "claude-sonnet-5, two constraints, ten turns, three seeds per arm. With the standing grant, the grant held "
            "on every turn and the backup rule on every turn that had something to back up. Without the grant, five "
            "approval requests, all on turns 6 and 9, the only turns that asked for a deletion.")
    f.text(20, 26, "Pilot · claude-sonnet-5 · 2 constraints · 10 turns · 3 seeds per arm", size=12, weight=700, color="soft")

    # a — per-turn compliance in the GRANT arm
    x0, x1, y0, y1 = 64, 340, 78, 268   # plot box: y0 = 1.0, y1 = 0.0
    f.text(20, 56, "a", size=15, weight=800)
    f.text(40, 56, "Neither constraint decayed over 10 turns", size=13, weight=700)
    yv = lambda v: y1 - (y1 - y0) * v
    xv = lambda t: x0 + (x1 - x0) * (t - 1) / 9
    for v in (0, 0.5, 1.0):
        f.line(x0 - 4, yv(v), x1, yv(v), color="faint", sw=0.8)
        f.text(x0 - 8, yv(v) + 4, f"{v:.1f}", size=10.5, color="soft", anchor="end")
    for t in range(1, 11):
        f.text(xv(t), y1 + 18, str(t), size=10.5, color="soft", anchor="middle")
        f.text(xv(t), y1 - 8, str(opp[t]), size=9.5, color="soft", anchor="middle")
    f.text((x0 + x1) / 2, y1 + 36, "turn", size=11, color="soft", anchor="middle")
    f.text(x0 - 2, y1 - 22, "modifications to back up, per turn ↓", size=9.5, color="soft")
    pts = " ".join(f"{xv(t):.1f},{yv(auth[t][0] / auth[t][1]):.1f}" for t in range(1, 11))
    f.add(f'<polyline points="{pts}" fill="none" stroke="{{blue}}" stroke-width="2.4"/>')
    for t in range(1, 11):
        f.circle(xv(t), yv(auth[t][0] / auth[t][1]), 4.2, fill="blue", stroke="blue")
        if bak[t][1]:
            v = bak[t][0] / bak[t][1]
            f.rect(round(xv(t) - 5, 1), round(yv(v) - 5, 1), 10, 10, fill="card", stroke="accent", sw=1.8, rx=1.5)
    f.text(xv(1), yv(1) + 26, "n.d.", size=9.5, color="soft", anchor="middle")
    f.line(xv(1), yv(1) + 8, xv(1), yv(1) + 16, color="soft", sw=0.8)
    ly = 330
    f.line(40, ly - 4, 62, ly - 4, color="blue", sw=2.4)
    f.circle(51, ly - 4, 4.2, fill="blue", stroke="blue")
    f.text(70, ly, "standing approval: no ask for an in-scope operation", size=11)
    f.rect(46, ly + 13, 10, 10, fill="card", stroke="accent", sw=1.8, rx=1.5)
    f.text(70, ly + 22, "back up before modify (MTAC-IFBench File Operation)", size=11)

    # b — asks in the NOGRANT arm
    bx0, bx1, by0, by1 = 426, 690, 78, 268
    f.text(386, 56, "b", size=15, weight=800)
    f.text(406, 56, "Without the grant, asks only on delete turns", size=13, weight=700)
    ymax = 3
    yb = lambda v: by1 - (by1 - by0) * v / ymax
    for v in range(0, 4):
        f.line(bx0 - 4, yb(v), bx1, yb(v), color="faint", sw=0.8)
        f.text(bx0 - 8, yb(v) + 4, str(v), size=10.5, color="soft", anchor="end")
    bw = (bx1 - bx0) / 10
    for t in range(1, 11):
        cx = bx0 + bw * (t - 0.5)
        f.text(cx, by1 + 18, str(t), size=10.5, color="soft", anchor="middle")
        if asks[t]:
            hot = t == 9
            f.rect(round(cx - bw * 0.34, 1), round(yb(asks[t]), 1), round(bw * 0.68, 1), round(by1 - yb(asks[t]), 1),
                   fill="accentfill" if not hot else "warnfill", stroke="accent" if not hot else "warn", rx=2)
            f.text(cx, yb(asks[t]) - 6, str(asks[t]), size=11, weight=700, anchor="middle", color="accent" if not hot else "warn")
    f.text((bx0 + bx1) / 2, by1 + 36, "turn  (6 and 9 are the only turns that ask for a deletion)", size=11, color="soft", anchor="middle")
    f.lines(400, ly - 2, ["approval requests, 3 seeds summed, no grant",
                          "turn 9 came after the turn-6 reply “do not ask again”;",
                          "both are conditional: “if it exists, may I delete…”"], size=10.8, color="soft", lh=16)

    f.line(20, 392, 700, 392, color="faint")
    f.lines(20, 414, [lit("Voided first run (max_tokens = 1500 cut a second tool call mid-write and the loop executed it): the arm told"),
                      "not to ask asked 13 times, 10 counted as violations. All 13 were the agent reporting its own broken writes."],
            size=10.8, color="bad", lh=17)
    save("mobius-ca-pilot", f)


# ---------------------------------------------------------------- 2 · load
def fig_load():
    rows = load_rows()
    cells = collections.defaultdict(list)
    for r in rows:
        cells[(r["m"], r["arm"], r["load"])].append(r)

    def grant(m, L):
        d = [r for r in cells[(m, "GRANT", L)] if r["delete_turn"]]
        return sum(r["n_asks"] == 0 for r in d), len(d)

    def backup(m, L):
        g = cells[(m, "GRANT", "L2")] if L == "L2" else cells[(m, "GRANT", "L30")] + cells[(m, "NOGRANT", "L30")]
        return sum(r["bak_ok"] for r in g), sum(r["bak_opp"] for r in g)

    def asked_t3(m, arm):
        t3 = [r for L in ("L2", "L30") for r in cells[(m, arm, L)] if r["turn"] == 3]
        return sum(r["n_asks"] > 0 for r in t3), len(t3)

    W, H = 720, 580
    f = Fig(W, H, "Load lowers the backup rule, not the standing approval; the probe detects asks and a grant removes them",
            "Under 30 constraints the backup rule fell from 39 of 39 to 116 of 152 on opus-4-6 and from 29 of 36 to 78 of "
            "157 on haiku-4-5, while no delete turn under a standing approval produced an approval request at either load. "
            "Without a grant, opus asked at the first deletion in 3 of 3 seeds, haiku in 1 of 3; with one, 0 of 6 each. "
            "After a runtime approval reply, 0 of 9 later deletions were re-asked. Most backup failures wrote no backup at all.")
    f.text(20, 26, "S3 · opus-4-6 and haiku-4-5 · 2 or 30 active constraints · 10 turns · 3 seeds per cell", size=12, weight=700, color="soft")

    # a — compliance by model × load
    f.text(20, 56, "a", size=15, weight=800)
    f.text(40, 56, "Load lowers the backup rule, not the standing approval", size=13, weight=700)
    x0, x1, y0, y1 = 70, 418, 96, 318          # y0 = 1.00, y1 = 0.25
    yv = lambda v: y1 - (y1 - y0) * (v - 0.25) / 0.75
    for v in (0.25, 0.5, 0.75, 1.0):
        f.line(x0 - 4, yv(v), x1, yv(v), color="faint", sw=0.8)
        f.text(x0 - 8, yv(v) + 4, f"{v:.2f}", size=10.5, color="soft", anchor="end")
    groups = [("opus", "L2"), ("opus", "L30"), ("haiku", "L2"), ("haiku", "L30")]
    gx = [110, 190, 300, 380]
    for (m, L), x in zip(groups, gx):
        k, n = grant(m, L)
        lo, _ = cp(k, n)
        xs = x - 13
        f.line(xs, yv(lo), xs, yv(1.0), color="blue", sw=1.6)
        f.line(xs - 4, yv(lo), xs + 4, yv(lo), color="blue", sw=1.6)
        f.circle(xs, yv(k / n), 5, fill="blue", stroke="blue")
        f.text(xs, yv(lo) + 13, f"n={n}", size=9.5, color="blue", anchor="middle")
        k, n = backup(m, L)
        lo, hi = cp(k, n)
        xb = x + 13
        f.line(xb, yv(lo), xb, yv(hi), color="accent", sw=1.6)
        for yy in (lo, hi):
            f.line(xb - 4, yv(yy), xb + 4, yv(yy), color="accent", sw=1.6)
        f.rect(round(xb - 5.5, 1), round(yv(k / n) - 5.5, 1), 11, 11, fill="card", stroke="accent", sw=1.8, rx=1.5)
        f.text(xb, yv(lo) + 13, f"n={n}", size=9.5, color="accent", anchor="middle")
        f.text(x, y1 + 18, "2" if L == "L2" else "30", size=11, color="ink", anchor="middle", weight=600)
    f.text(150, y1 + 38, "opus-4-6", size=11.5, anchor="middle", weight=700)
    f.text(340, y1 + 38, "haiku-4-5", size=11.5, anchor="middle", weight=700)
    f.text(x0 - 8, y1 + 18, "constraints", size=9.5, color="soft", anchor="end")
    f.text(x0 - 50, 80, "compliance, 95% CI", size=9.8, color="soft")
    ly = 384
    f.circle(51, ly - 4, 5, fill="blue", stroke="blue")
    f.text(64, ly, "standing approval: delete turns with no approval request", size=11)
    f.rect(45.5, ly + 12.5, 11, 11, fill="card", stroke="accent", sw=1.8, rx=1.5)
    f.text(64, ly + 22, "backup rule: modifications with a byte-equal .bak first", size=11)
    f.text(64, ly + 40, "(30 constraints pools both arms; 2 constraints ran with the grant only)", size=9.8, color="soft")

    # b — asked at the first deletion
    f.text(452, 56, "b", size=15, weight=800)
    f.text(472, 56, "A grant removes the asks", size=13, weight=700)
    bx0, by0, by1 = 478, 116, 300
    f.text(bx0 - 4, 80, "seeds asking at the first deletion (turn 3)", size=9.8, color="soft")
    bars = [("opus", "NOGRANT", "no grant"), ("opus", "GRANT", "grant"), ("haiku", "NOGRANT", "no grant"), ("haiku", "GRANT", "grant")]
    f.line(bx0, by1, 700, by1, color="line", sw=1)
    for i, (m, arm, lab) in enumerate(bars):
        k, n = asked_t3(m, arm)
        cx = bx0 + 26 + i * 55
        h = (by1 - by0) * k / n
        col = "soft" if arm == "NOGRANT" else "blue"
        if k:
            f.rect(cx - 18, round(by1 - h, 1), 36, round(h, 1), fill="fill", stroke="soft", rx=2)
        else:
            f.line(cx - 18, by1 - 1.5, cx + 18, by1 - 1.5, color="blue", sw=3)
        f.text(cx, by1 - h - 7, f"{k}/{n}", size=11.5, weight=700, anchor="middle", color="ink")
        f.text(cx, by1 + 16, lab, size=10, anchor="middle", color=col)
    f.text(bx0 + 53, by1 + 34, "opus-4-6", size=11, anchor="middle", weight=700)
    f.text(bx0 + 163, by1 + 34, "haiku-4-5", size=11, anchor="middle", weight=700)
    f.lines(460, 372, ["after a runtime approval reply", "(“do not ask again for operations",
                       "of this kind”): 0 of 9 later deletions", "re-asked — opus 5, haiku 4 (one seed)"],
            size=10.8, color="ink", lh=16)

    # c — how the backup rule failed at L30
    f.line(20, 450, 700, 450, color="faint")
    f.text(20, 474, "How the backup rule failed at 30 constraints (from the step logs)", size=12.5, weight=700)
    shapes = {"opus": (116, 33, 3), "haiku": (78, 73, 6)}
    for i, (m, (ok, none, wrong)) in enumerate(shapes.items()):
        y = 490 + i * 34
        tot = ok + none + wrong
        f.text(98, y + 16, f"{m} · {tot}", size=11, anchor="end", weight=600, color="soft")
        x = 108
        for v, fill, st in ((ok, "okfill", "ok"), (none, "badfill", "bad"), (wrong, "warnfill", "warn")):
            w = 470 * v / tot
            f.rect(round(x, 1), y, round(w, 1), 24, fill=fill, stroke=st, rx=3)
            if w > 20:
                f.text(round(x + w / 2, 1), y + 16.5, str(v), size=11, weight=700, anchor="middle", color=st)
            x += w
        f.text(588, y + 16, f"{wrong}" if 470 * wrong / tot <= 20 else "", size=11, weight=700, color="warn")
    f.rect(610, 486, 10, 10, fill="okfill", stroke="ok", rx=2)
    f.text(626, 495, "kept", size=10.5, color="soft")
    f.rect(610, 504, 10, 10, fill="badfill", stroke="bad", rx=2)
    f.text(626, 513, "no .bak written", size=10.5, color="soft")
    f.rect(610, 522, 10, 10, fill="warnfill", stroke="warn", rx=2)
    f.text(626, 531, "wrong content", size=10.5, color="soft")
    save("mobius-ca-load", f)


# ---------------------------------------------------------------- 3 · where each rule lived
def fig_where():
    W, H = 720, 704
    f = Fig(W, H, "Where each rule lived, and what held",
            "The model could delete in every arm. Rules delivered as text the model reads: a standing grant held in 52 "
            "delete turns; a backup rule fell 24 to 31 points under load; an approval reply held 9 of 9 in one experiment "
            "and not in 2 of 3 in another. Rules held as runtime state and checked before dispatch: MØBIUS approvals, typed "
            "constraints that no goal in the corpus used, and OS sandboxes. Completion decided by the criterion's grammar: "
            "a state predicate is established whoever wrote the file; an accomplishment predicate is not.")
    f.rect(20, 14, 680, 46, fill="bluefill", stroke="blue")
    f.text(36, 34, "Capability: the model could delete in every arm", size=12.5, weight=700, color="blue")
    f.text(36, 51, "74 of 75 delete turns removed the target; the 75th hit the step cap. haiku, with no grant, deleted 10 of 10 without asking.",
           size=10.5, color="ink")

    def band(y, h, title, sub, fill, stroke, items):
        f.rect(20, y, 680, h, fill=fill, stroke=stroke, rx=10)
        f.text(36, y + 24, title, size=12.8, weight=800, color=stroke)
        f.text(684, y + 24, sub, size=10.3, color="soft", anchor="end", italic=True)
        yy = y + 44
        for head, lines, verdict, vcol in items:
            f.text(36, yy, head, size=11.5, weight=700)
            f.lines(36, yy + 16, lines, size=10.5, color="soft", lh=14.5)
            f.text(684, yy, verdict, size=11, weight=700, color=vcol, anchor="end")
            yy += 16 + 14.5 * len(lines) + 12
        return y + h

    y = band(76, 218, "Held as text the model reads", "nothing checks it before the effect", "card", "warn", [
        (lit("standing grant, turn-0 prompt (“do not use ask_approval”)"),["0 approval requests in 52 delete turns; opus asked 3 of 3 without it"], "no asks", "ok"),
        ("backup rule, same prompt (“write .bak first”)", ["opus 1.00 → 0.76, haiku 0.81 → 0.50 under 30 constraints; failures skipped the step"], "fell 24–31 pp", "bad"),
        ("approval reply (“do not ask again for operations of this kind”)", ["S3: 0 of 9 later deletions re-asked · pilot, sonnet-5: 2 of 3 asked again, conditionally"], "mixed", "warn"),
        ("Claude Code documentation on CLAUDE.md", ["“context, not enforced configuration”"], "by design", "soft"),
    ])
    y = band(y + 16, 218, "Held as runtime state, checked before dispatch", "the model is not asked to remember", "card", "blue", [
        ("MØBIUS approval (V65, K8)", ["recomputed against the world it was granted over; “an answered question is not asked again”"], "gate", "blue"),
        ("MØBIUS typed constraints and protected invariants", ["refused before dispatch — and written on 0 of 159 goals in its own corpus"], "unused", "warn"),
        ("OS sandbox (Seatbelt, bubblewrap)", ["Claude Code docs: holds \u201cregardless of what the model chose to run\u201d \u2014 but not against egress through an allowed host"], "boundary", "blue"),
        ("pre-state capture before an overwrite", ["MØBIUS corpus 109 of 109 pairs — other tasks, one model, no load: not a controlled comparison"], "captured", "ok"),
    ])
    band(y + 16, 136, "Decided by the criterion's grammar", "what “done” means", "card", "accent", [
        ("state predicate (“notes.md is an index linking the three files”)", ["established 10 of 21 whether this run or another writer made it so (F = N = S, 21/21)"], "authorship invisible", "warn"),
        ("accomplishment predicate (“this run's own effects brought about …”)", ["another writer: 20 of 21 not-established · this run: 21 of 21 unchanged"], "authorship decides", "ok"),
    ])
    save("mobius-ca-where", f)


if __name__ == "__main__":
    fig_pilot()
    fig_load()
    fig_where()
