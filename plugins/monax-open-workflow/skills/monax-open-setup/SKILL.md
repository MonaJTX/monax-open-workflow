---
name: monax-open-setup
description: 接入 MonaX Open Workflow，为新项目或已有项目建立本地规则与记忆入口；普通任务接续不重新初始化。
---

# 项目接入

先读 [任务边界](../../rules/boundaries.md) 和 [上下文](../../rules/context.md)。确认当前项目根、已有 AGENTS.md、PROJECT_CONTEXT、Git 状态及真实需求。本技能只使用本包，不查找作者原工作流或其他安装缓存。

用 [初始化工具](../../scripts/project.py) 的 `init --project-root "<项目目录>"` 预览。用户已授权接入且无冲突时加 `--apply`。工具不覆盖现存文件；冲突时保留现有 owner，在独立临时项目生成模板，比较后按授权合并入口、规则快照、marker 和索引，不能删除旧文件后重新初始化。

从项目核验身份、阶段和架构/生产约束，更新生成的事实文件并清除已解决 blocker。不要用示例事实填空。执行 `check --project-root "<项目目录>" --require-ready`；Ready 只是结构状态。

规则和模板位于 `.monax-workflow`，项目事实位于 PROJECT_CONTEXT。工具不修改 .gitignore、不提交 Git、不安装插件。与用户现有分发约定一致地选择共享和私人记录；核验 Git 跟踪，而不是假设生成文件已共享。

静态入口已可手工使用，可选 Hook 需要用户自行安装与信任；安装不是本技能的隐含动作。恢复与记录用 [记忆规则](../../rules/memory.md)，不要反复接入。
