from .. import helpers
from ..fields import Field
from ..states import (
    GroupBy, Select, Initial, Limit, Offset, OrderBy, Where, state_aware,
)


class Model:
    def __init__(self, name, alias=None, schema=None):
        self._name = name
        self._alias = alias
        self._schema = schema

        self._state = Initial()
        self._storage = []

        self._set_name()

    def _set_name(self):
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                name = self._alias or self._name
                getattr(self, attr).set_table_prefix(name, self._schema)

    def __str__(self):
        result = ' '.join(self._storage)

        self.reset()

        return result

    def reset(self):
        self._state = Initial()
        self._storage.clear()

    def evaluate(self):
        return self.__str__()

    @state_aware(Select)
    def select(self, *fields):
        if fields:
            fields = list(map(self._set_field_alias, fields))
        else:
            fields = [self._set_field_alias('*')]

        self._storage.append(
            'SELECT {fields} FROM {table}'.format(
                fields=', '.join(map(str, fields)),
                table=self._table_name,
            )
        )

        return self

    @state_aware(Where)
    def where(self, clause):
        self._storage.append('WHERE {clause}'.format(clause=clause))

        return self

    @state_aware(GroupBy)
    def group_by(self, field, *fields):
        grouping_fields = [field]
        grouping_fields.extend(list(fields))

        self._storage.append('GROUP BY {fields}'.format(
            fields=', '.join(map(str, grouping_fields)),
        ))

        return self

    @state_aware(OrderBy)
    def order_by(self, field, *fields):
        ordering_fields = [field]
        ordering_fields.extend(list(fields))

        self._storage.append('ORDER BY {fields}'.format(
            fields=', '.join(map(str, ordering_fields)),
        ))

        return self

    @state_aware(Limit)
    def limit(self, limit):
        self._storage.append('LIMIT {limit}'.format(limit=limit))

        return self

    @state_aware(Offset)
    def offset(self, offset):
        self._storage.append('OFFSET {offset}'.format(offset=offset))

        return self

    def _set_field_alias(self, field):
        if isinstance(field, Field):
            field.set_table_prefix(self._name, self._schema)
        else:
            field = '{}.{}'.format(self._table_name, str(field))

        return field

    @property
    def _table_name(self):
        return helpers.quote_literal(
            '.'.join(filter(None, [self._schema, self._name]))
        )
