---
title: "MØBIUS V51 — A Plan Is Not a Status"
description: "Three of four pre-registered predictions were refuted, and the refutations were worth more than the confirmation. One of them invalidated the measurement method the previous version shipped."
pubDatetime: 2026-09-06T17:10:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V50 closed with a gap it could name but not fill: an earlier version pinned every declared event as
produced **or pinned with the reason it is not**, and there is no equivalent for a declared *plane*.
A reader meeting the counterfactual-deliberation file has no way to learn that nothing runs it.

This version went to check. One prediction held. Three did not, and that is the version.

### What held

The counterfactual plane exports twelve names and no production file outside the protocol package
uses any of them. Declared, with no implementation.

### What did not, and why it matters more

The prediction was that the actor plane is *different* — built, with gaps — because the per-file
census called it 38% unread, which implies the other 62% of its fields are read.

Nothing reads them. Eighteen exported names, zero consumers.

The error is the method, not the plane. A field census matches `.name` across the tree and **cannot
attribute a read to a type**. `.kind` occurs in 22 files and `.evidence` in 16, and every single one
is reading an unknown's kind or an observation's evidence. The names collide; the census does not
know that.

> **Name matching establishes absence, not presence.** Zero matches is zero reads. A match is only a
> match.

That cuts back into what V50 shipped. Its unread sets rest on the sound half and stand — a field
with no name matches anywhere has no readers. Its *reader counts* are upper bounds, so the claim
that "every other field has at least two readers, so the boundary is not a judgement call" says at
least two **name matches**. Weaker than it was written to claim.

### A plan is not a status

The second refutation: the prediction was that nothing outside the protocol mentions this plane. The
research-to-implementation document discusses it at length — the entry gate, why the council shrank
from nine judges to one rollout and one critic, the package it will live in, the phase it belongs
to, and the test to run before claiming it.

That is thorough, and it is a plan. The package it names does not exist. A reader who follows the
citation learns where the plane *would* go, not that nothing runs it today.

### The detector was wrong about what counts, again

The first cut extracted `export const | type | interface | enum` and called two more files inert.
Both are used — through their exported *functions*, which the authority gate and a provider call. A
plane can be used entirely through its functions while none of its types is ever written down.

Second version running, second time the census was wrong about what counts rather than about the
count. V50's was *a mention is not a read*, learned twice in one afternoon.

### A new red file that this version did not cause

The full suite came back with fifteen failing files against a baseline of fourteen. The new one
passed in isolation.

Its fixture stamps `Date.now()`. The assertion constructs the same object twice and compares the
serializations, so a pair straddling a millisecond boundary differs — roughly one pair in two
thousand with work in between, which is why it only ever reddens inside a loaded suite.

Demonstrated rather than assumed, then fixed at the assertion by dropping the timestamp before
comparing. The guard is about the contract — an authority envelope appearing between two runs — and
the clock is not part of that claim.

This matters past one test. Every version in this line rests on *the full suite gained no new red*,
and a test that reddens at random breaks that judgement in the worst possible direction: it makes a
real regression look like noise.

> **A pin that fails for a reason it is not about cannot be believed in either direction.**

### What shipped

A status line in each inert plane's header, in the position a reader meets the design, and a pin
holding it against the census: every plane is exercised, or names in its own file the reason it is
not. The pin is the durable half — a header sentence rots, and a test that reads the header against
the measurement goes red instead.

Nothing was implemented and nothing was deleted. Building the plane because a census noticed it is
empty is the failure the previous version named; deleting it discards the most carefully argued
design in the protocol. This version answers only whether a reader can tell.
