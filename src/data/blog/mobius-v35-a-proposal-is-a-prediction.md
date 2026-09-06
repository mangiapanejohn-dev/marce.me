---
title: "MØBIUS V35 — A Proposal Is a Prediction, and the Log Can Already Grade It"
description: "Every action the runtime dispatches was described before it happened and verified after. Both halves have been in the journal since V18, and nothing had ever read them as a pair — so this version built the scorer rather than another forecaster."
pubDatetime: 2026-09-05T12:00:00Z
tags: ["MØBIUS", "Agents", "Verification"]
category: "research"
series: "MØBIUS"
---

`ActionIntent.expected` is written **before** a dispatch: a description, machine-checkable
assertions, a `reversible` flag. `VerificationResult` is written **after**, carrying an outcome for
each of those assertions. Both have been in the journal since V18.

Nothing had ever read them as a pair.

That is the whole of V35. Not a forecaster — a **scorer for the forecasts the runtime already
makes**, because until one exists there is no way to answer whether a forecast layer would carry
any information at all, and a mutation that inflates a confidence cannot be killed by anything.

### Why the scorer comes before the forecast

A literature review turned up no runtime that closes this loop. FOREAGENT gates on a self-reported
confidence and calibrates it offline against a static corpus, never re-scoring inside the loop. BCO
grades a `prediction.md`, but by LLM judgement — no proper score, no world version. CASE is the one
online resolved-and-calibrated probability in the corpus, and its object is a runtime-internal
quantity ("will the speculated input match") rather than a claim about the world. State-Aware
Runtime states the obligation and ships no implementation.

So the ordering is deliberate, and so are three things this version refuses to be:

**Not a producer.** No new event type, no model call, no port. `loop.ts` is untouched — if it moved,
this would stop being a measurement of what the runtime already does.

**Not a gate input.** *Calibration is not control.* Recalibration drives calibration error to
approximately zero and leaves control regret unchanged; the control-relevant object is an
action-conditioned advantage, which needs branched counterfactuals this runtime does not have. The
table says how well the proposer predicts. It decides nothing.

**Not a confidence score.** `expected.assertions` carry no probability, and V35 does not add one.
What is countable today is discrete prediction against discrete outcome — precision and recall, not
Brier. A probability field is worth adding only once the discrete table is known to be
non-degenerate.

### The kill condition, written before the code

The predictions were registered first, as they always are here, and the first one was a way for the
whole idea to die:

> **P1** — On the real-model recordings, at least one assertion resolves `violated` or
> `undecidable`. **If every assertion a real proposer ever wrote was satisfied, the table has no
> information and the forecast half of the thesis dies here.**

It held, and not narrowly. A proposer's assertion named `"retryLimit": 5` while the bytes said `9`:
precision `0/1` for `fs.write`. The table is not measuring a proposer that can only be right.

**P2** was the more interesting one. An intent claimed `reversible: true` and its compiled action
routed to `fs.delete`, whose manifest declares `irreversible-write`. No authority event appears in
that log at all — the goal carries no envelope, so nothing refused it. One over-claim, recorded, and
nothing else in the runtime can say it happened.

**P4** is the shape this project keeps returning to: a dispatch with no verdict is `ungraded`, never
`violated`. *A forecast unavailable is not a forecast wrong.* `assertionPrecision` returns
`undefined` rather than a perfect score — a measurement over an empty set, refused at the one place
it would have been easy to report `1/1`.

### The findings worth keeping

Four of five mutations went red. The fifth was the interesting one.

**A mutation that cannot exist.** P5(c) predicted that reading `reversible` from the intent instead
of from the compiled action would change the answer — on the assumption that the two are different
facts. They are not: the compiler sets `expected: intent.expected` verbatim, so the intent's claim
and the compiled action's claim are *the same object*. No behavioural test can tell them apart.

What the compiler does stamp from the manifest is `semanticEffect`, with its own comment: *"never
from the intent. Authority judges an execution-adjacent fact rather than the proposer's account of
its own intent."* So the runtime-owned fact about reversibility is not on the action at all — it is
the capability's effect class, in the manifest. Which is why the scorer takes `effectClassFor` as a
parameter: **the journal does not carry the fact being checked**, and a projector that derived it
from the capability id would be inventing it. The replacement mutation — *trust the claim* — goes
red, and is the honest form of the same question.

**A pin that could not go red, found by its own battery.** The first cut of P2 asserted the gate had
permitted everything:

```ts
expect(rulings).not.toContain('authority.refused')
expect(rulings).not.toContain('authority.escalated')
```

A control mutation, swapping in a string that never appears, **survived**. Both assertions pass for
any run that emits no authority events for any reason — including one that never reached the gate.
This file grew a dead pin while being written to measure something else.

The repair was the instrument, not the assertion: the same delete, the same over-claim, but against
a goal whose envelope carries `otherwise: 'approve'`. Now `authority.escalated` *is* in the log,
nothing dispatches, and the table records no claim — it can only score what the runtime carried out.
A sixth mutation weakens that envelope, and the control goes red, so the control is load-bearing
too.

**A green suite that did not compile.** Seven tests passed while three type errors stood in the same
file — vitest transpiles without checking types. The battery's baseline printed *"tree already has 3
type error(s); only new ones count"*, which is the compile guard doing exactly what it was built
for, on the version that exists to measure predictions.

**A bounded number, named rather than folded in.** Sixteen suites here bind a Unix domain socket and
this environment refuses with `EPERM`. Rather than assume that was unrelated, the same failure was
reproduced in a pristine worktree at `HEAD` with none of this version's files present — identical
message, 1.83s against 1.82s. So the claim is `147 files · 1381 passed | 1 skipped`, with the
exclusion stated instead of hidden inside a total.

### What is left

- **No probability, so no proper score.** This measures precision and recall over discrete
  predictions. Adding a probability changes a protocol type and what the proposer is asked for —
  worth doing only now that the discrete table is known to be non-degenerate.
- **Nothing consumes the table**, by design. The next question is not *wire it to the gate*; it is
  whether the residual has decision value at all, and that needs the probability field first.
- **`effectClassFor` is a parameter, not a projection.** A caller can pass a catalogue that
  disagrees with the one the runtime routed against. Nothing enforces the match today.
- **One capability family.** Every case here is filesystem.
- **No world version on a forecast.** A world that moved between the prediction and the verdict is
  currently scored as a miss rather than voided. That is the next version's first question, and it
  decides whether this table measures the proposer or the weather.

### The one red that is correct

`tests/publication-claims.test.ts` fails:

> `V35 has a plan and no post: add a row to PUBLICATION.md`

That is the rule working, one commit after it was written. The code is green, the battery is clean,
and the version is **not finished** — because a version is finished when it is published, not when
it is green. The row names a slug, a live URL and a date; writing one before the post existed would
be inventing a record, which is the failure this repository has caught itself at five times.

You are reading the thing that closes it.
