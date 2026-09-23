# FTR_REDUCTION_GATE.md — FTR 归约关（纯归约，无代码）

研究负责人：Claude Science · 2026-09-22 · 仓库 HEAD `5e0843a`

## 0 · 我到底在关什么（必须先说清，否则这份判决无效）

`OBS` **仓库里没有 FTR 的权威强形态。** `docs/research/CLAUDE_SCIENCE_KICKOFF_PROMPT.md` §4 原文：唯一展开该缩写的文档是 M1 backlog 行 M5「**FTR — Follow-Time Reasoner**」；而「那份原本催生 FTR 的 51 节 research brief **不在仓库里**。**Do not reconstruct it. Ask the user for it if you need the original definition.**」

因此本关同时对**两个不同对象**下判定，且不混淆：

| 对象 | 来源 | 状态 |
|---|---|---|
**FTR-repo** | 仓库的 M1 M5 行 + `FTR_FRONTIER_RESEARCH.md` §7 三层协议 | 见 §1——**项目自己已判死大半** |
**FTR-strong** | **本对话中作者给出的 formulation**：`F_t = {(h_i, E_i, O_i, A_i)}`、runtime 执行 split/merge/eliminate、`A_t^safe = ∩_{h∈F_t^live} A(h)` | 见 §2–§4——本关的主要工作 |

`OBS` **FTR-strong 是作者在本对话中的表述，不是仓库的**。我按它归约，因为它是我能拿到的最强形态；但结论不得被引述为「仓库的 FTR 定义被归约」。若那份 51 节 brief 存在更强形态，本判决须重做。

## 1 · FTR-repo：项目自己已经判死，无需我关

`OBS` kickoff §4 记录的 frontier review 结论原文：**「FTR as a better monitor」: DROPPED.** 理由是它「structurally Proof-of-Execution's non-authoritative observation plane plus FOREAGENT-style confidence-bearing prediction」；Run-time assurance / Simplex 用 plant model 加 verified fallback 解决「谁监控监控者」，**而 FTR 两者都没有**。

`IMPL` 状态未变（本轮在 `5e0843a` 复核）：`grep -ril ftr packages --include=*.ts` **0 命中**；`Assumption` / `Hypothesis` / `Contradiction` 各在 2 个文件声明、`ProjectedWorldState` 在 1 个，`ObservationObligation` **0 个**。

`OBS` **更决定性的是：FTR 的三层协议自己禁止它改变执行语义。** `FTR_FRONTIER_RESEARCH.md` §7 的不变量原文：**「II 无 effect authority」**、**「VIII 只收窄——FTR 的唯一『介入』是让 selector 走 EXPLORE/ASK（已有规则），不能改 gate 裁决」**；「第一版明确不做：**任何 hold（即使作为 log position）、任何 gate 输入、任何 agent 可见的 FTR 输出**」。H-C 把 FTR 定义为「observation-plane shadow：fail-open、只 emit cognition 事件、agent 看不到它、它不进 gate 路径」。

`INTERP` 所以作者的问题——「uncertainty changes what the runtime is allowed/required to do?」——**对 FTR-repo 的答案是「否」，而且是按其自身规范构造为否，不是测量为否。** 一个明确无 effect authority、不进 gate、只收窄的对象，定义上就是 monitor，不是 execution semantics。

## 2 · FTR-strong 的逐项归约

