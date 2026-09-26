"""S2 · demand-side census of public agent permission configs (deterministic; no LLM).

Claude Code: .claude/settings.json (committed, team-shared) and .claude/settings.local.json (written by
the product when a user answers "don't ask again"; usually gitignored, so its presence in a public repo
is itself a selection effect). Codex: config.toml approval_policy / sandbox_mode.

Rule classes (Claude permission rule grammar  Tool  |  Tool(specifier)):
  BARE        whole tool, no specifier                         e.g. Edit, WebSearch, Bash
  PREFIX      Bash specifier ending in :* or * (command family) e.g. Bash(npm run test:*)
  EXACT_CMD   Bash specifier with no wildcard (one literal command line)
  PATH        Read/Edit/Write/... with a path/glob specifier
  DOMAIN      WebFetch(domain:...)
  MCP         mcp__server[__tool]
  OTHER       anything else
"""
import json, re, collections, tomllib

SHELL = {"Bash", "PowerShell"}
PATH_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit", "Glob", "Grep", "LS"}
RULE = re.compile(r"^\s*([A-Za-z_][\w\-]*)\s*(?:\((.*)\))?\s*$", re.S)


def classify_rule(r):
    if not isinstance(r, str):
        return "OTHER", None
    if r.startswith("mcp__"):
        return "MCP", "mcp"
    m = RULE.match(r)
    if not m:
        return "OTHER", None
    tool, spec = m.group(1), m.group(2)
    if spec is None or spec.strip() in ("", "*"):
        return "BARE", tool
    s = spec.strip()
    if tool in SHELL:
        return ("PREFIX" if (s.endswith(":*") or s.endswith("*") or " *" in s) else "EXACT_CMD"), tool
    if tool == "WebFetch" and s.startswith("domain:"):
        return "DOMAIN", tool
    if tool in PATH_TOOLS:
        return "PATH", tool
    return "OTHER", tool


STATEY = re.compile(r"\b(git (status|diff)|test|pytest|jest|vitest|lint|eslint|ruff|mypy|tsc|check|verify|validate|"
                    r"guard|protect|block|deny|prevent|exit 2|sha|hash|lock|clean)\b", re.I)


def hook_summary(h):
    out = []
    if not isinstance(h, dict):
        return out
    for event, entries in h.items():
        for e in entries if isinstance(entries, list) else []:
            if not isinstance(e, dict):
                continue
            for hk in e.get("hooks", []) if isinstance(e.get("hooks"), list) else []:
                cmd = (hk or {}).get("command", "") if isinstance(hk, dict) else ""
                out.append({"event": event, "matcher": e.get("matcher"), "cmd": cmd[:300],
                            "statey": bool(STATEY.search(cmd or ""))})
    return out


def parse_claude(txt):
    try:
        d = json.loads(txt)
    except Exception:
        try:                                    # tolerate trailing commas / comments
            d = json.loads(re.sub(r",\s*([}\]])", r"\1", re.sub(r"^\s*//.*$", "", txt, flags=re.M)))
        except Exception:
            return None
    if not isinstance(d, dict):
        return None
    p = d.get("permissions") or {}
    if not isinstance(p, dict):
        p = {}
    lists = {k: [x for x in (p.get(k) or []) if isinstance(x, str)] for k in ("allow", "deny", "ask")}
    return {"lists": lists, "defaultMode": p.get("defaultMode"),
            "additionalDirectories": len(p.get("additionalDirectories") or []),
            "hooks": hook_summary(d.get("hooks")), "keys": sorted(d.keys())}


def parse_codex(txt):
    try:
        d = tomllib.loads(txt)
    except Exception:
        return None
    prof = d.get("profiles") or {}
    vals = {"approval_policy": [d.get("approval_policy")] + [v.get("approval_policy") for v in prof.values() if isinstance(v, dict)],
            "sandbox_mode": [d.get("sandbox_mode")] + [v.get("sandbox_mode") for v in prof.values() if isinstance(v, dict)]}
    return {k: [x for x in v if x] for k, v in vals.items()}
