from ._state import State


class Finite(State):
    @property
    def possible_states(self):
        return ()
