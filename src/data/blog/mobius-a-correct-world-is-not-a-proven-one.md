---
title: "MØBIUS — A Correct World Is Not a Proven One"
description: "Thirteen days after the last update, MØBIUS moved from execution reliability into completion: who decides that work is done, on what evidence, and what that evidence forgets. Most of the claims I started the fortnight with are now dead or known under other names. What is left is narrower, measured, and more interesting — including a much smaller FTR."
pubDatetime: 2026-09-19T19:30:00Z
tags: ["MØBIUS", "Agents", "Verification", "FTR"]
category: "research"
series: "MØBIUS"
timezone: "America/New_York"
showInBlog: true
cover: "/cover-correct-world.svg"
---

The last thing this blog told you about MØBIUS was on 6 September: a binary that could load 132 of its 167
production modules, a ladder for telling *the code exists* apart from *the system does this*, and a
filesystem provider and a repository provider finally composed over one working tree.

Since then the repository has taken 531 commits. I am not going to walk through them. Most were one of three
things: a prediction written down before a change, the change, or the record of the prediction failing.
What I want to report is what those thirteen days did to the **questions** — because by the end of them,
MØBIUS had stopped being mainly the thing I was building and become mainly the thing I was measuring with.

This post covers 6 September (the last public post, V56) through 19 September (`61f7100`, the R3 handoff, plus
an audit I ran for this post). Where a number appears, the evidence directory it came from is named, and I
re-derived it from the journals rather than copying it from a summary. Where something is a hypothesis, it is
called one.

<figure class="fig">
<a href="/research/mobius-r3-timeline.svg"><img class="fig-light" src="/research/mobius-r3-timeline.svg" alt="Timeline from 6 to 19 September 2026: the last public post at V56; a world declared not discovered (ADR 0014–0019, Probes 1–6); human decisions outliving their world (V59–V73); the approval line meeting its neighbours (VB-1, VB-2, PP-1, OV-1, B1, K8); an unattended mission reporting success (S-M1/B, ADR 0021–0026); a real model in the loop (R1); completion starting to lie (R2); the judge shown more (R3); claims killed in review; this audit; and the open frontier." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-timeline-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure A.</strong> Thirteen days. The coral points are where the research question itself moved; the red one is where claims died.</figcaption>
</figure>

A note on what kind of statements follow. I use a small vocabulary and try to hold to it:
**measured** (a count from a named journal), **observation** (something I saw in code or events that is not a
rate), **interpretation**, **hypothesis**, **open question**, **prior art**, **retired** (a claim I no longer
make because someone else made it first or better), **killed** (a claim an experiment refuted), and
**implemented** versus **proposed**. The two I care most about keeping apart are *hypothesis* and *result*.

## Part I — The runtime got stricter

### A revision is a record of what a provider did

The first days after V56 settled a question the previous post left hanging. With two providers over one
directory, is freshness one clock or two? ADR 0015 answered it: a revision records **what its own provider
did**, never a description of the world, and two such counters are never aggregated. ADR 0014 made the world a
thing the assembly *declares* rather than something the core discovers. Probes 1–6 then found that a premise
an action declared was carried, persisted — and **inert**: the scheduler satisfied preconditions just in time,
so drift at a declared dispatch was structurally zero, and ADR 0019's decided mechanism did nothing as
specified. That was the first of many times in this fortnight that a mechanism I believed was working turned
out to be present and not load-bearing.

### Human decisions outlive the world that justified them

V59 (8 September) measured the thing I had been circling for weeks: **a person approves an effect, the world
changes, and the runtime reuses the approval anyway.** The recorded decision carried nothing about the world
it was granted in; it matched on `(capability, resources)` and was decisive across a real persist-and-resume
boundary onto a rewritten file. V60–V64 narrowed why: the blindness was specific to authority (an
observation-derived premise *did* revalidate, because it was anchored to a session; an approval was anchored
to nothing), and one value in the invalidation path meant both *unchanged* and *no identity to compare*.

V65 was the first slice on this line that implemented rather than measured. An approval now records what it
was granted over, and before it is reused the runtime recomputes that and returns one of three verdicts:

$$
\mathrm{Revalidate}(A, t) \in \{\textsf{reusable},\ \textsf{superseded},\ \textsf{unevaluable}\}
$$

with, per bound resource $$r$$,

$$
\textsf{reusable} \iff \forall r \in R(A):\ \mathrm{id}_t(r) = \mathrm{id}_A(r)
\;\wedge\; \mathrm{occ}(\text{proposal}) = \mathrm{occ}(A)
$$

<div class="eq-note">

That is the shipped rule in `approval-revalidation.ts` plus the K8 repair, not an idealisation: identity is a content digest taken by a look the runtime charges to the goal, `occ` is the proposal instance the person was shown, and a resource with no computable identity makes the approval `unevaluable` — never `reusable`.

</div>

The shape I had in mind going in was

$$
\mathit{Approval} = (\mathit{Decision},\ \mathit{WorldBasis},\ \mathit{Bindings},\ \mathit{Evidence}),
$$

valid while the current world matches the approved basis. The code is narrower than that: its "world basis" is
a set of per-resource content identities, and an approval whose basis cannot be recomputed is not reused.
Where the prose and the code disagree, the code is what I measured.

The paper track then attacked it from every side:

- **K8** (measured, on the shipped daemon): the person approved `write(notes.txt, "…3pm")`; the model
  re-proposed `…4pm`; **B executed on A's approval**, because to the runtime A and B were one question. The
  repair binds an approval to the proposal instance; the re-run shows B escalated and reuse of A unchanged.
- **VB-1** (measured, rules not systems): a content-blind lease trades unsafe permits for unnecessary
  re-approvals exactly one for one at every TTL; the shipped content binding gets 0/14 and 0/14 — and loses
  the `CLOSED` arm outright, 14/14, where a lifecycle rule wins.
- **PP-1** (killed a claim of ours): the provenance link from an approval to the observation the person was
  shown is carried end to end and **read by nothing**. We had called it our strongest distinction from
  optimistic concurrency control. It was not load-bearing.
- **OV-1** (killed a sentence in our own draft): *"reuse still costs nothing"* — reuse costs exactly what first
  use costs, one covering look per resource.
- **R1-P6b** (measured, real model, N = 1 per cell): with the approved proposal carried and the approved
  dispatch grounded (ADR 0034, 0035), a change after the decision is caught at the gate; with the mechanism
  removed, the same cell executes stale. A change after the last look is caught by the provider in both.

B1, ratified on 11 September, compressed all of it into one sentence the evidence derives rather than
decorates: **a human approval is a memoized decision whose validity key is the state it was about, and "key
not recomputable" is a different outcome from "key differs."** Two surprises — the inert provenance link and
reuse costing what first use costs — become *predictions* under that reading. That is the one abstraction from
this period I would still defend.

