# S2 · 需求侧普查：真实用户在权限配置里写了什么

研究负责人：Claude Science · 2026-09-23 · 解锁自 GitHub 凭据；回答 `WHAT_IS_LEFT.md` §3 与 Track A 的需求侧分母
方法：GitHub code search 按文件大小分层抽样 → 按 blob SHA 取精确内容 → **确定性**分类（`policy_census.py`，无 LLM）

## 0 · 三个结论

1. **声明式权限面几乎只被用来表达动作/资源范围**（与项目七运行时供给侧普查同形，这次来自需求侧）。allow 规则 54% 是命令前缀、22% 是精确命令、4% 是路径；deny 规则 57% 前缀、37% 路径。规则语法本身无法表达状态不变式。
2. **想要状态检查的用户绕过语法去写 hook，但很少。** 1,959 个文件中 **≥70 个（3.6%）** 有查询世界状态的 hook（测试 / 类型检查 / `git status`），**12 个（0.6%）** 用 Stop hook 做完成闸门。这是下界：1,020 个 hook 调用不可见的外部脚本。**§3 的「空位」存在需求，但需求很小**——它不被判死，但也不能再称为「用户需要的缺失能力」而不附这个比例。
3. **「不再询问」按钮持久化的授权有相当一部分永远不会再命中。** 产品自动写入的 `settings.local.json` 中，shell allow 规则 **47%（95% CI 44–50%）是精确命令行**（手写提交的 `settings.json` 为 29%），其中 **≥66%（63–68%）** 带一次性内容（`/tmp/claude-1000/<uuid>`、heredoc 提交信息、具体 URL）。即 **约 31% 的「不再询问」shell 授权在构造上不可能再次匹配**。这是 codex#38328 所述现象在 Claude Code 上的第一次野外测量（仅就我检索所及）。

## 1 · 样本

| 类别 | 查询 | 文件 | 解析成功 | 仓库 |
|---|---|---|---|---|
| `.claude/settings.json`（提交、团队共享） | `path:.claude filename:settings.json permissions` × 5 个大小层 × 2 页 | 1,001 | — | — |
| `.claude/settings.local.json`（产品自动写入） | 同上 `settings.local.json` | 1,000 | — | — |
| Claude 合计（去重） | | 1,982 | 1,959 | 1,976 |
| codex `config.toml` | `filename:config.toml approval_policy` × 5 层 × 3 页 | 360 / ~1,490（**抓取未完成**） | 354 | — |

## 2 · Claude：规则形状（按仓库做 cluster bootstrap，B=2000）

| 文件 | 列表 | 类 | 占比 | 95% CI | 规则数 | 仓库 |
|---|---|---|---|---|---|---|
| settings.json | allow | PREFIX | 0.54 | 0.50–0.59 | 21,410 | 875 |
| settings.json | allow | EXACT_CMD | 0.22 | 0.18–0.27 | | |
| settings.json | allow | MCP | 0.08 | 0.05–0.10 | | |
| settings.json | allow | BARE（整工具） | 0.06 | 0.05–0.07 | | |
| settings.json | allow | PATH / DOMAIN | 0.04 / 0.04 | | | |
| settings.local.json | allow | PREFIX | 0.44 | 0.42–0.47 | 32,739 | 965 |
| settings.local.json | allow | **EXACT_CMD** | **0.39** | 0.36–0.42 | | |
| settings.json | allow（仅 shell） | EXACT_CMD | 0.29 | 0.24–0.34 | 16,444 | 825 |
| settings.local.json | allow（仅 shell） | **EXACT_CMD** | **0.47** | 0.44–0.50 | 27,208 | 942 |
| 两者 | deny | PREFIX / PATH | 0.57 / 0.37 | | 4,156 | 351 |

精确命令中的一次性比例（含引号、heredoc、`&&`/`;`、命令替换、git hash、多级路径或 >80 字符）：settings.json **0.50**（0.44–0.56），settings.local.json **0.66**（0.63–0.68）。另有 1,666 条（9.5%）多行精确命令未被正则解析、被计为「可复用」，故 0.66 是**下界**。

`defaultMode`（1,959 个文件）：未设 1,837；`acceptEdits` 42、`bypassPermissions` 33、`auto` 20、`default` 13、`plan` 8、`dontAsk` 4、`allowEdits` 2。

## 3 · Claude：hook 在做什么（关键词分类，1,959 个文件中 419 个有 hook）

| 事件 | 查状态：测试/类型/lint | 查状态：git | 拦截/保护 | 格式化 | 通知/日志 | 注入上下文 | 外部脚本（不可见） |
|---|---|---|---|---|---|---|---|
| PreToolUse | 9 | 18 | 210 | 2 | 7 | 22 | 323 |
| PostToolUse | 43 | 11 | 18 | 50 | 23 | 10 | 236 |
| Stop | 8 | 7 | 10 | 1 | 28 | 12 | 159 |
| SessionStart | 4 | 7 | 3 | 0 | 3 | 32 | 174 |

PreToolUse 的「拦截/保护」（210）绝大多数是**动作谓词**（拦 `rm -rf`、拦推送、拦危险命令），不是状态谓词。Stop 上的状态检查原文示例：`bun typecheck … || exit 2`、`git diff --quiet HEAD … || echo 'REMINDER: There are uncommitted changes'`。

## 4 · codex（**部分**，360 个文件，全部 <700 字节——小文件偏置）

| `approval_policy` | n | `sandbox_mode` | n |
|---|---|---|---|
| on-request | 181 | workspace-write | 208 |
| **never** | **154** | danger-full-access | 81 |
| on-failure | 10 | (未设) | 58 |
| 其他 | 9 | read-only | 7 |

`never` + `danger-full-access` 同时出现 72 个（20%）。**仅作方向参考**。

## 5 · 对项目的含义

- **`WHAT_IS_LEFT.md` §3（「设计空间的空位」是否无人需要）**：未被反转，但被量化为一个小数。可辩护的表述是：「无运行时提供状态不变式语言；在公开配置中，≥3.6% 的文件用 shell hook 自行实现状态检查，0.6% 用于完成闸门。」
- **Track A 的需求侧**：常驻自治需求真实存在（codex `never` 43%，Claude 5% 的文件改默认模式），但 S3 已表明模型层不退回授权。野外可见的失败在**运行时层**：持久化授权的粒度——约 31% 的「不再询问」shell 授权不可再命中。该机制空间已被占据（2608.15888、SessionBound、2609.15422），**测量**我未检到先例，但这是产品缺陷的测量，不是研究问题；本项目只记录，不追。

## 6 · 口径

- **选择偏倚**：`settings.local.json` 通常被 `.gitignore` 排除；公开提交它的仓库不代表典型用户。
- code search 返回 best-match 排序、每查询 ≤1,000 条；按大小分层只缓解、不消除排序偏倚。
- 精确命令也可能源自用户手写而非「不再询问」按钮；local 文件是产品写入的**主要**通道，但不是唯一通道。
- hook 分类为关键词启发式；外部脚本内容不可见，故状态检查比例只是下界。
- codex 抓取在报告时未完成（360/~1,490），且已抓部分全部来自最小两个大小层。
