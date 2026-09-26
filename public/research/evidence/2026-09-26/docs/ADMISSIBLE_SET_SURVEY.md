# ADMISSIBLE_SET_SURVEY.md — 为什么 run-time assurance 移植不到 agent runtime：七个系统的可容许集调查

研究负责人：Claude Science · 2026-09-22 · 纯源码普查 + 语料测量，未写任何代码

**这份文件是对我自己前一个负结果的更正。** 我在 `SYSTEM_ONE_REDUCTION_GATE.md` §5 写过一个负结果并给了它 falsifier，本轮跑了那个 falsifier。**它开了一半，而开的那一半否掉了我给出的机制。**

## 0 · 被检验的负结果与它的 falsifier

原陈述：*「RTA 的保证无法移植到 LLM agent runtime，因为 DM 这个位置既接不了可信模型 f，也接不了校准代理。」*
原 falsifier：*「若有人给出一个 agent runtime 的可容许状态集与可判定检查器（哪怕只对一类效果），则该负结果作废。」*

## 1 · falsifier 的三个成分，逐个测

| RTA DM 需要 | 在 MØBIUS 的文件系统效果类上 | 判定 |
|---|---|---|
**模型 f**（动作如何改变状态） | `fs.write(path, content)` 的**后态就是实参本身**——无扰动、无惯性。CPS 里 f 难，这里平凡已知 | **有** |
**派发前可判定的检查器** | `enforceableConstraints` 的 schema 注释原文：*"Constraints with a **deterministic consumer, checked before dispatch**."* | **有** |
**可容许集 A** | 见 §2 与 §3 | **实际为空，且语言只能表达范围** |

`INTERP` 所以我原来给的机制**是错的**：f 不缺，可判定检查器也不缺。**缺的是 A。** 这条更正比原陈述更具体，也更容易被检验。

## 2 · A 在语料上从未被写下

`EXP` 159 个 `goal.created` 中：

| 字段 | 非空的目标数 |
|---|---|
`constraints`（散文，advisory） | **0 (0.0%)** |
`enforceableConstraints`（定型，派发前强制） | **0 (0.0%)** |
`protectedInvariants` | **0 (0.0%)** |

`OBS` **口径**：这批是项目自造的基准任务，任务作者从未填写这三个字段。**所以这一节说的是语料，不是用户行为**——我不能据此声称「用户写的约束不可表达」，因为这批语料里用户什么都没写。我原本计划的「按可表达性分类散文约束」因此**没有数据可测**。

## 3 · 即便被写下，A 的语言也只能表达范围

`IMPL` `packages/protocol/src/constraint.ts:64`：

```ts
export const TypedConstraint = z.discriminatedUnion('kind', [ResourceScopeConstraint])
```

**一个成员。** 而 `ProtectedInvariant`（`authority.ts:121`）= `{id, statement: string（散文）, forbids: EffectScope, because: string}`——机器可检查的部分只有 `forbids: EffectScope`。

`IMPL` 而 `EffectScope`（`authority.ts:54`）的全部维度是 `{effectClasses, capabilityIds, environmentKinds, semanticEffects, resourcePrefixes}`——**全是动作与资源的范围，零个状态谓词。** 它的注释自证了这个设计压力：*"`fs.delete` and `shell.run` are both `irreversible-write`, so \"you may run commands, you may not delete files\" is **inexpressible without this**"*——即**不断增加范围维度去逼近一个状态谓词本来能直说的事**。

`OBS` schema 自己也写明了为什么散文那半不强制：*"Kept, and kept unenforced. Deciding whether \"stay inside the project\" forbids a given path means **parsing English**, and a boundary the runtime is **confidently wrong about is worse than one it admits it lacks**."*

## 4 · 跨系统：七个运行时的声明式策略面全是范围，无一是状态不变式

`EXP` 源码普查（三个已装 + 三个 vendored + MØBIUS 自身）。声明式策略标识符的出现次数：

| 运行时 | 声明式策略面（范围/允许清单） |
|---|---|
**codex** | `approval_policy` 1581 · `sandbox_permissions` 403 · `writable_roots` 264 · `network_access` 233 · `sandbox_mode` 230 · `allowed_sources` 199 · `allowed_domains` 163 |
**browser-use** | `allowed_domains` 129 · `allowed_domain` 14 · `approval_policy` 2 |
**openai-agents 0.22.3** | `sandbox_path_str` 134 · `allowed_callers` 110 · `sandbox_id` 83 · `needs_approval` 68 · `sandbox_mode` 17 |
**pydantic-ai 2.47.0** | `allowed_domains` 64 · `requires_approval` 51 · `allowed_file_url_schemes` 47 · `allowed_hosts` 31 · `allowed_tools` 25 |
**langgraph 1.2.12** | `allowlist` 44 · `allowed_modules` 6（均为反序列化安全，非世界策略） |
**deepseek-harness** | `sandbox_permissions` 79 · `sandbox_mode` 2 |
**mini-swe-agent** | **无** |
**MØBIUS** | `EffectScope` 的五个维度，全部为动作/资源范围 |

