---
title: "Presence Is Not Truth"
description: "Four ways a check about your own codebase can pass while the thing it checks is false — all four found in one afternoon, all four by a test going red somewhere else."
pubDatetime: 2026-09-06T21:45:00Z
tags: ["Verification", "Testing", "Research", "MØBIUS"]
category: "research"
series: "MØBIUS"
---

If you have ever written a script that checks something about your own codebase — a linter, a census
of unused exports, a test that a doc is not stale — you have probably written this bug and not found
out.

The shape: **you assert that a name appears, and treat that as evidence the thing is true.** It
usually is, right up until the moment it matters.

I hit it four times in one afternoon, in four different disguises. Each was found by a *different*
test going red, never by reading. That is the part worth telling.

### One — the report counted itself

I had a census that found capability fields nothing reads. It found two, and I wrote a small
renderer to disclose them, in the shape the runtime already used elsewhere: *these fields are read,
these are advisory and the runtime reads nothing.*

The renderer took the manifests and totalled the declarations it was reporting on — how many
capabilities declare a prerequisite, how many declare a predicate. Reasonable. Also a read.

The census immediately found readers for the two fields the report calls unread, and the pin went
red.

There is no exemption available. A detector that could tell *reading to report* from *reading to
decide* would have to see intent, and the entire value of a census is that it cannot. The renderer
now takes no argument and counts nothing; the detector carries the counts.

> **A report that measures what it describes becomes part of what it describes.**

### Two — the disclosure named what it disclosed

Later, a different census: exports nothing calls. It found a report renderer with no caller, and I
added a status line to the source so a reader would know:

> *"...so neither this nor `renderAuthorityReport` is reached from anything that can be started."*

That census counts any line mentioning an identifier as a use. So the sentence saying the function
is uncalled **made it look called**, by the sentence saying it is not.

Fixed at the source rather than with an exclusion — the docstring now refers to the renderer without
spelling it, and says why. Adding an exemption for a *production* file would have pushed that
mechanism out of test fixtures and into the code, which is a much worse precedent than the problem.

Same rule as the first, one level out and cheaper to hit:

> **Prose written to disclose that nothing uses a symbol is itself a use of it.**

### Three — the marker was asserted present, and was false

That status line got a test: *the provider's source contains `STATUS: not loadable by the daemon`.*

Weeks of work later, I wired that provider into the daemon. The sentence became **false**. The test
still passed, because the words were still there.

This is the one that actually scares me, because it is the most ordinary. A test that pins
documentation almost always pins its *presence*. Presence survives the documentation becoming a lie.

It now checks the marker against the measurement it describes — a reachability walk from the binary's
entry point — so a provider whose stated status stops matching what the binary can reach turns the
test red instead of going quietly stale.

### Four — the invariant asserted an identifier, not a mechanism

Last one, and I had just written the other three up.

A design decision said: *do not delete this session binding; widen what it binds to.* To make the
prohibition checkable I asserted that the private field `#boundSessionId` appears in the file.

A mutation replaced the single line that reads it with `undefined`. The refusal stopped happening.
The test stayed green — the identifier occurs three times in that file, and I had pinned the name,
not the use.

Fixed by pinning the **read site**, and by putting an existing behavioural test into the same
battery, so the invariant is guarded by behaviour and the text check only makes a deletion visible.

### What they have in common

All four are the same substitution: **a syntactic witness standing in for a semantic claim.** The
name is there, so the thing must be true. It is cheap to write, it passes on the day you write it,
and it decays silently.

Three rules I now use:

1. **Pin the read site, not the identifier.** `const bound = this.#boundSessionId` is a use.
   `#boundSessionId` is a spelling.
2. **A doc-pin must check the doc against the measurement it describes**, not against its own
   existence. If a status line claims something a test can measure, measure it.
3. **A checker must not be able to satisfy itself.** If your census reads source, its own source is
   part of what it reads — and so is every list, table and sentence you write *about* the thing it
   counts.

### The part I did not expect

Not one of these was found by reading. Every one was found by a *different* test going red — a
census tripping over a renderer, a suite tripping over a docstring, a wiring change tripping over a
marker, a mutation tripping over an invariant.

Which is an argument for a specific habit rather than for care: **write the check that would catch
you, then change the thing and see if it catches you.** The fourth one came from deliberately
breaking the mechanism to watch the invariant fail — and it did not fail. That is the only reason I
know about it.
