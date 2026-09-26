# RESEARCH_DIRECTION_DISCOVERY.md

研究负责人：Claude Science · 2026-09-22 · 仓库 HEAD `5e0843a` · 语料 104 journal / 3,653 事件 / 20 个事件类型

**结论提前给出：`NO PRIMARY THESIS YET`，且本轮没有任何候选达到 `SYSTEMS CANDIDATE`。** 依据在 §C–§F。这不是没找到，是找到的都被杀掉了，而且大部分死在本轮的新测量上。

## A. Search record

**被读取的系统与材料**（全部只读）：42 份 ADR（`docs/adr/0001`–`0046`，含交叉引用与 supersede/amend 关系抽取）；104 个 journal 的全事件流；`docs/research/results.jsonl`（272 行 / 33 个 exp）；`FTR_FRONTIER_RESEARCH.md`（含 §7 三层协议）、`ftr-workstreams/W2.md`、kickoff §4；本会话自有的 20 份研究与 pilot 产物。

**被检查的理论域**：capability systems / authorization（designation vs authority）；fault tolerance（rollback-recovery、output commit、livelock）；self-adaptive systems（MAPE-K 反馈环）；runtime verification（三值裁决、monitorability）；planning（contingent / conformant / knowledge preconditions）；POMDP 与 belief-state 充分统计量；safe RL（部分可观测下的 shielding）；databases（视图自维护性、OCC、条件写）；provenance / event sourcing；reproducibility standards。

**被打过的真实第三方运行时**（今日 pilot，非本轮新增）：langgraph 1.2.12、openai-agents 0.22.3、pydantic-ai 2.47.0，参照实现 temporalio 1.33.0。

**本轮新测量**（cheap kill gates，顺序严格按 §7：source census → existing logs → retrospective corpus）：ADR 反转图谱、run 级结局普查、放弃原因分布、诊断/恢复配对、提案处置追踪、目标修订普查、批准载荷检查、一次因果链检验。**没有写任何系统代码。**

## B. Raw phenomenon inventory（20 条）

标记 `[新]` = 本轮首次测量；`[旧]` = 本会话早先测量，有 artifact 支撑。

