# ƒ — 14 style modes for Claude Code

14 个套在 Claude Code 输出上的「函数」。每个就是一个 `SKILL.md`，纯提示词，零脚本零依赖。
全部带 `disable-model-invocation: true` —— 不注入系统提示，**不调用就零上下文开销**。

一键安装：

```bash
curl -fsSL https://marcyy.me/ƒ/install.sh | bash
```

Windows（PowerShell）：

```powershell
irm https://marcyy.me/ƒ/install.ps1 | iex
```

手动安装：把 `skills/` 下的 14 个目录拷进 `~/.claude/skills/` 即可，无需注册。

---

## 生命周期

| 写法 | 效果 |
| --- | --- |
| `/xxx` | 开启持续模式，之后每个回答都套用 |
| `/xxx [内容]` | 只对该内容作用一次，不进入模式 |
| 多个模式 | 可以叠加（`/ghost` + `/brief` = 像真人写的三行话） |
| 说「关闭 xxx」 | 解除该持续模式 |

一次性分析类（devil / roast / matrix / why / steal）执行完即结束，除非明说「接下来都这样」。

---

## 持续模式 · 9

| 命令 | 作用 |
| --- | --- |
| `/godmode` | 火力全开：拿出最高水平输出，不省力不藏拙 |
| `/artifacts [内容]` | 可视化优先：输出用图表/交互界面呈现，不用文字块 |
| `/eli5 [概念]` | 讲给 5 岁小孩：用日常比喻讲清复杂概念，零术语 |
| `/ghost` | 去 AI 味：写出来像真人写的，中英文都适用 |
| `/brief` | 长话短说：三行内先给结论，细节等追问 |
| `/nocode` | 去技术化：不出现代码块，用通俗概念解释技术问题 |
| `/silent` | 直接干活：不复述任务不客套，只给结果 |
| `/ooda [问题]` | 先推演再回答：观察→定向→决策→行动，防止信口开河 |
| `/step` | 手把手：展示每一个思考步骤，不跳步 |

## 一次性分析 · 5

| 命令 | 作用 |
| --- | --- |
| `/devil [观点]` | 唱反调：从反方立场挑战你的观点，找出思路漏洞 |
| `/roast [对象]` | 毒舌点评：最不留情面的真实反馈，零客套 |
| `/matrix A vs B` | 对比决策表：列优缺点对比矩阵并给明确立场 |
| `/why [现象]` | 只找根源：告诉我为什么会发生，不要解决方案 |
| `/steal [案例]` | 扒底层逻辑：拆解成功案例表象背后的可迁移原理 |

这五个不带参数时，默认作用于当前对话正在讨论的东西。

---

## 卸载

```bash
rm -rf ~/.claude/skills/{godmode,artifacts,eli5,ghost,brief,nocode,silent,ooda,step,devil,roast,matrix,why,steal}
```

安装器遇到同名目录会先备份成 `<name>.bak`，卸载后想找回原来的自己改回来。

---

## Shared as-is

这是我自己天天在用的一套模式，公开出来作参考。没有支持、没有保证，欢迎反馈。
—— Marc · [marcyy.me](https://marcyy.me)
