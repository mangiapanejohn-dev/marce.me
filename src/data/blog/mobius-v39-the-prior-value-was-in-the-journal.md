---
title: "MØBIUS V39 — The Prior Value Was in the Journal the Whole Time"
description: "The verification plane escalates to a fresh observation because a `changed` assertion has no prior value to compare against. Then the observation cannot decide it either. Measured with a perfect look — and the missing input had been accepted, unsupplied, since the plane was written."
pubDatetime: 2026-09-05T18:45:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

`changed` is the one assertion operator that no observation of post-action state can settle. The
verification plane knows this: when the provider's own returned result leaves the assertion
undecidable, it escalates and goes to look.

Then the look cannot settle it either.

### The measurement

Two probes on a two-action run. The first showed the escalated observation was a directory listing
while the assertion named `content` — but that was the *fixture's* observation port throwing away the
gap the loop builds, not the runtime. Recorded so it would not be mistaken for the finding.

The second pointed the port at the exact file, so `content` was unambiguously present in the observed
state:

```
verdict a1  undetermined  basis=fresh-observation
  undecidable  "changed" needs a pre-action value for "content"; none was recorded
verdict a2  undetermined  basis=fresh-observation
  undecidable  "changed" needs a pre-action value for "content"; none was recorded
```

**A perfect observation does not move the verdict.** The plane escalates *because* the result cannot
decide; it takes a look that cannot decide either; it returns `undetermined`; the loop diagnoses
`InsufficientEvidence` and runs a recovery cycle. Per action. For a question no amount of looking at
post-action state can answer.

### Both halves were already there

`VerificationInput.baseline` — documented as *"Pre-action state, for `changed` assertions"* — is
threaded through the planner into `ComparisonContext` and read by the comparator, which uses it and
falls back to `undecidable` rather than to `unchanged`:

> Without a recorded prior value it is undecidable — never "unchanged", which would be a fabricated
> negative.

`grep` for `baseline` across `runtime-core` returns nothing. **Nothing had ever supplied one.**

And since V21-2 the compiler stamps `ActionIR.basis`, naming an observation the loop still holds —
taken before the action, which is what pre-action state means. V38 had just measured that it is
populated for every action after the first.

V39 joins them, at one call site.

### Why an advisory basis is good enough evidence

`basis.freshness` is `advisory`, and it is fair to ask whether a possibly-stale observation should
decide a verdict. The comparator already answers it: with no baseline it falls back to
`assertion.value` — **the proposer's own account of the prior value** — and decides on that.

An observation the runtime took itself is strictly better evidence than the claim of the party being
graded. This version raises the standard of evidence; it does not lower it.

What `changed` asserts is *the value differs from the recorded prior value*. It has never asserted
attribution, and this does not make it. Whether the difference is **this action's doing** is V38's
question, and the premise-movement signal already answers it. The two stay separate.

### What it buys

| case | before | after |
|---|---|---|
| basis covers the asserted path, content differs | `undecidable` → recovery cycle | `satisfied`, verdict `verified` |
| same, content **identical** | `undecidable` | `violated` |
| basis is a directory listing, assertion names `content` | `undecidable` | `undecidable`, unchanged |
| first action of a run — no basis | `undecidable` | `undecidable`, unchanged |

The second row is the one worth pausing on. **The runtime can now say "the thing you promised to
change did not change"** — a sentence it could not previously form at all.

The third and fourth rows are the honest boundary: a baseline that does not reach the asserted path
is not a prior value, and reading it as *unchanged* would be the fabricated negative the comparator
refuses by construction. It would also turn every unobserved field into a violated prediction.

### Two things the version caught about its own method

**A green suite that did not compile.** `typecheck` was run after the source change and before the
test file existed; vitest then went green on four tests. The battery's compile guard opened with

```
(tree already has 2 type error(s); only new ones count)
```

Two `TS2339`s in the new test file — `reason` exists only on the `undecidable` arm of a union, and
`?.reason` on the union does not compile. vitest transpiles without checking types, so nothing in the
test run could have said so. This is a lesson V35 wrote down four versions earlier, committed here by
the same discipline that wrote it: the check was run, then invalidated by the next edit, and the green
that followed was read as covering both.

**A pre-registered mutation that cannot be built.** One of the five — *fall back to the most recent
observation when the basis names none* — is behaviourally identical to the real code under this loop.
`#groundingFor` returns the most recent observation in the session, so the basis *is* the newest one
at dispatch; and nothing observes between a dispatch and its verification, so "by id" and "by
recency" name the same envelope. No fixture can separate them.

Left standing in the plan rather than quietly rewritten, and replaced in the battery by one that asks
a live question: *which part of an observation is the pre-action state?*

### What is left

The recovery cycle is now avoidable, and still not avoided. A `changed` assertion is decidable
whenever the runtime looked before acting — and nothing makes the runtime look before acting on
purpose. It does so only when a previous action's verification happened to.

That is the same open question three versions have now arrived at from three directions, and it is a
question about when the loop observes, not about the verification plane.
