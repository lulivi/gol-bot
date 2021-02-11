# Copyright (c) 2020 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Counter main class."""
import json

from typing import Dict

from gol.error import WrongCounterFileFormatError
from gol.settings import SAVE_FILE
from gol.user import PushUpper
from gol.utils import is_weekend


class PushUpsCounter:
    """Manage the participants of the push-ups competition.

    :ivar _first_id: the first person identificator.
    :ivar _second_id: the second person identificator.
    :ivar _ppl: a dictionary containing the two participants by their
        identificator.

    """

    def __init__(
        self,
        first_person_name: str,
        first_person_id: str,
        second_person_name: str,
        second_person_id: str,
    ) -> None:
        """Build a new push-ups counter.

        :param first_person_name: human readable name for the first
            participant.
        :param first_person_id: machine identification for the first
            participant.
        :param second_person_name: human readable name for the second
            participant.
        :param second_person_id: machine identification for the second
            participant.

        """
        self._first_id: str = first_person_id
        self._second_id: str = second_person_id
        self._ppl: Dict[str, PushUpper] = {
            self._first_id: PushUpper(first_person_name, first_person_id),
            self._second_id: PushUpper(second_person_name, second_person_id),
        }

    def __getitem__(self, key: str) -> PushUpper:
        """Easy access to the participants by their identification.

        :param key: identification string for the participant.
        :raises KeyError: when the participant does not exist.
        :returns: the participant object.

        """
        if key not in self._ppl:
            raise KeyError(f"Could not find user '{key}'")

        return self._ppl[key]

    def add_pushups(self) -> None:
        pass

    def load_count(self) -> None:
        """Read the counter saved values from a file."""
        json_count = json.load(SAVE_FILE.open("r"))
        normals = json_count.pop("normals")

        if len(json_count) != 2:
            raise WrongCounterFileFormatError(
                "It should only be two id's in the serialized config file"
            )

        id_list = list(self._ppl)

        if any(map(lambda x: x not in id_list, normals)):
            raise WrongCounterFileFormatError(
                "The normals list does not match with the provided id's"
            )

        self._ppl[self._first_id].normals = normals
        self._ppl[self._first_id].name = json_count[self._first_id]["name"]
        self._ppl[self._first_id].rip_wknd = json_count[self._first_id][
            "rip_wknd"
        ]
        self._ppl[self._first_id].punishments = json_count[self._first_id][
            "punishments"
        ]
        self._ppl[self._second_id].name = json_count[self._second_id]["name"]
        self._ppl[self._second_id].rip_wknd = json_count[self._second_id][
            "rip_wknd"
        ]
        self._ppl[self._second_id].punishments = json_count[self._second_id][
            "punishments"
        ]

    def save_count(self) -> None:
        """Save the counter into a file."""
        p1 = self._ppl[self._first_id]
        p2 = self._ppl[self._second_id]

        json.dump(
            {
                self._first_id: {
                    "name": p1.name,
                    "rip_wknd": p1.rip_wknd,
                    "punishments": p1.punishments,
                },
                self._second_id: {
                    "name": p2.name,
                    "rip_wknd": p2.rip_wknd,
                    "punishments": p2.punishments,
                },
                "normals": p1.normals,
            },
            SAVE_FILE.open("w"),
            indent=4,
        )

    def push_up_table(self) -> str:
        """Write a pretty table with the counter information.

        :returns: a table string.

        """
        p1 = self._ppl[self._first_id]
        p2 = self._ppl[self._second_id]
        return (
            "            +----------+----------+\n"
            f"            |{p1.name[:5]:^10}|{p2.name[:5]:^10}|\n"
            "+-----------+----------+----------+\n"
            f"|    Normals|{p1.n_normals:^10}|{p2.n_normals:^10}|\n"
            f"|Punishments|{p1.punishments:^10}|{p2.punishments:^10}|\n"
            f"|RIP Weekend|{p1.rip_wknd!r:^10}|{p2.rip_wknd!r:^10}|\n"
            "+-----------+----------+----------+"
        )

    def __str__(self) -> str:
        """String representation of the object.

        :returns: the representation.

        """
        return f"{self._ppl[self._first_id]}; {self._ppl[self._second_id]}."
