from ._finite import Finite
from ._limit import Limit
from ._offset import Offset
from ._state import State


class OrderBy(State):
    @property
    def possible_states(self):
        return Limit, Offset, Finite
