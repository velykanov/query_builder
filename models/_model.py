"""General model module"""
from ._constants import (
    CROSS_JOIN,
    FULL_JOIN,
    FULL_OUTER_JOIN,
    INNER_JOIN,
    JOIN,
    LEFT_JOIN,
    LEFT_OUTER_JOIN,
    RIGTH_JOIN,
    RIGHT_OUTER_JOIN
)

from .. import helpers
from ..expressions import Clause
from ..expressions import Expression
from ..fields import Field


# TODO: add schema support
class Model:  # pylint: disable=too-many-public-methods
    """
    Model class for representing DB table structure

    Args:
        name (str): Table name in DB (**required**)
        alias (str): Alias for this table (``None`` - default)
    """
    def __init__(self, name, alias=None):
        self._name = name
        self._alias = alias
        self._inner_state = {}

        self._set_name()

    def __repr__(self):
        return "<DB model '{}'>".format(type(self).__name__)

    def __str__(self):  # pylint: disable=too-many-branches
        query_parts = []

        if 'with' in self._inner_state:
            with_parts = []
            for alias, model in self._inner_state['with'].items():
                with_parts.append(
                    'WITH {alias} AS ({query})'.format(
                        alias=helpers.quote_literal(alias),
                        query=model,
                    )
                )

                model.set_alias(alias)
            query_parts.append(', '.join(with_parts))

        if 'delete' in self._inner_state:
            query_parts.append(
                'DELETE FROM {table}'.format(
                    table=self._get_name(),
                )
            )
        elif 'insert' in self._inner_state:
            select = self._inner_state.pop('select', None)

            if select is None:
                query_parts.append(
                    'INSERT INTO {table} ({fields}) VALUES {values}'.format(
                        table=self._get_name(),
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
                        table=self._get_name(),
                        fields=', '.join(map(str, self._inner_state['insert']['fields'])),
                        query=select,
                    )
                )
        elif 'update' in self._inner_state:
            query_parts.append(
                'UPDATE {table} SET {pairs}'.format(
                    table=self._get_name(),
                    pairs=', '.join(map(str, self._inner_state['update'])),
                )
            )
        elif 'select' in self._inner_state:
            distinct = self._inner_state.pop('distinct', None)

            select = 'SELECT'
            if distinct is not None:
                distinct_on = distinct.get('on')
                if distinct_on is not None:
                    select = 'SELECT DISTINCT ON ({})'.format(
                        ', '.join(map(str, distinct_on)),
                    )
                else:
                    select = 'SELECT DISTINCT'

            query_parts.append(
                '{select} {fields} FROM {table}'.format(
                    select=select,
                    fields=', '.join(map(str, self._inner_state['select'])),
                    table=self._get_name(),
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

        if 'group' in self._inner_state:
            query_parts.append(
                'GROUP BY {}'.format(
                    ', '.join(map(str, self._inner_state['group']))
                )
            )

        if 'having' in self._inner_state:
            query_parts.append(
                'HAVING {}'.format(
                    ', '.join(map(str, self._inner_state['having']))
                )
            )

        if 'order' in self._inner_state:
            query_parts.append(
                'ORDER BY {}'.format(
                    ', '.join(map(Model._apply_ordering, self._inner_state['order']))
                )
            )

        if 'limit' in self._inner_state:
            query_parts.append('LIMIT {}'.format(self._inner_state['limit']))

        if 'offset' in self._inner_state:
            query_parts.append('OFFSET {}'.format(self._inner_state['offset']))

        # clear inner state
        self._inner_state = {}

        return ' '.join(query_parts)

    @staticmethod
    def _apply_ordering(field):
        if isinstance(field, Field):
            field = field.as_alias()

        if field.startswith('-'):
            return '{} DESC'.format(field[1:])

        if field.startswith('+'):
            return '{} ASC'.format(field[1:])

        return '{} ASC'.format(field)

    def _get_name(self):
        if self._alias is None:
            return helpers.quote_literal(self._name)

        return '{table} AS {alias}'.format(
            table=helpers.quote_literal(self._name),
            alias=helpers.quote_literal(self._alias),
        )

    def _set_name(self):
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                name = self._alias or self._name
                getattr(self, attr).set_table_prefix(name)

    def select(self, *fields):
        """
        Puts fields to select into inner state
        Accepts either Expression or Field instances as fields (optional)
        In case of no fields puts asterisk

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        if not all(isinstance(field, (Expression, Field)) for field in fields):
            raise TypeError('fields must be either Expression or Field instances')

        if fields:
            self._inner_state['select'] = fields
        else:
            self._inner_state['select'] = ('*',)

        return self

    def insert(self, fields, values, operations=None):
        """
        Puts fields and values (with possible operations) to insert into inner
        state

        Args:
            fields (list): List of Field instances (**required**)
            values (list): List of values to insert (**required**)
            operations (list): List of respective operations to apply (``None`` - default)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        # TODO: implement values instance checking for operations applying
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError('fields must be list of Field instances')

        if isinstance(values, self.__class__):
            inner_state = self._inner_state
            inner_state['select'] = str(values)
            self._inner_state = inner_state
            self._inner_state['insert'] = {
                'fields': fields,
                'operations': operations,
            }

        else:
            self._inner_state['insert'] = {
                'fields': fields,
                'values': values,
                'operations': operations,
            }

        return self

    def update(self, field, *fields, from_model=None):
        """
        Puts fields to update into inner state

        Args:
            field (Field): Field with value to set (**required**)
            from_model (Model): Model for data retrieving (``None`` - default)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        update_fields = [field]
        update_fields.extend(list(fields))

        if not all(isinstance(field, Field) for field in update_fields):
            raise TypeError('fields must be Field instances')

        self._inner_state['update'] = {'fields': fields}
        if from_model is not None:
            self._inner_state['update']['from'] = from_model

        return self

    def delete(self):
        """
        Marks inner state as needed to delete

        Returns:
            Model: Same object with changed inner state
        """
        self._inner_state['delete'] = True

        return self

    def returning(self, *fields):
        """
        Puts fields to return after completion into inner state
        Accepts Field instances as fields (optional)
        In case of no fields puts asterisk

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        if not all(isinstance(field, Field) for field in fields):
            raise TypeError('fields must be Field instances')

        if fields:
            self._inner_state['returning'] = fields
        else:
            self._inner_state['returning'] = ('*',)

        return self

    def join(self, model, condition, join_type=JOIN):
        """
        Puts join condition into inner state

        Args:
            model (Model): Model to join on (**required**)
            condition (Expression|Field): Joining condition (**required**)
            join_type (str): Joining type (``'JOIN'`` - default)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid `condition` input
            ValueError: In case of invalid `join_type` input
        """
        if not isinstance(condition, (Expression, Field)):
            raise TypeError('condition must be either Expression or Field instance')

        possible_join_types = [
            CROSS_JOIN, FULL_JOIN, FULL_OUTER_JOIN, INNER_JOIN, JOIN, LEFT_JOIN,
            LEFT_OUTER_JOIN, RIGTH_JOIN, RIGHT_OUTER_JOIN,
        ]

        if join_type not in possible_join_types:
            raise ValueError(
                'join_type must be one of (%s)' % ', '.join(possible_join_types)
            )

        if 'join' not in self._inner_state:
            self._inner_state['join'] = []

        self._inner_state['join'].append(
            (join_type, getattr(model, '_get_name')(), condition),
        )

        return self

    def cross_join(self, model, condition):
        """
        Puts cross join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, CROSS_JOIN)

    def full_join(self, model, condition):
        """
        Puts full join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, FULL_JOIN)

    def full_outer_join(self, model, condition):
        """
        Puts full outer join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, FULL_OUTER_JOIN)

    def inner_join(self, model, condition):
        """
        Puts inner join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, INNER_JOIN)

    def left_join(self, model, condition):
        """
        Puts left join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, LEFT_JOIN)

    def left_outer_join(self, model, condition):
        """
        Puts left outer join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, LEFT_OUTER_JOIN)

    def right_join(self, model, condition):
        """
        Puts right join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, RIGTH_JOIN)

    def right_outer_join(self, model, condition):
        """
        Puts right outer join condition into inner state (look at :func:`~Model.join`)
        """
        return self.join(model, condition, RIGHT_OUTER_JOIN)

    def where(self, clause):
        """
        Puts where clause into inner state

        Args:
            clause (Clause|Expression): Logical clause (**required**)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        if not isinstance(clause, (Clause, Expression)):
            raise TypeError('clause must be either Clause or Expression instance')

        self._inner_state['where'] = clause

        return self

    # TODO: rethink WITH CTE implementation
    def with_cte(self, alias, model):
        """
        Puts model as CTE object into inner state

        Args:
            alias (str): Alias for WITH CTE (**required**)
            model (Model): CTE object (**required**)

        Returns:
            Model: Same object with changed inner state
        """
        if 'with' not in self._inner_state:
            self._inner_state['with'] = {}

        self._inner_state['with'][alias] = model

        return self

    def order(self, field, *fields):
        """
        Puts ordering fields into inner state
        For all of fields leading sign (if present) defines ordering type:
            `+` - ascending
            `-` - descending
        If no leading sign, ascending is used by default

        Args:
            field (str|Field): Field to order by (**required**)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        ordering_fields = [field]
        ordering_fields.extend(list(fields))

        if not all(isinstance(field, (str, Field)) for field in ordering_fields):
            raise TypeError('fields must be either str or Field instances')

        self._inner_state['order'] = ordering_fields

        return self

    def group(self, field, *fields):
        """
        Puts grouping fields into inner state

        Args:
            field (Expression|Field): Field to group by (**required**)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        grouping_fields = [field]
        grouping_fields.extend(list(fields))

        if not all(isinstance(field, (Expression, Field)) for field in grouping_fields):
            raise TypeError('fields must be either Expression or Field instances')

        self._inner_state['group'] = grouping_fields

        return self

    def having(self, field, *fields):
        """
        Puts grouping fields into inner state

        Args:
            field (Expression|Field): Field for having clause (**required**)

        Returns:
            Model: Same object with changed inner state

        Raises:
            TypeError: In case of invalid input
        """
        having_fields = [field]
        having_fields.extend(list(fields))

        if not all(isinstance(field, (Expression, Field)) for field in having_fields):
            raise TypeError('fields must be either Expression or Field instances')

        self._inner_state['having'] = having_fields

        return self

    def limit(self, limit):
        """
        Puts selecting limitation into inner state

        Args:
            limit (int): Limitation quantity (**required**)

        Returns:
            Model: Same object with changed inner state
        """
        self._inner_state['limit'] = limit

        return self

    def offset(self, offset):
        """
        Puts selecting offset into inner state

        Args:
            offset (int): Offset quantity (**required**)

        Returns:
            Model: Same object with changed inner state
        """
        self._inner_state['offset'] = offset

        return self

    def distinct(self, *fields):
        """
        Puts distinct part into inner state
        Could be applied ON some fields (optional, group by recommended)

        Returns:
            Model: Same object with changed inner state
        """
        self._inner_state['distinct'] = {
            'distinct': True,
        }

        if fields:
            self._inner_state['distinct'].update({'on': fields})

        return self

    def set_alias(self, alias):
        """
        Sets alias for table

        Args:
            alias (str): Alias for table (**required**)

        Returns:
            Model: Same object with changed inner state
        """
        self._alias = alias
        self._set_name()

        return self

    def reset_alias(self):
        """
        Undoes alias setting

        Returns:
            Model: Same object with changed inner state
        """
        self.set_alias(None)

        return self
