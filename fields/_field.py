"""Field class module"""
import decimal
import json


class Field:
    _unsupported_operand = "unsupported operand type(s) for {}: '{}' and '{}'"
    _unsupported_unary_operand = "bad operand type for unary {}: '{}'"

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

    def __truediv__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '/',
            type(self).__name__,
            type(other).__name__,
        ))

    def __mul__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '*',
            type(self).__name__,
            type(other).__name__,
        ))

    def __rmul__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '*',
            type(self).__name__,
            type(other).__name__,
        ))

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

    def _general_operation(self, other, operand, need_parenthesis=False):
        current_value = self._fields[self.name]
        if need_parenthesis:
            current_value = '({})'.format(current_value)

        if isinstance(other, Field):
            name = '_'.join((self.name, other.name))
            value = other._fields[other.name]
        elif isinstance(other, (int, float, bool, decimal.Decimal)):
            name = self.name
            value = other
        elif isinstance(other, (list, tuple, set, dict)):
            name = self.name
            value = json.dumps(other)
        elif isinstance(other, (str, dt.datetime, dt.date, dt.time)):
            name = self.name
            value = str(other)
        else:
            # TODO: create mapping to raise correct type error
            super(type(self), self).__add__(other)

        instance = self.__class__(name)
        instance._fields = {name: ' '.join((current_value, operand, value))}

        return instance

    def set_alias(self, alias):
        self.alias = alias
