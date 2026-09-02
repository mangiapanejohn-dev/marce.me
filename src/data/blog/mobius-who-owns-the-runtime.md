---
title: "MØBIUS — Who Actually Owns the Runtime?"
description: "Three of my planning documents deferred a load-bearing architectural decision to a section of a document that does not exist. Finding that out took a week of session-lifecycle bugs, and it changed what I think architecture work actually is."
pubDatetime: 2026-08-29T12:00:00Z
tags: ["MØBIUS", "Agents", "Building"]
cover: "/cover-section-58.svg"
---

For three consecutive versions, my planning documents said some version of the same thing: host ownership belongs to `mobius-cli`, so this repository must not own runtime or host assembly. Each one cited the same authority — _§58 of the governing prompt_.

I eventually went looking for §58.

There is no §58. No document in the repository contains that section. It was a paraphrase someone — me — made while planning, which got copied into the next plan as context, and into the one after that as a constraint, and by the third one it was being cited the way you cite a decision record. Nobody ever went back and checked, because it had the grammatical shape of a thing that had already been decided.

That's the post. But the way I got there matters more than the finding, because I did not get there by auditing my documents. I got there by having a week of bugs that made no sense until I admitted I couldn't say who owned anything.

### The week that forced the question

MØBIUS is a runtime for agents, which means the objects it manages are sessions: a connection to a filesystem, a shell, a repository, a browser. Six slices of work landed in one morning, and each one found the same class of defect from a different angle.

**A capability was declared and never chosen.** Session ownership was modelled as `launch` or `attach` — either the runtime started this thing, or it connected to something already running. Reasonable model. Then I checked the call sites, and every single one on the kernel side passed `launch`. The distinction existed in the type and nowhere in the behaviour. The measurable consequence: open a session as `attach`, ask to close it with `terminate`, and it closes. **The runtime could destroy a session it had never created.**

**Attaching never attached.** Call adopt twice on the same surface and you got `fs-session-1` and `fs-session-2` — two live sessions against one thing. Attach wasn't joining anything. It opened a new session and labelled it attached, which is the worst possible failure mode, because everything downstream then behaves as though a shared object is shared.

**The set had an add and no remove.** Adopting a session wrote into the coordinator's held-session set. Nothing ever took anything out of it.

**The teardown path had no callers.** `shutdown()` and `exit()` existed, were correct as far as I could tell, and were invoked by nothing. Not in production — there was no production. And not in tests either, because the test fixture's cleanup deleted two temporary directories and never closed the client, so no test had ever needed a drain to exist in order to pass.

That last one is the one that unsettled me. A whole lifecycle can be sitting in your repository, fully written, reviewed, typed, and be load-bearing for nothing at all.

There was also a mutation that survived — a test that should have failed when I broke the code and didn't. It survived because every fixture in the repository had exactly one provider. When I strengthened it, it exposed that surface lookup was doing `find` over a list, which silently resolves to whichever provider booted first; two providers both advertising a `workspace` surface returned the same session. My tests had been agreeing with me because my fixtures were too simple to disagree.

### The common shape

None of those were the same bug. They shared a shape, though, and the shape was that no component could say what it owned.

The coordinator held sessions but had no theory of when it stopped holding them. Boot produced a capability graph and a schema loader and — I checked — was called by nothing outside its own tests. The runtime could be assembled from several places, each slightly differently, which is a nice way of saying the system had several realities and no way to tell which one was running.

Boot, to its credit, said so in its own comments: adopting is a decision with an owner, and boot is not the owner. It knew. It just had nowhere to point.

Both of the tracks I was working on reached the same conclusion within a couple of hours of each other, independently: the reason nothing could say what it owned was that the document defining ownership didn't exist.

### The re-read

So I went back to the two decision records that actually exist and read them as written rather than as remembered.

The first one draws a wall between the core packages and anything host-shaped. I had been carrying it as _this repository cannot own host assembly_. What it actually says is that `protocol`, `cognition` and `state` take **zero host imports**, enforced by a CI gate from the first commit. That is a directional constraint on dependencies: host types must not leak downward into the core. It has nothing to say about whether host-facing code may live here. And the giveaway, which I had read past several times, is that the ADR itself names a host package as belonging in this repository. It just hadn't been written yet.

The second one is even more direct. It records adopting Codex's terminal as a shell and nothing else, and it decides, explicitly and with a date on it, that `mobiusd` implements the Codex app-server v2 wire protocol — and `mobiusd` is mine, and `mobiusd` is TypeScript.

So the inherited rule wasn't merely unsourced. It contradicted the two decisions that _were_ sourced.

The correction is short:

- `mobius-cli` is the Rust TUI and client. It renders and it connects; it does not decide.
- `mobiusd` is the TypeScript host implementing the app-server wire protocol, and it belongs in this repository.
- The Codex thread and turn types are a **host wire shape**, never canonical state. That distinction is what keeps the wall intact while letting the host live here.
- Prior "§58" references are not authority.

And the correction was written as a new section rather than by editing the old plans. The older documents are left exactly as they were. I'd rather the record show that I believed a wrong thing for three versions than have it quietly show that I never did.

### Then the assembly question answered itself

With ownership settled there was an obvious follow-up: fine, who assembles a runtime today?

Nothing did. No production path took a boot report and an explicitly adopted session and produced a runtime. The schema loader reached a compiler in exactly one place. Every construction of the cognitive loop in the entire repository was underneath `tests/`.

**Tests owned the assembly.** The only thing that knew how to build the system was the thing whose job was to check it — which is why the system had multiple realities, and why nothing could name an owner, and why a whole teardown path could exist with no callers. There was no composition root. There was a test suite doing an impression of one.

### What I actually took from this

I used to think architecture was the diagram — the boxes, the layers, the rule about what may import what. Produce a good one, follow it, and you have an architecture.

I now think architecture is the part that can be **checked**. A rule is only architecture if you can point at the thing that enforces it: a CI gate, a dependency graph, a test that goes red, a decision record with a date on it, an observable runtime behaviour. Everything else is a habit that everyone in the room happens to share, and habits propagate through documents beautifully and are invisible to review, because reviewing a plan means checking that it's consistent with the previous plan.

The practical version, which I now do:

**When a plan cites a rule, open the rule.** Not the plan that cites it. The rule. If you cannot find the document, the rule does not exist, no matter how many places repeat it.

The one that stings is that all three plans citing §58 passed review. They were internally consistent, they agreed with each other, and they were confidently wrong in unison. Consistency is not evidence. It's just consistency.
