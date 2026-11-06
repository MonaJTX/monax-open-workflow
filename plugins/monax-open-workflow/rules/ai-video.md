# AI 视频工作流入口

Rule ID：VIDEO-PIPELINE-01。适用于脚本到镜头、静态图、导演分镜、动态生成、后期及审片。这里只提供方法，不自带图像/视频服务，不自动上传或生成。

## 项目先于案例

先读取当前项目的传播目标、受众、脚本、角色/主体母版、视觉基线、交付规格和工具限制。故事、角色、品牌、审美、镜头秒数与模型选择均由当前项目决定，不继承其他项目的事实或偏好。

已有材料可参考方法，不能自动借用人物、构图、机位或台词。模板是待填写问题，不是生产数据；素材来源与使用边界必须能定位。

## 阶段与按需读取

| 阶段 | 主文件 | 主要结果 |
| --- | --- | --- |
| 需求和策划 | 本文件 | 项目 Brief、脚本、视觉方向、交付范围 |
| 导演设计 | [ai-video-directing.md](ai-video-directing.md) | 镜头总表、导演卡、时长与出口 |
| 静态图/分镜/视频 Prompt | [ai-video-prompts.md](ai-video-prompts.md) | 自包含镜头包和实际输入绑定 |
| 真实素材、上传、付费、下载、审片 | [ai-video-production.md](ai-video-production.md) | 生产台账、输入输出版本、检查与采用状态 |
| 复盘与恢复 | [memory.md](memory.md) | 现行基线、剩余工作、失败经验与失效条件 |

建议流程：Brief → 脚本与事实边界 → 主体母版与全片视觉方向 → 镜头总表 → 导演卡 → 静态图审阅 → 导演分镜审阅 → 动态 Prompt 与提交预检 → 视频候选 → 后期 → 整片验收。

每层解决不同问题，不把整篇文字直接丢给模型生成完整长片。任务明确只要脚本或 Prompt 时，交付对应阶段，不要求先购买或调用生成工具。

## 生产模式

在项目中明确 PromptHandoff（交接 Prompt）、AgentOrchestrated（Agent 编排）或 Hybrid（混合）。记录 Agent 负责哪些阶段、用户审阅点、可用工具、外部操作授权和状态台账。用户已授权的同范围动作可继续；模式名称本身不授予上传、扣费、重试或发布权限。

典型状态：Planned → InputsBound → StaticReview → StoryboardReview → VideoPreflight → Submitted → Downloaded → TechnicalPass → ReviewCandidate → UserAccepted。

Rejected、Paused、Superseded 和 DoNotUseAsReference 独立保留。未采用候选不覆盖正式基线；用户暂停时停止相应动作并保存恢复信息。一次只完成镜头资产链时，不声称整片已经自动完成。

## 项目 Brief

使用 [Brief 模板](../templates/video-brief.md)，只填当前任务需要的字段。核心是：观众需要理解什么、哪些内容必须保真、风格和交付规格、采用什么生产路线、谁在何时决定采用。

系列或批次接续时，从项目 owner 恢复已确认的角色、风格和默认配套交付。只修一个镜头时保护已接受邻镜；修改 beat、时长或出口后核对衔接。用户明确限定范围时记录本轮例外。

## 复盘

分别记录设计、输入/Prompt、模型输出和平台/传输问题。保留问题是 Open、Mitigated、Verified 还是 Recurring，以及实际证据。单轮有效只表示条件性经验，不能因某个失败词出现过就把它设成所有项目的禁词。

只有经过去项目化且有明确适用条件的方法才适合分享；原始素材、账号、费用回执和私人项目事实留在各项目受控目录。
