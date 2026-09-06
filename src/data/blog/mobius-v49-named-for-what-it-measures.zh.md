---
slug: "mobius-v49-named-for-what-it-measures.zh"
title: "MØBIUS V49 — 按它实际测量的东西命名"
description: "V48 的测量本来是对着 runtime 的，结果找到了产出这次测量的那个 provider。一个叫 worktreeChanged 的字段，建在一个看不见第二次修改的 token 上，在工作树确实变了的时候报 false——而且从来没有人读过它。"
lang: "zh"
pubDatetime: 2026-09-06T14:20:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V48 在一棵工作树上量了三个证人，发现它们的盲区互不重叠。这次测量第一个被对准的东西不是 runtime，
是产出这次测量的那个 provider。

### 一份对某一种误读很小心的报告

`RepoSession.compareWithPrevious` 保留上一份快照，好告诉下一份「这中间地面动没动」。它的头部注释
把「它不是什么」写得很清楚：

> 不是一个 guard，不是一次 invalidation……一个把它误当作变更检测的消费者，会以为「没变」的报告意味着
> 仓库很安静，而它只意味着这中间没人问过。

这防住了一种误读。V48 的表格说，它下面还有第二种。

### marker 带的是状态 token

```ts
export interface SnapshotMarker {
  readonly observationId: string
  readonly commit: string | null
  readonly changeSetDigest: string
}
```

`changeSetDigest` 是关于**哪些路径处在哪种状态**的。V48 表格第三行：已修改文件再改一次，会动
`diffDigest`，不动 `changeSetDigest`——因为这个路径写之前是 `modified`，写之后还是 `modified`。

所以两次 `repo.status` 观测之间发生了一次真实的内容变更，建在那个 token 上的标志位读出来是 `false`。
它的 docstring——*「待处理变更的集合与上一次观测不同」*——一直都是准的。它的**名字**是
`worktreeChanged`，而工作树确实变了。消费者读的是名字。

`headMoved` 没有对应的缺口：`commit` 是一个完整身份，不是一份摘要。这是一个字段的问题，不是机制的问题。

### 这个区分是「带没带上」，不是「测没测」

`diffDigest` 就在 marker 所依据的同一份 `RepositoryState` 上。不管把它放进 marker 的理由是什么，
*那得再问一次 git* 都不是反对它的理由。这把「没做的测量」和「没带上的测量」分开了，而这里是后者。

### 发了什么，和刻意没发什么

发了：改名，`worktreeChanged` → `changeSetChanged`，并且把那个盲区写进字段自己的 docstring 里，而不是
留在一份没人会在调用现场读的计划里。

**没**发：一个从 `diffDigest` 来的 `contentChanged` 标志位。它只要一行，数据是现成的，而且 V48 已经
证明它能工作——而这就是支持它的全部理由。没有任何东西在读这份报告。给一份没有读者的报告加第二个字段
是按机会发明认知；ADR 0007 拒绝这么做，V47 三版前在信念平面上因为同样的理由拒绝过同一件事。

> **一个「能工作」的测量不构成去做它的理由。一个需要它的读者才是。**

### Battery 攻击的是比较，不是名字

改名没法被变异成一个测试抓得住的东西，所以四条 mutation 都去打那个被改名的字段所报告的内容。全部被杀。
值得点名的是这条：让第一次观测伪造一份「没变」的比较，而不是返回 `null`，杀掉两个测试。`null` 的意思是
*没有人做过测量*，拿一个 `false` 顶上去，是一个没有人做出过的断言——而这恰恰是那段头部注释为自己声称的
诚实，现在它被检查了，而不是被声称。

四条预测确认，`4 mutations · 0 survived · 0 unreported`，全套
`176 files · 1517 passed | 36 failed`——已知的那些红文件，没有新的。

### 同一个形状的第二例

V47 找到 `contradiction.detected`：被两个投影器 fold，权重是所有种类里最高的，被路由排在每一个 unknown
之上，而没有任何东西发出它。V49 找到一份每次 `repo.status` 都会算、而没有任何东西读的移动报告。两个平面，
一个形状——**代价每次都付，价值从来不收**。

两次是巧合。能分辨这一点的仪器并不存在：更早的一版建过「没人读的导出」的探测器，另一版建过「没人产出的
事件」的探测器，而两者都从来没有被对准过协议字段。
