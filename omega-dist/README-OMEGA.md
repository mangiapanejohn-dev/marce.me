# ø / Omega — 共生型元认知进化层

<p align="center"><img src="assets/omega-logo.png" alt="ø" width="180"></p>

> /omega thinks with Marc. /omega-update grows the Brain. Friday keeps ø alive.

ø 不是总结器：它读 Marc Brain 的最新与历史状态，结合外部世界做多世界线推演（7-subagent council），与 Marc 对话对齐后形成共识，经 `/omega-update` 落库——**Marc 进化，ø 进化，Brain 也进化**。

## 组成

| 部件 | 位置 | 说明 |
|---|---|---|
| ø 记忆层 | vault `_omega/` | 四模型 / knowledge-graph 视图 / review 待审 / error-book / logs / weekly 收件箱（进 git） |
| 运行态 | repo 根 `.omega/` | status.json 状态机等（gitignore，缺失自动重建） |
| 入口 skill | 全局 `~/.claude/skills/{omega,omega-update}` | 仓库 `.claude/skills/` 是快照归档 |
| Council | 全局 `~/.claude/agents/omega-*.md` ×7 | historian / marc-simulator / builder / critic / trend / knowledge-architect / judge |
| 自动化 | `scripts/omega-*.sh` + `launchd/me.marcyy.marcbrain.omega-weekly.plist` | 周五 21:30 headless 扫描 + macOS 通知 |
| 权限 | repo `.claude/settings.json` | headless allowlist；`thoughts/`、`evolution/` 硬 deny |

## 使用

```
/omega                  # 提议主题或现场给题，推演+对话
/omega [topic]          # 指定主题推演
/omega resume weekly    # 接周五 brief 进入对话对齐
/omega-update           # 展示 Merge Plan，确认后落库
/omega-update --yes     # 跳过确认（仍打印 Merge Plan）
```

状态机：`idle → running_weekly → pending_dialogue → in_dialogue → pending_update → updating → synced → idle`（任何状态可 → `error`，错误写 `_omega/logs/events.jsonl`）。查看：`bash scripts/omega-status.sh`。

## 安装（重建机器时）

```sh
# 1. skill + agents 到全局
cp -r .claude/skills/omega .claude/skills/omega-update ~/.claude/skills/
mkdir -p ~/.claude/agents && cp .claude/agents/omega-*.md ~/.claude/agents/
# 2. 周五自动扫描
bash scripts/install-omega-launchd.sh
```

## 测试

```sh
bash scripts/omega-notify.sh                    # 通知弹出（terminal-notifier 或 osascript fallback）
bash scripts/omega-status.sh                    # 读取/重建 status.json
bash scripts/omega-weekly.sh --dry-run          # 全链路不烧 token：锁→状态流转→占位brief→通知→还原 idle
bash scripts/install-omega-launchd.sh --dry-run # 预览将安装的 plist
launchctl list | grep me.marcyy.marcbrain.omega-weekly
```

交互测试：`/omega` 冒烟（能读 status+四模型、派 council）；`/omega-update` 无 pending 时应直接说"无待合并共识"。

## 通知持久化（⚠️ 需要一次手动系统设置）

macOS 通知默认是 **横幅(Banners)**——几秒后自动消失，周五晚的提醒很容易错过。要让 ø 的通知**常驻到手动关闭**：

> 系统设置 → 通知 → **ø** → 通知样式选 **提醒(Alerts)**。

通知左侧小图标 = 发送方 App 的图标，新版 macOS 不允许参数修改——所以有专属通知器：
`bash scripts/build-omega-notifier.sh` 会克隆 terminal-notifier.app → 换 ø 图标/改名 ø/ad-hoc 重签 → 装到 `~/Applications/omega-notifier.app`。omega-notify.sh 优先用它，没有则退 terminal-notifier，再退 osascript。

四层兜底设计（通知只是第一层，**`.omega/status.json` 才是唯一事实源**）：
1. **系统通知**：专属 ø 通知器（左侧 ø 图标，`-group omega-weekly` 同组聚合不刷屏），fallback terminal-notifier / `osascript`。
1.5 **常驻悬浮框（dialog 模式，周五 weekly 成功时启用）**：swiftDialog（`~/Applications/Dialog.app`）在**屏幕右上角**弹 ø logo 悬浮窗，置顶、可拖动、**不点"知道了"永不消失**，零通知设置依赖；无 swiftDialog 时退 osascript 居中框。⚠️ 必须前台阻塞运行——后台会被父进程退出连带杀掉；`--small`/`--timer` 参数组合会导致窗口不渲染，勿加。
2. **会话启动提醒**：repo `.claude/settings.json` 的 SessionStart 钩子跑 `scripts/omega-remind.sh`——只要状态是 `pending_dialogue`/`pending_update`/`error`，在本 repo 打开的每个 Claude Code 会话开头都会看到一行提醒。
3. **/omega 自检**：任何模式启动都先读 status.json，有待办先提醒。

ø 只提醒、绝不自动开始：通知不会自动运行 `/omega`，对话永远由 Marc 手动发起。

## 回滚

```sh
bash scripts/uninstall-omega-launchd.sh          # 停周五自动化
rm -rf ~/.claude/skills/omega ~/.claude/skills/omega-update ~/.claude/agents/omega-*.md
git revert <ø落地commit>                          # 库内文件回滚
```

## 设计边界（为什么这么长）

- **三方分治**：ø 可写 `_omega/` + 事实层（遵 `_system/sync-playbook.md`）；**绝不写 `thoughts/`、`evolution/`**——自述层属于 `/main-self-up`。`marc-model.yaml` 是 ø 对 Marc 的外部观察，与自述并存不同步。
- **双链为真**：权威图谱是 vault `[[双链]]`+MOC；`_omega/knowledge-graph/*.yaml` 只是 ø 视图与变更日志。
- **待审分工**：`_system/inbox.md` 管事实冲突裁决；`_omega/review/` 管 ø 共识合并。
- **压缩不删除**：旧理解归档为 `compressed_archive` / previous version / evolution note / deprecated edge。
- **Judge 不自产**：裁判只基于其他 6 个 agent 的输出打分组合。
- **Best Path 是参考不是命令**：Marc 有权合理偏离，分歧本身可成为共识。
