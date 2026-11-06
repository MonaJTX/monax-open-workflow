# 项目记忆读取规则

Owner：本文件。Rule ID：MEMORY-READ-01。

在项目相关回答、建议或改动前，以及新任务、切换主题/子项目、压缩恢复时，从当前项目 AGENTS.md 和 PROJECT_CONTEXT/README.md 检索相关长期约束。无需用户提醒“读记忆”。已在有效上下文读过且有来源的正文可复用；版本、配置或约束变化后只复核受影响部分。

检索用当前对象、动作与同义词，例如存档/持久化、奖励/解锁、BGM/配乐、排行榜/分数。集合仓库需继续到所选子项目索引，最近项目的规则不自动归于其他子项目。没有命中时只扩大到相关 PROJECT_CONTEXT、README 和已知 owner，不扫描所有历史聊天、全局记忆或其他项目。

读取命中规则的正文和必要状态 owner，把约束落实到本次产物检查。文件存在、看过标题、搜索片段、总览页均不能代替正文证据。模板只是待核验问题，不是当前事实。

记忆不可读或来源冲突时说明具体缺口，继续不依赖它的已授权工作；不能把“没读到”当“没有限制”。明确的新用户决定可替代旧约束，但应定位更新原 owner；旧授权与费用不能跨目标继承。

按实际任务选择以下主文件，不按某个关键词全量加载：

| 任务 | 读取 |
| --- | --- |
| 需求、实现、修复、复用选型 | [development.md](development.md) |
| UI、架构取舍、性能或审查 | [design-review.md](design-review.md) 的相关部分 |
| 游戏行为、引擎资产、平台交付 | [game-development.md](game-development.md) |
| 预约/异步完成、缓存、字体覆盖、资产适配 | [game-methods.md](game-methods.md) 的匹配方法 |
| AI 视频策划、静态图、分镜或生产 | [ai-video.md](ai-video.md)，再按阶段进入子文件 |
| 长期记录、接续、经验提炼 | [memory.md](memory.md) |
| 授权或任务范围不清 | [boundaries.md](boundaries.md) |
| 验证、交付、验收 | [verification.md](verification.md) |

每次补读解决具体证据缺口，足够判断时停止。代码任务不会因存在视频模块而读取视频方法。混合项目只加载本次实际涉及的模块。catalog.json 的 conditional_rules 是触发目录，不表示所有项目都必须执行。
