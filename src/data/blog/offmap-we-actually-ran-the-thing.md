---
title: "Offmap-X — We Actually Ran the Thing"
description: "For months Offmap-X was a schema, a deploy pipeline and a lot of server actions. Then a few hundred people walked into a building in Chengdu and it stopped being software. Notes on the week the system met the people it was for."
pubDatetime: 2026-08-26T12:00:00Z
tags: ["Building", "Offmap-X", "Founder Notes"]
cover: "/offmap-chengdu.webp"
---

There's a specific kind of unreality to building event software before the event exists.

You write a registration flow and nobody registers. You write a review queue and there is nothing in it. You write judging, and scoring, and a submission deadline, and a voting system with four votes per contestant, and all of it runs perfectly against seed data you invented, which is to say all of it runs perfectly against a world you also wrote. For months the most honest description of Offmap-X was: a Postgres schema, a couple of dozen server actions, and a Vercel project that goes green.

Then, on the twenty-third of August, people showed up.

### What existed before anyone showed up

The lineage is short and I'll keep it short: I got into this by building a website for a hackathon that didn't have one, ended up as the first engineer on that team, and eventually the work and the team moved on to something of their own. Offmap-X is that something. I'm the CTO of the team that runs it, which mostly means I'm the person whose phone matters at 2 a.m.

By the time Chengdu came around, "the site" had stopped being a site. Registration and authentication. Participant and team management. An admin console, a reviewer flow, a judging flow, project submission with file uploads, voting, receipts and reimbursement, transactional email, the contracts people sign for a seat. Server actions, API routes, webhooks, row-level security, storage policies, stored procedures, CI security checks. It is a real application, and I could describe every seam in it from memory, and none of that told me anything useful about what was going to happen in that building.

### The moment it stops being software

Here is what changes, and I don't think you can learn it any other way.

A bug in staging is a puzzle. You reproduce it, you narrow it, you fix it, and the whole time you are the only person in the room. A bug at an event is a person standing in front of you who cannot submit their project, and the clock is real, and there are eleven other people behind them, and the fix and the conversation are the same event happening at the same time.

Some of it was code. On the twenty-third I found, in a local preview, a voting path where the interface counted one vote and the server counted three — the kind of discrepancy that is invisible until the number matters to someone, and then it is the only thing that matters. I found a fallback path that misbehaved when the current event resolved to null during a migration window. Seven database migrations are dated inside the event itself: one on the twenty-third, one on the twenty-fourth, and five on the twenty-fifth, the final day. Poster formats, upload policy for solo participants, who actually owns a submission, four votes per team. Every one of those is a rule that seemed adequately specified until someone tried to use it.

And a lot of it wasn't code at all. The venue has one WiFi exit. Which means every person in the room shares an IP address, and a naive per-IP rate limit — the obvious defence, the one I'd have written without thinking about it two weeks earlier — locks the entire venue out of its own event. The check-in flow uses the camera, and the camera has to keep working no matter what else is being tightened. Our autosave fires every couple of seconds, which is fine for one person and is a thousand requests a minute from a room. Every security decision I'd been making in the abstract had a physical constraint attached to it that only existed once the room existed.

I'd built all this defensively, from an incident a week earlier that I've written about separately. Sitting in the venue was the first time the defences had to coexist with several dozen people on one network trying to do legitimate things very fast. Those are not the same test.

### Developer to operator

I did not spend the three days at a laptop. I spent maybe half of it at a laptop and the other half doing things I have no training for: explaining a rule to someone who had understood it differently, working out whether a submission that arrived four minutes late was a submission, keeping a room moving through a presentation schedule, answering the same question eleven times without the eleventh person hearing anything different in my voice than the first one did.

There is a lot of chaos in a seventy-two hour event. Things break, people misread instructions, a project won't render on the projector, someone's teammate leaves, the schedule slips and then slips again. I kept expecting to hit the point where I lost the thread of it. It didn't really come. Not because I'm calm — I'm not especially — but because when you are the person holding the thing, the alternative to staying steady is watching it stop, and that turns out to be a very effective motivator.

The part I was least prepared for is that "is this working?" stopped being a question with a technical answer. The system was up the entire time. The system being up was not the same as the event working, and I could not have told you the difference in advance.

### It finished

That's the whole claim, and I think it's a bigger one than it sounds.

Participants arrived. Teams formed. Projects got built, submitted, and presented. Judges judged. Demo Day happened. Scores came out. Then everyone went home and the site is now showing a Chengdu retrospective and pointing at the next city.

Most software I have written has never been used by anyone standing in a room. This one was. Registration wasn't a flow, it was how a person got a seat. The submission deadline wasn't a timestamp comparison, it was the moment a team stopped working. The uptime graph I'd been watching for months was, for three days, a building with people in it.

It stopped being a website and became infrastructure that real people were standing inside. I don't think I understood the weight of that distinction until I was in there with them.

**Offmap-X:** [offmap-x.org](https://offmap-x.org)
