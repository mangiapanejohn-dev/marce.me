---
slug: "mobius-v46-the-premise-is-what-it-declared.zh"
title: "MØBIUS V46 — 一个动作的 premise，是它自己说过依赖什么"
description: "forecast 这条线最后一个开口。缺的 scope 恰好有一个字段，而每个 provider 都写 []。而显而易见的填法，重现的正是早已被否决的那个 scope。"
lang: "zh"
pubDatetime: 2026-09-06T10:15:00Z
tags: ["MØBIUS", "Agents", "Verification", "Research"]
category: "research"
series: "MØBIUS"
---

六个版本之前，forecast 表学会了说*「这个决策所处的世界动了」*——而且是**报告**它，不是拿它计分。理由是
作用域。premise 见证的是那次 grounding 观测**恰好**捕到的一切，对目录列表来说就是整棵树，所以拿它去
void，等于把前一版花整整一版删掉的过宽失败原样装回来。

于是留下一行：

| 窗口 | 作用域 | 能诚实地说什么 |
|---|---|---|
| effect → verdict | 这个动作的 receipt | `void` —— 对着错的世界评了分 |
| premise → verdict | 观测到的一切 | *报告* —— 这个决策所处的世界动了 |
| premise → verdict | `ActionBasis.targets` | 才有资格 void —— **没人写** |

`ActionBasis.targets` 的文档是*「identity 必须仍然成立、否则动作失效的 targets」*。这正是缺的那个作用域。
每个 provider 都写 `[]`。

### 测量定了设计

显而易见的填法是 `grounding.targets`——编译这个动作时依据的那次观测，编译器本来就在从它拷贝。在前面那版
自己的双动作 fixture 上量：

```
a2 grounded on:        obs-…-1
resource facts on it:  ["notes.txt", "other.json"]
a2 acts on:            settings.json
```

`notes.txt` 正是整个论证赖以成立的那个旁观者。它出现在 grounding 观测里，是因为那次 look 是目录列表。
而 `settings.json`——这个动作真正写的东西——根本不在这个列表里。

**所以这个字段空着不是因为没人管。** 它显而易见的来源就是 premise 本身，拿 premise 去限定 premise 是恒等
变换。更糟的是，动作自己的 subject 都不在里面。

### 声明是存在的，只是不在观测里

<a class="fig-plate" href="/research/mobius-a06-runtime-truth-model.png">
  <img src="/research/mobius-a06-runtime-truth-model.png" alt="runtime 真值模型：观测/证据回答或收窄一个 unknown，并可能引发失效，失效会作废一个前提或假设。前提支撑决策/意图，决策被 authority 与前置条件检查，并携带一个关于预期结果的 forecast。编译后的 effect 造成结果，验证对它裁决，而 forecast 与已裁决结果之对照就是 calibration。一个建立在已失效前提上的待执行 effect 不得提交。" loading="lazy" />
</a>

<p class="fig-note">一个决策依赖什么，以及证据如何让它下游的执行失效。左边那一列前提，正是这一版给了它作用域的东西。</p>


`ActionIntent.preconditions` 就是动作在派发之前说出自己依赖什么。`fresh-observation(X)` 的意思是*这个动作
依赖 X 被看过*。这是 runtime 里唯一一个和 `targets` 同义的东西——而编译器本来就拿得到 intent，什么都不用
铺管子。

只带一次 look 能重新获取的那两种 kind。批准不是个能重新观测的东西，另一个动作必须先完成的任务也不是；
把它们放进 `targets` 等于说「重新观测这个来重新验证该动作」，而没有任何 look 会那么做。

### 先查再动，因为上次的教训

`basis.targets` 有三个读者，而六版之前有一版填了一个 targets 形状的字段、碰到了它没考虑过的平面——在一次
跑偏的 look 上恢复了工作。所以：

- `staleness.ts` 只在 `freshness: 'revalidate'` 下查 targets。编译器盖的是 `advisory`，那个分支直接
  `proceed`，根本不读。
- `diagnosis.ts` 把 `targets.length` 当诊断信号读。
- 前置条件门的 `namesSubject` 读的是 **`observation.targets`**——另一个对象上的另一个字段。

这是记录改动，不是控制改动。钉住它的测试断言的是直接证据——两个动作都到达了 provider，结束理由里没有
staleness 自己的用词——在此之前第一版断言的是「run 不以 abandoned 结束」，那是个会因为无关理由失败的替身。

### 换来什么，以及刻意没做什么

`premiseMoved` 现在在有声明时按声明限定。同一次旁观者位移，对没有声明依赖的动作照常报告，对声明了的那个
则不在作用域内。

**没声明的动作保留全树报告。** 没有声明并不说明动作依赖什么；把它收窄成「什么都不依赖」是把沉默变成主张。

而且什么都没 void。*这条预测是对着错的世界评的分* 和 *这个决策所处的世界在它声明过的东西上动了* 仍然是
两个主张，把第二个收窄并不会让它变成第一个。它们该不该合并，是这一版刻意不回答的设计问题——它把报告收窄，
然后停下。

### 那个存活者

第一轮 battery 有一条 mutation 存活：把 look 无法重新获取的 kind 也当 targets。没有任何 loop fixture 能碰到
那个过滤器，因为**动作只在全部前置条件都满足后才 dispatch**——`user-authority` 会挂起，
`dependency-verified` 会 withhold，所以被排除的 kind 在编译时永远不在手上。

改成直接测编译器（它是纯的、不需要 loop）才杀掉。这是连续两版第二个存活者，原因相同：断言是照着顺手的
fixture 写的，不是照着分支写的。battery 能发现，读测试发现不了。

### 还剩什么

<a class="fig-plate" href="/research/mobius-a05-ftr-research-target.png">
  <img src="/research/mobius-a05-ftr-research-target.png" alt="FTR 研究目标拓扑：多个执行 actor，各自持有独立封存的 forecast，汇入一个共享的证据场——该证据场追踪 provenance、异议与证据谱系，并且「来源之间达成一致」并不蕴含「彼此独立」。competing hypotheses 供给 active falsification，后者挑选最便宜的判别实验；epistemic scheduler 把算力分配给决策关键的不确定性。在既有 runtime 门提交 effect 之前，有一步 reality admission 追问前提是否新鲜、证据是否独立；结果再回流到 按 proper scoring 的 calibration。" loading="lazy" />
</a>

<p class="fig-note">这是目标拓扑，不是当前实现。图上每条线都是点线，是有原因的——而上面那段天花板，正是左边那一列仍然是理论的理由。</p>


这个作用域的好坏，取决于提议者愿不愿意声明依赖，而目前没有任何东西奖励它这么做。大多数动作什么都不声明，
所以大多数仍然是全树报告——诚实，也是天花板。
