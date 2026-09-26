# 运行时决策权归属：第二轮最近邻检索与证伪

研究负责人：Claude Science · 2026-09-23
输入：一份外部第一轮素材（七类「自主性失败」+ 一个待命名概念 + 11 个 issue + 4 个 arXiv ID）
任务口径：**只做最近邻检索与证伪，不设计机制**

---

## 0 · 命名屏蔽与检索口径（先说不能主张什么）

**命名屏蔽已执行。** 本轮所有对外查询只使用领域自身词汇（escalation / clarification / adjustable autonomy / delegated authority / oversight / underspecification / value of information / meaningful human control 等），未向任何外部服务发送项目内部名称或概念代号。屏蔽是**单向**的：我仍持有项目全部历史记录，所以这不是盲评，只是「不按项目词汇锚定检索」。差别重要——下面的归约判定来自领域词汇命中，不来自项目词汇的自我印证。

**检索面**
- arXiv API：第一轮 20 条查询 → 389 条唯一记录；第二轮 10 条定向查询（漂移方向）→ 53 条唯一记录。
- Crossref：15 条经典条目按题名检索，12 条精确匹配，3 条不匹配（见 §6）。
- GitHub REST API：11 个 issue 逐条取回。
- 判读：389 条摘要经 LLM 逐条分类（严格提示，`relevance` 0–3），其后 **30 篇由我读 arXiv 原始摘要**（不是读 LLM 转述）。台账 31 行 / 29 个唯一 ID，其中 **2 个（2603.19997、2607.21909）只到题名级**，已在 `read_depth` 列标出。

**这批检索不能支撑的三件事**
1. **不能作缺席证据。** 未检 DBLP / ACM DL / IEEE Xplore。CHI / CSCW / UIST 2026 这条线正是「agent 何时该打断人」的主场，本轮**完全未覆盖**。项目自身已有的明文警告（`WHAT_IS_LEFT.md` §1）在此照旧生效。
2. **不能作发生率。** issue tracker 不是工作负载。把 11 个 issue 当现象频率用，与项目已撤回的那个 56% 是同一个错误（`CLAIM_RETIREMENT` B2）。
3. **摘要级判读 ≠ 正文级归约。** 下表标「占据」的条目读的是摘要（若有 venue comment 则一并记），未读正文。少数摘要在我截取处被截断，凡截断处我不补全句意。

---

## 1 · 来源核验：素材本身是真的，但关闭状态改变了它的证据强度

**4 个 arXiv ID 全部解析成功，题名逐字一致**（arXiv API）：

| ID | 日期 | 题名 | 作者数 |
|---|---|---|---|
| 2608.12355 | 2026-07-04 | Humans are Missing from AI Coding Agent Research | 13 |
| 2605.24309 | 2026-05-23 | Reframing LLM Agent Security as an Agent-Human Interaction Problem | 3 |
| 2606.29957 | 2026-06-29 | SWE-Together: Evaluating Coding Agents in Interactive User Sessions | 11 |
| 2609.04611 | 2026-09-04 | $τ^τ$-Bench: An Environment for End-To-End, Realistic Agent Construction | 4 |

其中 **2605.24309 早已在本项目语料中**（`HUMAN_CONTROL_AND_INTERACTION.md` 引用 6 次，读取深度 ABS，已核验）。另三条是新 ID。

**11 个 issue 全部存在，题名逐字一致。但关闭原因是新信息，而第一轮素材没有取：**

| 状态 | 条数 | issue |
|---|---|---|
| open | 4 | claude-code#80765；codex#29406、#38328、#16536 |
| closed as `duplicate` | 3 | claude-code#40162、#42236、#27002 |
| closed as `not_planned` | 2 | claude-code#62917、#10049 |
| closed as `completed` | 2 | claude-code#59505、codex#33313 |

`OBS` 这改变了三处引用方式：
- **#40162（TaskCreate 之间停下来）被判 duplicate**，故它不是一个独立观察，而是某条主 issue 的一次报告；把它当「典型案例」引用时必须说明这一点。
- **#62917（长会话中自主性漂移）被判 `not_planned`**，即维护方未否认现象但不计划处理。对研究而言这是**最有利**的一种状态：现象未被修掉，测量窗口仍开着。
- **#27002（用户拒绝后命令仍被执行）被判 duplicate**，且第一轮素材自己已标注为用户报告。它不能当作已独立验证的系统行为。**我维持这个保留，并且强化它**：本轮未做任何复现尝试。

