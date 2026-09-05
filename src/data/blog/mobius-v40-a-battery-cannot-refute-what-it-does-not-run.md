---
title: "MØBIUS V40 — A Battery Cannot Refute What It Does Not Run"
description: "The change passed all four of its pre-registered predictions and a five-mutation battery with nothing surviving. Then the full suite refuted it, and it was reverted. What ships is a pin and the reason."
pubDatetime: 2026-09-05T19:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

This version shipped no production change. It is here because of how it failed.

### First, a recommendation withdrawn

V39 closed by proposing a conformance pin on `ObservationSource`: *the request names the resource the
gap named*. Three versions had been mismeasured by a test double standing in for a seam, and a pin
looked like the fix.

**That recommendation was wrong, and it was wrong because it was written without reading
`revalidation.ts` or `narrow-look.ts`.** Both already handle a port that ignores targeting, and they
handle it better than a pin would:

> It also does not trust that the look went where it was asked. `ObservationSource` is a model seam;
> a port that ignores a targeting request and returns something unrelated must not be able to restore
> work. Coverage is checked against the facts that came back, so an observation that does not mention
> the resource yields `disputed` rather than a verdict derived from silence.

The verification plane does the same in its own vocabulary — an observation that does not cover the
asserted path yields `undecidable`. And `narrow-look.ts` deliberately **forwards** an off-target look
rather than correcting it, with the reason spelled out: correcting it would mean the downstream
coverage check *"would then only ever see looks that had already been corrected, and the defence would
go untested in production while appearing to hold."*

A conformance pin would have been a third defence against a failure two already cover, and would have
blunted the second — the exact failure that docstring warns about.

### The narrower thing that was actually wrong

The runtime is right not to trust the look. But it never tells the look what it needs.

```
loop.ts:1555  #targetedLook  gap = { …, targetResources: resources, resource }
loop.ts:1842  #verifyNext    gap = { …,                             resource }
```

And `resource` there is not the thing being looked at: it comes from `#bindActiveResource`, whose own
comment reads *"Remember which world the last look was taken in."* Which world, not which thing.

So the verifying gap carries a sentence and a workspace. And `narrowLook` computes coverage as

```ts
const targets = context.gap.targetResources ?? []
if (targets.length === 0) return true
```

recording `coversTargets` into the port's attempt trail. On every verification look, `targets` is
empty — so that diagnostic is wired, recorded, and **unconditionally true**. A pin that cannot go red,
appearing in production code rather than in a test.

The fix looked obvious: aim the verifying look from the receipt of the action being verified, using
the field and the extraction that already exist.

### It passed everything, and it was wrong

Four predictions, all confirmed. A five-mutation battery, nothing surviving. Then the full suite:

```
V21-P4 — a real port that looks somewhere else cannot restore work
  → work was restored on an off-target look: expected 'failed' to be 'blocked'
```

That is the safety property `revalidation.ts` exists to hold — the one this version's own opening
section had just finished explaining was already in place. Nine failures across four files:
`v21-1-observation-port`, `v18j1-revalidation`, `v18j2-observation-accounting`,
`v18j3-budget-enforcement`. **None of which any battery in this line runs.**

Reverted.

### Why the field belongs to one look

`reflex.ts` had already said it, in a file read before the change was written:

> a subject the runtime knows precisely, **because it recorded the dependency itself**

Revalidation knows its subject — it is re-reading resources it recorded a dependency on. Verification
does not. It knows what was **written**, and what was written is not what the assertion is **about**.
The pin that ships measures exactly that: the receipt names `a.txt`, the assertion is `entryCount`,
and the answer is in the directory listing. A look aimed by the receipt reads the file and misses it.

There was a second error stacked on the first. `v18j1`'s fixture *honours* targeting — the behaviour
the change was asking ports to have — and uses `targetResources.length > 0` to know **which of the two
looks it is being asked for**: *"the next request out is the revalidating one."* Putting the field on
both gaps made the two looks indistinguishable to any port that reads it.

One mechanism answering two questions — the shape this repository has undone five times, introduced
here by the version written to be careful about seams.

### The finding worth keeping

The battery ran six files. I chose all six, and all six were about this line of work — V35 to V40.
Every mutation died. The change was wrong the whole time, and the evidence lived in four files about
the observation port and the revalidation plane: precisely the machinery a change to the observation
gap touches.

**A battery measures the tests you hand it.** Its guards defend against a mutation that does not land
and a mutant that does not compile. Nothing in it defends against a test list that does not cover the
blast radius.

Five consecutive versions of green batteries had made the full suite feel like a formality — V35
through V39 each ran it, and each time it said exactly what the battery had already said. That is the
conditioning, and it is why the suite has to run on every version rather than when a change *feels*
risky.

The rule this yields is narrower than "run the suite":

> **The test list must be derived from what the change touches, not from what the version is about.**

A gap handed to `ObservationSource` is touched by every plane that consumes an observation, and the
batteries for those planes already existed.

### What ships

`loop.ts` is back to what it was after V39.

- **A pin**: the verifying gap names no target resources, and — measured, not asserted in a comment —
  the receipt names the file while the assertion is about the directory. A version already tried to
  move this field once.
- **A battery of two mutations**, both red: adding `targetResources` to the verifying look kills 10
  tests; removing it from the revalidating look kills 8.

The refutation is now something the repository checks, rather than something this post remembers.

### A note on publishing this one

There is an obvious version of this project's log where V40 does not appear, because nothing shipped.
That version would be a worse record. A change that passes its own predictions, passes its own
battery, and is still wrong is the most informative thing to happen in six versions — and it is only
visible if the failed ones get written down with the same care as the rest.
