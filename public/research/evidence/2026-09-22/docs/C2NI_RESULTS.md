# C2NI_RESULTS.md — Delegated Obligation Closure（LangGraph C2-N kill test）

Pilot: `agent-runtime-invariants-pilot` · 2026-09-22 · 状态 **ENGINEERING PILOT — not a paper result**
表格由 `pilot/results/rows.jsonl` 与 `pilot/results/runs/*/events.jsonl` 生成，未手工编辑汇总数字。

## 0 · 被检验的命题

> **当运行时明确把一个 correctness obligation 交给应用时，它是否同时暴露了足够的稳定机制，使应用能在该运行时自己的 replay / resume 语义下真正履行它？**

判据：`delegates(R, O) ⇒ ∃ M_R : M_R 足以履行 O`，且 `M_R` 必须全部来自**公开、文档化 API**。三项能力条件全真则 `closed`，缺任一则 `open`：

| 条件 | 含义 |
|---|---|
`stable_identity` | replay 前后能识别同一 logical effect
`boundary_access` | 应用在 effect 之前有机会施加 mitigation
`durable_reconciliation` | 应用能查询已提交结果

**不使用 LOC 作指标**，只测能力。

## 1 · 首先必须撤回我自己的一条断言

`OBS` **撤回**：上一轮我写「LangGraph 要求应用层幂等，却不提供实现幂等所需的键」。该断言的**唯一依据是一次字符串检索**（`idempotency_key|dedupe_key|effect_id|operation_id` 在包内 0 命中）。那只能说明**没有叫这些名字的字段**，不能说明**没有可用的稳定身份**。证据不足，判断为假。

`IMPL` 已装的 **langgraph 1.2.12** 公开暴露 `langgraph.runtime.Runtime.execution_info`（`ExecutionInfo` 的 docstring：*"Read-only execution info/metadata for the execution of current thread/run/node."*），字段为 `checkpoint_id, checkpoint_ns, task_id, thread_id, run_id, node_attempt, node_first_attempt_time`，经公开的 `get_runtime()` 取用。`langgraph.types.CheckpointTask` 亦公开带 `id`。

## 2 · 方法

同 `C2-N` 的窗口——外部效果已提交、task 尚未被确认时进程死亡——但应用按运行时自己推荐的模型实现 mitigation：

```
key = f"{thread_id}|{checkpoint_ns}|{task_id}|{i}"      # 只来自公开 execution_info
hit = store.idem_lookup(key)                             # 外部效果库
if hit: return hit                                       # 复用已提交结果
else:   store.idem_commit(key, payload)                  # 原子 check-and-commit
```

约束全部满足：**只用公开 API**（不读 checkpoint DB、不 patch 运行时）、**不依赖真实 LLM**（harness 的确定性 stub）、**外部 audit oracle**（判定只读外部事件流与外部效果库）。`key` 的唯一性由外部库以 `PRIMARY KEY` + `BEGIN IMMEDIATE` 强制，不由调用方自检。

**正对照**：同一探针的 `unstable` 模式，键每次由 `uuid4()` 新生成。若它不报违反，则「只提交一次」无法与「oracle 没功能」区分。

## 3 · 结果（每模式 3 次，判定全部一致）

| 模式 | 判定 | 外部效果数 | task 尝试数 | 进程数 | `stable_identity` | `boundary_access` | `durable_reconciliation` | **dischargeable** |
|---|---|---|---|---|---|---|---|---|
| `stable`（被测） | **not-violated** | **1** | 2 | 2 | True | True | True | **True** |
| `unstable`（正对照） | **violated** | 2 | 2 | 2 | False | True | False | False |

正对照 3/3 报违反 → **oracle 能检出未闭合**，故被测格的 `not-violated` 可采信。

### 3.1 逐条外部事件（`stable` 模式）

```
pid 70399  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…
pid 70399  idem.lookup           hit=False   before_effect=True
pid 70399  effect.committed
pid 70399  faultpoint.reached    AFTER_EFFECT_COMMIT_BEFORE_ACK      ← 父进程 SIGKILL
pid 70400  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…   ← 逐字节相同
pid 70400  idem.lookup           hit=True    before_effect=True
pid 70400  effect.reused
pid 70400  tasks.completed
```

### 3.2 逐字段稳定性（这一节才是机制证据）

`EXP` 跨 SIGKILL 与跨进程恢复边界，快照的**六个字段全部稳定**（3 次运行一致）：

| 字段 | 跨边界 |
|---|---|
`thread_id` | STABLE
`run_id` | STABLE
`checkpoint_id` | STABLE
`checkpoint_ns` | STABLE
`task_id` | STABLE
`node_attempt` | STABLE

`OBS` 其中两项与我的预期相反：`run_id` 在第二次 `invoke` 后**没有**改变，`node_attempt` 在重试后**也没有**递增。这对结论是加强——应用不必挑选字段即可得到稳定键。逐行数据见 `execution_info_field_stability.csv`。

## 4 · 结论

`EXP` **delegated obligation is dischargeable。** 在 LangGraph 1.2.12 上，应用只用公开 API 即可在其 replay 语义下履行运行时委派的幂等义务：三项能力条件全真，跨崩溃恢复后外部效果恰好一次。

`INTERP` 因此「运行时把正确性责任推给应用但不给履行手段」这一候选方向**当轮被杀**。剩下的只是一个被 End-to-End Arguments（Saltzer, Reed & Clark, 1984，其典型例子正是 duplicate suppression 与 delivery acknowledgement）覆盖的正常分层选择。

## 5 · 边界（必须随结论引用）

`OBS` 单一运行时、单一窗口（`AFTER_EFFECT_COMMIT_BEFORE_ACK`）、单一 task。**未测**：多资源效果、并发写者下的同键竞争、非 task 路径（节点内联效果）是否也能取到同样稳定的身份。
`OBS` `checkpoint_id` 在本窗口稳定，是因为恢复自同一 checkpoint；若恢复已推进过 checkpoint 则不应假定其稳定。键里真正承载逻辑位置的是 `checkpoint_ns` 与 `task_id`。
`OBS` 外部库的原子性由我实现（SQLite `PRIMARY KEY` + `BEGIN IMMEDIATE`）。本测试证明**运行时提供了足以构造稳定键的信息**；它不证明任意外部系统都提供条件写原语——那是 effect 目标侧的性质，与运行时无关。

## 6 · 研究阶段的收束

`OBS` 累计证据：

| 卡 | 机制 | 运行时数 | 适用格违反数 |
|---|---|---|---|
C1 | 明文 post-approval revalidation seam | 2 | **0** |
C2 | 文档化 durable 边界（完成的 task 不重执行） | 1 | **0** |
C3 | replay 状态封闭性 | 1 | **0** |
C2-NI | 被委派义务的可履行性 | 1 | **0**（closed）

`INTERP` 按作者预注册的决定：本刀 PASS ⇒ **停止沿 correctness-under-adoption 这条线继续挖，包括暂不做 C7**。理由是再换 subsystem 很容易变成「为了找到一个失败而换 subsystem」。

`INTERP` 本阶段最有价值的结论是一个**负结果**：我们连续提出多个「agent runtime 可能重新犯经典系统错误」的假说，但在把**契约、适用范围、应用责任、公开 mitigation 机制**四者分开之后，大部分 apparent violations 消失了。这些消失**不是**测量不敏感造成的——每一格都有 100% 检出的正对照。

`OPEN` 该负结果可作研究方法材料保留，**不宜硬做主论文**。
