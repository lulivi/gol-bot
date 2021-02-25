# Copyright (c) 2021 Luis Liñán Villafranca. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>
"""Counter main class."""
import json

from json.decoder import JSONDecodeError
from typing import Dict, Optional

from gol.error import ParticipantNotFound, WrongCounterFileFormatError
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

    def __init__(self) -> None:
        """Instantiate the class."""
        self._first_id: str = ""
        self._second_id: str = ""
        self._ppl: Dict[str, PushUpper] = {}

    def config(
        self,
        first_person_name: str,
        first_person_id: str,
        second_person_name: str,
        second_person_id: str,
    ) -> None:
        """Configure the counter.

        :param first_person_name: human readable name for the first
            participant.
        :param first_person_id: machine identification for the first
            participant.
        :param second_person_name: human readable name for the second
            participant.
        :param second_person_id: machine identification for the second
            participant.

        """
        self._clean()
        self._first_id = first_person_id
        self._second_id = second_person_id
        self._ppl[self._first_id] = PushUpper(
            first_person_name, first_person_id
        )
        self._ppl[self._second_id] = PushUpper(
            second_person_name, second_person_id
        )
        self.save_count()

    def is_configured(self) -> bool:
        """Check if the counter is configured.

        :returns: True if the counter is configured.

        """
        is_configured = False

        if self._first_id and self._second_id and len(self._ppl) == 2:
            is_configured = True

        return is_configured

    def add_pushups(self, requester: str, target: str) -> None:
        """Apply the correct push-ups depending of the choosen rules.

        :param requester: the requester participant identification.
        :param target: the identification of the target messager.

        """
        requester_user = self._ppl[requester]
        non_requester_user = self._ppl[self.opposite(requester)]

        if requester == target:
            if is_weekend():
                requester_user.add_normals(1)
            else:
                non_requester_user.add_normals(1)
        else:
            if is_weekend():
                requester_user.add_normals(2)
            else:
                requester_user.add_normals(1)

    def process_audio(self, sender: str) -> None:
        """Add the necessary push-ups if the conditions are chosen.

        :param sender: the push-ups inquisitor.

        """
        if is_weekend() and self._ppl[sender].rip_wknd:
            self.add_pushups(self.opposite(sender), sender)

    def process_error(self, sender: str) -> None:
        """Add necesary push-ups when error occurs.

        :param sender: the push-ups inquisitor.

        """
        opposite = self.opposite(sender)
        self.add_pushups(sender, opposite)
        self.add_pushups(sender, opposite)

    def load_count(self) -> None:
        """Read the counter saved values from a file."""
        try:
            json_count = json.load(SAVE_FILE.open("r"))
        except JSONDecodeError as error:
            raise WrongCounterFileFormatError(
                f"There was an error reading the config file: {error}"
            )
        normals = json_count.pop("normals")

        if len(json_count) != 2:
            raise WrongCounterFileFormatError(
                "It should only be two id's in the serialized config file"
            )

        id_list = list(json_count.keys())

        if any(map(lambda x: x not in id_list, normals)):
            raise WrongCounterFileFormatError(
                "The normals list does not match with the provided id's"
            )

        self.config(
            json_count[id_list[0]]["name"],
            id_list[0],
            json_count[id_list[1]]["name"],
            id_list[1],
        )

        first_person = json_count[self._first_id]
        second_person = json_count[self._second_id]

        self._ppl[self._first_id].normals = normals
        self._ppl[self._first_id].name = first_person["name"]
        self._ppl[self._first_id].rip_wknd = first_person["rip_wknd"]
        self._ppl[self._first_id].punishments = first_person["punishments"]
        self._ppl[self._second_id].name = second_person["name"]
        self._ppl[self._second_id].rip_wknd = second_person["rip_wknd"]
        self._ppl[self._second_id].punishments = second_person["punishments"]

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

    def opposite(self, participant_id: str) -> str:
        """Obtain the opposite participant.

        :param participant_id: id of the participant to check the other.
        :returns: the opposite participant.

        """
        if participant_id not in self._ppl:
            raise ParticipantNotFound(
                f"Couldn't find the participant {participant_id}"
            )

        return set(self._ppl).difference({participant_id}).pop()

    def _clean(self) -> None:
        """Clean the counter."""
        self._first_id = ""
        self._second_id = ""
        self._ppl.clear()

    def __str__(self) -> str:
        """Return the string representation of the object.

        :returns: the representation.

        """
        return f"{self._ppl[self._first_id]}; {self._ppl[self._second_id]}."
