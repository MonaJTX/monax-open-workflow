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

先看预览结果的 `conflicts` 列表。下面用最常见的情况举例：你的项目已有一份写着团队约定的 `AGENTS.md`，其余目标文件都不存在。

1. 在 MonaX 工具目录打开终端。选一个全新的临时目录，生成一套**空白**接入文件：

   ```sh
   mkdir ../monax-merge-template
   python -B plugins/monax-open-workflow/scripts/project.py init --project-root "../monax-merge-template" --apply
   ```

2. 在文件管理器里并排打开 `monax-merge-template` 和你的项目根目录。将临时目录里的 **`.monax-workflow` 和 `PROJECT_CONTEXT` 两个目录**复制到项目根目录。必要时打开“显示隐藏文件”，确保点号开头的目录也复制到了。如果目标已经有其中之一，请走下方的逐文件合并。
3. 用文本编辑器打开两份 `AGENTS.md`。把**临时模板里的入口文字（包括第一行 HTML 注释）追加**到项目原文件，保留团队写下的约定。注释、规则路径和项目索引路径都要保留；初始化工具用它们辨认入口。
4. 打开自己的项目，按[首页的项目接入说明](../README.zh-CN.md#用到自己的项目)填写事实。在工具目录运行 `python -B plugins/monax-open-workflow/scripts/project.py check --project-root "../我的项目" --require-ready`，将示例路径换成实际项目路径。

**多个文件冲突时**，根据预览列出的路径逐个比较。下面的做法也适用于目标目录里已经有其他项目文件的情况。

| 已有内容 | 怎样合并 |
| --- | --- |
| `PROJECT_CONTEXT/README.md` 或事实文档 | 保留现有事实和索引，为缺少的职责添加模板文件与相对链接。若继续沿用已有 Markdown 文件名，将激活表 `project_owners` 中对应路径改为该文件，并从索引链接过去。 |
| `workflow_activation_profile.json` | 先核对原文件用途。只有与本包格式兼容时才合并规则列表、事实路径和仍未解决的事项；如果另一个工作流也把这个文件作为专用配置，请先在项目副本中验证兼容性。 |
| `.monax-workflow` 快照或 marker | 先运行 `check`。已接入的项目走升级步骤；有版本或内容差异时保留现有定制，逐项审阅后再采用。 |

初始化默认 dry-run，`--apply` 只创建本次清单中的文件。采用独占创建保护已有写入；运行中失败保留并列出残留，不自动回滚删除。路径含符号链接或 junction 时拒绝。它不是对抗恶意并发改目录的操作系统沙箱。

## 团队共享与个人记录

初始化不改 ignore、不提交文件。团队决定哪些事实可共享后核对 Git 跟踪/忽略状态。个人凭据和私人记录放项目约定的私有位置，不混入公共规则。

团队规则优先写项目 owner，不修改已安装插件缓存。规则快照被编辑后检查报 Rule drift；这是要求审阅版本差异，不是让工具覆盖定制。普通项目偏好写事实 owner，通常无需改包规则。

## 升级

此版不含自动迁移。新包到达后比较规则、模板、索引与本地约束，保留定制，更新实际采用版本及 marker 中的 SHA-256，检查通过后按项目分发约定交付。hash 是变化检测，不是签名或权限证明；不要仅刷新 hash 来绕过审阅。

升级包源码不会自动更新项目内快照。插件也有单独安装缓存；本地文件改变不证明宿主已加载新版本。新版本须重新核验 Hook 与正常任务行为。

## 停用

可以先在宿主中停用可选插件，静态项目规则仍然存在。移除项目接入前先审查引用和保留长期事实；本包不提供自动删除项目记忆的命令。不要删除自己的 PROJECT_CONTEXT 来卸载规则。
