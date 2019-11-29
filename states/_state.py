"""State module"""
import functools


def state_aware(state):

    def _state_aware(decorated):

        @functools.wraps(decorated)
        def wrapper(*args, **kwargs):

            if args:
                current_state = getattr(args[0], '_state')
                if isinstance(current_state, state):
                    return args[0]

                try:
                    setattr(args[0], '_state', current_state.set_state(state))
                except ValueError:
                    args[0].reset()
                    raise

            return decorated(*args, **kwargs)

        return wrapper

    return _state_aware


class State:
    def __str__(self):
        return self.__class__.__name__

    @property
    def possible_states(self):
        raise NotImplementedError

    def set_state(self, state):
        if state not in self.possible_states:
            raise ValueError('Impossible action: {} -> {}'.format(
                str(self),
                str(state()),
            ))

        return state()
