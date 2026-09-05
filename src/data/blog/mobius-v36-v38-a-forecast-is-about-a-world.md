---
title: "MØBIUS V36–V38 — A Forecast Is a Claim About a World, and the World Has to Be Named"
description: "V35 built a scorer. Three versions then spent their whole length answering a question the scorer had made askable: which world is a prediction about? Two of the three refuted the version before them."
pubDatetime: 2026-09-05T18:30:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

V35 scored the pair the journal already carried — a prediction written before a dispatch, a verdict
written after. The moment that table existed it asked a question it could not answer: **if something
other than the action moved the world in between, who is being charged for it?**

Three versions on that question. Two of them refuted the version before.

### V36 — a world that moved is not a wrong forecast

The signal was already there, and was measured before anything was designed. A filesystem write
bumps the session's `worldRevision`; a read does not. `EffectReceipt.worldRevisionAfter` records the
world the action's own effect left behind, and the observation that grades it carries its own
revision.

```
rcpt worldRevisionAfter=1
obs  worldRev=1
verd basis=fresh-observation
```

Equal means the verdict read exactly the world the action produced. Greater means someone else wrote
in between, and the assertions were graded against a world the prediction was not about. That case
becomes `void` — a third resolution beside `graded` and `ungraded`, kept separate because *a
forecast resolved against the wrong world is not a forecast that was wrong*.

Then its own P3 failed on the first cut, and the failure was worth more than the prediction.

The foreign write was made with `writeFileSync`, straight to disk. The result was **graded, not
voided**: the bytes changed and the counter did not. `worldRevision` is bumped inside the provider's
own write path. It is a count of writes *this provider performed*, not a version of the world — so
the rule is blind to a person editing the file, a build step, or anything that does not go through
the provider.

That was pinned as its own failing-when-fixed test rather than described in a comment, because the
sentence *"only provider-mediated writes are visible"* is exactly the kind that goes stale.

### V37 — the counter was wrong in both directions at once

The probe that opened V37 caught the other half. The counter is not only blind, it is also **too
broad**: V36's own P3 voided a forecast about `settings.json` because someone wrote `unrelated.txt`
through the provider. A file the assertions never read moving does not make a prediction about
another file unresolvable.

| | provider-bypassing write to the action's own resource | provider write to an unrelated resource |
|---|---|---|
| **counter** (V36) | misses it | voids — over-broad |
| **identity** (V37) | voids | grades |

One run, two rules, opposite answers:

```
RCPT settings.json = dbe90cd729a1   worldRevisionAfter = 1
OBS  settings.json = a7254c4184a3   worldRevision      = 1
```

So drift became a resource changing **content identity**, scoped to the resources this action's own
receipt attributed. Receipts *attribute*; observations *compare*. A difference an observation reports
that no receipt explains is unexplained change — which is `DependencyInvalidator`'s rule, folded from
the log instead of held in memory.

**V36's P3 stands refuted in its own plan, unedited.** It is an accurate record of what the counter
rule did and of the evidence that convinced that version; rewriting it to agree with the next version
would remove the only trace that the rule was wrong in a way its own battery could not see.

#### A mutation with no case that could kill it

The pre-registered mutation list included *drop the receipt-attributed scope, so an unrelated
resource voids again*. Writing the battery, it had no test that could go red: the foreign write in
every fixture landed on a file no receipt had ever attributed, so a rule comparing **every** witnessed
resource and one comparing **this action's** would both grade it. The mutation would have run, the
suite would have stayed green, and the battery would have reported a survivor whose real meaning is
*the property was never tested*.

The repair is a case, not an assertion. Two actions in one run; the first makes `other.json` true; a
foreign writer then changes `other.json` behind the provider's back; the look that grades the
**second** action reports the change. A global-witness rule voids the second action, the scoped rule
grades it — and the test asserts the drift was real before it asserts the grade, so it cannot pass by
nothing having happened.

### V38 — the world a prediction was made in

V37 left a residual it stated plainly: a foreign write to a resource the runtime has **never made
true** has no witness to differ from. Closing that needs a witness taken *before* the action.

V36 had concluded that witness did not exist. It was wrong, and the way it was wrong is the finding.

One probe, real compiler, two write intents in a single run:

```
 3 action.dispatched    a1   basis: null
 6 observation.received  obs-1  worldRevision 1
 7 verification.decided  fresh-observation ← obs-1
12 action.dispatched    a2   basis: { observationId: "obs-1", targets: [], freshness: "advisory" }
```

The observation taken to *verify the first action* is the grounding the compiler stamps on the
second. The world a prediction was made in has been bindable since V21-2.

**V36's pin could not have seen it.** That test ran on a stub compiler that destructures
`{ intent, route }` and discards the `grounding` input entirely, so `expect(action.basis).toBeUndefined()`
held no matter what the loop supplied. It was measuring a double and was read as a report about the
runtime. Underneath it, the plan's conclusion *"nothing grounds the action"* was generalised from a
fixture with one action in it, where it is true for an unrelated reason.

Each failure hid the other: the stub made the pin unfalsifiable, and the one-action fixture made the
sentence look measured.

### The line V38 refused to cross

The premise makes a wider class of change visible — and V38 reports it without ever voiding on it.

V37 earned the right to void by **narrowing**: the resources this action's own receipt attributed,
because a forecast is about the resources its assertions read. The premise has no such scope. It
witnesses whatever the observation happened to capture — for `fs.observe` on `.`, the whole tree — so
voiding on it would restore precisely the over-broad failure V37 spent a version removing.

| window | scope | what it can honestly say |
|---|---|---|
| effect → verdict | this action's receipt | `void` — graded against the wrong world |
| premise → verdict | everything observed | *reported* — this decision's world moved |
| premise → verdict | `basis.targets` | would license voiding — **the field exists and nothing fills it** |

That third row is the standing debt. `ActionBasis.targets` is documented as *targets whose identity
must still resolve for the action to be valid* — exactly the declaration a premise scope needs — and
every provider writes `[]`.

### What three versions cost, and what they bought

Bought: a forecast that resolves `graded | ungraded | void`, where `void` means a specific,
identity-checked, receipt-scoped claim, plus a separately reported signal for the world a decision
was made in. None of it reaches the authority gate, for V35's reason unchanged — *calibration is not
control*.

Cost: two refuted predictions left standing, one vacuous pin found and rewritten, one mutation
replaced because it could not kill anything, and three cases moved out of V36's test file because
under the new rule they were green and **unable to go red** — which is worse than absent.
