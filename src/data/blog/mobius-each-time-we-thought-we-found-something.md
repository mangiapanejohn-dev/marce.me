---
title: "MØBIUS — What Happened After Each Time We Thought We Had Found Something"
description: "The full research record of 18–22 September: the approval line's last two residuals, evidence selection in completion judgement, completion attribution, transition witnesses, late-bound obligations, Jepsen-style probes across agent runtimes, Delegated Obligation Closure, and the reduction gate for the strong form of FTR. Every step keeps its prediction, measurement, interpretation, correction and final status — including our own instrument's mistakes. The conclusion: there is no primary thesis yet that I am willing to call a new systems abstraction."
pubDatetime: 2026-09-22T16:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research", "Negative Results"]
category: "research"
series: "MØBIUS"
timezone: "America/New_York"
showInBlog: true
---

The previous MØBIUS post went out on 19 September. It ended by saying that FTR had killed itself under investigation but that the question which produced it had not died, and it listed a queue: evidence horizon, transition-dependent completion, unsupported establishment, certificate replayability, anticipatory evidence preservation, future information requirements.

This post records what happened after that, from 18 to 22 September (one day overlaps the last post, because the research lead's line started on the 18th), plus a forensic pass I ran to write it. It is not a progress report. More than a dozen candidate directions were proposed, tested and given a status in those days (Figure 1 lists fifteen). Six were reduced **in the same shape**, and two more lines were stopped or killed directly by cross-runtime experiments. As of today none has survived to become a primary thesis.

I want this to read as a research record, not as "what we found". So every candidate keeps, as far as possible, five links:

| link | meaning |
|---|---|
| **prediction** | what was expected before measuring, and the kill criterion |
| **measurement** | the number actually obtained, and the file it came from |
| **interpretation** | how the number was read at the time |
| **correction** | where the reading (or the number) later turned out wrong |
| **final status** | today: <span class="st st-killed">KILLED</span> <span class="st st-retired">RETIRED</span> <span class="st st-prior">PRIOR ART</span> <span class="st st-measured">MEASURED</span> <span class="st st-open">OPEN</span> <span class="st st-ne">NOT EVALUABLE</span> |

Whatever credibility this post has can only come from that chain, not from how tidy the last version looks. Wrong predictions, withdrawn verdicts and bugs in our own harness all stay in.

**"I" and "the research lead".** Most of the measurement and literature reduction in this period was done by an independent research-lead agent I run in Claude Science; the directions, the kill criteria and when to stop were mine. "I" is me; "the research lead" is that agent. Its ledger is a handful of files: `RESEARCH_MAP.md` (§0–§40), `TRACKS.md`, `INVARIANT_CARDS.md`, `PILOT_RESULTS.md`, `C1_RESULTS.md`, `C2NI_RESULTS.md`, `FTR_REDUCTION_GATE.md`, and the pilot harness's `rows.jsonl`. MØBIUS's experiment journals are in the repository under `docs/research/evidence/` (104 `events.json`). The repository is private for now, so this post names files, commits and directories rather than linking them. **Every number below was recomputed for this post from those raw files**; where the recomputation disagrees with the ledger, the text says so.

External literature and API contracts were all re-opened at their primary records on 22 September: arXiv pages, DOIs, publisher pages, official documentation and installed package source. The depth of each check is marked in the references: `FULLTEXT`, `ABSTRACT-ONLY` or `UNVERIFIED-FULLTEXT`.

<figure class="fig">
<a href="/research/mobius-rl-graveyard.svg"><img class="fig-light" src="/research/mobius-rl-graveyard.svg" alt="Timeline of candidates from 18 to 22 September. One row per candidate: approval-line residuals, evidence substitution, transition witness, evidence selection, verification-input ownership, completion attribution, criterion-directed active observation, temporal witness lifecycle, late-bound obligations, recovery closure, correctness-under-adoption, delegated obligation closure, the strong form of FTR, and the direction discovery still running. Each row shows what attacked it and its status today; almost all end retired or killed, and the last row reads NO PRIMARY THESIS YET." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-graveyard-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 1.</strong> The research trajectory of 18–22 September. Each row is one candidate: what it was, what attacked it, and its status today. It is deliberately not a roadmap: most branches terminate on the right. It shows what these directions went through; it does not show that the killed ones have no engineering value.</figcaption>
</figure>

## 0 · From features to the runtime

MØBIUS started out growing by features: a planner, subagents, skills, a harness. None of the failures that actually stopped me was a missing feature. They lived between features: a person approves an effect, the world changes while they wait, and the approval is reused anyway; a task is declared complete, and the evidence of completion is an expectation it wrote itself; after a resume, a counter that should have been durable is back at its initial value. So the question slowly turned from "add one more capability" into the runtime's own objects: **state, evidence, authority, freshness, verification, replay, completion, failure semantics**.

Early on I got excited whenever a structure "looked like nobody does it this way". The approval line in the last post started exactly like that: I believed that binding a person's approval to the version of the world it was about was a new mechanism. It was reduced to the third instance of a design family [[1]](#ref-1) [[2]](#ref-2) [[3]](#ref-3) [[4]](#ref-4).

After that I set myself a rule, and every candidate in this post is judged by it:

> Without a prior-art reduction, a falsifier and an observable consequence, it is not a research result.

The rule was written before these days. What these days did was apply it for the first time without discount.

## 1 · The approval line's last two residuals (18–19 September)

The last post already reported the approval line as a whole reducing to prior work. Two residuals were left after that, and the research lead dealt with them as well. I put them first because they established the shape that keeps coming back.

**Residual A: effect shapes with no content precondition.** In a surface census of four systems, 13 of 16 mutating tool paths carry no per-call content precondition (an `old_str`, an `If-Match`), and none of the 11 non-file paths (DOM clicks, shell) carries one. For a while this was treated as the region only MØBIUS's mechanism covered.

Then someone (me) pointed out that "the target has no prior content" is not "there is no expressible precondition". Creating a file can be preconditioned on its absence: `If-None-Match: *`, `O_EXCL`, GCS's `ifGenerationMatch=0`. CommitGuard's witnesses are versions or epochs rather than contents, and its list of coupling primitives includes the conditional write [[1]](#ref-1). Back in MØBIUS's own filesystem provider, the freshness guard reads `if (basis && basis.freshness !== 'advisory' && existedBefore)`: when the file does not exist the whole check is switched off, and the write that follows does not use `O_EXCL`. `fs.move` checks the destination and then calls `rename`, with a check-then-act window in between. CommitGuard explicitly excludes "runtimes without an atomic check-and-commit primitive" from its guarantee, and MØBIUS falls in exactly that class — by an implementation choice, not for want of an underlying primitive. **Residual A is killed**; what is left is a one-flag engineering defect.

**Residual B: who produces the validity key.** PlanFence uses the dependency set a tool declares, and measures unsafe issuance rising under omission (37.4% at $$p = 50\%$$, in a setup where three of four true dependencies are each omitted with probability $$p$$) [[2]](#ref-2); MØBIUS's ADR 0041 has the runtime take a look of its own. That looked like an axis worth writing up — until S-Bus, whose title is *Automatic Read-Set Reconstruction*: it rebuilds each agent's read set on the server from HTTP traffic and names the property Observable-Read Isolation [[3]](#ref-3). **Residual B is occupied.** On 22 September we also read ATR, which separates "the version changed" from "the change invalidates the action's justification" as version conflict versus decision conflict, and rechecks only the affected conditions [[5]](#ref-5) — taking the last piece of phrasing the approval line had left, "revalidate the premise, not the effect".

The lesson of this section is not in any mechanism but in something more embarrassing: the approval line's own decision units (S2, S10, S15, VB-1, VB-2) **always compared against earlier designs of MØBIUS itself**, and never against these published systems on the same grid. When the research lead encoded CommitGuard's predicate as a rule and ran it over VB-2's 36 cells, it gave 0 unsafe permits on MØBIUS's own separation grid, against 9 for the shipped mechanism. That is a predicate-level comparison, not a system-level one, but the direction is clear.

## 2 · Completion judgement: the evidence was in the journal, and the judge did not see it (18–20 September)

### Starting from false success

On R2's six multi-step tasks, the checker passed 0 and the runtime declared 5 complete. Every false completion went the same way: a read whose proposer-written expectation held (`content exists`) closed a success criterion that had no assertion, through ADR 0031's rule. One task read a file, wrote nothing, and was "complete".

At first I took this as the most underrated observation in the project and called it "evidence substitution". It was reduced the same afternoon: Advani named the phenomenon false success, measured it over thousands of trajectories on tau2-bench and AppWorld, and wrote down exactly R2-6's shape — agents read the environment without modifying it and then claim completion [[6]](#ref-6). R2 is a replication, not a discovery.

### The judge and `cannot-tell`

ADR 0043 introduced an independent judge: a separate model call that sees only the criterion and the evidence, never the proposer's expectation. False completions went from 5/6 to 0/6, but the runtime also almost stopped completing multi-resource work. Across all committed journals the judge ruled 133 times: established 21, not-established 24, **cannot-tell 88**.

The research lead classified the reasons of the 88 `cannot-tell` verdicts one by one (the test: "could a fresh look at the world now obtain this fact?"), giving (measurement, recomputed from `cannot_tell_classified.json`):

| class | n | share |
|---|---|---|
| **T_TRANSITION**: what is missing is a relation between past and present | 51 | 58.0% |
| A_MORE_LOOKING: one more read of the current world decides it | 31 | 35.2% |
| S_SHAPE: the fact is in the observation but the evidence projection drops it | 4 | 4.5% |
| other | 2 | 2.3% |

And T_TRANSITION concentrates in three tasks of unrelated shapes: **rename 13/13, config edit to a spec 19/22, split a file 19/32**. All three have completion criteria that assert something about a change: archive.txt holds the **former** content of notes.txt; settings.ini reflects the spec **and nothing else changed**; each section of the **old** notes.md is its own file.

The decisive check was one T4-rename journal: event [7] observes `notes.txt` with digest `sha256:6862e454…`; [10] is `fs.move`; [17] observes `archive.txt` with the same digest. The judge said three times that it could not tell, because "no evidence records what notes.txt formerly contained". The criterion is decided mechanically by one digest comparison, and both digests were in the journal.

This is where the last post's *transition witness* came from. It failed three kill tests in one pass: it is a before-image plus a provenance edge plus a past-time operator; past-time temporal logic exists precisely for assertions about change [[7]](#ref-7), and WAL undo records [[8]](#ref-8), valid time in temporal databases [[9]](#ref-9) and provenance [[10]](#ref-10) cover the rest. <span class="st st-retired">RETIRED</span> as a primitive. That verdict is already public, so I will not expand it here.

### The first key correction: the information was not lost, it was not delivered

The next step matters for every step after it.

The research lead first ruled out two explanations that need nothing new. **Judged too early?** Of the 86 `cannot-tell` verdicts whose reason names a specific file, 84 (98%) had that file observed **before** the verdict, and 0 never had it observed. **Too little bound?** `cannot-tell` verdicts bind 2.43 pieces of evidence on average and `established` 2.48; the count does not separate them.

What separates them is another quantity. For the 106 verdicts whose criterion names specific files, compare coverage of those files by **the bound evidence** and by **the observations already in the journal at the time**:

| verdict | n | bound evidence covers what the criterion names | already in the journal |
|---|---|---|---|
| `cannot-tell` | 77 | 66% | 100% |
| `established` | 15 | 93% | 100% |
| `not-established` | 14 | 93% | 100% |

Availability is 100% in all three classes; **selection** separates them. In the source, `ActionIntent.satisfies` is a field in which the proposer declares which criteria its own action satisfies, and `#bindClaimed` routes observations to criteria by it. The project had already named and repaired two failures of this design — an empty `satisfies` means completion never fires, and "the proposer is the completion oracle" — but not the third: `satisfies` non-empty and pointing at the wrong thing. The independent judge settled **who rules**; it did not settle **who decides what the judge sees**.

> "Missing evidence" and "evidence exists but is not delivered" are completely different problems. The first needs new capture; the second only needs different routing. Every later candidate in these days had to say first which of the two it was.

### A pre-registered experiment that hit — and was then trimmed by our own accounting errors

**prediction** (written on 20 September before the run): if evidence binding moves from the proposer's declaration to "the runtime derives it from what the criterion names", `cannot-tell` should fall substantially, by about 93% − 66% = 27 points. Three arms share a judge predicate and rendering reconstructed verbatim from source: C (the original binding, as a validity gate), T (derived from referents), R (random observations, as many as T, as a count control).

**measurement, first round**: 32.4 pp observed — a hit. But the validity gate reached only 64.2%: with the same evidence, our judge was far more lenient than the original (of the 77 verdicts that were originally `cannot-tell`, arm C called 36 established). The cause was found quickly: we had used a judge one tier weaker than the original run's. **This round's absolute rates are void.**

**measurement, second round**: the original judge model is recorded in the corpus itself — the `models` field of all 96 `results.jsonl` rows is `claude-opus-5`. Rerun with that model, the validity gate reaches 79.2%, and:

| arm (77 verdicts originally `cannot-tell`) | still cannot-tell | vs C |
|---|---|---|
| C proposer's binding | 77.9% | — |
| T derived from referents | 20.8% | **−57.1 pp** |
| R random (more evidence than C) | 88.3% | +10.4 pp |

Arm R has more evidence and does worse: **irrelevant evidence is not neutral; it dilutes.** Split by corpus commit, the difference is 58.8 pp on `f9b27dd`, where ADR 0045 is in effect (n=68), and 44.4 pp on the earlier `33e599e` (n=9); the second sample is too small for the two to be a comparison. In other words, the effect size is a residual **on top of** a partial fix the system had already adopted.

**correction**: the table is followed by two accounting errors of our own. First, comparing mid-run verdicts against the checker's task-level result is wrong — the checker grades the final world; the fix is to take only the last verdict per (run, criterion). Second, the first grouping stripped the criterion id and gave n=18; the right number is n=22. After the fixes, T's net effect is `cannot-tell` 9→4 and established 12→16, **at the cost of not-established 1→2**, one of which, in R2-2-module, is a false negative that persists to the last verdict: the original judge, arm C and the checker all say the criterion holds, and arm T says it does not in all five rulings from e7 to e52. We had also written "T has zero not-established on last verdicts"; that number was computed on a subset, and is withdrawn.

Three more selector arms followed (T2, T2′, T3). T3 (per referent, the first observation plus the latest one after the last effect) reaches both the history arm's and the snapshot arm's upper bounds on the verdict that decides completion, and does worse than T on mid-run verdicts (42.9% against 20.8%). Two by-products are worth recording: adding a one-line annotation `(most recent observation…)` to evidence items is by itself worth about 12 pp — a confound manufactured by the evaluation instrument; and telling the judge "there is a gap here" changes nothing (the `cannot-tell` rate with and without the gap item is 33% in both). All three arms ran on the same small set, which is already researcher degrees of freedom. The research lead stopped at T3, and I agreed: any more tuning would be fitting these 106 verdicts.

### Cross-system: first a failure, then a partial pass

**The first attempt failed, and the way it failed was informative.** The external corpus was 6,670 SWE-agent trajectories. On a balanced sample of 200, arm A gave the judge the agent's own narrative and arm B a mechanically extracted diff. B was more accurate (55.0% against 48.8%) with the shortest evidence, but only by 6.2 pp; more importantly, **the independent variable had been swapped**: MØBIUS's intervention is "the same kind of evidence, a different selector", while an SWE-agent task is issue prose with no mechanically matchable set of referents, so the only B available was the diff — the variable became "state versus narrative", which is a different claim, the one the false-success paper already measured. Arm B also failed to parse in 37/200, so A and B could be compared on only 160. **Not a pass.**

**The second attempt passed at the mechanism level.** Restating the claim in a portable form — "does the judge's evidence coverage depend on the choices of the party being judged?" — immediately found a second host in browser-use: its production path has an independent judge whose textual evidence is the agent's own final message plus the returns of actions the agent chose; the only evidence not authored by the agent is the last few screenshots; the verdict is a boolean with no third value; and the prompt says that if the agent extracted information the screenshot does not show, the judge can assume it is there [[11]](#ref-11). Both systems leave evidence coverage to the judged party and differ only in how they absorb the uncertainty: MØBIUS fails closed and pays in liveness; browser-use fails open and pays in reliability.

**The third attempt passed partly at the effect-size level.** On a public trajectory set in browser-use's schema (webarena-infinity, successful trajectories only), 25 samples under the same judge predicate: fed only the agent's own text, established 3/25; fed only the last 3 screenshots, 15/25. The 3/25 is partly definitional — the predicate says outright that claims are not evidence, so a judge fed only claims cannot rule; the defensible reading is "agent-authored text contains almost nothing that is not a claim". Stratified by whether the instruction contains a universal or extremal quantifier (every, only, highest…), the screenshot arm's decidability drops from 13/17 (76%) to 2/8 (25%): a fixed-size evidence window cannot cover an unbounded or multi-page set of referents. **But the false-positive direction cannot be measured** (the corpus has only successes), and that is precisely the risk browser-use's design takes. And the MØBIUS result that "a complete final snapshot decides 0 of 9 cross-time criteria" did **not** replicate here (cross-time 2/7 undecided, state 7/18): these are the last 3 frames, not a single snapshot, so that conclusion holds only for "final snapshot only".

### Reduction: monitorability, and useful ≠ novel

On the morning of 22 September the research lead ran a prior-art gate on this line. Bollig's lecture notes on runtime verification give three-valued verdicts like `cannot-tell` an epistemic semantics (true when $$K_a\hat\varphi$$, false when $$K_a\neg\hat\varphi$$, otherwise inconclusive), define "can this observer decide it" as monitorability, and prove it decidable [[12]](#ref-12); the classical definition of monitorability is older [[13]](#ref-13) [[14]](#ref-14). A snapshot failing to decide a cross-time criterion is textbook past-time modality.

The reduction exposed one interesting seam: in the notes, each agent's set of observable propositions $$AP_a \subseteq AP$$ is **a fixed system parameter** [[12]](#ref-12), while in MØBIUS and browser-use the effective $$AP_a$$ is chosen at run time by the party being judged. Noisy-RV frameworks handle observations corrupted by noise, not an observation scope chosen by one of the parties [[15]](#ref-15).

$$
\mathrm{Mon}(S,\varphi \mid AP_a) \quad\longrightarrow\quad \mathrm{Mon}(S,\varphi \mid AP_a(\pi))
$$

<div class="eq-note">

On the left, the object of the standard theory: a fixed observation alphabet. On the right, what actually happens in an agent runtime: the alphabet depends on the judged party's policy $$\pi$$. No theorem is claimed; only that the standard theory's precondition does not hold in these systems.

</div>

I called this **verification-input ownership**: the verifier's inputs are decided by the party being verified. It is a level above "make the LLM judge more accurate", and it came with 58.8 pp on one system and 76%→25% on a second.

As the main novelty it lived about two hours. First cut: RTLola's active monitoring, in which the monitor **itself decides**, from the specification and its internal state, which sensors to query and how often [[16]](#ref-16) — the general idea that "a verifier should not let the verified system decide what it observes" is already there. Second cut: Goal-Autopilot externalises a natural-language goal as a gated state machine and forbids declaring done unless a falsifiable gate actually executed and passed [[17]](#ref-17). The third and most damaging, IRA: the evaluator generates completion conditions from the task instruction and then **itself chooses** system, application and GUI tools to gather evidence from the environment, with 86.9% accuracy on 321 trajectories [[18]](#ref-18). And one cut came from ourselves: MØBIUS's ADR 0021 §4 had written on 13 September that "a runtime-owned look remains the better long-term answer … It is named, not taken", and ADR 0041 took it on the 18th.

So **criterion-directed active observation** cannot be the headline. It is not useless — the 57.1 pp is real, and so is browser-use's fail-open prompt — but:

> **useful ≠ novel.**

| link | record |
|---|---|
| prediction | routing by referent lowers `cannot-tell` by about 27 pp |
| measurement | 32.4 pp (weaker judge, gate 64.2%, absolute rates void) → 57.1 pp (original judge, gate 79.2%); 58.8 pp on top of ADR 0045, n=68; browser-use coverage 76%→25% |
| interpretation | the judge's inputs are chosen by the judged party; $$AP_a$$ is endogenous |
| correction | two accounting errors (n=18→22; mid-run verdicts compared with the checker); T has a persistent false negative; the SWE-agent replication swapped the variable; the cross-time prediction did not replicate on the second system |
| final status | <span class="st st-measured">MEASURED</span> kept as a measurement dimension; <span class="st st-prior">PRIOR ART</span> as a mechanism (active monitoring, IRA, Goal-Autopilot, ADR 0021/0041) |

## 3 · Completion attribution (morning of 22 September)

### The question

If a third party produces the goal state while the agent is waiting, and the completion judge only sees that the goal state holds, does the agent receive credit for something it did not do?

$$
\mathrm{Goal}(S_t) = \mathit{true} \;\not\Rightarrow\; \mathrm{AccomplishedBy}(\mathit{run}, \mathrm{Goal})
$$

It looks as if this needs causal attribution: the evidence the judge receives is only observations, never "this state was caused by this effect of this run". For action safety that half had long been answered by ATR: another writer's change only has to invalidate the justification; nobody needs to know who wrote it [[5]](#ref-5). What remained was the completion half.

**An existence check came first, offline.** Rebuilding per-path digest timelines across the 104 journals and looking for "the digest changed while no effect of this run touched the path" found 6 instances, all from the same injection fixture (`config.json` in the world-moves experiment family), and zero in the other 98 journals. In 5 of the 6 the runtime re-escalated or suspended (it already fails closed on "the world moved during an approval wait"); 1 completed, but its final state was written by the agent itself. **No instance in the corpus had misattribution change a completion verdict** — the injected change was never the goal state, so the decisive cell did not exist by construction. That is a missing test, not an absence.

### Pre-registered: predicted from source to rule `established`

Reading the source, the research lead wrote down a definite prediction: the judge's evidence type `JudgedEvidence` has only `{id, what, content}`, and all three of its sources are reads, none an effect, so at the type level the judge cannot tell "I caused this" from "someone else did"; yet the runtime knows exactly which of its effects touched which resource — it uses that to drop stale observations, and the source comment even says *"A foreign change after an observation is not known here; this is a completion judgement, not a gate."*

> **prediction**: G-ext will rule `established`; the cause is a fact captured but not delivered to its consumer — the third instance of "evidence exists but is not delivered".

### The prediction was refuted by its own experiment

The repository was read-only and the injection fixture could not be changed, so the test was a faithful offline simulation with the judge rebuilt from source: 21 (run, criterion) pairs from 5 tasks, all checker-passing last verdicts, with the real contents of the files each criterion names as evidence. Four arms differ by one extra evidence item:

- N: no causal information
- S: "This run dispatched `fs.write`; the content above is what this run's own effect wrote"
- F: "This run dispatched no effect touching these paths; the content above was written by a different writer"
- Z: "This run dispatched no effect touching these paths"

**measurement** (recomputed from `gext_offline_four_arm.csv`): arms N, S and F all give established 10, cannot-tell 11. **F equals N case by case 21/21, and F equals S 21/21**; 19 of the 21 F-arm reasons do not mention the causal item at all.

With the causal term explicitly supplied, not one verdict moved. It is not that the judge distrusts it; it is **irrelevant**: none of the 21 criteria contains a single word referring to an agent — *notes.md is an index linking the three files*, *settings.ini reflects every change SPEC.md lists*. The judge was asked about a proposition about the world, saw it hold, and answering established was **correct**.

Then only the shape of the criterion was changed, with the evidence untouched: every criterion got the same prefix, *This run's own effects brought about the following state of the world:*.

| | caused by this run (S2) | caused by another (F2) |
|---|---|---|
| state predicate (as is) | established 10 | **established 10** |
| accomplishment predicate (prefixed) | established 10 | **not-established 20**, cannot-tell 1 |

In the honest case S2 equals S case by case, 21/21 — the rewrite introduces no false negatives; in the other-writer case 20/21 flip to a denial. To rule out "a longer prefix just makes the judge stricter", a length control used a prefix of the same length with no agent in it (*The following state of the world holds:*): the F arm matches the baseline case by case, 21/21. Three different agent-bearing wordings all flip the F arm (notEst 18, 21, 18). In that rerun the original wording's F arm gave 18/21 rather than 20/21; I keep both numbers. The flip holds under every wording, but wording affects the cost in the honest case (two wordings introduced one or two false negatives in arm S).

**correction**: completion attribution is **not an evidence problem but a specification problem**. The source-level mechanism ("the judge lacks a causal term") is void.

### Why it retired

Written as a formal problem, the reduction is complete: "which agent caused this outcome" is actual causality [[19]](#ref-19) [[20]](#ref-20), and it has been treated together with responsibility attribution on Dec-POMDPs — multi-agent, partially observable, sequential decisions [[21]](#ref-21). On the trajectory side, process-mining conformance checking has been used to measure the fidelity of agent workflows, finding 10 of 18 models systematically skipping a confirmation checkpoint [[22]](#ref-22); it solves attribution implicitly (it only looks at the agent's own trajectory), at the price of needing a reference trajectory and not verifying the world.

There is also a competing explanation nobody killed: "if the goal holds, who did it does not matter". Its signed supporter is MØBIUS's own source comment — **a completion judgement is deliberately not a gate**. The situations where attribution really matters (truthfulness of reports, credit assignment, rollback scope, training signal) are none of them failures of completion judgement itself.

Three narrow things remain: 0 of 42 success conditions across two systems and three kinds of verifier refer to an agent (I reran a text search for this post; its one hit was the job title *Senior Agent*); MØBIUS's assertion language cannot express an accomplishment predicate at the type level (its only temporal operator, `changed`, is satisfied by another writer too); and the table above. Together: a cheap correctness improvement nobody has adopted, plus a measurement — an engineering recommendation, not a mechanism contribution.

| link | record |
|---|---|
| prediction | G-ext rules established because the judge's evidence has no causal term |
| measurement | causal term supplied: F==N 21/21; accomplishment predicate: F2 flips 20/21 (rerun 18/21), S2==S 21/21; length control unchanged 21/21 |
| interpretation | the judge lacks causal evidence → **wrong**; the criteria are state predicates |
| correction | the mechanism moves from "evidence pipeline" to "specification shape"; the original prediction is void |
| final status | <span class="st st-retired">RETIRED</span> to actual causality / conformance checking; kept as an engineering recommendation |

## 4 · The last form of the transition witness: Late-Bound Witness Obligations (morning of 22 September)

### R2-6-split: more and more evidence, less and less decidability

After completion attribution retired, the ledger still held one real non-monotone instance. In R2-6-split's first repetition, the verdicts on criterion c1 (*each section of the old notes.md is its own file under notes/*) were:

<figure class="fig">
<a href="/research/mobius-rl-r26-split.svg"><img class="fig-light" src="/research/mobius-rl-r26-split.svg" alt="Verdict timeline for criterion c1 in R2-6-split repetition 1: events 8, 23, 47 cannot-tell, 57 established; 65 rewrites notes.md into an index with a basis pointing at the full read at 64; 78 the first run is stopped by the repeat guard; 79 a second run begins; 87, 98, 105, 116 cannot-tell with 1, 2, 3 and 8 bound pieces of evidence. Below, four successive explanations: binding narrowed (wrong), pre-state destroyed (wrong), filtered by a staleness rule (partial), run boundary plus latest-per-resource (consistent with journal and source)." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-r26-split-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 2.</strong> Every verdict on criterion c1 in R2-6-split repetition 1 (<code>evidence/r2/f9b27dd/P3-judge-run-b/R2-6-split/rep-1</code>), by journal event. After [57] rules established, [65] rewrites notes.md into an index, the first run is stopped by the repeat guard at [78], and a second run begins at [79]. The four verdicts after that are all <code>cannot-tell</code>, while the bound evidence goes 1→2→3→8. The four rows below are the explanations given for this, in order; only the last is consistent with both the journal and the source.</figcaption>
</figure>

**"The evidence binding got smaller" was the first explanation we wrote down.** The ledger's 07:24 version on 22 September says the cause of this flip back was "the evidence binding narrowed". That sentence was never computed. Eight minutes later the next version counted: the binding went **1→2→3→8**, growing. So the explanation changed to a second one: the run itself later rewrote notes.md into a three-link index and **destroyed** the pre-state that verdict depended on.

At that point I found it beautiful: a temporal proposition that had already been established, whose only witness was destroyed by later execution. **More evidence, less ability to decide.** I called it the Temporal Witness Lifecycle.

### First absorbed by 1996

The research lead reduced it. IRA gathers evidence actively on the post-execution final state [[18]](#ref-18), and so by construction cannot handle "the witness a verdict needs no longer exists during execution" — a separation established by IRA's own formalisation. But the solution structure had a formal theory long ago: whether a materialised view can be maintained without accessing the base data [[23]](#ref-23); and deriving **auxiliary views** so that the warehouse view together with them is **self-maintainable** [[24]](#ref-24). Item by item: the criterion's truth is the materialised view, the world is the base data, a destroyed pre-state is an unreachable source, and the minimal frozen witness is the auxiliary view. "Keep minimal auxiliary state rather than copying all history" was argued in 1996. (Only abstract-level and secondary descriptions of these two papers were available; they are marked `UNVERIFIED-FULLTEXT`.)

My two remaining intuitions each hit older work too: "the monitored objects are unknown at the start and a monitor is instantiated when a concrete value appears" is parametric trace slicing [[25]](#ref-25); "old state disappears, so the monitor must keep enough of the past" is the core of past-time monitoring [[7]](#ref-7).

### Then narrowed into a form data could kill

One seam remained. Parametric RV assumes the event has happened, the event carries the parameter value, and then a monitor is created. Here a more dangerous order might exist — **a resource's identity first becomes resolvable only when the effect that will destroy its pre-state is proposed**. If the runtime binds the parameter only after the event, it is already too late.

I wrote it like this. Let $$C$$ be the success criterion and $$B_t$$ the referents resolved up to $$t$$:

$$
O_t = \mathrm{Obligations}(C, B_t)
$$

When effect $$e_t$$ is proposed it exposes its footprint $$F(e_t)$$, and the binding may grow:

$$
B_{t^+} = \mathrm{Resolve}\big(C,\ B_t,\ F(e_t)\big), \qquad \Delta O_t = O(C, B_{t^+}) - O(C, B_t)
$$

If $$e_t$$ destroys the pre-state these new obligations need, then

$$
\mathrm{Destroys}(e_t, \Delta O_t) \;\Rightarrow\; \mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)
$$

<div class="eq-note">

Binding and instrumentation happen on both sides of the effect boundary, rather than in ordinary RV's event-after-the-fact model. MØBIUS's existing <code>#targetedLook</code> can insert a look before the world is actually changed; the question this form asks is whether that look's resource set can be derived from the criterion's late-bound obligations.

</div>

The first time I wrote $$\mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)$$, it felt as if this might be the thing.

So the next step had to be finding the data that could kill it, not writing an implementation. The kill criterion was written before the measurement:

> Classify every (criterion, changed resource) pair: `STATIC` (resolved when the criterion was created), `LATE-SAFE` (resolved later, before any destructive effect), `LATE-CRITICAL` (resolved only when an effect's footprint appears, and that effect immediately destroys the needed pre-state), `UNBOUND`. **If `LATE-CRITICAL` essentially does not exist, the line retires.**

The research lead also wrote its own expectation before measuring: `LATE-CRITICAL` near zero, because what binds late in R2-6-split is the **new filenames** under `notes/`, while the pre-state destroyed is the literally named `notes.md` — the two fall on different resources.

### LATE-CRITICAL = 0 / 165

<figure class="fig">
<a href="/research/mobius-rl-late-bound.svg"><img class="fig-light" src="/research/mobius-rl-late-bound.svg" alt="Matrix of 165 criterion–resource pairs. STATIC 126, LATE-SAFE 12, LATE 27; none of the LATE resources existed before, so LATE-CRITICAL is 0 of 165. Side notes: pre-state captured for 109 of 109 pairs on pre-existing resources; 75 of 75 overwrites of existing files carry a basis observation." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-late-bound-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 3.</strong> 165 (criterion, changed resource) pairs, by when the resource was first resolvable and by "does the criterion need the pre-state × did the resource exist before". The <code>LATE-CRITICAL</code> cell is 0. All 27 late-bound resources were newly created; for resources that existed before, the pre-state was captured 109/109. Recomputed from <code>late_bound_obligations.csv</code> and the 104 journals. What it shows is that the execution this theory guards against did not occur in this corpus; it does not show that it cannot occur in other workloads.</figcaption>
</figure>

**measurement** (165 pairs from 65 journals and 102 criteria, recomputed for this post):

| binding time | n | resource existed before | criterion needs pre-state and resource existed |
|---|---|---|---|
| STATIC | 126 | 97 | 47 |
| LATE-SAFE | 12 | 12 | 0 |
| LATE | 27 | **0** | **0** |

- **`LATE-CRITICAL = 0 / 165`**. Remeasured with a harsher definition (pre-state existence taken from the effect's own receipt, so that "the file had content, the runtime never observed it, and the effect overwrote it" cannot be misfiled): still 0/165.
- **All 27 LATE bindings have `pre_existed = false`**: in this corpus a late-bound resource is always a new one, with no pre-state to destroy. This is the other face of what was measured on 19 September — the write set of creations cannot be predicted, because the path does not exist yet.
- For the 109 pairs on pre-existing resources, **109/109 had the pre-state captured by the runtime** (57 through the effect receipt's `previousDigest`, 52 through an earlier observation). The unit here is (criterion, resource) pairs; in deduplicated effects it is 75 applied writes over existing files, and **75/75** have a `basis` pointing at an earlier observation, 55 of which are full-content file reads.
- More generally, **107 of 120** dispatched `fs.write`/`fs.patch`/`fs.move` carry a `basis.observationId`. The ledger calls all 120 "destructive effects"; that is too broad — 36 of them are creations and 9 were refused. I use the narrower numbers above.
- The sharpest one: the `fs.write` at R2-6-split event [65] that rewrites `notes.md` has a `basis.observationId` pointing at a full read at event [64] — **the full text of the old notes.md is in the journal, pointed to by the very effect that destroyed it.**

The theory itself is beautiful. But data has no obligation to respect beauty. The existing look-before-change discipline (ADR 0020, 0021, 0041) already turns every late-bound resource into `LATE-SAFE` before a destructive effect lands, and the truly late-bound resources are all new.

### The second, third and fourth explanations

**interpretation (ledger §40.2)**: the witness was not destroyed; it was **filtered out** by a staleness rule in ADR 0045 — the judge's view takes the latest observation per resource and explicitly leaves out "what this run's own effects have made stale". Right for a gate, that rule happens to filter out the only evidence a cross-time criterion has.

**correction (found while checking the journal for this post)**: §40.2 is missing a step. The first run is stopped by the repeat guard at event [78] (`goal.abandoned`, *"fs.observe was already read in this run with the same arguments"*); from [79] on it is a **second run** of the same task — the session changes from `session-8` to `session-9` and observation numbering restarts at 1. All four `cannot-tell` verdicts after the rewrite happen in the second run, and `#runView` in `runtime-core/src/loop.ts` walks only **this run's** `#observations`. The engineering side had actually written this on 19 September in the R3 plan (F3): *"Those judgements came in the mission's second run, whose view holds only that run's observations"*, noting that within one run the staleness rule would "also" leave the pre-state out, but that this was read from code, not measured. So the accurate statement is: the old notes.md is in the journal, pointed to by [65]'s basis, and was not delivered to the judge because of **the run boundary** (and, within a run, the latest-observation-per-resource and staleness rules).

The four explanations in order: the binding narrowed (never computed; wrong) → the pre-state was destroyed (wrong; the content is in the journal) → it was filtered by the staleness rule (partly right) → the run boundary plus the latest-per-resource rule (consistent with journal and source). They all point to the same category: **evidence exists but is not delivered**. And that is a defect in an ADR's rule — engineering, not a new abstraction.

| link | record |
|---|---|
| prediction | research lead: `LATE-CRITICAL` near zero; kill criterion: retire if essentially absent |
| measurement | 0/165; still 0/165 under the harsher definition; 27/27 LATE are new; pre-state captured 109/109 pairs; 107/120 carry a basis |
| interpretation | Temporal Witness Lifecycle → auxiliary views (1996); Late-Bound Obligations → does not occur |
| correction | "binding narrowed" → "pre-state destroyed" → "filtered by the staleness rule" → "run boundary" |
| final status | <span class="st st-killed">KILLED</span> at the existence gate; <span class="st st-prior">PRIOR ART</span> for generic witness preservation (auxiliary views, WAL, past-time RV) |

At this point the research lead wrote a table into the ledger: the same shape had now appeared five times — **the theory exists and is more general than needed, and the runtime implements neither the general solution nor the cheap special case.** It wrote that it would open no new candidate abstractions along this line. The sixth came in the afternoon.

## 5 · Changing the method: from inventing mechanisms to Jepsen-style probes (22 September, 08:51)

After five reductions in the same shape, I formally changed direction: no more digging a sixth mechanism out of MØBIUS's correctness bugs, but a systems question data could kill directly.

One more direction was reduced along the way at this point. After ADR 0013, a resume resets the run-local `#ledger` to zero, which really does break semantics; but "every piece of state that affects future control flow must be durable across a resume" is the basic requirement of durable execution — AWS's documentation even gives an isomorphic example: a step appends to an outer variable, the step is skipped on replay, and the variable stays at its initial value [[26]](#ref-26); and work that explicitly names re-consuming an authorization budget after crash, retry or replan as **semantic replay** already exists [[27]](#ref-27).

So "five reductions in the same shape" was rewritten as a research question:

> To what extent do modern agent runtimes re-expose correctness problems that classical systems theory solved long ago? Why do those failures reappear, and at which runtime seams do they concentrate?

The candidate explanation fit in one line:

$$
I \text{ requires } F \;\wedge\; F \in S_i \;\wedge\; F \notin \pi_{i\to j}(S_i) \;\Longrightarrow\; I \text{ may fail at subsystem } j
$$

<div class="eq-note">

$$\pi_{i\to j}$$ is the projection at a subsystem boundary. A fact existing somewhere in the runtime does not imply the invariant is enforceable at its consumer. The ledger's instances at the time: the journal has provenance and the extractor drops it; an effect's basis holds the old observation and the completion evidence filter drops it; the runtime has effect attribution and the criterion does not ask for it; the resume journal has history and the run-local ledger resets.

</div>

For this not to be "see your own system's bug first, then pick a theory to explain it", there was only one way: **freeze the invariants first, then attack other people's systems.**

### The method is not ours

Turning preregistered invariants into black-box probes, injecting faults, and checking the external history against a consistency model is exactly what Jepsen does [[28]](#ref-28), and Elle is its academic form: inferring isolation anomalies from experimentally observed histories [[29]](#ref-29). The first paragraph of `INVARIANT_CARDS.md` says so: the methodology is not new, and any novelty can only come from **the choice of the invariant set**, **cross-runtime empirical findings**, and **agent-specific execution semantics**. We searched arXiv and found no preregistered, black-box, invariant-style fault-injection study of existing agent runtimes; the nearest were studies that inject faults into LLM API responses and measure pass@1, and a preprint that formalises four concurrency anomalies in TLA+ and reproduces tool-effect reordering in LangGraph [[30]](#ref-30). Only arXiv was searched, so not finding one is not evidence of absence.

### Seven cards

Each card has only four parts — precondition → required runtime state → violation oracle → classical ancestor — **with no MØBIUS implementation detail**, and each must carry a positive and a negative control.

| card | invariant | classical ancestor |
|---|---|---|
| C1 stale decision / revalidation | a decision (including a human approval) made at $$t_0$$ on state $$s$$ must not be applied at $$t_1$$ as usual if a third party has meanwhile changed $$s$$ so the decision is no longer justified | backward validation in optimistic concurrency control, `If-Match`, fencing tokens; selective revalidation [[5]](#ref-5) |
| C2 durable consumption / semantic replay | a single-use allowance must not be consumed again after a crash and resume | deterministic replay in durable execution, exactly-once, idempotent consumers [[27]](#ref-27) |
| C3 replay-state closure | non-deterministic results that affect future control flow must be recorded, not regenerated on replay | closure of record–replay [[26]](#ref-26) |
| C4 provenance preservation | provenance must cross subsystem boundaries with the fact, never degrade silently | provenance semirings, context propagation [[10]](#ref-10) |
| C5 temporal evidence preservation | the pre-state a relational condition needs must be kept before the effect commits, and delivered | past-time LTL, auxiliary views, WAL undo [[7]](#ref-7) [[24]](#ref-24) [[8]](#ref-8) |
| C6 monitorability | the observations a verdict needs derive from the condition's referents, not from the judged party's behaviour | monitorability, active monitoring [[13]](#ref-13) [[16]](#ref-16) |
| C7 concurrency isolation | conflicts between concurrent writers must be exposed, not silently overwritten with both reporting success | isolation levels, write–write conflict detection [[29]](#ref-29) |

The kill criterion was frozen before any probe ran (in my own words): if on at least 5 independent agent runtimes the preregistered probes are overwhelmingly handled correctly, or the defects appear only in MØBIUS, "systematic under-adoption" retires. Conversely, the paper only becomes interesting with ≥3 independent runtimes, ≥3 distinct theory families, the same "information exists but is unavailable after projection" structure, reproducible triggering, and fixes that need only a little glue.

In the end we did not run all seven cards just to fill a paper. The reason is below: the first cells were already enough to move the prior, and switching subsystems to find a failure would have become switching subsystems in order to find a failure.

<figure class="fig">
<a href="/research/mobius-rl-probe-method.svg"><img class="fig-light" src="/research/mobius-rl-probe-method.svg" alt="Probe method: a deterministic stub drives the runtime under test; the parent process injects a crash, a wait or a foreign world mutation at an announced fault point; an external audit event stream and an external world database produce one of five verdicts. Beside it, two control rails: a deliberately broken implementation must be caught and a deliberately correct one must pass, otherwise the card is probe-insensitive." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-probe-method-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 4.</strong> The shape of a probe. The runtime under test is driven by a deterministic stub; a fault, a wait or a third party changing the world is injected by the parent process at an announced fault point; the verdict reads only the audit event stream and the external world database outside the runtime — never the runtime's self-report, never its source. Every card must also run a deliberately broken and a deliberately correct implementation: the first must be ruled violated and the second must pass, otherwise the whole card is <code>probe-insensitive</code> and no runtime result on it may be read.</figcaption>
</figure>

## 6 · Our own instrument, needing more suspicion each time

### LangGraph, the first apparent violation

The first probes hit LangGraph 1.2.12 on card C2: an allowance of 3, a real independent process kill on the second consumption, then resume. The external audit sequence was:

```text
[1, 2, 2, 3]
```

An allowance of 3, four external consumptions recorded, with `n=2` twice — even under its strongest durability mode, `sync`. In the same run, the runtime's self-reported final state was:

```text
{"spent": 3, "limit": 3, "done": true}
```

By its own books, the allowance was not exceeded. An oracle that believed the runtime's self-report could not see this violation. The positive control reported a violation 100% of the time (`[1, 2, 1, 2, 3]`) and the negative control was clean.

That result was beautiful enough that my first reaction was to save it, not to doubt it. It looked too much like a paper result: external audit disagreeing with internal self-report, happening even in the strongest mode, with probe sensitivity backed by a positive control. The research lead recorded it as `VIOLATED` and added a white-box comparison: fields named `idempotency_key|dedupe_key|effect_id|operation_id` had 0 hits in the LangGraph package, while Temporal has explicit exactly-once and idempotent. It read as "the durable-execution engine has it and the agent runtime does not".

So the second thing had to be doubting it.

Section 4 of that same file says that "at-least-once plus a requirement that steps be idempotent may be this runtime's stated contract" is "the first thing to do next" — and yet §1's table had already written `VIOLATED`. **The verdict was issued before the contract check.** After checking the official documentation: LangGraph's durable execution is **replay**, not resumption from the line where it crashed; `interrupt()` resumes by re-executing the whole node from the start; the documentation asks for side effects and non-deterministic operations to be wrapped in tasks and warns that a task that started but did not finish may run again on resume, and that writes with side effects should use an idempotency key or check for existing results [[31]](#ref-31). `sync` only promises that changes are persisted synchronously "before the next step starts" [[31]](#ref-31); it strengthens step-boundary durability, not atomic commit of an external effect with a checkpoint.

> The experimental result was real; the interpretation was wrong.

<figure class="fig">
<a href="/research/mobius-rl-langgraph-correction.svg"><img class="fig-light" src="/research/mobius-rl-langgraph-correction.svg" alt="Three readings of a LangGraph result: first, external audit sequence 1, 2, 2, 3 against budget 3 while the runtime reports spent 3, read as VIOLATED; contract check, durable execution is replay and side effects are the application's to make idempotent; corrected, C2-N inapplicable and C2-T with a task gives 1, 2, 3, not-violated. Below, three instrument errors: an untyped StateGraph(dict) fabricating approve-A-dispatch-B; a cross-thread SQLite error; a missing socksio package producing NOT-CAPTURED rows mixed into one cell with later rows." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-langgraph-correction-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 5.</strong> Three readings of the same external audit data. First read as a violation; after the contract check, the window falls in the region the runtime explicitly hands to the application; with the probe rewritten to the official programming model, a completed <code>@task</code> is not re-executed across SIGKILL. Below, three mistakes our own instrument made the same day. What the figure shows is that the audit sequence itself never changed; what changed was its comparison with the contract.</figcaption>
</figure>

**correction**: `PROBE_RESULTS.md` was voided in full, with the reasons at the top of the file; the C3 cell was re-judged too — the journaled value survived the resume and the branch did not change, so C3 itself passed; the duplicated external write belongs to effect semantics and cannot fail C3. The probe was then split in two:

- **C2-T**: the consumption is written as an `@task`, as officially recommended, and SIGKILL lands after the task returns successfully and before the next durable boundary. **Result `[1, 2, 3]`, not-violated 3/3** — correct at the boundary it promises.
- **C2-N**: SIGKILL inside the task, after the external effect commits and before the task result is persisted. The raw oracle reading is 4 effects on an allowance of 3. But the runtime explicitly hands this window to the application, **so it is recorded `inapplicable` + `contract_relation = explicitly-outside-guarantee`, outside C2's violation denominator.**

"Was it violated" and "is this invariant part of the runtime's contract" are two questions. From then on the second became an orthogonal field on every result row, not a sixth state squeezed into the five.

### `StateGraph(dict)`: a violation entirely of our own making

In the first batch of rewritten LangGraph rows, C3-W (proposal identity across a human wait) produced an almost perfect replay-state-closure failure:

```text
approval for A  →  resume  →  dispatch B (no new approval)
```

It looked even more like a paper result than `[1,2,2,3]`, because it was exactly the failure shape the approval line had studied for three weeks.

This time the research lead stopped before reporting any LangGraph result: C2-T had not run a single task (`models=[]`); C2-R had only 2 effects, meaning phase two had not consumed anything at all — that `not-violated` was fake; C3-W used an untyped `StateGraph(dict)`. The event stream was decisive: in phase two `propose` did **not** re-run; `dispatch` found `state["proposal"]` missing and asked the stub for a new one, getting B. With an untyped schema the whole state is one root channel that keeps only the last value — the `gate` node returned `{"approved": True}` and replaced the root state wholesale, so the harness itself erased `proposal`. (We later checked this directly on LangGraph 1.2.12: input `{'x': 1}`, a node returning `{'b': 2}`, result `{'b': 2}`. [[31]](#ref-31)) The same bug explains why C2-R had only two effects: `approve`'s return erased `budget`, and the resumed run ended immediately.

The test the research lead wrote down at the time: "Run C3-W with no fault injected at all. If it loses the proposal even without a crash, it is definitively my bug. This no-fault baseline should have been there from the start."

I have to record the order in which this step actually happened, because it differs from how I first remembered it: fixing the schema (`StateGraph(S)`, a `TypedDict`) and adding the no-fault baseline **happened in the same step**, so the baseline never ran under the `dict` schema. The baseline also first exposed a second-layer problem — for probes built on `interrupt()`, "no fault" still stops at the interrupt; the right baseline is **resume in the same process**. With that added, all four baselines were correct under the typed schema: C3-W called the model once, dispatched A, and regenerated nothing. The evidence that convicted the earlier `violated` as a harness defect is the event stream (`propose` not re-run, `proposal` gone after `gate`) together with the correct baseline under the typed schema; the sentence "it loses state even without a crash" is not in the record.

The same round fixed a third: the external world's SQLite connection was used from LangGraph's worker thread and raised `SQLite objects created in a thread can only be used in that same thread`, so C2-T never ran and had been recorded `NOT-CAPTURED`.

Sometimes what most needs suspicion is not the runtime under test but your own experiment. A fabricated violation and a real one look exactly the same in the oracle's output; only a no-fault baseline and the external event stream, entry by entry, tell them apart. Since then a no-fault baseline has been a precondition of every real-runtime cell.

### socksio and a mixed ledger

The first OpenAI Agents SDK run on card C1 produced three `NOT-CAPTURED` rows. The cause had nothing to do with agents: the sandbox exports SOCKS proxy variables, the SDK's tracing exporter builds an httpx client at import time, and without `socksio` it raised `ImportError`. A pure environment fix.

The problem came afterwards. By rule, result tables may only be generated from `rows.jsonl`, never by writing aggregate numbers by hand. When the table was generated, the stability check reported:

```text
unstable: [('openai-agents', 'C1-RV')] | C1 rows: 27
```

The same cell mixed the three `NOT-CAPTURED` rows from the socksio failure with the three `not-violated` rows after the fix. Those three rows came from a different harness configuration: they could not be counted in one cell, and they could not be deleted by hand either. What we did: archive the whole mixed ledger, append-only, as `rows_archive_mixed.jsonl` (60 rows), save the C2/C3 rows separately as `rows_c2c3.jsonl` (33 rows), and rerun the whole C1 set with the final harness into a clean 24 rows. The archive still exists, and the stderr tail on those three `NOT-CAPTURED` rows is still that `ImportError`.

### Positive and negative controls, and five states

After those three things the method settled: every probe must come with a **deliberately broken control** and a **deliberately correct control**. The first must be caught and the second must pass; if the two are not separated 100%, the card is `probe-insensitive`, and a PASS on a real runtime may not be read as the system being correct.

Every cell lands in exactly one of five states:

```text
violated           the runtime claims the relevant surface, the probe reached the fault point, the oracle had enough, and the invariant broke
not-violated       the probe reached the fault point, the oracle had enough, and the invariant held
NOT-CAPTURED       the path ran, but the evidence needed to decide is not exposed or not durably observable
probe-insensitive  the positive control did not trigger the oracle
inapplicable       the runtime does not offer the semantic surface the card needs
```

Two things I keep reminding myself: **`inapplicable` is not a PASS** and does not enter the denominator; **`NOT-CAPTURED` is not a violation** — it says the instrument cannot see. Had the first LangGraph result had this vocabulary, it would have been recorded as "contract to check" from the start, not `VIOLATED`.

## 7 · C1 / C2 / C3: negative results (22 September, 09:16–10:08)

### LangGraph 1.2.12

The control sensitivity gate passed first: the positive controls of the three cards reported violations 9/9, the negative controls were clean 9/9. Then (3 attempts per cell, verdicts all identical, recomputed from `rows_c2c3.jsonl`):

| probe | fault point | verdict | model calls | external effects / allowance |
|---|---|---|---|---|
| C2-T | `AFTER_ACK_BEFORE_NEXT_STEP` | not-violated | A, B, C | 3 / 3 |
| C2-R | `AT_WAIT` | not-violated | A, B, C | 3 / 3 |
| C3-W | `AT_WAIT` | not-violated | A | 1 (dispatched A) |
| C3-C | `AFTER_CHECKPOINT_BEFORE_WAIT` | not-violated | A | 1 (branch matches pre-fault) |
| C2-N | `AFTER_EFFECT_COMMIT_BEFORE_ACK` | inapplicable · explicitly-outside-guarantee | A, B, C, D | 4 / 3 (not in denominator) |

A completed task is not re-executed after SIGKILL; the journaled value and branch survive resume; an external effect inside a node that crashes before its ack is replayed, and the official contract explicitly hands that window to the application's idempotency.

### OpenAI Agents SDK and Pydantic AI: P-FOREIGN

C1 was frozen narrower this time than "whenever the world changes after approval, the runtime must notice", because most frameworks promise no such thing:

> If a runtime provides and declares a validation / guardrail seam that runs again after approval, then after the external world changes during the wait, that seam must re-evaluate against the new world; an old validation result may not be carried forward as a current fact.

Formally, $$V(a, S_0) = \mathit{allow}$$; during the wait $$S_0 \xrightarrow{\text{foreign}} S_1$$; the person approves the same $$a$$. If the runtime claims to revalidate before execution it must compute $$V(a, S_1)$$; when $$V(a,S_0)=\mathit{allow} \wedge V(a,S_1)=\mathit{deny}$$, the only legal outcomes are deny, escalate or replan — never dispatch.

Both runtimes were hit on mechanisms they explicitly promise, not a standard we invented. The docstring of the OpenAI Agents SDK's `pre_approval_tool_input_guardrails` says the same guardrails run again after approval, immediately before tool execution [[32]](#ref-32). Pydantic AI's `args_validator` runs after schema validation and before execution, and runs again after approval with `tool_call_approved=True` [[33]](#ref-33). Both ship deterministic test models (`ScriptedModel`, `FunctionModel`), so no real model or API key is needed. AutoGen was not included: its documentation says waiting on `UserProxyAgent` inside a run leaves the team in an unstable state that cannot be saved or resumed [[34]](#ref-34) — by the rule it is recorded `inapplicable` first, not recruited as a third system.

The first round has only one variable, "the world changes", and no crash injection, so that a failure could not be confused between stale decision and durability.

<figure class="fig">
<a href="/research/mobius-rl-c1-timeline.svg"><img class="fig-light" src="/research/mobius-rl-c1-timeline.svg" alt="C1-RV timeline: validation sees version 1, unprotected, allow; approval wait; a third party changes the world to version 2, protected; human approves; the post-approval validation sees version 2, deny; zero destructive effects; validation_world_versions is 1, 2. Control: a deliberately broken implementation validates once, caches allow, executes on version 2, one destructive effect." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-c1-timeline-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 6.</strong> The C1-RV timeline: the first validation sees version 1, unprotected, and allows; the approval wait begins; a third party changes the world to version 2, protected; the person approves; the post-approval validation sees version 2 and denies; zero destructive effects. On the right, the deliberately broken control: it validates once, caches allow, and executes on version 2. The core evidence is <code>validation_world_versions</code> in the external event stream, not the runtime saying "I revalidated". The figure does not show the runtime noticing the change itself — what noticed it is the validator we wrote into the seam.</figcaption>
</figure>

**measurement** (recomputed from `rows.jsonl`, 3 attempts per cell):

| runtime | probe | verdict | `validation_world_versions` | decisions | destructive effects |
|---|---|---|---|---|---|
| openai-agents 0.22.3 | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| pydantic-ai 2.47.0 | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| broken-control | C1-RV | violated | `[1]` | allow | 1 |
| correct-control | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| both runtimes | C1-RAW (no seam) | inapplicable | `[]` | — | 1 (not in denominator) |

The real evidence on this card is not the runtime saying "I revalidated" but the external oracle seeing that the validator **actually read two versions of the world**:

```text
validation_world_versions = [1, 2]
```

Pydantic AI adds one more piece: the first validation has `tool_call_approved = false`, the second `tool_call_approved = true` — the runtime's own flag confirms the second is the post-approval one. The oracle also separates a case that would earlier have passed by mistake: no destructive effect, but no post-approval validation call either — which cannot tell "revalidated and refused" from "never tried again", and is recorded `NOT-CAPTURED`. The two C1-RAW cells are `inapplicable`: their only purpose is to show that **approval identity ≠ freshness guarantee**.

Two things this result does not show: the first round has no crash, so it does not cover "is the seam still re-invoked after a cross-process resume"; and, as said, what noticed the change is our validator, not the runtime.

Running total: 3 real runtimes, 5 applicable cells across C1/C2/C3, **zero violations in applicable cells**, each with a positive control detected 100% of the time.

## 8 · Delegated Obligation Closure: killed in one round (22 September, 10:19–10:24)

After two rounds of negative results I had another idea. The runtimes did not violate the invariants because they pushed the obligation onto the application (C2-N and C1-RAW both do). So a new question might be:

> When a runtime explicitly hands a correctness obligation to the application, does it also expose enough stable mechanism for the application to actually discharge it under the runtime's own replay / resume semantics?

First its ancestor: "the responsibility must ultimately be carried out at the endpoint" is the End-to-End Arguments, whose canonical examples are precisely duplicate suppression and delivery acknowledgement — what lower layers can offer is a performance aid, and complete correctness can only be implemented at the endpoints [[35]](#ref-35). Idempotency as an application-level discipline has its classic statement too [[36]](#ref-36). So we did not test "why push it to the application", only:

$$
\mathrm{delegates}(R, O) \;\Rightarrow\; \exists M_R :\ M_R \text{ is sufficient to discharge } O
$$

where $$M_R$$ must come entirely from public, documented API — no reading internal checkpoints, no patching the runtime, no home-built recovery system. Three capability conditions: stable identity (the same logical effect is recognisable before and after replay), boundary access (the application gets a chance to mitigate before the effect), durable reconciliation (the application can look up committed results). All true is `closed`; any missing is `open`. Lines of code are not a metric.

### A wrong inference from one grep

First, a claim of ours has to be withdrawn. In the white-box comparison after the first LangGraph probe, `idempotency_key`, `dedupe_key`, `effect_id` and `operation_id` had 0 hits in the package, and we inferred:

> LangGraph requires idempotency but does not give you the tools to implement it.

The only basis for that inference was one string search. It shows only that **no field has those names**.

### C2-NI

LangGraph 1.2.12 publicly exposes `Runtime.execution_info`, reached through the public `get_runtime()`, with fields `thread_id`, `run_id`, `checkpoint_id`, `checkpoint_ns`, `task_id` and `node_attempt` (the full set arrived in 1.1.5) [[31]](#ref-31). The probe hits C2-N's window — the process dies after the external effect commits and before the task is acknowledged — but the application mitigates the way the runtime itself recommends, building its key only from public fields:

```text
key = thread_id | checkpoint_ns | task_id | i
hit = idem.lookup(key)            # external effect store, PRIMARY KEY + BEGIN IMMEDIATE
if hit: return hit                # reuse the committed result
else:   idem.commit(key, payload)
```

The positive control is the same probe in `unstable` mode: a fresh `uuid4()` key every time.

Across a real SIGKILL and a brand-new process, the external event stream looks like this:

```text
pid 70399  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…
pid 70399  idem.lookup           hit=False   before_effect=True
pid 70399  effect.committed
pid 70399  faultpoint.reached    AFTER_EFFECT_COMMIT_BEFORE_ACK      ← parent SIGKILL
pid 70400  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…   ← byte-identical
pid 70400  idem.lookup           hit=True    before_effect=True
pid 70400  effect.reused
pid 70400  tasks.completed
```

**measurement** (recomputed from `rows.jsonl`, 3 attempts per mode, all `phase1_returncode = -9`): the stable-key mode has **1** external effect, all three capability conditions true, not-violated 3/3; the unstable-key positive control has **2** external effects, violated 3/3. All six fields are **stable** across the crash and the process boundary, two of them against expectation: `run_id` did not change after the second invoke, and `node_attempt` did not increment after the retry — which only strengthens the conclusion, since the application does not need to choose fields.

**Delegated Obligation Closure was killed in one round.** What remains is an ordinary layering choice covered by the End-to-End Arguments.

> A string's absence ≠ a capability's absence.

This is one of the methodological lessons from these days I most want to keep, because it is the most natural kind of mistake: grep is cheap, and zero hits looks like evidence.

The limits go with the conclusion: one runtime, one window, one task; the atomicity of the external store was implemented by us — this shows the runtime provides the information needed to build a stable key, not that every external system offers a conditional-write primitive.

### correctness-under-adoption stops

By the decision written in advance: if this cut passed, stop digging along correctness-under-adoption, including not doing C7. The running total:

| card | mechanism | runtimes | violations in applicable cells |
|---|---|---|---|
| C1 | explicit post-approval revalidation seam | 2 | 0 |
| C2 | documented durable boundary | 1 | 0 |
| C3 | replay-state closure | 1 | 0 |
| C2-NI | dischargeability of the delegated obligation | 1 | 0 (closed) |

The formal retirement condition required expanding to at least 5 applicable independent runtimes. We did not expand, so strictly it was not "triggered"; it was **stopped**. The reason: switching subsystems again very easily becomes switching subsystems in order to find a failure. One fact has to be stated next to this stop: the C7 we did not test is exactly the family in which that TLA+ preprint reports reproducing tool-effect reordering in LangGraph [[30]](#ref-30). So the scope of this negative result is these C1–C3 windows, not "LangGraph has no concurrency problems".

The most valuable conclusion of this phase is a negative one: we proposed, one after another, hypotheses that "agent runtimes may be repeating classical systems mistakes", and once **contract, applicability, application responsibility and public mitigation mechanisms** were separated, the apparent violations disappeared. They did not disappear because the measurement was insensitive — every cell had a positive control detected 100% of the time.

The scale also has to be stated: this whole stretch (from freezing seven cards to C2-NI) happened in about two hours on the morning of 22 September, driven by deterministic stubs, 3 attempts per cell. It is a pilot, not a measurement paper. Its value is in moving the prior, not in giving rates.

## 9 · The strong form of FTR, and its reduction gate (22 September, 10:30–10:52)

### What the strong form looks like

The last post covered FTR's formalisation and its retirement by its own criteria. But that version did not restore FTR at its strongest. Its strongest form is drawn in the dotted band at the bottom of the V42 runtime architecture map: several execution actors each seal their own forecast before seeing the others'; a shared evidence field records provenance, dissent and evidence ancestry, insisting that "agreement between sources is not independence"; competing hypotheses and candidate trajectories; active falsification — find the cheapest experiment that tells two hypotheses apart, executing for information if necessary; an epistemic scheduler that spends compute on the uncertainty a decision actually turns on, scheduling among reason, ask, test, fork, observe and act; reality admission — are the premises fresh? is the evidence independent? is there a cheap falsifier left? is the uncertainty acceptable? — before the authority / resource / invariant gates that exist today; and, after an effect commits, calibration written back to each forecaster by proper scoring.

<figure class="fig">
<a href="/research/mobius-rl-ftr-strong.svg"><img class="fig-light" src="/research/mobius-rl-ftr-strong.svg" alt="The strong form of FTR, from the research-frontier band of the V42 architecture map: several execution actors, an evidence field, competing hypotheses, active falsification, an epistemic scheduler, reality admission, today's gates, the effect and calibration, plus the forecast contract, future evidential need Omega-star and A-safe. Each node is labelled with what it reduced to: belief state and ATMS, Bayesian experimental design and value of information, rational metareasoning, POMDP shielding, dual control, epistemic fault domains, proper scoring, output commit." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-ftr-strong-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 7.</strong> The strong form of FTR, with nodes and edges taken from the research-frontier band of the V42 runtime architecture map (Graphviz) and from the $$\mathcal{F}_t = \{(h_i, E_i, O_i, A_i)\}$$ formulation I gave on 22 September; redrawn in Graphviz. The green line in each node is the existing object the reduction gate mapped it to. Dashed nodes were never implemented; the only item here that would change execution semantics is $$A^{\mathrm{safe}}_t$$, which corresponds to a shield under partial observability. What the figure shows is that the strong form was reduced item by item; it does not show that these parts are useless as engineering architecture.</figcaption>
</figure>

On 22 September I gave it a statement stronger than any version in the repository:

$$
\mathcal{F}_t = \big\{ (h_i,\ E_i,\ O_i,\ A_i) \big\}
$$

<div class="eq-note">

Each hypothesis $$h_i$$ carries its current supporting evidence $$E_i$$, the observation obligations $$O_i$$ it needs next, and the action set $$A_i$$ allowed while it has not been eliminated; the runtime itself performs split, merge and eliminate; once an action commits it constrains in turn which future hypotheses remain legal.

</div>

and a property actually worth trying to kill:

$$
A^{\mathrm{safe}}_t = \bigcap_{h \in \mathcal{F}^{\mathrm{live}}_t} A(h)
$$

<div class="eq-note">

The runtime may commit an irreversible action directly only if every still-possible world allows it; otherwise it should observe, delay, branch or escalate. The question changes from "what does the agent believe" to "what does uncertainty change about what the runtime is allowed / required to do".

</div>

Plus the quantity the last post kept — future evidential need:

$$
\Omega_t^{*} = \arg\min_{\Omega}\ \mathrm{Cost}(\Omega) \quad \text{s.t.}\quad \forall h_i, h_j:\ E_\Omega(h_i) = E_\Omega(h_j) \Rightarrow C(h_i) = C(h_j)
$$

The kill criterion was written by me when I approved the gate: if a simple mapping $$\mathrm{FTR} \equiv \mathrm{BeliefState} + \mathrm{Planner} + \mathrm{Monitor}$$ exists and MØBIUS is merely wiring them together in TypeScript, FTR retires and is not implemented. And: **if it dies too, we know MØBIUS's paper value is not in a new systems abstraction.**

### Reduction, item by item

<figure class="fig">
<a href="/research/mobius-rl-reduction-map.svg"><img class="fig-light" src="/research/mobius-rl-reduction-map.svg" alt="Seven candidates linked to what killed them: completion attribution, transition witness, late-bound obligations, observation ownership, correctness-under-adoption, delegated obligation closure and FTR, each connected to experiments, prior art, official contracts and controls." loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-reduction-map-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 8.</strong> Seven candidates and what killed them: experiments (solid), prior work (dashed), official contracts (dash-dot), controls (dotted). Most candidates were hit by more than one thing. The figure shows "killed by what"; it says nothing about any direction's engineering value.</figcaption>
</figure>

| part of FTR's strong form | existing object | mapping |
|---|---|---|
| competing hypotheses, labelled assumption sets, cascading retraction | ATMS [[37]](#ref-37); belief state as a sufficient statistic of history [[38]](#ref-38) | complete: a set of atomic hypotheses with evidence is one representation of a belief; the 2026 Agent-BRACE represents belief as a set of atomic natural-language claims with ordinal certainty labels and conditions the policy only on it [[39]](#ref-39) |
| which experiment to run, execute-for-information | Bayesian experimental design [[40]](#ref-40) [[41]](#ref-41) [[42]](#ref-42); value of information [[43]](#ref-43) | complete: "the cheapest discriminating experiment" is a special case of EIG/EVSI |
| scheduling among ask / test / fork / observe / act | rational metareasoning, value of computation [[44]](#ref-44) [[45]](#ref-45) | complete; the earlier frontier review also noted that the original priority formula double-counted P(decision change) |
| action permission under uncertainty, $$A^{\mathrm{safe}}_t$$ | shielding under partial observability [[46]](#ref-46) [[47]](#ref-47) | complete, and stronger: a shield allows only actions that keep the agent in a winning region from a winning belief support; it needs only the possible transitions — **probabilities and rewards may remain unspecified** [[47]](#ref-47) |
| an effect that both controls and probes | dual control [[48]](#ref-48) [[49]](#ref-49) | complete |
| evidence ancestry, agent count ≠ evidence independence | epistemic fault domains [[50]](#ref-50); epistemic Sybil [[51]](#ref-51); the Sybil attack [[52]](#ref-52); non-independent failures of multiversion software [[53]](#ref-53) | complete: κ_E can be computed from provenance, and adding voters cannot raise it |
| forecast scoring and calibration | proper scoring and calibration [[54]](#ref-54) [[55]](#ref-55) [[56]](#ref-56); and "calibration is not control" [[57]](#ref-57) | complete, and the latter says calibration scores should not enter the gate |
| forecasts as first-class runtime state, validated separately | a POMDP framework that decomposes autonomous decisions into information, beliefs, forecasts, actions and utility and validates each [[58]](#ref-58) | mostly |
| a barrier before irreversible externalisation | the output commit problem [[59]](#ref-59) [[60]](#ref-60) | complete |

The research lead had prepared an escape hatch: "POMDPs and conformant planning need a known probability model, and an agent runtime has none" [[61]](#ref-61) [[62]](#ref-62) [[63]](#ref-63). The full text of Carr et al. closes it — the shield is computed by satisfiability solving and needs only a partial model.

One result that is easy to get backwards deserves its own paragraph: **the 2026 nearest neighbours do not kill it; the classical side does.** A full-text word count on the two closest 2026 papers shows Agent-BRACE and Dixon almost completely silent on the permission/obligation axis (`obligation`: 0 in both; `runtime`: 0 in both). My narrowing — ask not what the agent believes but what uncertainty changes about what the runtime may do — really did shake off the agent literature. What killed it were two older objects: the shield under partial observability, and output commit. Checked only against the agent side, this direction would have been misjudged as surviving.

The other half is in the repository: FTR's own three-layer protocol says it has **no effect authority, does not enter the gate, and only narrows** (`FTR_FRONTIER_RESEARCH.md` §7). An object that explicitly does not change execution semantics is, by definition, a monitor. And the frontier review had written back in early September that "FTR as a better monitor" was dropped — structurally it is Proof-of-Execution's non-authoritative observation plane plus confidence-bearing prediction, while run-time assurance answers "who monitors the monitor" with a plant model and a verified fallback, neither of which FTR has. In the code, `grep -ril ftr packages` still has 0 hits today.

The research lead also tried three candidate residuals, and none lived: a hypothesis set generated openly by the model at run time and not enumerable breaks the guarantees of the classical objects, but gives FTR no guarantee either — it makes FTR **weaker**, not new; obligations being deontic rather than value-maximising — knowledge preconditions and the shield itself are already deontic in shape; a commit constraining which hypotheses stay legal — belief update and belief revision with a protected core already cover it.

### Final stance

**Verdict: RETIRE.** The kill criterion held. It is the sixth reduction in the same shape:

| # | candidate | existing object | what the runtime actually does |
|---|---|---|---|
| 1 | the judge lacks a causal term | refuted by experiment (the criteria are state predicates) | the supplied causal term is ignored |
| 2 | completion attribution | actual causality | one syntactic lookup in the effect log |
| 3 | minimal witness commitment | auxiliary views / self-maintainability | the capture point is known, easier than the 1996 problem |
| 4 | late-bound witness obligations | does not occur (0/165) | look-before-change already closed the window |
| 5 | endogenous observation alphabet | monitorability, decidable | computable, and computed by nobody |
| 6 | FTR, strong form | shield + output commit + belief representation + validation framework | not implemented, and its own spec forbids it from changing execution semantics |

I am not shy about writing these two sentences:

> FTR as engineering architecture may still be useful.
>
> FTR as a new systems abstraction is currently not supported.

The question the last post left behind — "which facts must be kept before acting, because a later proof will need them" — was also narrowed to its end in these days: first it became the Temporal Witness Lifecycle (absorbed by auxiliary views), then Late-Bound Obligations (refuted by 0/165). It did not leave a new abstraction strong enough to stand.

This verdict has an honest gap that must be written with it: the 51-section research brief that produced FTR is not in the repository, and the research lead's kickoff forbids reconstructing it from memory. The gate was run against the strong form I gave in conversation and the material in the repository. If that brief contains an operation not isomorphic to any row of the table above, the verdict has to be redone.

## 10 · How I changed in these days

This is not a paper, so "I" is allowed. But I only want to write the part that happened at turning points in the research.

At first, when a new abstraction took shape, I was genuinely excited. The first time I wrote $$\mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)$$, I thought it might be the thing. Then, within hours, a 1988 paper, a 1996 paper or a preprint from July 2026 absorbed the whole abstraction.

When that happens once, it is a letdown. After it happens many times in a row, the question itself changes. I stopped asking "is it new?" first, and started asking "what will kill it fastest?"

When `LATE-CRITICAL = 0/165` came out, what I remember is not disappointment but a very specific clarity: the formula was right; this world just does not contain the execution it guards against. When LangGraph first showed `[1, 2, 2, 3]` there were a few minutes of excitement — it looked too much like a paper result; after the contract check I had to withdraw the `VIOLATED` I had just written. Later `StateGraph(dict)` showed that sometimes the thing that most needs suspicion is not the runtime but my own experiment.

Earlier, when a direction was killed, my reaction was "gone again". In these days it became "good, that won't waste half a year". Later still, a negative result began to feel like progress in its own right: it crosses a region off the map, with reasons written clearly enough for someone else to check.

This is not a motivational point. It has a very practical consequence: when a result looks too beautiful, my first move now is to look for its no-fault baseline, its contract, its positive control, and evidence beyond its grep.

## 11 · Where things stand

| direction | status | basis |
|---|---|---|
| approval line (capture time, effect shape, who produces the key) | <span class="st st-prior">PRIOR ART</span> | CommitGuard, PlanFence, S-Bus, ATR; residual A is an `O_EXCL` defect |
| evidence substitution | <span class="st st-prior">PRIOR ART</span> | false success; R2 is a replication |
| transition witness as a primitive | <span class="st st-retired">RETIRED</span> | before-image + provenance edge + past-time operator |
| evidence selection / verification-input ownership | <span class="st st-measured">MEASURED</span> · <span class="st st-prior">PRIOR ART</span> | 57.1 pp (58.8 pp on top of ADR 0045, n=68); active monitoring, IRA, ADR 0021/0041 |
| completion attribution | <span class="st st-retired">RETIRED</span> | actual causality; a specification-shape problem; one engineering recommendation |
| temporal witness lifecycle | <span class="st st-prior">PRIOR ART</span> | auxiliary views / self-maintainability (UNVERIFIED-FULLTEXT) |
| late-bound witness obligations | <span class="st st-killed">KILLED</span> | `LATE-CRITICAL = 0/165` |
| recovery semantic closure | <span class="st st-prior">PRIOR ART</span> | durable execution, semantic replay |
| correctness-under-adoption | <span class="st st-killed">STOPPED</span> | 0 violations in C1/C2/C3 applicable cells; not expanded to 5 runtimes; C7 untested |
| delegated obligation closure | <span class="st st-killed">KILLED</span> | C2-NI: public API suffices |
| FTR, strong form | <span class="st st-retired">RETIRED</span> | reduction gate; one material gap (the 51-section brief) |
| layered determinism (capability 0.923, content 0.795) | <span class="st st-open">OPEN</span> | the one positive claim with data only we have; needs real-model n=10 |
| the last post's E1–E4 | <span class="st st-ne">NOT RUN</span> | none of them ran in this record |

## Coda: NO PRIMARY THESIS YET

At eleven in the morning on 22 September, my last instruction to the research lead named no direction at all. Its task is autonomous research-direction discovery: not starting from an idea but from **unexplained phenomena** — what in the system's actual behaviour still lacks a satisfying existing theoretical explanation. Find the phenomenon first, then reduce it, then kill it; nothing in the table above may come back under a new name without new evidence. "Some field wasn't wired through" does not count as a phenomenon. It was explicitly allowed to hand back the conclusion:

```text
NO PRIMARY THESIS YET
```

As I write this, that round is still running, and I do not know what it will return. On today's evidence the most honest status is that one line: we do not yet have a surviving primary thesis that I am willing to call a new systems abstraction.

We started out hoping MØBIUS would demonstrate a new runtime abstraction. So far what it has demonstrated first is something more basic: an apparent runtime failure is not yet a systems result; and a research direction worth pursuing should first be able to survive everything we do to it — the contract check, the no-fault baseline, the positive control, 0/165, and a paper from 1996.

No direction survived these days. But each one that did not now has a cause of death written down clearly. When the next candidate appears, it will have to walk past those first.

---

<p class="fig-note">Figure sources: the data figures are generated by <code>scripts/research/rl-figures.py</code> from the result files named in the text; Figure 7's Graphviz source is <code>scripts/research/mobius-rl-ftr-strong.dot</code>. The previous post and the FTR formalisation PDF are on the <a href="/research/">research page</a>.</p>

### References

Every entry was re-checked on 22 September 2026 against its primary record (arXiv page, DOI, publisher page, official documentation or installed package source). The bracket gives verification depth: `FULLTEXT` means the relevant full text was read, `ABSTRACT-ONLY` means only the abstract, `UNVERIFIED-FULLTEXT` means the metadata is confirmed and the content rests on secondary descriptions. Preprints are preprints; peer review is not assumed where no venue is stated.

1. <span id="ref-1"></span>I. Santos-Grueiro. *Temporary Authority, Permanent Effects: Commit-Time Authorization for LLM Agents.* Preprint, arXiv:[2607.10487](https://arxiv.org/abs/2607.10487), 2026. [FULLTEXT]
2. <span id="ref-2"></span>E. Chen, S. Wang, C. G. Brinton. *Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory.* Preprint, arXiv:[2609.03340](https://arxiv.org/abs/2609.03340), 2026. [FULLTEXT]
3. <span id="ref-3"></span>S. Khan. *S-Bus: Automatic Read-Set Reconstruction for Multi-Agent LLM State Coordination.* Preprint, arXiv:[2605.17076](https://arxiv.org/abs/2605.17076), 2026. [FULLTEXT]
4. <span id="ref-4"></span>M. Rashidi. *The Balkanization of Execution-Security Research for AI Coding Agents: Isolation, Access Control, and Time-of-Check-to-Time-of-Use Vulnerabilities.* Preprint, arXiv:[2607.05743](https://arxiv.org/abs/2607.05743), 2026. [FULLTEXT]
5. <span id="ref-5"></span>Y. Lyu, Y. Ren, R. Lai, W. Liu. *From Version Conflicts to Decision Conflicts: Selective Revalidation for Long-Running AI Agents.* Preprint, arXiv:[2609.08015](https://arxiv.org/abs/2609.08015), 2026. [FULLTEXT]
6. <span id="ref-6"></span>L. Advani. *From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents.* FAGEN Workshop at ICML 2026. arXiv:[2606.09863](https://arxiv.org/abs/2606.09863). [FULLTEXT]
7. <span id="ref-7"></span>K. Havelund, G. Roşu. *Synthesizing Monitors for Safety Properties.* TACAS 2002, LNCS, pp. 342–356. [doi:10.1007/3-540-46002-0_24](https://doi.org/10.1007/3-540-46002-0_24). [FULLTEXT]
8. <span id="ref-8"></span>C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, P. Schwarz. *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging.* ACM TODS 17(1):94–162, 1992. [doi:10.1145/128765.128770](https://doi.org/10.1145/128765.128770). [UNVERIFIED-FULLTEXT]
9. <span id="ref-9"></span>R. Snodgrass, I. Ahn. *Temporal Databases.* IEEE Computer 19(9):35–42, 1986. [doi:10.1109/MC.1986.1663327](https://doi.org/10.1109/MC.1986.1663327). [UNVERIFIED-FULLTEXT]
10. <span id="ref-10"></span>T. J. Green, G. Karvounarakis, V. Tannen. *Provenance Semirings.* PODS 2007, pp. 31–40. [doi:10.1145/1265530.1265535](https://doi.org/10.1145/1265530.1265535). See also P. Buneman, S. Khanna, W.-C. Tan, *Why and Where: A Characterization of Data Provenance*, ICDT 2001, [doi:10.1007/3-540-44503-X_20](https://doi.org/10.1007/3-540-44503-X_20). [UNVERIFIED-FULLTEXT]
11. <span id="ref-11"></span>browser-use. `browser_use/agent/judge.py`, commit d8110c5 (task-completion judge: final result, agent steps and screenshots; boolean verdict). [github.com/browser-use/browser-use](https://github.com/browser-use/browser-use/blob/d8110c5ff87ccba887aaa726cdb780f2f84bef8d/browser_use/agent/judge.py). [FULLTEXT (source)]
12. <span id="ref-12"></span>B. Bollig. *Runtime Verification: Monitoring, Knowledge, and Uncertainty* (lecture notes). arXiv:[2604.26753](https://arxiv.org/abs/2604.26753), 2026 — Def. 5.1 (monitorability), Thm. 5.3 (decidability), and $$AP_a \subseteq AP$$ as a fixed parameter. [FULLTEXT]
13. <span id="ref-13"></span>A. Pnueli, A. Zaks. *PSL Model Checking and Run-Time Verification via Testers.* FM 2006, LNCS, pp. 573–586. [doi:10.1007/11813040_38](https://doi.org/10.1007/11813040_38) (read in the NYU TR2006-881 version). [FULLTEXT]
14. <span id="ref-14"></span>A. Bauer, M. Leucker, C. Schallhart. *Runtime Verification for LTL and TLTL.* ACM TOSEM 20(4), 2011. [doi:10.1145/2000799.2000800](https://doi.org/10.1145/2000799.2000800). [ABSTRACT-ONLY]
15. <span id="ref-15"></span>S. A. Logan, S. Standefer, T. Ferguson. *A Formal Framework for Noisy Runtime Verification.* Preprint, arXiv:[2609.10462](https://arxiv.org/abs/2609.10462), 2026 (author order as on the arXiv record). [FULLTEXT]
16. <span id="ref-16"></span>J. Baumeister, B. Finkbeiner, F. Scheerer. *Active Monitoring with RTLola: A Specification-Guided Scheduling Approach.* Preprint, arXiv:[2507.20615](https://arxiv.org/abs/2507.20615), 2025. [ABSTRACT-ONLY]
17. <span id="ref-17"></span>Y. Deng. *Goal-Autopilot: A Verifiable Anti-Fabrication Firewall for Unattended Long-Horizon Agents.* Preprint, arXiv:[2606.11688](https://arxiv.org/abs/2606.11688), 2026. [FULLTEXT]
18. <span id="ref-18"></span>C. Shi, Y. Wu, Y. Liu, et al. *Interactive Reward Agent: GUI Task Evaluation via Environment-State Verification.* Preprint, arXiv:[2607.25904](https://arxiv.org/abs/2607.25904), 2026. [ABSTRACT-ONLY]
19. <span id="ref-19"></span>J. Y. Halpern, J. Pearl. *Causes and Explanations: A Structural-Model Approach. Part I: Causes.* British Journal for the Philosophy of Science 56(4):843–887, 2005. [doi:10.1093/bjps/axi147](https://doi.org/10.1093/bjps/axi147). [ABSTRACT-ONLY]
20. <span id="ref-20"></span>J. Y. Halpern. *Actual Causality.* MIT Press, 2016. ISBN 978-0-262-03502-6. [UNVERIFIED-FULLTEXT]
21. <span id="ref-21"></span>S. Triantafyllou, A. Singla, G. Radanovic. *Actual Causality and Responsibility Attribution in Decentralized Partially Observable Markov Decision Processes.* AIES 2022, pp. 739–752. [doi:10.1145/3514094.3534133](https://doi.org/10.1145/3514094.3534133); arXiv:[2204.00302](https://arxiv.org/abs/2204.00302). [ABSTRACT-ONLY]
22. <span id="ref-22"></span>D. Huang, J. K. Chua, Z. Wang. *Beyond Task Success: Measuring Workflow Fidelity in LLM-Based Agentic Payment Systems.* AIDS4DF Workshop at PAKDD 2026. arXiv:[2605.06457](https://arxiv.org/abs/2605.06457). [FULLTEXT]
23. <span id="ref-23"></span>F. Wm. Tompa, J. A. Blakeley. *Maintaining Materialized Views without Accessing Base Data.* Information Systems 13(4):393–406, 1988. [doi:10.1016/0306-4379(88)90005-1](https://doi.org/10.1016/0306-4379(88)90005-1). [UNVERIFIED-FULLTEXT]
24. <span id="ref-24"></span>D. Quass, A. Gupta, I. S. Mumick, J. Widom. *Making Views Self-Maintainable for Data Warehousing.* PDIS 1996, pp. 158–169. [doi:10.1109/PDIS.1996.568677](https://doi.org/10.1109/PDIS.1996.568677). [UNVERIFIED-FULLTEXT]
25. <span id="ref-25"></span>F. Chen, G. Roşu. *Parametric Trace Slicing and Monitoring.* TACAS 2009, LNCS, pp. 246–261. [doi:10.1007/978-3-642-00768-2_23](https://doi.org/10.1007/978-3-642-00768-2_23). [UNVERIFIED-FULLTEXT]
26. <span id="ref-26"></span>AWS. *Durable Execution SDK — Determinism during replay* (section “Pass data through return values, not closures”). [docs.aws.amazon.com](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/determinism/), accessed 22 Sep 2026. [FULLTEXT (docs)]
27. <span id="ref-27"></span>J. Xu, L. Fan, Z. Wang, et al. *Beyond Single-Use Tokens: Durable Authorization State for Replay-Resistant LLM Agent Actions.* Preprint, arXiv:[2608.01710](https://arxiv.org/abs/2608.01710), 2026. [ABSTRACT-ONLY]
28. <span id="ref-28"></span>K. Kingsbury. *Jepsen* — a framework for distributed-systems verification with fault injection, and its published analyses. [jepsen.io](https://jepsen.io); [github.com/jepsen-io/jepsen](https://github.com/jepsen-io/jepsen). [FULLTEXT (project pages)]
29. <span id="ref-29"></span>K. Kingsbury, P. Alvaro. *Elle: Inferring Isolation Anomalies from Experimental Observations.* PVLDB 14(3):268–280, 2020. [doi:10.14778/3430915.3430918](https://doi.org/10.14778/3430915.3430918). [FULLTEXT]
30. <span id="ref-30"></span>S. Khan. *Verified Detection and Prevention of Concurrency Anomalies in Multi-Agent Large Language Model Systems.* Preprint, arXiv:[2606.17182](https://arxiv.org/abs/2606.17182), 2026. [ABSTRACT-ONLY]
31. <span id="ref-31"></span>LangGraph (Python) documentation and source, v1.2.12: functional API — determinism and idempotency ([docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/functional-api#idempotency)); `interrupt()` and `Durability` docstrings in `langgraph/types.py`; `Runtime.execution_info` in `langgraph/runtime.py`; root-channel behaviour of an untyped state schema in `langgraph/graph/state.py` (checked by running it). Accessed 22 Sep 2026. [FULLTEXT (docs + source)]
32. <span id="ref-32"></span>OpenAI Agents SDK (Python) v0.22.3: `ToolExecutionConfig.pre_approval_tool_input_guardrails` docstring in `agents/run_config.py`; human-in-the-loop guide ([github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python/blob/main/docs/human_in_the_loop.md)); `agents.testing.ScriptedModel`. [FULLTEXT (docs + source)]
33. <span id="ref-33"></span>Pydantic AI v2.47.0: deferred tools ([deferred-tools.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/deferred-tools.md)); `Tool(args_validator=…)` and `RunContext.tool_call_approved` docstrings; `FunctionModel`. [FULLTEXT (docs + source)]
34. <span id="ref-34"></span>Microsoft AutoGen. *AgentChat user guide: Human-in-the-Loop.* [microsoft.github.io/autogen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html), accessed 22 Sep 2026. [FULLTEXT (docs)]
35. <span id="ref-35"></span>J. H. Saltzer, D. P. Reed, D. D. Clark. *End-to-End Arguments in System Design.* ACM TOCS 2(4):277–288, 1984. [doi:10.1145/357401.357402](https://doi.org/10.1145/357401.357402). [FULLTEXT]
36. <span id="ref-36"></span>P. Helland. *Idempotence Is Not a Medical Condition.* ACM Queue 10(4):30–46, 2012. [doi:10.1145/2181796.2187821](https://doi.org/10.1145/2181796.2187821). [UNVERIFIED-FULLTEXT]
37. <span id="ref-37"></span>J. de Kleer. *An Assumption-based TMS.* Artificial Intelligence 28(2):127–162, 1986. [doi:10.1016/0004-3702(86)90080-9](https://doi.org/10.1016/0004-3702(86)90080-9). [UNVERIFIED-FULLTEXT]
38. <span id="ref-38"></span>L. P. Kaelbling, M. L. Littman, A. R. Cassandra. *Planning and Acting in Partially Observable Stochastic Domains.* Artificial Intelligence 101(1–2):99–134, 1998. [doi:10.1016/S0004-3702(98)00023-X](https://doi.org/10.1016/S0004-3702(98)00023-X). The belief-state formulation goes back to K. J. Åström, J. Math. Anal. Appl. 10(1):174–205, 1965, [doi:10.1016/0022-247X(65)90154-X](https://doi.org/10.1016/0022-247X(65)90154-X). [FULLTEXT]
39. <span id="ref-39"></span>J. Singh, Z. Khan, A. Prasad, et al. *Agent-BRACE: Decoupling Beliefs from Actions in Long-Horizon Tasks via Verbalized State Uncertainty.* Preprint, arXiv:[2605.11436](https://arxiv.org/abs/2605.11436), 2026. [FULLTEXT]
40. <span id="ref-40"></span>D. V. Lindley. *On a Measure of the Information Provided by an Experiment.* Annals of Mathematical Statistics 27(4):986–1005, 1956. [doi:10.1214/aoms/1177728069](https://doi.org/10.1214/aoms/1177728069). [UNVERIFIED-FULLTEXT]
41. <span id="ref-41"></span>K. Chaloner, I. Verdinelli. *Bayesian Experimental Design: A Review.* Statistical Science 10(3), 1995. [doi:10.1214/ss/1177009939](https://doi.org/10.1214/ss/1177009939). [UNVERIFIED-FULLTEXT]
42. <span id="ref-42"></span>T. Rainforth, A. Foster, D. R. Ivanova, F. Bickford Smith. *Modern Bayesian Experimental Design.* Statistical Science 39(1), 2024. [doi:10.1214/23-STS915](https://doi.org/10.1214/23-STS915). [ABSTRACT-ONLY]
43. <span id="ref-43"></span>R. A. Howard. *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics 2(1):22–26, 1966. [doi:10.1109/TSSC.1966.300074](https://doi.org/10.1109/TSSC.1966.300074). [UNVERIFIED-FULLTEXT]
44. <span id="ref-44"></span>S. Russell, E. Wefald. *Principles of Metareasoning.* Artificial Intelligence 49(1–3):361–395, 1991. [doi:10.1016/0004-3702(91)90015-C](https://doi.org/10.1016/0004-3702(91)90015-C). [UNVERIFIED-FULLTEXT]
45. <span id="ref-45"></span>E. J. Horvitz. *Reasoning about Beliefs and Actions under Computational Resource Constraints.* Proc. Third Workshop on Uncertainty in AI (UAI 1987), pp. 429–444. arXiv:[1304.2759](https://arxiv.org/abs/1304.2759). [FULLTEXT]
46. <span id="ref-46"></span>M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, U. Topcu. *Safe Reinforcement Learning via Shielding.* AAAI 2018. [doi:10.1609/aaai.v32i1.11797](https://doi.org/10.1609/aaai.v32i1.11797). [FULLTEXT]
47. <span id="ref-47"></span>S. Carr, N. Jansen, S. Junges, U. Topcu. *Safe Reinforcement Learning via Shielding under Partial Observability.* AAAI 2023, 37(12):14748–14756. [doi:10.1609/aaai.v37i12.26723](https://doi.org/10.1609/aaai.v37i12.26723); arXiv:[2204.00755](https://arxiv.org/abs/2204.00755). [FULLTEXT]
48. <span id="ref-48"></span>A. A. Feldbaum. *Dual Control Theory, I–IV.* Automation and Remote Control 21(9):874–880, 21(11):1033–1039, 22(1), 22(2), 1960–1961 (English translations; page ranges of III–IV not confirmed). [UNVERIFIED-FULLTEXT]
49. <span id="ref-49"></span>Y. Bar-Shalom, E. Tse. *Dual Effect, Certainty Equivalence, and Separation in Stochastic Control.* IEEE TAC 19(5):494–500, 1974. [doi:10.1109/TAC.1974.1100635](https://doi.org/10.1109/TAC.1974.1100635). [UNVERIFIED-FULLTEXT]
50. <span id="ref-50"></span>J. He, D. Yu. *The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures in Agentic Quorums.* Preprint, arXiv:[2609.02925](https://arxiv.org/abs/2609.02925), 2026. [FULLTEXT]
51. <span id="ref-51"></span>M. Bara. *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence.* Preprint, arXiv:[2609.01873](https://arxiv.org/abs/2609.01873), 2026. [ABSTRACT-ONLY]
52. <span id="ref-52"></span>J. R. Douceur. *The Sybil Attack.* IPTPS 2002, LNCS, pp. 251–260. [doi:10.1007/3-540-45748-8_24](https://doi.org/10.1007/3-540-45748-8_24). [FULLTEXT]
53. <span id="ref-53"></span>J. C. Knight, N. G. Leveson. *An Experimental Evaluation of the Assumption of Independence in Multiversion Programming.* IEEE TSE SE-12(1):96–109, 1986. [doi:10.1109/TSE.1986.6312924](https://doi.org/10.1109/TSE.1986.6312924). [ABSTRACT-ONLY]
54. <span id="ref-54"></span>G. W. Brier. *Verification of Forecasts Expressed in Terms of Probability.* Monthly Weather Review 78(1):1–3, 1950. [doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2](https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2). [UNVERIFIED-FULLTEXT]
55. <span id="ref-55"></span>A. P. Dawid. *The Well-Calibrated Bayesian.* JASA 77(379):605–610, 1982. [doi:10.1080/01621459.1982.10477856](https://doi.org/10.1080/01621459.1982.10477856). [UNVERIFIED-FULLTEXT]
56. <span id="ref-56"></span>T. Gneiting, A. E. Raftery. *Strictly Proper Scoring Rules, Prediction, and Estimation.* JASA 102(477):359–378, 2007. [doi:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437). [UNVERIFIED-FULLTEXT]
57. <span id="ref-57"></span>C. Zhang, Z. Wan, X. Yu, et al. *Calibration Is Not Control: Why LLM-Agent Oversight Needs Intervention.* Preprint, arXiv:[2606.21399](https://arxiv.org/abs/2606.21399), 2026. [FULLTEXT]
58. <span id="ref-58"></span>M. F. Dixon. *Model Validation of Agentic AI Systems: A POMDP-Based Framework for Belief-State, Forecast, and Policy Validation.* Preprint, arXiv:[2606.17383](https://arxiv.org/abs/2606.17383), 2026. [ABSTRACT-ONLY]
59. <span id="ref-59"></span>R. Strom, S. Yemini. *Optimistic Recovery in Distributed Systems.* ACM TOCS 3(3):204–226, 1985. [doi:10.1145/3959.3962](https://doi.org/10.1145/3959.3962). [ABSTRACT-ONLY]
60. <span id="ref-60"></span>E. N. Elnozahy, L. Alvisi, Y.-M. Wang, D. B. Johnson. *A Survey of Rollback-Recovery Protocols in Message-Passing Systems.* ACM Computing Surveys 34(3):375–408, 2002. [doi:10.1145/568522.568525](https://doi.org/10.1145/568522.568525) — states the output commit problem and credits it to Strom & Yemini. [FULLTEXT]
61. <span id="ref-61"></span>B. Bonet, H. Geffner. *Planning with Incomplete Information as Heuristic Search in Belief Space.* AIPS 2000, pp. 52–61. [FULLTEXT]
62. <span id="ref-62"></span>D. E. Smith, D. S. Weld. *Conformant Graphplan.* AAAI-98, pp. 889–896. [FULLTEXT]
63. <span id="ref-63"></span>J. Hoffmann, R. I. Brafman. *Contingent Planning via Heuristic Forward Search with Implicit Belief States.* ICAPS 2005, pp. 71–80. [FULLTEXT]
