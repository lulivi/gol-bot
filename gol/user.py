# Copyright (c) 2020 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""User related information."""
from enum import Enum
from operator import eq, ne
from typing import List


class UserOp(Enum):
    """Choose the operation to use when checking who has to do the normals."""

    CURRENT = eq
    OTHER = ne


class PushUpper:
    """Save information about one participant and their shared count.

    :cvar _normals: shared list of current person with normal push-ups to-do.
    :ivar _name: name of the participant.
    :ivar _id: identification of the participant.
    :ivar _punishments: number of punishment push-ups the participant has
        remaining.
    :ivar _rip_wknd: whether the participant has to continue talking correctly
        over the weekend.

    """

    _normals: List[str] = []

    def __init__(self, person_name: str, person_id: str) -> None:
        """Build a new push-ups counter.

        :param person_name: human readable name for the participant.
        :param person_id: ne identification for the participant.

        """
        self._name: str = person_name
        self._id: str = person_id
        self._punishments: int = 0
        self._rip_wknd: bool = False

    @property
    def name(self) -> str:
        """Variable ``_name`` getter.

        :returns: the ``_name`` value.

        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Variable ``_name`` setter.

        :param new_name: new value for the variable.

        """
        self._name = new_name

    @property
    def id(self) -> str:
        """Variable ``_id`` getter.

        :returns: the ``_id`` value.

        """
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        """Variable ``_id`` setter.

        :param new_id: new value for the variable.

        """
        self._id = new_id

    @property
    def rip_wknd(self) -> bool:
        """Variable ``_rip_wknd`` getter.

        :returns: the ``_rip_wknd`` value.

        """
        return self._rip_wknd

    @rip_wknd.setter
    def rip_wknd(self, new_rip_wknd) -> None:
        """Variable ``_rip_wknd`` setter.

        :param self: new value for the variable.

        """
        self._rip_wknd = new_rip_wknd

    def _has_normals(self, who: UserOp = UserOp.CURRENT) -> bool:
        """Check whether the choosen user in the ``who`` param has normals p-u.

        :param who: who we want to check the normals to.
        :returns: true when the choosen user (the current one or the other) has
            to do normal push-ups.

        """
        has_normals = False

        if self._normals and who.value(self._normals[-1], self._id):
            has_normals = True

        return has_normals

    @property
    def normals(self) -> List[str]:
        """Variable ``_normals`` getter.

        :returns: the ``_normals`` value.

        """
        return self._normals

    @normals.setter
    def normals(self, normals: List[str]) -> None:
        """Variable ``_normals`` setter.

        :param self: new value for the variable.

        """
        self._normals = normals

    @property
    def n_normals(self) -> int:
        """Get the number of normal push-ups for the current user.

        :returns: number of normal push-ups for the current user if any.

        """
        return len(self._normals) if self._has_normals() else 0

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
        """Variable ``_punishments`` getter.

        :returns: the ``_punishments`` value.

        """
        return self._punishments

    @punishments.setter
    def punishments(self, new_punishments: int) -> None:
        """Variable ``_punishments`` setter.

        :param self: new value for the variable.

        """
        self._punishments = new_punishments

    def add_punishments(self, number: int = 1) -> None:
        """Add another punishment.

        :param number: number of new punishments.

        """
        if number <= 0:
            raise ValueError(
                "You only can pass a positive number of punishment push-ups"
            )

        self._punishments += number

    def complete_pushups(self, number: int = 1) -> None:
        """Complete a number of pending push-ups.

        .. note:: This method will first end with the normal push-ups, then,
           with the punishment ones.

        :param number: number of push-up groups completed.

        """
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
        """String representation of the object.

        :returns: the representation.

        """
        modal_wknd_verb = "does" if self._rip_wknd else "doesn't"

        return (
            f"{self._name} has to do {self.n_normals} normal and "
            f"{self._punishments} punishment push-up blocks and "
            f"{modal_wknd_verb} have a bad weekend"
        )
