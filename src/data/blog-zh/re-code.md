---
title: "🤫 RE CODE：我的第二个项目，救 Claude 于ban海"
description: "受够了随机的 Claude ban？整了 RE CODE —— 一个能绕过 Claude Tango Tengu 监控的开源 Claude API 客户端。"
pubDatetime: 2026-04-15T01:00:00Z
tags: ["RE CODE", "Claude", "绕过", "API 客户端"]
---

Yo again,各位码友和 ban 受害者们！我是那个还在 Resonix-AG 成就感的余震中躺平的叛逆开发者——现在我带了第二轮：RE CODE，我的第二个"这破玩意儿太垃圾，我还是自己整吧"项目 😂。要是你之前被 Claude 随意 ban 过（咱都懂的），这篇就是为你整的。

先说背景（再次强调，但真的痛）：我正肝个项目呢，疯狂用 Claude 解析代码、头脑风暴、顺便骂骂有bug的代码——然后就bang!账号被ban了。没有警告，没有解释，就一句"你的账号已被暂停"。我盯着屏幕寻思，"哥，我也没整啥花儿啊！"

然后一通猛查（读：Google 了三个小时加骂电脑），整明白了 Claude 的小秘密：一个叫"Tango Tengu"的监控系统，简直就是个过度保护的保安。它追踪一切——你的设备指纹（40多个维度！）、每一次点击、每一个指令、还有你 IP 的"名声"。分享账号？ban。用第三方客户端？ban。IP 换太多？ban。用个AI跟走钢丝似的。

我试了网上各种"修复"——新IP、新账号、甚至重置设备——但啥用没有。要么ban继续来，要么 workaround 拉胯到比不用还难受。然后我就想了，"得，没人整一个安全稳定的不会被ban的 Claude 客户端，那我来！"然后又是两周的熬夜肝、debug、骂骂咧咧——RE CODE 就来了。

直接说重点：RE CODE 不是什么神奇的hack——就是一个为了一个目标而生的开源 Claude API 客户端：不再ban。我整它就是为了躲 Claude 的 Tango Tengu 监控，让你自由地用 Claude，不用提心吊胆。简单、有效，不整花儿。

说说它为啥能改变游戏规则：我给它整了个4层安全流水线，就像给你的设备和请求穿了隐身斗篷。不用讲术语，简单说：

**第1层：** 隐藏你设备的"指纹"——MAC地址、UUID、时区、甚至你的user agent。再也不给 Tango Tengu "哎，这设备有猫腻！"的机会！

**第2层：** 调时间、token、headers，让你的请求看着100%合法（不再标"可疑活动"）。

**第3层：** 用住宅IP轮换，所以你的 IP 不会被拉黑。

**第4层：** 整个加密 AES-256 + HMAC，所以就算有人偷看，也读不了你的请求。简直给你的 Claude 穿了防弹背心。

还有别的的好处：完全隐私控制（关掉遥测就不追踪你）、自定义代理支持（进一步隐藏真IP）、跨平台——Windows、macOS、Linux、甚至 Termux。我是个懒的开发者，所以安装就一行代码，没有复杂的配置。没有依赖，没有头痛，复制粘贴就走。

分享个整 RE CODE 的糗事：有天我肝了一整天修 IP 轮换的bug，结果最后发现是代理URL里拼错了字。想自锤到留下印——但这就是编程，对吧 ？还有一次我测试反ban功能，硬给 Claude 发了100个请求（不要judge我）等ban……啥也没有。啥也没有！乐得差点哭——终于整到了一个不会背叛我的 Claude 客户端。

现在 RE CODE 是3.1.2版了，加了多模型支持、自定义API端点、甚至还有一个好用的CLI（不整花儿命令，保证的）。我还把 README 翻成了日语和朝鲜语——因为没人应该被卡在ban账号上，不管你在哪。

就像 Resonix-AG，我把 RE CODE 开源在 GitHub 上。要是你也是受害者或者只是想更安全地用 Claude���clone 一下、测一测、提PR 或者来骂 bug——我听着。是一个人能Tango Tengu 整的活有限——脑子越多 = 越无ban的 Claude 时间。

再掏心窝子一下：我整 RE CODE 不是为了出名或者赚钱。就是受够了用个我依赖的AI工具还要被罚。不完美——还有bug要修、有功能要加——但这是我的第二个"代码娃"，救了我不知道多少次。

你试了 RE CODE 拯救了你的ban（或者只是让你的 Claude 人生更easy），求求给个⭐。小小的举动是我继续的动力——知道我在帮别的码友避免跟我一样的 frustrations。要是不-work？来 issues 喷！我不玻璃心，反馈（哪怕是骂人的）才能让东西更好。

好了， rant 完了（暂时）。我去给 RE CODE 加更多反ban trick 了——可能还要整个功能嘲笑 Tango Tengu（开玩笑……可能）。下次见，祝大家都能无ban用 Claude 😜。

**RE CODE 仓库：** **[https://github.com/mangiapanejohn-dev/-Re-Code](https://github.com/mangiapanejohn-dev/-Re-Code)** —— 去救你的 Claude 账号！