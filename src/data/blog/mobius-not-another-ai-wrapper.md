---
title: "MØBIUS — I Don't Want Another AI Wrapper"
description: "I set out to build myself a better coding-agent harness. Every feature I wanted turned out to be a question about the runtime rather than the model, and somewhere in there the harness stopped being the means and became the thing."
pubDatetime: 2026-08-28T12:00:00Z
tags: ["MØBIUS", "Agents", "AI"]
category: "research"
cover: "/mobius-card.svg"
---

The starting point was not ambitious. I use coding agents all day, and I wanted mine to be better at a specific set of things: plan a task instead of improvising it, decide for itself when to fan out into subagents and when not to, retry intelligently after a failure, be able to back up to a known-good point, keep a record of why it did what it did, and load skills without me pasting them in.

That's a feature list. I wrote it down expecting to work through it.

What actually happened is that every item on it dissolved, on contact, into a question that had nothing to do with the model.

### The features were all runtime questions wearing costumes

Take "back up to a known-good point." Fine — checkpoint the run. Checkpoint _what_, though? The conversation is easy. The agent's working state is less easy. And the world it has already changed is not checkpointable at all: it wrote three files and ran a migration, and no amount of rewinding your own memory un-runs a migration. So the real question isn't "add checkpointing," it's _what does this system consider its own state, and what does it merely have opinions about?_

Or take "ask me before doing something dangerous." Trivially, you print a prompt and wait. Except the run is in the middle of something. So: does the run block? If it blocks, its state lives in a paused stack frame, and that state survives a network drop but not a restart — which means your durability claim is false and stays invisibly false until the first crash. Does it stop instead? Then something has to be able to answer it later, and a resumed run has to be able to reconstruct enough of itself to continue, and now you are designing a lifecycle, not adding a confirmation dialog.

Or "run subagents." Which owns the task? Do they share state or send messages? If two of them touch the same file, who finds out? If one is suspended waiting for me, is the parent suspended too?

Every single one went the same way. I kept starting with a feature and arriving at ownership, lifecycle, or state.

At some point I stopped treating that as an obstacle. The questions I kept falling into were more interesting than the features I'd been trying to build:

- What owns a task, and what owns a session?
- What is a session's lifecycle — who opens it, who is allowed to close it, and what happens to it when the process dies?
- Where does state actually live, and which parts of it are recoverable?
- What belongs to the host, what belongs to the runtime, what belongs to the protocol?
- How does an approval interrupt execution without destroying it?
- How do you observe _why_ an agent did something, months later, from a record rather than from a memory?

None of that is model capability. All of it is the machinery the model sits inside. The shorthand I use for myself is that a model plus a harness is what people are actually calling an agent — and almost all of the engineering difficulty is on the harness side of that plus sign.

MØBIUS is what happened when I let the harness be the project.

### It is emphatically not a rewrite

I want to be careful here, because "I built my own agent runtime" reads like _I decided the existing tools were bad_. That's not what happened and it would be a stupid thing to decide.

The method is closer to archaeology. There's a directory of reference systems checked out read-only in the repo — Codex and several pinned builds of it, browser-use, a phone-control harness, a terminal multiplexer, aider, mini-swe-agent, another vendor's harness. They are not forks and not dependencies. They are things I read.

The notes have a discipline attached that I'm glad I imposed early: nothing is cited that wasn't opened, nothing is described as measured that wasn't measured, and every note ends in a table with a column headed _compose vs rewrite_ — because the useful question about someone else's excellent code is not "is this good," it's "is this **implementation** reusable, or only the idea." Sometimes the answer is take it. Sometimes it's _rewrite, but copy the shape_. Once it was: this layer is clean except for exactly one import line, and here is the line.

The clearest instance of the discipline paying off is the terminal. Codex has a genuinely good one — the rendering, the diff presentation, the scrollback, the slash commands, the packaging. Rebuilding that would cost months and buy nothing, because my claim isn't about renderers. So it's adopted, and the decision record spends far more words on what is _not_ adopted: not its agent loop, not its session store, not its approval policy, not its model providers, not its state model. The shell renders; it never decides.

That distinction is the whole posture. Take the mature thing where the mature thing is genuinely the answer. Be extremely specific about where it stops.

### Connecting a model to the world is the actual hard part

<a class="fig-plate" href="/research/mobius-a01-system-context.png">
  <img src="/research/mobius-a01-system-context.png" alt="System context: a human gives intent and authority to a client which is an interaction surface and never runtime truth; the client passes turns to the MØBIUS runtime, which owns goal, cognition, authority, effects and journal. Model providers return proposals that are advisory rather than authoritative; tool and effect ports dispatch compiled effects to the external world and return observations and receipts; the durable journal holds authoritative event history." loading="lazy" />
</a>

<p class="fig-note">Who owns intent, who owns semantics, who touches reality. The model proposes and the runtime decides — that boundary is the whole argument of this post, drawn.</p>


The other half of this is tools, and tools drag the same problems in through a different door.

I've spent time on browser control, on driving a phone, on multiplexed terminal sessions. From a feature standpoint these look like a checklist — support the browser, support the device, support the shell. Read three harnesses that do them and the checklist stops being interesting, because they all solve the surface and none of them solve what happens underneath it.

The real question is not how many tools a runtime supports. It's how a runtime lets a model touch the world without lying about what happened. Which needs permissions, and approval, and observability, and failure recovery, and state that stays consistent when an action half-succeeded. One of the reference systems I read handles this with a refusal I keep thinking about: on a platform where it can't do a gesture properly, it simply doesn't expose it, rather than faking it convincingly. That is a runtime being honest about its own reach, and it's rarer than it should be.

The gap I found across everything I read — and I went looking for a reason not to do this — is that none of them can check their own work. There's no plane in any of them that asks _did that action actually do what the model claims it did._ That is simultaneously the largest hole in the field and the clearest reason for this project to exist.

### Why I'm still on it

I've built a lot of things. Most of them had a shape: figure out the problem, ship it, feel briefly good, move on. Finishing was the point.

This one doesn't do that. Every problem I close opens one underneath it, and the one underneath is consistently more fundamental than the one I started with. Checkpointing led to state ownership. State ownership led to session lifecycle. Session lifecycle led to a question about what a host even is, and that one turned out to have a wrong answer sitting in my own planning documents for three versions running — but that's the next post.

For the first time I have something that doesn't feel finishable, and instead of that being discouraging, it's the reason I keep opening it. It's still a research repository — nothing to install, nothing public to link to. That's fine. It isn't a product yet, and pretending otherwise would be the exact thing I'm trying not to build.

---

_Written 2026-08-28, when there was nothing to link to. There is now: the running log of what
this became lives at [**/mobius**](/mobius) — twelve versions of a daemon that causes real
effects, asks before each one, and can be told to stop._
