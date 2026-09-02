---
title: "QuotaLens — The Small Tool That Refused to Stay Small"
description: "The smallest thing I've built is still the most used thing I've built, and it hasn't needed a commit in two months. A note on my habit of turning every annoyance into an operating system, and the one time I didn't."
pubDatetime: 2026-09-01T12:00:00Z
tags: ["Open Source", "macOS", "Building"]
cover: "/quotalens-gauge.png"
---

QuotaLens exists because I got annoyed on a Wednesday.

If you spend all day inside Claude Code or Codex you know the failure: you're deep in something, the agent is working, and then you hit a rate limit with no warning at all. There's no gauge. You're either rationing tokens on vibes or walking into a wall mid-task. So I spent a couple of days writing a macOS menu-bar app that puts a ring up there showing exactly how much of the window you've burned. I wrote it up [when it shipped](/posts/quotalens-menu-bar-for-ai-quotas), back in June.

I'm writing about it again because of something that happened after, which is: nothing. And nothing turned out to be the interesting part.

### The scoreboard, such as it is

As of today it has 149 stars and a couple of forks. Those numbers are outside signal and I'm glad of them, but I want to be accurate about what they are, because the version of this post where a teenager tells you his repo took off is not a version I'd trust if I were reading it. Nobody else has contributed code. The only pull request on it is my own. It's a small tool that some strangers found useful enough to bookmark.

The number I actually care about is a different one: the last commit was the seventh of July. Nearly two months, no changes. Not because I abandoned it — I use it every single day, it's open right now — but because it does the thing and the thing is done.

I have never had that before.

### I have a habit and it is not always a good one

I turn problems into systems. I want to be clear that I know this about myself, because it isn't modesty, it's the actual failure mode.

The pattern goes: notice a small annoyance, start fixing it, notice the annoyance is a symptom of something structural, start fixing _that_, and eight steps later I am designing a general solution to a category of problem when what I needed was a gauge in the menu bar. I have shipped genuinely useful things this way. I have also spent weeks building the general case for a problem that occurred exactly once.

MØBIUS is Exhibit A and I'm not even defensive about it. That project started as _I want my coding agent to be a bit better at planning_ and has become a research repository with sixteen packages, a wall of architecture decision records, mutation testing, and a several-thousand-word note about who is allowed to close a session. I think that escalation is correct — the problems underneath really were more fundamental than the feature I started with, and I've written about why. But it is unmistakably the same habit, operating at full power, with nothing stopping it.

QuotaLens is the one time the habit didn't fire. There was a real temptation: a plugin system, a web dashboard, team accounts, historical export, a service. I can still see the whole roadmap. I didn't build any of it, mostly by accident, and the not-building is the reason it's finished.

### What the small one has that the big one doesn't

It's local-first, which means there is no server, which means there is no server to keep alive. It's pure Swift with system frameworks, so there is no dependency tree to rot. It does one thing, so there is no feature interacting badly with another feature. Its scope is small enough that "correct" is a state it can actually reach and stay in.

None of those are clever decisions. They're consequences of the thing being small. But they add up to a property I've started to want more of: **it can be done.** Not abandoned, not stable-for-now — done. It has an end state, and it's in it.

MØBIUS cannot be done. That's not a criticism of it; it's a research project and generating new questions is what it's _for_. But you can't run your whole life on projects that only generate more work, and until recently that's basically all I was building.

### The useful version of the lesson

The temptation is to end with _keep it simple_, which is worthless advice because everyone already agrees with it and nobody can act on it.

Here's the version I can actually act on. Some problems are worth a runtime. Most are worth an afternoon. The skill I don't have yet is telling which is which **before** I've spent three weeks on it, and the closest thing I have to a heuristic is this: ask whether the annoyance is _specific_. "I can't see my quota" is specific — it has an end. "My agent should be better at hard tasks" is not specific, and everything downstream of it is going to be architecture, and I should go in knowing that's the deal I'm making rather than discovering it in week three.

QuotaLens is 149 stars of evidence that a small tool solving one real irritation can matter more than most of what I build. It sits in my menu bar and reminds me of that several times a day, which is more supervision than I get from anywhere else.

**QuotaLens:** [quotalens.fun](https://quotalens.fun) · [source](https://github.com/mangiapanejohn-dev/QuotaLens) — macOS 13+, MIT.
