from ._state import State


class Join(State):
    @property
    def possible_states(self):
        return ()