---

## 2 · 七类失败逐条判定：六类已被占据，一类只剩窄残余

判定词表：**占据** = 已有工作提出同一决策对象或同一测量对象；**部分占据** = 覆盖同一现象但换了一个更一般的框；**命名** = 现象已被命名但未测量；**反证** = 结论与之相反。完整逐条见 `escalation_neighbour_ledger.csv`（30 行，含日期、作者数、venue comment）。

### 2.1 类 1「false escalation」与类 2「missed escalation」——占据，且已被合并为一个指标

这两类在领域里**不是两个问题，是一个指标的两端**：

- **2604.09408 HiL-Bench（12 作者）** 的核心指标 **Ask-F1 = 提问精确率与阻塞召回率的调和平均**，摘要明写它「captures the tension between over-asking and silent guessing」，并明写现有基准的缺陷正是「侥幸猜中缺失需求的 agent 与本会提问的 agent 得分相同」。第一轮素材推导出的「interaction 少也不一定好」在此已是指标的结构性质。
- **2608.05519 EcoAgent-Bench（4 作者）**：304 个带价格与预算的任务，四项被测决策中前两项就是 *avoiding unnecessary escalation* 与 *escalating when local evidence is insufficient*；并且为防 always-escalate 策略刷分，报告 **economic-consistency = 升级向与节省向两组准确率中的较差者**。
- **2607.13594 Safety Sentry（3 作者）**：把守卫从二分类改为**逐实例三路路由 {EXECUTE, ASK, REFUSE}**，动机摘要含「例行打断侵蚀自主性，并训练用户放行最要紧的告警」。

### 2.2「基准把 ambiguity 删掉了，我们可以把它放回去」——占据三次，其中两次已发表

第一轮素材的这一条推论是本次判定中**最干净的一次归约**：

| 工作 | 做法 | 状态 |
|---|---|---|
| 2502.13069 Ambig-SWE（5 作者） | SWE-bench Verified 的欠规格变体，测检测 / 提问 / 利用交互三步 | **ICLR 2026 已接收** |
| 2603.26233 Ask or Assume?（2 作者） | 同样是 SWE-bench Verified 的欠规格变体 + 检测与执行解耦的脚手架，69.40% 解决率 | **EMNLP 2026 camera-ready** |
| 2607.02294 UnderSpecBench（7 作者） | 69 任务族 / **2,208 个提示变体**，跑 Claude Code、Codex、OpenCode；三轴 intent clarity / target certainty / blast radius；固定环境与安全动作真值以隔离欠规格与难度 | preprint |

`INTERP` 即「把 Verified 过滤掉的东西放回去」已被独立做过至少三次，其中一次（2607.02294）的独立变量设计比第一轮素材的设想更细：它把「欠规格」拆成三条正交轴并固定真值动作。

### 2.3 类 4「authorization granularity」与类 6「delegated autonomy」——占据，含一条已证明的性质

- **2608.15888 Bounded Agents（1 作者）**：摘要的问题陈述与 codex#38328 同构——会话开始时设定权限、此后静态、每个请求独立评估。其 Agentic Principal Chain 沿 principal 链**携带并收紧**委派范围与预算，用 composition closure 阻止「单独允许的动作组合成被禁结果」，并明写「未加限制即把权威委派给子代理」；给出 **Blast Radius Monotonicity** 的证明。这一条同时占据类 4 与类 6，并且回答了第一轮素材提的 `Authority(parent) → Authority(child)?`。
- **2607.00751 SessionBound（1 作者）**：把**已批准的业务任务**转成短时、有预算、可审计的数据库会话（签名任务令牌）。这正是第一轮素材所说的 syntactic → semantic authorization，且已有原型。
- **2609.15422（1 作者）**：把同一问题命名为 **task-context mismatch** 并端到端评测（角色上限 + 任务权限分类器 + 策略禁令；RoBERTa-large macro-F1 0.881 对 Claude Haiku 4.5 0.886，600 条标注提示）。
- **2607.17225（3 作者）**：requirements-engineering 侧命名为 **delegated-autonomy boundary**，权威明确建模为 graduated tiered。
- **2608.23550（1 作者，测量类）**：481 个公开 `CLAUDE.md`，只有约 **4–16%** 的安全规则有对应的内建控制，最严标准下 **4.4%（95% CI 2.6–6.7%）**，抽取方法覆盖 66.3% 的合格规则。这是「写下来的语义授权 vs 能执行的语法控制」的一次定量测量。

