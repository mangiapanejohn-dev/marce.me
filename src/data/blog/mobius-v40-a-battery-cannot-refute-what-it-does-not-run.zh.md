---
slug: "mobius-v40-a-battery-cannot-refute-what-it-does-not-run.zh"
title: "MØBIUS V40 — battery 无法推翻它没有跑过的东西"
description: "这个改动通过了它全部四条预注册预测，通过了五条 mutation 的 battery，零存活。然后全套件把它推翻了，它被回滚。交付的是一条 pin 和理由。"
lang: "zh"
pubDatetime: 2026-09-05T19:00:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
---

这一版没有交付任何生产代码改动。它之所以在这里，是因为它失败的方式。

### 先是一次撤回

V39 结尾提议给 `ObservationSource` 加一条 conformance pin：*请求必须指名 gap 指名的那个资源*。三个版本
被"测试替身顶替 seam"误导过，一条 pin 看起来就是解药。

**那条建议是错的，而且错在写它的时候没有读 `revalidation.ts` 和 `narrow-look.ts`。** 两者早就处理了
"port 忽略 targeting"这件事，而且处理得比一条 pin 更好：

> 它也不信任那次 look 去了该去的地方。`ObservationSource` 是一个 model seam；一个忽略 targeting 请求、
> 返回无关内容的 port，绝不能有能力恢复工作。覆盖率是对着**回来的事实**检查的，所以一次没提到该资源的
> 观测得到 `disputed`，而不是从沉默里推出一个裁决。

验证平面用它自己的词汇做同一件事——一次覆盖不到断言路径的观测得到 `undecidable`。而 `narrow-look.ts`
刻意**转发**跑偏的 look 而不纠正它，理由写得很明白：纠正之后，下游那道覆盖率检查*"就只会看到已经被修正过
的 look，防线会在生产里未经检验却看起来成立"*。

加一条 conformance pin，等于给一个已经有两道防线的失败加第三道，并且会钝化第二道——正是那段注释警告的事。

### 真正错的那个更窄的东西

runtime 不信任那次 look，是对的。但它**从来不告诉那次 look 自己需要什么**。

```
loop.ts:1555  #targetedLook  gap = { …, targetResources: resources, resource }
loop.ts:1842  #verifyNext    gap = { …,                             resource }
```

而那里的 `resource` 并不是"被看的东西"：它来自 `#bindActiveResource`，那个方法自己的注释写着
*"记住上次 look 是在哪个世界里取的"*。**哪个世界，不是哪个东西。**

所以验证 gap 携带的是一句话和一个工作区。而 `narrowLook` 是这样算覆盖率的：

```ts
const targets = context.gap.targetResources ?? []
if (targets.length === 0) return true
```

并把 `coversTargets` 记进 port 的 attempt trail。在**每一次**验证 look 上，`targets` 都是空的——所以那个
诊断接好了线、被记录着、而且**恒为真**。一条不可能变红的 pin，出现在生产代码里而不是测试里。

修法看起来很显然：用被验证动作的 receipt 去瞄准验证 look，用的是已经存在的字段和已经存在的提取函数。

### 它通过了一切，而它是错的

四条预测，全部确认。五条 mutation 的 battery，零存活。然后是全套件：

```
V21-P4 — a real port that looks somewhere else cannot restore work
  → work was restored on an off-target look: expected 'failed' to be 'blocked'
```

那正是 `revalidation.ts` 存在的那条安全性质——也正是这一版自己开头刚刚解释过"已经有了"的那一条。四个文件
九个失败：`v21-1-observation-port`、`v18j1-revalidation`、`v18j2-observation-accounting`、
`v18j3-budget-enforcement`。**这条线上没有任何一个 battery 会跑它们。**

已回滚。

### 为什么这个字段只属于其中一种 look

`reflex.ts` 早就说过了，就在这个改动写出来之前读过的那个文件里：

> 一个 runtime **精确知道的** subject，因为依赖是它自己记录的

revalidation 知道自己的 subject——它在重读自己记录过依赖的那些资源。verification 不知道。它知道**写了
什么**，而写了什么不等于断言**关于什么**。交付的那条 pin 测的正是这个：receipt 指名 `a.txt`，断言是
`entryCount`，而答案在目录清单里。一次按 receipt 瞄准的 look 会去读那个文件，然后错过它。

第一个错误上面还叠着第二个。`v18j1` 的 fixture **是遵守** targeting 的——正是这个改动希望 port 具备的
行为——而它用 `targetResources.length > 0` 来判断**自己正被要求做哪一种 look**：*"下一个出去的请求就是
那次 revalidating 的。"* 把这个字段同时放到两个 gap 上，就让任何读它的 port 再也分不清这两种 look。

一个机制回答两个问题——这个仓库拆过五次的形状，被那个专门为了小心 seam 而写的版本引进来了。

### 真正该留下的发现

battery 跑了六个文件。六个都是我选的，六个都属于这条线（V35–V40）。每条 mutation 都死了。而这个改动从头到
尾就是错的，证据活在四个关于 observation port 和 revalidation plane 的文件里：也就是"改动 observation
gap"真正会碰到的那套机器。

**battery 衡量的是你交给它的那些测试。** 它的两道 guard 防的是"mutation 没落地"和"mutant 编译不过"。
没有任何一道防"测试清单没覆盖爆炸半径"。

连着五个版本的绿 battery，让全套件感觉像是走过场——V35 到 V39 每一版都跑了它，每一次它说的都和 battery
已经说过的一模一样。这就是那个条件反射，也正是为什么全套件必须**每一版**都跑，而不是等到某个改动
*感觉*危险的时候。

由此得到的规则，比"跑全套件"更窄：

> **测试清单要从改动碰到什么推导，而不是从版本讲什么推导。**

一个交给 `ObservationSource` 的 gap，会被每一个消费观测的平面碰到，而那些平面的 battery 早就存在。

### 交付了什么

`loop.ts` 回到 V39 之后的状态。

- **一条 pin**：验证 gap 不带 target resources；并且——测出来的，不是写在注释里的——receipt 指名文件，
  而断言关于目录。已经有一个版本试图搬动这个字段了。
- **两条 mutation 的 battery**，都红：给验证 look 加上 `targetResources` 杀掉 10 个测试；从 revalidating
  look 拿掉它杀掉 8 个。

这次推翻，现在是仓库会检查的东西，而不是这篇文章记得的东西。

### 关于为什么要发这一篇

存在一个显而易见的版本，在那个版本的项目日志里 V40 根本不出现，因为它什么都没交付。那会是一份更差的记录。
一个通过了自己全部预测、通过了自己的 battery、却依然是错的改动，是这六个版本里信息量最大的一件事——
而它只有在失败被和成功同样认真地写下来的时候，才是可见的。
