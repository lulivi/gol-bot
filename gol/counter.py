from gol.utils import PushUpper


class PushUpsCounter:
    def __init__(
        self, first_person_name: str, second_person_name: str
    ) -> None:
        self._px = PushUpper(first_person_name)
        self._py = PushUpper(second_person_name)
        setattr(self, first_person_name, self._px)
        setattr(self, second_person_name, self._py)

    @property
    def px(self):
        return self._px

    @property
    def py(self):
        return self._py

    def __str__(self):
        return f"{self._px}; {self._py}."
