"""Date/Time fields module"""
from ._field import Field


POSSIBLE_PRECISION = [0, 1, 2, 3, 4, 5, 6]


class Date(Field):
    """Date field type. Look at :class:`~Field`"""
    _type = 'date'


class Time(Field):
    """
    Time field type

    Args:
        name (str): Column name in DB (**required**)
        alias (str): Alias for column (``None`` - default)
        table (str): Table name for prefixing (``None`` - default)
        precision (int): Seconds precision (``None`` - default)
        with_tz (bool): Defines field type 'time' or 'timetz' (``False`` - default)
    """
    _type = 'time'

    def __init__(self, name, alias=None, table=None, precision=None, with_tz=False):
        if with_tz:
            self._type = '{}tz'.format(self._type)

        if precision is not None:
            if precision not in POSSIBLE_PRECISION:
                raise ValueError('precision must be in [0, 6]')

            self.precision = precision

        super(Time, self).__init__(
            name,
            alias,
            table,
            precision=precision,
            with_tz=with_tz,
        )


class Timestamp(Time):
    """Timestamp field type. Look at :class:`~Time`"""
    _type = 'timestamp'
