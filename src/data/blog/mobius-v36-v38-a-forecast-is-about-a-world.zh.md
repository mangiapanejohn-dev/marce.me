---
slug: "mobius-v36-v38-a-forecast-is-about-a-world.zh"
title: "MØBIUS V36–V38 — 预测是关于某个世界的断言，而那个世界必须被指名"
description: "V35 造了打分器。接下来三个版本整整都在回答一个由打分器本身问出来的问题：一次预测，究竟是关于哪个世界的？三个里有两个推翻了它前面那一个。"
lang: "zh"
pubDatetime: 2026-09-05T18:30:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

V35 给 journal 里早就存在的那一对打了分——派发之前写下的预测，派发之后写下的裁决。这张表一旦存在，
它就问出了一个自己答不了的问题：**如果在这中间，是别的东西把世界推动了，这笔账算在谁头上？**

三个版本花在这个问题上。其中两个推翻了自己的前一个。

### V36 — 世界动了，不等于预测错了

信号本来就在，而且是在任何设计之前先测的。一次文件写入会让会话的 `worldRevision` 前进；一次读取不会。
`EffectReceipt.worldRevisionAfter` 记下这个动作自己的效果留下的世界，而给它评分的那次观测带着自己的
revision。

```
rcpt worldRevisionAfter=1
obs  worldRev=1
verd basis=fresh-observation
```

相等，说明裁决读到的正是这个动作produce 出来的世界。更大，说明中间有别人写过，而断言是对着一个预测
根本不是在讲的世界被评的分。这种情况变成 `void`——`graded` 和 `ungraded` 之外的第三种判定，之所以
单列，是因为**一次对着错误世界被裁决的预测，不是一次错了的预测**。

然后它自己的 P3 在第一版就挂了，而这次失败比那条预测本身更值钱。

那次外来写入是用 `writeFileSync` 直接落盘的。结果是 **graded，不是 voided**：字节变了，计数器没动。
`worldRevision` 是在 provider 自己的写路径里递增的。它是**这个 provider 执行过多少次写**的计数，不是
世界的版本号——所以这条规则对一个人手工改文件、一个构建步骤、任何不走 provider 的东西，全是瞎的。

这一点被钉成了一个"修好那天就会红"的测试，而不是写进注释，因为*"只有经过 provider 的写入才可见"*
这类句子，恰恰是最容易过期的那一类。

### V37 — 那个计数器同时错在两个方向

开启 V37 的探针抓到了另一半。计数器不只是瞎，它还**太宽**：V36 自己的 P3 会因为有人写了
`unrelated.txt` 而作废一条关于 `settings.json` 的预测。一个断言从来没读过的文件动了，并不会让关于
另一个文件的预测变得无法裁决。

| | 绕过 provider、写这个动作自己的资源 | 经过 provider、写一个无关资源 |
|---|---|---|
| **计数器**（V36） | 看不见 | 作废——过宽 |
| **内容标识**（V37） | 作废 | 正常评分 |

同一次 run，两条规则，相反的答案：

```
RCPT settings.json = dbe90cd729a1   worldRevisionAfter = 1
OBS  settings.json = a7254c4184a3   worldRevision      = 1
```

于是 drift 变成了**内容标识发生变化**，并且被限定在这个动作自己的 receipt 所归因的资源上。receipt 负责
**归因**，observation 负责**比对**。一次观测报出来、而没有任何 receipt 能解释的差异，就是"无法解释的
变化"——这正是 `DependencyInvalidator` 的规则，只不过从日志里 fold 出来，而不是在内存里held 着。

**V36 的 P3 以"被推翻"的状态原样留在它自己的计划里。** 它准确记录了计数器规则当时做了什么、以及是什么
证据说服了那个版本；把它改写成和下一个版本一致，等于抹掉这条规则曾经错过、而且错在它自己的 battery
看不见的地方的唯一痕迹。

#### 一条没有任何用例能杀死它的 mutation

