---
title: "⛏️ TabWorld — Minecraft in a Browser Tab, and the Three Architectures I Had to Kill First"
description: "Dev diary about TabWorld, a site where you open a tab, pick a world, and play Minecraft with friends — no install, no server, no cost. Also a confession about the self-built engine, the Docker fleet, and the tunnel daemon I shelved to get there."
pubDatetime: 2026-07-04T12:00:00Z
tags: ["Dev Diary", "Web", "Games"]
cover: "/tabworld-hero.png"
---

Yoo fellow coders and block-placing enjoyers! Marc here 😜

Today's diary is about **TabWorld** — a website where you open a browser tab, pick a world, and you're playing Minecraft with your friends. No launcher, no download, no VPS bill. And honestly, the real story isn't the product. It's the graveyard of over-engineered architectures I had to bury to get here 🪦.

<img src="/tabworld-hero.png" alt="TabWorld landing page — no install, browser-first Minecraft" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

The itch: my friends and I wanted to hop into a quick shared world after class. But vanilla multiplayer means someone rents a server, someone installs a launcher, someone's on a school laptop that can't install anything. The dream was "playing together should be as easy as sharing a link."

So naturally, I did the most Marc thing possible and **massively over-built it. Three times.**

### Architecture graveyard, in loving memory

**Attempt #1: write my own engine.** Three.js renderer, a hand-rolled 1.20.4 chunk decoder (custom palette containers! greedy meshing! unit tests!), browser-side Minecraft protocol. It worked… ish. It was also a lifetime project disguised as a feature. Shelved.

**Attempt #2: host everyone's worlds.** Full Turborepo platform — six apps: orchestrator spinning up Docker Paper servers, a WebSocket↔TCP proxy, a router, job queues, a whole multi-tenant database schema with backups and audit logs. It was beautiful. It also meant *I* pay for every idle world, forever. Shelved.

**Attempt #3: BYO compute.** Players run a desktop agent that hosts the server on their own machine through a reverse tunnel. Design doc was gorgeous. Then I hit the fact that the whole thing still needs a relay, plus a Java version conflict right in the middle of the stack. Shelved before a line of the tunnel was written.

Bonus blooper from this era: the old engine routes were so heavy that pulling Three.js + the protocol stack into the build **OOM'd Vercel's 8GB build container** 💀. When your *build machine* runs out of memory, the universe is telling you something.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/tabworld-steps.png" alt="Three steps to playing on TabWorld" style="width: 100%; max-width: 400px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p style="font-weight: bold; margin-bottom: 0.5rem;">The final shape:</p>
    <p>Open TabWorld → pick a version and a nickname → start a world and share a 5-letter code. Your friend hits Direct Connect, types the code, done. <strong>The host's browser tab <em>is</em> the server</strong> — peer-to-peer, relayed through public relays. Zero backend. Zero cost. Zero "let me just install Java real quick".</p>
  </div>
</div>

The engine that makes this possible is **EaglercraftX** — a wild community project that runs 1.8.8 fully in the browser, with built-in shared worlds. I did not write the game, and TabWorld doesn't pretend to (there's an honest credit line in the footer, and no, we're not affiliated with Mojang). What TabWorld adds is everything around it: a clean launcher, custom profiles, sane defaults, docs that explain the boring parts, and a bunch of invisible glue — like hand-encoding NBT to inject server entries into the runtime's local storage byte-for-byte, and using the Keyboard Lock API so pressing Escape opens the *game* menu instead of yeeting you out of fullscreen.

<img src="/tabworld-features.png" alt="TabWorld feature grid — launcher, versions, servers, profiles" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

Real talk: the lesson of TabWorld is that the best architecture was the one with the least *my code* in it. I spent weeks building server fleets so that people could play together, when "the host's tab is the server" was sitting right there. Deleting three architectures hurt. Shipping the simple one felt better.

If you've got ten minutes and a friend, go punch a tree together. And if you're curious about the shelved engine, ping me — the greedy mesher deserves a eulogy post of its own 😅.

**Play now:** **[https://tabworld.fun](https://tabworld.fun)** — open the browser, pick a world, start playing.
