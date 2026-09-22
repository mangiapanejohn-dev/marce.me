#!/usr/bin/env python3
"""Figures for "MØBIUS — What Happened After Each Time We Thought We Had Found Something".

Same conventions as r3-figures.py (whose drawing helpers and palettes this imports): hand-placed SVG,
one source, a light and a dark file, embedded as `.fig-light` / `.fig-dark`. Labels inside the figures
are English technical vocabulary so both language versions of the post share them; captions are
localised in the posts.

Every number drawn here is stated in the post with the file it was recomputed from. The late-bound
matrix is aggregated from the research lead's `late_bound_obligations.csv` (165 rows) with the query
written next to it; the R2-6-split timeline is read from
`docs/research/evidence/r2/f9b27dd/P3-judge-run-b/R2-6-split/rep-1/events.json` in the MØBIUS repo.

Figure 7 (FTR strong form) is Graphviz: `mobius-rl-ftr-strong.dot` is rendered once per palette.

    python3 scripts/research/rl-figures.py      # writes public/research/mobius-rl-*.svg
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("r3figs", os.path.join(HERE, "r3-figures.py"))
r3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r3)
Fig, save, PALETTES, OUT, SANS, MONO, SERIF = r3.Fig, r3.save, r3.PALETTES, r3.OUT, r3.SANS, r3.MONO, r3.SERIF


def lit(s: str) -> str:
    """Keep a literal underscore (an identifier) from being drawn as a subscript by r3's fmt()."""
    return s.replace("_", "_\u2060")

VERDICT = {  # label -> (colour key, fill key, glyph)
    "PRIOR ART": ("ok", "okfill", "×"),
    "RETIRED": ("soft", "fill", "×"),
    "KILLED": ("bad", "badfill", "×"),
    "STOPPED": ("bad", "badfill", "■"),
    "MEASURED": ("blue", "bluefill", "◐"),
    "OPEN": ("accent", "accentfill", "○"),
}


def badge(f, x, y, label, w=104):
    col, fill, glyph = VERDICT[label]
    f.rect(x, y - 13, w, 19, fill=fill, stroke=col, rx=4)
    f.text(x + w / 2, y + 1, f"{glyph} {label}", size=10.5, weight=800, color=col, anchor="middle")


