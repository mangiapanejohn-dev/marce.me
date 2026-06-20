---
title: "👾 Am I Crazy? Built a Personal AI Agent in Two Weeks"
description: "A rogue developer's funny journey of building Resonix-AG, an autonomous AI agent with permanent memory and self-learning capabilities, to fix the frustration of 'goldfish-memory' traditional AIs."
pubDatetime: 2026-02-06T01:00:00Z
tags: ["Dev Diary", "AI"]
cover: "/IMG_3375.jpg"
---

Yoo! Hey fellow coders and slacker buddies, I'm Marc, a rogue developer who got so fed up with traditional AI that I decided to build my own 😂. Today, no fancy tech jargon, no pretending to be a guru—just gonna chat about why I went nuts and spent two months hacking together the Resonix-AG repo, and how weirdly "in tune" it is with me.

Let me set the scene: As someone who codes and messes with AI every day, I'm totally done with those "goldfish-memory" AI assistants! One second I'm telling it, "I like my coffee with oat milk, not bubble tea," and the next, when I ask what I prefer, it's like, "Huh? What'd you say?" Having to explain myself from scratch every single conversation is like babysitting a toddler—I'm this close to throwing my keyboard out the window.

So one late night, I stared at my Claude chat window and thought, "If no one's gonna make an AI that actually remembers me, why not do it myself?" And just like that, I dived in. Two months later, what started as a janky demo is now Resonix-AG—stable, self-learning, and full of bugs I've cried over (okay, maybe not cried, but definitely sighed loudly at 2 AM). The number of potholes I hit? Let's just say it's a good thing I don't charge by the hour.

<div style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; margin: 2rem 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 280px;">
    <img src="/IMG_3375.jpg" alt="Resonix-AG Demo" style="width: 100%; max-width: 400px; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);" />
  </div>
  <div style="flex: 1; min-width: 280px;">
    <p><strong>Let me cut to the chase:</strong> Resonix-AG isn't some fancy black tech—it's an autonomous AI agent that treats you like a friend, not a stranger.</p>
    <p>It remembers every word you say, every preference you have, and even every mistake you make—so it'll never repeat your blunders. Promise.</p>
  </div>
</div>

Let me cut to the chase: Resonix-AG isn't some fancy black tech—it's an autonomous AI agent that treats you like a friend, not a stranger. Simply put, it's not "petty," but it remembers every word you say, every preference you have, and even every mistake you make—so it'll never repeat your blunders. Promise.

Case in point 🌰: Tell it, "I'm a night owl, and I work best between 10 PM and 2 AM," then add, "I hate parsing HTML with regex—it always crashes." A few days later, ask it, "When do I work most efficiently? And what's the deal with parsing HTML?" It'll repeat your words verbatim, and even nudge you: "Don't forget that regex HTML fail you had last week!" More attentive than your partner (no shade, bae).

I know what you're thinking: "Isn't that just a memory feature? Big whoop." Oh, it's way more than that! I built it with a two-layer permanent memory system. Layer A stores your preferences and habits in machine-readable code, but Layer B? It's a game-changer. It creates a folder right on your desktop (~/Desktop/resonix-M/) with human-readable files—your identity, knowledge, chat history, everything. No secrets, no guesswork—just open the folder if you wanna check what it's "thinking."

Another thing I'm low-key proud of: It evolves! Not the "empty marketing slogan" kind of evolution—actual, learn-from-mistakes evolution. Let it run an automation task, and after it's done, it'll analyze the results, figure out what worked and what flopped, and store that lesson. Next time you ask it to do something similar, it'll avoid the same pitfalls and work twice as fast. It's like having a tiny apprentice that gets better the more you use it—no constant micromanaging required.

Speaking of automation, let me rant about the browser tools I used to use—total garbage! They either rely on Chrome extensions that crash every five minutes, or their element selectors are so rigid that a single webpage update breaks everything. I'd spend hours debugging and yelling, "Why is this so bad?!" So this time, I built Resonix-AG with Playwright—no sketchy extensions, smart element detection that survives UI updates, automatic screenshots, and consistent results. Suddenly, my slacking time doubled 🤫.

Look, I'm a rogue developer—I don't do fancy, unnecessary features. The whole point is "useful, easy to use, and no hassle." Installation is a breeze, too. Whether you're on macOS, Linux, Windows, or even Termux, just copy one line of code and you're good to go. No complicated setup, no dependency headaches—even newbies can figure it out (because let's be real, I'm too lazy to deal with complex configs myself).

Let me share a couple of bloopers from development: One night, I stayed up till 4 AM fixing a Windows compatibility issue, only to realize the problem was a missing punctuation mark. I wanted to throw my laptop across the room, but hey—it worked in the end. Otherwise, Resonix-AG would've been a "macOS-only biased AI." Another time, I tested the memory feature by rambling about bubble tea for an hour—and it filled my desktop folder with so many bubble tea preferences, I thought my computer was gonna crash 😂.

Right now, Resonix-AG is on version 2026.3.12, and I've added support for Telegram, Discord, Slack, and WhatsApp. No matter what app you use, you can chat with it and send commands anytime, anywhere. And yeah, I open-sourced the whole thing on GitHub (that's the repo you're looking at). If you're a coder and wanna mess around with it, clone it, test it, submit PRs, or point out bugs—I'd owe you a coffee (with oat milk, obviously). Let's be real, one person can only catch so many issues—more brains = better AI.

Let me get real for a second: I didn't build Resonix-AG to be some fancy, world-changing project. I built it because I wanted an AI that "gets" me—one I don't have to explain myself to over and over, one that grows with me. It's not perfect, it's got bugs, and it's still a work in progress—but it's my two-month labor of love, my "coding baby."

If you try Resonix-AG and like it, please drop a star ⭐ on the repo. It might seem small, but it means the world to me—it's the fuel that keeps me coding and improving. And if you hate it? Spam my issues tab with complaints! I'm not fragile—feedback (even the angry kind) is how we get better.

Alright, that's enough rambling. I'm off to add new features to Resonix-AG. Catch you next time—here's hoping it gets even better at understanding you (and me) 😜.

Repo link: **[https://github.com/mangiapanejohn-dev/Resonix-AG](https://github.com/mangiapanejohn-dev/Resonix-AG)** — come play around!