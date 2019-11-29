"""Initial state module"""
# from ._delete import Delete
# from ._insert import Insert
from ._select import Select
from ._state import State
# from ._update import Update
# from ._with import WithCTE


class Initial(State):
    @property
    def possible_states(self):
        return (
            Select,
        )