# ---------------------------------------------------------------- 1 · graveyard
def fig_graveyard():
    rows = [
        ("18 Sep", "Approval line: capture at decision time", "CommitGuard · PlanFence (rule-encoded, VB-2)", "PRIOR ART"),
        ("18 Sep", "Evidence substitution (R2: 5/6 false completions)", "false success, measured at scale", "PRIOR ART"),
        ("19 Sep", "Residual A: effects with no content precondition", lit("If-None-Match: * / O_EXCL — a one-flag bug"), "KILLED"),
        ("19 Sep", "Residual B: who produces the validity key", "S-Bus DeliveryLog / ORI; later ATR", "PRIOR ART"),
        ("19 Sep", "Transition witness (51/88 cannot-tell)", "WAL undo · provenance · past-time LTL", "RETIRED"),
        ("20 Sep", "Evidence selection: −57.1 pp cannot-tell", "2nd system: coverage 76% → 25%", "MEASURED"),
        ("22 Sep 06:14", "Verification-input ownership (endogenous AP_a)", "monitorability · RTLola · IRA · ADR 0041", "PRIOR ART"),
        ("22 Sep 07:06", "Completion attribution (G-ext)", "F = N 21/21; actual causality", "RETIRED"),
        ("22 Sep 08:33", "Temporal witness lifecycle", "auxiliary views, self-maintainability (1996)", "PRIOR ART"),
        ("22 Sep 08:45", "Late-bound witness obligations", "LATE-CRITICAL = 0 / 165", "KILLED"),
        ("22 Sep 08:51", "Recovery semantic closure (#ledger reset)", "durable execution · semantic replay", "PRIOR ART"),
        ("22 Sep 10:08", "Correctness-under-adoption (cards C1–C3)", "0 violations in 5 applicable cells", "STOPPED"),
        ("22 Sep 10:24", "Delegated obligation closure", "C2-NI: stable identity, 1 effect", "KILLED"),
        ("22 Sep 10:52", "FTR, strong form", "shield + output commit + belief state", "RETIRED"),
        ("22 Sep 11:07", "Direction discovery from unexplained phenomena", "running — NO PRIMARY THESIS YET", "OPEN"),
    ]
    W, top, step = 790, 58, 40
    H = top + step * len(rows) + 30
    f = Fig(W, H, "Research trajectory, 18 to 22 September 2026",
            "Fifteen candidates in the order they were raised, what attacked each, and its status today.")
    f.text(16, 24, "18 → 22 Sep 2026 · candidate → attack → verdict", size=12.5, color="soft", weight=700)
    f.text(118, 44, "candidate", size=10.5, color="soft", weight=700)
    f.text(420, 44, "what attacked it", size=10.5, color="soft", weight=700)
    x0 = 98
    f.line(x0, top - 6, x0, top + step * (len(rows) - 1) + 6, color="faint", sw=2)
    for i, (d, cand, att, v) in enumerate(rows):
        y = top + i * step
        col = VERDICT[v][0]
        f.text(x0 - 12, y + 4, d, size=10.5, color="soft", anchor="end", weight=600)
        f.circle(x0, y, 4, fill="card", stroke=col, sw=2)
        f.line(x0 + 5, y, 112, y, color=col, sw=1.2)
        f.text(118, y + 4, cand, size=11.8, weight=700, color="ink")
        f.line(412 - 6, y, 412 - 2, y, color="faint")
        f.text(420, y + 4, att, size=10.8, color="soft")
        badge(f, 676, y, v)
    f.text(16, H - 10, "Terminal glyphs: × retired, reduced or killed · ■ stopped by a pre-written decision · ◐ measured, kept as a dimension · ○ open.",
           size=10.3, color="soft", italic=True)
    save("mobius-rl-graveyard", f)


