from ._finite import Finite
from ._having import Having
from ._state import State
from ._limit import Limit
from ._offset import Offset
from ._order_by import OrderBy


class GroupBy(State):
    @property
    def possible_states(self):
        return Having, OrderBy, Limit, Offset, Finite
