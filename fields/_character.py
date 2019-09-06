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

    def __init__(self, name, alias=None, table=None, quote=True, max_length=None):
        if max_length is None:
            self.max_length = 1

        super(Varchar, self).__init__(name, alias, table, quote, max_length=max_length)


class Char(Varchar):
    _type = 'char'