# ---------------------------------------------------------------- 2 · R2-6-split c1
def fig_r26():
    W, H = 720, 440
    f = Fig(W, H, "R2-6-split repetition 1, criterion c1: evidence grows while decidability falls",
            "Every judgement of criterion c1 by journal event, the rewrite of notes.md, the run boundary, and "
            "four successive explanations.")
    X0, X1, EMAX = 40, 700, 122
    X = lambda e: X0 + (X1 - X0) * e / EMAX
    ya = 124  # axis
    f.rect(X(0), 18, X(78.5) - X(0), 150, fill="fill", stroke="faint", rx=4)
    f.rect(X(78.5), 18, X(EMAX) - X(78.5), 150, fill="bluefill", stroke="blue", rx=4)
    f.text(X(1.5), 36, "run 1 · session-8", size=11, weight=700, color="soft")
    f.text(X(80), 36, "run 2 · session-9 · view = its own observations", size=10.5, weight=700, color="blue")
    f.line(X0, ya, X1, ya, color="line", sw=1)
    for e in (0, 20, 40, 60, 80, 100, 120):
        f.line(X(e), ya, X(e), ya + 4, color="line")
        f.text(X(e), ya + 16, str(e), size=10, color="soft", anchor="middle")
    f.text(X(38), ya + 36, "journal event →", size=10, color="soft", anchor="end")
    judged = [(8, "CT", 1), (23, "CT", 3), (47, "CT", 3), (57, "EST", 2), (87, "CT", 1), (98, "CT", 2), (105, "CT", 3), (116, "CT", 8)]
    for e, v, n in judged:
        col = "ok" if v == "EST" else "bad"
        f.circle(X(e), ya - 20, 6.5, fill="okfill" if v == "EST" else "badfill", stroke=col, sw=1.6)
        f.text(X(e), ya - 34, "est" if v == "EST" else "c-t", size=10, weight=700, color=col, anchor="middle")
        f.text(X(e), ya - 47, f"[{e}]", size=9.5, color="soft", anchor="middle")
        if e > 80:
            f.text(X(e), 158, f"{n}", size=12, weight=800, color="blue", anchor="middle")
    f.text(X(84), 158, "bound", size=10, color="blue", anchor="end")
    marks = [(64, "[64] full read of notes.md", "end"), (65, "[65] fs.write notes.md → index · basis = [64]", "end"),
             (78, "[78] repeat guard stops run 1", "start"), (79, "[79] run 2 begins", "start")]
    for k, (e, lab, anc) in enumerate(marks):
        yy = 190 + k * 17
        c = "accent" if e in (64, 65) else "soft"
        f.line(X(e), ya + 2, X(e), yy - 4, color=c, sw=1, dash="3 3")
        f.text(X(e) + (-6 if anc == "end" else 6), yy, lab, size=10.5, color=c, weight=600, anchor=anc)
    # explanations
    f.text(20, 280, "Four explanations, in the order they were written", size=12, weight=800)
    ex = [
        ("KILLED", "“the evidence binding narrowed”", "07:24 ledger — never computed; bindings were 1 → 2 → 3 → 8"),
        ("KILLED", "“the run's own rewrite destroyed the pre-state”", "07:32 — but notes.md's full text is in the journal at [64]"),
        ("MEASURED", "“ADR 0045's staleness rule filtered it out”", "08:45 — true within one run, read from code"),
        ("OPEN", "run boundary + latest-per-resource view", "this audit — all four cannot-tell come after [79] (R3 plan F3)"),
    ]
    for i, (v, a, b) in enumerate(ex):
        y = 308 + i * 32
        badge(f, 20, y, v, w=96)
        f.text(128, y + 1, a, size=11.5, weight=700)
        f.text(128, y + 16, b, size=10.3, color="soft")
    save("mobius-rl-r26-split", f)


# ---------------------------------------------------------------- 3 · late-bound matrix
def fig_late_bound():
    # Aggregated from late_bound_obligations.csv (165 rows):
    #   cell[binding][(needs_pre, pre_existed)] = count
    cells = {
        "STATIC": {(False, False): 22, (False, True): 50, (True, False): 7, (True, True): 47},
        "LATE-SAFE": {(False, False): 0, (False, True): 12, (True, False): 0, (True, True): 0},
        "LATE": {(False, False): 15, (False, True): 0, (True, False): 12, (True, True): 0},
    }
    W, H = 720, 380
    f = Fig(W, H, "LATE-CRITICAL = 0 of 165",
            "165 criterion–resource pairs by when the resource was first resolvable and by whether the criterion needs "
            "the pre-state and whether the resource existed before the effect.")
    f.text(20, 26, "165 (criterion, changed resource) pairs · 65 journals · 102 criteria", size=12, weight=700, color="soft")
    cols = [(False, False), (False, True), (True, False), (True, True)]
    heads = [("needs pre-state: no", "resource existed: no"), ("needs pre-state: no", "resource existed: yes"),
             ("needs pre-state: yes", "resource existed: no"), ("needs pre-state: yes", "resource existed: yes")]
    x0, cw, y0, rh = 118, 132, 76, 58
    for j, (a, b) in enumerate(heads):
        f.text(x0 + j * cw + cw / 2, 52, a, size=10.3, color="soft", anchor="middle")
        f.text(x0 + j * cw + cw / 2, 66, b, size=10.3, color="soft", anchor="middle")
    for i, row in enumerate(["STATIC", "LATE-SAFE", "LATE"]):
        y = y0 + i * rh
        f.text(x0 - 12, y + rh / 2 + 5, row, size=12.5, weight=800, anchor="end", family=MONO)
        for j, c in enumerate(cols):
            n = cells[row][c]
            crit = row == "LATE" and c == (True, True)
            fill = "badfill" if crit else ("fill" if n else "card")
            f.rect(x0 + j * cw + 3, y + 3, cw - 6, rh - 6, fill=fill, stroke="bad" if crit else "faint", sw=1.6 if crit else 1, rx=6)
            f.text(x0 + j * cw + cw / 2, y + rh / 2 + 7, str(n), size=18 if crit else 15, weight=800,
                   color="bad" if crit else ("ink" if n else "faint"), anchor="middle")
        f.text(x0 + 4 * cw + 8, y + rh / 2 + 5, f"n = {sum(cells[row].values())}", size=11, color="soft")
    cx = x0 + 3 * cw + cw / 2
    f.text(cx, y0 + 3 * rh + 18, "↑ LATE-CRITICAL", size=11.5, weight=800, color="bad", anchor="middle")
    notes = [
        "27 / 27 LATE resources did not exist before the effect — a late-bound resource had no pre-state to lose.",
        "109 / 109 pairs on pre-existing resources had the pre-state captured (57 receipt digest, 52 earlier observation).",
        "75 / 75 applied overwrites of existing files carry a basis observation; 55 are full-content file reads.",
        "Stricter definition (pre-state existence from the effect's own receipt): still 0 / 165.",
    ]
    f.lines(20, 292, notes, size=11, color="ink", lh=19)
    save("mobius-rl-late-bound", f)


