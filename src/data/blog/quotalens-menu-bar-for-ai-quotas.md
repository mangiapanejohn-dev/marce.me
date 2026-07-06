---
title: "🔭 QuotaLens Blew Up — A Tiny Menu-Bar Gauge for Your Claude & Codex Quotas"
description: "Dev diary about QuotaLens, a local-first macOS menu-bar app that shows exactly how much of your Claude and Codex rate limits you've burned — 5-hour and 7-day rings, token and cost history, zero servers. It somehow became my most-starred project."
pubDatetime: 2026-06-28T12:00:00Z
tags: ["Dev Diary", "macOS", "AI"]
cover: "/quotalens-hero.png"
---

Yoo fellow coders and quota-anxiety sufferers! Marc here 😜

Quick dev diary today, because something unexpected happened: I shipped a tiny menu-bar app three days ago and it's already my most-starred repo. Ever. Meet **QuotaLens**.

<img src="/quotalens-hero.png" alt="QuotaLens landing page — know where every token goes" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

Here's the itch. If you live inside Claude Code or Codex all day like I do, you know the feeling: you're deep in a refactor, the agent is cooking, and then — *"you've hit your 5-hour limit"*. Out of nowhere. No warning, no gauge, nothing. The official tools just don't tell you how close to the cliff you are, so you either ration tokens like it's wartime or you slam into the wall mid-task. Both are terrible. Classic Marc move: nobody made the gauge, so I built the gauge.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/quotalens-gauge.png" alt="QuotaLens menu bar panel with usage rings" style="width: 100%; max-width: 400px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p style="font-weight: bold; margin-bottom: 0.5rem;">One glance, zero anxiety:</p>
    <p>QuotaLens sits in your menu bar with a little colored ring — orange for Claude, teal for Codex. Pop it open and you get live 5-hour and 7-day usage, per account, plus a 24-hour activity timeline. When the ring hits 90%, it turns red and yells at you <em>before</em> the API does.</p>
  </div>
</div>

A few bits I'm low-key proud of:

### It reads the *official* numbers, not vibes

Most usage trackers just guess by counting your local logs. QuotaLens does both: it parses the local JSONL session logs for token/cost detail, **and** it fires a minimal throttled probe (literally a `max_tokens: 1` request, at most once every five minutes) purely to read the official rate-limit headers back. Official numbers always win. So the ring you see is the same number Anthropic sees — no more "why am I banned, my tracker said 60%".

### Local-first, zero dependencies, actually

The whole app is pure Swift with system frameworks only — no Electron, no analytics, no server. Your usage data never leaves the Mac. And parsing history was a fun one: my own Claude logs were ~500MB of JSONL across five hundred files 💀, so there's an incremental byte-offset reader and a per-day cache that only chews the new bytes. First full scan takes a moment; after that it's instant.

<img src="/quotalens-stats.png" alt="QuotaLens statistics window with token and cost trends" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

### A proper stats window for the data gremlins

Tokens, cost, and cache-hit rate over Today / 3d / 7d / 30d / All, with Claude and Codex plotted side by side. It's weirdly satisfying watching the cost line and realizing your caching discipline actually works (63% cache hit, baby).

Obligatory dev blooper: at one point the "reset detection" logic decided that *every tiny dip* in the official percentage meant a new rate-limit window had started, so it archived about forty fake "cycles" in one afternoon and cheerfully notified me that my quota had reset. Forty times. Nothing builds trust in your monitoring tool like it hallucinating good news 😅. It now requires a real drop before it believes anything.

Install is one brew away:

```
brew tap mangiapanejohn-dev/tap
brew install --cask quotalens
```

macOS 13+, MIT licensed, open source. If it saves you from one mid-refactor rate-limit wall, drop a star ⭐ — apparently a lot of you already have, and I'm still grinning about it.

Alright, back to watching my own ring fill up while I build stuff. Catch you next time!

**Get QuotaLens:** **[https://quotalens.fun](https://quotalens.fun)** — know where every token goes.