`EXP` **状态不变式语言：零。** `invariant|postcondition|admissible|must not change` 的命中已逐条核实**全部是代码/类型不变式的注释**，不是可声明的策略：pydantic-ai 的 25 条是 TypeVar 变型（*"An invariant TypeVar"*）、assert 文档、历史不可变纪律；codex 的 37 条是数据结构不变式（历史配对、遍历顺序、`project_root_markers` 的 *"Invariants:"*）。browser-use 与 mini-swe-agent 为 0。
`OBS` **词频不是发现**——这一条我先做了词频，命中后逐条读了才敢下结论。

## 5 · 结论：更正后的负结果

`INTERP` **RTA 的保证移植不过来，不是因为缺 f，也不是因为校准不可能，而是因为这些运行时提供的是可容许的「动作集」，而 RTA 的 DM 需要可容许的「状态集」。** 二者不是同一个对象：动作范围无法表达「测试仍然通过」「config.json 仍是合法 JSON」「其余文件未被改动」——而 goal schema 的注释自己举的例子正是 *"'Make the tests pass' is satisfied by deleting the tests."*

`INTERP` 而主principal 唯一能表达状态谓词的途径是**任意代码钩子**（guardrail / `args_validator` / `interrupt`）。它能表达任何东西，但**属应用责任、不产生可分析的保证**，且今日的 C2-NI 已测得这类被委派的义务在公开 API 下确实可履行——即这不是运行时的缺陷，而是一个**被明确外推的责任**。所以设计空间里存在一个空位：**声明式、派发前可判定、且非平凡（有透明性）的状态不变式语言。**

`OBS` 为什么它是空的，本会话另有一半证据：任何状态谓词要在派发前被评估，运行时的观察投影必须覆盖该谓词的指称对象——而我早先测得**闭合 provider 上 1,345 条带路径断言中 181 条（13%）静态不可解析**。两半合起来：不是没人想做，是**投影可能评估不了它**。

## 6 · 判决：`MEASUREMENT`，不是 `SYSTEMS CANDIDATE`

`INTERP` 构造性的那半（「造一个可判定非平凡的状态不变式语言」）归约到**数据库完整性约束**：声明式谓词、提交前检查、以及信息不完整时约束求值变三值（SQL 的 `UNKNOWN`）。形式内核已被占据。
`INTERP` 幸存的是**刻画**：七个独立运行时一致地只提供动作范围，而它们各自都用「再加一个范围维度」来逼近状态谓词（MØBIUS 的 `semanticEffects` 注释是自证）。这是「多个独立系统共有但刻画不足的行为」，**是测量文的材料，不是机制贡献。**
`FALSIFIER` 若任一部署中的 agent runtime 提供了主principal 可声明的、派发前求值的状态谓词（而非动作范围、而非代码钩子），本节作废。我查的七个都没有；**这是七个可读样本，不是抽样**。
`OPEN` 而 §5 的两半合起来给出唯一仍然开放的技术问题：**给定运行时的观察投影，哪些状态不变式能在派发前被可靠求值？** 这个问题有形式内核（三值完整性约束）与可测的经验半边（投影覆盖率），但**它需要一个会写状态不变式的语料，而本语料三个字段全空**——按 §F 的结论，这是换仪器的问题。

## 7 · 本轮的自我更正记录

`OBS` 我给出的负结果机制被我自己的 falsifier 否掉（缺的是 A，不是 f 或校准）。这是本会话第六次我自己的假设被自己的测量杀死。
`OBS` 我原计划的测量（按可表达性分类语料中的散文约束）**无法执行**，因为三个约束字段在 159 个目标上全为空；我把它记为无数据，而不是换一个能出结果的读法。


---

## 8 · §6 的开放问题已测，并再次更正我自己（`EXP`）

### 8.1 我上一节说「无语料可测」是错的

`OBS` 我写过「这需要一个会写状态不变式的语料，而本语料三个约束字段全空」。**但语料里有 252 条 `successCriterion`，它们本身就是状态谓词**，其中 **174 条带机器可检查的断言** `{path, operator, value}`，operator 仅 `matches`(152) 与 `contains`(22)，全部 `kind: observable`。所以那条开放问题的经验半边**可以在现有日志上直接测**，只是求值时点从「事后判定」换成「派发前准入」。

