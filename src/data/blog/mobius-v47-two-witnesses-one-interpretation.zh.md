---
slug: "mobius-v47-two-witnesses-one-interpretation.zh"
title: "MØBIUS V47 — 两个证人，一种解释"
description: "整条研究线里唯一没人碰过的那条前沿假设：一个能自己制造独立证据根的 runtime。一次普查说明了为什么从这里到不了那儿——而障碍并不是所有人第一反应会去补的那个缺失的 emitter。"
lang: "zh"
pubDatetime: 2026-09-06T11:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

开启这整条线的那份前沿综述，结尾列了一串假设，其中一条——**一个能自己制造独立证据根的 runtime**——是
被调研的整个语料里唯一没有任何系统尝试过的。十二个版本过去，这里也一样没碰过。

这一版不去建它。它先测「要建它，什么必须先成立」，而答案不是你第一反应会去够的那个东西。

### 四条 ref，两个根

对一次双动作的 run 做普查，数清 journal 携带的每一条 `EvidenceRef`：

```
evidence by carrier : {"receipt": 2, "verification": 4}
evidence by trust   : {"observed": 4, "asserted": 2}
observations taken  : 0
```

不看计数、去读那些 ref，就会发现两个 carrier 并不独立：

```
R observed | filesystem:post-write-stat | a.json is 17 bytes with digest sha256:4e5e21c2…
V observed | filesystem:post-write-stat | a.json is 17 bytes with digest sha256:4e5e21c2…
V asserted | result:fs.write            | the provider result for fs.write decided 1 of 1 assertion(s)
```

裁决里那条 `observed` ref **就是 receipt 的那一条**，只是被带了下来。所以一次看起来有四条证据的 run，
实际上有两个根，每个动作一个，而每个根都是**一次**读取。

那个根是真的，不是回声——`post-write-stat` 会把字节从磁盘重新读出来再做摘要，不是把写入的参数原样送回。
它不是的东西是**独立**：只有一个证人，而这次 run 里没有任何别的东西对同一个事实持有意见。

### 显而易见的那个答案，已经被钉过两次

`contradiction.detected` 被两个投影器 fold，在 working set 里权重 `0.95`——所有种类里最高——并且被
meta-action 选择器排在每一个 unknown 之上。没有任何东西发出它。

这**不是一个发现**。一个普查测试早就钉住了它，并且给了理由：*「信念修订是没有主人，而不是主人闲着；
为了满足 switch 语句去写 emitter，是按机会发明认知，ADR 0007 拒绝这么做。」* 另一个测试从 depth gate
抵达同一个事实：*「接好了线却在挨饿——缺口在上游。」*

在宣称发现之前值得先查一下，而这一查改变了这一版讲什么。上游的缺口不是「没人写 emitter」，而是
**从来就没有第二个意见，可以让第一个去矛盾**。

### 只有一条路径例外，而 V37 早就在比对那两个

`fresh-observation` 的裁决路径会产生对同一个资源的两次独立读取：receipt 的 `post-write-stat` 摘要，以及
用于验证的那次观测的摘要。更早的一版建了这个比对，并记下了它发现的东西：

```
RCPT settings.json = dbe90cd729a1   worldRevisionAfter = 1
OBS  settings.json = a7254c4184a3   worldRevision      = 1
```

两个证人，一个资源，**在同一个被记录的世界版本上**互相矛盾——provider 做过的任何事都解释不了这个差异。

V37 把它读作 `void{drift}`：*世界动了，这条预测是对着错的世界评的分。* 这是一种读法。另一种是：这两次
读取里有一次是错的。在版本相等时两者不可区分，而 runtime 把第一种硬编码了。

这个默认几乎肯定是对的——一个怀疑自己读数的 runtime 什么结论都得不出——但它是个**默认**，而在此之前它
和一个事实无法区分。现在它被钉成了默认。

### 为什么什么都没建

给 `contradiction.detected` 加一个 producer 今天就能做：V37 已经算出了那个分歧。而它会错两次。

信念平面的消费者从头到尾都在挨饿。`FailureDiagnosis.invalidates` 被算出来、从来没人读；`assumption.made`
没有 producer，所以一个矛盾会去作废的那个集合永远是空的。加一个 producer 会点亮一条 switch 语句，而它
背后是一条只接了一半的路径。

而且那个分歧**已经被报告了**，就在拥有它的那个平面里。再作为一个信念事件报告第二遍，就是一个观察配两套
机制——这个项目已经拆过五次的形状。

**H5 是被定位了，不是被关闭了。** 挡在中间的是第二个**来源**：另一个 provider、另一种模态、或者一个不
属于施动 provider 的证人。这个 runtime 每个资源只有一个 provider，所以最近的一步实际的路是组合——
`repo` 和 `filesystem` 都能看见同一棵工作树——而不是 loop 内部的任何东西。

### 两条造坏了的 mutation

第一轮 battery 报了一个存活者和一个无法报告，而**两个都跟代码无关**。

一条 mutation 被写成了 `… + void 0`——一个空操作。它存活是因为它什么都没改，而那是一条不会变异的变异。

另一条编译不过，而这反倒是一条值得知道的性质：`const resolution: ForecastResolution = …` 会收窄到实际
赋的那几个字面量，所以从表达式里去掉 `'void'`，就会让后面的 `resolution === 'void'` 变成类型错误。
**这个 resolution 少掉一个成员，计分那边立刻会察觉。** compile guard 报告了它，而不是把它算成一次击杀。

一个存活者是一个问题，不是一个发现。这里的答案是「这条 mutation 写错了」——值得记下来，因为条件反射
是把存活者读成测试有洞。
