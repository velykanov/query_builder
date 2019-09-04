"""Model test module"""
import unittest

from query_builder import fields
from query_builder.models import Model


class User(Model):
    name = fields.Char('name', max_length=32)
    age = fields.Integer('age')


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User('users')

    def test_select(self):
        """Tests simple select cases"""
        query = str(self.user.select())
        expected = 'SELECT * FROM users'

        self.assertEquals(query, expected)

        query = str(self.user.select(self.user.name, self.user.age))
        expected = 'SELECT "users"."name", "users"."age" FROM users'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name + ' hello WORLD!',
            self.user.age - 7,
        ))
        expected = 'SELECT "users"."name" || \' hello WORLD!\', "users"."age" - 7 FROM users'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            (self.user.name + ' hello WORLD!').set_alias('new_name'),
            (self.user.age - 7).set_alias('new_age'),
        ))
        expected = 'SELECT "users"."name" || \' hello WORLD!\' AS "new_name", "users"."age" - 7 AS "new_age" FROM users'

        self.assertEquals(query, expected)

    # def test_select_where(self):
