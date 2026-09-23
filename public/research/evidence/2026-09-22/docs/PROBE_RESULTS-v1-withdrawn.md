# Probe Results — 第 1 个运行时

研究负责人：Claude Science · 2026-09-22 · taxonomy 冻结后的第一批探针
被测：**langgraph 1.2.12**（PyPI）· 参照实现：**temporalio 1.33.0** · 卡：`C2` durable consumption、`C3` replay-state closure

## 0 · 方法（三条决定都会进论文方法节）

1. **崩溃是真实的独立进程终止**：`os._exit(9)`，不走任何清理或 flush 路径。两个阶段是两个 OS 进程，共享同一个 sqlite checkpoint 文件与同一 `thread_id`。
2. **oracle 的判据取自运行时之外的审计文件**，不取运行时自述。这一条在本轮就产生了差异（见 §1.2）。
3. **每张卡同时跑正负对照**，且结果报五态。正对照未触发时，该格的「无违反」**不计入**。
4. 驱动用确定性节点函数，不用真实模型——本研究**不主张**任何关于模型行为的结论。

## 1 · C2 · durable consumption / semantic replay

额度 3，消费第 2 次时崩溃，恢复后继续。两个崩溃窗口 × 三档 `durability` × {预算存 checkpoint 状态（被测）, 预算存进程内存（正对照）}。

| 角色 | 崩溃窗口 | durability | 外部事件数 | 外部审计序列 | 判定 |
|---|---|---|---|---|---|
| 被测 | 节点中途（副作用后） | **sync** | **4** | `[1, 2, 2, 3]` | **VIOLATED** |
| 被测 | 节点中途（副作用后） | async | **4** | `[1, 2, 2, 3]` | **VIOLATED** |
| 被测 | 节点中途（副作用后） | exit | 2 | `[1, 2]` | inapplicable |
| 被测 | 下一节点入口 | sync | 3 | `[1, 2, 3]` | not-violated |
| 被测 | 下一节点入口 | async | 3 | `[1, 2, 3]` | **probe-insensitive** |
| 被测 | 下一节点入口 | exit | 1 | `[1]` | inapplicable |
| 正对照 | 节点中途 | sync / async | 5 | `[1, 2, 1, 2, 3]` | **VIOLATED** ✓ |
| 正对照 | 下一节点入口 | sync / async | 4 | `[1, 1, 2, 3]` | **VIOLATED** ✓ |
| 负对照 | 无崩溃 | sync | 3 | `[1, 2, 3]` | not-violated ✓ |

**探针敏感性**：正对照在 sync/async 四格全部报违反 → 探针有功能。负对照干净 → 无假阳性。**故本轮的 `not-violated` 与 `VIOLATED` 都可采信。**

### 1.1 主结果

`EXP` **在该运行时最强的 durability 档（`sync`）下，节点内崩溃使该节点在恢复时被重新执行，其外部副作用重复一次。** 一次性额度为 3，外部审计记录 4 次消费，且 `n=2` 出现两次。

`IMPL` 机制在文档里就能读到：`sync` 的承诺是 *"Changes are persisted synchronously **before the next step starts**"*——即在节点**完成之后**。三档（`sync`/`async`/`exit`）控制的都只是「节点完成后的状态何时落盘」，**没有一档使节点的外部效果恰好一次**。

### 1.2 自述与外部审计不一致（方法决定 2 的直接回报）

`EXP` 同一次运行里，运行时自述最终状态为 `{"spent": 3, "limit": 3, "done": true}`——**按它自己的账本，额度没有超支**。而外部审计文件记录了 4 次消费。若 oracle 采信运行时自述，本违反**不可见**。

### 1.3 `exit` 档：响亮失败，不是静默失败

`EXP` `durability="exit"` 下 checkpoint 表为 0 行 0 写入，恢复时抛 `EmptyInputError: Received no input for __start__`。这是文档化的取舍且失败响亮，故记 `inapplicable` 而非违反。**我起初差点写成「静默不恢复」，实测否证了这一点。**

### 1.4 `probe-insensitive` 一格的诚实处理

`OBS` 下一节点入口崩溃在 `async` 下得到正确序列 `[1,2,3]`。但异步持久化可能在我的崩溃点之前就已落地，**我无法区分「async 在此窗口安全」与「我的崩溃点错过了竞态窗口」**。按预注册规范记 `probe-insensitive`，不记 `not-violated`。要判定这一格需要在持久化线程内插桩，那已不是黑盒。

## 2 · C3 · replay-state closure

| 配置 | 恢复后行为 | 判定 |
|---|---|---|
| 值入 checkpoint 状态（被测） | 值正确保留（`used_value: v-31876`，走 `known` 分支）；**但 `external_write` 重复一次** | 值的重放封闭性 not-violated；**效果恰好一次 VIOLATED** |
| 值存进程内存（正对照） | 值丢失 → `used_value: null` → 分支由 `known` 变为 `fallback` | **VIOLATED** ✓ |

`INTERP` C3 把 C2 的结果分解成两个可分离的性质：**非确定值本身的持久化是被支持的**（入 checkpoint 即可），而**外部效果的恰好一次不被支持**。正对照证明探针能检出前者的失败，所以后者的失败不是探针假阳性。

## 3 · 机制对照（白盒，仅作解释，不作判定依据）

| 词族 | langgraph 1.2.12 | temporalio 1.33.0 |
|---|---|---|
| `exactly.once` / `at.least.once` / `idempoten` / `dedup` | 45 命中，**全部是 channel write 与 streamed message 的内部去重** | 42 命中，含明文 *"exactly-once delivery"*、*"at-least-once dedup"*、*"idempotent"* |
| `idempotency_key` / `dedupe_key` / `effect_id` / `operation_id` | **0 命中** | 有 |

`INTERP` 这正是 `C2` 卡的经典祖先所要求的那件东西：效果边界上的持久去重键。durable execution 引擎有，该 agent runtime 没有——它的去重只发生在内部通道层。
`OBS` **口径**：这是安装包内 `*.py` 的字符串检索，不是 API 语义核验；`0 命中` 只说明**没有以这些名字出现的概念**，不排除以别的名字实现。定稿前须逐 API 核。首次检索因命名空间包导致路径解析为空、得到虚假的「0 命中」，已重做（`110` 个 py 文件）。

## 4 · 对主结论的贡献与尚缺的

`INTERP` 这是 taxonomy 冻结后的**第 1 个独立运行时、第 1 张卡**，形态符合预注册的支持条件之一：信息与机制在生态里存在（temporalio），在 agent runtime 的跨层组合处缺失，修复只需效果边界的去重键而不是新算法。
`OPEN` 预注册的支持条件要求 **≥3 个独立 runtime × ≥3 张不同的卡**。当前是 1×2。**结论尚不成立，不得据此写任何跨系统主张。**
`OPEN` 一个必须回答的反论点：at-least-once + 要求步骤幂等，可能是该运行时**明示的契约**。§3 的检索表明它没有提供实现幂等所需的键，但我尚未核其官方文档是否显式声明该契约。**若它显式声明，则本格应从 `VIOLATED` 改判为 `by-design`，而主张改为「契约把责任推给用户且不提供实现手段」——那是更弱但仍可测的主张。** 这是下一步的第一件事。
