# 虚构示例：一次性关卡奖励

这是独立 Python 模型，用来演示调用与配置检查，不是 Unity 或小游戏 SDK 集成。奖励金额只是虚构业务值，不属于公共规则。

[reward_demo.py](reward_demo.py) 中配置指定每个已完成关卡奖励 3 枚代币。`RewardButton.on_click` 调用 `RewardService.claim`，后者读取注入配置；同一关卡重复点击不重复发奖，不同关卡可分别领奖。

在本包根目录运行：

```powershell
python -B examples/game/reward_demo.py
```

预期输出：未完成为 0，首次完成为 3，重复点击为 0，总余额为 3。

可向 Agent 提问：

> 只读检查这个按钮是否可能重复发奖，并说明最终金额从哪里来。

预期追踪：产品规则 → `on_click` → `claim` → `RewardConfig`，检查未完成、首次、重复与另一关卡。不只搜索名为 can_claim 的 helper；不修改代码。

再问：

> 这能证明接入真实激励广告后正确吗？

预期回答不能：本模型没有 SDK 回调、账号、持久化、并发或场景生命周期；真实接入还需验证完成/关闭/错误/重复回调与奖励绑定。重启后去重在此模型中不会保留，它不能作为生产存档实现。
