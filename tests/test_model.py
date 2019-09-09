"""Model test module"""
import unittest

from query_builder import fields
from query_builder.expressions import Clause
from query_builder.expressions import Expression
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
        expected = 'SELECT * FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(self.user.name, self.user.age))
        expected = 'SELECT "users"."name", "users"."age" FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name + ' hello WORLD!',
            self.user.age - 7,
        ))
        expected = 'SELECT ' + \
            '"users"."name" || \' hello WORLD!\', "users"."age" - 7 FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            (self.user.name + ' hello WORLD!').set_alias('new_name'),
            (self.user.age - 7).set_alias('new_age'),
        ))
        expected = 'SELECT ' + \
            '"users"."name" || \' hello WORLD!\' AS "new_name", ' + \
            '"users"."age" - 7 AS "new_age" FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            ('hello WORLD! ' + self.user.name).set_alias('new_name'),
            (7 - self.user.age).set_alias('new_age'),
        ))
        expected = 'SELECT ' + \
            '\'hello WORLD! \' || "users"."name" AS "new_name", ' + \
            '7 - "users"."age" AS "new_age" FROM "users"'

        self.assertEquals(query, expected)

    def test_select_functions(self):
        """Tests selections with functions applied to fields"""
        query = str(self.user.select(self.user.name.upper()))
        expected = 'SELECT upper("users"."name") FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name.upper().set_alias('upper_name'),
        ))
        expected = 'SELECT upper("users"."name") AS "upper_name" FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            ('prefix_' + self.user.name).upper().set_alias('upper_name'),
        ))
        expected = 'SELECT ' + \
            'upper(\'prefix_\' || "users"."name") AS "upper_name" FROM "users"'

        self.assertEquals(query, expected)

    def test_select_raw_sql(self):
        """Tests raw SQL expressions"""
        query = str(Expression("SELECT * FROM users"))
        expected = "SELECT * FROM users"

        self.assertEquals(query, expected)

    def test_select_where(self):
        """Tests selects with WHERE clauses"""
        query = str(self.user.select().where(
            Clause(self.user.name == "O'Reilly")
        ))
        expected = 'SELECT * FROM "users" WHERE "users"."name" = \'O\'\'Reilly\''

        self.assertEquals(query, expected)

        query = str(self.user.select().where(
            Clause(self.user.name == "O'Reilly") | Clause(self.user.age >= 18)
        ))
        expected = 'SELECT * FROM "users" ' + \
            'WHERE ("users"."name" = \'O\'\'Reilly\' OR "users"."age" >= 18)'

        self.assertEquals(query, expected)

        query = str(self.user.select().where(
            Clause(self.user.name == "O'Reilly")
            | Clause(self.user.age >= 18) & Clause(self.user.name == 'Nikita')
        ))
        expected = 'SELECT * FROM "users" ' + \
            'WHERE ("users"."name" = \'O\'\'Reilly\' OR ' + \
            '"users"."age" >= 18 AND "users"."name" = \'Nikita\')'

        self.assertEquals(query, expected)

        query = str(self.user.select().where(
            (Clause(self.user.name == "O'Reilly") | Clause(self.user.age >= 18))
            & Clause(self.user.name == 'Nikita')
        ))
        expected = 'SELECT * FROM "users" ' + \
            'WHERE ("users"."name" = \'O\'\'Reilly\' OR "users"."age" >= 18) ' + \
            'AND "users"."name" = \'Nikita\''

        self.assertEquals(query, expected)

        query = str(self.user.select().where(
            (Clause(self.user.name == "O'Reilly") | Clause(self.user.age >= 18))
            & Clause(self.user.name == 'Nikita') | True
        ))
        expected = 'SELECT * FROM "users" ' + \
            'WHERE (("users"."name" = \'O\'\'Reilly\' OR "users"."age" >= 18) ' + \
            'AND "users"."name" = \'Nikita\' OR true)'

        self.assertEquals(query, expected)

        query = str(self.user.select().where(
            Clause(self.user.name.upper() == 'NIKITA')
        ))
        expected = 'SELECT * FROM "users" WHERE upper("users"."name") = \'NIKITA\''

        self.assertEquals(query, expected)

        query = str(self.user.select().where(Expression('random() > 0.5')))
        expected = 'SELECT * FROM "users" WHERE random() > 0.5'

        self.assertEquals(query, expected)

    def test_insert(self):
        """Tests simple insertions"""
        query = str(self.user.insert(
            (self.user.name, self.user.age),
            (('Nikita', 23),),
        ))
        expected = 'INSERT INTO "users" ("users"."name", "users"."age") ' + \
            'VALUES (\'Nikita\', 23)'

        self.assertEquals(query, expected)
