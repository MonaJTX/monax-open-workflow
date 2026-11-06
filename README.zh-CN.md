# MonaX Open Workflow

[English](README.md) · **简体中文**

**MonaX 是一套给 AI 助手用的项目工作流，帮你少花时间重复交代需求，也更容易检查 AI 交回来的工作。**

比如，你们昨天定下了「搜索只匹配标题，列表始终按加入时间倒序」。今天想加一个「只看未读」按钮，你可以直接谈这个按钮。MonaX 提供项目记忆模板和读取规则，让助手能从项目文件找回那两条约定，写进这次的方案。你和接手的同事也能打开同一份 Markdown，看到决定是怎么来的。[试试这个阅读清单项目](examples/general/README.md)

## 它能帮你做什么

| 你手上的事 | 用 MonaX 可以得到什么 |
| --- | --- |
| **隔几天继续做，或者把项目交给同事** | 一份随项目保存的交接记录，写清已定的要求、上次做到哪里、还有什么待验证。新聊天可以从下一件事开始。[项目记忆](plugins/monax-open-workflow/rules/memory.md) |
| **让 AI 给已有软件加功能、修问题** | 先找项目里能复用的实现，明确这次要改到哪里。交付时拿到改动说明、实际跑过的检查和仍需验证的部分，方便你决定能否采用。[开发流程](plugins/monax-open-workflow/rules/development.md) |
| **查一个游戏问题到底出在哪儿** | 沿玩家操作查到真正生效的代码、场景或配置。领奖示例里可以亲手跑出结果：同一关首次领取 3 枚，重复点击领取 0 枚，再看哪些行为还需要上真机验证。[运行领奖示例](examples/game/README.md) |
| **把一个视频想法交给下一位制作伙伴** | 从脚本拆出每镜的画面、动作和衔接，给静态图、分镜和视频分别写提示词。伙伴拿到镜头包和台账，就能看见哪些素材待准备、哪一镜等审阅。[打开两镜头提示词](examples/ai-video/shots.md) · [看配套台账](examples/ai-video/ledger.md) |

可以先点开上面的成品示例。想让自己的 AI 用起来，准备一个能读本地文件的助手和 Python 3.10 或更高版本，即可从一个小项目开始。

[下载并试用](#第一次用从-github-到本地) · [接入自己的项目](#用到自己的项目) · [MIT 许可证](LICENSE)

## 第一次用，从 GitHub 到本地

在准备存放工具的目录打开终端，运行：

```sh
git clone https://github.com/MonaJTX/monax-open-workflow.git
cd monax-open-workflow
python --version
```

也可以在 GitHub 点 **Code → Download ZIP**，解压后在能同时看见 `README.md` 和 `plugins` 的那一层打开终端。确认 Python 版本至少为 3.10。macOS/Linux 通常把以下命令里的 `python` 写成 `python3`，Windows 如果只有 `py`，可以用 `py -3`。

接下来的**终端命令都在下载的 MonaX 目录运行**。参数 `--project-root` 指向你想接入的项目。跟 AI 聊天时则打开那个项目，让它能读到项目自己的文件。

## 先体验一次「换聊天接着做」

**1. 建一个练习项目。** 第一次试用请选一个尚不存在的 `demo-project` 目录。运行下面四行：

```sh
mkdir demo-project
python -B plugins/monax-open-workflow/scripts/project.py init --project-root "./demo-project"
python -B plugins/monax-open-workflow/scripts/project.py init --project-root "./demo-project" --apply
python -B plugins/monax-open-workflow/scripts/project.py check --project-root "./demo-project"
```

两次 `init` 的结果依次是 `Planned`（预览）和 `Created`（写入）。检查会显示 `NeedsProjectFacts`，并在 `pending` 里列出需要填写的文件。此时工具已经准备好，接下来给练习项目一点背景。

**2. 让 AI 认识这个项目。** 用文件管理器把 [阅读清单练习说明](examples/general/project-brief.md) 复制进刚建好的 `demo-project`，保留文件名 `project-brief.md`。在能读写本地文件的 AI 工具里打开 **demo-project**，发送：

> 请读 AGENTS.md 和 project-brief.md。根据练习说明，把项目目标、当前进度、技术约束和已经商量好的决定分别写到 PROJECT_CONTEXT 索引指向的文件，替换对应的 TODO。核对完身份、阶段和约束后，在 workflow_activation_profile.json 的 blocking_items 中移除这一条已解决的提醒。只整理项目说明。

回到之前的终端运行：
```sh
python -B plugins/monax-open-workflow/scripts/project.py check --project-root "./demo-project" --require-ready
```

看到 `Ready` 表示项目说明已就位。仍是 `NeedsProjectFacts` 时，按 `pending` 里的文件名补齐事实；如果是 `Blocked`，先看 `issues` 指出的文件或入口。

**3. 在同一个 demo-project 打开新聊天。** 这次只问：

> 阅读清单里，搜索和「未读」筛选一起用，结果该怎么排？请告诉我依据哪份项目文件。

看回答是否同时保留三条约定：只匹配标题、只显示未读条目、仍按加入时间倒序。答案还应能指到保存这些决定的项目文件。如果 AI 读不到文件，先检查打开的文件夹；若工具需要手动指定入口，请它先读 `AGENTS.md` 再试。[完整练习](examples/general/README.md)

## 用到自己的项目

假设你的工具和项目是并排的两个目录 `monax-open-workflow` 和 `我的项目`。在 **monax-open-workflow** 的终端先预览，把引号里的路径换成自己已有的项目目录：

```sh
python -B plugins/monax-open-workflow/scripts/project.py init --project-root "../我的项目"
```

- **看到 `Planned`**：看一眼 `planned` 列出的文件。决定接入后，运行同一条命令并在末尾加 `--apply`，预期返回 `Created`。
- **看到 `Conflict`**：`conflicts` 会列出已有的文件名。保留你的文件，按[已有 AGENTS.md 或项目记录时的合并步骤](docs/USAGE.md#已有项目合并)操作。
- **已经接入过**：直接运行下面的 `check`，从现有记录接着做。

现在在 AI 工具中打开 **你自己的项目**，把下面这句话发给它：

> 请读 AGENTS.md，结合这个项目的 README、现有文件和我的说明，把目标、当前进度、需要保留的约束填进 PROJECT_CONTEXT。遇到只有我知道的事就问我。核对每一项后，更新 workflow_activation_profile.json 里已解决的 blocking_items。

再在 MonaX 目录检查一次：
```sh
python -B plugins/monax-open-workflow/scripts/project.py check --project-root "../我的项目" --require-ready
```

接下来就可以在项目里正常提需求。软件项目可以问「加这个筛选会影响现有排序吗」；游戏项目可以问「实际场景读取的是哪份配置」；视频项目可以说「只调整第二镜的出口，保留第一镜」。项目说明留在你自己的文件夹，后续聊天可以继续读取。[共享和升级方法](docs/USAGE.md)

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
