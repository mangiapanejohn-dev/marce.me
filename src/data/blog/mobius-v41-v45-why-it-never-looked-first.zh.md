---
slug: "mobius-v41-v45-why-it-never-looked-first.zh"
title: "MØBIUS V41–V45 — 为什么 runtime 从不在动作之前先看一眼"
description: "连着四个版本从四个方向撞上同一个未决问题。runtime 一直有这个机制，而它从来产不出一次可用的 look——三个独立原因。四次修补里有两次先打偏了。"
lang: "zh"
pubDatetime: 2026-09-06T10:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

连着四个版本，结尾都是同一句话：*没有任何东西让 runtime 有意地在动作之前去看——它之所以看过，只是因为
上一个动作的验证恰好看了。*

runtime 有这个机制。`ActionPrecondition` 的 `kind: 'fresh-observation'` 就是模型在说*这个动作依赖一件
我还没看过的事*。V41 问它为什么从来产不出一次 look，答案是同一条路径上的三个缺陷。

<a class="fig-plate" href="/research/mobius-a03-action-lifecycle.png">
  <img src="/research/mobius-a03-action-lifecycle.png" alt="一个被提议的 effect 从认知到验证的十二步：ActionIntent、PreconditionGate、unknown.raised、路由缺口、fresh observation、resolution check、准入门、编译、派发、EffectReceipt、VerificationResult、forecast resolution。图上标了两个缺陷：路由缺口会在 no-route 和 look 之间翻转，以及一个 unknown 对三十一次 resolved、零次 dispatch。" loading="lazy" />
</a>

<p class="fig-note">一次 effect，从认知到验证。两个红框是 V41 量出来的东西；第 6 步之后的一切都没有发生。点开看原图。</p>


修它们的四个版本里，有两个先打偏了——而那反倒是更有意思的一半。

### V41 —— 测量，并且拒绝修

一个 intent，一个前置条件，三个探针。

**一次「动作前的 look」的路由，由一个自由文本字段决定。** 用一句提议者会写的话：

```
3 unknown.raised   question: "the write rests on what is there"
4 depth.changed    EXPLORE: a factual unknown is open and something can be looked at
5 goal.abandoned   no-route: 2 capabilities were the right effect class but shared
                   no term with the described need (fs.observe, repo.search)
```

到最后一步之前 runtime 做的每件事都对。`needFor` 把 `question: precondition.because` 塞进去，
`classifyUnknown` 把它变成词法 reflex 用来路由的 gap description。

这是刻意的，`precondition.ts` 自己写着：*「一个声明了含糊理由的 intent 得到一条含糊的路由，这是正确的
激励。」* 测量不反对它背后的意图——它反对的是那句描述。含糊的理由**得不到一条含糊的路由**，它得到的是
**没有路由、零次观测、目标被放弃**；而同一个对象上 `satisfies: [precondition.subject]` 精确地握着那个
名词。而且激励要成立，被激励方得看得见后果；放弃不是梯度。

**改一个字段整场翻转**——然后它停不下来：

```
unknown.raised 1 · observation.received 31 · unknown.resolved 31
action.dispatched 0 · abandoned "no terminal state within 32 turns"
```

一个问题，提出一次，被记录为「已回答」三十一次，从来没被回答过。

V41 一个都没修，而这就是那一版的内容。只修路由，会把一个不花钱的失败换成一个要花 31 次经过门、计费的
观测的失败——而剩下的部分是横跨五个平面的 unknown 生命周期改动，每个平面都有自己的 battery。上一版刚
好就栽在这件事上。

### V42 —— 一个字段，在每个写它的地方都只有一个含义

`Unknown.satisfies` 协议里定义为*「解决这个 unknown 会推进的 SuccessCriterion id」*。而
`precondition.ts` 往里写的是 `precondition.subject`——一个文件路径、一个批准名——三个读取方却都当它是
criterion id。

那就修写入方。改完了，被 battery 自己的 baseline 推翻。

`precondition.ts` 读的是 `state.evidenceByCriterion[subject]`。把证据归档到 subject 下**不是标错，它就是
机制**——`failure-reproduced` 和 `hypothesis-supported` 全靠它才可能被满足。清空 `satisfies` 之后，
evidence-before-fix 那个场景**再也不会 dispatch**：

```
expected -1 to be greater than 0
```

漏掉它的那次测量，列了 `loop.ts` 里和 `completion.ts` 里 `#evidenceByCriterion` 的读者，发现全是按
criterion id 查的，然后**从没问过「这个 record 还被交给了谁」**。前置条件门就被交给了。那个 map 刻意
承载两个 key 空间——completion 用 criterion id，dispatch gate 用前置条件 subject——而它的名字只说了一个。

两个内部含义都承重。**但只有一个被承诺出去**：`PendingQuestion.satisfies` 是给客户端的，文档写明是
criterion id，而一个 `user-authority` 前置条件挂起时带的是 `["deploy-approval"]`，目标的 criterion 是
`c1`。修在那个边界上，规则也不是发明的——`narrow.ts` 早就拒绝**模型**在同一个字段里声明未声明的 criterion。

### V43 —— 一次 look 没产出的「解决」

V41 把那 31 次 resolution 读作*「`unknown.resolved` 表示看过一次，不表示问题被答了」*。真实机制更锋利：

```
observation.evidence length: 0
unknown.resolved.by length:  0
```

look 回来时不带任何 evidence，所以事件带着 `by: []` 发出——而投影只在 `resolvedBy` 非空时才算已解决。
**runtime 自己的状态早就把那 31 个当空气了。** 它们不是 31 次被采信的声明，是 31 条假记录。

V43 不再写它们。它**没有**阻止重复，而它的测试钉住了这一点。