### 2.4 类 7「wrong uncertainty routing」——占据，且已有工作走得比该提案更远

第一轮素材把这一类标为「最值得追」。它被占据得最彻底，而且**其中一篇已经把该提案的核心公式判为错的决策对象**：

- **2606.21399 Calibration Is Not Control（8 作者，29 页）**：论点是运行时监督被普遍表述为标量风险预测（估失败概率/置信度/不确定性，越阈值就介入），而**这瞄错了控制对象**——相关问题不是「继续下去多可能失败」，而是「某个可用的介入是否会改善结局」；两个前缀可以有相同风险估计而需要不同动作，因为一个仍可恢复、一个不可。它把该错配形式化为 **target error**，提出 **intervention advantage** 作为决策对象，并给出 **prefix branching**——同前缀反事实协议，从同一轨迹状态执行候选动作。
- **2601.06407 Value of Information（7 作者）**：决策论地权衡提问的期望效用增益与施加给用户的认知成本，无需按任务调超参，四域验证。
- **2603.30031 Cognitive Friction（1 作者）**：查哪个信息源、何时停止查询而行动；HJB 最优停止 + 基于 rollout 的 belief-dependent VoI 近似。

`INTERP` 第一轮素材写的 `U_t → {Investigate, Experiment, Infer, Replan, AskHuman}` 与 `A_t = f(task, state, uncertainty, risk, intent, history, authority, recoverability)` 在这三篇面前是**更弱的表述**：前者是一个未定参的路由签名，后者是一个未定参的函数签名；2606.21399 指出这一族表述若以风险/不确定性为输入就瞄错了对象，2601.06407 与 2603.30031 已经给出定参的决策论替代。

### 2.5 类 5「interruption semantics」与「meaningful control points」

- 「No 到底指停任务还是跳过这一步」：最近邻是 **2603.19997 Cancelability in Interactive Instruction Following（4 作者）**，覆盖同一现象的一部分。这一格是七类中**覆盖第二薄**的，但它的形状是一个交互 affordance（#10049，`not_planned`），不是一个可测的运行时对象。
- 「meaningful control points」（2608.12355 用语）：已有术语是 **meaningful human control**，Santoni de Sio & van den Hoven 2018（Frontiers in Robotics and AI，Crossref 438 次引用）为哲学基础；agent 侧 2609.24242 已有 anticipatory human oversight 的对应论述。**这是换词而非新概念**，项目自身的评审准则（「不要因为术语不同就叫它新颖」）在此直接适用。
- 「approval fatigue 使审批失去安全意义」（Cursor 官方论证）：**已被命名并测量三十年**。项目自己的 `HUMAN_CONTROL_AND_INTERACTION.md` §D.2 已收录 Parasuraman & Manzey 2010（Crossref 1330 引）、Anderson 等 CHI 2015、Vance 等 MISQ 2018。本轮新增的更强一条是 **2606.08919 Oversight Has a Capacity（1 作者）**：125 条对抗加权动作上审阅者对「什么算 risky」只中度一致（**Fleiss' κ = 0.52**，即无单一正确标签）；把审阅者建模为**随升级负荷疲劳的内生主体**后，实测安全性对升级率呈**倒 U**——更多人类监督可以使系统更不安全。
- 「autonomy 不该是 0/1 开关」：**2510.26752 The Oversight Game（2 作者）** 已把它形式化为两人 Markov 博弈（agent ∈ {play, ask} × human ∈ {trust, oversee}），并在 Markov Potential Game 条件下证明对齐保证。

### 2.6 类 3「autonomy drift」——唯一还有残余的一格，但也已被两侧夹住

389 条中被判为此类的只有 7 条，是七类中最稀的。逐条读后：

- **2505.02709 Evaluating Goal Drift in Language Model Agents（4 作者）**：系统提示给定目标后施加竞争性环境压力；最优 agent 在最难设置下 **>100,000 token** 保持近乎完美的目标遵循，但所有模型都有一定漂移，且**漂移与上下文增长下模式匹配倾向的上升相关**。
- **2609.14992 MTAC-IFBench（9 作者，23 页）**：多轮 agentic coding 的过程指令遵循，平均 7.04 轮 / 91.33 条约束，结论是现有 code agent 「**随交互会话变长性能迅速退化**」。
- **2605.10481（7 作者，立场论文）** 把一般现象命名为 **constraint drift**：约束在经过记忆、委派、通信、工具使用、审计、优化后不再 operative，明列「把权威委派到超出原范围」。
- **2512.20662（2 作者）** 给出**反证**：200 轮混乱会话测试中对 context degradation「意外地稳健」。