# ---------------------------------------------------------------- 4 · probe method
def fig_probe():
    W, H = 700, 400
    f = Fig(W, H, "A Jepsen-style invariant probe with mandatory controls",
            "Runtime under test, injected fault, external audit oracle, five-state verdict, and the broken and correct controls.")
    f.text(20, 26, "one card × one runtime × 3 attempts", size=12, weight=700, color="soft")
    steps = [
        ("deterministic stub model", "ScriptedModel / FunctionModel / harness stub · no real model"),
        ("runtime under test", "LangGraph 1.2.12 · OpenAI Agents 0.22.3 · Pydantic AI 2.47.0"),
        ("fault · wait · foreign world mutation", "parent process, at an announced fault point: SIGKILL, fresh-process resume"),
        ("external audit oracle", "reads the event stream + external world SQLite — never self-report, never source"),
    ]
    y = 44
    for i, (a, b) in enumerate(steps):
        hot = i == 3
        f.rect(20, y, 420, 52, fill="accentfill" if hot else "card", stroke="accent" if hot else "line", rx=8)
        f.text(34, y + 21, a, size=12.5, weight=800, color="accent" if hot else "ink")
        f.text(34, y + 39, b, size=10.5, color="soft")
        if i < 3:
            f.line(230, y + 52, 230, y + 70, arrow=True)
        y += 70
    f.line(230, y - 18, 230, y + 2, arrow=True)
    verdicts = [("violated", "bad"), ("not-violated", "ok"), ("NOT-CAPTURED", "warn"), ("probe-insensitive", "warn"), ("inapplicable", "soft")]
    for i, (v, c) in enumerate(verdicts):
        f.rect(20 + i * 86, y + 2, 82, 26, fill="card", stroke=c, rx=5)
        f.text(61 + i * 86, y + 19, v, size=9.2, weight=700, color=c, anchor="middle")
    f.text(20, y + 50, lit("orthogonal fields: contract_relation · responsibility · mitigation"), size=10.5, color="soft", family=MONO)
    f.text(20, y + 67, "inapplicable is not a pass · NOT-CAPTURED is not a violation", size=10.5, color="soft", italic=True)
    # controls rail
    for k, (t, sub, pred, col) in enumerate([
        ("deliberately broken control", ["caches the first answer, resets", "the budget, drops the proposal"], "must be caught: violated 3/3", "bad"),
        ("deliberately correct control", ["persists budget, proposal and", "effect id; re-reads the world"], "must pass: not-violated 3/3", "ok"),
    ]):
        yy = 44 + k * 128
        f.rect(470, yy, 210, 112, fill="badfill" if col == "bad" else "okfill", stroke=col, rx=8)
        f.text(484, yy + 22, t, size=11.8, weight=800, color=col)
        f.lines(484, yy + 44, sub, size=10.5, color="ink", lh=15)
        f.text(484, yy + 94, pred, size=11, weight=700, color=col)
    f.rect(470, 312, 210, 60, fill="warnfill", stroke="warn", rx=8)
    f.lines(484, 334, ["controls not 100% separated", "→ card is probe-insensitive;", ], size=10.8, color="warn", lh=15)
    f.text(484, 364, "no runtime verdict is read", size=10.8, color="warn", weight=700)
    f.path("M470,100 C452,100 452,260 442,260", color="faint", dash="3 3", arrow=True)
    f.path("M470,228 C458,228 458,266 442,266", color="faint", dash="3 3", arrow=True)
    save("mobius-rl-probe-method", f)


