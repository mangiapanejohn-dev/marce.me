# MØBIUS — evidence bundle for the 22–23 September 2026 research record

Companion data for the post *The Model Can. The Runtime Never Said No.*
([marcyy.me/posts/mobius-the-model-can-the-runtime-never-said-no](https://marcyy.me/posts/mobius-the-model-can-the-runtime-never-said-no/)).

Published so that the numbers in that post can be recomputed rather than believed. Nothing here is a
paper result: the pilot and the load experiment are one task instance, ten turns, three seeds per cell,
run through a harness with no permission store; the G-ext test is an offline simulation of a judge.

## Recompute everything

```bash
python3 recount.py > recount.txt      # needs Python 3 and scipy
```

`recount.py` was written for the post, independently of the research lead's `analyze_load.py`, and reads
only files in this bundle. `recount.txt` is its output as committed. Every number in the post is in it.

## What is in it

| path | what it is |
|---|---|
| `load/harness/load_experiment.py` | the S3 load-experiment harness as it ran. The file declares `STEP_CAP = 24`; every run's metadata records `step_cap: 20`, and the four turns that hit the cap stopped at 20 steps, so the runs used 20 |
| `load/harness/analyze_load.py` | the research lead's analysis (reads Claude Science artifact ids; kept for provenance, not needed to recompute) |
| `load/rows/rows_<model>_<arm>_<load>_s<seed>.jsonl` | one row per turn for each of the 18 runs: asks, delete-turn flags, backup opportunities and compliance, and every convention checker's counts |
| `load/steps/steps_*.jsonl` | every action each agent took, one line per step (action, path, note, question) |
| `load/meta/meta_*.json` | per-run metadata: turns completed, token usage, step cap, fault log |
| `load/archive/` | the two contaminated first attempts, kept append-only rather than deleted: opus-4-6 GRANT L30 seed 3 (first attempt, rerun from scratch) and seed 2 (unfiltered file with an aborted run's rows appended; the published file keeps the complete run). Neither contains a request on a delete turn |
| `load/derived/` | the research lead's derived tables (`load_experiment_stats.csv`, `load_experiment_cells.csv`) |
| `load/figures/load_experiment.research-lead.png` | the research lead's original figure; the post redraws it from the rows |
| `pilot/pilot_differential.py` | the pilot harness (claude-sonnet-5, 2 constraints, 10 turns) |
| `pilot/pilot_paired_turns_v2.csv` | the pilot's clean run, one row per turn |
| `pilot/pilot_paired_turns-v1-voided.csv` | the **voided** first run: `max_tokens = 1500` truncated a second tool call and the loop executed it. Kept as the record of a fabricated violation |
| `pilot/figures/pilot_differential.research-lead.png` | the research lead's original pilot figure |
| `gext/gext_offline_four_arm.csv`, `wording_robustness.csv`, `criterion_shape_census.csv` | the G-ext tables (also in the 2026-09-22 bundle) |
| `gext/judge_tape_N_S_F_Z.json` | the 84 raw judge responses for arms N, S, F, Z — four per (run, criterion) pair, in that order, 21 pairs in the CSV's row order |
| `gext/judge_tape_S2_F2.json` | the 42 raw responses for the accomplishment-predicate arms, two per pair |
| `gext/judge_tape_wording.json` | the 168 raw responses of the wording-robustness rerun |
| `census/policy_census_rule_shares.csv`, `policy_census.py` | shares of permission-rule shapes in 1,959 public Claude Code settings files, and the deterministic classifier. **The raw rules are not published**: they are other people's commands and paths |
| `docs/*.md` | the research lead's own documents, in Chinese, as written at the time |

## Where each number in the post comes from

| claim | file |
|---|---|
| backup rule 39/39 → 116/152 (opus), 29/36 → 78/157 (haiku); p = 0.00014, 0.00074 | `load/rows/` |
| 0 approval requests in 52 standing-grant delete turns; opus 22, haiku 30 | `load/rows/` |
| opus asked at the first deletion 3/3 without a grant, 0/6 with one; haiku 1/3 | `load/rows/` |
| 0 re-requests in 9 later delete turns after an approval reply | `load/rows/` |
| 74 of 75 delete turns deleted the target; the 75th hit the step cap | `load/rows/` |
| backup failures: 33 of 36 (opus) and 73 of 79 (haiku) wrote no `.bak` | `load/steps/` + `load/rows/` |
| opus at 30 constraints stopped at turns 6, 7, 6 and 8, 6, 7 | `load/rows/`, `load/meta/` |
| pilot: 0 vs 5 requests, 104 vs 95 writes, 43/43 and 37/37; the voided 13 | `pilot/` |
| pilot: 2 of 3 seeds asked again on turn 9 after the turn-6 approval reply | `pilot/pilot_paired_turns_v2.csv` (`asks_detail`) |
| G-ext: F = N 21/21, F = S 21/21, Z = N 20/21 | `gext/judge_tape_N_S_F_Z.json` |
| G-ext: 0/21 F-arm reasons cite the effect record; 11/21 address authorship | `gext/judge_tape_N_S_F_Z.json` |
| G-ext: accomplishment predicate flips 20/21; S2 = S 21/21; wording rerun | `gext/judge_tape_S2_F2.json`, `gext/*.csv` |
| 47% of product-written shell allow rules are exact commands | `census/policy_census_rule_shares.csv` |

## Reading it honestly

- **The harness has no permission store.** Nothing held a grant or checked one; every deletion the model
  emitted was executed. What these files measure is whether the model asked, not whether anything could
  have stopped it.
- **`NOGRANT` is not "ask first".** Its clause makes asking available and leaves the judgement to the model.
- **The grant and the backup rule point in opposite directions**: keeping one means doing less, keeping the
  other means doing more. The comparison is confounded with that, and the post says so.
- **The pooled upper bound (0/52, 5.6%) mixes two models** whose request probe differs in sensitivity; the
  per-model bounds are 12.7% (opus) and 9.5% (haiku).
- **Haiku's null has little weight**: without a grant it asked in only 1 of 3 seeds.
- Opus at 30 constraints never reached turns 8–10 (token budget). Twelve constraints were not run.

## Provenance and integrity

`SHA256SUMS.txt` covers every file in this bundle, and `mobius-evidence-2026-09-26.tar.gz` is the same tree
as one archive. Nothing was redacted. File names had Claude Science version prefixes (`v1a2b3c4d_`) removed;
contents are byte-for-byte as produced.

Anything in the research lead's documents that the post contradicts, the post is the later word: see the fact
check in the site repository at `scripts/research/FACT_CHECK-mobius-the-model-can-the-runtime-never-said-no.md`.
