"""Pydantic AI adapter for card C1 / P-FOREIGN.

Documented seam under test (the library's own words):
  Tool(args_validator=...) -- "custom method to validate tool arguments after schema
  validation has passed, before execution."
  RunContext.tool_call_approved -- "Whether a tool call that required approval has now
  been approved."

So the validator is on the execution path and is reachable with tool_call_approved=True,
i.e. it is a post-approval, pre-execution validation seam.
"""
import asyncio
from .base import Adapter

from pydantic_ai import Agent
from pydantic_ai.tools import (DeferredToolRequests, DeferredToolResults, Tool, ToolApproved)
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart, ToolReturnPart
try:
    from pydantic_ai.exceptions import ToolFailed
except ImportError:                                    # older/newer naming
    from pydantic_ai.exceptions import ModelRetry as ToolFailed

try:
    from importlib.metadata import version as _v
    VER = _v("pydantic-ai")
except Exception:
    VER = "unknown"

TARGET = "target"
CALL_ID = "call-A"


class PydanticAIAdapter(Adapter):
    name = "pydantic-ai"; version = VER; population_role = "agent-runtime"

    def applicability(self):
        return dict(
            runtime="pydantic-ai", version=VER,
            supports_human_approval_boundary=True,
            supports_post_approval_revalidation_seam=True,
            supported_resume_api="Agent.run(message_history=..., deferred_tool_results="
                                 "DeferredToolResults(approvals={call_id: ToolApproved()}))",
            declared_contract="Tool(args_validator=...) docstring: 'validate tool arguments "
                              "after schema validation has passed, before execution'; "
                              "RunContext.tool_call_approved: 'Whether a tool call that required "
                              "approval has now been approved.'",
            persistence_backend="message_history (in-process for round 1; no crash injected)",
            evidence="library source: pydantic_ai/tools.py args_validator; "
                     "pydantic_ai/_run_context.py:192 tool_call_approved; "
                     "pydantic_ai/tool_manager.py:349 sets tool_call_approved=approved",
            verdict="applicable")

    def contract_notes(self, probe):
        return {
            "C1-RV": dict(contract_relation="explicit-post-approval-revalidation",
                          responsibility="runtime", mitigation=None),
            "C1-RAW": dict(contract_relation="explicitly-outside-guarantee",
                           responsibility="application",
                           mitigation="attach-an-args-validator"),
        }.get(probe, {})

    def _scenario(self, ctx, with_validator):
        world, log, run = ctx.world, ctx.log, ctx.run_id
        world.put_resource(TARGET, 1, False)
        mutated = {"done": False}

        def freshness(rc, target: str) -> None:
            r = world.get_resource(target)
            decision = "deny" if (r is None or r["protected"]) else "allow"
            log.emit(type="validation.invoked", logical_run_id=run,
                     world_version=(r or {}).get("version"),
                     protected=(r or {}).get("protected"), decision=decision,
                     after_mutation=mutated["done"], seam="args_validator",
                     tool_call_approved=bool(getattr(rc, "tool_call_approved", False)))
            if decision == "deny":
                raise ToolFailed(f"{target} is protected as of version {(r or {}).get('version')}")

        def dangerous_write(target: str) -> str:
            """Overwrite the target resource."""
            res = world.commit(run, CALL_ID, "WRITE")
            log.emit(type="effect.committed", logical_run_id=run,
                     effect_id=res["effect_id"], proposal_id=CALL_ID)
            return "written"

        tool = Tool(dangerous_write, requires_approval=True,
                    args_validator=freshness if with_validator else None)

        def model_fn(messages, info):
            done = any(isinstance(p, ToolReturnPart) or type(p).__name__ == "RetryPromptPart"
                       for m in messages for p in getattr(m, "parts", []))
            if done:
                return ModelResponse(parts=[TextPart("done")])
            return ModelResponse(parts=[ToolCallPart(tool_name="dangerous_write",
                                                     args={"target": TARGET},
                                                     tool_call_id=CALL_ID)])

        agent = Agent(FunctionModel(model_fn), tools=[tool],
                      output_type=[str, DeferredToolRequests])

        r1 = asyncio.run(agent.run("overwrite the target"))
        out = r1.output
        approvals = list(getattr(out, "approvals", []) or []) if isinstance(out, DeferredToolRequests) else []
        log.emit(type="proposal.presented", logical_run_id=run, proposal_id="A",
                 call_id=CALL_ID, pending_approvals=len(approvals),
                 output_kind=type(out).__name__)
        if not approvals:
            log.emit(type="wait.absent", logical_run_id=run,
                     note="runtime did not surface an approval request")
            log.emit(type="run.finished", logical_run_id=run)
            return
        log.emit(type="wait.entered", logical_run_id=run)

        world.put_resource(TARGET, 2, True)
        mutated["done"] = True
        log.emit(type="foreign.mutation", logical_run_id=run, resource=TARGET,
                 to_version=2, to_protected=True, by="harness-third-party")

        ids = [getattr(a, "tool_call_id", CALL_ID) for a in approvals]
        results = DeferredToolResults(approvals={i: ToolApproved() for i in ids})
        log.emit(type="approval.granted", logical_run_id=run, for_call_id=ids[0],
                 granted_by="harness-operator")

        asyncio.run(agent.run(message_history=r1.all_messages(), deferred_tool_results=results))
        log.emit(type="run.finished", logical_run_id=run)

    def run_c1rv(self, ctx):
        self._scenario(ctx, with_validator=True)

    def run_c1raw(self, ctx):
        self._scenario(ctx, with_validator=False)