# ---------------------------------------------------------------- 5 · LangGraph correction
def fig_langgraph():
    W, H = 720, 560
    f = Fig(W, H, "One LangGraph result, read three times; and three instrument errors",
            "First reading, contract check, corrected reading; below, the untyped state schema, the cross-thread SQLite "
            "connection and the missing socksio package.")
    panels = [
        ("1 · first reading", "bad", "badfill", [("external audit", "[1, 2, 2, 3]"), ("budget", "3"), ("runtime self-report", "spent = 3"), ("durability", "\"sync\"")], "VIOLATED?"),
        ("2 · contract check", "warn", "warnfill", [("durable execution", "replay, not resume-at-line"), ("interrupt()", "node re-executes"), ("side effects", "wrap in @task"), ("unfinished task", "may run again →"), ("", "idempotency key")], "documented"),
        ("3 · corrected reading", "ok", "okfill", [("C2-N (inside node)", "inapplicable"), ("", "outside guarantee"), ("C2-T (@task done)", "[1, 2, 3]"), ("", "not-violated 3/3"), ("C3 journaled value", "kept")], "no violation"),
    ]
    pw = 222
    for i, (t, c, fill, kv, verdict) in enumerate(panels):
        x = 20 + i * (pw + 8)
        f.rect(x, 16, pw, 232, fill=fill, stroke=c, rx=8)
        f.text(x + 12, 38, t, size=12.5, weight=800, color=c)
        for k, (a, b) in enumerate(kv):
            yy = 64 + k * 30
            if a:
                f.text(x + 12, yy, a, size=10.3, color="soft")
            f.text(x + 12, yy + 14, b, size=11.8, weight=700, family=MONO)
        f.text(x + pw / 2, 234, verdict, size=12.5, weight=800, color=c, anchor="middle")
        if i < 2:
            f.line(x + pw + 1, 132, x + pw + 7, 132, arrow=True)
    f.text(20, 272, "The audit sequence never changed. What changed was its comparison with the contract.", size=11.2, italic=True, color="soft")
    f.text(20, 304, "The same morning, our own instrument", size=12.5, weight=800)
    errs = [
        ("StateGraph(dict)", ["untyped schema = one root", "channel, last value wins;", "gate's return erased", "`proposal` → approve A,", "dispatch B"], "fabricated a C3-W violation"),
        ("SQLite across threads", ["world connection used", "on LangGraph's worker", "thread → C2-T never ran", "", ""], "recorded NOT-CAPTURED"),
        ("socksio + mixed ledger", ["tracing exporter import", "failed under a SOCKS proxy;", "3 NOT-CAPTURED rows mixed", "with 3 fixed rows →", "unstable (openai, C1-RV)"], "archived 60 rows, reran 24"),
    ]
    for i, (t, body, res) in enumerate(errs):
        x = 20 + i * (pw + 8)
        f.rect(x, 318, pw, 196, fill="card", stroke="line", rx=8)
        f.text(x + 12, 342, t, size=12, weight=800, family=MONO, color="accent")
        f.lines(x + 12, 366, body, size=10.8, lh=17)
        f.text(x + 12, 500, res, size=10.8, weight=700, color="bad")
    f.text(20, 540, "Found by: event stream + typed-schema baseline with in-process resume; stderr; tables generated from rows.jsonl.", size=10.3, color="soft")
    save("mobius-rl-langgraph-correction", f)