| # | Observed phenomenon | Concrete evidence | Why surprising | Cheapest falsifier |
|---|---|---|---|---|
1 `[新]` | 放弃比完成更常见 | `goal.abandoned` **81** vs `goal.completed` **55** / 104 journal | 一个以「先看后改 + 门控」为核心的运行时，最常见终局是放弃 | 分解放弃原因（已做，见 2/3/7） |
2 `[新]` | **三分之一的放弃是基础设施故障，却被记成 agent 卡死** | 73 个 `stop:"stuck"` 中 **26** 条原因为 `transport-failed`（claude CLI 180s 未答 / port 调用上限） | 终局分类把 harness 故障映射进行为类别；任何「agent 卡住」的统计被污染 ~32% | 看原因字符串（已做） |
3 `[新]` | 重复读守卫是最大的单一放弃原因 | 34/81：「fs.observe was already read in this run with the same arguments, and the proposer asked for it again」 | — | — |
4 `[新]` | 诊断→恢复是固定 1:1 表，且**恢复结局从不记录** | 4 类诊断 → 3 种恢复：`InsufficientEvidence→REOBSERVE` 19、`VerificationMismatch→REPLAN_FRONTIER` 11、`ActionRejected→{CHANGE_CAPABILITY 6, REPLAN_FRONTIER 6}`、`StaleObservation→REOBSERVE` 3；20 个事件类型中**没有任何恢复结局类型** | 运行时尝试恢复 45 次，无法知道恢复是否有效 | 枚举事件类型（已做） |
5 `[新]` | 恢复处方与进度守卫指向同一动作 | `REOBSERVE` 被处方 22/45 次（「look again first」），而 34 次放弃的判据是「同参数重复读」 | 两个子系统各自正确，复合可能互相拆台 | 因果链检验（已做 → **否**，见 §C） |
6 `[新]` | 提案不带 capabilityId；能力靠**词项重合**事后路由 | `intent` 键为 `{id, goalId, desiredEffect, expected, target, parameters, preconditions…}`；`no-route` 原因原文「10 capability/capabilities were the right effect class but **shared no term with the described need**」 | 开放词汇的意图与封闭词汇的能力之间是词法匹配 | 查批准载荷展示什么（已做 → **无缺口**，见 §C） |
7 `[新]` | 路由可跨到与会话不同的 provider | 6/81 放弃：「"repo.diff" belongs to provider "mobius.repo" but the request names a session owned by "mobius.filesystem"」 | 能力解析与会话归属是两套命名空间 | 属 ADR 0008/0012 已知的身份纪律 |
8 `[新]` | 批准载荷是**已解析的**能力与字节，不是散文 | `authority.escalated.report.effect` 带 `capabilityId`、`effectClass`、`semanticEffect`、逐字 `occurrence`、`resourceBindings[{resource, sha256, fromObservation}]` | 与 6 相反方向：designation/authority 缺口**不存在** | 读载荷（已做） |
9 `[新]` | 读提案与写提案的可追踪性严重不对称 | 221/245 读提案在其后无任何事件引用其 `intent.id`；写提案仅 29/172 | append-only journal 的 fold 能回答「这个写发生了什么」，通常回答不了「这个读发生了什么」 | 源码核对观察是否按设计不回填 intent id |
10 `[新]` | 规格在执行中**不**变异 | 159 个 `goal.created` 的 `revisedBecause` **全部为空**；相邻 `goal.created` 的 `successCriteria` 变化 **0 次** | 反直觉的干净：55/104 journal 有多次 goal.created 但标准集恒等 | 已做 |
11 `[新]` | `task.changed`（196 事件 / 69 run）是状态转移记录 | 两个样例 `description` 逐字相同，变的是 `status`（active→verified）与 `dependsOnEvidence` | 高频但语义平凡；曾被我误读为规格变异 | 已做 |
12 `[新]` | run 长度与完成率非单调且有悬崖 | 事件数 0–39: 54.1%（n=74）· 40–79: **81.2%**（n=16）· 80–119: 20.0%（n=10）· 120–159: **0%**（n=4） | 看似相变 | 反向因果与 n 太小 |
13 `[新]` | 七天内 13 条 ADR 全在收窄同一个关系 | `0021`–`0046`：look-before-change、read-as-read、judged-against-observed、criterion-judged-on-world、runtime-looks-where-model-did-not、judge-sees-what-run-has-seen、a-look-that-cannot-evaluate…；`0046` 明文 replaces `0031` 的绑定规则（对修正的修正）；另 `0030`/`0033` 双双修散文→能力路由；`0037`–`0040` 两天内四条互相 supersede | 一个关系需要 13 次修正 | 能否证明该关系是 ill-posed（早先已测：闭合 provider 上可静态判定 → 工程） |
14 `[旧]` | 证据**数量**不区分可判定性，**指称覆盖**才区分 | cannot-tell 绑 2.43 条 / established 2.48；而覆盖标准所指：66% vs 93% | — | 已做（三臂重判） |
15 `[旧]` | 确定性是分层的 | 能力序列众数占比 0.923，能力+实参 0.795；提案数 CV=0 的两个任务其内容层众数仅 0.667 | 同样的审议量、不同的写入内容 | n=3 → 需 n=10 |
16 `[旧]` | 13% 的带路径断言在闭合 provider 上静态不可解析 | 1,345 条中 181 条；提议者自发写的 JSONPath filter 语法**全部**落在不可解析集 | 规格语言的可寻址性与观察 schema 不共延 | 已做（静态分析） |
17 `[旧]` | 两个独立运行时把同一个不可避免状态解成相反方向 | 一个 fail-closed 付活性；另一个无第三种裁决、提示要求「假定 agent 的抽取正确」→ fail-open | 跨系统同构失败 | 已在退役清单内 |
18 `[旧]` | 一个文档化选项的恢复路径不可用；身份字段跨崩溃不变 | langgraph `durability="exit"`：恢复抛 `EmptyInputError`、checkpoint 表 0 行；`run_id` 与 `node_attempt` 跨 SIGKILL/跨进程**均不变** | 应用无法仅凭 `execution_info` 区分首次执行与重执行 | 已做（逐字段稳定性表） |
19 `[旧]` | 成熟运行时在适用格上零违反 | C1/C2/C3/C2-NI 四张卡 × 3 个真实运行时，适用格违反数 **0**，每格正对照 100% 检出 | 「经典错误被重犯」的先验被削弱 | 已做 |
20 `[旧]` | 语料按构造产生不出判决性并发情形 | 注入的外部变更从不是目标状态；误归属改变完成判定的实例 0 | 缺少检验 ≠ 不存在 | 需 G-ext 配置（工程，只读权限下我做不了） |

