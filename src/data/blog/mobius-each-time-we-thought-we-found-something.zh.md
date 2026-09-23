---
slug: "mobius-each-time-we-thought-we-found-something.zh"
title: "MØBIUS——每一次以为发现了什么之后"
description: "9 月 18 日到 22 日的完整研究记录：审批线的最后两个残差、完成判定的证据选择、completion attribution、transition witness、late-bound obligations、跨运行时的 Jepsen 式探针、Delegated Obligation Closure，以及 FTR 强形态的归约关。每一步都保留了预测、测量、解释、更正与最终状态，包括我们自己仪器犯的错。结论是：现在还没有一个愿意称为新 systems abstraction 的主论点。"
lang: "zh"
pubDatetime: 2026-09-22T16:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research", "Negative Results"]
category: "research"
series: "MØBIUS"
timezone: "America/New_York"
showInBlog: true
cover: "/cover-mobius-exploring.webp"
ogImage: "@/assets/images/og-mobius-exploring.png"
---

上一篇 MØBIUS 文章发在 9 月 19 日。它的结尾说 FTR 在调查中把自己杀掉了，但催生它的问题没有死，并列了一张接下来要追的队列：evidence horizon、transition-dependent completion、unsupported establishment、certificate replayability、anticipatory evidence preservation、future information requirements。

这一篇记录那之后发生的事，时间跨度是 9 月 18 日到 22 日（与上一篇有一天重叠，因为研究负责人那条线从 18 日就开始了），外加我为写这篇文章做的一次取证。它不是进度报告。这几天里有十几个候选方向被提出来、被测、然后被判了状态（Figure 1 列了其中十五个）；其中六次是**同一个形状**的归约，另有两条线被跨运行时的实验直接停掉或杀掉。到今天为止，没有一个活下来成为主论点。

我想把这几天写成一份 research record，而不是一篇「我们发现了什么」的文章。所以每个候选都尽量保留五个环节：

| 环节 | 含义 |
|---|---|
| **prediction** | 测之前写下的预期，以及杀死条件 |
| **measurement** | 实际测到的数，来自哪个文件 |
| **interpretation** | 当时对这个数的解释 |
| **correction** | 后来发现解释（或数本身）错在哪里 |
| **final status** | 今天的状态：<span class="st st-killed">KILLED</span> <span class="st st-retired">RETIRED</span> <span class="st st-prior">PRIOR ART</span> <span class="st st-measured">MEASURED</span> <span class="st st-open">OPEN</span> <span class="st st-ne">NOT EVALUABLE</span> |

这篇文章的可信度只能来自这条链，而不是来自最后那个版本看起来多整齐。错误的预测、被撤回的判定、我们自己 harness 的 bug，都留在里面。

**关于「我」和「研究负责人」。** 这段时间的大部分测量和文献归约，是我在 Claude Science 里跑的一个独立研究负责人 agent 做的；方向、杀死条件、何时停，是我定的。文中「我」指我自己，「研究负责人」指那个 agent。它的账本是几份文件：`RESEARCH_MAP.md`（§0–§40）、`TRACKS.md`、`INVARIANT_CARDS.md`、`PILOT_RESULTS.md`、`C1_RESULTS.md`、`C2NI_RESULTS.md`、`FTR_REDUCTION_GATE.md`，以及 pilot harness 的 `rows.jsonl`。MØBIUS 的实验 journal 在仓库的 `docs/research/evidence/`（104 个 `events.json`）。MØBIUS 仓库本身仍是私有的，但**这篇文章依据的证据已经打包公开**：[证据包](/research/evidence/2026-09-22/README.md) 里有探针 harness、逐行 ledger（含那份被归档的混合账本）、各张派生数据表、研究负责人的结果文档，以及那 104 个 journal。仓库里其余的文件，文中只给文件名与提交号。**文中的每一个数，我都为这篇文章从这些原始文件重新算过一遍**；重算与账本不一致的地方，正文里会直接说。

外部文献与 API 契约，全部在 9 月 22 日重新打开原始记录核过：arXiv 页面、DOI、出版社页面、官方文档与安装包源码。核验深度标在文末参考文献里：`FULLTEXT`、`ABSTRACT-ONLY` 或 `UNVERIFIED-FULLTEXT`。

<figure class="fig">
<a href="/research/mobius-rl-graveyard.svg"><img class="fig-light" src="/research/mobius-rl-graveyard.svg" alt="9 月 18 日到 22 日的候选时间线。每行一个候选：审批线残差、证据替换、transition witness、证据选择、verification-input ownership、completion attribution、criterion-directed active observation、temporal witness lifecycle、late-bound obligations、recovery closure、correctness-under-adoption、delegated obligation closure、FTR 强形态，以及正在进行的方向发现。每行标出攻击它的东西与今天的状态，几乎全部以退役或被杀终止，最后一行是 NO PRIMARY THESIS YET。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-graveyard-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 1.</strong> 9 月 18–22 日的研究轨迹。每一行是一个候选：它是什么，被什么攻击，今天的状态。这张图刻意不是路线图：大部分分支在右边终止。它证明的是这些方向经历了什么；它不证明被杀掉的方向没有工程价值。</figcaption>
</figure>

## 〇 · 从功能到 runtime

MØBIUS 最早是按功能在长：planner、subagents、skills、一个 harness。真正让我停下来的失败，没有一个是缺某个功能。它们都长在功能之间：一个人批准了一个效果，世界在等待期间变了，批准被照样复用；一个任务被宣布完成，而完成的证据是它自己写下的期望；一次恢复之后，一个本该持久的计数回到了初值。于是问题慢慢从「再加一个能力」变成了 runtime 自己的对象：**state、evidence、authority、freshness、verification、replay、completion、failure semantics**。