| FTR-strong 组件 | 已有对象 | 主要出处 | 我的核验深度 |
|---|---|---|---|
`F_t = {(h_i, E_i)}`：一组带证据与确定度的原子假设 | belief state 表示为「**a set of atomic natural language claims about the environment, each annotated with an ordinal verbalized certainty label ranging from certain to unknown**」，policy 只条件于该信念而非全历史 | **Agent-BRACE**, arXiv **2605.11436**（UNC/UT Austin/MSR） | 全文下载，摘要逐字 |
belief 是历史的充分统计量、policy 定义在 belief 上 | POMDP 的 belief-state MDP | Åström 1965；Smallwood & Sondik 1973；Kaelbling–Littman–Cassandra 1998 | **UNVERIFIED-FULLTEXT**（凭知识归因） |
forecast 作为被解析、打分、校准的一等运行时状态（D1） | 把自主决策分解为 **information, beliefs, forecasts, actions, utility** 并**各自独立验证**；LLM 形式化为 approximate Bayesian filtering operator；含 **belief calibration diagnostics、coverage tests、ablation** | **Dixon**, arXiv **2606.17383**（2026-06） | 全文下载，摘要逐字 |
`O_i`：未消解假设生成的观察义务 | contingent / AND-OR planning 的 sensing action 选择；active diagnosis / sensor scheduling | 本会话早先已归约（active diagnosis 一节） | 早先已核 |
split / merge / eliminate | belief 更新 `τ(b,a,o)`；AND-OR 展开；hypothesis elimination | 同上 | UNVERIFIED-FULLTEXT |
**`A_t^safe = ∩_{h live} A(h)`：仅当所有存活世界都允许才可 commit** | **POMDP 的 shield**：*"A shield allows only actions that enable the agent to stay in a winning region. That means, when taking an action from some winning belief support, any next belief support reached by taking this action must belong to a winning region."*，其中 *"A state s is in the belief support B for a belief b, if s ∈ supp(b)."* | **Carr, Junges, Jansen, Topcu**, arXiv **2204.00755**，AAAI'23 | **全文下载，定义逐字** |
不可逆外化的屏障 | **output commit problem**：*"before sending a message (output) to OWP, the system must ensure that the state from which the message is sent will be recovered despite any future failure. This is commonly called the output commit problem [Strom and Yemini 1985]."* | Strom & Yemini 1985，经 **Elnozahy, Alvisi, Wang, Johnson**, ACM CSUR 34(3) 2002 | **survey 全文逐字**；Strom & Yemini 原文未取 |
commit 反向约束仍合法的 future hypotheses | belief revision 带受保护核 / integrity constraints；DB 侧即「已提交的写固定了读集」（本会话已归约） | AGM + integrity constraints | UNVERIFIED-FULLTEXT |

### 2.1 我原本留着的辩护出口被堵掉了

`OBS` 我本来准备的 FTR 抗辩是：「POMDP / conformant planning 需要已知的概率模型，agent runtime 没有」。**2204.00755 明文否掉了这一条**：*"we need to know all potential transitions in the POMDP, while **probabilities and rewards may remain unspecified**"*，shield 由 satisfiability solving 计算，**只需 partial model**。所以「我们没有概率」不构成空地。

## 3 · 一个容易搞反的结果：**最近邻不杀它，经典侧才杀它**

`EXP` 对两篇 2026 年最近邻做词频（全文）：

| 词族 | Agent-BRACE (79,532 字符) | Dixon (64,320 字符) |
|---|---|---|
`permitted / allowed / disallow` | **0** | 1 |
`obligation` | **0** | **0** |
`forbid / must not / prohibit` | 3 | **0** |
`irreversible` | 1 | **0** |
`runtime` | **0** | **0** |
`all possible worlds / states` | **0** | **0** |
`shield / safety constraint` | **0** | **0** |

`INTERP` 两篇最近邻占据的是 **表示**（Agent-BRACE 的信念结构，与 `F_t={(h_i,E_i)}` 几乎逐项相同）与 **验证/治理**（Dixon 的 belief/forecast/policy 独立验证与校准诊断），**但在「许可/义务」这一轴上近乎完全沉默，且两篇 `runtime` 词频均为 0**。

`INTERP` 所以作者那句收窄——「不要问 agent believes what，要问 uncertainty changes what the runtime is allowed/required to do」——**是一个正确且必要的收窄**：它确实把 2026 年的 agent 文献甩开了。杀死它的不是这些最近邻，而是**部分可观测下的 shielding 与 output commit 这两个更老的对象**。这个方向如果不核经典侧而只核 agent 侧，会误判为存活。

## 4 · 判决：**RETIRE**

`INTERP` 作者预注册的杀死条件为：若存在简单映射 `FTR ≡ BeliefState + Planner + Monitor`，且 MØBIUS 只是在 TypeScript 里把它们拼起来，则 FTR 退役、不做实现。**该条件成立：**

