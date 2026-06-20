---
title: "📣 I Built DiscorverX — What If Discord and Your Campus Had a Baby"
description: "A dev diary about DiscorverX, a campus social platform that mashes a Twitter-style feed with Discord-style real-time channels, so your whole school life lives in one app."
pubDatetime: 2026-06-09T12:00:00Z
tags: ["Dev Diary", "AI"]
cover: "/discorverx-landing.png"
---

Yoo fellow coders and campus slackers! It's Marc again 😜

Different flavor today. Not a CLI tool, not a sneaky bypass thing — this time I built a full-on social platform. Say hi to **DiscorverX**: imagine if Discord and your campus had a baby, and that baby actually had good taste.

Let me set the scene (you know I love a good scene): campus life is scattered across a hundred WeChat groups, random QQ chats, posters nobody reads, and group links that expire before you even click them. Wanna find people building cool stuff at your school? Good luck. Wanna ask a quick question to your whole department? Spam five group chats and pray. I was so done with it that I thought, "Why isn't there ONE place for all of this?" And you already know how that sentence ends — I built it myself.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/discorverx-landing.png" alt="DiscorverX landing page" style="width: 100%; max-width: 400px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p style="font-weight: bold; margin-bottom: 0.5rem;">One app for your whole campus:</p>
    <p>Post campus updates, browse a feed by nationwide / province / your own school, and jump into real-time community channels — all in one place.</p>
  </div>
</div>

Here's the core idea: DiscorverX is two things stitched together that usually live in two different apps.

**Part one — the feed.** It's your campus timeline. Drop a post, share a side project, ask a dumb question, flex a win. You can filter the whole thing three ways: **Nationwide** (全国), **Your Province** (本省), and **Your School** (本校). So you can either zoom out and see what students everywhere are building, or zoom all the way in to just your campus. There's a "For You" recommendation tab, a Following tab, Trending, Media, and even an AI-picked feed — because of course I had to sneak some AI in there 🤫.

<img src="/discorverx-feed.png" alt="DiscorverX feed homepage" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

**Part two — the channels.** This is the Discord half. You can spin up groups with text channels (`#general`, `#-coding`, whatever you want) and chat in real time. Online/offline member list, reactions, the whole vibe. My own little server already has the crew in it dropping "yooo thanks" and 🎉 reactions on builds. It feels less like a forum and more like hanging out.

<img src="/discorverx-chat.png" alt="DiscorverX real-time group channel" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin: 2rem 0;" />

And because I'm a lazy developer who hates friction, getting in is dead simple — sign in with Google or just an email and password, pick your school, and you're in. No invite-link scavenger hunt, no "ask an admin to add you" nonsense.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/discorverx-login.png" alt="DiscorverX sign-in page" style="width: 100%; max-width: 400px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p style="font-weight: bold; margin-bottom: 0.5rem;">"It happens here."</p>
    <p>That's the whole pitch. Sign in, connect your campus life, and stop juggling fifteen group chats.</p>
  </div>
</div>

Time for a blooper, as tradition demands: I spent an entire night chasing a bug where new posts showed up for some users but not others. Convinced it was some deep real-time sync nightmare, I rewrote half the feed logic. Turns out I was caching the timeline too aggressively and never busting it. One line. ONE LINE. I closed my laptop very gently and went to bed before I did something dramatic 😂.

Real talk: I didn't build DiscorverX to "kill Discord" or whatever. I built it because campus stuff should not feel like archaeology. It's still early, there are rough edges, and the trending tab literally says "no hot topics yet" because, well, it's day one — but it's live, it works, and people are actually posting on it.

If you're a student (or just nosy), come make an account and post something. Yell at me about bugs, request features, or just say hi in a channel — feedback is the fuel. More people = a better campus = a better DiscorverX.

Alright, that's enough rambling. I'm off to add more channels and probably break the feed again 😜. Catch you next time!

**Try DiscorverX:** **[https://m.discorver.club](https://m.discorver.club)** — your whole campus, one app.
