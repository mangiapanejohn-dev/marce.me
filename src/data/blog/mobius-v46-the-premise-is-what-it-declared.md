---
title: "MØBIUS V46 — An Action's Premise Is What It Said It Rested On"
description: "The forecast line's last open row. A field existed for exactly the missing scope and every provider wrote []. The obvious way to fill it turned out to reproduce the scope that had already been rejected."
pubDatetime: 2026-09-06T10:15:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

Six versions ago the forecast table learned to say *the world this decision was made in has moved* —
and to report it rather than score it. The reason was scope. The premise witnesses whatever the
grounding observation happened to capture, which for a directory listing is the whole tree, so voiding
on it would have restored the over-broad failure the version before had spent itself removing.

That left a row open:

| window | scope | what it can honestly say |
|---|---|---|
| effect → verdict | this action's receipt | `void` — graded against the wrong world |
| premise → verdict | everything observed | *reported* — this decision's world moved |
| premise → verdict | `ActionBasis.targets` | would license voiding — **unwritten** |

`ActionBasis.targets` is documented as *"targets whose identity must still resolve for the action to
be valid."* That is precisely the missing scope. Every provider writes `[]`.

### The measurement decided the design

The obvious fill is `grounding.targets` — the observation the action was compiled against, which is
what the compiler already copies from. Measured on the earlier version's own two-action fixture:

```
a2 grounded on:        obs-…-1
resource facts on it:  ["notes.txt", "other.json"]
a2 acts on:            settings.json
```

`notes.txt` is the bystander that whole argument was built on. It is in the grounding observation
because the look was a directory listing. And `settings.json` — what the action actually writes — is
not in the list at all.

**So the field was not unfilled through neglect.** Its obvious source is the premise itself, and
scoping the premise to the premise is the identity function. Worse, the action's own subject isn't
even in it.

### There is a declaration, and it is not the observation

<figure class="fig-pan-wrap">
  <div class="fig-pan"><img src="/research/mobius-a06-runtime-truth-model.png" alt="The runtime truth model: observation and evidence answer or narrow an unknown and can raise an invalidation, which invalidates a premise or assumption. A premise supports a decision or intent, which is checked by authority and preconditions and carries a forecast of the expected outcome. The compiled effect causes an outcome that verification adjudicates, and forecast against resolved outcome is calibration. A pending effect resting on an invalidated premise must not commit." loading="lazy" /></div>
</figure>

<p class="fig-note">What a decision depends on, and how evidence invalidates execution downstream of it. The premise column on the left is what this version gave a scope to.</p>


`ActionIntent.preconditions` is the action saying what it rests on, before dispatch.
`fresh-observation(X)` means *this action depends on X having been looked at*. It is the only thing in
the runtime that means what `targets` means — and the compiler already receives the intent, so nothing
had to be plumbed.

Only the two kinds a look can re-acquire are carried. An approval is not a thing to re-observe, and a
task another action must finish is not either; putting them in `targets` would say *re-observe this to
revalidate the action*, which no look does.

### Checked before built, because of what happened last time

`basis.targets` has three readers, and a version six back had filled a targets-shaped field and reached
a plane it had not considered — restoring work on an off-target look. So:

- `staleness.ts` consults targets only under `freshness: 'revalidate'`. The compiler stamps
  `advisory`, whose branch returns `proceed` without reading them.
- `diagnosis.ts` reads `targets.length` as a diagnostic signal.
- the precondition gate's `namesSubject` reads **`observation.targets`** — a different field on a
  different object.

A recording change, not a control change. The test that pins it asserts the direct evidence — both
actions reached the provider, and the ending contains neither of staleness's own words — after a first
cut asserted "the run does not end abandoned", which is a proxy that fails for reasons unrelated to
the claim.

### What it buys, and what it deliberately does not

`premiseMoved` is now scoped to the declaration when there is one. The same bystander movement is
reported for an action that declared no dependency, and out of scope for one that did.

**An action that declared nothing keeps the tree-wide report.** Absence of a declaration says nothing
about what an action rests on; narrowing it to nothing would turn silence into a claim.

And nothing voids. *This forecast was graded against the wrong world* and *the world this decision was
made in has moved under something it declared* are still two claims, and narrowing the second does not
make it the first. Whether they should merge is a design question this version declined to answer — it
narrowed the report and stopped.

### The survivor

One mutation survived the first battery: carrying the kinds no look re-acquires. No loop fixture can
reach that filter, because **an action only dispatches once every precondition is satisfied** — a
`user-authority` one suspends the run, a `dependency-verified` one withholds it, so an excluded kind is
never in hand at compile time.

Killed by exercising the compiler directly, which is pure and needs no loop. That is the second
survivor in two versions with the same cause: the assertion was written against the fixture that was
convenient rather than against the branch. A battery finds that; reading the test does not.

### What is left

<figure class="fig-pan-wrap">
  <div class="fig-pan"><img src="/research/mobius-a05-ftr-research-target.png" alt="The FTR research target: several execution actors each with an independently sealed forecast, feeding a shared evidence field that tracks provenance, dissent and evidence ancestry, where agreement between sources does not imply independence. Competing hypotheses feed active falsification, which chooses the cheapest discriminating experiment, and an epistemic scheduler allocates compute to decision-critical uncertainty. A reality-admission step asks whether premises are fresh and evidence independent before the existing runtime gates commit an effect, and outcomes feed calibration by proper scoring." loading="lazy" /></div>
</figure>

<p class="fig-note">The target topology, not the current implementation. Everything on this diagram is dotted for a reason — and the ceiling above is why the left-hand column is still theory.</p>


The scope is only as good as the proposer's willingness to state a dependency, and nothing yet rewards
stating one. Most actions declare nothing, so most keep the tree-wide report — honest, and a ceiling.
