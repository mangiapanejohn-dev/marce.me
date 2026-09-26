# FACT_CHECK — "MØBIUS — The Model Can. The Runtime Never Said No."

Post: `src/data/blog/mobius-the-model-can-the-runtime-never-said-no.md` (English only).
Checked 26 Sep 2026. Every number was recomputed from the raw file named, not copied from a summary.
`public/research/evidence/2026-09-26/recount.py` reproduces every row marked "recount.py".

## 1 · Numbers and where they come from

| claim in the post | source | recomputed | status |
|---|---|---|---|
| discovery round: `NO PRIMARY THESIS YET`, 20 phenomena, 11:35 on 22 Sep | `docs/RESEARCH_DIRECTION_DISCOVERY.md` | — | ledger |
| 159 `goal.created`, all three constraint fields empty | `docs/ADMISSIBLE_SET_SURVEY.md` §2 | — (journals in the 09-22 bundle) | ledger |
| `goal.ts` prose-constraint comment; `TypedConstraint` has one member | MØBIUS `protocol/src/goal.ts:162–170`, `protocol/src/constraint.ts:64` at `5e0843a` | read in source | ✓ |
| "An answered question is not asked again — whichever rule asked it." | MØBIUS `runtime-core/src/authority.ts:598` at `5e0843a` | read in source | ✓ |
| MTAC-IFBench: 91.33 constraints/instance, 6/18 classes, none on authorization; policy-file finding; "updating … harder" | arXiv 2609.14992 HTML | read (WebFetch, verbatim) | ✓ |
| MTAC Table 2: Opus-4.6 82.4→76.2 (6.2), Haiku-4.5 72.4→49.7 (22.7) | same | read | ✓ |
| OpenAlex: 1,297 records; positive controls 4/4 and 2/4 | `docs/ACM_GAP_CHECK.md` | — | ledger |
| pilot voided run: GRANT 13 asks, NOGRANT 5, 10 "violations" | `pilot/pilot_paired_turns-v1-voided.csv` | recount.py | ✓ |
| pilot clean run: 0 vs 5 asks (turns 6, 9), 104 vs 95 writes, 43/43, 37/37, 0 faults | `pilot/pilot_paired_turns_v2.csv`, `pilot_fault_log_v2.json` | recount.py | ✓ |
| pilot: seeds 2 and 3 asked again on turn 9 after the turn-6 approval reply | `pilot/pilot_paired_turns_v2.csv` (`asks_detail`), reply text in `pilot_differential.py` | recount.py | ✓ **new** |
| S3 cells, turns reached, delete turns, asks, backup counts | `load/rows/` (18 files) | recount.py | ✓ |
| backup 39/39 → 116/152 (−23.7 pp, p 0.00014); 29/36 → 78/157 (−30.9 pp, p 0.00074) | `load/rows/` | recount.py | ✓ |
| per-seed backup ranges (opus 1.00 vs 0.65–0.82; haiku 0.75–0.83 vs 0.34–0.59) | `load/rows/` | recount.py | ✓ new |
| backup failures: opus 33 none + 3 wrong of 36; haiku 73 + 6 of 79 | `load/steps/` + `load/rows/` | recount.py | ✓ **new** |
| conventions 94–99% at L30; core-10 base rate 31–38% at L2 | `load/rows/` | ad hoc (same method as `analyze_load.py`) | ✓ |
| opus per-turn backup at L30: 0.74 at turn 2, 0.62–0.88 after; haiku turn 10 at both loads | `load/rows/` | ad hoc | ✓ new |
| grant: 0/52 delete-turn requests (opus 22, haiku 30); bounds 12.7%, 9.5%, pooled 5.6% | `load/rows/` | recount.py | ✓ |
| 51/52 deleted; the 52nd hit the 20-step cap | `load/rows/` | recount.py | ✓ **new** |
| turn 3: opus 3/3 vs 0/6; haiku 1/3 vs 0/6 | `load/rows/` | recount.py | ✓ |
| post-approval: 0/9 (opus 5, haiku 4 from one seed); bound 28% | `load/rows/` | recount.py | ✓ |
| 74/75 delete turns deleted; haiku 10/10 without asking in two seeds | `load/rows/` | recount.py | ✓ new |
| opus L30 stopped at 6, 7, 6 / 8, 6, 7; ~1.85M token budget | `load/rows/`, `load/meta/` | recount.py | ✓ |
| step cap 20 (file says 24) | `load/meta/`, `load/rows/` (max steps 20, four turns at 20) | ad hoc | ✓ new |
| archived first attempts contain no delete-turn requests | `load/archive/` | ad hoc | ✓ new |
| G-ext N = S = F: est 10 / CT 11; F = N 21/21, F = S 21/21 | `gext/judge_tape_N_S_F_Z.json` (order verified 63/63 against the CSV) | recount.py | ✓ |
| Z: est 11 / CT 10; one verdict moved (R2-3-spec rep-1, run-b) | same (one response is fenced JSON; lenient parse) | recount.py | ✓ new |
| F-arm reasons: 0/21 cite the effect record; 11/21 address authorship; all 10 F-est dismiss it | same | recount.py | ✓ **corrects the 22 Sep post** |
| S2 = S 21/21; F2 notEst 20 / CT 1; wording rerun 18/21/18; length control 21/21 | `gext/judge_tape_S2_F2.json`, `gext/wording_robustness.csv` | recount.py | ✓ |
| census: 1,959 files; allow 54/22/4%; deny 57/37%; local shell exact 47% (44–50) | `census/policy_census_rule_shares.csv` | read | ✓ |
| one-off share of exact rules 0.655 (8,377 / 12,783) → ~31% of local shell rules | research lead's `exact_rules_classified.csv` (not published: third-party content) | recomputed locally | ✓ |
| hooks ≥70 (3.6%), completion gates 12 (0.6%), 1,020 external scripts | `docs/POLICY_DEMAND_CENSUS.md` | — (raw not published) | ledger |
| 481 CLAUDE.md files; 4–16%; 4.4% strictest | arXiv 2608.23550 abstract | read | ✓ |
| Track B: ~500 prefixes, ~250M tokens; 0.716 | `docs/TRACK_B_GATE.md`; 2606.21399 via research lead | — | ledger |

