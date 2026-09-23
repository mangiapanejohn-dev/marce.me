# PILOT_APPLICABILITY.md

Pilot: `agent-runtime-invariants-pilot` · 2026-09-22 · 状态 **ENGINEERING PILOT — not a paper result**

## LangGraph

```json
{
  "runtime": "langgraph",
  "version": "1.2.12",
  "card": "C2 | C3",
  "supports_persisted_execution_state": true,
  "supports_resume_same_logical_run": true,
  "supports_cross_process_resume": true,
  "supported_resume_api": "CompiledStateGraph.invoke(None | Command(resume=...), {'configurable': {'thread_id': ...}}, durability='sync'); functional API: entrypoint.invoke(None, cfg)",
  "persistence_backend": "langgraph.checkpoint.sqlite.SqliteSaver",
  "evidence": "崩溃后由全新解释器以同一 thread_id 恢复并继续同一 logical run；33 行 rows.jsonl 中 killed_by_parent=true 且 phase1_returncode=-9（SIGKILL）；oracle 由两个不同 process_id 确认跨进程恢复",
  "verdict": "applicable"
}
```

## Temporal（参照，未运行）

`population_role: "reference"`。Phase B 尚未执行。**不进入 agent-runtime 主张的分子或分母。**

## CrewAI Flow（未运行）

Phase D 尚未执行。适用性闸门未做——按交付单，若安装包未暴露「在全新进程中续跑同一个已挂起的 logical execution」的受支持路径，则硬崩溃格记 `inapplicable`，且**不得**用自建 SQLite checkpoint 层替代。

## 未做的格

`C2-A`（ack-loss）按交付单要求在前三格稳定后才跑，本轮未跑。`P-CTXRESET`、`P-FOREIGN`、`P-MULTI` 探针族本轮未实现。


---

## 卡 C1 / P-FOREIGN 的适用性（2026-09-22）

机器可读版本：`pilot/results/applicability_c1.json`（由每个 adapter 的 `applicability()` 生成）。

| 运行时 | 版本 | 审批边界 | 声明的批准后重验 seam | 恢复 API | 判定 |
|---|---|---|---|---|---|
| openai-agents | 0.22.3 | 是（`ToolApprovalItem` 中断） | 是 — `ToolExecutionConfig` docstring：*"The same guardrails still run again immediately before tool execution after approval."* | `RunResult.to_state()` → `RunState.approve(item)` → `Runner.run(agent, state)` | **applicable** |
| pydantic-ai | 2.47.0 | 是（`DeferredToolRequests.approvals`） | 是 — `Tool(args_validator=...)` docstring：*"after schema validation has passed, before execution"*；`RunContext.tool_call_approved` | `Agent.run(message_history=..., deferred_tool_results=DeferredToolResults(approvals=...))` | **applicable** |
| autogen | — | run 内 `UserProxyAgent` 等待使 team 处于不能保存/恢复的状态 | — | — | **inapplicable（按作者判定，未跑）** |

确定性模型均用各 SDK 自带设施（`agents.testing.ScriptedModel` / `pydantic_ai.models.function.FunctionModel`），不需真实模型或凭据。

**环境**：`probe-openai-agents-c1`、`probe-pydantic-ai-c1`，与 `probe-langgraph` 完全隔离。`socksio` 为纯环境修复——沙箱导出 SOCKS 代理变量，OpenAI SDK 的追踪 exporter 在导入时构造 httpx 客户端因此失败；追踪与本卡无关。
