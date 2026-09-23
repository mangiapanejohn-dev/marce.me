# MØBIUS — evidence bundle for the 18–22 September 2026 research record

Companion data for the post *What Happened After Each Time We Thought We Had Found Something*
([English](https://marcyy.me/posts/mobius-each-time-we-thought-we-found-something/) ·
[中文](https://marcyy.me/zh/posts/mobius-each-time-we-thought-we-found-something/)).

Published so that the numbers in that post can be recomputed rather than believed. Nothing here is a
paper result: the cross-runtime work is an engineering pilot with deterministic stubs and 3 attempts
per cell, and the MØBIUS journals are a small corpus of experiment arms, not a workload.

## What is in it

| path | what it is |
|---|---|
| `pilot/` | the cross-runtime probe harness as it ran: neutral harness (`world.py`, `oracle.py`, `fault.py`, `eventlog.py`, `stub_model.py`, `worker.py`, `run_pilot.py`) and thin adapters (`adapters/langgraph_adapter.py`, `openai_agents_adapter.py`, `pydantic_ai_adapter.py`, `broken_control.py`, `correct_control.py`) |
| `pilot/results/rows.jsonl` | the clean ledger rerun with the final harness: 24 C1 rows plus 6 C2-NI rows, 30 in total. Every table in the post is generated from rows like these, never hand-written |
| `pilot/results/rows_c2c3.jsonl` | the C2/C3 ledger (33 rows), including the controls |
| `pilot/results/rows_archive_mixed.jsonl` | the archived mixed ledger (60 rows). Kept append-only rather than edited: it still holds the three `NOT-CAPTURED` rows from the `socksio` import failure that made the cell `unstable` |
| `pilot/results/runs/**` | per-run external audit event streams (`events.jsonl`), the external world SQLite, LangGraph checkpoint SQLite, fault markers, stderr |
| `pilot/results/applicability_c1.json`, `stability.json`, `manifests/lockfile.txt` | applicability gate, repeat-stability check, dependency lock |
| `data/*.csv`, `data/*.json` | the derived tables behind the post's figures and numbers (see the map below) |
| `docs/*.md` | the research lead's own result documents, in Chinese, as written at the time |
| `journals/` | the 104 MØBIUS `events.json` run journals the offline measurements were computed over |

## Where each number in the post comes from

| claim | file |
|---|---|
| `LATE-CRITICAL = 0 / 165`; 27/27 LATE are new; 109/109 pre-states captured | `data/late_bound_obligations.csv` |
| 51 of 88 `cannot-tell` are cross-time; 13/13, 19/22, 19/32 | `data/cannot_tell_classified.json` |
| evidence selection: C 77.9% → T 20.8%, R 88.3%; 58.8 pp at `f9b27dd` | `data/arm_comparison_all.csv` (plus `arm_T3_results.csv`, `oracle_arm_final.csv`, `state_rewrite_test.csv`) |
| G-ext: F = N 21/21, accomplishment predicate flips 20/21 | `data/gext_offline_four_arm.csv`, `data/wording_robustness.csv` |
| browser-use: 3/25 vs 15/25; 13/17 vs 2/8 | `data/browseruse_two_arm.csv` |
| 0 of 42 success conditions name an actor | `data/criterion_shape_census.csv` |
| the first LangGraph reading `[1, 2, 2, 3]` | `data/probe_verdicts.csv`, `docs/PROBE_RESULTS-v1-withdrawn.md` |
| C1-RV `validation_world_versions = [1, 2]`, 0 destructive effects | `pilot/results/rows.jsonl`, `pilot/results/runs/*C1-RV*/events.jsonl` |
| C2-NI: one external effect across SIGKILL; six stable identity fields | `pilot/results/rows.jsonl`, `data/execution_info_field_stability.csv` |
| 107/120 dispatched writes carry a basis; 75/75 overwrites; R2-6-split's [57]→[116] | `journals/` |

## Reading it honestly

- **`inapplicable` is not a pass** and does not enter any denominator; **`NOT-CAPTURED` is not a
  violation** — it means the instrument could not see. Both appear in these ledgers.
- **The controls carry the result.** A cell's `not-violated` may only be read when the deliberately
  broken control on the same probe was caught 3/3 and the deliberately correct one passed 3/3.
- `docs/PROBE_RESULTS-v1-withdrawn.md` is **withdrawn** and kept only as the record of a verdict
  issued before its contract check. `docs/PROBE_RESULTS.md` carries the withdrawal notice.
- The runtime versions under test were langgraph 1.2.12, openai-agents 0.22.3, pydantic-ai 2.47.0.
- The MØBIUS repository itself is private; `journals/` is the part of it these measurements used.

## Provenance and integrity

`SHA256SUMS.txt` covers every file in this bundle, and `mobius-evidence-2026-09-22.tar.gz` is the
same tree as one archive.

One redaction: `pilot/results/rows_archive_mixed.jsonl` had three captured stderr tails containing a
local filesystem path, replaced with `<env>/` and `<redacted-path>`. The `ImportError` they record is
intact. Nothing else was altered, and no row was removed — the checksums here are of the published
(redacted) files, so they will not match the manifests recorded inside the pilot run directories.

Anything in the research lead's documents that the post contradicts, the post is the later word: see
the fact check in the site repository at
`scripts/research/FACT_CHECK-mobius-each-time-we-thought-we-found-something.md`.
