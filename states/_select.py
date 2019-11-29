"""Select state module"""
from ._finite import Finite
from ._group_by import GroupBy
from ._limit import Limit
from ._offset import Offset
from ._order_by import OrderBy
from ._state import State
from ._where import Where


class Select(State):
    @property
    def possible_states(self):
        return Where, GroupBy, OrderBy, Limit, Offset, Finite
