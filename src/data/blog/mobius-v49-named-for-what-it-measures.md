---
title: "MØBIUS V49 — Named for What It Measures"
description: "V48's measurement was pointed at the runtime and found the provider that produced it. A field called worktreeChanged, built on a token that cannot see a second edit, reporting false while the working tree changed — and nothing has ever read it."
pubDatetime: 2026-09-06T14:20:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V48 measured three witnesses over one working tree and found their blind spots disjoint. The first
thing that measurement got pointed at was not the runtime. It was the provider that produced it.

### A report that is careful about one misreading

`RepoSession.compareWithPrevious` keeps the last snapshot so the next one can be told whether the
ground moved between them. Its header is explicit about what that is not:

> not a guard, not an invalidation […] A consumer that mistook this for change detection would
> believe an unchanged report meant the repository was quiet, when it only means nobody asked in
> between.

That defends against one misreading. V48's table says there is a second one underneath it.

### The marker carries the status token

```ts
export interface SnapshotMarker {
  readonly observationId: string
  readonly commit: string | null
  readonly changeSetDigest: string
}
```

`changeSetDigest` is over *which paths are in which state*. V48's third row: a second edit of an
already-modified file moves `diffDigest` and leaves `changeSetDigest` alone, because the path was
`modified` before the write and is `modified` after it.

So across two `repo.status` observations spanning a real content change, the flag built on that
token reads `false`. Its docstring — *"the set of pending changes differs from the previous
observation's"* — was accurate the whole time. Its **name** was `worktreeChanged`, and the working
tree had changed. Every consumer reads the name.

`headMoved` has no equivalent gap: `commit` is a full identity, not a summary. One field, not the
mechanism.

### The distinction is carried, not missing

`diffDigest` sits on the same `RepositoryState` the marker is built from. Whatever the case for
putting it in the marker, *we would have to ask git again* is not an argument against it. That
separates a measurement not taken from a measurement not carried, and this is the second kind.

### What shipped, and what did not

Shipped: the rename, `worktreeChanged` → `changeSetChanged`, with the blind spot written into the
field's own docstring rather than left in a plan nobody reads at the call site.

**Not** shipped: a `contentChanged` flag from `diffDigest`. It is one line, the data is already
there, and V48 proved it would work — which is the entire argument for it. Nothing reads this
report at all. Adding a second field to a report with no readers is inventing cognition by
opportunity; ADR 0007 refuses that, and V47 refused the same thing three versions ago on the belief
plane for the same reason.

> **A measurement that would work is not a reason to take it. A reader that needs it is.**

### The battery attacks the comparison, not the name

A rename cannot be mutated into something a test would catch, so the four mutations went after what
the renamed field reports. All died. The one worth naming: making the first observation fabricate an
unchanged comparison instead of returning `null` kills two tests. `null` means *nobody measured*,
and a `false` in its place is a claim nobody made — which is precisely the honesty the header
claimed for itself, now checked rather than asserted.

Four predictions confirmed, `4 mutations · 0 survived · 0 unreported`, full suite
`176 files · 1517 passed | 36 failed` — the known red files, none new.

### Two of a shape

V47 found `contradiction.detected`: folded by two projectors, weighted highest of any kind, routed
above every unknown, and emitted by nothing. V49 found a movement report computed on every
`repo.status` and read by nothing. Two planes, one shape — **machinery whose cost is paid every time
and whose value is never collected.**

Two is a coincidence. The instrument that would tell the difference does not exist: an earlier
version built a detector for *exports* nothing reads, another for *events* nothing produces, and
neither was ever pointed at protocol fields.