## C. Kill list

| 候选 | 死因 | 死在哪 |
|---|---|---|
**恢复处方 vs 进度守卫的复合活锁** | 因果链检验：REOBSERVE → 其后首个同参数读提案 → 放弃，只有 **3/12** 构成；9/12 不构成；3 例全是**同一任务** R2-6-split 跨两提交，且参数都是那次 `notes/` 目录读——**正是已归约为工程并由 ADR 0044 修掉的可寻址性情形** | 本轮新测量（自己的假设被自己的数据杀掉） |
**designation vs authority 分离（人批准散文、运行时执行词法匹配的能力）** | `authority.escalated` 载荷携带已解析 `capabilityId`、`effectClass`、逐字 `occurrence` 与 `resourceBindings`（sha256 + 来源观察）。人看到的是能力与字节。**缺口不存在** | 本轮新测量 |
**规格在执行中变异，使早先裁决对应不同规格** | `revisedBecause` 159/159 为空；`successCriteria` 相邻变化 0 次 | 本轮新测量 |
**`task.changed` 高频 ⇒ 任务不稳定** | 载荷是状态转移（active→verified）与证据绑定，`description` 逐字不变 | 本轮新测量 |
**run 长度相变** | 反向因果（跑得长正因为在失败）+ 悬崖桶 n=4 | §B-12 自身 |
**恢复子系统无反馈环 ⇒ 无法自适应** | MAPE-K / autonomic computing 的**整个要点**就是那条反馈环；经典文献要求它。属「理论存在而未采纳」，作者已明令不得作机制论文 | 跨域归约 |
**终局分类把基础设施混入行为类别** | 已被可复现性标准工作覆盖（审计多个仓库发现无一报告失败/报错/跳过的运行数，主张 drops manifest） | 早先已归约 |
**13 条 ADR 收窄同一关系 ⇒ 关系 ill-posed** | 无法证明 ill-posed：闭合 provider 上该匹配**可静态判定**（181/1,345 可在派发前检出）→ 工程收敛，不是缺失抽象 | 早先的静态分析 |
**读提案可追踪性不对称** | 未排除「观察按设计不回填 intent id」；即便成立也属 journal 完备性 → `MEASUREMENT` | 本轮未做源码核对，故不升格 |
**§0 清单里的 16 个方向** | 本轮**未发现**任何一条具备未被击中的强形态：我无法对其中任何一条同时给出「被哪一步错误归约 + 哪个 operation 未覆盖 + 哪篇 prior art 无法表达 + 可观察 counterexample」四件套。按作者规则，**不允许复活** | — |

## D. Surviving candidates

**没有候选达到 `SYSTEMS CANDIDATE`。** 三条勉强存活但只到 `MEASUREMENT`，且都不值得 6–12 个月：