- **BeliefState** ← Agent-BRACE（表示，逐字）+ POMDP belief（充分统计量）
- **Planner** ← contingent/AND-OR 的 sensing 义务 + conformant 的全世界量词
- **Monitor** ← 三值 RV / monitorability（本会话早先已归约）
- **而唯一会改变执行语义的那一项 `A_safe`**，正是 POMDP shield——**已发表、带保证、只需 partial model**，而 MØBIUS 没有那个保证。

`INTERP` 存活条件（「某个 operation 无法被已有三件套表达，且该差异能构造出已有模型无法表达/无法保证的执行」）**未被满足**。我逐一试过三个候选残余，无一存活：

1. **假设集是开放的、由模型在运行时生成、不可枚举。** 这破坏的是**经典对象的保证**，但同时也不给 FTR 任何保证——它使 FTR **严格更弱**，不是更新。
2. **义务是 deontic（被要求），不是 value-maximizing（被选择）。** 已被 knowledge preconditions（动作的可执行性以 agent 知道其前提为条件）覆盖；shield 也正是 deontic 形状（允许集，非偏好序）。
3. **commit 反向约束合法假设。** POMDP 的 `τ(b,a,o)` 与 belief revision 的受保护核已覆盖；本会话早先已把 DB 侧那一半归约完。

## 5 · 这是第六次同形归约

| # | 候选 | 已有对象 | 运行时实际做的 |
|---|---|---|---|
1 | 判官缺因果项 | actual causality | 效果日志一次语法查找 |
2 | 完成归属 | actual causality（需因果模型+反事实） | — |
3 | 最小 witness commitment | auxiliary views / self-maintainability（1996/1988） | — |
4 | 晚绑定见证义务 | 不存在（实测 0/165） | 先看后改已关窗口 |
5 | 内生观察字母表 | monitorability 可判定（Thm 5.3） | 可算而无人算 |
**6** | **FTR-strong** | **belief support shield（2204.00755）+ output commit（1985）+ Agent-BRACE 表示 + Dixon 验证框架** | **未实现（0 命中），且其自身规范禁止它改执行语义** |

`INTERP` 六次同一形状：**理论存在且比所需更一般，而运行时既没实现一般解也没实现便宜的特例。**

## 6 · 对项目的结论（按作者的要求直说）

`INTERP` **按当前证据，MØBIUS 的论文价值不在新的 systems abstraction。** 作者在批准本关时已写下这个条件分支：「如果它也死，那我们就知道 MØBIUS 的论文价值不在新的 systems abstraction」。它死了。

`OBS` 这与今天的 pilot 结果同向且互相独立：C1/C2/C3/C2-NI 四张卡、3 个真实运行时、适用格违反数 0，每格都有 100% 检出的正对照。一条线说「成熟运行时没有重犯经典错误」，另一条线说「MØBIUS 提出的抽象已被经典对象覆盖」。

`OPEN` **本关未覆盖的唯一实质缺口**：那份 51 节 FTR brief 不在仓库中，kickoff 明令不得重建。若它存在一个与 §2 表中七项都不同构的 operation，本判决须重做——**这是一个需要作者提供材料的阻塞项，不是我能自行解决的。**

## 7 · 核验深度声明

- **全文下载并逐字引用**：2204.00755（shield 定义）、Elnozahy et al. CSUR 2002（output commit 定义）、2605.11436 与 2606.17383（摘要逐字 + 全文词频）。
- **ID 已核**：2606.22528、2602.07883、2605.27922 全部解析且标题一致（`ToolSelf` 实际副标题为 "Tool-Driven **Emergent** Adaptation"，作者引文写作 "Intrinsic"）。
- **未取到全文**：Strom & Yemini 1985（只经 survey 引用）；1606.07528（旧式 arXiv PDF 路径持续 406，未伪装 UA，放弃）；POMDP 充分统计量、AGM、knowledge preconditions 的经典原文——以上均标 **UNVERIFIED-FULLTEXT**。
- **未做**：任何代码、任何实现、任何实验。本关按作者要求是纯归约。
