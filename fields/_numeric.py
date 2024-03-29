"""Numeric fields module"""
import decimal

from ._field import Field


class Decimal(Field):
    """
    Decimal field type

    Args:
        name (str): Field name (**required**)
        alias (str): Field's alias (``None`` - default)
        table (str): Table name of the field (``None`` - default)
        precision (int): Field's precision (``None`` - default)
        scale (int): Field's scale (``None`` - default)

    Raises:
        ValueError: When precision or/and scale is/are bigger than allowed
    """
    _type = 'decimal'
    _max_magnitude = 131072
    _max_scale = 16383

    def __init__(self, name, alias=None, table=None, precision=None, scale=None):
        self._max = float('{}.{}'.format(
            '9' * self._max_magnitude,
            '9' * self._max_scale,
        )) if getattr(self, '_max', None) is None else self._max
        self._min = -self._max if getattr(self, '_min', None) is None else self._min

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

    def _check_constraints(self, value):
        if isinstance(value, Field):
            return True

        if isinstance(value, (float, decimal.Decimal)):
            if not self._min <= value <= self._max:
                raise ValueError('value does not conform constraints')
            value = str(value)

        magnitude, *scale = map(len, value.split('.', 1))
        if scale:
            scale = scale[0]
        else:
            scale = 0

        if magnitude > self._max_magnitude or scale > self._max_scale:
            raise ValueError('value does not conform constraints')

        return True

    def max(self):
        """
        Wraps field into max(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('max')

    def min(self):
        """
        Wraps field into min(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('min')

    def avg(self):
        """
        Wraps field into avg(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('avg')

    def ceil(self):
        """
        Wraps field into ceil(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('ceil')

    def degrees(self):
        """
        Wraps field into degrees(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('degrees')

    def exp(self):
        """
        Wraps field into exp(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('exp')

    def floor(self):
        """
        Wraps field into floor(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('floor')

    def ln(self):
        """
        Wraps field into ln(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('ln')

    def radians(self):
        """
        Wraps field into radians(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('radians')

    def sign(self):
        """
        Wraps field into sign(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('sign')

    def sqrt(self):
        """
        Wraps field into sqrt(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('sqrt')

    def cbrt(self):
        """
        Wraps field into qbrt(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('cbrt')

    def sin(self):
        """
        Wraps field into sin(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('sin')

    def cos(self):
        """
        Wraps field into cos(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('cos')

    def asin(self):
        """
        Wraps field into asin(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('asin')

    def acos(self):
        """
        Wraps field into acos(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('acos')

    def tan(self):
        """
        Wraps field into tan(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('tan')

    def cot(self):
        """
        Wraps field into cot(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('cot')

    def atan(self):
        """
        Wraps field into atan(field)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('atan')

    def atan2(self, value):
        """
        Wraps field into atan2(field, value)

        Args:
            value (object): atan2 function argument (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('atan2', value)

    def width_bucket(self, left_bound, right_bound, count):
        """
        Wraps field into width_bucket(field, left_bound, right_bound, count)

        Args:
            left_bound (object): width_bucket function argument (**required**)
            right_bound (object): width_bucket function argument (**required**)
            count (object): width_bucket function argument (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('width_bucket', left_bound, right_bound, count)

    def mod(self, value):
        """
        Wraps field into mod(field, value)

        Args:
            value (object): mod function argument (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('mod', value)

    def div(self, value):
        """
        Wraps field into div(field, value)

        Args:
            value (object): div function argument (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('div', value)

    def power(self, value):
        """
        Wraps field into power(field, value)

        Args:
            value (object): power function argument (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('power', value)

    def round(self, places=0):
        """
        Wraps field into round(field, places)

        Args:
            places (object): round function argument (``0`` - default)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('round', places)

    def trunc(self, places=0):
        """
        Wraps field into trunc(field, places)

        Args:
            places (object): trunc function argument (``0`` - default)

        Returns:
            Field: Same object with changed inner state
        """
        return self._wrap_function('trunc', places)

    def log(self, base=10):
        """
        Wraps field into log(base, field)

        Args:
            base (object): log function argument (``10`` - default)

        Returns:
            Field: Same object with changed inner state
        """
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

    def __init__(self, name, alias=None, table=None, **kwargs):
        super(BigInt, self).__init__(name, alias, table, **kwargs)

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