| 候选 | 判决 | 最强主张 | 最近祖先 | 未解的 delta | 最便宜的下一步测量 | 什么会立刻杀死它 |
|---|---|---|---|---|---|---|
恢复结局不可观测 | `MEASUREMENT` | 45 次诊断、45 次恢复、0 个结局事件类型 ⇒ 无法计算恢复成功率 | MAPE-K；本会话的 protocol-state 普查 | 无（经典文献已要求反馈环） | 无需 | 已死 |
读/写提案可追踪性不对称 | `MEASUREMENT` | fold 能回答写的去向，通常回答不了读的去向（221/245 vs 29/172） | provenance / event sourcing 的完备性 | 是否为设计意图 | 一次源码核对 | 若观察按设计不回填 id，则为设计选择 |
规格语言可寻址性与观察 schema 不共延 | `MEASUREMENT` | 13% 带路径断言静态不可解析；提议者自发写的 filter 语法全部不可解析 | 早先已定位为源码级工程缺陷 | 开放 provider 下是否仍可静态判定 | 需另一个带机器可检查断言的运行时——landscape 调查未找到 | 已基本死 |

## D′. 本轮唯一通过第一轮归约、随后被自己的 falsifier 杀死的现象（补 §D）

**现象：前置条件词汇比意图的偏序粗，于是无环的意图被编码成有环的，死锁检测器正确地报告一个本不存在的循环等待。**

`EXP` **完整追踪**（`r1/f9b27dd/P3-control-b/T4-rename/rep-1`）：

```
[10] action.dispatched  fs.move  intentId=T4-rename-e2-e3   ← 重命名真的执行了
[11] effect.received                                          ← 效果落地
[12] task.changed       task:T4-rename-e2-e3  status=active（非 verified）satisfies=['c1']
[16] action.proposed    "Read the workspace root listing to confirm the rename landed"
     preconditions: [{kind:"dependency-verified", subject:"task:T4-rename-e2-e3",
                      because:"The listing can only bind evidence for the rename
                               once the rename itself has been carried out."}]
[17] goal.abandoned     stuck — "dispatch of T4-rename-e2-e10 is withheld and
                                 nothing can lift it: dependency-verified(...): active, not verified"
```
其后 `c1` 被判 `cannot-tell` **五次**（事件 44/51/58/65/72）。

`EXP` **循环是精确的**：任务变 `verified` ⟸ `c1` 被确立 ⟸ 那次确认读的证据 ⟸ 该读被 `dependency-verified` 扣住 ⟸ 任务变 `verified`。
`EXP` **而循环是编码产物**：提议者的 `because` 原文说的是 *"once the rename itself has been **carried out**"*——它要表达的是「效果落地之后」，效果在 [11] 已落地。意图的偏序（效果→读→验证）**无环**；被编码后的（验证→读→验证）**有环**。
`EXP` **词汇确实只有一种**：417 个 `action.proposed` 中 21 个（5.0%）带 `preconditions`，共 29 条，**`kind` 全部是 `dependency-verified`，语料中不存在第二种 kind**。其中 2 条的 `because` 明文描述效果时序而非验证时序（另一例：*"Checking that notes.txt is gone is only meaningful once the rename action itself has been carried out."*）。
`EXP` 不可解除死锁共 **3** 例，跨 **T4-rename** 与 **R2-1-rename** 两个任务族、两个臂。

**为什么它通过第一轮淘汰**：不是「字段没接上」（效果收据在 [11] 就存在）；不是单个 bug（跨两任务族）；不是缺工程（提议者无法表达的那个谓词在词汇表里不存在）；有可观察行为差异（withheld vs dispatched）；有 falsifier；更强的模型不会消失（模型已经把正确意图写在 `because` 里了）；运行时自己检测到并报告了它（*"nothing can lift it"*）——**检测存在，消解不存在**。

