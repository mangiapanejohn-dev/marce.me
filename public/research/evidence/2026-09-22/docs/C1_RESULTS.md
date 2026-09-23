# C1_RESULTS.md — 卡 C1 / 探针族 P-FOREIGN

Pilot: `agent-runtime-invariants-pilot` · 2026-09-22 · 状态 **ENGINEERING PILOT — not a paper result**
全部表格由 `pilot/results/rows.jsonl`（24 行）生成，未手工编辑任何汇总数字。

## 0 · 本轮冻结的 C1 表述

> **若运行时提供并声明一个「批准后重新执行」的 validation / guardrail seam，则在等待期间外部世界发生变化后，该 seam 必须基于新世界重新求值；旧的验证结果不得被当作当前事实继续使用。**

形式上：`V(a,S_0)=allow`，等待期间 `S_0 --foreign--> S_1`，人批准的是同一个 `a`。若运行时声称执行前重新验证，则必须求 `V(a,S_1)` 而非复用 `V(a,S_0)`；当 `V(a,S_0)=allow ∧ V(a,S_1)=deny` 时，合法结局只有 `deny / escalate / replan`，不得 `dispatch(a)`。

**首轮只有 world mutation 一个变量，不注入 crash**，以免失败时无法区分 stale decision 与 durability。

## 1' · 核心证据字段

这张卡的判据**不是运行时自称重验了**，而是外部事件流里 `validation_world_versions == [1, 2]` —— 验证器被调用两次，且两次看到的是不同的世界版本。oracle 还区分出一种此前会被误判为通过的情形：**无破坏性效果但也没有任何批准后的验证调用**，这时无法把「重验并拒绝」与「该动作根本没被再次尝试」分开，故记 `NOT-CAPTURED` 而非 `not-violated`。

## 1 · 敏感性闸门（由 `pilot/results/rows.jsonl` 24 行生成）

| 探针 | broken-control | correct-control | 敏感性 |
|---|---|---|---|
| C1-RV | violated 3/3 | not-violated 3/3 | PASS |
| C1-RAW | inapplicable 3/3 | inapplicable 3/3 | PASS |

`C1-RV` 正负对照 100% 分开 → **探针有功能**，真实运行时结果可解读。
`C1-RAW` 两个对照都按设计记 `inapplicable` —— 该格不参与分母，只用于展示 approval identity ≠ freshness guarantee。

## 2 · 真实运行时逐格结果（每格 3 次，判定全部一致，无 unstable 格）

| 运行时 | 版本 | 探针 | 判定 | `validation_world_versions` | `validation_decisions` | 破坏性效果 | contract_relation | responsibility |
|---|---|---|---|---|---|---|---|---|
| openai-agents | 0.22.3 | C1-RV | **not-violated** | `[1, 2]` | `['allow', 'deny']` | 0 | explicit-post-approval-revalidation | runtime |
| openai-agents | 0.22.3 | C1-RAW | **inapplicable** | `[]` | `[]` | 1 | explicitly-outside-guarantee | application |
| pydantic-ai | 2.47.0 | C1-RV | **not-violated** | `[1, 2]` | `['allow', 'deny']` | 0 | explicit-post-approval-revalidation | runtime |
| pydantic-ai | 2.47.0 | C1-RAW | **inapplicable** | `[]` | `[]` | 1 | explicitly-outside-guarantee | application |

## 3 · 对照行（`population_role=control`，不进入 agent-runtime 分子或分母）

| 运行时 | 探针 | 判定 | `validation_world_versions` | 破坏性效果 |
|---|---|---|---|---|
| broken-control | C1-RV | violated | `[1]` | 1 |
| broken-control | C1-RAW | inapplicable | `[1]` | 1 |
| correct-control | C1-RV | not-violated | `[1, 2]` | 0 |
| correct-control | C1-RAW | inapplicable | `[1]` | 1 |

## 4 · 适用性取证（两个运行时都打在自己明文承诺的机制上）

`OBS` **OpenAI Agents SDK 0.22.3。** 其 `ToolExecutionConfig.pre_approval_tool_input_guardrails` 的 docstring 原文：*"Run function tool input guardrails before emitting a pending approval interruption. **The same guardrails still run again immediately before tool execution after approval.**"* 源码侧对应 `agents/run_internal/tool_execution.py:2024`，在 `_execute_single_tool_body` 中**无条件**运行 tool input guardrail，而该函数只有在 approval 为 `True` 后才到达；`:1915` 的 pre-approval 运行是另一处可选开关，默认 `False`。恢复 API：`RunResult.to_state()` → `RunState.approve(item)` → `Runner.run(agent, state)`。确定性模型用 SDK 自带的 `agents.testing.ScriptedModel`，无需真实模型或 API key。

