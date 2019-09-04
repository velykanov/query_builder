"""Field class module"""
import datetime
import decimal
import inspect
import json

import helpers


class Field:
    """
    General field class. Exists as an abstract

    Args:
        name (str): Column name in DB (**required**)
        alias (str): Alias for column (``None`` - default)
        table (str): Table name for prefixing (``None`` - default)
    """
    _unsupported_operand = "unsupported operand type(s) for {}: '{}' and '{}'"
    _unsupported_unary_operand = "bad operand type for unary {}: '{}'"

    _operations = None

    def __init__(self, name, alias=None, table=None):
        self.name = helpers.quote_literal(name)
        self._alias = helpers.quote_literal(alias)
        self._table = helpers.quote_literal(table)

    def __add__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '+',
            type(self).__name__,
            type(other).__name__,
        ))

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '-',
            type(self).__name__,
            type(other).__name__,
        ))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
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
        return self._general_operation(other, '=')

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

    def __operation_actions(self, operations):
        operand, need_parenthesis, value, other_value = operations
        operand = ' {} '.format(operand)

        if isinstance(value, list):
            value = self.__operation_actions(value)
            if need_parenthesis:
                value = '({})'.format(value)
        elif isinstance(value, Field):
            value = self._format_field(value)

        if isinstance(other_value, list):
            other_value = self.__operation_actions(other_value)
            if need_parenthesis:
                other_value = '({})'.format(other_value)
        elif isinstance(other_value, Field):
            other_value = self._format_field(other_value)

        return operand.join((value, other_value))

    def _format_field(self, value=None):
        if value is None:
            value = self

        if value._table is not None:
            value.name = '{}.{}'.format(value._table, value.name)

        if value._alias is not None:
            return '{} as {}'.format(value.name, value._alias)

        return value.name

    def __str__(self):
        if self._operations is None:
            return self._format_field()

        return self.__operation_actions(self._operations)

    def _general_operation(self, other, operand, need_parenthesis=False):
        name = None
        other_value = None
        value = self._format_field()
        if self._operations is not None:
            value = self._operations

        if isinstance(other, Field):
            name = '_'.join((self.name, other.name))
            other_value = other._format_field()
            if other._operations is not None:
                other_value = other._operations
        elif isinstance(other, (list, tuple, set, dict, bool)):
            name = self.name
            other_value = helpers.quote_ident(json.dumps(other))
        elif isinstance(other, (int, float, decimal.Decimal)):
            name = self.name
            other_value = str(other)
        elif isinstance(other, (str, datetime.datetime, datetime.date, datetime.time)):
            name = self.name
            other_value = helpers.quote_ident(other)
        else:
            func_name = str(inspect.stack()[1].function)
            getattr(Field(None), func_name)(other)

        instance = self.__class__(name)
        instance._operations = [operand, need_parenthesis, value, other_value]

        return instance

    def set_alias(self, alias):
        self._alias = helpers.quote_literal(alias)

        return self

    def set_table_prefix(self, table):
        self._table = helpers.quote_literal(table)

    def cast(self, as_type):
        operation = 'cast({} as {})'.format(self, as_type)

        if self._operations is None:
            return self.__class__(operation, self._alias, self._table)

        # TODO: the worst implementation ever
        self._operations[2] = operation

        return self
