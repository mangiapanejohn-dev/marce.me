---
title: "🧠 I Built Myself a Second Brain — A Personal Knowledge OS That an AI Agent Keeps Alive"
description: "Dev diary about Marc Brain, a personal knowledge operating system: an Obsidian vault of everything I've built and decided, maintained by Claude Code agents under strict guardrails — fact sync pipelines, confidence labels, git-reviewed self-evolution, the works."
pubDatetime: 2026-07-06T12:00:00Z
tags: ["Dev Diary", "AI", "Knowledge"]
cover: "/brain-mindmap.png"
---

Yoo fellow coders and fellow humans who forget their own projects! Marc here 😜

Big one today. Yesterday I finished the first full build of something I've wanted for years: **Marc Brain** — a personal knowledge operating system. Not a notes app. Not a wiki I'll abandon in three weeks. A living system that *an AI agent maintains for me*, under rules strict enough that I actually trust what's in it.

The itch is embarrassing but real: I ship a lot of stuff (this blog is the evidence), and I kept catching myself unable to answer basic questions about my own life. *When did I pivot TabWorld? Why did I shelve that architecture? What did I decide about that naming mess?* The answers were scattered across git logs, half-dead folders, chat histories, and my extremely unreliable wetware. Every AI assistant I use starts from zero about me. So: classic Marc move. Nobody built my brain, so I built my brain.

<img src="/brain-mindmap.png" alt="Marc Brain full map — fact system, self system, guardrails, git workflow, backup" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

### What it actually is

At the core it's an Obsidian vault — projects, people, decisions, concepts, timelines, all bidirectionally linked. But the interesting part is that **I'm not the one who writes most of it**. A set of Claude Code skills does: one command does a deep sync that crawls my local repos, GitHub, and this blog, then creates or updates pages; another lets any agent *query* the brain before answering questions about me; another captures what we just learned after finishing a task. Every page carries frontmatter with its type, status, **confidence level**, sensitivity, and sources — so six months from now I know not just *what* the brain believes, but *why* and *how sure* it is.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/brain-architecture.png" alt="Marc Brain system architecture — command layer, fact pipeline, vaults, guardrails" style="width: 100%; max-width: 420px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p style="font-weight: bold; margin-bottom: 0.5rem;">The architecture, roughly:</p>
    <p>A command layer (sync, capture, query, self-interview) feeds two pipelines — a <strong>fact pipeline</strong> that turns external sources into vault pages, and a <strong>self-evolution pipeline</strong> that interviews me about values and beliefs. Both write through a shared wall of guardrails before anything lands in the vaults. Everything is git-committed and backed up to a private mirror.</p>
  </div>
</div>

### The part I'm proudest of: the guardrails

An AI writing your biography unsupervised is a horror movie premise. So the write path is paranoid by design:

- **Sources are read-only.** The agent never touches my actual files or repos — it only writes pointers and interpretations into the vault.
- **No making stuff up.** If something can't be verified, it gets labeled `inferred` or `disputed` instead of being stated as fact. When the agent later read the *actual source code* of one of my projects and found the docs had oversold a feature, it didn't silently rewrite history — it recorded the correction, with evidence.
- **Contradictions are preserved, not smoothed over.** Conflicting facts sit side by side in an inbox until *I* rule on them.
- **Private stays private.** Sensitive pages are tagged and never leave the machine; secrets are recorded as "where it lives", never the value.

### And my favorite flex: the brain has version control on *me*

The self-model side runs a periodic interview — the agent reads everything new in the vault, generates pointed questions, and classifies my answers into stable beliefs, temporary moods, experimental thoughts, and abandoned beliefs. Then it does the full git ceremony: snapshot, diff against my previous self, human review, merge. **I literally review pull requests against my own personality.** Approved changes merge to main; the rejected ones stay on a branch, because even my discarded selves get history.

<img src="/brain-state-machine.png" alt="Command state machine — fact sync and self-evolution flows from idle to backup" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

Obligatory dev blooper: during the first full build, the sync agent dutifully catalogued an hour of my old test conversations about bubble-tea preferences (long story, see the Resonix post) and proposed them as a "stable belief". My second brain's first strongly-held opinion was almost *oat milk, no boba* 😂. The confidence system caught it. The system works.

Real talk: the unlock isn't the vault, it's the trust. Because every claim has sources and confidence attached, I can point any AI agent at this thing and it instantly knows me — my projects, my decisions, my history — without me re-explaining my life in every session. It's the memory layer I always wanted my agents to have, except now *I* own it, in plain markdown, on my disk.

The repo is private for now — it is, quite literally, my entire life in markdown 😅 — but I'm cleaning up the system itself (the skills, the sync playbook, the guardrail rules, the vault skeleton) into an open-sourceable template. If that's something you'd want for your own brain, star-watch the repo or yell at me on X to ship it faster.

**The brain lives here:** **[https://github.com/mangiapanejohn-dev/Marc-Brain-2](https://github.com/mangiapanejohn-dev/Marc-Brain-2)** — one skull is not enough storage.