**Mutation**：世界 W = 目标文件已被重命名；运行时 R 的前置条件词汇只有 `dependency-verified`；动作序列 τ = move → propose(read, precondition=dependency-verified(task of move))。**有 `effect-landed` 这种 kind 时**：读被派发，证据绑定，`c1` 确立，任务 verified。**没有它时**：读被永久扣住，`c1` 五次 `cannot-tell`，goal abandoned。可观察差异：`action.dispatched` 的有无与终局。

**Verdict: `RETIRE`（工程缺陷）—— 我自己的 falsifier 在同一轮内开火，把它杀了。**

`OBS` **`PreconditionKind` 是 6 成员枚举**（`packages/protocol/src/action.ts:101-113`）：`fresh-observation`、`target-exists`、`failure-reproduced`、`hypothesis-supported`、`user-authority`、`dependency-verified`。所以「词汇只有一种」是**语料偏差，不是词汇表事实**——而 `target-exists`（注释原文 *"The thing being acted on must be known to exist."*）恰好比 `dependency-verified` 更贴合那两条 `because` 的真实意图。
`OBS` 三处源码把它压成工程错配：
- `adapters/model-port/src/intent-source.ts:100` —— **提示模板只演示一种 kind**：`'[{ kind: "dependency-verified", subject: <a task id from TASKS>, because: <why> }]'`。这足以解释语料中 29/29 的单一化。
- `adapters/model-port/src/narrow.ts:228` —— *"**Only `dependency-verified` is checked.** The other kinds name evidence, a path or a person, and…"*：另外五种**不被强制**。
- `runtime-core/src/precondition.ts:170` —— *"And `dependency-verified` is **not closable by looking or by asking**, even…"*：**源码自己已经知道这个 kind 不可解除。**

`INTERP` 于是现象的真实形状是：**提示演示的唯一 kind、运行时唯一强制的 kind、源码标注为不可解除的 kind，是同一个。** 这是跨三个文件的错配，修法是提示里演示 `target-exists`、或对不可解除的 kind 在扣住时回落。**属工程，不是缺失抽象。** 表达力从未不足——是唯一被演示且被强制的那一种恰好不可解除。
`OBS` 我此前写「提议者无法表达那个谓词」是**错的**，已作废。这条更正不影响 §E 的结论（它本来也没进 shortlist），但它是本轮第五次「我自己的假设被自己的测量杀死」。
`OBS` 最近的经典祖先是**粒度粗化产生的伪依赖/伪环**：构建系统里按 target 而非按 file 的依赖造成 false cycle；事务里锁粒度造成 false conflict；工作流引擎里粗粒度数据依赖造成 false serialization。该失败模式经典且已命名，本例没有产生新的不可约语义。
`INTERP` 唯一 agent-specific 的差别（也是「为什么 agent runtime 把它推进新 regime」的答案）：**依赖边由模型在运行时用一个它没有参与设计的固定 kind 集合写出，描述一个它无法命名的事件时序；而它把真实意图用自然语言留在了 `because` 字段里。** 传统系统没有「依赖作者留了一张说明我真正意思的纸条」这种东西——所以这个错配是**可测的**，测法就是比对 `because` 描述的时序与所选 `kind` 表达的时序。本语料上该比对为 2/29，样本太小。
`FALSIFIER` 若 `preconditions` 的 kind 集合在源码中本就只有一种（而非语料偏差），且运行时在死锁时能回落到「效果收据即证据」，则这条降为工程缺陷。**最便宜的下一步**：一次源码普查，数 `PreconditionKind` 的枚举成员数——20 分钟，我这一轮没做。

## E. One primary candidate

> # NO PRIMARY THESIS YET

`INTERP` 依据：本轮 20 条现象中，8 条被本轮新测量直接杀死（其中 4 条是我自己的假设），7 条属基础设施或已知模型行为，5 条已在早先归约中被经典对象吃掉。**没有一条能构造出 §6 要求的 mutation**——即「若该抽象不存在，运行时在某个具体执行上一定表现不同」——因为每一条要么已有经典原语给出该行为，要么差异落在 harness 而非运行时。

