"""General model module"""
from expressions import Clause
from expressions import Expression
from fields import Field


# TODO: implement join
# TODO: implement aliasing
# TODO: implement table prefixing
class Model:
    _inner_state = {}
    def __init__(self, name):
        self._name = name

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
            query_parts.append('DELETE FROM {table}'.format(table=self._name))

        if 'insert' in self._inner_state:
            select = self._inner_state.pop('select', None)

            if select is None:
                query_parts.append(
                    'INSERT INTO {table} ({fields}) VALUES {}'.format(
                        table=self._name,
                        fields=self._inner_state['insert']['fields'],
                        values=', '.join(
                            '({})'.format(
                                ', '.join(value for value in values_row)
                            ) for values_row in self._inner_state['insert']['values']
                        ),
                    )
                )
            else:
                query_parts.append(
                    'INSERT INTO {table} ({fields}) {query}'.format(
                        table=self._name,
                        fields=self._inner_state['insert']['fields'],
                        query=select,
                    )
                )
        elif 'update' in self._inner_state:
            query_parts.append(
                'UPDATE {table} SET {pairs}'.format(
                    table=self._name,
                    pairs=', '.join(map(str, self._inner_state['update'])),
                )
            )
        elif 'select' in self._inner_state:
            query_parts.append(
                'SELECT {fields} FROM {table}'.format(
                    fields=', '.join(map(str, self._inner_state['select'])),
                    table=self._name,
                )
            )

        if 'where' in self._inner_state:
            query_parts.append(
                'WHERE {clause}'.format(clause=self._inner_state['where'])
            )

        return ' '.join(query_parts)

    def select(self, *fields):
        assert all(isinstance(field, (Expression, Field)) for field in fields)

        self._inner_state['select'] = fields

        return self

    def insert(self, fields, values, operations=None):
        # TODO: implement values instance checking for operations applying
        assert all(isinstance(field, Field) for field in fields)

        self._inner_state['insert'] = {
            'fields': fields,
            'values': values,
            'operations': operations,
        }

        return self

    def update(self, *fields):
        assert all(isinstance(field, Field) for field in fields)

        self._inner_state['update'] = fields

        return self

    def delete(self):
        self._inner_state['delete'] = True

        return self

    def returning(self, *fields):
        assert all(isinstance(field, (Expression, Field)) for field in fields)

        if fields:
            self._inner_state['returning'] = fields

        return self

    def join(self):
        pass

    def where(self, clause):
        assert isinstance(clause, Clause)

        self._inner_state['where'] = clause

        return self

    def with_cte(self, alias, model):
        assert isinstance(model, self)

        self._inner_state['with'] = {
            'alias': alias,
            'query': model,
        }

        return self