# ---------------------------------------------------------------- 6 · C1 timeline
def fig_c1():
    W, H = 700, 470
    f = Fig(W, H, "C1-RV: post-approval revalidation under a foreign world change",
            "Validation at version 1 allows; wait; a third party moves the world to version 2, protected; approval; "
            "validation at version 2 denies; no destructive effect. A broken control that caches allow executes.")
    f.text(20, 26, "OpenAI Agents SDK 0.22.3 and Pydantic AI 2.47.0 · 3/3 each", size=12, weight=700, color="soft")
    steps = [
        ("V(a, S₀) = allow", "world: version 1, protected = false", "card", "line"),
        ("approval wait", "pending tool call held in run state", "fill", "faint"),
        ("foreign mutation", "harness, outside the runtime: version 2, protected = true", "warnfill", "warn"),
        ("human approves a", "same call id", "fill", "faint"),
        ("V(a, S₁) = deny", lit("guardrail / args_validator runs again after approval"), "okfill", "ok"),
        ("effect blocked", "destructive effects = 0", "okfill", "ok"),
    ]
    y = 42
    for i, (a, b, fill, st) in enumerate(steps):
        f.rect(20, y, 390, 50, fill=fill, stroke=st, rx=8)
        f.text(34, y + 21, a, size=12.8, weight=800, family=SERIF if "V(" in a else SANS)
        f.text(34, y + 39, b, size=10.5, color="soft")
        if i < len(steps) - 1:
            f.line(215, y + 50, 215, y + 64, arrow=True)
        y += 64
    f.rect(20, y + 2, 390, 30, fill="card", stroke="accent", rx=6)
    f.text(34, y + 22, lit("validation_world_versions = [1, 2]"), size=12.5, weight=800, family=MONO, color="accent")
    # control
    f.rect(440, 42, 240, 306, fill="badfill", stroke="bad", rx=8)
    f.text(454, 64, "broken control", size=12.5, weight=800, color="bad")
    f.lines(454, 88, ["V(a, S₀) = allow", "cache ALLOW", "", "foreign mutation → v2", "approve", "reuse cached ALLOW", "", "effect executes on v2"], size=11.2, lh=19)
    f.text(454, 262, "versions = [1]", size=12, weight=800, family=MONO, color="bad")
    f.text(454, 282, "destructive effects = 1", size=11.2, weight=700, color="bad")
    f.text(454, 302, "violated 3/3", size=11.2, weight=700, color="bad")
    f.text(454, 330, "correct control: [1, 2], 0 effects", size=10.3, color="ink")
    f.lines(440, 376, ["What detected the change is the validator we", "wrote in the seam — not the runtime. The runtime",
                       "re-invoked the seam and obeyed its denial."], size=10.5, color="soft", lh=15, italic=True)
    save("mobius-rl-c1-timeline", f)


