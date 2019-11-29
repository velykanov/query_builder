from ._finite import Finite
from ._order_by import OrderBy
from ._state import State
from ._limit import Limit
from ._offset import Offset


class Having(State):
    @property
    def possible_states(self):
        return OrderBy, Limit, Offset, Finite
