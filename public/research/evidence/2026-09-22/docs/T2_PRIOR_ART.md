# T-2 对经典与近邻文献的归约判定

研究负责人：Claude Science · 2026-09-22 · 关一（计划 phase-0）产出

**结论先说**：T-2 原形态（「并发写者下运行时如何知道变化是自己造成的」）**三个半中有两个半被占据**，其中一个是被**竞争解释**否掉的——对动作安全而言归因**不必要**。存活的残余很窄但未被占据，且与本项目 HEAD 提交信息（`5e0843a` "a correct world is not a proven one"）同向。

---

## 1 · 最近邻（全部逐字核验）

### 1.1 ATR — arXiv 2609.08015《From Version Conflicts to Decision Conflicts: Selective Revalidation for Long-Running AI Agents》（Lyu, Ren, Lai / Huawei UK；Liu / XJTU）

**这是本项目原始主线（C1/C2：过期人类审批）迄今最接近的近邻，比 CommitGuard 与 PlanFence 更近。** 原文：

> *"Long-running AI agents may read state, reason, wait for tools or **human approval**, and perform an external action much later. **The state that justified the action can change in the meantime.**"*
> *"Standard optimistic concurrency control and version checks can detect that previously read state has changed, but **by themselves do not determine whether that change invalidates the pending action's justification.**"*

它给出的东西与项目所设想的高度重合，且更完整：
- **命名区分**：任何被检出的版本变化是 **version conflict**；使正当性失效者才是 **decision conflict**。
- **机制**：记录「使待执行动作正当的、显式可执行的条件」，变更发生时**只重查受影响的条件**。
- **四种结局**（非二值）：KEEP / REFRESH（仅刷新非决定性元数据）/ 要求重规划 / **BLOCK**（*"a safety, authority, policy, or irreversible-effect condition is false, missing, contradictory, or **unverifiable**"* ——注意 unverifiable 已在其结局语义里）。
- **原子绑定**：*"a target-side transaction or compare-and-set binds checked state to commit"*，另列 uniqueness constraint、lease、fencing token。
- **规模**：210,000 次受控执行 / 15 个变更用例，*"matched every developer-specified outcome with no false allows or blocks"*；10 个 durable SQLite checkpoint/resume 单元中每次变更评估 0.6 条条件对 FullScan 的 6.0 条。

`INTERP` 这使项目「写集 vs 读集」「重验证前提而非重验证效果」那一整套表述**不再有分离点**——ATR 正是「重查正当性条件」而不是「重查效果」，并且已经度量过。

### 1.2 ConcAnom — arXiv 2606.17182《Verified Detection and Prevention of Concurrency Anomalies in Multi-Agent LLM Systems》（S. Khan）

四类异常在 TLA+ 中形式化：**stale-generation、phantom-tool、causal-cascade、tool-effect reordering**，各附 TLC 反例；机器验证的一致性层级 `L0 ⊊ … ⊊ L4`，自称 *"to our knowledge the first machine-checked consistency hierarchy for such runtimes"*；274 条 Verus 义务（zero assume / zero admit）；三个已部署 Rust 运行时实现 L0–L1（悲观锁、可串行化快照隔离、默认 SI）；**防护代价已测**：SI 在一个工作负载上约 **+8% token**，悲观锁 **1.6–2.3×**。
`INTERP` **stale-generation 即项目的陈旧基准问题**，已被形式化、验证并部署。

### 1.3 Position — arXiv 2608.18092《Position: Multi-Agent Systems Should Prioritize Concurrency Control》（Yang, Li, Ji, Zhang, Jiang）

主张 *"many MAS failures are fundamentally concurrency control problems"*，并把被归为「协调」或「通信」失败的模式**直接映射到经典并发异常**；呼吁把 conflict detection、isolation guarantees、structured access 作为一等设计关切。
`INTERP` 「多 agent 并发是运行时缺失能力」这个**立场本身**已被公开主张。

### 1.4 经典侧

