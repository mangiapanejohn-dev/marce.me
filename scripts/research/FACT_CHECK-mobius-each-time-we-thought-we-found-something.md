# FACT_CHECK — "MØBIUS — What Happened After Each Time We Thought We Had Found Something"

Post: `src/data/blog/mobius-each-time-we-thought-we-found-something.zh.md` (primary) and `.md` (English).
Checked 22 Sep 2026. Every number was recomputed from the raw file named, not copied from a summary.

## 1 · Numbers and where they come from

| claim in the post | source | recomputed | status |
|---|---|---|---|
| 133 judgements: 21 est / 24 not-est / 88 cannot-tell | RESEARCH_MAP §22 | — (ledger count over all committed journals) | ledger |
| 51/88 T_TRANSITION (58.0%); rename 13/13, config 19/22, split 19/32 | `cannot_tell_classified.json` | yes | ✓ |
| 84/86 file observed before verdict; 2.43 vs 2.48 bound | RESEARCH_MAP §25 | — | ledger |
| coverage 66% / 93% / 93%, availability 100% | RESEARCH_MAP §25 | — | ledger |
| first round 32.4 pp, gate 64.2%, 36 CT→est in arm C | RESEARCH_MAP §26 | — | ledger |
| 57.1 pp (77.9 → 20.8), R 88.3%, gate 79.2% | `arm_comparison_all.csv` | yes (C 77.9, T 20.8, R 83.0/88.3, agree 79.2) | ✓ |
| 58.8 pp at `f9b27dd` (n=68), 44.4 pp at `33e599e` (n=9) | `arm_comparison_all.csv` split by commit | yes | ✓ |
| T3 42.9% vs T 20.8%; annotation ≈12 pp; gap item 33% vs 33% | RESEARCH_MAP §31 | T3 42.9% yes | ✓ / ledger |
| SWE-agent 6,670; 55.0 vs 48.8; B 37/200 parse failures; n=160 | RESEARCH_MAP §28 | — | ledger |
| browser-use 3/25 vs 15/25; 13/17 vs 2/8; cross-time 2/7, state 7/18 | `browseruse_two_arm.csv` | yes | ✓ |
| G-ext N=S=F est 10 / CT 11; F==N 21/21; F==S 21/21; S2==S 21/21; F2 20/21 flip | `gext_offline_four_arm.csv` | yes | ✓ |
| wording rerun: F notEst 18 / 21 / 18; length control 21/21 | `wording_robustness.csv` | yes | ✓ |
| 19/21 F-arm reasons ignore the causal item | RESEARCH_MAP §37.2 | not recomputable (CSV has no reasons) | ledger |
| 0/42 success conditions refer to an agent | `criterion_shape_census.csv` | regex rerun: 1 hit, "Senior Agent" (job title) | ✓ |
| 6 unexplained changes, all one fixture; 5 re-escalated, 1 completed by own write | `unexplained_changes.csv`, RESEARCH_MAP §33 | 6 rows yes | ✓ |
| LATE-CRITICAL 0/165; 65 journals; 102 criteria; STATIC 126 / LATE-SAFE 12 / LATE 27 | `late_bound_obligations.csv` | yes, cell by cell | ✓ |
| 27/27 LATE `pre_existed=false`; 109/109 captured (57 + 52) | same | yes | ✓ |
| 75/75 applied overwrites carry a basis; 55 full-content file reads | 104 journals under MØBIUS `docs/research/evidence/` | yes (new for this post) | ✓ |
| 107/120 dispatched write/patch/move carry `basis.observationId` | same journals | yes | ✓ |
| R2-6-split c1: [8][23][47] CT, [57] est, [87][98][105][116] CT, bindings 1→2→3→8 | `r2/f9b27dd/P3-judge-run-b/R2-6-split/rep-1/events.json` | yes | ✓ |
| [65] basis → obs-9 = [64] full read; [78] goal.abandoned; [79] new session-9 | same | yes | ✓ |
| LangGraph first reading `[1,2,2,3]`, self-report spent 3, positive control `[1,2,1,2,3]` | `probe_verdicts.csv`, PROBE_RESULTS v1 | yes | ✓ |
| controls 9/9 and 9/9; LangGraph C2-T/C2-R/C3-W/C3-C not-violated, C2-N inapplicable 4/3 | `rows_c2c3.jsonl` (33 rows) | yes | ✓ |
| `unstable: [('openai-agents','C1-RV')] \| C1 rows: 27`; archive 60, c2c3 33, clean 24 | session log; `rows_archive_mixed.jsonl`; `rows.jsonl` | yes; archive shows 3 NOT-CAPTURED (socksio ImportError) + 3 not-violated | ✓ |
| C1-RV `[1, 2]`, allow/deny, 0 effects, 3/3 both runtimes; broken `[1]`, 1 effect | `rows.jsonl` | yes | ✓ |
| C2-NI stable: 1 effect, 3/3; unstable control: 2 effects, violated 3/3; rc −9 | `rows.jsonl` | yes | ✓ |
| `grep -ril ftr packages` → 0 `.ts` files | MØBIUS @ `5e0843a` | yes | ✓ |