# ---------------------------------------------------------------- 8 · reduction map
def fig_reduction():
    W, H = 720, 520
    f = Fig(W, H, "Seven candidates and what killed them",
            "Candidates on the left; experiments, prior art, official contracts and controls on the right.")
    cands = ["completion attribution", "transition witness", "late-bound obligations", "observation ownership",
             "correctness-under-adoption", "delegated obligation closure", "FTR strong form"]
    killers = [
        ("G-ext four arms: F = N 21/21", "exp"),
        ("actual causality (Halpern–Pearl; Dec-POMDP)", "prior"),
        ("WAL undo · past-time LTL · provenance", "prior"),
        ("auxiliary views, self-maintainable (1988/96)", "prior"),
        ("LATE-CRITICAL = 0 / 165", "exp"),
        ("RV monitorability (decidable, fixed AP_a)", "prior"),
        ("RTLola active monitoring · IRA · ADR 0041", "prior"),
        ("LangGraph / OpenAI / Pydantic contracts", "contract"),
        ("broken + correct controls, 100% separated", "control"),
        (lit("C2-NI: stable execution_info, 1 effect"), "exp"),
        ("End-to-End Arguments (1984)", "prior"),
        ("POMDP shield · output commit · belief state", "prior"),
    ]
    edges = [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 3), (3, 5), (3, 6), (4, 7), (4, 8), (5, 9), (5, 10), (6, 11), (6, 5)]
    style = {"exp": ("ink", None, 1.6), "prior": ("ok", "6 4", 1.3), "contract": ("blue", "8 3 2 3", 1.4), "control": ("warn", "2 3", 1.6)}
    cy = lambda i: 60 + i * 60
    ky = lambda j: 44 + j * 36
    for i, c in enumerate(cands):
        f.rect(20, cy(i) - 17, 200, 34, fill="card", stroke="line", rx=6)
        f.text(120, cy(i) + 4, c, size=11.5, weight=700, anchor="middle")
    for j, (k, t) in enumerate(killers):
        col, dash, sw = style[t]
        f.rect(430, ky(j) - 14, 270, 28, fill="card", stroke=col, rx=6, dash=dash)
        f.text(442, ky(j) + 4, k, size=10.5, color="ink")
    for i, j in edges:
        col, dash, sw = style[killers[j][1]]
        f.path(f"M220,{cy(i)} C330,{cy(i)} 330,{ky(j)} 430,{ky(j)}", color=col, sw=sw, dash=dash)
    lg = [("experiment", "exp"), ("prior art", "prior"), ("official contract", "contract"), ("control", "control")]
    for n, (lab, t) in enumerate(lg):
        col, dash, sw = style[t]
        x = 20 + n * 170
        f.line(x, H - 22, x + 36, H - 22, color=col, sw=sw, dash=dash)
        f.text(x + 44, H - 18, lab, size=10.5, color="soft")
    save("mobius-rl-reduction-map", f)


# ---------------------------------------------------------------- 7 · FTR strong form (Graphviz)
def fig_ftr_dot():
    src = open(os.path.join(HERE, "mobius-rl-ftr-strong.dot"), encoding="utf-8").read()
    for theme, pal in PALETTES.items():
        dot = src
        for k, v in pal.items():
            dot = dot.replace("{" + k + "}", v)
        svg = subprocess.run(["dot", "-Tsvg"], input=dot.encode(), capture_output=True, check=True).stdout.decode()
        # Graphviz sizes the root in pt; give <img> a real pixel size from the viewBox (as render-figures.sh does).
        svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
        m = re.search(r'viewBox="[-0-9.]+ [-0-9.]+ ([0-9.]+) ([0-9.]+)"', svg)
        w, h = float(m.group(1)), float(m.group(2))
        svg = re.sub(r'<svg width="[^"]*" height="[^"]*"', f'<svg width="{round(w)}" height="{round(h)}"', svg, count=1)
        svg = svg.replace('<polygon fill="white" stroke="none"', '<polygon fill="none" stroke="none"', 1)
        name = "mobius-rl-ftr-strong" + ("" if theme == "light" else "-dark")
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    fig_graveyard(); fig_r26(); fig_late_bound(); fig_probe(); fig_langgraph(); fig_c1(); fig_reduction(); fig_ftr_dot()
    print("wrote", sorted(n for n in os.listdir(OUT) if n.startswith("mobius-rl-")))