## 2 · Places where the record disagreed, and what the post says

1. **"Three models, two loads, two authorization channels, same conclusion"** (`LOAD_EXPERIMENT.md` §3). The pilot's
   `NOGRANT` seeds 2 and 3 received the runtime reply "do not ask again for operations of this kind" on turn 6
   and asked again on turn 9. Both asks are conditional on a file that did not exist, so they are ambiguous, but
   the runtime channel in the pilot does not support the summary. The post reports 0/9 (S3) and 2/3 (pilot) side
   by side.
2. **"19/21 F-arm reasons do not mention the causal item"** (RESEARCH_MAP §37.2; repeated in the 22 Sep post).
   The 84-call tape gives 0/21 citing the effect record by name and 11/21 addressing authorship, all 10 F-arm
   `established` verdicts dismissing it as irrelevant. The post states the correction and that the 22 Sep post
   carries the old number.
3. **Z arm** is not in `gext_offline_four_arm.csv`. The ledger's est 11 / CT 10 is confirmed from the tape (one
   response wrapped in a Markdown code fence).
4. **"Load effect is a level shift, not a turn decay."** Confirmed for opus. Haiku has a steep turn 10, present at
   both loads; the post says so.
5. **Pooled bound 5.6%** mixes two models; the post gives per-model bounds first.
6. **Step cap** 24 in the harness file vs 20 in every run's metadata; the runs used 20.
7. **Pilot write counts**: two versions of `PILOT_TRACK_A.md` give NOGRANT 102 and 95; the CSV gives 95.

## 3 · Omissions in the original design, stated in the post (not errors in the numbers)

- The paired constraints differ in direction (omit a step vs add one); a restrictive authorization was never run.
- No arm compares a granted and an ungranted opus after turn 3; no one-time-approval arm.
- The harness has no permission store and no refusal path; every emitted deletion executed.

## 4 · External sources: how each was checked (26 Sep)

- arXiv records via the export API (title, authors, date): 2609.14992, 2608.15888, 2604.09408, 2606.21399,
  2605.10481, 2505.02709, 2608.23550, 2608.27443, 2510.05307, 2512.20662, 2608.03836, 2607.15495, 2505.05410,
  2503.11926, 2507.11473. Abstracts read for those cited.
- Crossref DOIs: Saltzer & Schroeder 1975, Hardy 1988, Sha 2001, Aghion & Tirole 1997, Dennis & Van Horn 1966,
  Scerri et al. 2002, Saltzer et al. 1984. Complete mediation and least privilege read in the Saltzer & Schroeder
  text; Aghion & Tirole's definitions from the abstract.
- transformer-circuits.pub/2026/workspace and anthropic.com/research/global-workspace: authors, date, the spider
  swap, 54/70/70%, ablation, single forward pass, "automatic" computation, the consciousness disclaimer.
- anthropic.com/engineering/how-we-contain-claude, anthropic.com/engineering/managed-agents: fetched directly.
- code.claude.com docs (memory, permission-modes, sandboxing): fetched directly.
- openai.com pages returned 403; read from Internet Archive copies of the same URLs (`web.archive.org/web/2026id_/…`).
- Codex docs (learn.chatgpt.com/docs/sandboxing) fetched directly; `on_request.md` read at commit `ba2b67f` via the
  GitHub API. OpenAI conversation-state docs fetched directly.
- GitHub issues: title, state and state reason via `gh api`; bodies not read.

## 5 · Adversarial questions, answered

- **A behavioural result written as a mechanism?** No. §4 and §8 both say the data are behavioural, and the
  J-space section says nobody has looked for a permission representation.
- **Correlation written as causation?** The grant's effect at turn 3 is an arm contrast (3/3 vs 0/6); later-turn
  persistence is stated as uncontrolled.
- **"Model obeyed" written as "model is safe"?** The coda says it is not a guarantee and should not be built on.
- **A killed or retired claim revived?** FTR's strong form is named and explicitly not restored under the
  "structured possible futures" description.
- **An OPEN item written as established?** "Authorization is more robust than other rules" is OPEN in §4 and §9.
- **Prior art hidden?** The deference/enforcement distinction is marked PRIOR ART with three sources.
- **Unresolved.** The raw census is withheld for privacy; its one-off share was recomputed locally but cannot be
  recomputed by readers.
