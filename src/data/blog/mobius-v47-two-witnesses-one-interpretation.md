---
title: "MØBIUS V47 — Two Witnesses and One Interpretation"
description: "The one frontier hypothesis nothing had touched: a runtime manufacturing independent evidence roots. A census says why it is not reachable from here, and the obstacle is not the missing emitter everyone would reach for first."
pubDatetime: 2026-09-06T11:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

The frontier review that started this whole line closed with a list of hypotheses, and one of them —
**a runtime manufacturing independent evidence roots** — was the only one nothing in the surveyed
corpus attempted. Twelve versions later nothing here had touched it either.

This version does not build it. It measures what would have to be true first, and the answer is not
the thing you would reach for.

### Four refs, two roots

A census over a two-action run, counting every `EvidenceRef` the journal carries:

```
evidence by carrier : {"receipt": 2, "verification": 4}
evidence by trust   : {"observed": 4, "asserted": 2}
observations taken  : 0
```

Reading the refs rather than the counts shows the carriers are not independent:

```
R observed | filesystem:post-write-stat | a.json is 17 bytes with digest sha256:4e5e21c2…
V observed | filesystem:post-write-stat | a.json is 17 bytes with digest sha256:4e5e21c2…
V asserted | result:fs.write            | the provider result for fs.write decided 1 of 1 assertion(s)
```

The verdict's `observed` ref **is the receipt's ref**, carried forward. So a run that looks like four
pieces of evidence has two roots, one per action, and each is a single read.

That root is real rather than an echo — `post-write-stat` re-reads the bytes from disk and digests
them, so it is not the write's own arguments coming back. What it is not is *independent*. There is
one witness, and nothing else in the run has an opinion about the same fact.

### The obvious answer is already pinned, twice

`contradiction.detected` is folded by two projectors, weighted `0.95` in the working set — the highest
of any kind — and routed by the meta-action selector above every unknown. Nothing emits it.

That is **not a finding**. A census test pins it with a reason: *"belief revision has no owner rather
than an idle one; writing emitters to satisfy the switch statements would be inventing cognition by
opportunity, which ADR 0007 refuses."* A second test reaches the same fact from the depth gate:
*"wired but starved — the gap is upstream."*

Worth checking before claiming a discovery, and it changed what this version is about. The upstream
gap is not that nobody wrote an emitter. It is that **there is never a second opinion for a first one
to contradict.**

### Except on one path, where V37 already compares two

The `fresh-observation` verdict path produces two independent reads of the same resource: the
receipt's `post-write-stat` digest, and the verifying observation's digest. An earlier version built
that comparison and recorded what it found:

```
RCPT settings.json = dbe90cd729a1   worldRevisionAfter = 1
OBS  settings.json = a7254c4184a3   worldRevision      = 1
```

Two witnesses, one resource, disagreeing **at the same recorded world revision** — nothing the
provider did explains the difference.

V37 calls that `void{drift}`: *the world moved, and this forecast was graded against the wrong one.*
That is one reading. The other is that one of the two reads is wrong. At equal revisions the two are
indistinguishable, and the runtime hard-codes the first.

The default is almost certainly right — a runtime that suspects its own reads concludes nothing — but
it is a default, and until now it was indistinguishable from a fact. It is pinned as one.

### Why nothing was built

Giving `contradiction.detected` a producer is available today: V37 already computes the disagreement.
It would be wrong twice over.

The belief plane's consumers are starved end to end. `FailureDiagnosis.invalidates` is computed and
never read; `assumption.made` has no producer, so the set a contradiction would invalidate is always
empty. A producer would light one switch statement and leave a half-wired path behind it.

And the disagreement is already reported, in the plane that owns it. Emitting it a second time as a
belief event is two mechanisms for one observation — a shape this project has collapsed five times.

**H5 is located, not closed.** What stands between is a second *source*: another provider, another
modality, or a witness the acting provider does not own. This runtime has one provider per resource,
so the nearest real step is composition — `repo` and `filesystem` both see a working tree — rather
than anything inside the loop.

### Two mutations that were badly built

The first battery reported one survivor and one unreported, and **neither was about the code**.

One mutation was written as `… + void 0` — a no-op. It survived because it changed nothing, which is
a mutation that does not mutate.

The other could not be compiled, and that turned out to be a property worth knowing:
`const resolution: ForecastResolution = …` narrows to the literals actually assigned, so removing
`'void'` from the expression makes the later `resolution === 'void'` a type error. The resolution
cannot lose a member without the tally noticing. The compile guard reported it rather than counting
it as a kill.

A survivor is a question, not a finding. Here the answer was that the mutation was wrong — worth
recording, because the reflex is to read a survivor as a hole in the tests.
