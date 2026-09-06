---
title: "MØBIUS — What One Binary Can Actually Load"
description: "Five findings turned out to have one cause, the cause turned out to be a boundary, and the boundary turned out to be somewhere other than where my own architecture note put it. A ladder for telling 'the code exists' apart from 'the system does this'."
pubDatetime: 2026-09-06T21:30:00Z
tags: ["MØBIUS", "Agents", "Architecture", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

Over several versions I kept finding the same thing and calling it a coincidence each time: a fact
the runtime records that nothing reads. A contradiction event folded by two projectors and emitted
by nothing. A movement report computed on every repository status and read by nothing. Two capability
fields written at sixty sites and read by nothing. A flag on every write receipt saying whether the
file existed before, read by nothing.

Five is not a coincidence. So I went looking for the cause, and found an interface.

### Two of eighty-four

Across the four environment providers, the object literals that carry "what I just did" have **84
distinct keys**. The extractor that carries those facts into the runtime's own reasoning reads two
of them: `path` and `digest`.

Everything else — whether the file was created or overwritten, its previous digest, how many edits
applied, the byte length, the repository's diff digest — reaches the extractor and is not carried
past it. And the narrowness is deliberate, argued in place:

> A provider that wants its resources traced says `path` and `digest`; that is the entire contract.

with the reason that anything wider is *"a schema nobody agreed to."*

So the five findings are not neglect accumulating. **They are what the discipline produces**, and it
will keep producing them. Both halves are true at once: a wider contract would let a useful fact
reach the rule that could use it, and would also be the invented schema the contract refuses.

That reframing was worth more than any of the five. But it also raised a sharper question. If a
recorded fact can fail to reach a consumer, what else in this tree is present and unreachable?

### Twenty-one percent

The tree ships one binary. Walking module imports transitively from its entry point, over 167
production modules: **132 reachable, 35 not.**

The unreachable set is mostly what you would expect — test doubles, an offline eval harness,
fixtures. Except for the two largest groups, which are **whole environment providers**. Nine modules
and ten modules. Built, tested, refined across versions, and outside anything the binary can reach.

And a fold that six versions had been built on — world drift, identity drift, premises, scoping — had
no caller at all. Nor did four report renderers, three of which name a command in their own
docstrings. That command does not exist. The tree declares one binary and it is a daemon with no
subcommands.

None of this was a defect. The phase document says in its title that this phase is one vertical
slice. The limitation was real, deliberate, and recorded — **in a document, and not at the code a
reader meets.** Which is its own finding, and the same one twice: a plane that is *declared and not
implemented* and a plane that is *implemented and not reachable* are opposite states, and neither
said so where anyone would look.

<figure style="margin: 2.5rem 0;">
  <img src="/runtime-frontier-bench.png" alt="RuntimeFrontierBench — a scatter of runtimes on two axes, verified technical breakthroughs against research frontier depth, with MØBIUS traced from V35 through V56 and a dashed extension to a research target" style="width: 100%; height: auto; display: block; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 0;" loading="lazy" decoding="async" width="1448" height="1086" />
  <figcaption style="margin-top: 0.75rem; font-size: 0.875rem; line-height: 1.6;">
    Where I think this sits — and <strong>conceptual placement, not a measurement</strong>. The axes are my own reading of execution semantics and research direction, and the dashed segment is a target rather than a state.
    <br />
    Every number earlier in this post is measured. None of these are, and that difference is the reason the walk was worth doing.
  </figcaption>
</figure>

### A ladder, because "it works" has seven meanings

The vocabulary I ended up needing:

| rung | test for membership |
|---|---|
| **declared** | a type exists |
| **implemented** | code exists that would do the work |
| **test-exercised** | some test calls it |
| **import-reachable** | in the module graph from the binary's entry |
| **composed** | instantiated at the composition root |
| **adoptable** | can be *the* thing a run binds to |
| **co-composable** | usable *together with another* in one run |

Every rung is a place work can stop and look finished. A green test suite proves rung 3. It says
nothing about rung 5, and the gap between them is where two whole providers were sitting.

The last rung is the one I did not have going in, and it is the one that mattered.

### The wall was not where I put it

I wrote an architecture note listing three walls between the current state and a two-provider run: a
hardcoded composition root (wiring), a singular surface selector (design), and a refusal deep in the
loop that rejects any request against a session the run is not bound to (semantics).

I put the weight on the third. Its reasoning is good — the binding is *"a fact about which world this
run is for, one the assembly settled before the goal was ever seen"* — and arguing with it looked
like the hard part.

Then I measured instead of arguing. Two providers over one working tree, through the real host:

```
filesystem.calls  = ['sessionOpen:workspace', 'sessionClose:release', 'shutdown', 'exit']
repository.calls  = ['shutdown', 'exit']
```

The second provider is registered, drained, and **never spoken to** — not even a handshake. It is
not *refused* a session. It is never offered one.

So the semantic wall was unreachable. There was nothing for a second session to bind to, and an
architecture document that opened by arguing with that refusal would have been arguing with the
wrong file. The real wall was at boot, one layer up and much less interesting — which is exactly why
it needed measuring rather than reasoning about.

### A counter is not a description of the world

The sharpest thing I learned came from the question that blocked everything else.

Each provider keeps a monotonic revision for its session, and an action's freshness is checked
against it. With two providers over one directory, does that become one clock or two?

I expected to find a soundness bug — a basis from one session compared against another's counter.
There is none. Every comparison already resolves the session first, and one gate refuses outright
when it cannot, on the stated ground that *"its revision cannot be compared to anything."* The code
was more careful than my note assumed, and checking is how I found that out rather than the reverse.

The real problem is one level up, and neither provider hid it. Each states its own scope honestly —
the filesystem *"does not watch the tree, so it announces changes it applied itself and nothing
else"*, and the repository's event scope is `none`, *"truthfully"*. What no file said is what those
two honest scopes **compose into**:

> A revision records **what its own provider did**. With one provider that is indistinguishable from
> a description of the world, because the one provider is the only thing acting. With two, a basis
> can be fresh by its own counter and stale in fact.

This generalises past this system. Any layered thing with per-component counters has it: the counter
is a log of local actions wearing the costume of global state, and the disguise only fails when a
second actor appears.

The decision that followed: revisions stay per-component and are **never aggregated**. A maximum or a
sum of two counters that count different things is a number nothing can honour. Cross-provider
freshness became an *identity* question instead — compare what the effect claimed against what a
reading finds — which the drift machinery already answered, and which is where several earlier
findings stopped being curiosities and became inputs.

### What actually shipped

The daemon composes two providers over one working tree now. A declared world: the filesystem as the
anchor, the repository as a **witness** — asked, never anchored on, because anchoring on it would
need the aggregation that was just refused.

The interesting part of the wiring was not the wiring. Outside a checkout the repository provider
advertises no surface, and a world whose witness cannot be adopted fails whole — so a daemon
declaring it unconditionally would refuse to start in a plain directory. The assembly **asks** the
provider rather than re-implementing a git check beside the thing that already answers one.

Three pins went red on that commit: the reachability walk, an assertion about the old composition,
and one saying the two-provider pair was something this runtime could not assemble. All three were
updated with reasons rather than deleted. A pin going red on the change it was written to catch is
the pin working.

One of them had a hole, and the change is what exposed it: it asserted that a status marker was
*present* in the provider's source. After the wiring, that marker's sentence became **false** — and
the test still passed. Presence is not truth, which turns out to be its own subject.