`INTERP` 并且本轮与今日两条独立线同向：FTR 归约关判 RETIRE（`A_safe` 即部分可观测下的 shield，只需 partial model）；跨系统探针四张卡零违反。**三条独立证据都指向同一结论：当前没有值得成为主论文的新 systems abstraction。**

## F. Research frontier — 杀掉这些之后，MØBIUS 真正还不知道的是什么

`EXP` **第一个答案是定量的。** 81 次放弃的全量分解（按原因字符串归类，非从预览加总）：

| n | 占比 | 类别 |
|---|---|---|
| 34 | 42.0% | 重复读守卫（已知模型行为，他处已基准化） |
| **28** | **34.6%** | **transport-failed（基础设施）** |
| 6 | 7.4% | intent 编译失败 |
| 6 | 7.4% | provider/session 归属不匹配（ADR 0008/0012 的已知身份纪律） |
| **5** | **6.2%** | **未归因** |
| 2 | 2.5% | no-route（词项无重合） |

`OBS` **自我更正**：我起初写「78/81，剩 3 条未归因」，那是从只打印了前 8 条的 reason 表加总出来的，错。全量分解为 **76/81 已归因，5 条未归因**。
`OBS` 而那 5 条里有东西（见 §D）：3 条是运行时自己宣告的死锁，2 条是「ACT chosen but no intent was proposed」。

`OPEN` 真正未知的三件，且都不是抽象问题：

1. **并发 regime 从未被检验。** 语料按构造产生不出判决性情形（§B-20），而这需要一个我在只读权限下做不到的注入配置。**但这个 regime 已被他人形式化**（多 agent 并发异常的机器可检查层级 + 「这类失败根本是并发控制问题」的立场文），所以进入它是**测量，不是抽象**。
2. **stub transport 之外的行为。** 26/81 的终局由 180 秒超时与调用上限决定。在真实负载下，这个运行时的行为分布未知——而任何基于当前语料的行为主张都带这个 ~32% 的污染。
3. **泛化性为负。** 3 个成熟第三方运行时在其文档化边界内全部正确，所以「MØBIUS 观察到的失败是否在别处也发生」这个问题，目前的答案偏向「不」。这削弱的不是某个候选，而是**以 MØBIUS 为仪器发现通用缺失原语**这一整条路径的前提。

`INTERP` 我的建议（这是方向判断，交作者定）：**不要再开第七个候选。** 现有资产最诚实的形态是一篇方法论/负结果——一条假说死亡链加一套已过闸门的探针 harness，其价值在于**它的纪律可被他人复用**（正负对照、五态词表、契约与责任正交、NOT-CAPTURED ≠ violated、harness bug 能伪造 violation）。若要继续做 systems 研究，**换仪器比换候选更有希望**：当前仪器的单写者、stub-transport、单 agent regime 已被榨干。

## G. 方法与纪律声明

`OBS` 本轮继承并实际触发了先前的负结果纪律：**我自己的五个假设被自己的测量杀死**（恢复/守卫复合、designation/authority、规格变异、task.changed 语义、前置条件词汇表达力不足），其中两个我在上一格还写成了「最强信号」，最后一个是我自己写下 falsifier 后一条 grep 就否掉的。这正是 §8 那条「apparent violation 在核 contract 后消失」的同形重演，只不过这次被核的是我自己的读法。
`OBS` 两处我明确拒绝采用的数字：ADR 的 status 与 "Changes production behaviour" 计数（我的正则未匹配实际格式，结果无效）；`harness.answered` 的 `{"__answered": true}` 载荷（测试桩，不是生产审批路径）。
`OBS` 未写任何系统代码，符合本轮「纯研究、纯归约、纯候选发现」的默认。
