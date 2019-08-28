class Field:
    _not_implemented_method = NotImplementedError('implement method in child')

    def __add__(self, other):
        raise self._not_implemented_method

    def __sub__(self, other):
        raise self._not_implemented_method

    def __and__(self, other):
        raise self._not_implemented_method

    def __or__(self, other):
        raise self._not_implemented_method

    def __lt__(self, other):
        raise self._not_implemented_method

    def __lte__(self, other):
        raise self._not_implemented_method


class BigInt(Field):
    _type = 'bigint'
    _min = -9223372036854775808
    _max = 9223372036854775807

    def __add__(self, other):
        if isinstance(other, Field) and issubclass(other.__class__(), BigInt):


class Integer(BigInt):
    _type = 'integer'
    _min = -2147483648
    _max = 2147483647


class SmallInt(Integer):
    _type = 'smallint'
    _min = -32768
    _max = 32767


class SmallSerial(SmallInt):
    _type = 'smallserial'
    _min = 1
