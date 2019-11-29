import pytest

from .. import fields
# from ..expressions import Clause
# from ..expressions import Expression
from ..models import Model


@pytest.fixture()
def user_model():
    class User(Model):
        id_ = fields.Integer('id')
        name = fields.Char('name', max_length=32)
        surname = fields.Char('surname', max_length=32)
        age = fields.Integer('age')

    return User('users')


def test_simple_select(user_model):
    assert user_model.select().evaluate() == 'SELECT "users".* FROM "users"'
    assert user_model.select(
        user_model.name,
    ).evaluate() == 'SELECT "users"."name" FROM "users"'
    assert user_model.select(
        user_model.surname,
        user_model.name,
    ).evaluate() == 'SELECT "users"."surname", "users"."name" FROM "users"'

    assert user_model.select(
        user_model.name + ' <- NAME',
        17 - user_model.age + 15,
    ).evaluate() == 'SELECT "users"."name" || \' <- NAME\', ' + \
        '17 - "users"."age" + 15 FROM "users"'

    # assert user_model.select(
    #     (user_model.name + ' <- NAME').set_alias('new_name'),
    #     (17 - user_model.age + 15).set_alias('new_age'),
    # ).evaluate() == 'SELECT "users"."name" || \' <- NAME\' AS "new_name", ' + \
    #     '17 - "users"."age" + 15 AS "new_age" FROM "users"'
