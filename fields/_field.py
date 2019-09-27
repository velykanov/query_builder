"""Field class module"""
import copy
import datetime
import decimal
import inspect
import json

from .. import helpers


# TODO: fix interaction with operations and functions
# TODO: add schema support
class Field:
    """
    General field class. Exists as an abstract

    Args:
        name (str): Column name in DB (**required**)
        alias (str): Alias for column (``None`` - default)
        table (str): Table name for prefixing (``None`` - default)

    Raises:
        TypeError: in case operation is not allowed
        ValueError: in case of not conforming to constraints
    """
    _unsupported_operand = "unsupported operand type(s) for {}: '{}' and '{}'"
    _unsupported_unary_operand = "bad operand type for unary {}: '{}'"

    _has_constraints = False
    _functions = None
    _operations = None

    def __init__(self, name, alias=None, table=None, **kwargs):
        self.name = name
        self._alias = alias
        self._table = table

        self.kwargs = kwargs

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
        return self.__mul__(other)

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
        return self._general_operation(other, '<')

    def __le__(self, other):
        return self._general_operation(other, '<=')

    def __gt__(self, other):
        return self._general_operation(other, '>')

    def __ge__(self, other):
        return self._general_operation(other, '>=')

    def __ne__(self, other):
        raise TypeError(self._unsupported_operand.format(
            '!=',
            type(self).__name__,
            type(other).__name__,
        ))

    def __eq__(self, other):
        self._check_constraints(other)

        return self._general_operation(other, '=')

    def __hash__(self):
        return hash((self.name, self._alias, self._table))

    def __neg__(self):
        return '-{}'.format(self)

    def __pos__(self):
        return '+{}'.format(self)

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

        result = operand.join((value, other_value))

        if self._functions:
            result = self._unwrap_functions(self._functions)

        if self._alias is None:
            return result

        return '{} AS {}'.format(result, self._alias)

    def _format_field(self, value=None):
        if value is None:
            value = self

        name = helpers.quote_literal(value.name)
        if getattr(value, '_table', None) is not None:
            name = '{}.{}'.format(
                helpers.quote_literal(getattr(value, '_table')),
                name,
            )

        if getattr(value, '_functions', None) is not None:
            name = getattr(
                value,
                '_unwrap_functions',
                self._unwrap_functions,
            )(getattr(value, '_functions'))

        if getattr(value, '_alias', None) is not None:
            return '{} AS {}'.format(
                name,
                getattr(value, '_alias'),
            )

        return name

    def __str__(self):
        if self._operations is None:
            return self._format_field()

        return self.__operation_actions(self._operations)

    def _check_constraints(self, _):
        if self._has_constraints:
            raise NotImplementedError('implement in child class')

    def _general_operation(
            self, other, operand, need_parenthesis=False, inverse=False,
    ):
        name = None
        other_value = None
        value = str(self)
        if self._operations is not None:
            value = self._operations

        if isinstance(other, Field):
            name = '_'.join((self.name, other.name))
            other_value = other
            if getattr(other, '_operations') is not None:
                other_value = getattr(other, '_operations')
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
            getattr(Field(...), func_name)(other)

        instance = self.__class__(name, **self.kwargs)
        # TODO: test this behavior out (not sure if it's correct)
        # instance._functions = self._functions
        setattr(
            instance,
            '_operations',
            [
                operand,
                need_parenthesis,
                *[value, other_value][::-1 if inverse else 1],
            ],
        )

        return instance

    def _wrap_function(self, func_name, *args, inverse=False):
        instance = self.__class__(self.name, self._alias, self._table, **self.kwargs)
        setattr(instance, '_operations', self._operations)
        self._alias = None

        functions = copy.deepcopy(self._functions) or self
        setattr(
            instance,
            '_functions',
            {func_name: (*args, functions) if inverse else (functions, *args)}
        )

        return instance

    def _unwrap_functions(self, functions):
        func_name = list(functions.keys())[0]
        new_args = []

        for arg in functions[func_name]:
            if isinstance(arg, dict):
                arg = self._unwrap_functions(arg)
            new_args.append(arg)

        return '{}({})'.format(
            func_name,
            ', '.join(['{}'] * len(new_args)).format(*new_args),
        )

    def set_alias(self, alias):
        """
        Sets alias on field

        Args:
            alias (str): Alias name (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        self._alias = helpers.quote_literal(alias)

        return self

    def set_table_prefix(self, table):
        """
        Sets table extension

        Args:
            table (str): Table name (**required**)

        Returns:
            Field: Same object with changed inner state
        """
        self._table = table

        return self

    def cast(self, as_type):
        """
        Casts field as specified type

        Args:
            as_type (str): Type to cast field as (**required**)

        Returns:
            Field: Object with changed inner state
        """
        operation = 'cast({} as {})'.format(self, as_type)

        if self._operations is None:
            return self.__class__(operation, self._alias, self._table, **self.kwargs)

        # TODO: the worst implementation ever
        self._operations[2] = operation

        return self

    def count(self):
        """
        Wraps field into count(field)

        Returns:
            Field: Object with changed inner state
        """
        return self._wrap_function('count')

    def array_agg(self):
        """
        Wraps field in array_agg(field)

        Returns:
            Field: Object with changed inner state
        """
        return self._wrap_function('array_agg')

    def as_alias(self):
        """
        Gets field name or field's alias

        Returns:
            str: Field's alias or name
        """
        if self._alias:
            return self._alias

        return str(self)
