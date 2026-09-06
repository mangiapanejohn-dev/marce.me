---
title: "MØBIUS V41–V45 — Why the Runtime Never Looked Before It Acted"
description: "Four versions had arrived at the same open question from four directions. The runtime had a mechanism for it all along, and it never produced a usable look — for three independent reasons. Two of the four fixes went to the wrong site first."
pubDatetime: 2026-09-06T10:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

Four versions in a row had ended on the same sentence. *Nothing makes the runtime look before acting
on purpose — it does so only when a previous action's verification happened to look.*

The runtime has a mechanism for exactly this. `ActionPrecondition` with `kind: 'fresh-observation'`
is the model saying *this action rests on something I have not looked at yet*. V41 asked why it never
produces a look, and the answer was three defects in one path.

<a class="fig-plate" href="/research/mobius-a03-action-lifecycle.png">
  <img src="/research/mobius-a03-action-lifecycle.png" alt="One proposed effect from cognition to verification, in twelve steps: ActionIntent, PreconditionGate, unknown.raised, route gap, fresh observation, resolution check, admission gates, compile, dispatch, EffectReceipt, VerificationResult, forecast resolution. Two defects are marked on it — the route gap flipping no-route against look, and one unknown raised against thirty-one resolved and no dispatch." loading="lazy" />
</a>

<p class="fig-note">One effect, cognition to verification. The two red boxes are what V41 measured; everything after step 6 is what never happened. Click to open it full size.</p>


Two of the four versions that fixed them aimed at the wrong site first, and that turned out to be the
more interesting half.

### V41 — measuring, and declining to fix

One intent, one precondition, three probes.

**The routing of a pre-action look is decided by a free-text field.** With a sentence a proposer would
plausibly write:

```
3 unknown.raised   question: "the write rests on what is there"
4 depth.changed    EXPLORE: a factual unknown is open and something can be looked at
5 goal.abandoned   no-route: 2 capabilities were the right effect class but shared
                   no term with the described need (fs.observe, repo.search)
```

The runtime does everything right up to the last step. `needFor` sets `question: precondition.because`
and `classifyUnknown` makes that the gap description the lexical reflex routes on.

This is deliberate, and `precondition.ts` says so: *"an intent that declares a vague reason gets a
vague route, which is the right incentive."* The measurement does not dispute the intent behind that
— it disputes the description. A vague reason does not get a vague route. It gets **no route, zero
observations, and an abandoned goal**, while `satisfies: [precondition.subject]` on the same object
holds the noun precisely. And an incentive requires the incentivised party to see the consequence;
abandonment is not a gradient.

**Rewording one field turns the run around** — and then it does not stop:

```
unknown.raised 1 · observation.received 31 · unknown.resolved 31
action.dispatched 0 · abandoned "no terminal state within 32 turns"
```

One question, raised once, recorded as answered thirty-one times, never answered.

V41 fixed none of it, and that was the version. Repairing the routing alone converts a failure that
costs nothing into one that costs 31 gated, charged observations — and the rest is a change to the
unknown lifecycle across five planes that each have their own test batteries. The version before it
had just been burned by exactly that.

### V42 — a field that means one thing, at every site that writes it

`Unknown.satisfies` is defined by the protocol as *"`SuccessCriterion` ids that resolving this unknown
would advance."* `precondition.ts` writes `precondition.subject` there — a file path, an approval
name — while all three readers treat it as criterion ids.

So: fix the writer. That was implemented, and the battery's own baseline refuted it.

`precondition.ts` reads `state.evidenceByCriterion[subject]`. Filing evidence under the subject is not
a mislabel — **it is the mechanism** by which `failure-reproduced` and `hypothesis-supported` ever
become satisfied. Emptying `satisfies` made the evidence-before-fix scenario never dispatch at all:

```
expected -1 to be greater than 0
```

The measurement that missed it had listed the readers of `#evidenceByCriterion` inside `loop.ts` and
in `completion.ts`, found them all keyed by criterion id, and never asked *who else is handed the
record*. The precondition gate is. That map carries two key spaces on purpose — criterion ids for
completion, precondition subjects for the dispatch gate — and its name says one of them.

Both internal meanings are load-bearing. Only one is ever **promised**: `PendingQuestion.satisfies`
goes to a client, documented as criterion ids, and a `user-authority` precondition was suspending with
`["deploy-approval"]` while the goal's criterion was `c1`. The fix is at that boundary, and the rule
is not invented — `narrow.ts` already refuses a *model* that declares an undeclared criterion in the
same field.

### V43 — a resolution the look did not produce

V41 read the 31 resolutions as *`unknown.resolved` means a look happened, not a question answered*.
The mechanism is sharper:

```
observation.evidence length: 0
unknown.resolved.by length:  0
```

The look came back carrying no evidence, so the event was emitted with `by: []` — and the projection
counts an unknown resolved only when `resolvedBy` is non-empty. The runtime's own state already
treated all 31 as meaningless. They were not claims anything acted on; they were false records.

V43 stopped writing them. It did **not** stop the repeat, and its test pinned that it did not.

