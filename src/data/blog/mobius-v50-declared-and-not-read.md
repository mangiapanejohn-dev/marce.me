---
title: "MØBIUS V50 — Declared and Not Read"
description: "Two versions found machinery whose cost is paid every time and whose value is never collected. Two is a coincidence. This builds the instrument that counts — and the first thing it caught was the report written to disclose the problem."
pubDatetime: 2026-09-06T15:45:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V49 closed by naming a shape it had seen twice and could not count: `contradiction.detected`, folded
by two projectors and emitted by nothing; a movement report computed on every `repo.status` and read
by nothing. **Two is a coincidence.**

This repository has two instruments of that family. One detects exports nothing reads, one detects
events nothing produces, and the first of them stated the rule both rest on:

> **A count is checkable; a cleanup is not.** After a deletion nothing stops the next one
> accumulating.

Neither was ever pointed at protocol fields. This is that bill.

### Seventeen fields, two with no reader

`CapabilityManifest` is what every provider authors, once per capability, today. Counting readers
across production TypeScript — excluding the schema that declares the fields and the
`capabilities.ts` files that write them:

| field | readers | | field | readers |
|---|---|---|---|---|
| `capabilityId` | 34 | | `stateBearing` | 7 |
| `providerId` | 24 | | `environmentKind` | 6 |
| `description` | 17 | | `reversible` | 6 |
| `effectClass` | 14 | | `semantics` | 5 |
| `schemaHash` | 5 | | `semanticEffect` | 3 |
| `observes` | 3 | | `concurrency` | 2 |
| `expectedLatencyClass` | 2 | | `idempotent` | 2 |
| `constraints` | 2 | | | |
| **`prerequisites`** | **0** | | **`stateful`** | **0** |

`prerequisites` is authored at 34 sites across four providers. Every field outside that pair has at
least two readers — none has exactly one — so *read* and *unread* is not a matter of degree here.

### The half the type exists for

`constraints` has two readers and they are the same read. The only consumer of a manifest's
constraints takes `.id` into a display string. So `description` is never read, and `predicate` —
authored 23 times — is never read either. Its own docstring:

> A precondition the capability cannot honour outside. **Duck-typed discovery cannot express these,
> which is exactly why they are here.**

The schema states its own necessity, providers wrote to it, and the machine-readable predicate has
never been machine-read. Routing does not consult it: the matcher touches `providerId`, `semantics`
and `effectClass`, and nothing else.

### The report falsified itself

The runtime already had the honest report — for the other plane. A goal's constraints can be asked
which of them bind; the answer prints `enforced` beside `advisory — prose; the runtime checks
nothing`, and exists so *"which of my constraints are actually enforced?"* does not require reading
the source. A capability's constraints had no such answer, so a provider author writing
`prerequisites` on eleven capabilities had no way to learn it binds nothing.

So this version ships the capability-side twin. The first cut of it took the manifests and totalled
the declarations it was reporting on — and `m.prerequisites.length` is a read. The census
immediately found readers for the two fields the report calls unread, and the pin went red.

There is no exemption available. A detector that could tell *reading to report* from *reading to
decide* would have to see intent, and the entire value of a census is that it cannot.

> **A report that measures what it describes becomes part of what it describes.**

The renderer now takes no argument and counts nothing. The detector carries the counts.

### A mention is not a read

The same class of error appeared twice more, both found by the test going red rather than by
foresight. The renderer's docstring quotes `m.prerequisites`. The renderer's *output* contains the
string `constraints[].predicate`. Both matched as reads.

Comments are stripped, then string literals — but the index form is tested *before* strings are
removed, because `obj['predicate']` is a real read that lives inside one.

The difficulty of a census is never the counting. It is settling what counts, and each of these was
settled by being wrong first.

### The number that did not ship

The wide census is real: **52 of 259** protocol schema fields have no reader anywhere. It is not
what shipped, and the reason is worth more than the number. Measured per file the distribution is
bimodal — `worldline.ts` is 79% unread while eight protocol files are 0% — so a single average
describes neither group.

`worldline.ts` is not a built plane with gaps. It is a declared plane with no implementation, and
its header, which is long and careful and cites the research it came from, does not say so. Neither
does the actor plane's. Neither does anything in the architecture docs.

The rule for events was that every declared one is produced **or pinned with the reason it is not**.
There is no equivalent for a declared plane, and a reader meeting that file has no way to learn that
nothing runs it.
