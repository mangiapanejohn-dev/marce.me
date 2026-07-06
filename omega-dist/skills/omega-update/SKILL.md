---
name: omega-update
description: ø / Omega 的落库入口——把 /omega 形成的 pending consensus 合并进 Marc Brain 知识库。展示 Merge Plan、默认要求确认（--yes 跳过）、压缩不删除、更新模型与图谱、状态置 synced。Use when the user types /omega-update or /omega-update --yes.
---

# /omega-update — 共识落库

> /omega thinks with Marc. **/omega-update grows the Brain.** Friday keeps ø alive.

只有这个命令才真正更新知识库。没有 pending consensus 时什么都不做。

## 0. 定位与读取

1. 定位 vault：`find "$HOME/Desktop" -maxdepth 5 -name '首页.md' 2>/dev/null | grep -i 'Marc Brain'`；repo 根 = vault 上一级。
2. 读 `_omega/review/pending.md`。为空或无未处理段落 → 告知「无待合并共识，先跑 /omega」，结束。
3. 读 `<repo>/.omega/status.json`；读 `_system/sync-playbook.md` 的写入规则（事实层落库必须遵守它）。

## 1. Merge Plan（必须先展示）

把 pending consensus 翻译成 **Knowledge Patch Merge Plan**，逐条列出：

| # | 更新类型 | 目标文件 | 操作（append/新建/归档） | 内容摘要 |

七种更新类型：
1. **Stable Consensus** —— 新理解写入事实层对应页面（项目/决策/概念/时间线…）
2. **Compressed Archive** —— 旧理解压缩保留（见下方压缩规则）
3. **New Branches** —— 新增分支页面
4. **New Hubs** —— 新增中枢/MOC（连接数≥5 才够格）
5. **New Links** —— 新增 `[[双链]]`（权威图谱永远是双链+MOC）
6. **Model Updates** —— `_omega/models/` 四模型的字段级变更
7. **Omega Error Book** —— ø 本次的误判/过时理解/被 Marc 纠正的点 → `_omega/error-book/omega-errors.md`

## 2. 确认

- 默认：展示 Merge Plan 后**停下等 Marc 确认**，支持逐条否决（否决项进 rejected.md）。
- 命令带 `--yes`：跳过确认直接执行（仍要先打印 Merge Plan）。

## 3. 执行（三方分治写入边界）

**可写**：① `_omega/` 全部；② 事实层（项目/决策/概念/技术/人物/时间线/索引/术语表），遵守 sync-playbook：append-first、带 confidence 标注、来源可溯。
**绝不可写**：`thoughts/`、`evolution/`（settings.json 有硬 deny）。marc-model.yaml 是 ø 的外部观察模型，与 thoughts/ 自述层是两个并存视角——若共识涉及自述层过时，只能在结果里建议 Marc 跑 `/main-self-up`。

执行顺序：
1. `status.json` → `updating`。
2. 按 Merge Plan 逐条执行。双链/MOC 变更直接改 vault 页面；同时在 `_omega/knowledge-graph/edges.yaml`/`hubs.yaml` 记录变更日志（Add Edge / Deprecate Edge / Promote Hub / Compress Branch / Create MOC 五种操作，带日期与理由）。
3. 压缩归档按规则，写入原页面的「历史归档」段或 `_omega/patches/`：

```yaml
compressed_archive:
  topic: ""
  old_understanding: ""
  new_understanding: ""
  compression_reason: ""
  status: "archived_as_previous_version"
```

4. 模型更新：改 `_omega/models/*.yaml` 时保留 `updated_at` 与变更来源；被取代的关键判断移入文件内 `previous_versions` 段，不删除。
5. error-book：ø 的误判追加进 `_omega/error-book/omega-errors.md`（日期 / 误判内容 / Marc 的纠正 / 根因 / 防再犯）。

## 4. 收尾

1. pending.md 中已处理段落**移动**到 `accepted.md`（否决项移动到 `rejected.md`，附否决理由）——移动，不是复制。
2. `_omega/logs/events.jsonl` append 本次更新事件；`_omega/logs/decisions.jsonl` append 本次共识的决策条目。
3. `status.json` → `synced`，写 `last_synced_at`；稍后回 `idle`（message 注明 synced 时间）。
4. git：`git add` 本次改动 → commit（信息格式：`ø update: <主题> — <N> patches merged`）。post-commit hook 自动 push；用 `git status -sb` 验证无 `ahead`。
5. 向 Marc 汇报：改了哪些文件、归档了什么、error-book 记了什么、被否决了什么。

## 硬禁

- 不准直接覆盖原始资料；改既有文件前先看内容，冲突时 append + 归档旧版。
- 不准删除旧历史（压缩≠删除）。
- 不准自动改核心身份、时间线既有事实、价值观（那是 /main-self-up 的领地）。
- 不准把临时情绪写成人格事实。
- 不准把 Best Path 写成「Marc 将执行 X」的命令式记录——写成「共识/选择/理由」。
- 不准把外部趋势写成确定事实（保留 Trend 的置信标注）。
- 不准用旧 Marc Model 固定评判新 Marc——模型条目被证伪时更新模型，而不是坚持模型。
- 出错时：`status.json` → `error` + events.jsonl 记录，不留半完成状态不报告。
