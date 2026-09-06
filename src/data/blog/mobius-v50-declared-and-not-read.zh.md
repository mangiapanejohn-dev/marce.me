---
slug: "mobius-v50-declared-and-not-read.zh"
title: "MØBIUS V50 — 声明了，而没人读"
description: "两个版本各自找到一处「代价每次都付、价值从来不收」的机械。两次是巧合。这一版建了那个能数的仪器——而它抓到的第一个东西，正是为了揭露这个问题而写的那份报告。"
lang: "zh"
pubDatetime: 2026-09-06T15:45:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V49 收尾时点了一个它见过两次、却数不出来的形状：`contradiction.detected`，被两个投影器 fold，而没有
任何东西发出它；一份每次 `repo.status` 都会算、而没有任何东西读的移动报告。**两次是巧合。**

这个仓库有两件同族的仪器。一件探测没人读的导出，一件探测没人产出的事件，而其中更早的那件立下了两者
共同依据的规则：

> **计数是可查的，清理不是。** 删掉之后，没有任何东西能阻止下一个再堆起来。

两件都从来没有被对准过协议字段。这一版就是这笔账。

### 十七个字段，两个没有读者

`CapabilityManifest` 是每个 provider 今天就在写的东西，每个 capability 一份。在生产 TypeScript 里数
读者——排除声明这些字段的 schema 本身，以及写入它们的那些 `capabilities.ts`：

| 字段 | 读者 | | 字段 | 读者 |
|---|---|---|---|---|
| `capabilityId` | 34 | | `stateBearing` | 7 |
| `providerId` | 24 | | `environmentKind` | 6 |
| `description` | 17 | | `reversible` | 6 |
| `effectClass` | 14 | | `semantics` | 5 |
| `schemaHash` | 5 | | `semanticEffect` | 3 |
| `observes` | 3 | | `concurrency` | 2 |
| `expectedLatencyClass` | 2 | | `idempotent` | 2 |
| `constraints` | 2 | | | |
| **`prerequisites`** | **0** | | **`stateful`** | **0** |

`prerequisites` 被四个 provider 在 34 处认真写过。这一对之外的每个字段都至少有两个读者——没有任何一个
恰好只有一个——所以在这里，「被读」和「没被读」不是一个程度问题。

### 这个类型存在的那一半

`constraints` 有两个读者，而它们是同一次读取：manifest 约束的唯一消费者，把 `.id` 拼进一个展示字符串。
所以 `description` 从不被读，而 `predicate`——被写过 23 次——也从不被读。它自己的 docstring：

> 一条 capability 在外部无法兑现的前置条件。**鸭子类型的发现表达不了这些，这正是它们在这里的原因。**

schema 陈述了自己的必要性，provider 照着写了，而那个机器可读的谓词从来没有被机器读过。路由不查它：
匹配器碰的是 `providerId`、`semantics`、`effectClass`，没别的。

### 报告证伪了自己

runtime 其实已经有那份诚实的报告了——只不过是给另一个平面的。一个 goal 的约束可以被问「哪些是真的
生效的」，答案会把 `enforced` 和 `advisory — 散文；runtime 什么都不检查` 并排打出来，它存在的理由是让
*「我的哪些约束是真的被执行的？」* 不需要读源码。capability 的约束没有这样一个答案，所以一个在十一个
capability 上写了 `prerequisites` 的 provider 作者，无从得知它不绑定任何东西。

所以这一版发的是 capability 侧的孪生体。它的第一版接收 manifest，然后去统计自己正在报告的那些声明有
多少条——而 `m.prerequisites.length` 是一次读取。普查立刻为这份报告称之为「无人读」的两个字段找到了
读者，pin 变红了。

而且没有豁免可用。一个能分辨*为了报告而读*和*为了决策而读*的探测器，必须能看见意图，而一次普查的全部
价值恰恰在于它看不见。

> **一份去测量它所描述之物的报告，会变成它所描述之物的一部分。**

现在这个渲染器不接收任何参数，也不数任何东西。计数归探测器。

### 提及不是读取

同一类错误又出现了两次，两次都是测试变红发现的，不是先见之明。渲染器的 docstring 引用了
`m.prerequisites`。渲染器的**输出**里含有字符串 `constraints[].predicate`。两者都被当成了读取。

先剥注释，再剥字符串字面量——但索引形式必须在剥字符串**之前**测，因为 `obj['predicate']` 是一次活在
字符串里的真读取。

一次普查的难点从来不是数数，是把「什么算数」定下来，而这里每一条都是先错一次才定下来的。

### 那个没有发出去的数字

宽口径的普查是真的：协议 259 个 schema 字段里有 **52 个**在任何地方都没有读者。它不是这一版发出去的
东西，而理由比数字更值钱。按文件测量，这个分布是**双峰**的——`worldline.ts` 79% 无人读，而八个协议
文件是 0%——所以一个平均数哪一组都描述不了。

`worldline.ts` 不是一个「建了但有缺口」的平面。它是一个被声明、没有实现的平面，而它的头部注释——很长、
很仔细、引用了它所依据的研究——一个字都没说。actor 平面的头部也没说。架构文档里也没有。

对事件的规则是：每一个被声明的事件，要么被产出，要么被钉上「为什么不产出」的理由。对一个被声明的
**平面**没有对应物，而一个初次读到那个文件的人，无从得知没有任何东西在运行它。
