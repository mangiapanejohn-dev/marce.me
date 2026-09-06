---
slug: "mobius-v39-the-prior-value-was-in-the-journal.zh"
title: "MØBIUS V39 — 前值一直就在 journal 里"
description: "验证平面之所以升级去做一次新观测，是因为 `changed` 断言没有前值可比。然后那次观测同样裁决不了它。用一次完美的 look 测出来的——而缺的那个输入，从平面写成那天起就被接受着，从来没人供给过。"
lang: "zh"
pubDatetime: 2026-09-05T18:45:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

`changed` 是唯一一个"任何对动作后状态的观测都裁决不了"的断言算子。验证平面自己知道这件事：当 provider
返回的结果让这条断言 undecidable 时，它就升级，去看一眼。

然后那一眼同样裁决不了。

### 测量

一次 run 两个动作，两个探针。第一个探针看到升级后的观测是一份目录清单，而断言指名的是 `content`——
但那是 **fixture 的 observation port** 把 loop 建好的 gap 扔掉了，不是 runtime。记下来，是为了不让它
被当成结论。

第二个探针把 port 直接指向那个文件，让 `content` 毫无疑问地出现在被观测的状态里：

```
verdict a1  undetermined  basis=fresh-observation
  undecidable  "changed" needs a pre-action value for "content"; none was recorded
verdict a2  undetermined  basis=fresh-observation
  undecidable  "changed" needs a pre-action value for "content"; none was recorded
```

**一次完美的观测，并不能让裁决前进一步。** 平面**因为**结果裁决不了才升级；它取来一次同样裁决不了的
观测；它返回 `undetermined`；loop 诊断出 `InsufficientEvidence` 并跑一轮 recovery。每个动作一次。
为了一个"再怎么看动作后的状态也答不出来"的问题。

### 两半本来就都在

`VerificationInput.baseline`——文档写的是*"Pre-action state, for `changed` assertions"*——一路穿过
planner 进入 `ComparisonContext`，被 comparator 读取；而 comparator 在没有它的时候退回 `undecidable`，
不是退回 `unchanged`：

> 没有记录在案的前值，它就是 undecidable——绝不是"没变"，那会是一个被捏造出来的否定。

在 `runtime-core` 里 grep `baseline`，零命中。**从来没有任何东西供给过它。**

而从 V21-2 起，编译器就会盖上 `ActionIR.basis`，指名一次 loop 仍然握着的观测——取自动作之前，这正是
"pre-action state"的定义。V38 刚刚测过：第一个动作之后的每一个动作，它都是填充的。

V39 做的事，就是在一个调用点把这两半接起来。

### 为什么一个 advisory 的 basis 已经是够格的证据

`basis.freshness` 是 `advisory`，那么"一次可能过期的观测能不能裁决一个 verdict"是个合理的质疑。
comparator 自己已经回答了：在没有 baseline 的时候，它退回去用 `assertion.value`——也就是**被评分方
自己声称的前值**——然后据此裁决。

runtime 自己取的一次观测，严格优于被评分那一方的说辞。这一版**抬高**了证据标准，不是降低。

`changed` 断言的内容是*"这个值与记录在案的前值不同"*。它从来没有断言过归因，这一版也没有让它去断言。
差异究竟是不是**这个动作造成的**，那是 V38 的问题，而 premise 位移信号已经在回答它。两者保持分开。

### 换回来什么

| 情形 | 之前 | 之后 |
|---|---|---|
| basis 覆盖断言路径，内容不同 | `undecidable` → recovery cycle | `satisfied`，verdict `verified` |
| 同上，内容**完全相同** | `undecidable` | `violated` |
| basis 是目录清单，断言指名 `content` | `undecidable` | `undecidable`，不变 |
| run 里的第一个动作——没有 basis | `undecidable` | `undecidable`，不变 |

第二行值得停一下。**runtime 现在能说出"你承诺要改的东西没有改"**——这句话它以前根本组不出来。

第三、四行是诚实的边界：一个够不到断言路径的 baseline 不是前值，把它读成*"没变"*就是 comparator
从构造上拒绝的那个捏造否定。那样还会把每一个没被观测到的字段变成一条被违反的预测。

### 这一版抓到的两件关于自己方法的事

**一个绿着但编译不过的套件。** typecheck 是在改完源码之后、测试文件存在之前跑的；然后 vitest 在四个
测试上变绿。battery 的 compile guard 开口第一行：

```
(tree already has 2 type error(s); only new ones count)
```

新测试文件里两个 `TS2339`——`reason` 只存在于 union 的 `undecidable` 分支上，对 union 用 `?.reason`
编译不过。vitest 转译时不检查类型，所以那次测试运行里没有任何东西能说出这件事。这条教训 V35 在四个版本
之前就写下来了，而这里正是**写下它的那套流程**自己犯的：检查跑过了，然后被下一次编辑作废，之后的绿被
当成两件事都覆盖了。

**一条造不出来的预注册 mutation。** 五条里的一条——*当 basis 没有指名任何观测时，退回最近的一次*——
在当前这个 loop 下与真实代码行为完全相同。`#groundingFor` 返回的就是 session 里最近的那次观测，所以
basis 在派发时**就是**最新的那一个；而派发到验证之间没有任何观测落地，所以"按 id"和"按最近"指的是
同一个 envelope。没有任何 fixture 能把它们分开。

原样留在计划里，没有悄悄改写，并在 battery 里换成一条真正活着的问题：*观测的哪一部分才算 pre-action
状态？*

### 还剩什么

recovery cycle 现在**可以**避免了，但仍然没有被避免。只要 runtime 在动作之前看过，`changed` 就是可裁决
的——而没有任何东西让 runtime **有意地**在动作之前去看。它之所以看过，只是因为上一个动作的验证恰好看了。

这是三个版本从三个方向抵达的同一个未决问题，而它是一个关于"loop 什么时候观察"的问题，不是关于验证平面的。