`INTERP` 判定：**「长会话中自主性漂移」在机制层归约为 goal drift / 多轮指令遵循衰减，现象已被命名（constraint drift）且已被两次测量，第三次测量给出相反结论。** 该类不是空白。

### 2.7 「占据」的强度校准：基准侧占得实，机制侧占得虚

`OBS` 台账的 29 个唯一最近邻中，**7 个是单作者预印本**（2603.30031、2606.08919、2607.00751、2607.21909、2608.15888、2608.23550、2609.15422），只有 **4 个带场次接收声明**：2502.13069（ICLR 2026，5 作者）、2603.26233（EMNLP 2026 camera-ready，2 作者）、2605.28108（EMNLP 2026 Main，5 作者）、2512.04111（ICML 2026，12 作者）。其余均无场次声明。经典侧另有 1106.4573 = Scerri 等 JAIR 2002（见 §6），但它不占据七类中任何一格，故**不计入这 29 个**。这与项目此前记录的密度一致（上一批 11 个最近邻中 6 个为单作者预印本）。

`INTERP` 因此「占据」必须分两档读，且分档的结论不同：

| | 占据方性质 | 对该提案的含义 |
|---|---|---|
| **基准 / 测量侧**（类 1、2 与指标批评） | 4 篇已被 ICLR / EMNLP / ICML 接收，作者数 2–12 | **门已关。** 「把 ambiguity 放回基准」「用介入次数替代成功率」都已是同行评审过的公开结果 |
| **机制侧**（类 4、6、7 与控制点） | 多为未评审预印本，其中 7 篇单作者 | **门只是被占了位。** 这些是「已公开且有日期」，不是「已被验证」。在此赌新颖的失败方式不是被证伪，是被先发日期挡住 |

`INTERP` 这一分档对结论的方向没有影响，但改变了理由：不建议做机制的理由不是「已有人做对了」，而是**机制空间的公开候选密度高而验证密度低**——与项目已记录的基率同一形状（8 个自命名候选 + 7 个裁决 + ≥8 个子假设，存活 0）。

---

## 3 · 与本项目已有记录的碰撞：该提案的两个接口都接在已退役的桩上

第一轮素材的收尾有两个动作，都与本项目的既有裁决冲突，且冲突理由与本轮检索**无关**（是项目自己在更早的会话里判的）：

1. **把新框架挂到运行时未来状态那条主线上。** 该方向已于 2026-09-19 记入退役（`CLAIM_RETIREMENT` A5）：四个子主张中三个已被项目自己判死，第四个在现有 journal 上不可检验（断言全为布尔、resolution 恒零），代码侧 0 命中。**给一条已退役的方向增加新载荷，不构成复活它的理由**；要复活必须先回答 A5 的三条归约，而本轮检索没有削弱其中任何一条。
2. **把「决策权」做成逐动作的授权对象。** 逐动作同步人类授权门已记入退役（`CLAIM_RETIREMENT` A8）：同步 AuthorityGate 等于 Gemini CLI 默认模式 / OpenHands `AlwaysConfirm`，只是换名字；产业界正为可用性放弃该形态。本轮 2606.08919 的倒 U 结果**进一步加强** A8，而不是削弱它。

此外，`HUMAN_CONTROL_AND_INTERACTION.md` §D 已经把「人应该批准什么」拆成六个候选对象并逐一判定，结论是 **§D.4：六个候选中五个在机制层归约为已知抽象，第六个归约为前两者加集成分歧；没有一个是新的批准对象类型**。第一轮素材的 semantic authorization 即 §D 的 H-D1（批准对象从效果实例上移到带失效条件的类），该假设在项目内**已带三臂实验与 kill criterion**，且已在 §D.4 被记为「机制层已归约，残余是 HCI 侧能否审阅一个类」。

`INTERP` 综合：该提案不是一个新方向，而是**本项目 §D 的重述，外加一组该项目未收录的公开 issue**。它是第 24 个机制候选；`WHAT_IS_LEFT.md` §4 建议不做第 24 个的理由（前 23 个存活 0）在此未被任何新证据推翻。

