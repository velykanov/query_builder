"""Date/Time fields module"""
from . import Field


class Date(Field):
    _type = 'date'


class Time(Field):
    _type = 'time'

    def __init__(self, name, alias=None, with_tz=False):
        if with_tz:
            self._type = 'timetz'

        super(Time, self).__init__(name, alias)


class Timestamp(Field):
    _type = 'timestamp'

    def __init__(self, name, alias=None, with_tz=False):
        if with_tz:
            self._type = 'timestamptz'

        super(Timestamp, self).__init__(name, alias)
