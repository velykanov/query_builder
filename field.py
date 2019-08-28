import decimal


class Field:
    _unsupported_operand = "unsupported operand type(s) for {}: '{}' and '{}'"
    _unsupported_unary_operand = "unsupported operand type(s) for {} on type {}"

    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias
        self._fields = {name: name}

    def __add__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '+',
            type(self).__name__,
            type(other).__name__,
        ))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '-',
            type(self).__name__,
            type(other).__name__,
        ))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __and__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '&',
            type(self).__name__,
            type(other).__name__,
        ))

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '|',
            type(self).__name__,
            type(other).__name__,
        ))

    def __ror__(self, other):
        return self.__or__(other)

    def __lt__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '<',
            type(self).__name__,
            type(other).__name__,
        ))

    def __le__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '<=',
            type(self).__name__,
            type(other).__name__,
        ))

    def __gt__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '>',
            type(self).__name__,
            type(other).__name__,
        ))

    def __ge__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '>=',
            type(self).__name__,
            type(other).__name__,
        ))

    def __ne__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '!=',
            type(self).__name__,
            type(other).__name__,
        ))

    def __eq__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '==',
            type(self).__name__,
            type(other).__name__,
        ))

    def __neg__(self):
        raise TypeError(self._unsupported_unary_operand.format(
            '-',
            type(self).__name__,
        ))

    def __bool__(self):
        raise TypeError(self._unsupported_unary_operand.format(
            'bool',
            type(self).__name__,
        ))

    def __repr__(self):
        return "<{} '{}'>".format(type(self).__name__, self.name)

    def set_alias(self, alias):
        self.alias = alias


class BigInt(Field):
    _type = 'bigint'
    _min = -9223372036854775808
    _max = 9223372036854775807

    def __general_operation(self, other, operand):
        if isinstance(other, Field):
            name = '{}_{}'.format(self.name, other.name)
            value = '{} {} {}'.format(self._fields[self.name], operand, other.name)
        elif isinstance(other, (int, float, decimal.Decimal)):
            name = self.name
            value = '{} {} {}'.format(self._fields[self.name], operand, other)
        else:
            super(BigInt, self).__add__(other)
        
        instance = self.__class__(name)
        instance._fields = {name: value}
        
        return instance

    def __add__(self, other):
        self.__general_operation(other, '+')


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
