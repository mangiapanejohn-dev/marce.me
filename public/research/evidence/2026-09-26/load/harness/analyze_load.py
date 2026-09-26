"""Analysis for S3 (load experiment). Reads rows_*.jsonl artifacts listed in handoff/s3_results.json."""
import json, os, glob
import numpy as np, pandas as pd

XS = [f"X{i:02d}" for i in range(1, 29)]
CORE = XS[:10]


def load_rows(results_path="handoff/s3_results.json"):
    R = json.load(open(results_path))
    frames = []
    for fid, v in R.items():
        so = v.get("so") or {}
        vid = so.get("rows_version_id")
        if v.get("status") != "completed" or not vid:
            continue
        p = host.artifact_path(vid)
        rows = [json.loads(l) for l in open(p) if l.strip()]
        for r in rows:
            r["cell_name"] = v["name"]
        frames.append(pd.DataFrame(rows))
    df = pd.concat(frames, ignore_index=True)
    df["msub"] = df["model"].str.extract(r"(opus-4-6|haiku-4-5)")[0]
    return df


def csr(df, keys):
    opp = df[[f"{k}_opp" for k in keys]].sum(axis=1)
    ok = df[[f"{k}_ok" for k in keys]].sum(axis=1)
    return ok, opp


def cell_summary(df):
    out = []
    for (m, a, l), g in df.groupby(["msub", "arm", "load"]):
        ok, opp = csr(g, CORE)
        early = g[g.turn <= 3]; late = g[g.turn >= 8]
        eo, ep = csr(early, CORE); lo, lp = csr(late, CORE)
        allk = XS if l == "L30" else CORE
        aok, aopp = csr(g, allk)
        out.append({"model": m, "arm": a, "load": l, "seeds": g.seed.nunique(), "run_turns": len(g),
                    "asks": int(g.n_asks.sum()),
                    "asks_delete_turns": int(g[g.delete_turn == 1].n_asks.sum()),
                    "delete_turns": int(g.delete_turn.sum()),
                    "targets_deleted": int(g.target_deleted.fillna(0).sum()),
                    "bak_csr": g.bak_ok.sum() / max(1, g.bak_opp.sum()), "bak_opp": int(g.bak_opp.sum()),
                    "core_csr": ok.sum() / max(1, opp.sum()), "core_opp": int(opp.sum()),
                    "core_csr_t1_3": eo.sum() / max(1, ep.sum()), "core_csr_t8_10": lo.sum() / max(1, lp.sum()),
                    "all_given_csr": aok.sum() / max(1, aopp.sum()),
                    "faults": int(g.faults.sum()), "errors": int(g.errors.sum())})
    return pd.DataFrame(out)


def per_turn(df, keys=CORE):
    rows = []
    for (m, a, l, t), g in df.groupby(["msub", "arm", "load", "turn"]):
        ok, opp = csr(g, keys)
        rows.append({"model": m, "arm": a, "load": l, "turn": t,
                     "core_csr": ok.sum() / max(1, opp.sum()), "core_opp": int(opp.sum()),
                     "asks": int(g.n_asks.sum()),
                     "bak_csr": g.bak_ok.sum() / max(1, g.bak_opp.sum()) if g.bak_opp.sum() else np.nan})
    return pd.DataFrame(rows)


def per_constraint(df):
    rows = []
    for (m, l), g in df.groupby(["msub", "load"]):
        for k in XS:
            o, n = g[f"{k}_ok"].sum(), g[f"{k}_opp"].sum()
            e = g[g.turn <= 3]; la = g[g.turn >= 8]
            rows.append({"model": m, "load": l, "constraint": k, "opp": int(n), "csr": o / n if n else np.nan,
                         "csr_early": e[f"{k}_ok"].sum() / max(1, e[f"{k}_opp"].sum()) if e[f"{k}_opp"].sum() else np.nan,
                         "csr_late": la[f"{k}_ok"].sum() / max(1, la[f"{k}_opp"].sum()) if la[f"{k}_opp"].sum() else np.nan})
    return pd.DataFrame(rows)
