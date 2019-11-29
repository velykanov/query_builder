from ._finite import Finite
from ._offset import Offset
from ._state import State


class Limit(State):
    @property
    def possible_states(self):
        return Offset, Finite
