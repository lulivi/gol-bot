from enum import Enum
from operator import eq, ne
from typing import List


class UserOp(Enum):
    CURRENT = eq
    OTHER = ne


class PushUpper:
    _normal: List[str] = []

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._punishment: int = 0

    def _has_normals(self, who: UserOp = UserOp.CURRENT) -> bool:
        has_normals = False

        if self._normal:
            if who.value(self._normal[-1], self._name):
                has_normals = True

        return has_normals

    def add_normal(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError("You only can add positive punishment push-ups")

        while number > 0:
            if self._has_normals(UserOp.OTHER):
                if len(self._normal) > number:
                    del self._normal[-number:]
                    break
                else:
                    number -= len(self._normal)
                    self._normal.clear()
            else:
                self._normal.extend([self._name] * number)
                break

    def add_punishment(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError(
                "You only can pass a positive number of punishment push-ups"
            )

        self._punishment += number

    def complete_pushup(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError("You only can pass a positive number of push-ups")

        if self._punishment > number:
            self._punishment -= number
        else:
            number -= self._punishment
            self._punishment = 0

            if self._has_normals():
                if len(self._normal) > number:
                    del self._normal[-number:]
                else:
                    self._normal.clear()

    def __str__(self):
        person_normal_pushups = (
            len(self._normal) if self._name in self._normal else 0
        )
        return (
            f"{self._name} has to do {person_normal_pushups} normal and "
            f"{self._punishment} punishment push-up blocks."
        )
