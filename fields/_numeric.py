"""Numeric fields module"""
from . import Field


class Decimal(Field):
    _type = 'decimal'
    _max_magnitude = 131072
    _max_scale = 16383

    def __init__(self, name, alias=None, precision=None, scale=None):
        if precision is not None and self._max_scale + self._max_magnitude < precision:
            raise ValueError('Precision is bigger than allowed')
        self.precision = precision
        if scale is not None and self._max_scale < scale:
            raise ValueError('Scale is bigger than allowed')
        self.scale = scale

        super(Decimal, self).__init__(name, alias)

    def __add__(self, other):
        return self._general_operation(other, '+')

    def __sub__(self, other):
        return self._general_operation(other, '-')

    def __truediv__(self, other):
        return self._general_operation(other, '/', True)

    def __mul__(self, other):
        return self._general_operation(other, '*', True)

    def max(self):
        self._fields[self.name] = 'max({})'.format(self)
    
        return self
    
    def min(self):
        self._fields[self.name] = 'max({})'.format(self)
    
        return self

    def avg(self):
        self._fields[self.name] = 'avg({})'.format(self)

        return self


class Double(Decimal):
    _type = 'double precision'
    _max_magnitude = 15
    _max_scale = 14


class BigInt(Decimal):
    _type = 'bigint'
    _min = -9223372036854775808
    _max = 9223372036854775807
    _max_magnitude = 19
    _max_scale = 0

    def __init__(self, name, alias=None):
        super(BigInt, self).__init__(name, alias)


class BigSerial(BigInt):
    _type = 'bigserial'
    _min = 1


class Integer(BigInt):
    _type = 'integer'
    _min = -2147483648
    _max = 2147483647
    _max_magnitude = 10


class Real(Double):
    _type = 'real'
    _max_magnitude = 6
    _max_scale = 5


class Serial(Integer):
    _type = 'serial'
    _min = 1


class SmallInt(Integer):
    _type = 'smallint'
    _min = -32768
    _max = 32767
    _max_magnitude = 5


class SmallSerial(SmallInt):
    _type = 'smallserial'
    _min = 1
