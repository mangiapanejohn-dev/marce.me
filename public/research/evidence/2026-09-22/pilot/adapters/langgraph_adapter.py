"""LangGraph adapter. Uses only documented APIs: persistent SqliteSaver checkpointer,
thread_id as the logical run identity, interrupt()/Command(resume=...) for the wait
boundary, and the functional API (@entrypoint/@task) for the completed-task cell.

The adapter translates APIs. It adds NO durability semantics of its own.
"""
import os, sqlite3
from .base import Adapter
from ..fault import announce_and_wait

import langgraph
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command
from langgraph.func import entrypoint, task
from typing import Any, TypedDict


class S(TypedDict, total=False):
    budget: int
    attempts: int
    approved: bool
    finished: bool
    proposal: Any
    decision: str
    tool: str
    done: bool

try:
    from importlib.metadata import version as _v
    LGVER = _v("langgraph")
except Exception:
    LGVER = "unknown"

DURABILITY = "sync"          # the runtime's strongest documented setting


class LangGraphAdapter(Adapter):
    name = "langgraph"; version = LGVER; population_role = "agent-runtime"

    def applicability(self):
        return dict(
            runtime="langgraph", version=LGVER,
            supports_persisted_execution_state=True,
            supports_resume_same_logical_run=True,
            supports_cross_process_resume=True,
            supported_resume_api="CompiledStateGraph.invoke(None|Command(resume=...), "
                                 "{'configurable': {'thread_id': ...}}, durability='sync')",
            persistence_backend="langgraph.checkpoint.sqlite.SqliteSaver",
            evidence="documented checkpointer + thread_id resume; verified cross-process",
            verdict="applicable")

    def contract_notes(self, probe):
        return {
            "C2-R": dict(contract_relation="within-documented-guarantee", responsibility="runtime",
                         mitigation=None),
            "C3-W": dict(contract_relation="within-documented-guarantee", responsibility="runtime",
                         mitigation=None),
            "C3-C": dict(contract_relation="within-documented-guarantee", responsibility="runtime",
                         mitigation=None),
            "C2-T": dict(contract_relation="documented-task-result-replay", responsibility="runtime",
                         mitigation=None),
            "C2-NI": dict(contract_relation="delegated-obligation-closure-test",
                          responsibility="application",
                          mitigation="idempotency-key-from-public-execution_info"),
            "C2-N": dict(contract_relation="explicitly-outside-guarantee", responsibility="application",
                         mitigation="idempotency-key-or-result-check"),
        }.get(probe, {})

    # ---------- plumbing ----------
    def _saver(self, ctx):
        c = sqlite3.connect(os.path.join(ctx.statedir, "lg_checkpoints.sqlite"),
                            check_same_thread=False, timeout=30)
        return SqliteSaver(c)

    def _cfg(self, ctx):
        return {"configurable": {"thread_id": ctx.run_id}, "recursion_limit": 100}

    # ============ C2-R : budget across a supported wait boundary ============
    def run_c2r(self, ctx):
        def consume(state):
            if state.get("budget", 0) <= 0:
                return {"finished": True}
            p = ctx.stub.call()
            r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
            ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                         effect_id=r["effect_id"], proposal_id=p["proposal_id"],
                         budget_remaining_runtime_view=state["budget"] - 1)
            return {"budget": state["budget"] - 1, "attempts": state.get("attempts", 0) + 1}

        def approve(state):
            ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)
            interrupt({"question": "continue?"})       # documented wait boundary
            return {"approved": True}

        def route(state):
            if state.get("finished") or state.get("budget", 0) <= 0: return END
            if state.get("attempts", 0) >= 4: return END
            if state.get("attempts", 0) == 2 and not state.get("approved"): return "approve"
            return "consume"

        g = StateGraph(S)
        g.add_node("consume", consume); g.add_node("approve", approve)
        g.set_entry_point("consume")
        g.add_conditional_edges("consume", route)
        g.add_edge("approve", "consume")
        app = g.compile(checkpointer=self._saver(ctx))
        cfg = self._cfg(ctx)
        if ctx.phase == 1:
            app.invoke({"budget": ctx.budget, "attempts": 0, "approved": False},
                       cfg, durability=DURABILITY)
            announce_and_wait(ctx.marker, "AT_WAIT", ctx.log)
        else:
            app.invoke(Command(resume="APPROVE"), cfg, durability=DURABILITY)
            ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    # ============ C3-W : proposal identity across a human wait ============
    def run_c3w(self, ctx):
        def propose(state):
            p = ctx.stub.call()
            ctx.log.emit(type="proposal.presented", logical_run_id=ctx.run_id,
                         proposal_id=p["proposal_id"])
            return {"proposal": p}

        def gate(state):
            ctx.log.emit(type="wait.entered", logical_run_id=ctx.run_id)
            interrupt({"approve": state["proposal"]["proposal_id"]})
            return {"approved": True}

        def dispatch(state):
            p = state.get("proposal")
            if p is None:
                p = ctx.stub.call()
                ctx.log.emit(type="proposal.regenerated", logical_run_id=ctx.run_id,
                             proposal_id=p["proposal_id"])
            r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
            ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                         effect_id=r["effect_id"], proposal_id=p["proposal_id"])
            return {"done": True}

        g = StateGraph(S)
        for n, f in (("propose", propose), ("gate", gate), ("dispatch", dispatch)):
            g.add_node(n, f)
        g.set_entry_point("propose"); g.add_edge("propose", "gate")
        g.add_edge("gate", "dispatch"); g.add_edge("dispatch", END)
        app = g.compile(checkpointer=self._saver(ctx)); cfg = self._cfg(ctx)
        if ctx.phase == 1:
            app.invoke({}, cfg, durability=DURABILITY)
            announce_and_wait(ctx.marker, "AT_WAIT", ctx.log)
        else:
            app.invoke(Command(resume="APPROVE"), cfg, durability=DURABILITY)
            ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    # ============ C3-C : replay closure for a model decision ============
    def run_c3c(self, ctx):
        def decide(state):
            d = ctx.stub.call()
            ctx.log.emit(type="decision.recorded", logical_run_id=ctx.run_id,
                         decision=d["decision"])
            return {"decision": d["decision"]}

        def branch(state):
            # fault point is here: node "decide" has COMPLETED and, under durability=sync,
            # its state was persisted before this step started.
            if ctx.phase == 1:
                announce_and_wait(ctx.marker, "AFTER_CHECKPOINT_BEFORE_WAIT", ctx.log)
            dec = state.get("decision")
            if dec is None:
                d = ctx.stub.call(); dec = d["decision"]
                ctx.log.emit(type="decision.regenerated", logical_run_id=ctx.run_id, decision=dec)
            tool = {"A": "toolX"}.get(dec, "toolY")
            r = ctx.world.commit(ctx.run_id, dec, tool)
            ctx.log.emit(type="branch.taken", logical_run_id=ctx.run_id, decision=dec,
                         tool=tool, effect_id=r["effect_id"])
            return {"tool": tool}

        g = StateGraph(S)
        g.add_node("decide", decide); g.add_node("branch", branch)
        g.set_entry_point("decide"); g.add_edge("decide", "branch"); g.add_edge("branch", END)
        app = g.compile(checkpointer=self._saver(ctx)); cfg = self._cfg(ctx)
        app.invoke({} if ctx.phase == 1 else None, cfg, durability=DURABILITY)
        ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)

    # ==== C2-T : does a COMPLETED @task re-execute after a crash before the next boundary? ====
    def run_c2t(self, ctx):
        world, log, stub, run = ctx.world, ctx.log, ctx.stub, ctx.run_id

        @task
        def consume_task(i: int):
            p = stub.call()
            r = world.commit(run, p["proposal_id"], p["payload"])
            log.emit(type="effect.committed", logical_run_id=run, effect_id=r["effect_id"],
                     proposal_id=p["proposal_id"], task_ordinal=i)
            return {"effect_id": r["effect_id"], "proposal_id": p["proposal_id"]}

        saver = self._saver(ctx)
        phase, marker, budget = ctx.phase, ctx.marker, ctx.budget

        @entrypoint(checkpointer=saver)
        def flow(inp):
            got = []
            for i in range(1, 3):
                got.append(consume_task(i).result())
            log.emit(type="tasks.completed", logical_run_id=run, n=len(got))
            if phase == 1:
                # completed tasks have returned; the entrypoint has NOT finished
                announce_and_wait(marker, "AFTER_ACK_BEFORE_NEXT_STEP", log)
            if budget - len(got) > 0:
                got.append(consume_task(3).result())
            return {"effects": got}

        cfg = self._cfg(ctx)
        flow.invoke({} if phase == 1 else None, cfg, durability=DURABILITY)
        log.emit(type="run.finished", logical_run_id=run)

    # ==== C2-NI : can the APPLICATION discharge the delegated idempotency obligation
    #              using only the runtime's public API? ====
    def run_c2ni(self, ctx):
        """Same window as C2-N, but the application implements the mitigation the runtime
        documents (an idempotency key), sourcing identity ONLY from the public
        langgraph.runtime.Runtime.execution_info surface. No checkpoint DB is read and no
        runtime code is modified."""
        import uuid
        from langgraph.runtime import get_runtime
        world, log, run = ctx.world, ctx.log, ctx.run_id
        mode = os.environ.get("PILOT_IDEM_MODE", "stable")   # stable | unstable(pos. control)

        @task
        def effectful(i: int):
            info = get_runtime().execution_info
            snap = {k: getattr(info, k, None) for k in
                    ("thread_id", "run_id", "checkpoint_id", "checkpoint_ns",
                     "task_id", "node_attempt")}
            if mode == "stable":
                key = f"{snap['thread_id']}|{snap['checkpoint_ns']}|{snap['task_id']}|{i}"
            else:
                key = f"unstable|{uuid.uuid4()}"
            log.emit(type="execution_info.read", logical_run_id=run, attempt_pid=os.getpid(),
                     idempotency_key=key, key_mode=mode,
                     **{f"ei_{k}": (str(v) if v is not None else None) for k, v in snap.items()})

            hit = world.idem_lookup(key)
            log.emit(type="idem.lookup", logical_run_id=run, idempotency_key=key,
                     hit=bool(hit), before_effect=True)
            if hit:
                log.emit(type="effect.reused", logical_run_id=run,
                         effect_id=hit["effect_id"], proposal_id=key)
                return {"effect_id": hit["effect_id"], "reused": True}

            p = ctx.stub.call()
            eid, reused = world.idem_commit(run, key, p["payload"], "written")
            log.emit(type="effect.committed", logical_run_id=run, effect_id=eid,
                     proposal_id=key, reused=reused)
            if ctx.phase == 1:
                # process dies after the external effect, before the task is acknowledged
                announce_and_wait(ctx.marker, "AFTER_EFFECT_COMMIT_BEFORE_ACK", log)
            return {"effect_id": eid, "reused": reused}

        saver = self._saver(ctx)
        phase = ctx.phase

        @entrypoint(checkpointer=saver)
        def flow(inp):
            r = effectful(1).result()
            log.emit(type="tasks.completed", logical_run_id=run, n=1)
            return {"effect": r}

        flow.invoke({} if phase == 1 else None, self._cfg(ctx), durability=DURABILITY)
        log.emit(type="run.finished", logical_run_id=run)

    # ==== C2-N : non-idempotent effect inside a node, crash mid-node (outside the guarantee) ====
    def run_c2n(self, ctx):
        def consume(state):
            if state.get("budget", 0) <= 0: return {"finished": True}
            p = ctx.stub.call()
            r = ctx.world.commit(ctx.run_id, p["proposal_id"], p["payload"])
            ctx.log.emit(type="effect.committed", logical_run_id=ctx.run_id,
                         effect_id=r["effect_id"], proposal_id=p["proposal_id"])
            n = state.get("attempts", 0) + 1
            if ctx.phase == 1 and n == 2:
                announce_and_wait(ctx.marker, "AFTER_EFFECT_COMMIT_BEFORE_ACK", ctx.log)
            return {"budget": state["budget"] - 1, "attempts": n}

        def route(state):
            return END if (state.get("finished") or state.get("budget", 0) <= 0
                           or state.get("attempts", 0) >= 4) else "consume"

        g = StateGraph(S)
        g.add_node("consume", consume); g.set_entry_point("consume")
        g.add_conditional_edges("consume", route)
        app = g.compile(checkpointer=self._saver(ctx)); cfg = self._cfg(ctx)
        app.invoke({"budget": ctx.budget, "attempts": 0} if ctx.phase == 1 else None,
                   cfg, durability=DURABILITY)
        ctx.log.emit(type="run.finished", logical_run_id=ctx.run_id)
