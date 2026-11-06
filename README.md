# MonaX Open Workflow

**换一个聊天，也能接着昨天的工作。** MonaX 帮你把项目里已经商量好的事写在项目自己的文件中。下次打开项目，AI 可以找到上次做到哪里、哪些决定要保留，以及哪一步还需要你看一眼。

如果下面有一件事你也遇到过，可以从对应的例子开始。

- **昨天刚说好怎么排，今天加个筛选又要解释一遍。** 把「默认按加入时间倒序」记在阅读清单项目里。下次只问「未读筛选和搜索一起用时，列表怎么显示？」，就能检验 AI 是否找回并沿用了这个决定。[试试换聊天接着做](examples/general/README.md)
- **玩家连点两次领奖，究竟会领到几份？** 顺着按钮找到实际发奖的代码和生效的配置，再分别试未完成、首次领取和重复点击。你能看见每个结果从哪里来，也知道上真机还要验证什么。[跟着查一次发奖流程](examples/game/README.md)
- **上一镜纸船刚从手边漂走，下一镜却又从放船拍起。** 把第一镜结束时船的位置、方向和动作写成第二镜的起点，再分别写静帧、分镜和视频提示词。改第二镜时，手边有一份清楚的衔接依据。[看看两个镜头怎样接起来](examples/ai-video/README.md)

示例可以直接阅读。想在自己的项目里试，准备 Python 3.10 或更高版本，跟着下面的步骤即可。工具只用 Python 标准库，Codex 插件可按需安装。

[English overview](docs/README.en.md) · [按任务找方法](plugins/monax-open-workflow/rules/context.md) · [验证记录](VALIDATION.md) · [MIT 许可证](LICENSE)

## 十分钟本地试用：无需安装插件

在本包根目录打开终端。以下命令只操作你新建的 `demo-project`，不会安装插件、联网或上传素材。

```powershell
mkdir demo-project
python -B plugins/monax-open-workflow/scripts/project.py init --project-root ./demo-project
python -B plugins/monax-open-workflow/scripts/project.py init --project-root ./demo-project --apply
python -B plugins/monax-open-workflow/scripts/project.py check --project-root ./demo-project
```

macOS/Linux 使用 `python3`。第一条 `init` 命令列出将创建的文件，加上 `--apply` 后才写入。第一次检查看到 **NeedsProjectFacts** 是正常的。接下来把你自己的项目目标和约束填进去。

在支持读取文件的 AI 工具中打开 `demo-project`，发送：

> 读取本项目 AGENTS.md。帮我整理当前项目的目标、阶段和约束；从已有文件核验，缺少的事实问我，不要把示例当事实。填写 PROJECT_CONTEXT，保持现有文件与任务范围。

对于纯演示，可参照 [通用项目示例](examples/general/README.md) 使用明确标注的虚构事实。真实项目必须使用自己的事实。解决后更新激活表 `blocking_items`，再运行：

```powershell
python -B plugins/monax-open-workflow/scripts/project.py check --project-root ./demo-project --require-ready
```

**Ready 只表示入口、规则快照和项目事实占位检查通过。** 不表示实现正确、插件生效、视频质量达标或用户已验收。

工具复制 `.monax-workflow/rules`、`.monax-workflow/templates` 和项目入口/事实骨架。接入后的静态规则无需依赖本包原位置；视频模板也随项目复制。

## 接入已有项目

把 `--project-root` 换成自己的项目路径，先运行不带 `--apply` 的预览。任何目标文件已存在时返回 Conflict，整批不写入；它不会覆盖现有 AGENTS.md、事实或定制规则。

不要删除旧上下文来强行初始化。在空临时目录生成一份模板，比较后合并入口、marker、规则快照和索引，保留项目原有约束，再执行检查。具体操作见 [接入与升级](docs/USAGE.md)。

工具不修改 `.gitignore` 或 Git 索引。团队可选择跟踪脱敏后的入口、规则和项目事实；个人记录是否跟踪由项目决定。不要把凭据写进共享上下文。

## 正常使用

完成接入后正常提出任务，不必每次说“读取记忆”。静态模式取决于宿主是否加载入口；切换主题后可用实际任务检查发现链。

- “修复领取按钮重复点击导致重复发奖，保留现有奖励规则。”
- “只读检查当前配置是否真的被运行场景使用。”
- “为一个虚构短片写两镜头导演卡和三层 Prompt，不生成、不上传。”
- “记录这次已确认的约束和剩余工作，下次从这里继续。”

完整练习与预期行为见 [examples](examples/README.md)。示例全部为虚构文本与小型代码，不包含真实项目资产或已生成媒体。

## 可选 Codex 插件

插件 ID 为 `monax-open-workflow`，本地 marketplace 为 `monax-open-workflow-local`，项目标记为 `.monax-workflow`。它与原工作流使用独立名称；不要在同一项目重复叠加两套入口，迁移前先合并规则。

只有需要自动技能发现和提醒时才安装。由使用者自行执行：

```powershell
codex plugin marketplace add .
```

随后在宿主支持的插件界面选择此本地来源、安装并启用插件，按提示重启并审阅信任 Hook。各客户端能力可能不同，安装方式以当前宿主和 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins) 为准。

提供五个技能：`$monax-open-setup`、`$monax-open-memory`、`$monax-open-development`、`$monax-open-game`、`$monax-open-video`。

两个只读 Hook 在 SessionStart / UserPromptSubmit 查找已接入标记，只发送规则指针，不读取项目业务正文、不回显用户 Prompt。Hook 需要单独审阅与信任，传输成功不证明模型遵循。见 [Hook 官方说明](https://learn.chatgpt.com/docs/hooks)。此包没有自动安装或信任脚本。

## 维护、验证与打包

```powershell
python -B tools/check_distribution.py
python -B tools/run_checks.py
python -B tools/package_release.py --output ../releases
```

打包只使用根目录 `distribution-files.json` 的显式文件清单，默认拒绝覆盖已有产物，输出 ZIP 和 SHA-256 清单；不执行 Git 提交、推送或上传。发布文件变化后先审查清单，再运行检查。

运行测试无需网络。包内工具不会调用付费服务。实际图像/视频工具、素材权利、费用与发布授权由使用者自己的项目负责。

## 范围与限制

这是独立公开发行版本，不是原私人仓库镜像；不带其历史、真实业务项目、个人习惯、安装缓存、运行回执或机器路径。通用方法经过重新组织，保留核心职责；源规则与本包不会自动双向同步。详见 [来源与适配](docs/PROVENANCE.md)。

实际验证范围见 [VALIDATION.md](VALIDATION.md)。Windows 为本轮验证环境；其他宿主和操作系统须独立验证。当前不声称效率提升比例，也不声称所有模型都会执行规则。

[MIT License](LICENSE) · [贡献方式](CONTRIBUTING.md) · [安全与隐私](SECURITY.md)