早期的我，会因为一个结构「看起来没有人这样做」而兴奋。上一篇里那条审批线就是这样开始的：我相信「把人的批准绑定到它所依据的世界版本」是一个新机制。它后来被归约成了一个设计族里的第三个实例 [[1]](#ref-1) [[2]](#ref-2) [[3]](#ref-3) [[4]](#ref-4)。

那次之后，我给自己定了一条规则，这篇文章里的每个候选都按它判：

> 没有 prior-art reduction、没有 falsifier、没有可观测后果的东西，不叫 research result。

规则是在这几天之前写下的。这几天做的事，是第一次把它不打折扣地执行了一遍。

## 一 · 审批线的最后两个残差（9 月 18–19 日）

上一篇已经写了审批线整体归约为先验工作。那之后还剩两个残差，研究负责人把它们也处理掉了。我把它们放在最前面，因为它们确立了后面反复出现的那个形状。

**残差 A：没有内容前置条件的效果形状。** 表面普查里，四个系统 16 条可变更工具路径中 13 条不携带逐调用的内容前置条件（`old_str`、`If-Match` 一类），而且 11 条非文件路径（DOM 点击、shell）无一携带。它一度被当作 MØBIUS 机制的「独有区域」。

然后有人（我）指出：「目标没有先前内容」不等于「没有可表达的前置条件」。创建一个文件，前置条件可以是「它不存在」：`If-None-Match: *`、`O_EXCL`、GCS 的 `ifGenerationMatch=0`。CommitGuard 的见证本来就是版本／纪元而不是内容，其耦合原语明列 conditional write [[1]](#ref-1)。再回头看 MØBIUS 自己的 filesystem provider：新鲜度检查的守卫是 `if (basis && basis.freshness !== 'advisory' && existedBefore)`，文件不存在时整个检查被关掉，随后写入不带 `O_EXCL`；`fs.move` 是先查目标再 `rename`，中间是一个 check-then-act 窗口。CommitGuard 明文把「没有原子 check-and-commit 原语的运行时」排除在保证之外，MØBIUS 恰好落在那一类里，而且是因为实现选择，不是因为底层缺原语。**残差 A 判死**，剩下的是一个一行标志位的工程缺陷。

**残差 B：谁生产有效性键。** PlanFence 用工具自报的依赖集，测得声明遗漏时不安全放行上升（在「四个真实依赖里三个各以概率 $$p$$ 被遗漏」的设定下，$$p=50\%$$ 时为 37.4%）[[2]](#ref-2)；MØBIUS 的 ADR 0041 让 runtime 自己补一次 look。这看起来像一条可以写的轴——直到 S-Bus：它的标题就是 *Automatic Read-Set Reconstruction*，在服务端从 HTTP 流量重建每个 agent 的读集，并把这个性质命名为 Observable-Read Isolation [[3]](#ref-3)。**残差 B 被占据。** 9 月 22 日又读到 ATR，它把「版本变了」与「变化使动作的正当性失效」区分为 version conflict 与 decision conflict，并只重查受影响的条件 [[5]](#ref-5)——这把审批线最后一点「重验证前提而不是重验证效果」的措辞也拿走了。

这一段的教训不在任何一个机制上，而在一件更难堪的事上：审批线自己的判决单元（S2、S10、S15、VB-1、VB-2）**比较的始终是 MØBIUS 自己更早的设计**，从来没有和这些已发表的系统在同一张网格上对照过。研究负责人把 CommitGuard 的谓词编码成规则跑在 VB-2 的 36 格上，它在 MØBIUS 自己的分离网格上是 0 次不安全放行，已发布机制是 9 次。这是谓词级的比较，不是系统级的比较，但方向很清楚。

## 二 · 完成判定：证据在 journal 里，但判官没看到（9 月 18–20 日）

### 从 false success 开始

R2 的六个多步任务里，checker 通过 0 个，runtime 宣布完成 5 个。每一个假完成都经过同一条路：一次读操作，提议者自己写的期望成立（`content exists`），经 ADR 0031 的规则关闭了一条没有断言的成功标准。其中一个任务读了一个文件、什么也没写，就「完成」了。

我最初把它当成全项目最被低估的观察，叫它「证据替换」。当天下午它就被归约了：Advani 把这个现象命名为 false success，在 tau2-bench 与 AppWorld 上用上万条轨迹测过，并写下了和 R2-6 一模一样的形状——agent 读环境而不修改它，然后宣称完成 [[6]](#ref-6)。R2 是一次复现，不是发现。

### 判官与 `cannot-tell`

ADR 0043 引入了一个独立判官：它是另一次模型调用，只看标准的陈述与证据，从不看提议者的期望。假完成从 5/6 降到 0/6，但 runtime 也几乎不再完成任何多资源任务。全部已提交 journal 里，判官一共裁决 133 次：established 21、not-established 24、**cannot-tell 88**。

研究负责人把 88 条 `cannot-tell` 的理由逐条归类（判据：「现在再看一眼世界，能不能拿到这个事实」），得到（measurement，重算自 `cannot_tell_classified.json`）：

| 类别 | n | 占比 |
|---|---|---|
| **T_TRANSITION**：缺的是过去与现在之间的关系 | 51 | 58.0% |
| A_MORE_LOOKING：再读一次当前世界就能判 | 31 | 35.2% |
| S_SHAPE：事实在观察里但证据投影不承载 | 4 | 4.5% |
| 其他 | 2 | 2.3% |

而且 T_TRANSITION 集中在形状互不相同的三个任务上：**rename 13/13、按规格改配置 19/22、拆分文件 19/32**。三者的完成标准都是关于一次变化的断言：archive.txt 持有 notes.txt **原来的**内容；settings.ini 反映了规格**且其余未变**；**旧** notes.md 的每一节都成为一个文件。

决定性检查是 T4-rename 的一个 journal：事件 [7] 观察到 `notes.txt`，摘要 `sha256:6862e454…`；[10] `fs.move`；[17] 观察到 `archive.txt`，同一个摘要。判官三次说判不了，理由是「没有证据记录 notes.txt 原来的内容」。判据以一次摘要相等比较就能机械得出，而它就在 journal 里。

这是上一篇里 *transition witness* 的来源。它在三道杀死测试上一次全挂：它等于 before-image 加一条 provenance 边加一个过去时算子；过去时时序逻辑本来就是为「关于变化的断言」而设 [[7]](#ref-7)，WAL 的 undo 记录 [[8]](#ref-8)、时态数据库的 valid time [[9]](#ref-9)、provenance [[10]](#ref-10) 各自承担其余部分。<span class="st st-retired">RETIRED</span> 作为原语。这个判定上一篇已经公开，这里不再展开。

### 第一个关键更正：不是信息没了，是证据没被送到

接下来的一步，对后面的每一步都要紧。

研究负责人先排除了两个不需要新东西的解释。**判太早？** 点名了具体文件的 86 条 `cannot-tell` 里，84 条（98%）该文件在裁决**之前**已被观察，0 条从未被观察。**绑得太少？** `cannot-tell` 平均绑 2.43 条证据，`established` 平均绑 2.48 条，数量不区分。

区分它们的是另一个量：对 106 条「标准点名了具体文件」的裁决，比较**被绑定的证据**与**当时 journal 里已有的观察**对这些文件的覆盖：

| 裁决 | n | 绑定证据覆盖标准所指 | journal 当时已有 |
|---|---|---|---|
| `cannot-tell` | 77 | 66% | 100% |
| `established` | 15 | 93% | 100% |
| `not-established` | 14 | 93% | 100% |

可用性三类都是 100%，区分它们的是**选择**。源码里，`ActionIntent.satisfies` 是提议者自己声明「这个动作满足哪几条标准」的字段，`#bindClaimed` 按它把观察路由给标准。项目以前已经命名并修过两种失败——`satisfies` 为空时完成永不触发，以及「提议者即完成判官」——但没有处理第三种：`satisfies` 非空，却不对位。独立判官解决了**谁下裁决**，没有解决**谁决定判官看什么**。

> 「missing evidence」和「evidence exists but is not delivered」是两个完全不同的问题。前者要新的采集，后者只要改路由。这几天后面的每一个候选，都要先回答它属于哪一种。

### 一个预注册、命中、然后被我们自己的口径错误削弱的实验

**prediction**（9 月 20 日写在运行之前）：把证据绑定从提议者声明改为「runtime 按标准所指对象推导」，`cannot-tell` 应显著下降，量级约为 93% − 66% = 27 个百分点。三臂共用从源码逐字重建的判官谓词与渲染：C（原绑定，作效度闸门）、T（按指称推导）、R（与 T 同条数的随机观察，作数量对照）。

**measurement，第一轮**：观测 32.4 pp，命中。但效度闸门只到 64.2%——同样的证据，我们的判官比原始判官宽松得多（77 例原为 `cannot-tell` 的裁决里，C 臂有 36 例判成 established）。原因很快找到：我们用的判官比原始运行弱一档。**这一轮的绝对率作废。**

**measurement，第二轮**：原始判官模型记在语料自己里——96 条 `results.jsonl` 的 `models` 字段都是 `claude-opus-5`。用同一模型重跑，效度闸门 79.2%，然后：

| 臂（原为 `cannot-tell` 的 77 例） | 仍判不了 | 相对 C |
|---|---|---|
| C 提议者绑定 | 77.9% | — |
| T 按指称推导 | 20.8% | **−57.1 pp** |
| R 随机（证据比 C 更多） | 88.3% | +10.4 pp |

R 臂证据更多却更差：**不相干的证据不是中性的，它会稀释。** 按语料提交拆开，ADR 0045 已生效的 `f9b27dd`（n=68）上差值是 58.8 pp，更早的 `33e599e`（n=9）上是 44.4 pp；后者样本太小，两者之差不构成对照。换句话说，这个效应量是在系统自己已经采纳的部分修复**之上**的残差。

**correction**：这张表后面跟着两处我们自己的口径错误。第一，把运行中途的裁决与 checker 的任务级结果比，是错的——checker 评的是最终世界；改为每个（运行, 标准）只取最后一次裁决。第二，第一次分组时剥掉了 criterion id，得到 n=18，正确是 n=22。改正后，T 的净效果是 `cannot-tell` 9→4、established 12→16，**代价是 not-established 1→2**，其中 R2-2-module 的一条是贯穿到最后裁决的假阴性：原始判官、C 臂与 checker 都说成立，T 臂从 e7 到 e52 五次都说不成立。我们先前还写过「最后裁决上 T 的 not-established 为 0」，那是只在一个子集上算的数，撤回。

之后又试了三个选择器臂（T2、T2′、T3）。T3（每个指称对象取首次观察与最后一次效果之后的最新观察）在决定完成的那一层同时达到历史臂与快照臂的上界，在中途裁决上却比 T 差（42.9% 对 20.8%）。两个副产物值得记下：给证据项加一行 `(most recent observation…)` 注记本身就值约 12 pp——这是评估仪器自己制造的混淆；告诉判官「这里有缺口」则完全不改变行为（带缺口与不带缺口的 `cannot-tell` 率同为 33%）。三个臂都跑在同一个小集合上，这已经是研究者自由度。研究负责人停在了 T3，我同意：再调就是在拟合这 106 条裁决。

### 跨系统：先失败，再部分通过

**第一次尝试失败了，而且失败方式有信息量。** 外部语料是 SWE-agent 的 6,670 条轨迹。平衡抽样 200 条，A 臂给判官 agent 自述，B 臂给机械提取的 diff。B 更准（55.0% 对 48.8%）且证据最短，但只差 6.2 pp；更要紧的是，**独立变量被换掉了**：MØBIUS 的干预是「同一种证据，换一个选择者」，SWE-agent 的任务是 issue 散文，没有可机械匹配的指称对象集合，只能拿 diff 当 B——变量变成了「状态对叙述」，那是 false success 那篇已经测过的另一个主张。另外 B 臂 37/200 解析失败，A/B 只能在 160 条上比。**不算通过。**

**第二次在机制层通过。** 把主张改成可移植的问法——「判官的证据覆盖范围，是否取决于被判方的选择？」——立刻在 browser-use 里找到第二个宿主：它的生产路径有独立判官，文本证据是 agent 自写的结语加 agent 所选动作的返回，唯一不由 agent 撰写的是末若干张截图；裁决是布尔值，没有第三态；提示里写着，如果截图里看不到 agent 提取的信息，可以假定它在那里 [[11]](#ref-11)。两个系统都把证据覆盖权留给被判方，只在吸收不确定性的方式上相反：MØBIUS fail closed，付活性；browser-use fail open，付可靠性。

**第三次在效应量层部分通过。** browser-use schema 的公开轨迹集（webarena-infinity，只收成功轨迹）上抽 25 条，同一判官谓词：只喂 agent 自述，established 3/25；只喂末 3 张截图，15/25。3/25 部分是定义性的——判官谓词明写「声明不是证据」，只喂声明当然判不了；可辩护的读法是「agent 撰写的文本里几乎没有非声明性内容」。按指令是否含全称／极值量词（every、only、highest…）分层，截图臂的可判定率从 13/17（76%）掉到 2/8（25%）：固定大小的证据窗口覆盖不了无界或跨页的指称集合。**但假阳性方向测不了**（语料里全是成功轨迹），而那正是 browser-use 的设计所冒的风险。另外，MØBIUS 上「完整最终快照对跨时间标准 9/9 判不了」这条，在这里**没有复现**（跨时间型 2/7、状态型 7/18）——这里的截图是末 3 帧而不是单一快照，所以那条结论只对「只有最终快照」成立。

### 归约：monitorability，以及 useful ≠ novel

9 月 22 日早上，研究负责人对这条线做了先验工作闸门。Bollig 的 runtime verification 讲义把 `cannot-tell` 这种三值裁决给出了认知语义（true 当 $$K_a\hat\varphi$$、false 当 $$K_a\neg\hat\varphi$$，否则 inconclusive），把「此观察者下能否判定」定义为 monitorability，并证明它可判定 [[12]](#ref-12)；monitorability 本身的经典定义更早 [[13]](#ref-13) [[14]](#ref-14)。快照判不了跨时间标准，是过去时模态的教科书内容。

归约暴露出一个有意思的缝：讲义里每个 agent 的可观察命题集 $$AP_a \subseteq AP$$ 是**固定的系统参数** [[12]](#ref-12)；而在 MØBIUS 与 browser-use 里，有效的 $$AP_a$$ 由被判方在运行时选择。噪声 RV 的框架处理观察被污染，不处理观察范围被某一方选择 [[15]](#ref-15)。

$$
\mathrm{Mon}(S,\varphi \mid AP_a) \quad\longrightarrow\quad \mathrm{Mon}(S,\varphi \mid AP_a(\pi))
$$

<div class="eq-note">

左边是标准理论的对象：观察字母表固定。右边是 agent runtime 里实际发生的：字母表依赖被判方的策略 $$\pi$$。这里不主张任何定理，只主张标准理论的适用前提在这类系统里不成立。

</div>

我当时把它叫做 **verification-input ownership**：验证方的输入由被验证方决定。这比「让 LLM 判官判得更准」高一层，手上还有单系统 58.8 pp、跨系统 76%→25%。

它作为主要新意只活了大约两个小时。第一刀，RTLola 的 active monitoring：monitor 根据规格与内部状态**自己决定**查哪个 sensor、多久查一次 [[16]](#ref-16)——「验证器不该让被验证系统决定观察什么」这个一般思想已经在那里。第二刀，Goal-Autopilot 把自然语言目标外化为带门的状态机，要求可证伪的门真的执行并通过才能宣布 done [[17]](#ref-17)。第三刀最致命，IRA：评估器先从任务指令生成完成条件，再**自己选择**系统、应用、GUI 工具去环境里取证，321 条轨迹上 86.9% 准确率 [[18]](#ref-18)。还有一刀来自我们自己：MØBIUS 的 ADR 0021 §4 在 9 月 13 日就写过「runtime 自己拥有的 look 仍是更好的长期答案……It is named, not taken」，ADR 0041 在 18 日把它采纳了。

所以 **criterion-directed active observation** 不能当论文头条。它不是没用——57.1 pp 是真的，browser-use 那个 fail-open 的提示也是真的——而是：

> **useful ≠ novel。**

| 链条 | 记录 |
|---|---|
| prediction | 按指称路由使 `cannot-tell` 下降约 27 pp |
| measurement | 32.4 pp（弱判官，闸门 64.2%，绝对率作废）→ 57.1 pp（原判官，闸门 79.2%）；ADR 0045 之上 58.8 pp，n=68；browser-use 覆盖 76%→25% |
| interpretation | 判官的输入由被判方选择；$$AP_a$$ 内生 |
| correction | 两处口径错误（n=18→22；中途裁决与 checker 比）；T 有一条持续假阴性；SWE-agent 复现换掉了自变量；跨时间预测在第二系统未复现 |
| final status | <span class="st st-measured">MEASURED</span> 作为测量维度保留；<span class="st st-prior">PRIOR ART</span> 作为机制（active monitoring、IRA、Goal-Autopilot、ADR 0021/0041） |

## 三 · Completion attribution（9 月 22 日上午）

### 问题

如果第三方在 agent 等待期间制造了目标状态，而完成判定只看到目标状态成立，agent 会不会拿到一份自己没有完成的 credit？

$$
\mathrm{Goal}(S_t) = \mathit{true} \;\not\Rightarrow\; \mathrm{AccomplishedBy}(\mathit{run}, \mathrm{Goal})
$$

它看起来需要因果归属：判官收到的证据只有观察，没有「这个状态由本 run 的哪个效果造成」。对动作安全，这一半早已被 ATR 否掉——他人写入只要使正当性失效就够了，不需要知道是谁写的 [[5]](#ref-5)。剩下的是完成判定这一半。

**离线先测了一次存在性。** 把 104 个 journal 按路径重建摘要时间线，找「摘要变了，而中间本 run 没有任何效果作用于该路径」的实例：6 个，全部是同一个注入夹具（world-moves 实验族的 `config.json`），其余 98 个 journal 为零。6 例里 5 例 runtime 重新升级或挂起（对「等待期间世界移动」已经 fail closed），1 例完成，但最终状态是 agent 自己的写造成的。**语料里没有一例误归属改变了完成判定**——注入的变更从来不是目标状态，这一格按构造就不存在。那是缺少检验，不是不存在。

### 预注册：从源码预测它会判 established

研究负责人读源码后写下一个确定的预测：判官看到的证据类型 `JudgedEvidence` 只有 `{id, what, content}`，三条来源全是读，没有一条是效果，所以判官在类型层面区分不了「我造成的」和「他人造成的」；而 runtime 其实精确知道自己哪个效果碰过哪个资源——它用这份信息做陈旧性剔除，源码注释甚至写着 *"A foreign change after an observation is not known here; this is a completion judgement, not a gate."*

> **prediction**：G-ext 将判 `established`；成因是事实被采集了却没送到消费者——这是「evidence exists but is not delivered」的第三个实例。

### 这个预测被自己的实验否掉了

仓库只读，没法改注入夹具，于是用从源码重建的判官做忠实的离线模拟：21 个（运行, 标准）对，取自 5 个任务，全部是 checker 通过的最后裁决，证据是标准所指文件的真实内容。四个臂只差一条附加证据：

- N：没有因果信息
- S：「本 run 派发了 `fs.write`，上面的内容是本 run 自己的效果写的」
- F：「本 run 没有派发任何触及这些路径的效果，上面的内容是另一个写者写的」
- Z：「本 run 没有派发任何触及这些路径的效果」

**measurement**（重算自 `gext_offline_four_arm.csv`）：N、S、F 三臂都是 established 10、cannot-tell 11。**F 与 N 逐例相同 21/21，F 与 S 逐例相同 21/21**；F 臂 21 条理由里有 19 条根本没提那条因果信息。

因果项被明确供上去，裁决一例未动。不是判官不采信，是**不相关**：21 条标准里没有任何一个词指称施动者——*notes.md is an index linking the three files*、*settings.ini reflects every change SPEC.md lists*。判官被问的是世界的一个命题，看到它成立，答 established 是**正确的**。

然后只改标准的形状，证据一字不动：给每条标准统一加上前缀 *This run's own effects brought about the following state of the world:*。

| | 本 run 造成（S2） | 他人造成（F2） |
|---|---|---|
| 状态谓词（原样） | established 10 | **established 10** |
| 成就谓词（加前缀） | established 10 | **not-established 20**，cannot-tell 1 |

诚实情形下 S2 与 S 逐例相同 21/21——改写不引入假阴性；他人所为情形 20/21 翻为否定。为排除「前缀变长让判官更严」，又做了一个长度对照：同样长度、但不含施动者的前缀（*The following state of the world holds:*），F 臂与基线逐例相同 21/21。三种不同措辞的施动者前缀全部在 F 臂翻转（notEst 18、21、18）。这一轮重跑时原措辞的 F 臂是 18/21 而不是 20/21，两个数我都留着；翻转本身在每一种措辞下都成立，但措辞影响诚实情形的代价（有两种措辞在 S 臂引入了 1–2 条假阴性）。

**correction**：完成归属**不是证据问题，是规格问题**。源码级的机制判断（「判官缺因果项」）作废。

### 为什么退役

把它写成形式问题之后，归约是完整的：「哪个施动者造成了这个结果」就是 actual causality [[19]](#ref-19) [[20]](#ref-20)，并且已经在多 agent、部分可观测、序贯决策的 Dec-POMDP 上与 responsibility attribution 一起被处理过 [[21]](#ref-21)。轨迹一侧，process mining 的 conformance checking 已被用来度量 agent 工作流的 fidelity，且发现 18 个模型里有 10 个系统性跳过一个确认检查点 [[22]](#ref-22)——它隐式解决了归属（只看 agent 自己的轨迹），代价是需要一条参考轨迹，而且不验证世界。

还有一个没被杀死的竞争解释：「目标成立即可，谁做的无关」。它的署名支持者是 MØBIUS 自己的源码注释——**完成判定刻意不是一道门**。归属真正要紧的场合（报告的真实性、credit 分配、回滚范围、训练信号），没有一个是完成判定本身的失败。

剩下的是三条窄东西：两个系统、三类验证机制的 42 条成功条件里 0 条指称施动者（我为这篇文章重跑了一次文本检索，唯一命中是一个职位名 *Senior Agent*）；MØBIUS 的断言语言在类型层表达不了成就谓词（唯一的时间算子 `changed` 他人写入同样满足）；以及上面那张表。合起来是一个便宜的正确性改进无人采纳，加一次测量——工程建议，不是机制贡献。

| 链条 | 记录 |
|---|---|
| prediction | G-ext 判 established，因为判官证据里没有因果项 |
| measurement | 供上因果项：F==N 21/21；改成就谓词：F2 20/21 翻为否定（重跑 18/21），S2==S 21/21；长度对照 21/21 不变 |
| interpretation | 判官缺因果证据 → **错**；标准是状态谓词 |
| correction | 机制从「证据管线」移到「规格形状」；原预测作废 |
| final status | <span class="st st-retired">RETIRED</span> actual causality / conformance checking；保留为一条工程建议 |

## 四 · Transition witness 的最后一种形态：Late-Bound Witness Obligations（9 月 22 日上午）

### R2-6-split：证据越来越多，判定能力越来越弱

完成归属退役之后，账本里还有一个真实的非单调实例。R2-6-split 第一次重复里，标准 c1（*each section of the old notes.md is its own file under notes/*）的裁决序列是：

<figure class="fig">
<a href="/research/mobius-rl-r26-split.svg"><img class="fig-light" src="/research/mobius-rl-r26-split.svg" alt="R2-6-split 第一次重复中标准 c1 的裁决时间线：事件 8、23、47 为 cannot-tell，57 为 established；65 把 notes.md 改写成索引，其 basis 指向 64 的完整读取；78 第一次运行被重复守卫停止；79 第二次运行开始；87、98、105、116 为 cannot-tell，绑定证据条数 1、2、3、8。下方四个先后解释：绑定变窄（错）、前态被销毁（错）、被陈旧性规则过滤（部分）、运行边界加每资源最新规则（与 journal 和源码一致）。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-r26-split-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 2.</strong> R2-6-split 第一次重复（<code>evidence/r2/f9b27dd/P3-judge-run-b/R2-6-split/rep-1</code>）中标准 c1 的全部裁决，横轴是 journal 事件序号。[57] 判 established 之后，[65] 把 notes.md 改写成索引，第一次运行在 [78] 被重复守卫停下，第二次运行从 [79] 开始。之后四次都是 <code>cannot-tell</code>，而绑定的证据条数是 1→2→3→8。下方四行是对这个现象先后给出的四个解释，只有最后一个与 journal 和源码同时一致。</figcaption>
</figure>

**「绑定证据变少」是我们最先写下的解释。** 账本在 9 月 22 日 07:24 的版本里写着这次翻回的「成因是证据绑定变窄」。那句话没有计算过。8 分钟后的版本数了：绑定是 **1→2→3→8**，在增长。于是解释换成第二个：本 run 自己后来把 notes.md 改写成三链接索引，**销毁**了那次裁决所依赖的前态。

这时我觉得它很漂亮：一个已经成立的时间命题，被后续执行销毁了它唯一的见证。**证据越来越多，判定能力反而下降。** 我把它叫做 Temporal Witness Lifecycle。

### 先被 1996 年吸收

研究负责人对它做归约。IRA 在执行后的终态上主动取证 [[18]](#ref-18)，按构造处理不了「见证在执行过程中已不复存在」——这条分离点由它自己的形式化确立。但解法结构早就有形式理论：物化视图在不访问 base data 的条件下能否维护 [[23]](#ref-23)；以及通过导出 **auxiliary views**，让仓库视图与辅助视图合起来成为 **self-maintainable** [[24]](#ref-24)。逐项对应：标准的真值是物化视图，世界是 base data，前态被销毁是数据源不可访问，最小冻结见证就是 auxiliary views。「保存最小辅助状态，而不是复制全部历史」，1996 年已经论证过。（这两篇只取到摘要级与二手描述，标 `UNVERIFIED-FULLTEXT`。）

我自己的两个直觉也各自撞上了老工作：「被监控对象在开始时不知道，运行时看到具体值才实例化 monitor」是 parametric trace slicing [[25]](#ref-25)；「旧状态会消失，所以 monitor 必须保留足够的过去」是 past-time 监控的核心能力 [[7]](#ref-7)。

### 然后收窄成一个可以被数据杀死的形式

剩下的缝只有一条：parametric RV 假设事件已经发生、事件携带参数值、然后创建 monitor。而这里可能存在一个更危险的顺序——**资源身份只有在即将销毁其前态的那个效果被提出时，才第一次可解析**。如果 runtime 直到事件之后才绑定参数，就已经晚了。

我把它写成这样。设 $$C$$ 为成功标准，$$B_t$$ 为截至 $$t$$ 已解析的指称对象，

$$
O_t = \mathrm{Obligations}(C, B_t)
$$

效果 $$e_t$$ 被提出时公开其 footprint $$F(e_t)$$，绑定可能扩张：

$$
B_{t^+} = \mathrm{Resolve}\big(C,\ B_t,\ F(e_t)\big), \qquad \Delta O_t = O(C, B_{t^+}) - O(C, B_t)
$$

若 $$e_t$$ 会销毁这些新义务所需的前态，则必须

$$
\mathrm{Destroys}(e_t, \Delta O_t) \;\Rightarrow\; \mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)
$$

<div class="eq-note">

binding 与 instrumentation 发生在 effect boundary 的两侧，而不是普通 RV 那种 event-after-the-fact 的模型。MØBIUS 已有的 <code>#targetedLook</code> 可以在真正改世界之前插入一次 look；这个形式问的是：那个 look 的资源集，能不能从标准的晚绑定义务里导出。

</div>

第一次写出 $$\mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)$$ 的时候，我的感觉是：这可能就是那个东西。

所以下一步必须是先找能杀死它的数据，而不是写实现。杀死条件在测量前写下：

> 把每个（标准, 被改资源）对分成四类：`STATIC`（标准创建时已解析）、`LATE-SAFE`（后来才解析，但解析时尚无破坏性效果）、`LATE-CRITICAL`（只有效果 footprint 出现时才解析，而该效果立即销毁所需前态）、`UNBOUND`。**若 `LATE-CRITICAL` 基本不存在，本线退役。**

研究负责人还在测之前写下了自己的预期：`LATE-CRITICAL` 接近零，因为 R2-6-split 里晚绑定的是 `notes/` 下的**新文件名**，被销毁的前态却是字面点名的 `notes.md`——两者落在不同资源上。

### LATE-CRITICAL = 0 / 165

<figure class="fig">
<a href="/research/mobius-rl-late-bound.svg"><img class="fig-light" src="/research/mobius-rl-late-bound.svg" alt="165 个标准与被改资源对的矩阵。STATIC 126 对、LATE-SAFE 12 对、LATE 27 对；LATE 中原本存在的资源为 0，因此 LATE-CRITICAL 为 0/165。旁注：原本存在的资源前态 109/109 已捕获，75 个覆盖既有文件的写入 75/75 带 basis。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-late-bound-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 3.</strong> 165 个（标准, 被改资源）对，按绑定时点与「标准是否需要前态 × 资源是否原本存在」交叉。<code>LATE-CRITICAL</code> 所在的格为 0。27 个晚绑定资源全部是新建的；原本存在的资源，前态 109/109 已被捕获。重算自 <code>late_bound_obligations.csv</code> 与 104 个 journal。它证明的是：在这批语料里，这个理论要求的那种执行没有出现。它不证明它在别的工作负载里不会出现。</figcaption>
</figure>

**measurement**（165 对，来自 65 个 journal、102 条标准，我为这篇文章重算）：

| 绑定时点 | n | 其中资源原本存在 | 其中标准需要前态且资源原本存在 |
|---|---|---|---|
| STATIC | 126 | 97 | 47 |
| LATE-SAFE | 12 | 12 | 0 |
| LATE | 27 | **0** | **0** |

- **`LATE-CRITICAL = 0 / 165`**。换一个更苛刻的定义再测（用效果收据自己携带的前态存在性，防止「文件本有内容、runtime 从未观察、效果把它覆盖」被误分），仍是 0/165。
- **27 个 LATE 绑定全部 `pre_existed = false`**：晚绑定的资源在这批语料里都是新建的，根本没有前态可销毁。这和 9 月 19 日测到的「创建类写集不可预测，因为路径还不存在」是同一件事的两面。
- 资源原本存在的 109 个对，**109/109 前态已被 runtime 捕获**（57 个靠效果收据的 `previousDigest`，52 个靠更早的观察）。这里的单位是（标准, 资源）对；落到去重后的效果上是 75 个覆盖既有文件的已执行写入，**75/75** 的 `basis` 都指向一条更早的观察，其中 55 条是带完整内容的文件读。
- 更一般地，120 次派发的 `fs.write`／`fs.patch`／`fs.move` 里，**107/120** 的 `basis` 带 `observationId`。账本原文把这 120 次都叫做「破坏性效果」，这个说法太宽：其中 36 次是创建、9 次被拒绝。我改用上面更窄的数。
- 最尖锐的那一条：R2-6-split 事件 [65] 那次改写 `notes.md` 的 `fs.write`，它的 `basis.observationId` 指向事件 [64] 的一次完整读取——**旧 notes.md 的全文就在 journal 里，而且被销毁它的那个效果自己指着。**

理论本身很漂亮。但数据没有义务尊重漂亮。现有的「先看后改」纪律（ADR 0020、0021、0041）已经在每个破坏性效果落地前把晚绑定资源变成了 `LATE-SAFE`，而真正晚绑定的资源都是新建的。

### 第二个、第三个与第四个解释

**interpretation（账本 §40.2）**：见证没有被销毁，是被 ADR 0045 的一条陈旧性规则**过滤掉**的——判官视图按资源取最新观察，并显式排除「本 run 自己的效果使之陈旧者」。这条规则对 gate 是对的，对跨时间标准恰好过滤掉了唯一的判据。

**correction（为这篇文章核 journal 时发现）**：§40.2 的解释少了一步。第一次运行在事件 [78] 被重复守卫停下（`goal.abandoned`，*"fs.observe was already read in this run with the same arguments"*）；[79] 起是同一任务的**第二次运行**，会话号从 `session-8` 变为 `session-9`，观察序号从 1 重新计。改写之后的四次 `cannot-tell` 全部发生在第二次运行里，而 `runtime-core/src/loop.ts` 的 `#runView` 只遍历**本次运行**的 `#observations`。工程侧在 9 月 19 日的 R3 计划（F3）里其实已经写了这一点：*"Those judgements came in the mission's second run, whose view holds only that run's observations"*，并注明单次运行内的陈旧性规则「也会」把前态排除，但那是读代码得出的，未经测量。所以准确的说法是：旧 notes.md 在 journal 里、被 [65] 的 basis 指着，却因为**运行边界**（以及同一运行内的「每资源只取最新观察」与陈旧性规则）没有送到判官面前。

四个解释依次是：绑定变窄（未经计算，错）→ 前态被销毁（错，内容在 journal 里）→ 被陈旧性规则过滤（部分对）→ 运行边界加每资源最新规则（与 journal 和源码一致）。它们指向同一个类别：**evidence exists but is not delivered**。而那是一条 ADR 规则的缺陷，也就是工程，不是新抽象。

| 链条 | 记录 |
|---|---|
| prediction | 研究负责人：`LATE-CRITICAL` 接近零；杀死条件：基本不存在则退役 |
| measurement | 0/165；苛刻定义仍 0/165；27/27 LATE 为新建；109/109 对前态已捕获；107/120 带 basis |
| interpretation | Temporal Witness Lifecycle → auxiliary views（1996）；Late-Bound Obligations → 不存在 |
| correction | 「绑定变窄」→「前态被销毁」→「被陈旧性规则过滤」→「运行边界」 |
| final status | <span class="st st-killed">KILLED</span> 存在性关未过；<span class="st st-prior">PRIOR ART</span> 通用 witness preservation（auxiliary views、WAL、past-time RV） |

到这里，研究负责人在账本里写下了一张表：同一个形状已经出现了五次——**理论存在且比所需更一般，而运行时既没实现一般解，也没实现便宜的特例。** 它写道，不再沿这条线开新的候选抽象。第六次在下午。

## 五 · 换方法：从发明机制到 Jepsen 式探针（9 月 22 日 08:51）

五次同形之后，我决定正式改方向：不再从 MØBIUS 的 correctness bug 里挖第六个新机制，而是问一个能被数据直接杀死的 systems question。

还有一个方向是在这时顺手被归约掉的。ADR 0013 之后，一次 resume 会让运行内的 `#ledger` 归零，这确实违反语义；但「恢复后所有影响未来控制流的状态必须 durable」就是 durable execution 的基本要求——AWS 的文档甚至给了同构的例子：一个 step 把结果追加到外部变量，重放时 step 被跳过，那个变量停在初值 [[26]](#ref-26)；而把 crash、retry、replan 之后重新消费授权预算明确命名为 **semantic replay** 的工作也已经有了 [[27]](#ref-27)。

于是，「五次同形」被改写成一个研究问题：

> 现代 agent runtime 在多大程度上重新暴露了传统系统理论早已解决的正确性问题？这些失败为什么会重新出现，又集中在哪些 runtime seam？

候选解释是一句话：

$$
I \text{ requires } F \;\wedge\; F \in S_i \;\wedge\; F \notin \pi_{i\to j}(S_i) \;\Longrightarrow\; I \text{ may fail at subsystem } j
$$

<div class="eq-note">

$$\pi_{i\to j}$$ 是子系统边界上的投影。事实在 runtime 某处存在，不蕴含不变式在它的消费者处可执行。当时账本里的实例：journal 有 provenance 而 extractor 丢了；effect basis 有旧观察而 completion 的证据过滤丢了；runtime 有效果归属而标准不要求它；resume journal 有历史而运行内 ledger 重置。

</div>

要让它不是「先看到自己系统的 bug，再挑理论解释它」，只有一个办法：**先冻结不变式，再去打别人的系统。**

### 方法不是我们发明的

把预注册的不变式做成黑盒探针、注入故障、再用外部历史检查一致性模型，这正是 Jepsen 做的事 [[28]](#ref-28)，Elle 是它的学术化：从实验观察到的历史推断隔离异常 [[29]](#ref-29)。研究负责人在 `INVARIANT_CARDS.md` 的第一段就写了：方法论不是新的，新意如果存在，只能来自**不变式集合的选择**、**跨运行时的经验发现**，以及 **agent 特有的执行语义**。我们在 arXiv 上检索过，没有找到对现有 agent runtime 做预注册、黑盒、不变式式故障注入的工作；最近的是对 LLM API 注入故障、测 pass@1 的研究，以及一篇用 TLA+ 形式化四类并发异常、并在 LangGraph 上复现 tool-effect reordering 的预印本 [[30]](#ref-30)。只检索了 arXiv，找不到不是不存在的证据。

### 七张卡

每张卡只有四段：前置条件 → 所需运行时状态 → 违反 oracle → 经典祖先，**不含任何 MØBIUS 实现细节**，并且必须带一个正对照和一个负对照。

| 卡 | 不变式 | 经典祖先 |
|---|---|---|
| C1 stale decision / revalidation | 在 $$t_0$$ 依据状态 $$s$$ 作出的决定（含人类批准），若在 $$t_1$$ 施加前 $$s$$ 被第三方改成使决定不再正当的值，不得照常施加 | 乐观并发控制的后向验证、`If-Match`、fencing token；selective revalidation [[5]](#ref-5) |
| C2 durable consumption / semantic replay | 一次性额度在崩溃与恢复之后不得被再次消费 | durable execution 的确定性重放、exactly-once、幂等消费者 [[27]](#ref-27) |
| C3 replay-state closure | 影响未来控制流的非确定性结果必须被记录，而不是在重放时重新产生 | record–replay 的封闭性 [[26]](#ref-26) |
| C4 provenance preservation | 来源必须随事实跨越子系统边界，不得静默降级 | provenance semiring、context propagation [[10]](#ref-10) |
| C5 temporal evidence preservation | 判定关系型条件所需的前态必须在效果提交前保留并送达 | 过去时 LTL、auxiliary views、WAL undo [[7]](#ref-7) [[24]](#ref-24) [[8]](#ref-8) |
| C6 monitorability | 裁决所需的观察集合由条件的指称对象推导，而不是由被裁决方的行为决定 | monitorability、active monitoring [[13]](#ref-13) [[16]](#ref-16) |
| C7 concurrency isolation | 并发写者之间的冲突必须暴露，不得静默覆盖后各自报成功 | 隔离级别、写写冲突检测 [[29]](#ref-29) |

杀死条件也在任何探针运行之前冻结（用我自己的原话）：若在至少 5 个独立 agent runtime 上，预注册的探针绝大部分都被正确处理，或缺陷只在 MØBIUS 出现，则「systematic under-adoption」退役。反过来，只有 ≥3 个独立 runtime、≥3 个不同理论族、同一种「信息存在但跨投影后不可用」的结构、可重复触发、且修复只需少量 glue 时，论文才开始有意思。

后来我们没有为了凑论文把七张卡都跑完。原因在下面：前四格的结果已经足以改变先验，再换 subsystem 找失败，就变成了为了找到失败而换 subsystem。

<figure class="fig">
<a href="/research/mobius-rl-probe-method.svg"><img class="fig-light" src="/research/mobius-rl-probe-method.svg" alt="探针方法图：确定性 stub 驱动被测运行时；父进程在宣告的故障点注入崩溃、等待或第三方改世界；外部审计事件流与外部世界数据库给出五态判定之一。旁边两条对照轨：刻意做坏的实现必须被判违反，刻意做对的实现必须通过，否则记 probe-insensitive。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-probe-method-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 4.</strong> 探针的形状。被测运行时由确定性 stub 驱动；故障、等待或第三方改世界由父进程在宣告的故障点注入；判定只读运行时之外的审计事件流与外部世界数据库，不读运行时自述，也不读源码。同一张卡必须同时跑一个刻意做坏的实现和一个刻意做对的实现：前者必须被判违反，后者必须通过，否则整张卡记为 <code>probe-insensitive</code>，真实运行时的结果不得解读。</figcaption>
</figure>

## 六 · 我们自己的仪器，一次比一次更需要被怀疑

### LangGraph，第一个 apparent violation

第一批探针打在 LangGraph 1.2.12 上，C2 卡：额度为 3，在第二次消费时用真实的独立进程终止杀掉，恢复后继续。外部审计序列是：

```text
[1, 2, 2, 3]
```

额度 3，外部记录了 4 次消费，`n=2` 出现两次。在它最强的 durability 档 `sync` 下也是如此。而同一次运行里，runtime 自述的最终状态是：

```text
{"spent": 3, "limit": 3, "done": true}
```

按它自己的账本，额度没有超支。如果 oracle 采信运行时自述，这个违反是不可见的。正对照同时 100% 报违反（`[1, 2, 1, 2, 3]`），负对照干净。

那个结果漂亮得让我第一反应是保存它，而不是怀疑它。它太像一个 paper result 了：外部审计与内部自述不一致，最强档位下仍然发生，探针的敏感性有正对照背书。研究负责人把它记成 `VIOLATED`，并补了一段白盒对照：LangGraph 包内以 `idempotency_key|dedupe_key|effect_id|operation_id` 为名的字段 0 命中，而 Temporal 有明文的 exactly-once 与 idempotent。读起来就是「durable execution 引擎有、agent runtime 没有」。

所以第二件事必须是怀疑它。

同一份文件的 §4 自己就写着，「at-least-once 加要求步骤幂等可能是该运行时明示的契约」是「下一步第一件事」——却在 §1 的表里先写了 `VIOLATED`。**判定发在了契约核验之前。**核官方文档之后：LangGraph 的 durable execution 是 **replay**，不是从崩溃的那一行继续；`interrupt()` 恢复时从整个 node 的开头重新执行；文档要求把副作用和非确定性操作包进 task，并明确警告一个已开始但未完成的 task 在恢复时可能再跑一次，有写副作用时要用 idempotency key 或先检查已有结果 [[31]](#ref-31)。`sync` 只承诺「在下一步开始前同步持久化」[[31]](#ref-31)，它加强的是 step 边界的持久性，不是外部效果与 checkpoint 的原子提交。

> 实验结果是真的，解释是错的。

<figure class="fig">
<a href="/research/mobius-rl-langgraph-correction.svg"><img class="fig-light" src="/research/mobius-rl-langgraph-correction.svg" alt="LangGraph 结果的三次读法：第一次，外部审计序列 1、2、2、3 对额度 3、运行时自述 spent 为 3，读成 VIOLATED；核契约，durable execution 是 replay，副作用交给应用幂等；更正后，C2-N 为 inapplicable，C2-T 用 task 得到 1、2、3，not-violated。下半部分是三个仪器错误：未类型化 StateGraph(dict) 伪造批准 A 派发 B；SQLite 跨线程错误；socksio 缺失导致 NOT-CAPTURED 并与后续行混入同一格。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-langgraph-correction-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 5.</strong> 同一组外部审计数据的三次读法。第一次读成违反；核契约后，该窗口落在运行时明文交给应用层的区间；按官方编程模型重写探针后，已完成的 <code>@task</code> 跨 SIGKILL 不被重执行。下半部分是同一天我们自己仪器犯的三个错误。这张图证明的是：外部审计序列本身没有变，变的是它与契约的对照。</figcaption>
</figure>

**correction**：`PROBE_RESULTS.md` 整份作废，文件头写着撤回理由；C3 那一格也改判——journaled 的值恢复后保留、分支不变，C3 本身是通过的，重复的外部写属于 effect semantics，不能拿来判 C3 失败。探针随后拆成两格：

- **C2-T**：按官方推荐把消费写成 `@task`，在 task 成功返回之后、下一个 durable 边界之前 SIGKILL。**结果 `[1, 2, 3]`，3/3 not-violated**——在它自己承诺的边界上是对的。
- **C2-N**：在 task 内部，外部效果已提交、task 结果尚未持久化时 SIGKILL。原始 oracle 读数 4 个效果、额度 3。但这个窗口被运行时明文交给了应用层，**记 `inapplicable` + `contract_relation = explicitly-outside-guarantee`，不进入 C2 的违反分母。**

「是否违反」和「这个不变式是否属于运行时的契约」是两个问题。后者从此成为每一行结果上一个正交的字段，而不是塞进五态里的第六态。

### `StateGraph(dict)`：一个完全由我们制造的违反

重写后的第一批 LangGraph 行里，C3-W（跨人类等待的 proposal 同一性）给出了几乎完美的 replay-state closure 失败：

```text
approval for A  →  resume  →  dispatch B（无新的批准）
```

它比 `[1,2,2,3]` 更像论文结果，因为它正好是审批线研究了三周的那个失败形状。

这一次，研究负责人在报任何 LangGraph 结果之前停了下来：C2-T 一个 task 都没跑（`models=[]`）；C2-R 只有 2 个效果，说明第二阶段根本没执行消费——那个 `not-violated` 是假的；C3-W 用的是未类型化的 `StateGraph(dict)`。事件流是决定性的：第二阶段里 `propose` **没有**重跑，是 `dispatch` 发现 `state["proposal"]` 不存在，于是重新向 stub 要了一个，得到 B。在未类型化的 schema 下，整个 state 是一个只保留最后值的根通道——`gate` 节点返回 `{"approved": True}`，就把根状态整个替换掉了，`proposal` 被 harness 自己抹掉。（这一点我们后来在 LangGraph 1.2.12 上直接运行核过：输入 `{'x': 1}`，节点返回 `{'b': 2}`，结果是 `{'b': 2}`。[[31]](#ref-31)）同一个 bug 也解释了 C2-R 只有两个效果：`approve` 返回时把 `budget` 抹掉，恢复后立即结束。

研究负责人当时写下的检验是：「不注入任何故障地跑 C3-W。若无崩溃也丢 proposal，就 definitively 是我的 bug。这个 no-fault 基线本该一开始就有。」

我得诚实地记录这一步实际发生的顺序，因为它和我最初的记忆不同：修 schema（`StateGraph(S)`，`TypedDict`）与加 no-fault 基线**是在同一步里做的**，所以基线从来没有在 `dict` schema 下跑过。基线还先暴露了第二层问题——对基于 `interrupt()` 的探针，「不注入故障」时进程也会停在 interrupt，正确的基线是**同进程内恢复**。补上之后，四个基线在类型化 schema 下全部正确：C3-W 只调用模型一次，派发 A，没有重新生成。把先前那个 `violated` 定为 harness 缺陷的证据，是事件流（`propose` 未重跑、`proposal` 在 `gate` 之后消失）加上类型化 schema 下的正确基线；「无崩溃也会丢状态」这句话，不在记录里。

同一轮还修了第三个：外部世界的 SQLite 连接被 LangGraph 的工作线程使用，抛 `SQLite objects created in a thread can only be used in that same thread`，C2-T 因此根本没跑起来，先前记为 `NOT-CAPTURED`。

有时候最需要被怀疑的不是被测的 runtime，而是自己的实验。一个伪造的违反和一个真实的违反，在 oracle 的输出上完全一样；能区分二者的只有 no-fault 基线和逐条的外部事件流。从那以后，no-fault 基线是每一个真实运行时格的前置条件。

### socksio 与混合账本

C1 卡的第一次 OpenAI Agents SDK 运行，三行全是 `NOT-CAPTURED`。原因与 agent 无关：沙箱导出了 SOCKS 代理变量，SDK 的 tracing exporter 在导入时构造 httpx 客户端，因为没装 `socksio` 抛了 `ImportError`。这是纯环境修复。

问题出在后面。结果表按规定只能从 `rows.jsonl` 自动生成，不得手写汇总数字。生成表时，稳定性检查报出：

```text
unstable: [('openai-agents', 'C1-RV')] | C1 rows: 27
```

同一格里混着 socksio 失败时的三行 `NOT-CAPTURED` 和修好之后的三行 `not-violated`。那三行来自不同的 harness 配置，不能同格混算，也不能手工删掉。处理方式是：把整个混合账本按 append-only 原则归档为 `rows_archive_mixed.jsonl`（60 行），C2/C3 的行另存为 `rows_c2c3.jsonl`（33 行），再用最终的 harness 把 C1 全套重跑成干净的 24 行。归档文件今天还在，里面那三行 `NOT-CAPTURED` 的 stderr 尾部仍然是那个 `ImportError`。

### 正负对照与五态

这三件事之后，方法定成了这样：每一个探针都必须同时存在一个 **deliberately broken control** 和一个 **deliberately correct control**。前者必须被抓出来，后者必须通过；两者没有 100% 分开，这张卡记为 `probe-insensitive`，真实运行时的 PASS 不得被读成系统正确。

每一格只能落在五态之一：

```text
violated           运行时声明了相关面，探针到达故障点，oracle 信息充分，不变式被破坏
not-violated       探针到达故障点，oracle 信息充分，不变式成立
NOT-CAPTURED       相关路径执行了，但判定所需的证据没有暴露或不可持久观察
probe-insensitive  正对照没有触发 oracle
inapplicable       运行时不提供该卡所需的语义面
```

两条我反复提醒自己的：**`inapplicable` 不是 PASS**，它不进入分母；**`NOT-CAPTURED` 不是 violation**，它说明的是仪器看不到。第一个 LangGraph 结果如果早有这套词汇，它会一开始就被记成「待核契约」，而不是 `VIOLATED`。

## 七 · C1 / C2 / C3：负结果（9 月 22 日 09:16–10:08）

### LangGraph 1.2.12

控制敏感性闸门先过：三张卡的正对照 9/9 报违反，负对照 9/9 干净。然后（每格 3 次，判定全部一致，重算自 `rows_c2c3.jsonl`）：

| 探针 | 故障点 | 判定 | 模型调用 | 外部效果 / 额度 |
|---|---|---|---|---|
| C2-T | `AFTER_ACK_BEFORE_NEXT_STEP` | not-violated | A, B, C | 3 / 3 |
| C2-R | `AT_WAIT` | not-violated | A, B, C | 3 / 3 |
| C3-W | `AT_WAIT` | not-violated | A | 1（派发 A） |
| C3-C | `AFTER_CHECKPOINT_BEFORE_WAIT` | not-violated | A | 1（分支与故障前一致） |
| C2-N | `AFTER_EFFECT_COMMIT_BEFORE_ACK` | inapplicable · explicitly-outside-guarantee | A, B, C, D | 4 / 3（不进分母） |

已完成的 task 跨 SIGKILL 恢复不重新执行；journaled 的值和分支在恢复后保持；节点内的外部效果在 ack 之前崩溃会被 replay，而官方契约明确把这个窗口交给应用的幂等。

### OpenAI Agents SDK 与 Pydantic AI：P-FOREIGN

C1 这次冻结得比「任何批准后世界变了，runtime 都必须发现」更窄，因为多数框架没有承诺后者：

> 若运行时提供并声明一个批准后重新执行的 validation / guardrail seam，则在等待期间外部世界变化后，该 seam 必须基于新世界重新求值；旧的验证结果不得被当作当前事实继续使用。

形式上，$$V(a, S_0) = \mathit{allow}$$，等待期间 $$S_0 \xrightarrow{\text{foreign}} S_1$$，人批准的是同一个 $$a$$。若运行时声称执行前重新验证，就必须求 $$V(a, S_1)$$；当 $$V(a,S_0)=\mathit{allow} \wedge V(a,S_1)=\mathit{deny}$$ 时，合法结局只有 deny、escalate、replan，不得 dispatch。

两个运行时都打在它们自己明文承诺的机制上，不是我们发明的标准。OpenAI Agents SDK 的 `pre_approval_tool_input_guardrails` 的 docstring 写着：同一组 guardrail 在批准之后、工具执行之前会再跑一次 [[32]](#ref-32)。Pydantic AI 的 `args_validator` 在 schema 校验之后、执行之前运行，批准之后会再跑一次，此时 `tool_call_approved=True` [[33]](#ref-33)。两者都自带确定性测试模型（`ScriptedModel`、`FunctionModel`），不需要真实模型或 API key。AutoGen 没有纳入：它的文档说，run 内等待 `UserProxyAgent` 会让 team 处于不能保存或恢复的不稳定状态 [[34]](#ref-34)——按规则它先记 `inapplicable`，而不是拿来凑第三个系统。

首轮只有「改世界」一个变量，不注入崩溃，免得失败时分不清是 stale decision 还是 durability。

<figure class="fig">
<a href="/research/mobius-rl-c1-timeline.svg"><img class="fig-light" src="/research/mobius-rl-c1-timeline.svg" alt="C1-RV 时间线：验证看到版本 1 未保护，放行；审批等待；第三方把世界改为版本 2 受保护；人批准；批准后的验证看到版本 2，拒绝；破坏性效果 0；validation_world_versions 为 1、2。对照：刻意做坏的实现只验证一次，缓存放行，在版本 2 上执行，破坏性效果 1。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-c1-timeline-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 6.</strong> C1-RV 的时间线：第一次验证看到版本 1、未保护，放行；进入审批等待；第三方把世界改成版本 2、受保护；人批准；批准后的验证看到版本 2，拒绝；破坏性效果为 0。右侧是刻意做坏的对照：只验证一次、缓存 allow，于是在版本 2 上照样执行。核心证据是外部事件流里的 <code>validation_world_versions</code>，不是运行时自称「我重新验证了」。这张图不证明运行时自己察觉了世界变化——察觉变化的是我们写在 seam 里的验证器。</figcaption>
</figure>

**measurement**（重算自 `rows.jsonl`，每格 3 次）：

| 运行时 | 探针 | 判定 | `validation_world_versions` | 决定 | 破坏性效果 |
|---|---|---|---|---|---|
| openai-agents 0.22.3 | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| pydantic-ai 2.47.0 | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| broken-control | C1-RV | violated | `[1]` | allow | 1 |
| correct-control | C1-RV | not-violated | `[1, 2]` | allow, deny | 0 |
| 两个运行时 | C1-RAW（不挂 seam） | inapplicable | `[]` | — | 1（不进分母） |

这张卡真正的证据不是运行时说「我重新验证了」，而是外部 oracle 看到验证器**真的访问了两个世界版本**：

```text
validation_world_versions = [1, 2]
```

Pydantic AI 那一侧还多一条：第一次验证 `tool_call_approved = false`，第二次 `tool_call_approved = true`——运行时自己的标志确认第二次就是批准之后的那一次。oracle 还区分出一种此前会被误判为通过的情形：没有破坏性效果，但也没有任何批准后的验证调用——那无法区分「重验并拒绝」与「根本没再尝试」，记 `NOT-CAPTURED`。C1-RAW 两格记 `inapplicable`：它存在的唯一意义，是说明 **approval identity ≠ freshness guarantee**。

还有两件事这个结果没有证明：首轮不含崩溃，所以不涵盖「跨进程恢复之后 seam 是否仍被重新调用」；以及上面说过的，察觉变化的是我们的验证器，不是运行时。

累计：3 个真实运行时，C1/C2/C3 的 5 个适用格，**适用格违反数 0**，每一格都有 100% 检出的正对照。

## 八 · Delegated Obligation Closure：当轮被杀（9 月 22 日 10:19–10:24）

两轮负结果之后，我又产生了一个新想法。runtime 没有违反不变式，是因为它把 obligation 推给了 application（C2-N、C1-RAW 都是这样）。那么新的问题可能是：

> 当 runtime 明确把一个 correctness obligation 交给 application 时，它是否同时暴露了足够的稳定机制，让 application 能在 runtime 自己的 replay / resume 语义下真正履行它？

先承认它的祖先：「责任最终必须由端点完成」就是 End-to-End Arguments，而那篇文章的典型例子恰好是 duplicate suppression 与 delivery acknowledgement——底层能做的是性能上的辅助，完整的正确性只能在端点实现 [[35]](#ref-35)。幂等作为应用层的纪律也早有经典表述 [[36]](#ref-36)。所以不测「为什么推给应用」，只测：

$$
\mathrm{delegates}(R, O) \;\Rightarrow\; \exists M_R :\ M_R \text{ is sufficient to discharge } O
$$

其中 $$M_R$$ 必须全部来自公开、文档化的 API——不读内部 checkpoint，不 patch runtime，不自建恢复系统。三个能力条件：stable identity（replay 前后能识别同一个 logical effect）、boundary access（应用在效果之前有机会施加缓解）、durable reconciliation（应用能查询已提交的结果）。全真记 `closed`，缺一记 `open`。不用代码行数当指标。

### 一次 grep 造成的错误推断

这里先要撤回一条我们自己的断言。第一次 LangGraph 探针的白盒对照里，`idempotency_key`、`dedupe_key`、`effect_id`、`operation_id` 在包内 0 命中，我们据此推断：

> LangGraph 要求 idempotency，却不给实现它的工具。

这个推断的唯一依据是一次字符串检索。它只能说明**没有叫这些名字的字段**。

### C2-NI

LangGraph 1.2.12 公开暴露 `Runtime.execution_info`，经公开的 `get_runtime()` 取用，字段有 `thread_id`、`run_id`、`checkpoint_id`、`checkpoint_ns`、`task_id`、`node_attempt`（这些字段在 1.1.5 才补齐）[[31]](#ref-31)。探针打在 C2-N 那个窗口上——外部效果已提交、task 尚未确认时进程死亡——但应用按运行时自己推荐的方式实现缓解，键只用公开字段构造：

```text
key = thread_id | checkpoint_ns | task_id | i
hit = idem.lookup(key)            # 外部效果库，PRIMARY KEY + BEGIN IMMEDIATE
if hit: return hit                # 复用已提交结果
else:   idem.commit(key, payload)
```

正对照是同一个探针的 `unstable` 模式：键每次由 `uuid4()` 新生成。

跨真实 SIGKILL 与全新进程，外部事件流是这样的：

```text
pid 70399  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…
pid 70399  idem.lookup           hit=False   before_effect=True
pid 70399  effect.committed
pid 70399  faultpoint.reached    AFTER_EFFECT_COMMIT_BEFORE_ACK      ← 父进程 SIGKILL
pid 70400  execution_info.read   checkpoint_ns=flow:a4c98e6f…|effectful:95673099…   ← 逐字节相同
pid 70400  idem.lookup           hit=True    before_effect=True
pid 70400  effect.reused
pid 70400  tasks.completed
```

**measurement**（重算自 `rows.jsonl`，每模式 3 次，全部 `phase1_returncode = -9`）：稳定键模式外部效果 **1 个**，三个能力条件全真，not-violated 3/3；不稳定键的正对照外部效果 **2 个**，violated 3/3。六个字段跨崩溃与跨进程**全部稳定**，其中两个与预期相反：`run_id` 在第二次 invoke 后没有变，`node_attempt` 在重试后也没有递增——这只让结论更强，应用不必挑字段。

**Delegated Obligation Closure 当轮被杀。** 剩下的只是一个被 End-to-End Arguments 覆盖的正常分层选择。

> 字符串不存在 ≠ capability 不存在。

这是这几天我最想留下的方法教训之一，因为它的错法是最自然的那种：grep 很便宜，0 命中看起来像证据。

边界也要随结论一起说：单一运行时、单一窗口、单一 task；外部库的原子性是我们自己实现的——这证明运行时提供了构造稳定键所需的信息，不证明任意外部系统都提供条件写原语。

### correctness-under-adoption 停止

按预写的决定：这一刀 PASS，就停止沿 correctness-under-adoption 继续挖，包括不做 C7。累计：

| 卡 | 机制 | 运行时数 | 适用格违反数 |
|---|---|---|---|
| C1 | 明文的批准后重验 seam | 2 | 0 |
| C2 | 文档化的 durable 边界 | 1 | 0 |
| C3 | replay 状态封闭 | 1 | 0 |
| C2-NI | 被委派义务的可履行性 | 1 | 0（closed） |

正式的退役条件要求扩展到至少 5 个适用的独立运行时。我们没有扩展，所以严格说它没有被「触发」；它被**停止**了。理由是：再换 subsystem 很容易变成为了找到一个失败而换 subsystem。有一个事实我必须和这个停止放在一起说：我们没有测的 C7 恰好是那篇 TLA+ 预印本报告在 LangGraph 上复现了 tool-effect reordering 的那一族 [[30]](#ref-30)。所以这个负结果的范围是 C1–C3 的这几个窗口，不是「LangGraph 没有并发问题」。

这一阶段最有价值的结论是一个负结果：我们连续提出多个「agent runtime 可能重新犯经典系统错误」的假说，但在把**契约、适用范围、应用责任、公开的缓解机制**四者分开之后，apparent violations 消失了。它们的消失不是测量不敏感造成的——每一格都有 100% 检出的正对照。

还要说清规模：这一整段（七张卡冻结到 C2-NI）发生在 9 月 22 日上午大约两个小时里；驱动是确定性 stub，每格 3 次。它是一个 pilot，不是一篇测量论文。它的价值是改变先验，不是给出比率。

## 九 · FTR 的强形态，和它的归约关（9 月 22 日 10:30–10:52）

### 强形态长什么样

上一篇写的是 FTR 的形式化与它按自己的判据退役。但那一版没有恢复它最强的样子。它最强的样子画在 V42 的 runtime 架构图最下面那条点线带里：多个执行 actor 各自在看到别人之前封存自己的预测；一个共享的证据场记录 provenance、dissent、evidence ancestry，并坚持「来源之间的一致不等于独立」；竞争假设与候选轨迹；active falsification——找能区分两个假设的最便宜实验，必要时 execute-for-information；一个 epistemic scheduler，把算力花在决策真正取决的那份不确定性上，在 reason、ask、test、fork、observe、act 之间调度；reality admission——前提新鲜吗？证据独立吗？还有便宜的 falsifier 没用吗？不确定性可以接受吗？——然后才进入今天已有的 authority / resource / invariant gates；效果提交后，按 proper scoring 回写到每个预测者的校准。

<figure class="fig">
<a href="/research/mobius-rl-ftr-strong.svg"><img class="fig-light" src="/research/mobius-rl-ftr-strong.svg" alt="FTR 强形态架构图，取自 V42 架构图的研究前沿带：多个执行 actor、证据场、竞争假设、主动证伪、认知调度器、现实准入、现有 gates、效果、校准，以及 forecast contract、未来证据需求 Omega 星与 A safe。每个节点标注其归约对象：belief state 与 ATMS、贝叶斯实验设计与信息价值、理性元推理、POMDP shield、dual control、epistemic fault domains、proper scoring、output commit。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-ftr-strong-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 7.</strong> FTR 的强形态，节点与连线取自 V42 runtime 架构图（Graphviz）的 research frontier 带，以及 9 月 22 日作者给出的 $$\mathcal{F}_t = \{(h_i, E_i, O_i, A_i)\}$$ 表述；用 Graphviz 重绘。每个节点右侧的标签是归约关把它归到的已有对象。点线节点从未实现；图里唯一会改变执行语义的是 $$A^{\mathrm{safe}}_t$$，它对应 partial observability 下的 shield。这张图证明的是强形态被逐项归约；它不证明这些部件作为工程架构没有用。</figcaption>
</figure>

9 月 22 日我给了它一个比仓库里任何版本都强的表述：

$$
\mathcal{F}_t = \big\{ (h_i,\ E_i,\ O_i,\ A_i) \big\}
$$

<div class="eq-note">

每个假设 $$h_i$$ 携带当前支持证据 $$E_i$$、下一步需要获得的观察义务 $$O_i$$、在它尚未被消除时允许的动作集 $$A_i$$；runtime 自己执行 split、merge、eliminate；动作一旦 commit，会反过来约束仍然合法的未来假设。

</div>

以及一个真正值得杀的性质：

$$
A^{\mathrm{safe}}_t = \bigcap_{h \in \mathcal{F}^{\mathrm{live}}_t} A(h)
$$

<div class="eq-note">

runtime 只有在所有仍然可能的世界都允许一个不可逆动作时才能直接 commit；否则应该观察、延迟、分支或升级。问题从「agent 相信什么」换成「不确定性改变了 runtime 被允许／被要求做什么」。

</div>

再加上上一篇保留下来的那个量——未来的证据需求：

$$
\Omega_t^{*} = \arg\min_{\Omega}\ \mathrm{Cost}(\Omega) \quad \text{s.t.}\quad \forall h_i, h_j:\ E_\Omega(h_i) = E_\Omega(h_j) \Rightarrow C(h_i) = C(h_j)
$$

杀死条件由我在批准归约关时写下：若存在简单映射 $$\mathrm{FTR} \equiv \mathrm{BeliefState} + \mathrm{Planner} + \mathrm{Monitor}$$，而 MØBIUS 只是在 TypeScript 里把它们拼起来，FTR 退役，不做实现。并且：**如果它也死，我们就知道 MØBIUS 的论文价值不在新的 systems abstraction。**

### 逐项归约

<figure class="fig">
<a href="/research/mobius-rl-reduction-map.svg"><img class="fig-light" src="/research/mobius-rl-reduction-map.svg" alt="七个候选与杀死它们的东西的连线图：completion attribution、transition witness、late-bound obligations、observation ownership、correctness-under-adoption、delegated obligation closure、FTR，分别连到实验、先验工作、官方契约与控制组。" loading="lazy" /><img class="fig-dark" src="/research/mobius-rl-reduction-map-dark.svg" alt="" aria-hidden="true" loading="lazy" /></a>
<figcaption><strong>Figure 8.</strong> 七个候选与杀死它们的东西：实验（实线）、先验工作（虚线）、官方契约（点划线）、控制组（点线）。多数候选被不止一样东西击中。这张图证明的是「被什么杀死」；它不给出任何方向的工程价值。</figcaption>
</figure>

| FTR 强形态的部件 | 已有对象 | 映射 |
|---|---|---|
| 竞争假设、带标签的假设集、级联撤回 | ATMS [[37]](#ref-37)；belief state 作为历史的充分统计量 [[38]](#ref-38) | 完整：带证据的原子假设集就是 belief 的一种表示；2026 年的 Agent-BRACE 把 belief 表示为一组带有序确定度标签的原子自然语言断言，policy 只条件于它 [[39]](#ref-39) |
| 选哪个实验、execute-for-information | Bayesian experimental design [[40]](#ref-40) [[41]](#ref-41) [[42]](#ref-42)；value of information [[43]](#ref-43) | 完整：「最便宜的区分性实验」是 EIG／EVSI 的特例 |
| 在 ask / test / fork / observe / act 之间调度 | rational metareasoning、value of computation [[44]](#ref-44) [[45]](#ref-45) | 完整；早先的 frontier 复审还指出过原优先级公式重复计数了 P(decision change) |
| 不确定下的动作许可 $$A^{\mathrm{safe}}_t$$ | 部分可观测下的 shielding [[46]](#ref-46) [[47]](#ref-47) | 完整，且更强：shield 只允许从获胜的 belief support 出发、仍停留在获胜区域的动作；只需知道可能的转移，**概率与奖励可以不指定** [[47]](#ref-47) |
| 效果同时是控制与探测 | dual control [[48]](#ref-48) [[49]](#ref-49) | 完整 |
| 证据 ancestry、agent 数不等于证据独立 | epistemic fault domains [[50]](#ref-50)；epistemic Sybil [[51]](#ref-51)；Sybil attack [[52]](#ref-52)；多版本软件的非独立失效 [[53]](#ref-53) | 完整：κ_E 可从 provenance 算出，增加投票者不能提高它 |
| forecast 打分与校准 | proper scoring 与 calibration [[54]](#ref-54) [[55]](#ref-55) [[56]](#ref-56)；以及「calibration is not control」[[57]](#ref-57) | 完整，并且后者说明校准分数不应进 gate |
| 把 forecast 当一等运行时状态并独立验证 | 把自主决策分解为 information、beliefs、forecasts、actions、utility 并各自验证的 POMDP 框架 [[58]](#ref-58) | 大部分 |
| 不可逆外化之前的屏障 | output commit problem [[59]](#ref-59) [[60]](#ref-60) | 完整 |

研究负责人原本准备了一个辩护出口：「POMDP 与 conformant planning 需要已知的概率模型，agent runtime 没有」[[61]](#ref-61) [[62]](#ref-62) [[63]](#ref-63)。Carr 等人的全文把这条堵死了——shield 由可满足性求解计算，只需 partial model。

有一个容易搞反的结果值得单独写：**2026 年的最近邻并不杀它，经典侧才杀它。** 对两篇最接近的 2026 年工作做全文词频，Agent-BRACE 与 Dixon 在「许可／义务」这条轴上几乎完全沉默（`obligation` 两篇都是 0，`runtime` 两篇都是 0）。我那句收窄——不问 agent 相信什么，问不确定性改变了 runtime 被允许做什么——确实甩开了 agent 文献。杀死它的是部分可观测下的 shield 与 output commit 这两个更老的对象。如果只核 agent 侧，这个方向会被误判为存活。

另一半在仓库里：FTR 自己的三层协议写着它**没有 effect authority、不进 gate、只收窄**（`FTR_FRONTIER_RESEARCH.md` §7）。一个明确不改变执行语义的对象，定义上就是 monitor。而 frontier 复审早在 9 月初就写过：「FTR as a better monitor」被放弃——它在结构上是 Proof-of-Execution 的非权威观察面加上带置信度的预测，而运行时保障用 plant model 加已验证的回退解决「谁监控监控者」，FTR 两者都没有。代码侧，`grep -ril ftr packages` 今天仍是 0 命中。

研究负责人还试了三个候选残余，一个都没活：假设集由模型在运行时开放生成、不可枚举——这破坏的是经典对象的保证，但也不给 FTR 任何保证，它使 FTR **更弱**，不是更新；义务是 deontic 的而不是 value-maximizing 的——knowledge preconditions 与 shield 本身就是 deontic 的形状；commit 反向约束合法假设——belief update 与带受保护核的 belief revision 已经覆盖。

### 最终态度

**判决：RETIRE。** 杀死条件成立。它是第六次同形归约：

| # | 候选 | 已有对象 | 运行时实际做的 |
|---|---|---|---|
| 1 | 判官缺因果项 | 被实验否掉（标准是状态谓词） | 供上因果项被无视 |
| 2 | 完成归属 | actual causality | 效果日志里一次语法查找 |
| 3 | 最小 witness commitment | auxiliary views / self-maintainability | 捕获时点可知，比 1996 年的问题更容易 |
| 4 | 晚绑定见证义务 | 不存在（0/165） | 先看后改已经关掉了窗口 |
| 5 | 内生观察字母表 | monitorability，可判定 | 可算而无人算 |
| 6 | FTR 强形态 | shield + output commit + belief 表示 + 验证框架 | 未实现，且自身规范禁止它改变执行语义 |

我不羞于写下这两句话：

> FTR as engineering architecture may still be useful.
>
> FTR as a new systems abstraction is currently not supported.

上一篇留下的那个问题——「行动之前，必须保留哪些事实，因为之后的证明会需要它们」——也在这几天被收窄到了尽头：它先成为 Temporal Witness Lifecycle（被 auxiliary views 吸收），再成为 Late-Bound Obligations（被 0/165 否掉）。它没有留下一个足够强的新抽象。

这个判决有一个诚实的缺口，也要一起写：催生 FTR 的那份 51 节 research brief 不在仓库里，研究负责人的启动说明明令不得凭记忆重建它。这次归约关对着的是我在对话里给出的强形态与仓库里的材料。如果那份 brief 里有一个与上表每一项都不同构的 operation，判决需要重做。

## 十 · 这几天里，我的变化

这篇文章不是论文，所以允许出现「我」。但我只想写真正发生在研究转折处的那部分。

最初，一个新的 abstraction 成形时，我会真的兴奋。$$\mathrm{Capture}(\Delta O_t) \prec \mathrm{Commit}(e_t)$$ 第一次写出来的时候，我觉得它可能就是那个东西。然后几个小时之内，一篇 1988 年、一篇 1996 年的论文，或者一篇 2026 年 7 月的预印本，把整个抽象吸收掉。

这种事发生一次，会失落。连续发生很多次以后，问题本身变了。我不再先问「它是不是新的」，而先问「什么能最快把它杀掉」。

`LATE-CRITICAL = 0/165` 出来的时候，我记得的不是失望，而是一种很具体的清醒：那个公式是对的，只是这个世界里没有它要防的那种执行。LangGraph 第一次出现 `[1, 2, 2, 3]` 的时候，有过几分钟的兴奋——它太像一个 paper result 了；核完契约之后，我不得不把刚写下的 `VIOLATED` 撤回。再后来 `StateGraph(dict)` 证明，有时候最需要被怀疑的不是 runtime，而是我自己的实验。

以前一个方向被杀，我的反应是「又没了」。这几天后来变成了「很好，这个不用再浪费半年」。再往后，negative result 本身开始像一种进展：它把一块区域从地图上划掉，而且划掉的理由写得清楚到别人可以复查。

这不是鸡汤。它有一个很实际的后果：当一个结果看起来太漂亮时，我现在的第一个动作是找它的 no-fault 基线、它的契约、它的正对照、它的 grep 之外的证据。

## 十一 · 现在的状态

| 方向 | 状态 | 依据 |
|---|---|---|
| 审批线（捕获时刻、效果形状、谁生产键） | <span class="st st-prior">PRIOR ART</span> | CommitGuard、PlanFence、S-Bus、ATR；残差 A 是一个 `O_EXCL` 缺陷 |
| 证据替换 | <span class="st st-prior">PRIOR ART</span> | false success；R2 是复现 |
| transition witness 作为原语 | <span class="st st-retired">RETIRED</span> | before-image + provenance 边 + 过去时算子 |
| 证据选择／verification-input ownership | <span class="st st-measured">MEASURED</span> · <span class="st st-prior">PRIOR ART</span> | 57.1 pp（ADR 0045 之上 58.8 pp，n=68）；active monitoring、IRA、ADR 0021/0041 |
| completion attribution | <span class="st st-retired">RETIRED</span> | actual causality；规格形状问题；一条工程建议 |
| temporal witness lifecycle | <span class="st st-prior">PRIOR ART</span> | auxiliary views / self-maintainability（UNVERIFIED-FULLTEXT） |
| late-bound witness obligations | <span class="st st-killed">KILLED</span> | `LATE-CRITICAL = 0/165` |
| recovery semantic closure | <span class="st st-prior">PRIOR ART</span> | durable execution、semantic replay |
| correctness-under-adoption | <span class="st st-killed">STOPPED</span> | C1/C2/C3 适用格违反 0；未扩展到 5 个运行时，C7 未测 |
| delegated obligation closure | <span class="st st-killed">KILLED</span> | C2-NI：公开 API 足以履行 |
| FTR 强形态 | <span class="st st-retired">RETIRED</span> | 归约关；有一个材料缺口（51 节 brief） |
| 分层确定性（能力层 0.923、内容层 0.795） | <span class="st st-open">OPEN</span> | 唯一有独有数据的正面主张；需真实模型 n=10 |
| 上一篇的 E1–E4 | <span class="st st-ne">NOT RUN</span> | 这段记录里一个都没有跑 |

## 结尾：NO PRIMARY THESIS YET

9 月 22 日上午十一点，我给研究负责人的最后一条指令，不再指定任何方向。它要做的是 autonomous research-direction discovery：不从一个 idea 开始，而从 **unexplained phenomena** 开始——系统真实行为里，有什么现象还没有一个令人满意的现有理论解释。先找现象，再归约，再杀；上面那张表里的每一条，没有新证据不得换个名字复活。「某个字段没接上」不算现象。它被明确允许交回的结论是：

```text
NO PRIMARY THESIS YET
```

写这篇文章的时候，那一轮还在进行，我不知道它会交回什么。按现在的证据，最诚实的状态就是这一行：我们还没有一个愿意称为新 systems abstraction 的 surviving primary thesis。

我们最开始希望 MØBIUS 能证明一个新的 runtime abstraction。到现在，它先证明的是一件更基础的事：一个表面上的 runtime failure，还不是一个 systems result；而一个值得做的研究方向，应该先能活过我们自己对它做的每一件事——契约核验、no-fault 基线、正对照、0/165、以及一篇 1996 年的论文。

这几天没有一个方向活过来。但每一个没活过来的方向，现在都有一条写得清楚的死因。下一个候选出现的时候，它要先从这些死因中间走过去。

---

<a class="resource-card" href="/research/evidence/2026-09-22/README.md">
  <span class="rc-title">证据包 · 2026-09-22</span>
  <span class="rc-desc">探针 harness 与逐行 ledger、正负对照、被归档的混合账本、派生数据表、研究负责人的结果文档，以及 104 个 MØBIUS run journal——本文每一个数都可以从这里重算。附 SHA256SUMS 与一个 tar.gz。</span>
  <span class="rc-meta">374 个文件 · 7.3 MB · <a href="/research/evidence/2026-09-22/mobius-evidence-2026-09-22.tar.gz">tar.gz（549 KB）</a></span>
</a>

<p class="fig-note">图的源文件：数据图由 <code>scripts/research/rl-figures.py</code> 从上文列出的结果文件生成；Figure 7 的 Graphviz 源是 <code>scripts/research/mobius-rl-ftr-strong.dot</code>。上一篇与 FTR 形式化 PDF 见 <a href="/research/">研究页</a>。</p>

### 参考文献

每条已于 2026 年 9 月 22 日按原始记录（arXiv 页面、DOI、出版社页面、官方文档或安装包源码）重新核对。方括号里是核验深度：`FULLTEXT` 为读过相关全文，`ABSTRACT-ONLY` 为只读到摘要，`UNVERIFIED-FULLTEXT` 为元数据已核、内容依据二手描述。预印本就是预印本，没有写出场次的不假定经过同行评审。

1. <span id="ref-1"></span>I. Santos-Grueiro. *Temporary Authority, Permanent Effects: Commit-Time Authorization for LLM Agents.* Preprint, arXiv:[2607.10487](https://arxiv.org/abs/2607.10487), 2026. [FULLTEXT]
2. <span id="ref-2"></span>E. Chen, S. Wang, C. G. Brinton. *Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory.* Preprint, arXiv:[2609.03340](https://arxiv.org/abs/2609.03340), 2026. [FULLTEXT]
3. <span id="ref-3"></span>S. Khan. *S-Bus: Automatic Read-Set Reconstruction for Multi-Agent LLM State Coordination.* Preprint, arXiv:[2605.17076](https://arxiv.org/abs/2605.17076), 2026. [FULLTEXT]
4. <span id="ref-4"></span>M. Rashidi. *The Balkanization of Execution-Security Research for AI Coding Agents: Isolation, Access Control, and Time-of-Check-to-Time-of-Use Vulnerabilities.* Preprint, arXiv:[2607.05743](https://arxiv.org/abs/2607.05743), 2026. [FULLTEXT]
5. <span id="ref-5"></span>Y. Lyu, Y. Ren, R. Lai, W. Liu. *From Version Conflicts to Decision Conflicts: Selective Revalidation for Long-Running AI Agents.* Preprint, arXiv:[2609.08015](https://arxiv.org/abs/2609.08015), 2026. [FULLTEXT]
6. <span id="ref-6"></span>L. Advani. *From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents.* FAGEN Workshop at ICML 2026. arXiv:[2606.09863](https://arxiv.org/abs/2606.09863). [FULLTEXT]
7. <span id="ref-7"></span>K. Havelund, G. Roşu. *Synthesizing Monitors for Safety Properties.* TACAS 2002, LNCS, pp. 342–356. [doi:10.1007/3-540-46002-0_24](https://doi.org/10.1007/3-540-46002-0_24). [FULLTEXT]
8. <span id="ref-8"></span>C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, P. Schwarz. *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging.* ACM TODS 17(1):94–162, 1992. [doi:10.1145/128765.128770](https://doi.org/10.1145/128765.128770). [UNVERIFIED-FULLTEXT]
9. <span id="ref-9"></span>R. Snodgrass, I. Ahn. *Temporal Databases.* IEEE Computer 19(9):35–42, 1986. [doi:10.1109/MC.1986.1663327](https://doi.org/10.1109/MC.1986.1663327). [UNVERIFIED-FULLTEXT]
10. <span id="ref-10"></span>T. J. Green, G. Karvounarakis, V. Tannen. *Provenance Semirings.* PODS 2007, pp. 31–40. [doi:10.1145/1265530.1265535](https://doi.org/10.1145/1265530.1265535). See also P. Buneman, S. Khanna, W.-C. Tan, *Why and Where: A Characterization of Data Provenance*, ICDT 2001, [doi:10.1007/3-540-44503-X_20](https://doi.org/10.1007/3-540-44503-X_20). [UNVERIFIED-FULLTEXT]
11. <span id="ref-11"></span>browser-use. `browser_use/agent/judge.py`, commit d8110c5 (task-completion judge: final result, agent steps and screenshots; boolean verdict). [github.com/browser-use/browser-use](https://github.com/browser-use/browser-use/blob/d8110c5ff87ccba887aaa726cdb780f2f84bef8d/browser_use/agent/judge.py). [FULLTEXT (source)]
12. <span id="ref-12"></span>B. Bollig. *Runtime Verification: Monitoring, Knowledge, and Uncertainty* (lecture notes). arXiv:[2604.26753](https://arxiv.org/abs/2604.26753), 2026 — Def. 5.1 (monitorability), Thm. 5.3 (decidability), and $$AP_a \subseteq AP$$ as a fixed parameter. [FULLTEXT]
13. <span id="ref-13"></span>A. Pnueli, A. Zaks. *PSL Model Checking and Run-Time Verification via Testers.* FM 2006, LNCS, pp. 573–586. [doi:10.1007/11813040_38](https://doi.org/10.1007/11813040_38) (read in the NYU TR2006-881 version). [FULLTEXT]
14. <span id="ref-14"></span>A. Bauer, M. Leucker, C. Schallhart. *Runtime Verification for LTL and TLTL.* ACM TOSEM 20(4), 2011. [doi:10.1145/2000799.2000800](https://doi.org/10.1145/2000799.2000800). [ABSTRACT-ONLY]
15. <span id="ref-15"></span>S. A. Logan, S. Standefer, T. Ferguson. *A Formal Framework for Noisy Runtime Verification.* Preprint, arXiv:[2609.10462](https://arxiv.org/abs/2609.10462), 2026 (author order as on the arXiv record). [FULLTEXT]
16. <span id="ref-16"></span>J. Baumeister, B. Finkbeiner, F. Scheerer. *Active Monitoring with RTLola: A Specification-Guided Scheduling Approach.* Preprint, arXiv:[2507.20615](https://arxiv.org/abs/2507.20615), 2025. [ABSTRACT-ONLY]
17. <span id="ref-17"></span>Y. Deng. *Goal-Autopilot: A Verifiable Anti-Fabrication Firewall for Unattended Long-Horizon Agents.* Preprint, arXiv:[2606.11688](https://arxiv.org/abs/2606.11688), 2026. [FULLTEXT]
18. <span id="ref-18"></span>C. Shi, Y. Wu, Y. Liu, et al. *Interactive Reward Agent: GUI Task Evaluation via Environment-State Verification.* Preprint, arXiv:[2607.25904](https://arxiv.org/abs/2607.25904), 2026. [ABSTRACT-ONLY]
19. <span id="ref-19"></span>J. Y. Halpern, J. Pearl. *Causes and Explanations: A Structural-Model Approach. Part I: Causes.* British Journal for the Philosophy of Science 56(4):843–887, 2005. [doi:10.1093/bjps/axi147](https://doi.org/10.1093/bjps/axi147). [ABSTRACT-ONLY]
20. <span id="ref-20"></span>J. Y. Halpern. *Actual Causality.* MIT Press, 2016. ISBN 978-0-262-03502-6. [UNVERIFIED-FULLTEXT]
21. <span id="ref-21"></span>S. Triantafyllou, A. Singla, G. Radanovic. *Actual Causality and Responsibility Attribution in Decentralized Partially Observable Markov Decision Processes.* AIES 2022, pp. 739–752. [doi:10.1145/3514094.3534133](https://doi.org/10.1145/3514094.3534133); arXiv:[2204.00302](https://arxiv.org/abs/2204.00302). [ABSTRACT-ONLY]
22. <span id="ref-22"></span>D. Huang, J. K. Chua, Z. Wang. *Beyond Task Success: Measuring Workflow Fidelity in LLM-Based Agentic Payment Systems.* AIDS4DF Workshop at PAKDD 2026. arXiv:[2605.06457](https://arxiv.org/abs/2605.06457). [FULLTEXT]
23. <span id="ref-23"></span>F. Wm. Tompa, J. A. Blakeley. *Maintaining Materialized Views without Accessing Base Data.* Information Systems 13(4):393–406, 1988. [doi:10.1016/0306-4379(88)90005-1](https://doi.org/10.1016/0306-4379(88)90005-1). [UNVERIFIED-FULLTEXT]
24. <span id="ref-24"></span>D. Quass, A. Gupta, I. S. Mumick, J. Widom. *Making Views Self-Maintainable for Data Warehousing.* PDIS 1996, pp. 158–169. [doi:10.1109/PDIS.1996.568677](https://doi.org/10.1109/PDIS.1996.568677). [UNVERIFIED-FULLTEXT]
25. <span id="ref-25"></span>F. Chen, G. Roşu. *Parametric Trace Slicing and Monitoring.* TACAS 2009, LNCS, pp. 246–261. [doi:10.1007/978-3-642-00768-2_23](https://doi.org/10.1007/978-3-642-00768-2_23). [UNVERIFIED-FULLTEXT]
26. <span id="ref-26"></span>AWS. *Durable Execution SDK — Determinism during replay* (section “Pass data through return values, not closures”). [docs.aws.amazon.com](https://docs.aws.amazon.com/durable-execution/patterns/best-practices/determinism/), accessed 22 Sep 2026. [FULLTEXT (docs)]
27. <span id="ref-27"></span>J. Xu, L. Fan, Z. Wang, et al. *Beyond Single-Use Tokens: Durable Authorization State for Replay-Resistant LLM Agent Actions.* Preprint, arXiv:[2608.01710](https://arxiv.org/abs/2608.01710), 2026. [ABSTRACT-ONLY]
28. <span id="ref-28"></span>K. Kingsbury. *Jepsen* — a framework for distributed-systems verification with fault injection, and its published analyses. [jepsen.io](https://jepsen.io); [github.com/jepsen-io/jepsen](https://github.com/jepsen-io/jepsen). [FULLTEXT (project pages)]
29. <span id="ref-29"></span>K. Kingsbury, P. Alvaro. *Elle: Inferring Isolation Anomalies from Experimental Observations.* PVLDB 14(3):268–280, 2020. [doi:10.14778/3430915.3430918](https://doi.org/10.14778/3430915.3430918). [FULLTEXT]
30. <span id="ref-30"></span>S. Khan. *Verified Detection and Prevention of Concurrency Anomalies in Multi-Agent Large Language Model Systems.* Preprint, arXiv:[2606.17182](https://arxiv.org/abs/2606.17182), 2026. [ABSTRACT-ONLY]
31. <span id="ref-31"></span>LangGraph (Python) documentation and source, v1.2.12: functional API — determinism and idempotency ([docs.langchain.com](https://docs.langchain.com/oss/python/langgraph/functional-api#idempotency)); `interrupt()` and `Durability` docstrings in `langgraph/types.py`; `Runtime.execution_info` in `langgraph/runtime.py`; root-channel behaviour of an untyped state schema in `langgraph/graph/state.py` (checked by running it). Accessed 22 Sep 2026. [FULLTEXT (docs + source)]
32. <span id="ref-32"></span>OpenAI Agents SDK (Python) v0.22.3: `ToolExecutionConfig.pre_approval_tool_input_guardrails` docstring in `agents/run_config.py`; human-in-the-loop guide ([github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python/blob/main/docs/human_in_the_loop.md)); `agents.testing.ScriptedModel`. [FULLTEXT (docs + source)]
33. <span id="ref-33"></span>Pydantic AI v2.47.0: deferred tools ([deferred-tools.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/deferred-tools.md)); `Tool(args_validator=…)` and `RunContext.tool_call_approved` docstrings; `FunctionModel`. [FULLTEXT (docs + source)]
34. <span id="ref-34"></span>Microsoft AutoGen. *AgentChat user guide: Human-in-the-Loop.* [microsoft.github.io/autogen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html), accessed 22 Sep 2026. [FULLTEXT (docs)]
35. <span id="ref-35"></span>J. H. Saltzer, D. P. Reed, D. D. Clark. *End-to-End Arguments in System Design.* ACM TOCS 2(4):277–288, 1984. [doi:10.1145/357401.357402](https://doi.org/10.1145/357401.357402). [FULLTEXT]
36. <span id="ref-36"></span>P. Helland. *Idempotence Is Not a Medical Condition.* ACM Queue 10(4):30–46, 2012. [doi:10.1145/2181796.2187821](https://doi.org/10.1145/2181796.2187821). [UNVERIFIED-FULLTEXT]
37. <span id="ref-37"></span>J. de Kleer. *An Assumption-based TMS.* Artificial Intelligence 28(2):127–162, 1986. [doi:10.1016/0004-3702(86)90080-9](https://doi.org/10.1016/0004-3702(86)90080-9). [UNVERIFIED-FULLTEXT]
38. <span id="ref-38"></span>L. P. Kaelbling, M. L. Littman, A. R. Cassandra. *Planning and Acting in Partially Observable Stochastic Domains.* Artificial Intelligence 101(1–2):99–134, 1998. [doi:10.1016/S0004-3702(98)00023-X](https://doi.org/10.1016/S0004-3702(98)00023-X). The belief-state formulation goes back to K. J. Åström, J. Math. Anal. Appl. 10(1):174–205, 1965, [doi:10.1016/0022-247X(65)90154-X](https://doi.org/10.1016/0022-247X(65)90154-X). [FULLTEXT]
39. <span id="ref-39"></span>J. Singh, Z. Khan, A. Prasad, et al. *Agent-BRACE: Decoupling Beliefs from Actions in Long-Horizon Tasks via Verbalized State Uncertainty.* Preprint, arXiv:[2605.11436](https://arxiv.org/abs/2605.11436), 2026. [FULLTEXT]
40. <span id="ref-40"></span>D. V. Lindley. *On a Measure of the Information Provided by an Experiment.* Annals of Mathematical Statistics 27(4):986–1005, 1956. [doi:10.1214/aoms/1177728069](https://doi.org/10.1214/aoms/1177728069). [UNVERIFIED-FULLTEXT]
41. <span id="ref-41"></span>K. Chaloner, I. Verdinelli. *Bayesian Experimental Design: A Review.* Statistical Science 10(3), 1995. [doi:10.1214/ss/1177009939](https://doi.org/10.1214/ss/1177009939). [UNVERIFIED-FULLTEXT]
42. <span id="ref-42"></span>T. Rainforth, A. Foster, D. R. Ivanova, F. Bickford Smith. *Modern Bayesian Experimental Design.* Statistical Science 39(1), 2024. [doi:10.1214/23-STS915](https://doi.org/10.1214/23-STS915). [ABSTRACT-ONLY]
43. <span id="ref-43"></span>R. A. Howard. *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics 2(1):22–26, 1966. [doi:10.1109/TSSC.1966.300074](https://doi.org/10.1109/TSSC.1966.300074). [UNVERIFIED-FULLTEXT]
44. <span id="ref-44"></span>S. Russell, E. Wefald. *Principles of Metareasoning.* Artificial Intelligence 49(1–3):361–395, 1991. [doi:10.1016/0004-3702(91)90015-C](https://doi.org/10.1016/0004-3702(91)90015-C). [UNVERIFIED-FULLTEXT]
45. <span id="ref-45"></span>E. J. Horvitz. *Reasoning about Beliefs and Actions under Computational Resource Constraints.* Proc. Third Workshop on Uncertainty in AI (UAI 1987), pp. 429–444. arXiv:[1304.2759](https://arxiv.org/abs/1304.2759). [FULLTEXT]
46. <span id="ref-46"></span>M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, U. Topcu. *Safe Reinforcement Learning via Shielding.* AAAI 2018. [doi:10.1609/aaai.v32i1.11797](https://doi.org/10.1609/aaai.v32i1.11797). [FULLTEXT]
47. <span id="ref-47"></span>S. Carr, N. Jansen, S. Junges, U. Topcu. *Safe Reinforcement Learning via Shielding under Partial Observability.* AAAI 2023, 37(12):14748–14756. [doi:10.1609/aaai.v37i12.26723](https://doi.org/10.1609/aaai.v37i12.26723); arXiv:[2204.00755](https://arxiv.org/abs/2204.00755). [FULLTEXT]
48. <span id="ref-48"></span>A. A. Feldbaum. *Dual Control Theory, I–IV.* Automation and Remote Control 21(9):874–880, 21(11):1033–1039, 22(1), 22(2), 1960–1961 (English translations; page ranges of III–IV not confirmed). [UNVERIFIED-FULLTEXT]
49. <span id="ref-49"></span>Y. Bar-Shalom, E. Tse. *Dual Effect, Certainty Equivalence, and Separation in Stochastic Control.* IEEE TAC 19(5):494–500, 1974. [doi:10.1109/TAC.1974.1100635](https://doi.org/10.1109/TAC.1974.1100635). [UNVERIFIED-FULLTEXT]
50. <span id="ref-50"></span>J. He, D. Yu. *The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures in Agentic Quorums.* Preprint, arXiv:[2609.02925](https://arxiv.org/abs/2609.02925), 2026. [FULLTEXT]
51. <span id="ref-51"></span>M. Bara. *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence.* Preprint, arXiv:[2609.01873](https://arxiv.org/abs/2609.01873), 2026. [ABSTRACT-ONLY]
52. <span id="ref-52"></span>J. R. Douceur. *The Sybil Attack.* IPTPS 2002, LNCS, pp. 251–260. [doi:10.1007/3-540-45748-8_24](https://doi.org/10.1007/3-540-45748-8_24). [FULLTEXT]
53. <span id="ref-53"></span>J. C. Knight, N. G. Leveson. *An Experimental Evaluation of the Assumption of Independence in Multiversion Programming.* IEEE TSE SE-12(1):96–109, 1986. [doi:10.1109/TSE.1986.6312924](https://doi.org/10.1109/TSE.1986.6312924). [ABSTRACT-ONLY]
54. <span id="ref-54"></span>G. W. Brier. *Verification of Forecasts Expressed in Terms of Probability.* Monthly Weather Review 78(1):1–3, 1950. [doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2](https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2). [UNVERIFIED-FULLTEXT]
55. <span id="ref-55"></span>A. P. Dawid. *The Well-Calibrated Bayesian.* JASA 77(379):605–610, 1982. [doi:10.1080/01621459.1982.10477856](https://doi.org/10.1080/01621459.1982.10477856). [UNVERIFIED-FULLTEXT]
56. <span id="ref-56"></span>T. Gneiting, A. E. Raftery. *Strictly Proper Scoring Rules, Prediction, and Estimation.* JASA 102(477):359–378, 2007. [doi:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437). [UNVERIFIED-FULLTEXT]
57. <span id="ref-57"></span>C. Zhang, Z. Wan, X. Yu, et al. *Calibration Is Not Control: Why LLM-Agent Oversight Needs Intervention.* Preprint, arXiv:[2606.21399](https://arxiv.org/abs/2606.21399), 2026. [FULLTEXT]
58. <span id="ref-58"></span>M. F. Dixon. *Model Validation of Agentic AI Systems: A POMDP-Based Framework for Belief-State, Forecast, and Policy Validation.* Preprint, arXiv:[2606.17383](https://arxiv.org/abs/2606.17383), 2026. [ABSTRACT-ONLY]
59. <span id="ref-59"></span>R. Strom, S. Yemini. *Optimistic Recovery in Distributed Systems.* ACM TOCS 3(3):204–226, 1985. [doi:10.1145/3959.3962](https://doi.org/10.1145/3959.3962). [ABSTRACT-ONLY]
60. <span id="ref-60"></span>E. N. Elnozahy, L. Alvisi, Y.-M. Wang, D. B. Johnson. *A Survey of Rollback-Recovery Protocols in Message-Passing Systems.* ACM Computing Surveys 34(3):375–408, 2002. [doi:10.1145/568522.568525](https://doi.org/10.1145/568522.568525) — states the output commit problem and credits it to Strom & Yemini. [FULLTEXT]
61. <span id="ref-61"></span>B. Bonet, H. Geffner. *Planning with Incomplete Information as Heuristic Search in Belief Space.* AIPS 2000, pp. 52–61. [FULLTEXT]
62. <span id="ref-62"></span>D. E. Smith, D. S. Weld. *Conformant Graphplan.* AAAI-98, pp. 889–896. [FULLTEXT]
63. <span id="ref-63"></span>J. Hoffmann, R. I. Brafman. *Contingent Planning via Heuristic Forward Search with Implicit Belief States.* ICAPS 2005, pp. 71–80. [FULLTEXT]