---

## 4 · 本轮唯一对项目**已存活**结论有实质影响的发现

这是本次检索最有价值的一条，与第一轮素材的提案无关：

**2606.21399 已部分占据 H-D2。** H-D2（项目 §D.3 的存活可测轴）主张：以同版本重复 rollout 的分歧作为「回到人」的触发，AUROC 高于 LLM 自报置信度，真值取「人若介入会改变结局」。2606.21399 提供了两件东西：

1. **对该表述的框架级批评**：H-D2 比较的两个臂（rollout 分歧、自报置信度）**都是标量分数**，正是 2606.21399 判为 target error 的那一族；它主张决策对象应是 intervention advantage。
2. **H-D2 计划用离线判官标注的真值，已有可执行协议**：prefix branching 从同一前缀执行候选动作，直接测「介入是否改善结局」，不需判官标注。项目自身的证据纪律（判官改判效应；cannot-tell 率对判官模型高度敏感）恰恰说明**用执行替代判官是升级而非退步**。

`INTERP` H-D2 因此必须收窄。存活内容不再是「运行时信号优于自报置信度」这一框架主张，而是一个窄的信号成本问题：**rollout 分歧是否是 intervention advantage 的廉价代理**（分歧可离线批量算，prefix branching 需要重复执行环境）。这条仍然开放、仍然可测，但它是代价—精度权衡，不是框架贡献。

**kill criterion（针对收窄后的 H-D2）**：在同一轨迹集合上，以 prefix-branching 测得的 intervention advantage 为真值，若 rollout 分歧的排序相关低于自报置信度，或两者与真值的相关都低于某个平凡基线（如「动作是否不可恢复」这一布尔特征），则该代理不成立，H-D2 整条退役。

---

## 5 · 存活残余：一条，窄，且是测量而非机制

七类中唯一还有可主张空间的，是类 3 的一个**方向不对称**：

`OBS` 已发表的漂移测量全部测**同一个方向**——约束遵循的衰减（goal drift 2505.02709、alignment tipping 2510.04860、已部署事故中的未授权升级 2605.00055）。这是安全动机决定的：安全文献关心 agent **丢掉**约束。
`OBS` 而公开报告的现场失败是**相反方向**——agent 重新获得用户已明确放弃的审批门（claude-code#62917，`not_planned`；codex#29406，open）。其代价是生产力与审批疲劳，不是安全事故，**这解释了为什么安全动机的文献不测它**。
`INTERP` 在本轮 442 条摘要中，我未找到测量**授权撤回方向**衰减的工作。这是弱缺席证据（仅 arXiv、仅摘要级、LLM 初筛），不是空白证明。

### 5.1 若要测，预注册设计（含必须先分开的混淆）

- **假设**：在有显式审批账本的运行时中，固定动作类不变，agent 为已获授权的动作类再次请求批准的概率随会话位置（轮数 / token 数）上升。
- **自变量**：同一动作类在会话中的位置。**因变量**：再询问率；并同时记录其对偶——未授权径行率（使测量双向，而非单向的生产力抱怨）。
- **必须分开的两个混淆源**（第一轮素材把它们混在一起了）：
  1. **粒度失败 vs 漂移。** codex#38328 报告的是「记住整条命令字符串而非能力类」。若测量时命令实参变化，粒度失败会伪装成漂移。**必须设两格：字面命令字符串完全相同的一格，与只换实参的一格。** 只有第一格的正斜率才是漂移。
  2. **模型侧衰减 vs 权限存储缺陷。** 授权可能仍在对话上下文里但不在运行时的权限状态里。**必须同时读运行时自己的 allowlist**；若斜率在权限状态存在时消失，这是工程缺陷，应作为 bug 报告而非研究结论。
- **对照**：(a) 从未授权的基线格（给出基率）；(b) 中途重述授权的格（区分上下文衰减与策略状态丢失）。
- **kill criterion**：字面字符串相同的那一格无正斜率；或斜率在读入运行时权限状态后消失；或先验检索（补检 DBLP / ACM DL / CHI-CSCW 2026）命中一篇测量授权类指令遵循衰减的工作。
- **先验风险（高）**：2609.14992 已测多轮 agentic coding 的过程指令遵循随会话退化。若「keep working autonomously」只是其约束类目之一，本条即被归约为它的一个实例，贡献降为「该实例的效应量」。**定稿前必须读 2609.14992 正文的 6 主类 / 18 子类约束表**，确认其中是否已含授权/自主类约束。这是本条的第一 falsifier，且成本低。

