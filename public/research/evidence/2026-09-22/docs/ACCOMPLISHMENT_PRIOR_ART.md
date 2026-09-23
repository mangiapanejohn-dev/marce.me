# 完成归属的对抗性先验工作判定

研究负责人：Claude Science · 2026-09-22 · 计划 phase-1 step3 与 phase-2 产出

**结论先说**：`AccomplishedBy(run, Goal)` 的**形式内容已被完全解决**（Halpern-Pearl 系的 actual causality，及其在 Dec-POMDP 上的实现），**轨迹侧的替代解法已部署**（process mining 的 conformance checking），二者**各缺一半**。残余是一条经验主张加一条关于「运行时能在原则上确立什么」的表述，不是新的形式概念。

---

## 1 · 形式侧：已解决，而且对我们的特例是过度设计

`OBS` **arXiv 2204.00302《Actual Causality and Responsibility Attribution in Decentralized Partially Observable Markov Decision Processes》**（Triantafyllou, Singla, Radanovic；MPI-SWS）。原文：*"Actual causality focuses on specific outcomes and aims to identify decisions (actions) that were critical in realizing an outcome of interest. Responsibility attribution is complementary and aims to identify the extent to which decision makers (agents) are responsible for this outcome."* 它建立 Dec-POMDP 与 SCM 的对应，沿用既有 actual causality 语言，并因既有定义会给出反直觉的实际原因而**提出一个更显式处理 agent 间因果依赖的新定义**，再据此做责任归属。

`INTERP` 故「哪个施动者造成了这个结果」在形式层**已解决**，且是在多 agent、部分可观测、序贯决策这一正是我们设定的框架里解决的。**本方向不得把形式概念当贡献。**

`OBS` 核实其前提：全文 `structural causal model|SCM` 41 命中、`counterfactual` 54 命中，but-for test 为其规范进路（*"A canonical approach to actual causality is based on the but-for test, which examines the counterfactual dependence of the outcome on agents' actions."*）。`external|non-agent|environment actor` 0 命中——它处理**模型内的** agent；外部写者原则上可被建模成另一个 agent，故这一条**不作强证据**，只记下它要求一个把其他写者包含在内的世界模型。

`INTERP` 但归约的方向值得记录：actual causality 要的是**一个因果模型加反事实**；运行时要回答的那个特例——「本 run 是否有任何已派发效果触及该资源」——是**效果日志里的一次语法查找**，不需要反事实结构。**即需要的检查比可用的理论便宜得多，而没有系统在做。** 这把残余从「理论缺口」改成「未采纳」。

---

## 2 · 轨迹侧：已部署的替代解法，但它不验证世界

`OBS` **arXiv 2605.06457《Beyond Task Success: Measuring Workflow Fidelity in LLM-Based Agentic Payment Systems》**（Huang, Chua, Wang；SMU / Mastercard）。原文：*"TSR captures only final outcomes, and HF1 evaluates routing in a bag-of-edges fashion, ignoring temporal order. Neither captures workflow fidelity—the agent's adherence to the expected sequence of steps."* 提出 **Agentic Success Rate**：给定期望轨迹 `E=[e1,…,en]` 与观测轨迹 `O`，按 transition multiset 算 `TR=|BE∩BO|/|BE|`、`TP=|BE∩BO|/|BO|`、`ASR=F1(TR,TP)`；明言取自 *"the conformance checking paradigm from process mining"*。规模：18 个模型 / 90,000 实例，发现 18 个模型中 10 个系统性跳过一个确认检查点，而 TSR 与 HF1 **都看不见**。

`OBS` **范围核验（词边界检索）**：`concurren*`、`another agent|writer|worker`、`external change`、`foreign` **全部 0 命中**；`world state`、`state verification`、`database`、`environment state` **全部 0 命中**。它的轨迹是 **agent 间 handoff 的序列**（`[A,B,C]`），**不验证世界状态**，也不考虑外部写者。
`OBS` 它**需要一个给定的期望轨迹**。这是 conformance checking 的前提，对固定工作流（支付）成立，对开放式任务不成立。

`INTERP` 轨迹侧**隐含地**解决了归属——只看 agent 自己的轨迹，他人写入自然拿不到 credit。但代价是：不确认世界真的变了，且需要参考序列。

---

## 3 · 三族成功条件的互补失败（这是本判定的核心表）

| 成功条件族 | 能确认世界变了 | 能排除他人所为 | 需要参考序列 | 部署现状 |
|---|---|---|---|---|
| **状态谓词**（TSR；本普查三系统的现状，42/42） | 是 | **否** | 否 | 普遍 |
| **轨迹一致性**（ASR / process mining conformance） | **否** | 隐含是 | **是** | 支付等固定工作流 |
| **成就谓词**（状态 + 与本 run 效果的绑定） | 是 | 是 | 否 | **本普查中 0/42** |

`INTERP` 两个已部署族各缺一项，而缺的那两项不同。第三族是二者的合取，且它所需的事实**完全在运行时自己的效果日志里**——不需要参考工作流，也不需要因果模型。

---

## 4 · 残余（允许成为论文主张的部分）

1. `EXP` **经验**：三个独立验证机制（模型判官读散文标准、程序化 web verifier、测试文件期望世界表）的成功条件中，**AGENT 类 0/42**。无一约束施动者。
2. `IMPL` **可表达性**：至少一个系统的机器断言语言**在类型层无法表达**成就谓词——算子集 `{equals, contains, matches, exists, absent, gte, lte, changed}` 全为状态算子；唯一时间算子 `changed` 是与记录 baseline 的 `deepEqual` 取反，**他人写入同样满足**。
3. `EXP` **代价与收益**：把标准改写为成就谓词后，诚实情形逐例不变（S2==S 21/21），他人所为情形 20/21 翻为否定；长度对照（同样加前缀但不含施动者）与基线逐例相同 21/21，故效应来自施动者子句。
4. `INTERP` **机制**：所需检查是效果日志的语法查找，比 actual causality 便宜得多；比 conformance checking 少一个前提（不需要参考序列）。

## 5 · 不允许成为主张的部分

- 「哪个施动者造成了结果」的形式定义 → 2204.00302 及其上游。
- 「最终结果不足够，要看过程」→ 2605.06457、TRAJECT-Bench(2510.04550)、Plan-RewardBench(2604.08178)、process mining conformance checking（二十年历史）。
- 「过程奖励 / 轨迹级奖励模型」→ Math-Shepherd(2312.08935) 一系。

`FALSIFIER` 若能找到任一部署系统的成功条件显式绑定「由本次执行的效果造成」，则第 1 条经验主张作废。目前普查为 0/42，但样本只覆盖三个系统，**且全部由我分类**。
