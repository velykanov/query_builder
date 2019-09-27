"""Character fields module"""
from ._field import Field


class Text(Field):
    """Text field type"""
    _type = 'text'

    def __add__(self, other):
        """Do concatenation"""
        return self._general_operation(other, '||')

    def __radd__(self, other):
        return self._general_operation(other, '||', inverse=True)

    def upper(self):
        """
        Wraps field into upper(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('upper')

    def lower(self):
        """
        Wraps field into lower(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('lower')


class Varchar(Text):
    """Varchar field type"""
    _type = 'varchar'
    _has_constraints = True

    def __init__(self, name, alias=None, table=None, max_length=1):
        self.max_length = max_length

        super(Varchar, self).__init__(name, alias, table, max_length=max_length)

    def _check_constraints(self, value):
        if isinstance(value, Field):
            return True

        if isinstance(value, str) and len(value) <= self.max_length:
            return True

        raise ValueError('value does not conform constraints')


class Char(Varchar):
    """Char field type"""
    _type = 'char'