### 5.2 不建议做的

`INTERP` 把七类失败写成一个 corpus 或 taxonomy 论文。理由不是悲观，是本轮判定：七类中六类已被占据，四类的占据方**已带指标**（Ask-F1、economic-consistency、Blast Radius Monotonicity、intervention advantage），两类的占据方**已发表**（ICLR 2026、EMNLP 2026）。11 个 issue 中 3 条 duplicate、2 条 not_planned、2 条 completed，作为语料既不能给发生率，也不都是未解决的现象。

---

## 6 · 经典条目核验（Crossref，题名匹配率）

12/15 精确匹配，可引用：

| 条目 | 年 | 载体 | Crossref 被引 |
|---|---|---|---|
| Lee & See. Trust in Automation: Designing for Appropriate Reliance | 2004 | Human Factors | 4054 |
| Parasuraman & Riley. Humans and Automation: Use, Misuse, Disuse, Abuse | 1997 | Human Factors | 3623 |
| Parasuraman, Sheridan, Wickens. Types and levels of human interaction with automation | 2000 | IEEE Trans. SMC-A | 3224 |
| Aghion & Tirole. Formal and Real Authority in Organizations | 1997 | J. Political Economy | 2210 |
| Parasuraman & Manzey. Complacency and Bias in Human Use of Automation | 2010 | Human Factors | 1330 |
| Horvitz. Principles of mixed-initiative user interfaces | 1999 | CHI | 1015 |
| Santoni de Sio & van den Hoven. Meaningful Human Control over Autonomous Systems | 2018 | Frontiers in Robotics and AI | 438 |
| Scerri, Pynadath, Tambe. Towards Adjustable Autonomy for the Real World | 2002 | JAIR（= arXiv 1106.4573） | 81 |
| Hoque et al. LazyDAgger | 2021 | CASE | 26 |
| Jensen & Meckling. Specific and General Knowledge, and Organizational Structure | 1996 | 书章 | 21 |
| Saunders et al. Trial without Error | 2018 | AAMAS | 8 |
| Basich et al. Learning to Optimize Autonomy in Competence-Aware Systems | 2020 | AAMAS | 1 |

**不匹配，不得引为已核验**：ThriftyDAgger（匹配率 0.63，Crossref 返回另一篇）、Interactive Task Learning（0.62）、Sheridan 监督控制原始报告（0.69）。

`OBS` 两条经典对该提案有直接归约作用：
- **Aghion & Tirole 1997**：「decision right」是组织经济学的既有术语，其 **formal authority（谁有权决定）vs real authority（谁实际决定）**的区分，正是第一轮素材所说「用户批准的是一类事 / runtime 记住的是一条命令」的一般形式。该命名不是新造。
- **Scerri et al. 2002**：adjustable autonomy 的核心研究问题已被表述为「transfers-of-control 是否以及何时应发生」，且已批评**一次性（one-shot）转移**并改为 **transfer-of-control strategy**（条件式序列），并计入转移对团队的代价。第一轮素材的「autonomy 应是动态 authority topology 而非开关」在此已是 2002 年的出发点。

---

## 7 · 核验深度声明

| 项 | 深度 |
|---|---|
| 4 个输入 arXiv ID | API 元数据核验（题名、日期、作者数）；正文未读 |
| 11 个 GitHub issue | API 核验（题名、状态、关闭原因、评论数）；正文未读；**无一条经复现** |
| 30 篇最近邻 | arXiv 原始摘要 + venue comment；**正文全部未读**；另 2 个 ID 仅题名级（2603.19997、2607.21909）。29 个唯一 ID 中 7 个单作者预印本、4 个带场次接收声明（作者数 2–12） |
| 15 条经典 | Crossref 元数据；12 条题名精确匹配；正文未读 |
| 389 + 53 条摘要 | LLM 逐条初筛（`relevance` 3 = 116、2 = 195、1 = 71、0 = 7）；初筛偏宽（`E` 类命中 355/389），故所有判定均以我读过的 31 篇为准，不以初筛标签为准 |
| 未覆盖 | DBLP、ACM DL、IEEE Xplore、CHI/CSCW/UIST 2026、任何非英文文献、任何产品变更日志 |
