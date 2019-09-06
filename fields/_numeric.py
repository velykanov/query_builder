"""Numeric fields module"""
from ._field import Field


class Decimal(Field):
    _type = 'decimal'
    _max_magnitude = 131072
    _max_scale = 16383

    def __init__(self, name, alias=None, table=None, quote=True, precision=None, scale=None):
        if precision is not None and self._max_scale + self._max_magnitude < precision:
            raise ValueError('Precision is bigger than allowed')
        self.precision = precision
        if scale is not None and self._max_scale < scale:
            raise ValueError('Scale is bigger than allowed')
        self.scale = scale

        super(Decimal, self).__init__(
            name,
            alias,
            table,
            quote,
            precision=precision,
            scale=scale,
        )

    def __add__(self, value):
        return self._general_operation(value, '+')

    def __sub__(self, value):
        return self._general_operation(value, '-')

    def __rsub__(self, value):
        return self._general_operation(value, '-', inverse=True)

    def __truediv__(self, value):
        return self._general_operation(value, '/', True)

    def __rtruediv__(self, value):
        return self._general_operation(value, '/', True, True)

    def __mul__(self, value):
        return self._general_operation(value, '*', True)

    def __mod__(self, value):
        return self._general_operation(value, '%', True)

    def __rmod__(self, value):
        return self._general_operation(value, '%', True, True)

    def __floordiv__(self, value):
        return self.div(value)

    def __pow__(self, value):
        return self._general_operation(value, '^', True)

    def __rpow__(self, value):
        return self._general_operation(value, '^', True, True)

    def __ge__(self, value):
        return self._general_operation(value, '>=')

    def __gt__(self, value):
        return self._general_operation(value, '>')

    def __le__(self, value):
        return self._general_operation(value, '<=')

    def __lt__(self, value):
        return self._general_operation(value, '<')

    def __round__(self, places=0):
        return self.round(places)

    def __abs__(self):
        return self._wrap_function('abs')

    def max(self):
        return self._wrap_function('max')

    def min(self):
        return self._wrap_function('min')

    def avg(self):
        return self._wrap_function('avg')

    def ceil(self):
        return self._wrap_function('ceil')

    def degrees(self):
        return self._wrap_function('degrees')

    def exp(self):
        return self._wrap_function('exp')

    def floor(self):
        return self._wrap_function('floor')

    def ln(self):
        return self._wrap_function('ln')

    def radians(self):
        return self._wrap_function('radians')

    def sign(self):
        return self._wrap_function('sign')

    def sqrt(self):
        return self._wrap_function('sqrt')

    def cbrt(self):
        return self._wrap_function('cbrt')

    def sin(self):
        return self._wrap_function('sin')

    def cos(self):
        return self._wrap_function('cos')

    def asin(self):
        return self._wrap_function('asin')

    def acos(self):
        return self._wrap_function('acos')

    def tan(self):
        return self._wrap_function('tan')

    def cot(self):
        return self._wrap_function('cot')

    def atan(self):
        return self._wrap_function('atan')

    def atan2(self, value):
        return self._wrap_function('atan2', value)

    def width_bucket(self, left_bound, right_bound, count):
        return self._wrap_function('width_bucket', left_bound, right_bound, count)

    def mod(self, value):
        return self._wrap_function('mod', value)

    def div(self, value):
        return self._wrap_function('div', value)

    def power(self, value):
        return self._wrap_function('power', value)

    def round(self, places=0):
        return self._wrap_function('round', places)

    def trunc(self, places=0):
        return self._wrap_function('trunc', places)

    def log(self, base=10):
        return self._wrap_function('log', base, inverse=True)


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

    def __init__(self, name, alias=None, table=None, quote=True, **kwargs):
        super(BigInt, self).__init__(name, alias, table, quote)

    def __lshift__(self, value):
        return self._general_operation(value, '<<', True)

    def __rlshift__(self, value):
        return self._general_operation(value, '<<', True, True)

    def __rshift__(self, value):
        return self._general_operation(value, '>>', True)

    def __rrshift__(self, value):
        return self._general_operation(value, '>>', True, True)


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
