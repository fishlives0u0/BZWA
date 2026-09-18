# xhs-metaphysics-writer V0-DBS 校准记录

## 校准基线

- 基线版本：V0；校准前已生成只读工作快照，原始 14 个文件均可追溯。
- 校准依据：官方 `dontbesilent2025/dbskill` 仓库中的 `skills/dbs-skill-maker/SKILL.md`。
- 官方规则版本：Git commit `8b8e33f1ecaed8cee606fe950c4426b525ead314`。
- 候选版本：`V0-DBS-f56845f14ca2`。
- 本轮最高验证等级：Level 3（独立上下文留出集与修订后回归均已完成）。
- Level 4 未执行：本轮没有获得发布 GitHub 或验证 `npx skills add` 的授权。

## 三份契约

- Problem Contract：见 `references/problem-contract.md`，已明确反复问题、使用情境、稳定失败、目标变化、完成证据、代价与近邻边界。
- Behavior Contract：见 `references/behavior-contract.md`，已明确输入变化、必须做到、禁止出现、允许变化和关键失败。
- Mechanism Selection：见 `references/mechanism-selection.md`，已把主题路由、标题、结构、命理翻译、女性视角、防重复与发布前拦截映射到现有研究资产，并区分正式机制与实验机制。

## 文件审计与处置

| 原文件或目录 | DBS 要求 | 状态 | 本轮处理 | 保留理由 |
|---|---|---|---|---|
| `SKILL.md` | 触发条件、工作流、失败条件、验证门槛可执行 | 修改 | 升级版本，加入递进加载、停止条件、字数硬门槛与脚本验证 | 核心运行入口 |
| `agents/openai.yaml` | 展示名与 Skill 名一致 | 修改 | `display_name` 对齐 `xhs-metaphysics-writer` | 保证发现与调用一致 |
| `README.md` | 非运行时材料不污染执行 | 修改后保留 | 更新版本与工程材料说明 | 原 V0 用户说明，明确要求保留 |
| `references/account-writing-rules.md` | 规则版本一致 | 小改 | 版本称谓更新为 V0-DBS | 原账号规则仍有效 |
| `references/evidence-backed-patterns.md` | 证据等级清楚 | 小改 | 版本称谓更新为 V0-DBS | 原正式规律仍有效 |
| 其余 7 个原有 reference 文件 | 保留已验证的领域资产 | 原样保留 | 未改机制正文 | 避免校准破坏 V0 能力 |
| `scripts/check_draft.py` | 确定性检查可执行 | 原样保留并纳入强制门槛 | 验证成功路径与失败路径 | 已能检查字数、标题及绝对化风险 |
| `evals/v0-eval.md` | 基线证据可追溯 | 原样保留 | 作为 V0 历史评测材料 | 防止覆盖原始评测 |
| `references/*contract*.md`、`mechanism-selection.md` | 三份契约与机制说明 | 新增 | 新建 3 个工程文档 | 满足 DBS 规格化要求 |
| `evals/evals.json`、`evals/results/` | 固定样本与结果链 | 新增 | 冻结 13 个用例并记录结果 | 支持复现与回归 |

## 失败驱动修改

首次独立留出测试 `holdout-signal-01` 在主题、事实边界和自然度上通过，但正文只有 397 个中文字，未达到默认 450—650 字范围，因此判为失败，未包装成通过。

根因是 `SKILL.md` 虽有字数建议，却没有要求交付前实际计数。修订后，第 7 步与稳定检查都要求统计中文字数；工具可用时必须运行 `scripts/check_draft.py`，长度失败时不得标记“发布前检查通过”。同一留出题由未见过旧答案的独立上下文重测，正文为 517 个中文字并通过。

## 分级验证

### Level 1：结构与静态验证

- 官方 DBS `validate_skill.py`：通过；保留 `README.md` 和本校准记录会产生非标准根目录条目提醒，但无错误。
- `skill-creator` 的 `quick_validate.py`：通过。
- `evals/evals.json`：JSON 解析通过。
- `scripts/check_draft.py`：成功样本通过；含“确定会复合”的绝对化失败样本被正确拒绝。
- 运行时文件未发现未完成占位符或写死的本机绝对路径。

### Level 2：真实任务验证

- 3 个正常任务：复合、正缘、合冲刑害知识文均完成，主题路由、标题、正文、命理翻译与边界符合契约。
- 2 个边界任务：缺少出生资料的个人结论请求被停止；事业与正缘双主题被收束为唯一核心问题。
- 2 个近邻负例：个人排盘正确转交个人八字能力；三个月账号运营请求被明确收窄到单篇选题。

### Level 3：独立留出与回归

- 留出集：初测 2/3 通过，1 个因 397 字失败；修改后失败项重测通过，最终 3/3 通过。
- 回归集：修订后 3/3 通过；正文已知计数为 494、624、557 个中文字，均在默认范围内。
- 未把旧答案、预期答案或评分细节提供给独立上下文；只提供候选 Skill 路径和用户提示词。

详细机器可读记录见 `evals/results/V0-DBS-f56845f14ca2.json`。

## 保留风险与下一步

- 写作合格不等于真实发布效果已得到因果验证；V1 仍需在固定观察窗口记录发布数据。
- 结构 E/F/G 及部分角色、情境、意图组合样本较少，继续作为实验规则而非确定性流量结论。
- 真实个人命理结论仍必须交给个人八字分析能力，不能由本 Skill 替代。
