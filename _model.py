"""General model module"""
from expressions import Clause
from expressions import Expression
from fields import Field

class Model:
    _inner_state = {}
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<DB model '{}'>".format(type(self).__name__)

    def __str__(self):
        # TODO: implement query building
        return ''

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

    def where(self, clause):
        assert isinstance(clause, Clause)

        self._inner_state['where'] = clause

        return self

    def with(self, alias, model):
        assert isinstance(model, self)

        self._inner_state['with'] = {
            'alias': alias,
            'query': str(model),
        }
        
        return self
