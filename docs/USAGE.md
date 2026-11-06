# 接入、共享与升级

## 静态与插件模式

静态模式在项目内保存 AGENTS.md、规则和上下文，适用于能读取 Markdown 的 Agent；是否自动加载由宿主决定。插件模式增加技能与提醒，需要使用者自行安装、启用和信任。两种模式共用规则，不代表所有 AI 宿主已做运行验证。

## 文件职责

| 路径 | 职责 |
| --- | --- |
| AGENTS.md | 轻量入口，不复制所有规则 |
| .monax-workflow/rules | 本项目使用的规则快照与条件路由 |
| .monax-workflow/templates | 视频模板，使用时另存项目文件 |
| .monax-workflow/project.json | 包版本、规则和模板 hash |
| PROJECT_CONTEXT/README.md | 任务到事实 owner 的索引 |
| project_identity.md | 身份、目标、工具/平台 |
| current_phase.md | 当前目标、完成状态、剩余与恢复 |
| architecture_coding_rules.md | 软件架构或视频生产路线与约束 |
| memory_notes.md | 已确认长期决定、证据、失效条件 |
| workflow_activation_profile.json | 核心规则、条件规则、事实 owner 与阻断 |

`conditional_rules` 是已知条件规则列表，实际触发取决于任务。工具核对字段和文件，不判断自然语言事实真假，也不把所有模块设为强制生产流程。

## 已有项目合并

1. 记录当前差异和已有入口、索引及实际事实 owner。
2. 在独立空目录生成模板。工具返回冲突时不做覆盖；不要把冲突当作要求重建项目。
3. 把 `.monax-workflow` 规则/模板快照带入目标；现存同名快照先比较，不静默替换。
4. 在原 AGENTS.md 加入包标记 `<!-- monax-open-workflow:v1 -->` 和 `.monax-workflow/rules/context.md`、`PROJECT_CONTEXT/README.md` 的发现指针，保留原要求。
5. 合并事实索引，激活表 `project_owners` 可指向已有 PROJECT_CONTEXT 下 Markdown owner；不要制造重复事实来源。
6. 审查 blocker 与待填写事实后执行 `check --require-ready`。未知事实保持未就绪，而不是删掉 TODO 伪装完成。

初始化默认 dry-run，`--apply` 只创建本次清单中的文件。采用独占创建保护已有写入；运行中失败保留并列出残留，不自动回滚删除。路径含符号链接或 junction 时拒绝。它不是对抗恶意并发改目录的操作系统沙箱。

## 团队共享与个人记录

初始化不改 ignore、不提交文件。团队决定哪些事实可共享后核对 Git 跟踪/忽略状态。个人凭据和私人记录放项目约定的私有位置，不混入公共规则。

团队规则优先写项目 owner，不修改已安装插件缓存。规则快照被编辑后检查报 Rule drift；这是要求审阅版本差异，不是让工具覆盖定制。普通项目偏好写事实 owner，通常无需改包规则。

## 升级

此版不含自动迁移。新包到达后比较规则、模板、索引与本地约束，保留定制，更新实际采用版本及 marker 中的 SHA-256，检查通过后按项目分发约定交付。hash 是变化检测，不是签名或权限证明；不要仅刷新 hash 来绕过审阅。

升级包源码不会自动更新项目内快照。插件也有单独安装缓存；本地文件改变不证明宿主已加载新版本。新版本须重新核验 Hook 与正常任务行为。

## 停用

可以先在宿主中停用可选插件，静态项目规则仍然存在。移除项目接入前先审查引用和保留长期事实；本包不提供自动删除项目记忆的命令。不要删除自己的 PROJECT_CONTEXT 来卸载规则。
