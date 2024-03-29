"""Clause module"""
import json

from ._expression import Expression


class Clause:
    """
    Clause class describes clauses that goes in `where` section.

    Args:
        field (Field): Field with comparison conditions
    """
    def __init__(self, field):
        self._field = field

    def __join(self, other, operand='AND'):
        if isinstance(other, bool):
            value = json.dumps(other)
        elif isinstance(other, self.__class__):
            value = getattr(other, '_field')
        else:
            raise TypeError(
                "unsupported operand type(s) for and: '{}' and '{}'".format(
                    type(self).__name__,
                    type(other).__name__,
                ),
            )

        if operand == 'AND':
            expression = '{} AND {}'.format(self._field, value)
        else:
            expression = '({} OR {})'.format(self._field, value)

        return self.__class__(Expression(expression))

    def __and__(self, other):
        return self.__join(other)

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        return self.__join(other, 'OR')

    def __ror__(self, other):
        return self.__or__(other)

    def __repr__(self):
        return "<Clause '{}'>".format(self)

    def __str__(self):
        return str(self._field)
