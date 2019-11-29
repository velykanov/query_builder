from ._finite import Finite
from ._state import State


class Offset(State):
    @property
    def possible_states(self):
        return (
            Finite,
        )
