# PILOT_RESULTS.md

Pilot: `agent-runtime-invariants-pilot` · 2026-09-22 · 状态 **ENGINEERING PILOT — not a paper result**
全部表格由 `pilot/results/rows.jsonl`（33 行）生成，未手工编辑任何汇总数字。

## 1 · 控制敏感性表（由 rows.jsonl 生成）

| 探针 | 正对照（broken-control） | 负对照（correct-control） | 敏感性 |
|---|---|---|---|
| C2-R | 3/3 violated | 3/3 not-violated | PASS |
| C3-W | 3/3 violated | 3/3 not-violated | PASS |
| C3-C | 3/3 violated | 3/3 not-violated | PASS |

**闸门：正对照 100% 检出、负对照 100% 干净 → PASS。** 故真实运行时的结果可解读。

## 2 · LangGraph 逐格结果（每格 3 次，全部一致）

| 探针 | 故障点 | 判定 | contract_relation | 模型调用 | 外部效果 | 理由 |
|---|---|---|---|---|---|---|
| C2-T | `AFTER_ACK_BEFORE_NEXT_STEP` | **not-violated** | documented-task-result-replay | ['A', 'B', 'C'] | 3/3 | 3 <= budget 3 |
| C2-R | `AT_WAIT` | **not-violated** | within-documented-guarantee | ['A', 'B', 'C'] | 3/3 | 3 <= budget 3 |
| C3-W | `AT_WAIT` | **not-violated** | within-documented-guarantee | ['A'] | 1/3 | dispatched the approved proposal A |
| C3-C | `AFTER_CHECKPOINT_BEFORE_WAIT` | **not-violated** | within-documented-guarantee | ['A'] | 1/3 | branch after resume matches pre-fault decision (toolX) |
| C2-N | `AFTER_EFFECT_COMMIT_BEFORE_ACK` | **inapplicable** | explicitly-outside-guarantee | ['A', 'B', 'C', 'D'] | 4/3 | runtime explicitly places this window outside its guarantee; raw oracle said v |

## 3 · 不稳定格

**无。** 33 行中每个 (runtime, probe) 格的 3 次尝试判定完全一致（`pilot/results/stability.json`）。

## 4 · 本轮修掉的三个 harness 缺陷（都曾伪造出「违反」或伪造出「通过」）

按交付单 §19「不得把 harness 的应用层 bug 读成违反」，以下三处在出任何判定之前被查出并修正：

1. `sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread` —— 外部世界的连接被运行时的工作线程使用。`C2-T`（本轮最关键的格）因此完全没跑起来，先前记为 `NOT-CAPTURED`。修法：连接改为可跨线程并以 RLock 串行化。
2. **state schema 用了未类型化的 `StateGraph(dict)`**，导致后一节点的返回把整个 root 通道替换、丢掉先前节点写入的键。这**伪造出一个 `C3-W` 的 `violated`**（批准 A 却派发 B）。改为显式 `TypedDict` 后消失。
3. **缺少 no-fault 基线**。补上后发现 `C2-R` 与 `C3-W` 在无崩溃时也只跑到 `interrupt()` 就停——对基于 interrupt 的探针，正确基线是**同进程内恢复**。补该基线后四格全部正确（`C3-W` 只调用模型一次、派发 A、无重生成），这才 definitively 把上一条判为我的缺陷。

`INTERP` 第 2 条是本轮最重要的方法教训：**一个伪造的违反和一个真实的违反在 oracle 输出上完全一样。** 唯一能区分二者的是 no-fault 基线加上逐条外部事件流。基线现在是每个真实运行时格的前置要求。

## 4' · 更正（2026-09-22，晚于本文件）

`OBS` 本文件此前依据一次字符串检索推断「该运行时没有提供实现幂等所需的键」。**该推断证据不足且为假，已撤回。** langgraph 1.2.12 公开暴露 `langgraph.runtime.Runtime.execution_info`（`thread_id / run_id / checkpoint_id / checkpoint_ns / task_id / node_attempt`）与 `langgraph.types.CheckpointTask.id`；实测这些字段跨 SIGKILL 与跨进程恢复**全部稳定**，应用只用公开 API 即可履行被委派的幂等义务（外部效果恰好一次，正对照 3/3 报违反）。详见 `C2NI_RESULTS.md`。字符串检索只能说明没有叫那些名字的字段，不能说明没有可用的稳定身份。

## 5 · 结论

`EXP` **LangGraph 1.2.12 通过了全部四个适用格**，每格 3/3 一致，且探针在同一轮里对刻意做坏的实现 100% 报违反。

- `C2-T`（交付单指定的决定性格）：**已完成的 `@task` 在 SIGKILL 后不被重新执行**——恰好 3 次模型调用、3 个外部效果、额度 3。该运行时在自己承诺的边界上正确。
- `C2-N`：节点内非幂等副作用在 `AFTER_EFFECT_COMMIT_BEFORE_ACK` 崩溃后重复（原始 oracle 读数 4 个效果 / 额度 3），但该窗口被运行时明确置于保证之外并要求应用层幂等，故记 **`inapplicable` + `explicitly-outside-guarantee`，不进入 C2 violation 的分母**。

`INTERP` 这是**对研究主张的干净负结果**，也是按交付单 §0 的有效 pilot 结果：它证明探针不会因为看到重复执行就乱判缺陷。

## 6 · 扩展闸门（逐条对照交付单 §16）

| 条件 | 状态 |
|---|---|
| 正对照 100% 检出 | **满足**（9/9） |
| 负对照 100% 干净 | **满足**（9/9） |
| Temporal 参照行为符合预期 | **未满足——Phase B 未运行** |
| 两个真实运行时中至少一个给出决定性的适用结果 | **满足**（LangGraph 四格决定性 `not-violated`） |
| 无 oracle 依赖运行时源码 | **满足**（判定只读外部事件流与外部世界 DB） |
| 每个判定可由外部事件 + 文档化 API 行为重建 | **满足**（每行带 SHA256 manifest） |

**扩展闸门未通过**：Temporal 参照与 CrewAI 适用性闸门未做。按交付单，不得仅因 harness 能跑就扩到五个运行时。

## 7 · 对研究主张的影响（不自动更新 claim register）

`OBS` 当前证据**不支持**「systematic under-adoption」：第一个真实运行时在其文档化边界内全部正确，唯一的重复执行落在它明确声明由应用层负责的窗口。
`OPEN` 这一个负结果**不足以**触发交付单 §17 的退役条件——那要求扩展到至少五个适用的独立运行时之后再判。
`OPEN` 但它已经改变了先验：若「projection loss」是普遍现象，它应当在第一个成熟运行时的恢复面上留下痕迹，而它没有。下一步的信息量最高处因此不是再多打一个框架的恢复面，而是**换探针族**——`P-FOREIGN`（第三方在审批等待期间改世界）与 `P-MULTI`（并发写者），因为那两族对应的 C1 与 C7 才是本会话归约后仍有开放残余的卡。
