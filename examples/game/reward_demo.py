"""Fictional in-memory model: not an SDK, persistence or concurrency example."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RewardConfig:
    tokens_per_level: int


class RewardService:
    def __init__(self, config):
        self.config = config
        self.claimed_levels = set()
        self.balance = 0

    def claim(self, level_id, completed):
        if not completed or level_id in self.claimed_levels:
            return 0
        amount = self.config.tokens_per_level
        self.claimed_levels.add(level_id)
        self.balance += amount
        return amount


class RewardButton:
    def __init__(self, service):
        self.service = service

    def on_click(self, level_id, completed):
        return self.service.claim(level_id, completed)


if __name__ == "__main__":
    service = RewardService(RewardConfig(tokens_per_level=3))
    button = RewardButton(service)
    print({"incomplete": button.on_click("demo-01", False),
           "first": button.on_click("demo-01", True),
           "repeat": button.on_click("demo-01", True),
           "balance": service.balance})