## 2 · Places where the record disagreed, and what the post says

1. **R2-6-split mechanism.** Ledger §40.2 attributes the four post-rewrite `cannot-tell` to ADR 0045's staleness filter. The journal shows run 1 abandoned at [78] and all four verdicts in run 2 (session-9), whose `#runView` walks only that run's observations. The engineering R3 plan (F3, 19 Sep) already said so. The post gives four explanations in order and marks the staleness one as partial.
2. **"109 destructive writes."** 109 counts (criterion, resource) pairs; deduplicated, it is 75 applied overwrites. The post states both units.
3. **"120 destructive effects."** The 120 are all dispatched `fs.write/patch/move`, including 36 creations and 9 refusals. The post uses "dispatched", not "destructive".
4. **`previousDigest` 57 vs 52.** Both ledger figures are right in different units: 57 pairs, 52 effects.
5. **StateGraph(dict) baseline.** The brief said the no-fault baseline showed state loss without a crash. The session log shows the typed-schema fix and the baseline were applied in the same step, so the baseline never ran under `dict`. The conviction rests on the event stream plus the correct typed-schema baseline. The post says this explicitly.
6. **G-ext F2 flip.** 20/21 in the first run, 18/21 in the wording rerun of the same wording. Both are reported.
7. **Evidence means.** Ledger §27 gives means 1.92 / 3.24 / 2.20 as if for the 77 cases; they are over all 106. The post does not repeat them.
8. **"Binding narrowed."** The 07:24 ledger version asserts it; the 07:32 version corrects it. Both timestamps are file versions, EDT.

## 3 · Prior art: corrections from re-verification

- 2204.00302 (Triantafyllou et al.) is **AIES 2022**, not AAMAS.
- 2204.00755 author order is **Carr, Jansen, Junges, Topcu**.
- CommitGuard: "non-observable" fails closed; the post does not call it a separate third outcome.
- 2609.01519 is submitted, not accepted; it is not cited in this post.
- ARIES: "undo records", not "before-images".
- LangGraph durable-execution wording now lives on the functional-API page (determinism, idempotency); `ExecutionInfo`'s full field set arrived in 1.1.5.
- AWS durable execution: the variable "stays at its initial value", not "reverts".
- Workflow Fidelity: 10 of 18 models skip the checkpoint (ledger was right).
- Quass et al. 1996 and Tompa & Blakeley 1988: metadata confirmed, content from abstracts and secondary sources → `UNVERIFIED-FULLTEXT`.
- Jepsen-style study of agent runtimes: none found on arXiv. The nearest is 2606.17182, which reproduces tool-effect reordering in LangGraph (C7 family, untested here). The post states this next to the "stopped" verdict.

## 4 · Adversarial questions, answered

- **Inapplicable written as pass?** No. C2-N and C1-RAW are outside every denominator and labelled so.
- **Documented behaviour written as a bug?** The first LangGraph `VIOLATED` is shown as withdrawn, with the contract.
- **Harness bug written as a runtime failure?** The C3-W violation is attributed to `StateGraph(dict)`.
- **Engineering usefulness written as novelty?** 57.1 pp is `MEASURED` and `PRIOR ART`; FTR is "may be useful as engineering, not supported as an abstraction".
- **Failed predictions removed?** The G-ext prediction, "binding narrowed", "zero not-established on last verdicts", the 32.4 pp round and the SWE-agent failure are all kept.
- **Later views presented as known at the time?** Timestamps are given for each turn. The run-boundary explanation is marked as found for this post.
- **Unresolved.** The 51-section FTR brief was not available, and the post says the verdict would need redoing if it has an unreduced operation. The discovery round was still running at publication.
