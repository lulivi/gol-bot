import json

from gol.error import WrongCounterFileFormatError
from gol.settings import SAVE_FILE
from gol.user import PushUpper
from gol.utils import is_weekend


class PushUpsCounter:
    def __init__(
        self,
        first_person_name: str,
        first_person_id: str,
        second_person_name: str,
        second_person_id: str,
    ) -> None:
        self._first_id = first_person_id
        self._second_id = second_person_id
        self._ppl = {
            self._first_id: PushUpper(first_person_name, first_person_id),
            self._second_id: PushUpper(second_person_name, second_person_id),
        }

    def __getitem__(self, key) -> PushUpper:
        if key not in self._ppl:
            raise KeyError(f"Could not find user '{key}'")

        return self._ppl[key]

    def add_pushups(self) -> None:
        pass

    def load_count(self) -> None:
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

        self._ppl[self._first_id].set_normals(normals)
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
                "normals": p1.get_normals(),
            },
            SAVE_FILE.open("w"),
            indent=4,
        )

    def push_up_table(self) -> str:
        p1 = self._ppl[self._first_id]
        p2 = self._ppl[self._second_id]
        return (
            "            +----------+----------+\n"
            f"            |{p1.name[:5]:^10}|{p2.name[:5]:^10}|\n"
            "+-----------+----------+----------+\n"
            f"|    Normals|{p1.normals:^10}|{p2.normals:^10}|\n"
            f"|Punishments|{p1.punishments:^10}|{p2.punishments:^10}|\n"
            f"|RIP Weekend|{p1.rip_wknd!r:^10}|{p2.rip_wknd!r:^10}|\n"
            "+-----------+----------+----------+"
        )

    def __str__(self) -> str:
        return f"{self._ppl[self._first_id]}; {self._ppl[self._second_id]}."
