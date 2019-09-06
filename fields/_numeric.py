"""Numeric fields module"""
from ._field import Field


class Decimal(Field):
    _type = 'decimal'
    _max_magnitude = 131072
    _max_scale = 16383

    def __init__(self, name, alias=None, table=None, precision=None, scale=None):
        if precision is not None and self._max_scale + self._max_magnitude < precision:
            raise ValueError('Precision is bigger than allowed')
        self.precision = precision
        if scale is not None and self._max_scale < scale:
            raise ValueError('Scale is bigger than allowed')
        self.scale = scale

        super(Decimal, self).__init__(name, alias, table)

    def _wrap_math_operation(self, operation, *args):
        positions = ', '.join(['{}'] * (len(args) + 1))
        operation = '{}({})'.format(
            operation,
            positions.format(self, *args),
        )

        if self._operations is None:
            return self.__class__(operation, self._alias, self._table)

        # TODO: check correctness of the execution
        self._operations[2] = operation

        return self

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

    def __floordiv__(self, value):
        return self.div(value)

    def __pow__(self, value):
        return self._general_operation(value, '^', True)

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
        return self._wrap_math_operation('abs')

    def max(self):
        return self._wrap_math_operation('max')

    def min(self):
        return self._wrap_math_operation('min')

    def avg(self):
        return self._wrap_math_operation('avg')

    def ceil(self):
        return self._wrap_math_operation('ceil')

    def degrees(self):
        return self._wrap_math_operation('degrees')

    def exp(self):
        return self._wrap_math_operation('exp')

    def floor(self):
        return self._wrap_math_operation('floor')

    def ln(self):
        return self._wrap_math_operation('ln')

    def radians(self):
        return self._wrap_math_operation('radians')

    def sign(self):
        return self._wrap_math_operation('sign')

    def sqrt(self):
        return self._wrap_math_operation('sqrt')

    def cbrt(self):
        return self._wrap_math_operation('cbrt')

    def sin(self):
        return self._wrap_math_operation('sin')

    def cos(self):
        return self._wrap_math_operation('cos')

    def asin(self):
        return self._wrap_math_operation('asin')

    def acos(self):
        return self._wrap_math_operation('acos')

    def tan(self):
        return self._wrap_math_operation('tan')

    def cot(self):
        return self._wrap_math_operation('cot')

    def atan(self):
        return self._wrap_math_operation('atan')

    def atan2(self, value):
        return self._wrap_math_operation('atan2', value)

    def width_bucket(self, left_bound, right_bound, count):
        return self._wrap_math_operation(
            'width_bucket',
            left_bound,
            right_bound,
            count,
        )

    def mod(self, value):
        return self._wrap_math_operation('mod', value)

    def div(self, value):
        return self._wrap_math_operation('div', value)

    def power(self, value):
        return self._wrap_math_operation('power', value)

    def round(self, places=0):
        return self._wrap_math_operation('round', places)

    def trunc(self, places=0):
        return self._wrap_math_operation('trunc', places)

    def log(self, base=10):
        operation = 'log({base}, {value})'.format(
            base=base,
            value=self,
        )

        if self._operations is None:
            return self.__class__(operation, self._alias, self._table)

        self._operations[2] = operation

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

    def __init__(self, name, alias=None, table=None):
        super(BigInt, self).__init__(name, alias, table)

    def __lshift__(self, value):
        return self._general_operation(value, '<<', True)

    def __rlshift__(self, value):
        return self._general_operation(value, '<<', True, True)

    def __rshift__(self, value):
        return self._general_operation(value, '>>', True)

    def __rrshift__(self, value):
        return self._general_operation


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
