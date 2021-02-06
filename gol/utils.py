from typing import NamedTuple


class PushUps:
    def __init__(self, normal: int = 0, punishment: int = 0) -> None:
        self.normal: int = normal
        self.punishment: int = punishment

    def __str__(self):
        return (
            f"{self.normal} normal and {self.punishment} punishment push-ups"
        )


class PushUpper:
    def __init__(self, name: str, count: PushUps = PushUps()) -> None:
        self.name: str = name
        self.count: PushUps = count

    def __str__(self):
        return f"{self.name} has to do {self.count}"