`OBS` **而 `fs.write` 使这件事平凡可判定**：后态内容就在实参里，不需要任何观察。120 次派发中（其中 81 次落在带断言标准的 journal 内）**36 次是后态完全已知的 `fs.write`**，45 次后态不可知（`fs.observe`／`fs.patch` 等）。

### 8.2 预注册与结果

`HYP` 测前写下的预测：**绝大多数写都会满足断言，因此该检查在本语料上大概率空转**（55/104 完成、有效行 checker 近乎全过）。这是本会话已被咬过两次的空转陷阱。

`EXP` 82 次 (fs.write × 带断言标准) 求值：**全部可求值**（75 `matches` + 7 `contains`，零正则错误，零 `path != content`）。初次结果为 59 满足 / **23 违反（28.0%）**，且 23 例中 11 例所在 run 最终完成。

`EXP` **但那 23 例是我自己的测量错误，已作废。** 决定性交叉表：

| 断言所指资源 == 被写资源 | 满足 | 违反 |
|---|---|---|
**是** | **59** | **0** |
**否** | **0** | **23** |

完美分离，**23/23 的违反全部是资源错配**（例：`T7-two-files` 的 c2 指名 `src/index.ts`，却被拿去测写入 `src/greet.ts` 的内容）。**真实违反为零。**

`EXP` 所以正确做法下的结论是：**派发前的准入检查在本语料上可判定且完全空转（59/59 满足）。** 我的预注册预测成立。

### 8.3 真正的结构性结论：谓词缺的是资源绑定，不是可判定性

`OBS` **让这个测量有定义的唯一办法，是我用正则从标准的英文 `statement` 里把资源名抠出来**——因为断言的 `path` 是 `"content"`，是观察载荷内部的路径，**不指名任何世界资源**。

`IMPL` **schema 已核（这次核在结论一边）**：`packages/protocol/src/goal.ts:35-41` 的断言定义为

```ts
assertion: z.object({
  path: z.string().min(1),
  operator: z.enum(['equals','contains','matches','exists','absent','gte','lte','changed']),
  value: z.unknown().optional(),
}).optional()
```

**没有资源字段。** 注释原文 *"Optional machine-checkable form, evaluated by the verification plane"*。所以「断言不带资源绑定」是 **schema 事实，不是语料偏差**。
`OBS` 我之所以专门核这一条：本会话已在同一种错误上栽过两次（`PreconditionKind` 有 6 个成员而语料只用 1 个；三个约束字段存在而语料全空）。
`OBS` **但同一段暴露另一处语料偏差**：operator 枚举有 **8** 个成员，语料只用了 **2** 个（`matches` 152、`contains` 22），从未用过 `exists`／`absent`／**`changed`**。`changed` 是一个**时间轴算子**——即规格语言里有一个跨时间比较的算子，而本语料一次没用过。这一条属「语言有、语料没用」，不得读作语言缺失。

`INTERP` 于是七个运行时只提供动作范围的原因，**不是状态谓词不可判定**——对整文件写它平凡可判定。而是：

> **状态谓词需要一个资源绑定，而规格语言不携带它；补上它需要的正好是运行时明确拒绝的那个操作（parsing English）。**

`OBS` 这与本会话早先那个可寻址性结论**同根不同果**：同一个根因（断言不带资源绑定）产生两个不同后果——事后判定时「内容断言对目录观察永不可解析」，派发前准入时「谓词根本没有定义」。
`INTERP` 所以 §5 那句「提供的是动作集而非状态集」现在有了更具体的机制：**不是缺一种语言，而是缺谓词与资源之间的那条绑定**，而 `EffectScope` 的五个维度恰好全是「资源在哪个范围」而不是「资源上成立什么」。

### 8.4 边界

`OBS` 空转结论只说明**本语料上没有可拒的写**，不说明该检查无价值——它证明的是「求值可行」，不是「有用」。要证明有用需要一个 checker 会失败的任务族，而本语料的有效行近乎全过（本会话早先已在确定性实验上踩过同一个坑并修订过交付单）。
`OBS` 36/120 的覆盖率意味着这个结论只对**整文件写**成立。`fs.patch` 的后态不在实参里（是 edits），`fs.move`／`fs.delete` 只知存在性——对这三类，派发前准入需要一次观察，于是又回到投影覆盖率问题（早先测得 181/1,345 = 13% 静态不可解析）。
`OBS` 资源绑定由我用正则从英文抠出，**该正则只认带扩展名的文件名**，不覆盖目录或通配指称；完美分离说明它在本语料上够用，但它是我的近似，不是运行时的能力。
