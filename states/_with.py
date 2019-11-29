from ._state import State


class WithCTE(State):
    @property
    def possible_states(self):
        return ()
