# 项目记忆框架

Owner：本文件。Rule ID：MEMORY-OWNER-01 / MEMORY-HISTORY-01 / MEMORY-DISTRIBUTION-01。

## 分层与唯一 owner

| 内容 | 落点 | 要求 |
| --- | --- | --- |
| 项目身份、架构、阶段、平台参数、验收事实、长期约束 | 当前项目的 PROJECT_CONTEXT/<owner>.md | 从当前仓库或明确决定取证，其他文件只引用 |
| 跨项目方法与错误预防 | 本项目 methods owner；只有显式分享/提升时进入独立公共规则 | 删除名称、路径、业务值，以可重复证据证明适用范围 |
| 历史案例、调试过程、复盘原材料 | PROJECT_CONTEXT/history 或已有历史 owner | 默认不加载，不替代当前状态 |
| 用户或团队偏好 | 接收者自己的可选 collaboration owner | 不默认制造偏好，不写进公共规则 |

写入前确定证据、适用对象、唯一 owner、失效条件与发现入口。无法分类或身份不明时先列缺口；核对 cwd、项目入口、身份 owner 和实际资产/结构，禁止把同名项目混写。不把项目事实写进插件缓存、Codex 全局记忆或另一项目。

优先更新现有 owner，只有新的独立职责才新增文件。默认最小框架为 README 索引、project_identity、current_phase、architecture_coding_rules、memory_notes、workflow_activation_profile；具体玩法、经济、UI、音频等仅在有真实内容时按主题新增。README 保留任务→长期规则与当前状态指针，不复制多份状态。

记忆条目至少能定位：结论/约束、适用对象、证据 owner、日期/版本、失效条件。恢复记录放 current_phase 或已有 checkpoint，记录目标、已完成、剩余、阻断、版本和下一步；不用把完整聊天复制成记忆。

## 历史再核验

旧总结用于找证据。按声明类型定位 owner：产品意图看现行需求；实现行为看真实 caller/资产绑定；部署状态看当前目标环境；历史理由看当时决策。冲突时分别记录预期、实现、部署、历史，不能平均化或拿旧摘要覆盖新事实。

旧结论分别记录适用性 Current/Conditional/Superseded/Unknown、问题 Open/Resolved/PartiallyResolved、验证 L0–L5/Unverified、验收 Unknown/UserAccepted。关闭问题不等于真机验证，用户验收不等于新环境仍有效。证据梯度由 verification.md 拥有。

## 写入与分发检查

同任务明确要求记录、恢复或沉淀时，在授权范围直接写入项目本地文件；普通实现不默认扩展为全局规则更新。写后验证索引→正文→实际约束，可用一个不含“记忆”关键词的普通任务以及主题切换任务验证发现链。

分别记录 Canonical Owner、Owner Availability（Versioned/Local Private）、Distribution Channel（Repository/Package/None）、Discovery Entry、Sync/Transfer、Method Promotion（None/Shared Method）。仓库分发核验 Git 跟踪与 ignore 状态；本机可读、工作区 clean 不证明同事或新 clone 能继承。交付副本不能替代原项目 owner。

游戏能力复盘可提炼 core/platform/social/ads/leaderboard 等候选组件，但复用前须拆开业务 provider、平台 adapter、配置/权限和 UI 绑定，验证版本、环境与接入条件。未经跨项目验证只标 Candidate。
