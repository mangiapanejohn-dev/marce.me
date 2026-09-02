---
title: "168,386 Applications Later"
description: "Offmap-X took 168,386 forged applications in five hours. Nothing was broken into — every row was written by an account that was allowed to write it. A postmortem about the difference between authorization and abuse prevention."
pubDatetime: 2026-08-20T12:00:00Z
tags: ["Offmap-X", "Security", "Building"]
cover: "/cover-168386.svg"
---

Before that morning, the `applications` table on Offmap-X held about four hundred rows. Real ones. People signing up for a hackathon in Chengdu.

By the time anyone looked at it, it held 168,926.

The difference — 168,386 rows — arrived between 03:02 and 08:13 UTC, at roughly eleven hundred rows a second, and all of it came from two accounts. Both of them were signed in. Both of them were doing something the system had told them they were allowed to do.

That last sentence is the entire postmortem. Everything else is detail.

### Nothing was broken into

I want to be precise about this, because the tempting version of the story is more dramatic and less true.

The database was not compromised. No credential leaked. Nobody escalated to an admin role. The rows were not written through some clever back door — they were written through the front door, by an authenticated client holding an ordinary user token, talking straight to the data API instead of to my application.

That last part is worth sitting with for a second. A Supabase anon key is not a secret; it ships in the browser, it is supposed to. Which means the data API is a public endpoint, and any signed-in user can address it directly. My application was never the gate. It was just the most convenient way to walk through the gate.

The actual gate was a row-level security policy on that table. And the policy did exactly what it said: it checked that the row you were inserting belonged to you.

It did not check anything else. Not the status you were writing. Not how many rows you already had. There was a uniqueness constraint meant to hold one application per person per event, but it was a partial index — it only applied to some of the status values, and rows written with a status it didn't cover slipped past it and kept slipping past it, forever, at machine speed.

So: was the actor authorized to insert an application row? Yes. Unambiguously yes. Every single one of those 168,386 inserts was an operation that a correctly-implemented authorization system was supposed to permit.

### Authorization and abuse prevention are not the same problem

I had been thinking about security as a property of individual operations. Can this person do this thing? Is there a check in front of it? Walk the surface, find the unguarded ones, guard them.

That model has a hole in the middle of it, and the hole is that it has no opinion about repetition. A user who is allowed to create an application is not thereby allowed to create a hundred thousand applications, but nothing in "can this person do this thing?" expresses that. You ask the question once, per row, and it keeps answering yes, because per row the answer genuinely is yes.

The failure was not a missing check. It was a category of check I did not have at all.

Two things follow from that, and they took me longer to accept than they should have:

**Rate is part of the authorization decision.** Not a performance concern, not something you bolt on when traffic gets annoying. If a permission has no bound on how often it can be exercised, it is not fully specified.

**Availability is a security property.** The visible damage here wasn't data theft. It was that the database ran out of CPU and connections, and then nobody could register, nobody could log in, and the portal stopped answering — a week before an event people had already booked travel for. A system that is up but wrong and a system that is down are both systems that failed the people using them.

### It ran for five hours because nothing was watching

The thing I find hardest to write down is that the attack did not end because we caught it. It ended, and then a while later we noticed, because a resource graph went vertical and services started timing out.

There was no detector. Not a bad detector — none. No alert on write volume, no anomaly on a single account producing more rows in an hour than the entire event had produced in a month, no signal at all until the infrastructure itself gave out. Five hours is not a detection delay. Five hours is the absence of detection, measured by how long it happened to take for the symptom to become physical.

### My first explanation was wrong

I wrote an incident report that same day, while it was still happening. In it I attributed the outage to something else entirely: a participant had been running a security scanner against the site and had found a genuinely awful route of mine — an admin endpoint that executed arbitrary SQL with elevated privileges and had no authentication in front of it at all. That was real, it was mine, it was inexcusable, and I removed it.

But it was not what caused this. The forensic work over the following days established the actual mechanism, and marked the connection between the scanner and the flood as _not established_. Two separate bad things happened to the same system in the same window, and in the first hours I welded them into one story because one story is easier to hold than two.

I've left that first report in the repository unedited. It's a useful artifact: it's what my judgment looks like at hour three, and it's wrong.

### What changed

The instinct after something like this is to go find every unguarded write and guard it. I started there. It doesn't work, and the reason it doesn't work is instructive: the day after, reviewing for the same shape of problem, I found two more legacy tables with the same weakness. They had never been defined in the migration chain at all — they existed in production and nowhere in the code. Table-by-table hardening can only ever cover the tables you managed to enumerate, and drift guarantees you didn't enumerate all of them.

So the fix moved down a layer, from _policies_ to _grants_:

- The `anon` and `authenticated` roles hold **no write privileges** in the public schema. Not narrowed — none. A user-scoped client attempting to write now gets a hard refusal, and that refusal is the design rather than a misconfiguration.
- Every write goes through a server action holding a privileged client, behind an explicit authentication check, an explicit role check, and an explicit ownership check. Which means the application layer is now the only real gate, honestly and visibly, instead of being a gate I merely assumed was there.
- Row-level security stays exactly as it was, demoted to a second layer that catches what the first one misses.
- A build-time guard fails CI if a privileged client shows up in a function without those checks around it, so the invariant is enforced by the build rather than by me remembering.
- A database event trigger revokes write access on any newly created table automatically. Drift will keep happening. It no longer opens a door when it does.

On top of that sits a detection layer — risk state per subject, escalating dispositions, an actual security console — and a deception layer that can route a suspected abuser into a synthetic copy of the world rather than the real one. Those are worth their own writeup. The honest summary is that the interesting part of both was never the detection logic; it was deciding what evidence is strong enough to act on, and what you owe a real person you have wrongly suspected.

### The parts where I looked stupid

A postmortem that only contains the attacker's mistakes is marketing.

On the morning of the seventeenth I tightened the database permissions before deploying the code that depended on them. Seven production write paths started returning 403 immediately — saving your profile, marking notifications read, granting roles, email templates, event seasons, judge scoring. I had to re-grant temporarily to stop the bleeding and then do it again in the right order. The rollout order was a hard constraint and I knew it was a hard constraint and I did it backwards anyway.

The same change surfaced a path that had been silently broken for a full day: bulk application review had been failing with a permission error since the first fix landed, and nobody noticed because nobody happened to click it.

And the honeypot — a field invisible to humans that only an automated client would fill in — I named `company`. Browser autofill helpfully filled it in for actual people, and my bot detector started flagging real applicants. The payload key was also literally named `honeypot`, which is roughly like labelling the trapdoor. Both fixed. Both entirely my own doing.

### The question I actually took from it

I used to ask, of any endpoint: _who is allowed to call this?_

It's the right question. It's just badly underspecified, and the number 168,386 is what the underspecification costs. The version I ask now has a second half:

**Who is allowed to call this, and how many times before the answer should change?**

Security is not a set of features you add. It's a set of boundaries you can point at and say what each one holds. Mine held who. It never held how much.
