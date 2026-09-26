# 研究计划：授权持久性（Track A）收束 + 两条被凭据解锁的旧阻塞项

研究负责人：Claude Science · 2026-09-23 · 执行方式：按序连续推进，每步结束写结果与判定，不在步间停

## 总问题

用户在会话中明确授予的常驻授权，是否会在执行过程中被 agent 非预期地退回？若会，成因是否是**授权特有的**，而不是一般约束衰减的一个实例？

## 已知（不重开）

- 七类「自主性失败」中六类已被占据（`ESCALATION_PRIOR_ART.md`）。
- 「授权会不会衰减」本身已被 MTAC-IFBench 结论 (4) 间接预测（`TRACK_AB_FALSIFIERS.md` §A.2）。
- 试点：2 条约束 / 10 轮 / 单模型下零 re-escalation；差分因天花板未检验（`PILOT_TRACK_A.md`）。

## 步骤（按信息增益/成本排序）

### S1 · 先验闭环：ACM/CHI 侧检索（OpenAlex，已解锁）
- **做什么**：检索 CHI / CSCW / UIST / IUI / FAccT 2024–2026 及 ACM DL 中「agent 重复询问 / 审批持久 / 授权撤回 / 打断时机」的工作；同时补 `WHAT_IS_LEFT.md` §1 那条「定稿前第一件事」（agent 评估方法论是否已覆盖四个混淆源的分离）。
- **kill**：命中一篇测量「已授权后再询问」随会话演化的工作 ⇒ Track A 归约，S3 改为复现。
- **产物**：`ACM_GAP_CHECK.md`。

### S2 · 需求侧普查：真实用户写了什么权限配置（GitHub，已解锁）
- **做什么**：GitHub 代码检索公开的 `.claude/settings.json`（`permissions.allow/deny/ask`）与 codex `config.toml`（`approval_policy` / `sandbox_mode`）。逐条分类：动作/命令范围、路径范围、工具范围、状态不变式、常驻授权（allow）vs 禁止（deny）vs 强制询问（ask）。
- **回答两件事**：(a) `WHAT_IS_LEFT.md` §3——用户想约束的是否也只是范围（若是，「设计空间空位」降为「无人需要」）；(b) 常驻授权在真实配置中有多普遍——这是 Track A 的需求侧分母。
- **口径**：公开仓库有幸存者偏差，只报比例与区间，不报「用户想要」。
- **产物**：`POLICY_DEMAND_CENSUS.md` + `policy_rules.csv`。

### S3 · 载荷实验：Track A 的判决性版本
- **假设 H-load**：授权约束的违反率随同时生效的约束条数上升。
- **差分 H-diff**：在载荷使一般约束开始衰减的条件下，授权约束衰减得更快 / 更慢 / 一样。
- **设计**：约束条数 L ∈ {2, 12, 30}（额外约束取 MTAC-IFBench 18 子类中可脚本核查者）；GRANT 三档 + NOGRANT@30 灵敏度对照；模型 `claude-opus-4-6`（MTAC 最低斜率 6.2 pp）与 `claude-haiku-4-5`（22.7 pp），**模型身份与 MTAC Table 2 行一一对应**；3 seed；10 轮。
- **修正试点的两个缺陷**：(1) 删除机会从每 run 2 次提至 5 次，且删除目标事先显式创建（试点里部分询问是「文件不存在要不要跳过」的澄清，不是审批）；(2) 每次询问按「审批 / 澄清 / 故障上报」三类标注。
- **阳性对照（关键）**：额外约束本身的 CSR 必须随载荷下降。若 L=30 时无任何约束衰减，实验不灵敏，结论记「未检验」。
- **no-fault 基线**：fault 日志 + 写入回读，fault>0 的 run-turn 剔除并报告。
- **kill**：L=30、两模型下授权违反率与 L=2 无差异，且阳性对照显示载荷确实压低了其他约束 ⇒ H-load 否证，Track A 在模型层退役。
- **产物**：`LOAD_EXPERIMENT.md` + 数据 + 图。

### S4 · Track B 可行性闸门
- **做什么**：判断 S3 的 harness 能否支撑 prefix branching（同一前缀执行 continue / intervene 并测结局）。需要：可快照的前缀状态（harness 已有）+ 可自动判定的结局（需为 todo 工具写功能测试）。
- **判定规则**：若结局判定可在一步内建成，跑最小版本（重复采样分歧 vs `p_fail` 类标量对 intervention advantage 的相关）；否则写成交付单，记「未执行」，不降格为代理测量。
- **门槛（已预注册）**：分歧的相关必须超过 2606.21399 Table 14 中 `p_fail` 的 0.716 / 0.604。

### S5 · 收束
- 更新 `TRACKS.md` 首段与项目记忆；写一页判定：Track A / B 各自是存活、收窄还是退役。

## 不做的
- 不设计任何保持授权的机制（`TRACK_AB_FALSIFIERS.md` §C：已被 2608.15888 占据）。
- 不把 GitHub issue 当发生率。
- 不把单模型结果外推。