`OBS` 检索到但判为不构成额外威胁：Kairos（2308.05034，whole-system provenance 做入侵检测与调查）、why/how-provenance 与 provenance 半环（2303.12773 等）、Dotted Version Vectors（1011.5808）、A Critique of Snapshot Isolation（2405.18393）。这些给出**归因的机制**（血缘、版本向量），但其归因对象是数据流与故障，不是「完成判定的归属」。

---

## 2 · 归约表

| T-2 的子命题 | 判定 | 依据 |
|---|---|---|
| 并发读写导致陈旧读、丢失更新、结果不一致 | **占据** | ConcAnom 的四类异常 + L0–L4 层级；Position 文的映射 |
| 人类审批后世界移动，需在派发前重验 | **占据，且被更完整地占据** | ATR 的 version/decision conflict + 四结局 + CAS 绑定 + 210k 执行 |
| 「运行时需知道变化是谁造成的」以保动作安全 | **被竞争解释否掉——归因不必要** | ATR 处理他人写入的方式是**使正当性失效**：*"a refund issued by another worker must prevent a duplicate"*。它从不问是谁改的 |
| 防护代价未知 | **占据** | ConcAnom 已测：SI +~8% token、悲观锁 1.6–2.3× |
| **完成判定的归属**：目标状态由他人造成时，运行时会不会把他人的工作记为自己完成 | **未占据** | 三篇中 `task completion\|goal achiev*\|completion criteri\|judg*` 命中 **0 / 0 / 7（仅立场文动机句）**；`credit\|self-attribut*` **0 / 0 / 0** |
| **不版本化的外部世界** | **未占据，且 ATR 自己点名为未闭合** | ATR：*"such a change **need not advance the target version** … ATR records the evidence as unbound and **exposes the residual race to policy**"*；ATR 全文 `file system\|filesystem` **0 命中**、`unversioned` **0 命中**；ConcAnom 的共享状态是 *"memory stores, vector indices, and tool registries"*，`file system` 亦 **0 命中** |

---

## 3 · 存活的残余（收窄后的 T-2）

> **在不版本化的外部世界（普通文件系统、浏览器 DOM、shell 状态）里存在并发写者时，运行时无法确立「被观察到的状态是由我的效果造成的」。重验证（ATR）解决的是「该不该动手」；它不解决「这个目标是不是由本 agent 完成的」。fail-open 的判官会把世界记为自己完成，fail-closed 的判官会停摆。两者都不对。**

`INTERP` 为什么这不是换名字：ATR 的归因不必要性论证**只对动作安全成立**。完成判定是另一个谓词——它问的不是「前提是否仍然成立」而是「这次变化的来源是谁」，而那正是 ATR 刻意不需要的信息。
`INTERP` 为什么它有意义（需在论文中论证，不可假定）：错误归属会腐蚀四件事——(a) 用于终止的完成信号；(b) 多 agent 系统的评估与 credit assignment；(c) 人对「我的批准达成了什么」的信念；(d) 回滚范围（撤销我的改动而非他人的）。
`OBS` 项目自身 HEAD 提交 `5e0843a` 的信息即 *"a correct world is not a proven one"*——**这句话项目已经有了**，本研究能加的是度量与机制，不是这句洞见。

---

## 4 · 对计划的修订（关二的问题换了）

`INTERP` 计划 phase-1 原定离线检验 H1「运行时能否归因」。按上述，**这是错的问题**——归因对动作安全不必要，所以「不能归因」本身不是缺陷。正确的问题是：

> **误归属是否会改变完成判定？** 即：存在第二写者产生目标状态时，完成判定是否会把它记为本 agent 已完成（fail-open）或停摆（fail-closed）。

`FALSIFIER`（关二据此重写）若在现有语料中找不到「观察到的变化不由本 run 任何已派发效果解释」的实例，或找到但完成判定未受影响，则残余的经验基础为零，T-2 退回「一个尚未发生的问题」，须按 `PAPER_FRAMING.md` §6 走回退路径。
`OBS` `ENG_HANDOFF_T2_ATTRIBUTION.md` 的 §2 假设与 §4 格表须据此改写：决定性的格不再是「同 digest 时能否归因」，而是「同 digest 时**完成判定给出什么**」。
