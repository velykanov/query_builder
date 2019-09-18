"""Date/Time fields module"""
from ._field import Field


class Date(Field):
    _type = 'date'


class Time(Field):
    _type = 'time'

    def __init__(self, name, alias=None, table=None, quote=True, precision=None, with_tz=False):
        if with_tz:
            self._type = 'timetz'

        if precision is not None:
            if precision not in range(7):
                raise ValueError('precision must be in [0, 6]')

            self.precision = precision

        super(Time, self).__init__(
            name,
            alias,
            table,
            quote,
            precision=precision,
            with_tz=with_tz,
        )


class Timestamp(Field):
    _type = 'timestamp'

    def __init__(self, name, alias=None, table=None, quote=True, precision=None, with_tz=False):
        if with_tz:
            self._type = 'timestamptz'

        if precision is not None:
            if precision not in range(7):
                raise ValueError('precision must be in [0, 6]')

            self.precision = precision

        super(Timestamp, self).__init__(
            name,
            alias,
            table,
            quote,
            precision=precision,
            with_tz=with_tz,
        )
