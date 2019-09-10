"""General model module"""
from .. import helpers
from ..expressions import Clause
from ..expressions import Expression
from ..fields import Field


class Model:
    _inner_state = {}
    def __init__(self, name):
        self._name = name

        self._set_name()

    def _set_name(self):
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                getattr(self, attr).set_table_prefix(self._name)

    def __repr__(self):
        return "<DB model '{}'>".format(type(self).__name__)

    def __str__(self):
        query_parts = []

        if 'with' in self._inner_state:
            query_parts.append(
                'WITH {alias} AS ({query})'.format(
                    alias=self._inner_state['with']['alias'],
                    query=self._inner_state['with']['query'],
                )
            )

        if 'delete' in self._inner_state:
            query_parts.append(
                'DELETE FROM {table}'.format(
                    table=helpers.quote_literal(self._name),
                )
            )

        if 'insert' in self._inner_state:
            select = self._inner_state.pop('select', None)

            if select is None:
                query_parts.append(
                    'INSERT INTO {table} ({fields}) VALUES {values}'.format(
                        table=helpers.quote_literal(self._name),
                        fields=', '.join(
                            str(field) for field in self._inner_state['insert']['fields']
                        ),
                        values=', '.join(
                            '({})'.format(
                                ', '.join(helpers.quote_ident(value) for value in values_row)
                            ) for values_row in self._inner_state['insert']['values']
                        ),
                    )
                )
            else:
                query_parts.append(
                    'INSERT INTO {table} ({fields}) {query}'.format(
                        table=helpers.quote_literal(self._name),
                        fields=self._inner_state['insert']['fields'],
                        query=select,
                    )
                )
        elif 'update' in self._inner_state:
            query_parts.append(
                'UPDATE {table} SET {pairs}'.format(
                    table=helpers.quote_literal(self._name),
                    pairs=', '.join(map(str, self._inner_state['update'])),
                )
            )
        elif 'select' in self._inner_state:
            query_parts.append(
                'SELECT {fields} FROM {table}'.format(
                    fields=', '.join(map(str, self._inner_state['select'])),
                    table=helpers.quote_literal(self._name),
                )
            )

        if 'join' in self._inner_state:
            query_parts.append(
                ' '.join(
                    '{} {} ON {}'.format(*join_condition)
                    for join_condition in self._inner_state['join']
                )
            )

        if 'where' in self._inner_state:
            query_parts.append(
                'WHERE {clause}'.format(clause=self._inner_state['where'])
            )

        # clear inner state
        self._inner_state = {}

        return ' '.join(query_parts)

    def select(self, *fields):
        if not all(isinstance(field, (Expression, Field)) for field in fields):
            raise TypeError('fields must be either Expression or Field')

        if fields:
            self._inner_state['select'] = fields
        else:
            self._inner_state['select'] = ('*',)

        return self

    def insert(self, fields, values, operations=None):
        # TODO: implement values instance checking for operations applying
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError('fields must be Field')

        self._inner_state['insert'] = {
            'fields': fields,
            'values': values,
            'operations': operations,
        }

        return self

    def update(self, *fields):
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError('fields must be Field')

        self._inner_state['update'] = fields

        return self

    def delete(self):
        self._inner_state['delete'] = True

        return self

    def returning(self, *fields):
        if not all(isinstance(field, (Expression, Field)) for field in fields):
            raise TypeError('fields must be either Expression or Field')

        if fields:
            self._inner_state['returning'] = fields

        return self

    def join(self, model, condition):
        if not isinstance(condition, (Expression, Field)):
            raise TypeError('condition must be either Expression or Field')

        if 'join' not in self._inner_state:
            self._inner_state['join'] = []

        self._inner_state['join'].append(
            ('JOIN', model._name, condition),
        )

        return self

    def where(self, clause):
        if not isinstance(clause, (Clause, Expression)):
            raise TypeError('clause must be Clause or Expression')

        self._inner_state['where'] = clause

        return self

    def with_cte(self, alias, model):
        if not isinstance(model, self):
            raise TypeError('model must be self')

        self._inner_state['with'] = {
            'alias': alias,
            'query': model,
        }

        return self

    def order(self, *fields):
        if not all(isinstance(field, (Expression, Field)) for field in fields):
            raise TypeError('fields must be either Expression or Field')

        # TODO: add fields negation
        self._inner_state['order'] = fields

        return self

    def group(self, *fields):
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError('fields must be Field')

        self._inner_state['group'] = fields

        return self

    def having(self, *fields):
        if not all(isinstance(field, (Expression, Field)) for field in fields):
            raise TypeError('fields must be either Expression or Field')

        self._inner_state['having'] = fields

        return self

    def limit(self, limit):
        self._inner_state['limit'] = limit

        return self

    def offset(self, offset):
        self._inner_state['offset'] = offset

        return self
