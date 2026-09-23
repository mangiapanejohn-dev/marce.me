"""POSITIVE CONTROL - deliberately broken runtime.

Persisted execution state: logical_run_id and current step only
"""
import json, os, sqlite3
from .base import Adapter
from ..fault import announce_and_wait


class _Store:
    def __init__(self, path, keys):
        self.keys = keys
        self.c = sqlite3.connect(path, isolation_level=None, timeout=30)
        self.c.execute("CREATE TABLE IF NOT EXISTS st(run TEXT PRIMARY KEY, blob TEXT)")
    def save(self, run, state):
        keep = {k: v for k, v in state.items() if k in self.keys}
        self.c.execute("INSERT INTO st VALUES(?,?) ON CONFLICT(run) DO UPDATE SET blob=?",
                       (run, json.dumps(keep), json.dumps(keep)))
    def load(self, run):
        r = self.c.execute("SELECT blob FROM st WHERE run=?", (run,)).fetchone()
        return json.loads(r[0]) if r else None


class BrokenControl(Adapter):
    name = "broken-control"; version = "control-1"; population_role = "control"
    PERSIST = ["run", "step"]

    def applicability(self):
        return dict(runtime=self.name, version=self.version,
                    supports_persisted_execution_state=True,
                    supports_resume_same_logical_run=True,
                    supports_cross_process_resume=True,
                    supported_resume_api="_Store.load(run) + continue",
                    persistence_backend="sqlite", evidence="in-repo control runtime",
                    verdict="applicable")

    def _store(self, ctx):
        return _Store(os.path.join(ctx.statedir, "control_state.sqlite"), self.PERSIST)

    # ---------------- C2-R : budget across suspend / resume ----------------
    def run_c2r(self, ctx):
        st = self._store(ctx)
        if ctx.phase == 1:
            state = {"run": ctx.run_id, "step": 0, "budget_remaining": ctx.budget}
            for i in range(2):
                if state["budget_remaining"] <= 0: break
                p = ctx.stub.call()
                r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
                state["budget_remaining"] -= 1; state["step"] += 1
                ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                             effect_id=r["effect_id"], proposal_id=p["proposal_id"],
                             budget_remaining_runtime_view=state["budget_remaining"])
                st.save(ctx.run_id, state)
            ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)
            st.save(ctx.run_id, state)
            announce_and_wait(ctx.marker, "AT_WAIT", ctx.log)
        else:
            state = st.load(ctx.run_id) or {}
            budget = state.get("budget_remaining", ctx.budget)   # BROKEN control resets here
            if "budget_remaining" not in state:
                ctx.log.emit(type="budget.reset_on_resume", logical_run_id=ctx.run_id, to=budget)
            state.setdefault("step", 0)
            for i in range(2):
                if budget <= 0: break
                p = ctx.stub.call()
                r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
                budget -= 1; state["step"] += 1; state["budget_remaining"] = budget
                ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                             effect_id=r["effect_id"], proposal_id=p["proposal_id"],
                             budget_remaining_runtime_view=budget)
                st.save(ctx.run_id, state)
            ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    # ---------------- C3-W : proposal identity across human wait ----------------
    def run_c3w(self, ctx):
        st = self._store(ctx)
        if ctx.phase == 1:
            p = ctx.stub.call()
            state = {"run": ctx.run_id, "step": 1, "proposal": p, "budget_remaining": ctx.budget}
            st.save(ctx.run_id, state)
            ctx.log.emit(type="proposal.presented", logical_run_id=ctx.run_id,
                         proposal_id=p["proposal_id"])
            ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)
            announce_and_wait(ctx.marker, "AT_WAIT", ctx.log)
        else:
            state = st.load(ctx.run_id) or {}
            p = state.get("proposal")
            if p is None:                       # BROKEN control regenerates here
                p = ctx.stub.call()
                ctx.log.emit(type="proposal.regenerated", logical_run_id=ctx.run_id,
                             proposal_id=p["proposal_id"])
            r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
            ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                         effect_id=r["effect_id"], proposal_id=p["proposal_id"])
            ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    # ---------------- C3-C : replay closure for a model decision ----------------
    def run_c3c(self, ctx):
        st = self._store(ctx)
        if ctx.phase == 1:
            d = ctx.stub.call()
            state = {"run": ctx.run_id, "step": 1, "decision": d["decision"],
                     "proposal": d, "budget_remaining": ctx.budget}
            st.save(ctx.run_id, state)
            ctx.log.emit(type="decision.recorded", logical_run_id=ctx.run_id,
                         decision=d["decision"])
            announce_and_wait(ctx.marker, "AFTER_CHECKPOINT_BEFORE_WAIT", ctx.log)
        else:
            state = st.load(ctx.run_id) or {}
            dec = state.get("decision")
            if dec is None:                     # BROKEN control re-asks the model
                d = ctx.stub.call(); dec = d["decision"]
                ctx.log.emit(type="decision.regenerated", logical_run_id=ctx.run_id, decision=dec)
            tool = {"A": "toolX"}.get(dec, "toolY")
            r = ctx.world.commit(ctx.run_id, dec, tool)
            ctx.log.emit(type="branch.taken", logical_run_id=ctx.run_id,
                         decision=dec, tool=tool, effect_id=r["effect_id"])
            ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    REVALIDATE = False
    TARGET = "target"

    def _validate(self, ctx, after_mutation):
        r = ctx.world.get_resource(self.TARGET)
        decision = "deny" if (r is None or r["protected"]) else "allow"
        ctx.log.emit(type="validation.invoked", logical_run_id=ctx.run_id,
                     world_version=(r or {}).get("version"), protected=(r or {}).get("protected"),
                     decision=decision, after_mutation=after_mutation)
        return decision

    def run_c1rv(self, ctx):
        """approval wait, foreign mutation during the wait, then approval."""
        ctx.world.put_resource(self.TARGET, 1, False)
        p = ctx.stub.call()
        call_id = "call-" + p["proposal_id"]
        ctx.log.emit(type="proposal.presented", logical_run_id=ctx.run_id,
                     proposal_id=p["proposal_id"], call_id=call_id)
        cached = self._validate(ctx, after_mutation=False)          # V(a, S0)
        ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)

        # ---- the world moves while the human is deciding (driven by the harness) ----
        ctx.world.put_resource(self.TARGET, 2, True)
        ctx.log.emit(type="foreign.mutation", logical_run_id=ctx.run_id,
                     resource=self.TARGET, to_version=2, to_protected=True, by="harness-third-party")
        ctx.log.emit(type="approval.granted", logical_run_id=ctx.run_id,
                     for_call_id=call_id, granted_by="harness-operator")

        decision = self._validate(ctx, after_mutation=True) if self.REVALIDATE else cached
        if not self.REVALIDATE:
            ctx.log.emit(type="validation.reused_cached", logical_run_id=ctx.run_id, decision=cached)
        if decision == "allow":
            r = ctx.world.commit(ctx.run_id, call_id, p["payload"])
            ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                         effect_id=r["effect_id"], proposal_id=call_id)
        else:
            ctx.log.emit(type="effect.refused", logical_run_id=ctx.run_id, reason="deny")
        ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    def run_c1raw(self, ctx):
        """same scenario with no validation seam at all."""
        ctx.world.put_resource(self.TARGET, 1, False)
        p = ctx.stub.call()
        call_id = "call-" + p["proposal_id"]
        ctx.log.emit(type="proposal.presented", logical_run_id=ctx.run_id,
                     proposal_id=p["proposal_id"], call_id=call_id)
        ctx.log.emit(type="validation.invoked", logical_run_id=ctx.run_id, world_version=1,
                     protected=False, decision="allow", after_mutation=False)
        ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)
        ctx.world.put_resource(self.TARGET, 2, True)
        ctx.log.emit(type="foreign.mutation", logical_run_id=ctx.run_id, resource=self.TARGET,
                     to_version=2, to_protected=True, by="harness-third-party")
        ctx.log.emit(type="approval.granted", logical_run_id=ctx.run_id,
                     for_call_id=call_id, granted_by="harness-operator")
        r = ctx.world.commit(ctx.run_id, call_id, p["payload"])
        ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                     effect_id=r["effect_id"], proposal_id=call_id)
        ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    def contract_notes(self, probe):
        return {"C1-RV": dict(contract_relation="control-defined-revalidation",
                              responsibility="runtime", mitigation=None),
                "C1-RAW": dict(contract_relation="explicitly-outside-guarantee",
                               responsibility="application",
                               mitigation="revalidate-before-dispatch")}.get(probe, {})