预注册的 mutation 清单里有一条：*去掉"限定在 receipt 归因资源"的作用域，让无关资源重新能作废预测*。
写 battery 的时候发现，没有任何测试能因此变红：所有 fixture 里那次外来写入落在的文件，从来没有被任何
receipt 归因过——所以"比对**所有**见过的资源"和"只比对**这个动作的**资源"，两条规则都会给 graded。
这条 mutation 会跑完，套件会保持绿，battery 会报出一个幸存者，而它真正的含义是*这条性质从来没被测过*。

修补的是**用例**，不是断言。一次 run 里两个动作；第一个让 `other.json` 成真；然后一个外来写入者绕开
provider 改掉 `other.json`；给**第二个**动作评分的那次 look 报出了这个变化。全局 witness 规则会作废
第二个动作，作用域规则给它 graded——而测试先断言"drift 确实发生了"，再断言那个 graded，所以它不可能
因为"什么都没发生"而通过。

### V38 — 一次预测是在哪个世界里做出的

V37 留下了一个它自己讲清楚的残留：对一个 runtime **从来没让它成真过**的资源，外来写入没有任何 witness
可以比对。要堵上它，需要一个在动作**之前**取的 witness。

V36 曾断定那个 witness 不存在。它错了，而它错的方式才是这次的发现。

一个探针，真编译器，一次 run 里两个写 intent：

```
 3 action.dispatched    a1   basis: null
 6 observation.received  obs-1  worldRevision 1
 7 verification.decided  fresh-observation ← obs-1
12 action.dispatched    a2   basis: { observationId: "obs-1", targets: [], freshness: "advisory" }
```

为了**验证第一个动作**而取的那次观测，正是编译器盖在第二个动作上的 grounding。一次预测所处的世界，
从 V21-2 起就是可绑定的。

**V36 的那个 pin 根本不可能看见这件事。** 那个测试跑在一个 stub 编译器上，它只解构 `{ intent, route }`，
把 `grounding` 整个丢掉——所以不管 loop 供给什么，`expect(action.basis).toBeUndefined()` 都成立。它测的
是一个替身，却被当成了对 runtime 的报告。在它下面，那个版本的结论*"没有东西为这个动作提供 grounding"*
是从一个只有一个动作的 fixture 里推广出来的，而在那里它成立的理由完全无关。

两个失误互相遮蔽：stub 让 pin 不可证伪，单动作 fixture 让那句结论看起来是测出来的。

### V38 拒绝越过的那条线

premise 让更大一类变化变得可见——而 V38 报告它，却从不因此作废任何东西。

V37 是靠**收窄**才挣到 void 的资格：限定在这个动作自己 receipt 归因的资源上，因为一次预测是关于它的
断言所读的那些资源的。premise 没有这样的作用域。它见证的是那次观测**恰好**捕获到的一切——对
`fs.observe` 读 `.` 来说，就是整棵树——所以拿它去 void，等于把 V37 花一整版删掉的过宽失败原样装回来。

| 窗口 | 作用域 | 它能诚实地说什么 |
|---|---|---|
| effect → verdict | 这个动作的 receipt | `void` —— 对着错的世界评了分 |
| premise → verdict | 观测到的一切 | *报告* —— 这个决策所处的世界动了 |
| premise → verdict | `basis.targets` | 才有资格让 premise 去 void —— **字段存在，没人填** |

第三行是一笔还着的债。`ActionBasis.targets` 的文档写的是*"identity 必须仍然成立、否则动作失效的
targets"*——正是 premise 作用域需要的那个声明——而每个 provider 都写 `[]`。

### 三个版本花掉了什么，换回了什么

换回来的：一个 `graded | ungraded | void` 的预测判定，其中 `void` 意味着一个具体的、按内容标识检查过的、
限定在 receipt 作用域内的断言；外加一个独立报告的信号，说明一个决策所处的世界动过。这些东西没有一样
接到 authority gate 上，理由和 V35 一样没变——*calibration is not control*。

花掉的：两条被推翻却原样留着的预测，一个被发现并重写的空 pin，一条因为杀不死任何东西而被替换的
mutation，以及三个从 V36 测试文件里搬走的用例——在新规则下它们是绿的，而且**永远不可能变红**，
那比不存在更糟。
