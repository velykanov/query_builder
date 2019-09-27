"""Date/Time fields module"""
from ._field import Field


POSSIBLE_PRECISION = [0, 1, 2, 3, 4, 5, 6]


class Date(Field):
    _type = 'date'


class Time(Field):
    _type = 'time'

    def __init__(self, name, alias=None, table=None, precision=None, with_tz=False):
        if with_tz:
            self._type = 'timetz'

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


class Timestamp(Field):
    _type = 'timestamp'

    def __init__(self, name, alias=None, table=None, precision=None, with_tz=False):
        if with_tz:
            self._type = 'timestamptz'

        if precision is not None:
            if precision not in POSSIBLE_PRECISION:
                raise ValueError('precision must be in [0, 6]')

            self.precision = precision

        super(Timestamp, self).__init__(
            name,
            alias,
            table,
            precision=precision,
            with_tz=with_tz,
        )
