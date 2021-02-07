from enum import Enum
from operator import eq, ne
from typing import List


class UserOp(Enum):
    CURRENT = eq
    OTHER = ne


class PushUpper:
    _normals: List[str] = []

    def __init__(self, person_name: str, person_id: str) -> None:
        self._name: str = person_name
        self._id: str = person_id
        self._punishments: int = 0
        self._rip_wknd: bool = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        self._id = new_id

    @property
    def rip_wknd(self) -> bool:
        return self._rip_wknd

    @rip_wknd.setter
    def rip_wknd(self, new_rip_wknd) -> None:
        self._rip_wknd = new_rip_wknd

    def _has_normals(self, who: UserOp = UserOp.CURRENT) -> bool:
        has_normals = False

        if self._normals and who.value(self._normals[-1], self._id):
            has_normals = True

        return has_normals

    @property
    def normals(self) -> int:
        return len(self._normals) if self._has_normals() else 0

    def get_normals(self) -> List[str]:
        return self._normals

    def set_normals(self, normals: List[str]) -> None:
        self._normals = normals

    def add_normals(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError("You only can add positive punishment push-ups")

        while number > 0:
            if self._has_normals(UserOp.OTHER):
                if len(self._normals) > number:
                    del self._normals[-number:]
                    break
                else:
                    number -= len(self._normals)
                    self._normals.clear()
            else:
                self._normals.extend([self._id] * number)
                break

    @property
    def punishments(self) -> int:
        return self._punishments

    @punishments.setter
    def punishments(self, new_punishments: int) -> None:
        self._punishments = new_punishments

    def add_punishments(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError(
                "You only can pass a positive number of punishment push-ups"
            )

        self._punishments += number

    def complete_pushups(self, number: int = 1) -> None:
        if number <= 0:
            raise ValueError("You only can pass a positive number of push-ups")

        if self._punishments > number:
            self._punishments -= number
        else:
            number -= self._punishments
            self._punishments = 0

            if self._has_normals():
                if len(self._normals) > number:
                    del self._normals[-number:]
                else:
                    self._normals.clear()

    def __str__(self) -> str:
        modal_wknd_verb = "does" if self._rip_wknd else "doesn't"

        return (
            f"{self._name} has to do {self.normals} normal and "
            f"{self._punishments} punishment push-up blocks and "
            f"{modal_wknd_verb} have a bad weekend"
        )