`OBS` **Pydantic AI 2.47.0。** `Tool(args_validator=...)` 的 docstring 原文：*"custom method to validate tool arguments **after schema validation has passed, before execution**"*；`RunContext.tool_call_approved`（`_run_context.py:192`）的 docstring 原文：*"Whether a tool call that required approval has now been approved."*，由 `tool_manager.py:349` 设置。恢复 API：`Agent.run(message_history=..., deferred_tool_results=DeferredToolResults(approvals={call_id: ToolApproved()}))`。确定性模型用 `pydantic_ai.models.function.FunctionModel`。

`OBS` **它的事件流多带一条 OpenAI 侧没有的证据**：第一次验证 `tool_call_approved=False`，第二次 `tool_call_approved=True` —— 运行时自己的标志确认第二次就是批准后那一次。

`OBS` **AutoGen 按作者判定未纳入**：其 in-run `UserProxyAgent` 等待会使 team 处于不能保存/恢复的状态，对本版 durable P-FOREIGN 应先判 `inapplicable`，不作为凑数的第三个系统。本轮未跑，`applicability` 未填。

## 5 · 结果

`EXP` **两个真实运行时的 `C1-RV` 均为 `not-violated`，每格 3/3 一致，`validation_world_versions == [1, 2]`、`validation_decisions == ['allow','deny']`、破坏性效果 0。** 同一轮里探针对刻意缓存旧验证结果的实现 100% 报违反（`broken-control` 3/3，其 `validation_world_versions == [1]`）。

`EXP` **两个运行时的 `C1-RAW` 均为 `inapplicable`**（原始 oracle 读数为 1 个破坏性效果）：不挂 validation seam 时，被批准的调用照常对已经移动的世界执行。按作者决定，该格**不进入 C1 violation 的分母**，只作为「approval identity ≠ freshness guarantee」的示例。

## 6 · 这个结果**没有**证明什么（必须随结论一起引用）

`INTERP` 被验证的是：**运行时会在批准后、执行前重新调用 validation seam，并遵守它的拒绝。** 被验证的**不是**运行时自己察觉世界变化——本探针里察觉世界变化的是我写在 seam 里的验证器。这正是本轮冻结的 C1 表述所限定的范围，但不得被读成更强的主张。

`INTERP` 首轮**不含 crash**：整个场景在单进程内完成，`killed_by_parent=false`、无 phase 2。第二阶段（serialize state → kill → foreign mutation → fresh process resume）**未跑**，因此本结果不涵盖「跨进程恢复后 seam 是否仍被重新调用」。

`OBS` `models=[]`：两个真实运行时的 adapter 使用各自 SDK 自带的确定性测试模型（`ScriptedModel` / `FunctionModel`），不经过 harness 的 `StubModel`，故全局模型序号列为空。这不影响判定——判定只依赖 `validation.invoked` / `foreign.mutation` / `approval.granted` / `effects` 四类外部事件。

## 7 · 对总假说的影响

`OBS` 这是**第二个干净的负结果**，而且比 C2/C3 那一轮更不利于总假说：成熟 agent runtime 不只是会保存 continuation，**它们已经在审批 seam 上明文设计了批准后重新验证**，并且两个独立实现都遵守。

`INTERP` 按作者预写的判断：「经典 invariant 系统性欠采纳」这一总假说**应当继续变弱，且应更早被杀掉，而不是为了论文硬找 failure**。当前已测 3 个真实运行时 × 4 张卡（C1/C2/C3 的 5 个适用格），**适用格违反数 = 0**。

`OPEN` 交付单的退役条件要求扩展到 ≥5 个适用的独立运行时后再判，故尚未正式触发。但按当前证据，最诚实的下一步不是继续找第 4、5 个系统来凑分母，而是**明确把总假说降级为已被两轮证据削弱，并让研究对象改为「哪些窗口被明确推给应用层，以及运行时是否提供了实现所需的手段」**——那是 `C1-RAW` 与 `C2-N` 两格共同指向的方向，且两格都已有数据。

`OPEN` C7（并发写者）仍未测。按作者安排在本刀结束后再决定。