And then it stopped being ours. External baselines showed LangGraph 1.2.11 and the OpenAI Agents SDK 0.22.2
executing on a changed world in all sixteen arms; but Claude Code 2.1.269 and Codex 0.149.0 **refuse** a stale
edit on their native editing paths — by a content precondition, not by revalidating anything — and execute
stale on a whole-file shell write. "Alone in refusing" did not survive whole runtimes. And a literature pass by
the research lead (below) found the design family already published: CommitGuard captures witnesses before
dispatch, recomputes them at the commit boundary and treats missing evidence as a third outcome
[[1]](#ref-1); PlanFence validates plan dependencies at action time and blocks on an incomplete
declaration [[2]](#ref-2); S-Bus reconstructs read sets from traffic without agent cooperation
[[3]](#ref-3); a systematization names *authorization checked once and trusted forever* as a root cause
[[4]](#ref-4).

> A human decision is a runtime object bound to a version of the world. That sentence is true, it is
> measured here, and it is **not new**. MØBIUS is one more instance of a boundary-witness family.

### Determinism is layered, and it is not a property of "the agent"

An aside I needed before trusting any N = 1 result. At `f9b27dd`, one arm, 13 tasks × 3 repetitions, all
valid (measured, re-derived from `evidence/{r1,r2}/f9b27dd`):

| what is compared across the three runs | modal share | groups identical in all 3 |
|---|---|---|
| sequence of dispatched **capabilities** | **0.923** | 10 / 13 |
| capabilities **plus normalised arguments** | **0.795** | 5 / 13 |
| number of proposals | CV mean **0.129** | 5 / 13 identical |

So "the agent is deterministic" is the wrong sentence, and so is its negation. At least six levels come apart:
semantic destination, capability choice, argument structure, exact proposal, execution result and world
consequence. Here the second is nearly fixed and the third is not: T3 and T6 used the same number of proposals
in every run and still wrote different bytes. And the question I most wanted answered — *does content variance
change outcomes?* — **cannot be answered from these runs**: all 39 passed their checker, so the number of
opportunities for variance to change an outcome was zero. That is not a negative result. It is an untested
one, and the difference turned out to matter everywhere below.

Whether the runtime's structure (a closed capability surface, one gated observation door, compiled effects)
*causes* the stability, or whether small tasks and one model would be this stable anywhere, is an open
question with a designed ablation and no data.

<figure class="fig">
<a href="/research/mobius-r3-runtime.svg"><img class="fig-light" src="/research/mobius-r3-runtime.svg" alt="The runtime at f9b27dd. Model and cognition — proposer, look and criterion judge through the model port — produce an ActionIntent carrying desiredEffect, expected, satisfies and parameters. The runtime loop owns authority, routing, world and version binding, observation, execution, verification, evidence, completion and the journal; evidence and completion are highlighted. Effects reach a world of a filesystem provider as anchor and a repository provider as witness, and a human is asked through mobiusd or the TUI." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-runtime-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure B.</strong> The runtime as it stands, drawn from the packages rather than from the plan. The two highlighted rows are where the rest of this post lives.</figcaption>
</figure>

## Part II — When completion started lying

### R1: the proposer was blind

On 13 September a real model (`claude-opus-5` through the Claude Code CLI) went into the mission loop for the
first time. The first baseline was humbling in an instructive way: in five of six rows the model's first
proposal was exactly right for an agent that cannot see — *read the file first* — the runtime performed the
read, and **nothing it read reached the next prompt**. So the model asked again and the repeat guard stopped
the run. ADR 0027–0030 fixed what the proposer is shown. By R1-P4 the seven tasks passed their checker 7/7 and
the runtime declared 6/7 complete. Claude Code and Codex on the same seven tasks were level with it: **this
suite does not separate runtimes**, and I stopped treating it as if it did.

### R2: 0 of 6 correct, 5 of 6 declared complete

R2 (18 September) gave the runtime six multi-step missions with checkers pinned against their seed, their
solution and the solution one step short (`evidence/r2/de5b79b`, measured):

- **checker pass: 0 of 6**
- **runtime declared complete: 5 of 6**

Every false completion closed its last criterion the same way: on a **read** whose proposer-written
expectation held (*"content exists"*), through ADR 0031's rule that such a read evidences the criterion it names.
One mission read a file, wrote nothing, and was complete. Two protocol decisions multiplied: a `satisfies`
field the model attached to 395 of 396 intents (it means *working toward* to the model and *evidences* to the
runtime), and a rule that let a satisfied expectation stand as evidence. Nobody was cheating. The runtime had
made the proposer its own completion oracle.

### ADR 0043–0045: a judge, and what it is shown

ADR 0043 made a criterion that no assertion checks bindable only on a separate judge's `established`. The judge
is another model call; it sees the criterion and the observations, and never the proposer's account of what it
expected. Measured at `33e599e`, N = 1:

| | before (R2 pilot) | after ADR 0043 |
|---|---|---|
| false completions | 5 / 6 | **0 / 6** |
| checker pass | 0 / 6 | 3 / 6 |
| runtime completed | 5 / 6 | **0 / 6** |

The judge made no false `established` in 19 judgements — and closed nothing on multi-resource work. What cost
the completions was what it was **shown**: one binding's evidence at a time, no evidence of absence (an empty
search returned no refs), and directory reads that carried no content. ADR 0044 made a listing carry small text
files' content; ADR 0045 showed the judge the binding's evidence **plus the run's latest non-stale observation
of each other resource**.

R3 P3 re-ran both suites three times at `f9b27dd` (measured, re-derived from
`evidence/{r2,r1}/f9b27dd`; in the first attempts every model call failed in seven rows — CLI timeouts, and an
OAuth refresh contended with another Claude Code session — and those rows are kept in the evidence and were
re-run at the same commit):

| suite | valid rows | checker pass | runtime completed | false completions |
|---|---|---|---|---|
| R2 | 18 | 18 | 10 | 0 |
| R1 | 21 | 21 | 19 | 0 |

That table is the easiest thing in this post to misread, so here is what it does **not** say. It does not say
verification is solved. **All 39 valid rows passed their checker, so there was no row in which a false
completion could have occurred.** Prediction 1, "no false completion", held with zero opportunities to fail.
It was pre-registered as the kill criterion, and on this data it could not kill anything. The honest reading is
that R3 P3 shows the runtime now completes most correct work (29 of 39 checker-passing rows, against 6 of 10
after ADR 0043), and says nothing about whether it would refuse incorrect work. The R2 pilot is the only data here with checker
failures in it.

## Part III — `cannot-tell` was mostly not a judge problem

The judge ruled 114 times in R3 P3 (measured):

| suite | judgements | established | not-established | cannot-tell |
|---|---|---|---|---|
| R2 | 103 | 19 | 20 | 64 |
| R1 | 11 | 1 | 0 | 10 |
| **all** | **114** | **20** | **20** | **74** |

Seventy-four `cannot-tell`. The natural reaction — mine — was *the judge is too timid; give it a better
prompt*. So I read all 74 reasons against their criteria and coded what each one says is missing. A reason can
cite a missing **prior state** (what the file held before), an **unread current resource** (a file nobody has
looked at yet), both, or neither:

| what the reason says is missing | n |
|---|---|
| prior state only | 40 |
| prior state **and** an unread current resource | 5 |
| an unread current resource only | 28 |
| the judge call timed out | 1 |
| **total** | **74** |

<div class="eq-note">

If the five mixed cases are assigned by the barrier the reason leads with, the split reads 43 missing-past / 30 current / 1 failure. The research lead's independent pass over *all* committed journals (133 judgements, 88 cannot-tell, coded by a model into five classes) found 58% transition-shaped. Different corpus, different coder, same direction.

</div>

<figure class="fig">
<a href="/research/mobius-r3-judge.svg"><img class="fig-light" src="/research/mobius-r3-judge.svg" alt="Stacked bars of judge verdicts in R3 P3: R2 103 judgements, 19 established, 20 not-established, 64 cannot-tell; R1 11, 1 established and 10 cannot-tell; all 114, 20, 20 and 74. Of 74 cannot-tell: 40 missing prior state only, 5 both, 28 an unread current resource only, 1 timeout. Share of each task's cannot-tell citing a missing prior state: T4 rename 10 of 10, R2-3 spec edit 20 of 22, R2-6 split 15 of 27, and 0 of 15 across R2-2, R2-4 and R2-5." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-judge-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure E.</strong> Verdicts in R3 P3, and what the <code>cannot-tell</code> reasons are missing. The third panel is the part that changed the question.</figcaption>
</figure>

The 28 current-state cases are ordinary: the run had not yet read `modules.json` or `package.json` when it
asked. Another look fixes them, and does. The 45 that cite a missing past are different in kind, and they are
not scattered — they sit in three tasks with nothing in common as tasks:

| task | shape | cannot-tell citing a missing prior state |
|---|---|---|
| T4 | rename a file | 10 / 10 |
| R2-3 | edit a config to a spec | 20 / 22 |
| R2-6 | split a document into files | 15 / 27 |
| R2-2, R2-4, R2-5 | module export, version bump, follow a moved config | 0 / 15 |

What the three share is the form of their success criterion: *archive.txt holds the **former** content of
notes.txt*; *settings.ini reflects the spec **and nothing else in it changed***; *each section of the **old**
notes.md is its own file*. None of these is a property of the world after the work. Each is a property of the
change:

$$
C \neq f(W_{\mathrm{post}}) \qquad\qquad C = f(W_{\mathrm{pre}},\, A,\, W_{\mathrm{post}})
$$

### The past was in the journal

This is where I expected to write *information that exists before an action becomes unrecoverable after it*.
The data does not support that sentence, so I am not writing it. In **every valid journal** with one of these
criteria, the prior content of the target was observed **before** the first effect on it (measured): in T4,
the model listed the workspace before the move, and since ADR 0044 that listing carried `notes.txt`'s content
and digest. The move's post-state has the same digest. The fact that decides the criterion is in the journal,
twice.

It was not in the judge's view, for two reasons that are both in the code. ADR 0045's view keeps **the latest
observation of each resource**, and "an older one is never a fallback" — so the post-move listing of `.` evicts
the pre-move listing of `.`. And a mission's second run sees only its own observations. The judge was right
every time it said `cannot-tell`. It was being shown a world with its past removed.

So the question moved. Not *how do we make the judge smarter*, but:

> **What must an agent runtime keep in view — not just keep — so that completion stays decidable?**

And one thing the audit could not show: whether the past would have been captured at all if the model had not
happened to list the directory with `includeContent` before acting. Here it always did. Nothing in the runtime
made it.

### The smallest example

Take the rename. Criterion $$C$$: *archive.txt exists with the former content of notes.txt, and notes.txt no
longer exists.* Post-state evidence:

$$
E_{\mathrm{post}} = \{\ \mathit{archive}_{\mathrm{post}} = \text{``the note''},\ \ \neg\,\mathrm{exists}(\mathit{notes}_{\mathrm{post}})\ \}
$$

Two histories produce exactly that evidence:

$$
\begin{aligned}
h_1 &:\ \mathit{notes}_{\mathrm{pre}} = \text{``the note''} \;\xrightarrow{\ \mathrm{move}\ }\; \mathit{archive}_{\mathrm{post}} = \text{``the note''} && C(h_1) = \text{true} \\
h_2 &:\ \mathit{notes}_{\mathrm{pre}} = \text{``something else''} \;\xrightarrow{\ \mathrm{delete;\ write}\ }\; \mathit{archive}_{\mathrm{post}} = \text{``the note''} && C(h_2) = \text{false}
\end{aligned}
$$

$$
E_{\mathrm{post}}(h_1) = E_{\mathrm{post}}(h_2) \quad\text{and}\quad C(h_1) \neq C(h_2) \qquad\Longrightarrow\qquad E_{\mathrm{post}} \not\models C
$$

<figure class="fig">
<a href="/research/mobius-r3-two-histories.svg"><img class="fig-light" src="/research/mobius-r3-two-histories.svg" alt="History A: notes_pre is 'the note', fs.move, archive_post is 'the note' and notes is absent; C true. History B: notes_pre is 'something else', notes deleted and archive written, archive_post is 'the note' and notes absent; C false. Both lead to the same post evidence and different criterion truth, so E_post does not entail C." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-two-histories-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure D.</strong> Two worlds that post-state evidence cannot tell apart, and a criterion that can. No judge, however capable, can soundly say <code>established</code> from the left-hand information alone.</figcaption>
</figure>

That is the whole mathematical content, and it is not deep. A post-state is a function of history, and not an
injective one:

$$
H_t \not\equiv W_t, \qquad W_t(h_i) = W_t(h_j) \not\Rightarrow h_i = h_j
$$

Adding one fact that only the past has — the pre-state digest — separates the histories:

$$
\mathrm{digest}(\mathit{notes}_{\mathrm{pre}}) = \mathrm{digest}(\mathit{archive}_{\mathrm{post}})\ \wedge\ \neg\,\mathrm{exists}(\mathit{notes}_{\mathrm{post}}) \;\Rightarrow\; C
$$

<div class="eq-note">

Up to the strength of the digest and of the move's semantics — a digest shows equal bytes, not that these bytes travelled by this path. For "content preserved" that is enough; for "moved, not rewritten" it is not.

</div>

### Transition witnesses — a candidate, not a discovery

The obvious name for the missing object is a **transition witness**: the pre-state projection, the action, the
post-state projection, and the relation that must hold across them.

$$
\mathcal{T}_{t \to t+1} = \big(\,W_t,\ A_t,\ W_{t+1},\ R_t\,\big)
$$

```text
TransitionWitness {
  pre:      { source.path, source.digest }          // taken before the effect, attributable to W_t
  action:   fs.move(source, destination)
  post:     { destination.digest, source.exists = false }
  relation: pre.source.digest == post.destination.digest
}
```

I want to be precise about its status, because it is the most tempting thing in this post to oversell.
Keeping history is not new. Past-time temporal logic exists precisely to state properties about change and
has efficient monitors [[5]](#ref-5); temporal databases keep valid-time history [[6]](#ref-6); provenance
records where a value came from and why [[7]](#ref-7) [[8]](#ref-8); before-images are what write-ahead logs
are made of. When the research lead ran the kill tests on *transition witness as a new primitive* it failed
three of them in one pass: it is a before-image plus a provenance edge plus a past-time operator; for MØBIUS
it is largely an engineering gap (give the judge an ordered slice of the journal and the T4 case goes away);
and the name is a new name for known parts. **Retired as a primitive.**

What survives is a narrower question, and I think a real one: in an autonomous-agent runtime, **which
transitions must produce first-class evidence, and how does the runtime decide that before it acts** — given
that the criterion is written in natural language by someone else, the model chooses the action, and the
runtime cannot know in general which part of the past a future judgement will need? That is open.

<figure class="fig">
<a href="/research/mobius-r3-state-vs-transition.svg"><img class="fig-light" src="/research/mobius-r3-state-vs-transition.svg" alt="Top: post state only — archive.txt equals 'the note', notes.txt absent; the former content of notes.txt is not in the evidence, so the justified verdict is cannot-tell. Bottom: a transition witness — pre state notes.txt digest 6862e4, action fs.move, post state archive.txt digest 6862e4 and notes.txt absent; the relation digest(notes_pre) = digest(archive_post) together with notes absent entails the criterion." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-state-vs-transition-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure C.</strong> State evidence against transition evidence, with the real digest from T4 repetition 3 (<code>sha256:6862e454…</code>, before and after the move).</figcaption>
</figure>

## Part IV — A harder failure: `established` without support

If most `cannot-tell` verdicts were correct refusals, the next question is the uncomfortable one: were the
`established` verdicts correct *for the right reason*? There are 20. I read every one against the evidence the
judge was actually shown (the ids are in each `criterion.judged` event).

Nineteen are supported by that evidence — three of them only on a literal reading (*"notes.md is an index
linking the three files"* was established from notes.md alone, without evidence the three files exist, which
the wording arguably does not require). **One is not.**

R1 T4, repetition 3 (`evidence/r1/f9b27dd/P3-control-b/T4-rename/rep-3`), in order:

1. Event 7 — the model lists `.`: `notes.txt`, content `"the note\n"`, digest `6862e454…`.
2. Event 10 — `fs.move(notes.txt → archive.txt)`.
3. Event 17 — the model lists `.` again: `archive.txt`, same digest.
4. Event 20 — the judge, shown the second listing: **`cannot-tell`** — *"no evidence records what notes.txt
   originally contained."* Correct.
5. Event 23 — the model proposes a read of `archive.txt`, arguing in its own intent that *"fs.move moves the
   same inode, so archive.txt's content is definitionally the former content of notes.txt."* The judge never
   sees that sentence.
6. Event 24 — the read: `archive.txt`, `"the note\n"`. Nothing about the past.
7. Event 27 — the judge, shown that read and the second listing: **`established`** — *"the workspace contains
   exactly one entry, archive.txt with content "the note\n" … and no notes.txt present."*
8. Event 30 — `goal.completed`.

Between the correct refusal and the `established`, the judge gained no information about the former content.
Its stated reason does not mention the former content. The world happened to be right — the checker passes, the
bytes did move — and the verdict was not entailed by what the judge saw:

$$
J(E, C) = \textsf{established} \qquad\text{while}\qquad E \not\models C
$$

I will call this, provisionally, **unsupported establishment** (or evidentially unsound establishment). The
wording I can defend is exactly this: *in a manual audit of the 20 real-model `established` judgements in R3
P3, at least one clear establishment was not entailed by the evidence the judge was shown.* One in twenty is
not a 5% error rate; with N = 20 and a hand audit it is an existence proof and nothing more. Whether it
recurs, and how often, is experiment E1 below.

What it does establish is the sentence I would put above the whole fortnight:

$$
\boxed{\ \text{world correctness} \;\not\Rightarrow\; \text{evidential correctness}\ }
$$

A checker compares the world to a solution. It cannot tell a verdict that was right from one that was lucky.
Every false-completion metric in this project — including the 0 of 39 above — is a checker metric.

## Part V — Completion certificates that cannot replay themselves

Reading those 20 verdicts turned up a second, purely structural gap. In `loop.ts`, the judge is asked with the
binding's evidence **and** the run view:

```ts
const answer = await this.#ports.judge!.judge({
  criterion: { id: criterion.id, statement: criterion.statement },
  evidence: [...shown, ...view],
})
```

and when it says `established`, `#bindClaimed` records **only the binding's evidence** under the criterion — and
that is what `goal.completed` carries. So:

$$
J_i = E_{\mathrm{binding}} \cup E_{\mathrm{runView}}, \qquad C_i = E_{\mathrm{binding}}, \qquad J_i \nsubseteq C_i \ \text{ whenever the view contributed}
$$

In T4 repetition 3 the judge used the `archive.txt` read and the listing that shows `notes.txt` gone; the
certificate keeps the read. From the certificate alone you cannot even establish the half of the criterion
that *was* supported.

Across R3 P3 (measured): **11** judge-bound criteria appear in completed runs, and $$J_i \subseteq C_i$$ holds in
**0** of them. By my reading of the judge's own stated reasons, in 8 of the 11 the omitted evidence carries part
of what the reason cites (a second file for a two-file criterion, the file saying where settings moved); in the
three R2-1 cases the kept search result is probably sufficient on its own.

<figure class="fig">
<a href="/research/mobius-r3-certificate.svg"><img class="fig-light" src="/research/mobius-r3-certificate.svg" alt="What the judge was shown: J_i equals the binding evidence (obs-5, a read of archive.txt with 'the note') union the run view (obs-4, a listing of the root with notes.txt absent). Verdict established. What goal.completed keeps: C_i equals the binding evidence only, obs-5; obs-4 is not kept. J_i is not a subset of C_i. In R3 P3, 0 of 11 judge-bound criteria in completed runs are closed; in 8 of 11 the omitted evidence carries part of what the judge's reason cites; the journal's criterion.judged event still names J." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-certificate-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure F.</strong> The decision basis against the completion record. The journal still names both observations in the <code>criterion.judged</code> event; the gap is in what the runtime calls the certificate.</figcaption>
</figure>

The closure condition a completion record should meet, and the replay property it should support:

$$
J_i \subseteq C_i, \qquad \mathrm{Replay}(C_i, \mathit{Criterion}_i) = \mathit{OriginalDecision}_i
$$

I am calling the current state a **certificate closure / replayability gap**, and I want to be careful about
the size of that claim. Proof-carrying code [[9]](#ref-9), provenance and audit logs are established fields;
*we invented replayable evidence* would be false. The engineering fix here is a few lines. The research
question it points at is narrower: in agent completion, the decision basis is assembled by the runtime from a
moving view, adjudicated by a model, and later reused by whoever reads the record — so **what must a completion
record contain for someone else to reach the same verdict, and how does it stay valid when the view that
produced it has moved on?** Nobody has run the replay yet (E3 below).

## Part VI — FTR: what survived trying to kill it

FTR — originally *Future Trajectory Reasoner*, and now more honestly a *future trajectory representation* —
has been the project's most ambitious idea and its least evidenced one. The story of this fortnight is mostly
the story of it getting smaller.

**What it was.** A continuously maintained layer of future simulation: roll the run forward, monitor how the
futures diverge, and let that inform what the runtime does now.

**What killed the strong form.**

1. *Predicting the future is not the novelty.* Predictive runtime verification already forecasts future
   trajectories from an observed prefix and bounds the violation probability with conformal prediction
   [[10]](#ref-10). Sample disagreement as an uncertainty signal is also established — self-consistency
   [[11]](#ref-11), semantic entropy over equivalence classes of samples [[12]](#ref-12), and conformal
   "ask for help" sets for LLM planners [[13]](#ref-13). The project's own review had already reduced the
   *monitor* sub-claim, the *worldline* sub-claim (an ATMS [[14]](#ref-14) with MVCC) and *epistemic
   scheduling* (rational metareasoning [[15]](#ref-15), where the right object is the value of information
   [[16]](#ref-16)).
2. *A specific prediction failed its threshold.* Could the stream of reads predict the future write set before
   the first write — the input any anticipatory scheduler would need? Across 69 journals with dispatched writes,
   the median fraction of the eventual write set covered by earlier reads was **0.25**, with 33 of 69 at
   exactly zero, against a kill threshold (recall < 0.5) fixed before the computation. The shape is structural:
   editing an existing file is highly anticipatable; creating or renaming one is not, because **a read cannot
   point at a path that does not exist yet**. Killed on this corpus.
3. *The designed evaluation could not run.* R3 P4 resolved every assertion a real model wrote in `expected`
   across 104 journals — 1,345 of them — as satisfied, violated, undecidable or void. They are bare Booleans. As
   forecasts their probability is 1, and for a constant forecast the resolution term of a proper score is zero
   by definition, whatever the outcomes. The kill criterion *"resolution ≈ 0 against a shuffled control"* would
   have fired on arithmetic, not measurement. Not killed; **not evaluable**.

**Near retirement.** On 18 September the research lead recommended dropping the name altogether: three of four
sub-claims dead, the fourth untestable, and the one live residue (who produces the validity key) better stated
without FTR's vocabulary. I think that recommendation was right about everything it examined.

**Reopened, deliberately.** It did not examine the thing FTR was for. The 791 — later 1,345 — Boolean
expectations were never a forecast of anything; testing FTR on them tested the wrong object, and a failed test of
the wrong object kills nothing. So I reopened FTR as an **open research question**, under a looser and more
exact framing: not "predict the future", but

- **future disagreement** — does the *structure* of divergence across possible futures carry information the
  runtime can act on;
- **future information requirements** — what will a future decision or a future proof need to know;
- **anticipatory evidence** — what should be captured *now* because the next action will make it
  unrecoverable or unreachable;
- **proof obligations** — can the runtime tell, before acting, that completion will become unprovable.

Status: **OPEN**. A hypothesis, with no measurement behind it yet. The reopening was a decision about what is
worth testing, not evidence that it is true.

## Part VII — The FTR formalization, as it currently stands

Everything in this section is a **candidate formalization**. None of it is implemented, and none of it is a
theorem. It is written down so that it can be attacked.

### Runtime state and history

$$
X_t = \big(W_t,\ H_t,\ G_t,\ M_t,\ C_t,\ E_t,\ \Gamma_t\big)
$$

<div class="eq-note">

World version, history, goals, the agent's and runtime's internal state (plan, tasks, subagents), completion criteria, available evidence, and calibration history.

</div>

$$
H_t = \big(O_0,\ A_0,\ E_1,\ O_1,\ A_1,\ E_2,\ \ldots,\ A_{t-1},\ E_t,\ O_t\big), \qquad H_t \not\equiv W_t
$$

### Possible futures, not a future

$$
\tau_{t:t+k} = \big(S_t,\ A_t,\ E_{t+1},\ O_{t+1},\ S_{t+1},\ \ldots,\ A_{t+k-1},\ E_{t+k},\ O_{t+k},\ S_{t+k}\big)
$$

$$
P_t(\tau) = P_\theta\big(\tau_{t:t+k} \mid H_t,\ W_t,\ G_t,\ C_t,\ M_t\big), \qquad
\mathcal{T}_t = \{(\tau_i,\ p_i)\}_{i=1}^{N},\ \ \sum_{i=1}^{N} p_i = 1
$$

<div class="eq-note">

The object is a distribution over structured trajectories — actions, effects, observations, failures, human interventions, evidence capture, completion — never "the next action".

</div>

### FTR is not a plan

$$
\boxed{\ \mathcal{F}_t \neq \mathit{Plan}_t\ } \qquad\qquad P(\tau \mid X_t,\ \mathit{Plan}_t) \neq \mathbf{1}[\tau = \mathit{Plan}_t]
$$

A plan answers *what do I intend to do?* FTR asks *which futures remain reachable from here, where do they
diverge, what will those futures require, and what should the runtime preserve or inspect now because of that?*
It must admit futures in which the plan fails, branches, stalls on a human, loses its evidence, or is replaced.
If an implementation of FTR turns out to be the planner under another name, that is a kill.

### Future disagreement

$$
D_t = 1 - \sum_{z \in Z} P(z \mid X_t)^2, \qquad \mathcal{H}_t = -\sum_{i=1}^{N} p_i \log p_i
$$

<div class="eq-note">

$$z$$ ranges over materially distinct outcome classes. $$D_t$$ is the Gini–Simpson index over those classes: near 0 when rollouts agree, toward 1 when they scatter. It does not require knowing which future is right; the open question is whether divergence is itself a useful runtime signal — for observing, preserving, asking, or delaying.

</div>

### Future evidence and proof obligations

The part of FTR I think is worth the most. Let $$E_\Omega(h)$$ be the evidence a history $$h$$ exposes when the
set of facts $$\Omega$$ is captured, and $$C(h)$$ whether the criterion holds in it. The cheapest sufficient
capture:

$$
\Omega_t^{*} = \arg\min_{\Omega}\ \mathrm{Cost}(\Omega)
\quad\text{s.t.}\quad
\forall h_i, h_j:\ E_\Omega(h_i) = E_\Omega(h_j) \Rightarrow C(h_i) = C(h_j)
$$

<div class="eq-note">

Capture as little as possible, subject to no two possible histories looking identical under the evidence while disagreeing on the criterion. For the rename, $$\Omega_t^{*} = \{\mathrm{digest}(\mathit{notes}_{\mathrm{pre}})\}$$. This is the indistinguishability condition from Part III turned into an objective; whether a runtime can estimate it before an action, for criteria written in prose, is exactly the open question.

</div>

### Proof failure is not task failure

$$
P_t^{\mathrm{proof}} = P\big(\neg\,\mathrm{Provable}(C_{t+k}) \mid X_t\big) \qquad\text{versus}\qquad P(\mathit{TaskFailure})
$$

An action can be very likely to succeed and still make success unprovable:
$$P(\text{succeeds} \mid a) \approx 1$$ while $$P(\mathrm{Provable}(C) \mid a) \ll 1$$. T4 is a small real
instance of the second quantity going to zero after the move — *for the judge's view*, even though the journal
could still prove it.

### Risk over futures

$$
R_t(a) = \mathbb{E}_{\tau \sim P_t}\big[L(\tau, a)\big] + \lambda_D D_t + \lambda_P P_t^{\mathrm{proof}}
$$

<div class="eq-note">

Three separate costs: the world ending up bad, the futures becoming highly divergent, and completion becoming unprovable.

</div>

### Meta-actions, including preserve

$$
\mathcal{X}_t = \{\textit{act},\ \textit{observe},\ \textit{test},\ \textit{ask},\ \textit{fork},\ \textit{replan},\ \textit{preserve},\ \textit{wait}\}
$$

`preserve` is the new candidate: *capture information that may become unrecoverable, or unreachable, after the
next action.* Checkpoints and rewind in today's code agents already preserve state wholesale, and speculative
execution in systems has long acted on a predicted future and rolled back when it did not arrive
[[19]](#ref-19). The candidate difference is choosing *what* to keep because of what a future proof will need —
and the cheapest rival to that, the wholesale snapshot, is the control E4 has to beat.

$$
V(\mathcal{F}_t) = -\big[\alpha\,\mathcal{H}_t + \beta D_t + \gamma R_t + \delta P_t^{\mathrm{proof}}\big]
$$

$$
x_t^{*} = \arg\max_{x \in \mathcal{X}_t}\Big[\ \mathbb{E}\big[V(\mathcal{F}_{t+1}) \mid x,\ X_t\big] - V(\mathcal{F}_t) - \lambda_C\,\mathrm{Cost}(x) - \lambda_L\,\mathrm{Latency}(x)\ \Big]
$$

<div class="eq-note">

A runtime should not compute futures without limit. It should ask which extra observation, test, fork, question to a person, or act of preservation is worth its cost now. This is value of computation and value of information [[15]](#ref-15) [[16]](#ref-16); the candidate contribution is only the new state it would be computed over.

</div>

### Version-bound forecasts, and void

$$
f_i = (W_i,\ B_i,\ \tau_i,\ p_i,\ \Omega_i,\ T_i), \qquad
\mathrm{Valid}(f_i, t) \iff B_i \simeq B_t \ \wedge\ W_i \simeq W_t
$$

<div class="eq-note">

World version, basis (observations and assumptions), trajectory or outcome class, probability, the information the forecast says the future will need, and the resolution condition. This is the same move as the approval rule in Part I: a forecast, like a decision, is bound to the world it was made in.

</div>

$$
\mathrm{Resolve}(f_i,\ O_{i+1:t}) \in \{\textsf{satisfied},\ \textsf{violated},\ \textsf{void}\}
$$

**satisfied**: the basis held and the predicted event happened. **violated**: the basis held and it did not.
**void**: the world or the premise changed so that the forecast no longer applies. A void forecast is not a wrong
one, and scoring it as wrong charges the forecaster for the weather — the same distinction V36 drew for drift.

### Calibration — a requirement, not a result

$$
y_i = \mathbf{1}\big[\mathrm{Resolve}(f_i) = \textsf{satisfied}\big], \qquad
\mathrm{BS} = \frac{\sum_{i:\,r_i \neq \textsf{void}} (p_i - y_i)^2}{\big|\{i : r_i \neq \textsf{void}\}\big|}
$$

$$
\Gamma_t = \mathrm{CalibrationHistory}(f_1, \ldots, f_t), \qquad \mathit{Trust}_{t+1} = g(\Gamma_t)
$$

<div class="eq-note">

The Brier score [[17]](#ref-17) over non-void forecasts, and a trust weight derived from it. None of this has been computed on MØBIUS journals, and on the current Boolean expectations it cannot be — see P4 above. It is a requirement on any future FTR experiment, not a finding.

</div>

### The candidate object, and the loop

$$
\mathcal{F}_t = \big(P_t(\tau),\ D_t,\ \mathcal{H}_t,\ \Omega_t^{*},\ P_t^{\mathrm{proof}},\ R_t,\ \Gamma_t\big)
\qquad
\boxed{\ \mathcal{F}_t = P_\theta\big(\tau_{t:t+k},\ \Omega_{t:t+k},\ R_{t:t+k} \mid H_t,\ W_t,\ G_t,\ C_t,\ M_t\big)\ }
$$

$$
X_t \rightarrow \mathcal{F}_t \rightarrow x_t^{*} \rightarrow A_t \rightarrow (O_{t+1},\ W_{t+1}) \rightarrow \mathrm{Resolve} \rightarrow \Gamma_{t+1} \rightarrow \mathcal{F}_{t+1}
$$

<figure class="fig">
<a href="/research/mobius-r3-ftr-loop.svg"><img class="fig-light" src="/research/mobius-r3-ftr-loop.svg" alt="The candidate FTR loop: reality and history feed a versioned world W_t; the FTR state F_t holds possible futures P_t(tau), disagreement D_t and H_t, future evidence Omega-star, proof failure P-proof, risk R_t(a) and calibration Gamma_t; it informs a runtime meta-decision among act, observe, test, ask, fork, replan, preserve and wait; the action produces a world transition; forecasts resolve as satisfied, violated or void; calibration updates; a new FTR state follows and loops back. A note says nothing here is implemented as FTR." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-ftr-loop-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure G.</strong> FTR as a candidate closed loop. Of everything in it, only a Boolean expectation layer exists in code today.</figcaption>
</figure>

The full formalization, with variable definitions, invariants, the status of each part and the experiments
that could kill them, is in the PDF at the end of this post.

## Part VIII — What has been killed, and what is actually open

<figure class="fig">
<a href="/research/mobius-r3-status.svg"><img class="fig-light" src="/research/mobius-r3-status.svg" alt="Research status map. Measured: cannot-tell dominated by missing prior state in three task shapes; unsupported establishment, one clear case in 20; certificate closure 0 of 11; layered determinism 0.923 and 0.795. Open: FTR as a runtime object, rollout disagreement as a signal, future information requirement, anticipatory evidence preservation, proof-failure prediction, open-provider addressability. Killed by experiment: pre-write write-set anticipation from reads, reuse costs nothing, provenance link is load-bearing, lease as approval validity. Retired as prior art: future prediction as novelty, approval capture and revalidation, false success, transition witness as a new primitive, append-only replay and per-action approval gate. Not yet evaluable: Boolean expected to Brier, zero false completions with zero opportunities, whether content variance changes outcomes." loading="lazy" /><img class="fig-dark" src="/research/mobius-r3-status-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure H.</strong> The status map. No column is a ranking; "retired" means someone else has it, not that it was wrong.</figcaption>
</figure>

| claim | status | why |
|---|---|---|
| FTR overall | <span class="st st-open">OPEN</span> | reopened as a question; no measurement yet |
| future prediction itself as the novelty | <span class="st st-retired">RETIRED</span> | predictive runtime verification [[10]](#ref-10) |
| exact prediction of future actions | <span class="st st-killed">UNSUPPORTED</span> | not the surviving claim; nothing measured supports it |
| read-only, pre-write write-set anticipation | <span class="st st-killed">KILLED</span> | median read coverage 0.25 against a < 0.5 threshold; 33/69 zero |
| Boolean `expected` → Brier / resolution | <span class="st st-ne">NOT EVALUABLE</span> | constant forecasts; resolution is zero by definition |
| predictive runtime verification | <span class="st st-prior">PRIOR ART</span> | [[10]](#ref-10) |
| rollout disagreement as a runtime signal | <span class="st st-open">OPEN</span> | known as uncertainty [[11]](#ref-11) [[12]](#ref-12); as a runtime trigger, untested |
| future information requirement $$\Omega^{*}$$ | <span class="st st-open">OPEN</span> | formalised above; no estimator |
| anticipatory evidence preservation | <span class="st st-open">OPEN</span> | E4 below |
| proof-failure prediction | <span class="st st-open">OPEN</span> | T4 is one instance of the quantity, not of a predictor |
| transition witness | <span class="st st-retired">CANDIDATE, NOT NOVEL</span> | = before-image + provenance edge + past-time operator |
| evidence horizon (the past out of the judge's view) | <span class="st st-measured">MEASURED</span> · <span class="st st-open">OPEN</span> | 45 of 74 cannot-tell, three task shapes; the general version is open |
| unsupported establishment | <span class="st st-measured">MEASURED</span> · <span class="st st-open">OPEN</span> | 1 clear case in 20; rate unknown |
| certificate closure / replayability | <span class="st st-measured">MEASURED</span> · <span class="st st-open">OPEN</span> | 0 of 11 closed; replay not yet run |
| approval as a version-bound decision | <span class="st st-prior">PRIOR ART</span> | implemented and measured here; published in [[1]](#ref-1) [[2]](#ref-2) [[4]](#ref-4) |
| false success / evidence substitution | <span class="st st-prior">PRIOR ART</span> | named and measured at scale [[18]](#ref-18); R2 is a replication |
| "0 false completions" in R3 P3 | <span class="st st-ne">NOT EVALUABLE</span> | 0 opportunities — every valid row passed its checker |

Three more that died in this period and belong on the record, because they were ours: *reuse costs nothing*
(OV-1), *the provenance link is load-bearing* (PP-1), and *MØBIUS is alone in refusing a stale edit* (the CLI
column). And two at the level of design, from the research lead's survey of ten code-agent products (read from
documentation, not run): a synchronous per-action approval gate is what several products already ship as a
confirmation mode — and are moving away from for usability — and a replayable append-only event log is a
headline feature of at least one open agent SDK. Neither is a contribution.

Two engineering defects surfaced along the way, both real, neither a research result: the filesystem provider
turns its freshness check off entirely when the target did not exist at approval time and then writes without
`O_EXCL` — so a file a third party creates in that window is silently overwritten; and `fs.move` checks the
destination and then renames, a check-then-act window. Both are one-flag fixes the operating system already
offers. The addressability defect is similar: 181 of 1,345 path assertions a model wrote can be shown
unresolvable *before* dispatch by a static check, because a directory's content lives at `entries[i].content`
and the path language has no search. The model itself reached for the missing syntax — it wrote JSONPath filters
like `entries[?(@.path=='notes.md')].content` seven times, all in the unresolvable set. For a closed set of
providers this is engineering. For an open ecosystem of third-party tools whose result shapes are unknown until
run time, whether a specification can be checked for addressability before it is relied on is, as far as I can
find, open.

On the manuscript: a paper built around the approval mechanism was **planned and targeted** at USENIX OSDI ’27.
The project's own readiness audit returned a conditional no-go on 10 September, and the literature since has
removed the mechanism contribution it would have rested on. It is a **manuscript in progress**, not submitted,
and what it becomes — a characterization of how agent runtimes fail and are verified, rather than a new
mechanism — is a decision I have not made.

## Part IX — MØBIUS as an instrument

Looking back over the fortnight, the pattern is consistent enough to name. I proposed a mechanism. An experiment
or a paper killed the claim that it was new, or the claim that it worked. What was left was a narrower question
the mechanism had been standing on. Approval revalidation narrowed to *what is a decision bound to*. The
completion judge narrowed to *what the judge is shown*. That narrowed to *what the runtime keeps in view about
the past*, and from there to *what a completion record must contain to be believed later*. FTR narrowed from
*simulate the future* to *know what the future will need you to have kept*.

None of those endpoints is a feature. They are questions about what an autonomous-agent runtime has to treat as
data. A conventional runtime manages state, processes, memory, I/O and permissions. An agent runtime is also,
whether it admits it or not, managing world versions, human decisions bound to those versions, evidence and its
provenance, proof obligations for criteria written in prose, information that will stop being reachable, plans
that are uncertain and change, long-running autonomy, other agents, and the correctness of *done*.

> MØBIUS is not only the system being studied. It is increasingly the instrument used to discover what agent
> runtimes are still missing.

That reframing is only worth anything if the instrument is trustworthy, which is why the unglamorous parts —
predictions committed before code, every invalid row kept, every refuted prediction left standing and signed —
matter more than any single result above. A recent audit of fifty agent repositories found none reporting how
many runs failed or were dropped alongside their scores [[20]](#ref-20). They are the reason a zero with no opportunities behind it was caught
rather than published as a result.

### Unnamed phenomena

The method changed too. I have stopped looking mainly for bugs to fix or gaps in papers, and started keeping a
list of things that happen and do not yet have a good name — then trying to kill each one before it gets a name:

```text
phenomenon → minimal counterexample → reproduction across unrelated tasks → prior-art search
           → abstraction → kill test → runtime consequence
```

The current entries, each at a different stage:

- **Two futures with the same end state and different causal histories, and a criterion whose truth differs
  between them.** Minimal counterexample: Figure D. Reproduced across three task shapes. Abstraction attempted
  (transition witness) and retired as a primitive. Runtime consequence: open.
- **A goal whose completion is a predicate over history, not over the current state.** Same evidence; this one I
  think is the most general.
- **Information that exists before an action and is gone after it, while a future proof depends on it.** Not yet
  observed here — in every case measured, the past was captured and merely out of view. I have a minimal
  construction (move without a prior read) and no reproduction. It stays a hypothesis.
- **Divergence among rollouts as a signal in itself, rather than a prediction error.** No data. It is the
  cheapest FTR experiment to design and the one most likely to reduce to known uncertainty estimation.
- **A verdict that is right about the world and unsupported by its evidence.** One instance, audited by hand.

The test every entry has to pass is the same: can I build two worlds that the runtime's current state cannot
distinguish, but whose correct decision differs? If yes, something is missing from the state. If the missing
thing is already a known object, it gets that object's name, and MØBIUS gets an implementation, not a
contribution.

## Next experiments

Only ones that can come out either way.

**E1 — Evidential soundness replay.** Freeze criterion, prompt, evidence and model for the T4 post-only
evidence (where $$E \not\models C$$ by construction) and re-ask the judge N times. Measure
$$\hat p_{\mathrm{est}} = \tfrac{1}{N}\sum_i \mathbf{1}[J_i(E, C) = \textsf{established}]$$. If it is zero across
N, repetition 3 was not reproducible from its inputs and the cause is elsewhere (the second read's framing, or
chance). If it is not zero, unsupported establishment is a property of the judge under this evidence.

**E2 — Evidence-horizon intervention.** Four arms on the transition-shaped tasks: post-state only; post plus the
genuine pre-state observation; post plus a typed transition witness; post plus the proposer's *self-claim*
("fs.move preserves the inode"). The hypothesis is that the two genuine arms raise justified `established` and
the self-claim arm does not. If the self-claim moves the judge as much as the evidence does, the judge is
reading assertions, not evidence, and ADR 0043's premise fails.

**E3 — Certificate closure audit and replay.** For every `established`, compute $$J_i$$ and $$C_i$$, check
$$J_i \subseteq C_i$$, and re-judge from $$C_i$$ alone. Prediction: in the eight load-bearing cases the replay
does not return `established`. This one is cheap and should run before any fix, so that the fix has a baseline.

**E4 — Anticipatory evidence preservation.** Before a world-changing action, give the runtime one extra choice —
`preserve` or proceed — on tasks where a later criterion depends on pre-state and on matched tasks where it does
not. Measure whether an FTR-style estimate of $$P^{\mathrm{proof}}$$ picks out the facts that the action will put
out of reach, against a baseline that preserves nothing and one that preserves everything. This is the
experiment that decides whether the most promising part of FTR is a runtime object or a paragraph. Its hardest
control is the obvious rival: "always snapshot the files you are about to touch", which costs almost nothing on
a filesystem and may leave nothing for prediction to add.

## Closing

What I understand better than I did on 6 September is not what the answer is. It is what the answer is not. It
is not approval revalidation, which exists. It is not a judge with a better prompt, since most of what the judge
could not tell it was right not to tell. It is not simulating the future, which predictive monitoring already
does. It is not keeping history, which databases have done for forty years.

What is left is a suspicion, stated as a question. An autonomous-agent runtime may need to manage more than
state, actions and observations: history, world versions, the basis of each decision, possible futures, the
information those futures will require, proof obligations, and the relations that must hold across a
transition. Which of those deserve to be first-class primitives, and which are ordinary engineering wearing new
names, is **open**. The next experiments are designed so that most of those candidates can die.

---

<a class="resource-card" href="/research/FTR_Core_Formalization_2026-09-19.pdf">
  <span class="rc-title">FTR Core Formalization</span>
  <span class="rc-desc">Current mathematical formulation, assumptions, research status and open experiments — including what has been killed and what is only a candidate.</span>
  <span class="rc-meta">PDF · 12 pages · Updated 19 Sep 2026</span>
</a>

### References

Every entry below was checked against its arXiv record or DOI on 19 September 2026. Preprints are preprints; I
have not assumed peer review where the record does not state it.

1. <span id="ref-1"></span>I. Santos-Grueiro. *Temporary Authority, Permanent Effects: Commit-Time Authorization for LLM Agents.* arXiv:[2607.10487](https://arxiv.org/abs/2607.10487), 2026.
2. <span id="ref-2"></span>E. Chen, S. Wang, C. G. Brinton. *Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory.* arXiv:[2609.03340](https://arxiv.org/abs/2609.03340), 2026.
3. <span id="ref-3"></span>S. Khan. *S-Bus: Automatic Read-Set Reconstruction for Multi-Agent LLM State Coordination.* arXiv:[2605.17076](https://arxiv.org/abs/2605.17076), 2026.
4. <span id="ref-4"></span>M. Rashidi. *The Balkanization of Execution-Security Research for AI Coding Agents: Isolation, Access Control, and Time-of-Check-to-Time-of-Use Vulnerabilities.* arXiv:[2607.05743](https://arxiv.org/abs/2607.05743), 2026.
5. <span id="ref-5"></span>K. Havelund, G. Roşu. *Synthesizing Monitors for Safety Properties.* TACAS 2002. [doi:10.1007/3-540-46002-0_24](https://doi.org/10.1007/3-540-46002-0_24). See also M. Leucker, C. Schallhart, *A brief account of runtime verification*, JLAP 2009, [doi:10.1016/j.jlap.2008.08.004](https://doi.org/10.1016/j.jlap.2008.08.004).
6. <span id="ref-6"></span>R. Snodgrass, I. Ahn. *Temporal Databases.* IEEE Computer 19(9), 1986. [doi:10.1109/MC.1986.1663327](https://doi.org/10.1109/MC.1986.1663327).
7. <span id="ref-7"></span>P. Buneman, S. Khanna, W.-C. Tan. *Why and Where: A Characterization of Data Provenance.* ICDT 2001. [doi:10.1007/3-540-44503-X_20](https://doi.org/10.1007/3-540-44503-X_20).
8. <span id="ref-8"></span>T. J. Green, G. Karvounarakis, V. Tannen. *Provenance Semirings.* PODS 2007. [doi:10.1145/1265530.1265535](https://doi.org/10.1145/1265530.1265535).
9. <span id="ref-9"></span>G. C. Necula. *Proof-Carrying Code.* POPL 1997. [doi:10.1145/263699.263712](https://doi.org/10.1145/263699.263712).
10. <span id="ref-10"></span>L. Lindemann, X. Qin, J. V. Deshmukh, G. J. Pappas. *Conformal Prediction for STL Runtime Verification.* arXiv:[2211.01539](https://arxiv.org/abs/2211.01539), 2022.
11. <span id="ref-11"></span>X. Wang, J. Wei, D. Schuurmans, Q. Le, et al. *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023. arXiv:[2203.11171](https://arxiv.org/abs/2203.11171).
12. <span id="ref-12"></span>L. Kuhn, Y. Gal, S. Farquhar. *Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation.* ICLR 2023. arXiv:[2302.09664](https://arxiv.org/abs/2302.09664).
13. <span id="ref-13"></span>A. Z. Ren, A. Dixit, A. Bodrova, S. Singh, et al. *Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners.* CoRL 2023. arXiv:[2307.01928](https://arxiv.org/abs/2307.01928).
14. <span id="ref-14"></span>J. de Kleer. *An Assumption-based TMS.* Artificial Intelligence 28(2), 1986. [doi:10.1016/0004-3702(86)90080-9](https://doi.org/10.1016/0004-3702(86)90080-9).
15. <span id="ref-15"></span>S. Russell, E. Wefald. *Principles of Metareasoning.* Artificial Intelligence 49, 1991. [doi:10.1016/0004-3702(91)90015-C](https://doi.org/10.1016/0004-3702(91)90015-C).
16. <span id="ref-16"></span>R. A. Howard. *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics 2(1), 1966. [doi:10.1109/TSSC.1966.300074](https://doi.org/10.1109/TSSC.1966.300074).
17. <span id="ref-17"></span>G. W. Brier. *Verification of Forecasts Expressed in Terms of Probability.* Monthly Weather Review 78(1), 1950. [doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2).
18. <span id="ref-18"></span>L. Advani. *From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents.* FAGEN Workshop at ICML 2026. arXiv:[2606.09863](https://arxiv.org/abs/2606.09863).
19. <span id="ref-19"></span>E. B. Nightingale, P. M. Chen, J. Flinn. *Speculative Execution in a Distributed File System.* SOSP 2005. [doi:10.1145/1095810.1095829](https://doi.org/10.1145/1095810.1095829) — the systems precedent for acting on a predicted future and rolling back when it does not arrive.
20. <span id="ref-20"></span>C. Masters, Z. Liu, S. V. Albrecht. *Rollout Cards: A Reproducibility Standard for Agent Research.* arXiv:[2605.12131](https://arxiv.org/abs/2605.12131), 2026 — on reporting failed and dropped runs alongside scores, which is why every invalid row above is kept.