Its designed change — putting a memory of explored needs in the precondition gate — was implemented,
worked exactly as predicted, and changed nothing observable. The selector chooses EXPLORE from an open
unknown in the projection, not from the gate's needs.

Recorded along the way: `fs.observe` attaches evidence in exactly one case, a file whose text is
shaped like instructions to an assistant. A directory listing carries none; a plain file read carries
none. So the explore-and-resolve path was inert on that provider, and the test suite's control had to
be built out of the prompt-injection advisory.

### V44 — a question already asked of the world

The stop was already there:

```ts
const actionable = await this.#raiseNeeds(report, state)
if (!actionable) {
  return { stop: 'stuck', reason: `dispatch of ${intent.id} is withheld and nothing can lift it: ${report.withheldBecause}` }
}
```

It was unreachable, for two reasons that had to move together. Rule 6 of the selector picks the first
open observable unknown with no memory of having explored it, so ACT was never chosen again. And
`#raiseNeeds` treats an open unknown as actionable whether or not anything has been done about it, so
a selector-only fix would have converted 31 looks into 32 withheld ACTs.

```
before   observation.received 31 · abandoned "no terminal state within 32 turns"
after    observation.received  1 · stuck
         "dispatch of i1 is withheld and nothing can lift it:
          fresh-observation(settings.json): nothing observed so far names \"settings.json\""
```

Nothing new was invented. The stop, the reason and the filter were all already there; what was missing
was one fact and the two places that had to read it.

#### A test that was passing on the defect

`v18f3-session-affinity` went red. It asserts that the active resource binds after an observation and
reaches the route, and checked that by requiring **more than one** routed turn.

The second routed turn was a **repeat look** — the behaviour V44 removes. And the ACT that should have
supplied it had been ending `no-route` for years, because the intent's desired effect shared no term
with any writing capability. The test had been green on a vehicle it did not intend, while the turn its
own comment describes was failing silently.

### V45 — the runtime knows what the look is for

The reflex has supported slot routing all along, and prints, when it has none, *"semantics: none —
this route was decided on text alone."* Routed against the real capability graph with V41's sentence:

```
text only                -> NO ROUTE
inspect/path/existence   -> fs.observe
inspect/file/content     -> fs.observe
```

So the runtime could always have routed the look. What it could not do was **say what the look was
for**. `ActionIntent.semantics` gave the proposer a slot channel; nothing gave one to the runtime,
which for a precondition knows the subject exactly and the kind from a closed enum.

`Unknown` gains an optional `semantics`, symmetric with the intent's, filled from the kind — a total
mapping over a closed enum, and only for the two kinds a look can close.

`question` is untouched. The proposer's sentence is still what reaches the trace and a wire question;
a person asked to approve something should read the reason its author gave. What changed is what the
**router** is given, not what a reader is told.

A `target-exists` precondition on a file that exists, with a reason sharing no term with any reading
capability, now dispatches and the goal completes. Before, it was `no-route` with nothing observed.

And routing the look exposed a hole in V44: a `fresh-observation` on an absent file routed, and then
took 32 *failed* looks. V44 counted a need as explored only after a look landed. For a refused or
unaffordable look that is right — the gate and the budget said no, and conditions change. For a look
that was permitted, affordable, taken, and answered *"I looked and could not see"*, it is not.

### What the five versions actually taught

**Two fixes went to the wrong site, on opposite sides of one misreading.** V42 emptied a field at its
writer and broke a reader that depended on it. V43 wrote a memory to a site no reader consults. The
question neither version asked early enough was *who actually reads this*.

**A control that keeps moving does not belong to the version holding it.** One assertion pinned the
shape of V41's run as a *nothing else moved* control. V43 moved its resolution count; V44 moved its
look count. It was retired rather than rewritten a third time — a control rewritten by every
subsequent version is tracking current behaviour under a name that claims otherwise.

**And V41's test file is gone.** It shipped no code; it pinned three defects and a reason for not
fixing them. Every one has now been acted on, and its last pin was not refuted but **made vacuous**:
it asserted that rewording `because` changes the outcome, and under V45 both wordings produce the same
run. The record of what it measured is its plan document. The tests belong to the versions that own
the claims.

### The map, for what it is worth

<a class="fig-plate" href="/research/mobius-v42-runtime-architecture.png">
  <img src="/research/mobius-v42-runtime-architecture.png" alt="The whole runtime at V42, in five bands: a live execution spine from human authority through goal, model port, ActionIntent, premise resolution, admission gates, compile, dispatch, world, receipt and verification; cognition and observation, holding the unknown lifecycle, gap routing and fresh observation; world and freshness, holding WorldRevision, ActionBasis and the staleness guard; durability and calibration, holding the durable journal, project() and the forecast calibration fold; and a dotted research frontier for the future trajectory reasoner. Solid edges are live, dashed are declared but dormant, dotted are research." loading="lazy" />
</a>

<p class="fig-note">The whole runtime at V42 — the version in the middle of this post. Solid is live, dashed is declared but dormant, dotted is research. Open it full size; at this width it is an orientation aid rather than a readable diagram.</p>