它设计的那个改动——把「已探索」的记忆放进前置条件门——实现了、完全按预测生效、**什么都没改变**。选择器
是从投影里的 open unknown 选 EXPLORE 的，不是从门的 needs 选的。

顺带记下：`fs.observe` 只在一种情况下附带 evidence——文件内容形如给助手的指令。目录列表没有，普通文件读
也没有。所以在那个 provider 上，整条 explore-and-resolve 路径本来就是空转的，而测试里的对照只能拿
prompt-injection 那条路搭。

### V44 —— 已经问过世界的问题，不算还开着

停止状态早就在：

```ts
const actionable = await this.#raiseNeeds(report, state)
if (!actionable) {
  return { stop: 'stuck', reason: `dispatch of ${intent.id} is withheld and nothing can lift it: ${report.withheldBecause}` }
}
```

它到不了，两个原因必须一起动。选择器规则 6 取第一个 open 的 observable unknown，完全不记得自己探索过
它，所以 ACT 再也没被选到。而 `#raiseNeeds` 把 open 当 actionable，不管有没有为它做过事——所以只修选择器
会把 31 次 look 变成 32 次被 withhold 的 ACT。

```
之前   observation.received 31 · abandoned "no terminal state within 32 turns"
之后   observation.received  1 · stuck
       "dispatch of i1 is withheld and nothing can lift it:
        fresh-observation(settings.json): nothing observed so far names "settings.json""
```

什么都没发明。停止、理由、过滤器全都早就在；缺的是一个事实，和两个必须读它的地方。

#### 一个靠着缺陷才绿的测试

`v18f3-session-affinity` 红了。它断言「active resource 在观测之后绑定并抵达 route」，方式是要求**多于一个**
带路由的 turn。

第二个带路由的 turn 是一次**重复的 look**——正是 V44 删掉的行为。而本该提供它的那个 ACT 多年来一直以
`no-route` 结束，因为 intent 的 desiredEffect 跟任何写能力都没有共同词。这个测试一直绿着，靠的是它并不
打算依赖的载体，而它自己注释描述的那个 turn 一直在静默失败。

### V45 —— runtime 知道这次 look 是为了什么

reflex 一直支持 slot 路由，没有 slot 时会打印*「semantics: none — this route was decided on text
alone」*。拿 V41 那句话对真实能力图路由：

```
text only                -> NO ROUTE
inspect/path/existence   -> fs.observe
inspect/file/content     -> fs.observe
```

所以 runtime 一直都能路由这次 look。它做不到的是**说出这次 look 是为了什么**。`ActionIntent.semantics`
给了提议者一个 slot 通道；没有任何东西给 runtime——而对一个前置条件，runtime 精确知道 subject，也从一个
封闭枚举知道 kind。

`Unknown` 加一个可选 `semantics`，与 intent 的对称，按 kind 填——封闭枚举上的全映射，且只给一次 look
能关闭的那两种 kind。

**`question` 一个字没动。** 提议者那句话仍然是抵达 trace 和 wire question 的那一句；一个被要求批准某件事
的人，应该读到作者给的理由。变的是给**路由器**什么，不是告诉读者什么。

一个 `target-exists` 前置条件、subject 是真实存在的文件、理由跟任何读能力都没有共同词——现在 dispatch
并且 goal 完成。之前是 `no-route` 加零次观测。

而路由通了之后，暴露出 V44 的一个洞：absent 文件上的 `fresh-observation` 路由成功，然后跑了 32 次**失败**
的 look。V44 只在 look 落地后才记「已探索」。对被拒绝或超预算的 look 这是对的——那是门和预算说不，条件会
变。对一次被许可、负担得起、真的执行了、回答「我看了，看不见」的 look，就不对。

### 这五版真正教会的事

**两次修补打偏了，而且是同一个误读的两面。** V42 在字段的写入方清空它，打断了一个依赖它的读取方。V43 把
记忆写到一个没有读者会查的位置。两版都没有足够早地问：**到底谁在读这个东西。**

**一个不停被移动的对照，不属于持有它的那个版本。** 有一条断言把 V41 那个 run 的形状钉成「别的都没动」的
对照。V43 动了它的 resolution 计数，V44 动了它的 look 计数。第三次时它被**退役**而不是再改一遍——一个
每个后续版本都要重写的对照，是在用一个声称别的意思的名字追踪当前行为。

**而 V41 的测试文件已经删除。** 它没交付任何代码，只钉了三个缺陷和一条「为什么不修」。每一条现在都被处理
了，而它最后一条 pin 不是被推翻，是**被变成空的**：它断言「改措辞会改变结果」，而 V45 之后两种措辞产生
同一个 run。它测量过什么，记录在它的 plan 文档里。测试属于持有主张的那些版本。

### 一张地图，聊胜于无

<a class="fig-plate" href="/research/mobius-v42-runtime-architecture.png">
  <img src="/research/mobius-v42-runtime-architecture.png" alt="V42 时的整个 runtime，分五个带：一条从人类授权出发的实时执行脊——goal、模型端口、ActionIntent、前提消解、准入门、编译、派发、世界、receipt、验证；认知与观测带，装着 unknown 生命周期、gap 路由与 fresh observation；世界与新鲜度带，装着 WorldRevision、ActionBasis 与 staleness guard；持久化与校准带，装着持久 journal、project() 与 forecast calibration fold；以及一条虚点表示的研究前沿，属于 future trajectory reasoner。实线是活的，虚线是已声明但休眠，点线是研究。" loading="lazy" />
</a>

<p class="fig-note">V42 时的整个 runtime——也就是这篇文章中段那一版。实线是活的，虚线是已声明但休眠，点线是研究。点开看原图；在这个宽度下它是张方位图，不是能读的图。</p>
