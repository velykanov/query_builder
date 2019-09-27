"""Character fields module"""
from ._field import Field


class Text(Field):
    _type = 'text'

    def __add__(self, other):
        """Do concatenation"""
        return self._general_operation(other, '||')

    def __radd__(self, other):
        return self._general_operation(other, '||', inverse=True)

    def upper(self):
        return self._wrap_function('upper')

    def lower(self):
        return self._wrap_function('lower')


class Varchar(Text):
    _type = 'varchar'
    _has_constraints = True

    def __init__(self, name, alias=None, table=None, quote=True, max_length=1):
        self.max_length = max_length

        super(Varchar, self).__init__(
            name,
            alias,
            table,
            quote,
            max_length=max_length,
        )

    def _check_constraints(self, value):
        if isinstance(value, Field):
            return True

        if isinstance(value, str) and len(value) <= self.max_length:
            return True

        raise ValueError('value does not conform constraints')


class Char(Varchar):
    _type = 'char'
