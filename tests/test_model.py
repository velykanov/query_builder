"""Model test module"""
import unittest

from query_builder import fields
from query_builder.expressions import Clause
from query_builder.expressions import Expression
from query_builder.models import Model
from query_builder.models import LEFT_JOIN


class TestCase(unittest.TestCase):
    """Tests model for building correct queries"""

    @classmethod
    def setUpClass(cls):
        """Initiates user's models"""
        class User(Model):
            """User's model"""
            id_ = fields.Integer('id')
            name = fields.Char('name', max_length=32)
            surname = fields.Char('surname', max_length=32)
            age = fields.Integer('age')

        class UserPet(Model):
            """User's pets model"""
            name = fields.Char('name', max_length=32)
            users_id = fields.Integer('users_id')

        cls.user = User('users')
        cls.user_pet = UserPet('users_pets')

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

        query = str(self.user.select(
            self.user.name + ' ' + self.user.surname,
        ))
        expected = 'SELECT "users"."name" || \' \' || "users"."surname" FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(self.user.age * 2 * 3 / 2))
        expected = 'SELECT (("users"."age" * 2) * 3) / 2 FROM "users"'

        self.assertEquals(query, expected)

    def test_select_distinct(self):
        """Tests unique tuples selection"""
        query = str(self.user.select().distinct())
        expected = 'SELECT DISTINCT * FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select().distinct(self.user.name))
        expected = 'SELECT DISTINCT ON ("users"."name") * FROM "users"'

        self.assertEquals(query, expected)

        query = str(self.user.select(self.user.age).distinct(self.user.name))
        expected = 'SELECT DISTINCT ON ("users"."name") "users"."age" FROM "users"'

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

    def test_select_pagination(self):
        """Tests selects with LIMIT and OFFSET"""
        query = str(self.user.select().limit(10))
        expected = 'SELECT * FROM "users" LIMIT 10'

        self.assertEquals(query, expected)

        query = str(self.user.select().limit(10).offset(5))
        expected = 'SELECT * FROM "users" LIMIT 10 OFFSET 5'

        self.assertEquals(query, expected)

        query = str(self.user.select().offset(5))
        expected = 'SELECT * FROM "users" OFFSET 5'

        self.assertEquals(query, expected)

    def test_select_orderring(self):
        """Tests selects with ORDER BY clauses"""
        query = str(self.user.select().order(self.user.name))
        expected = 'SELECT * FROM "users" ORDER BY "users"."name" ASC'

        self.assertEquals(query, expected)

        query = str(self.user.select().order(-self.user.name))
        expected = 'SELECT * FROM "users" ORDER BY "users"."name" DESC'

        self.assertEquals(query, expected)

        query = str(self.user.select().order(self.user.name, -self.user.age))
        expected = 'SELECT * FROM "users" ORDER BY "users"."name" ASC, "users"."age" DESC'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name.set_alias('__n'),
        ).order(self.user.name))
        expected = 'SELECT "users"."name" AS "__n" FROM "users" ORDER BY "__n" ASC'

        self.assertEquals(query, expected)

        # TODO: move this to reset_aliases
        self.user.name.set_alias(None)

    def test_select_grouping(self):
        """Tests selects with GROUP BY and HAVING clauses"""
        query = str(self.user.select(
            self.user.name,
            self.user.age.avg(),
        ).group(
            self.user.name,
        ))
        expected = 'SELECT "users"."name", avg("users"."age") FROM "users" ' + \
            'GROUP BY "users"."name"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name,
            self.user.age.array_agg(),
        ).group(
            self.user.name,
        ))
        expected = 'SELECT "users"."name", array_agg("users"."age") FROM "users" ' + \
            'GROUP BY "users"."name"'

        self.assertEquals(query, expected)

        query = str(self.user.select(
            self.user.name,
            self.user.age.avg(),
        ).group(
            self.user.name,
        ).having(
            self.user.name.count() > 1,
        ))
        expected = 'SELECT "users"."name", avg("users"."age") FROM "users" ' + \
            'GROUP BY "users"."name" HAVING count("users"."name") > 1'

        self.assertEquals(query, expected)

    def test_select_join(self):
        """Tests selects with join clause"""
        query = str(self.user.select().join(
            model=self.user_pet,
            condition=self.user.id_ == self.user_pet.users_id,
            join_type=LEFT_JOIN,
        ))
        expected = 'SELECT * FROM "users" ' + \
            'LEFT JOIN "users_pets" ON "users"."id" = "users_pets"."users_id"'

        self.assertEquals(query, expected)

        query = str(self.user.set_alias('u').select().join(
            model=self.user_pet.set_alias('up'),
            condition=self.user.id_ == self.user_pet.users_id,
            join_type=LEFT_JOIN,
        ))
        expected = 'SELECT * FROM "users" AS "u" ' + \
            'LEFT JOIN "users_pets" AS "up" ON "u"."id" = "up"."users_id"'

        self.assertEquals(query, expected)

        self.user.reset_alias()
        self.user_pet.reset_alias()

    def test_select_with_cte(self):
        """Tests selecting with WITH CTE"""
        query = str(self.user.with_cte(
            'pets',
            self.user_pet.select(
                self.user_pet.users_id,
            ),
        ).select(
            self.user.name,
        ).set_alias('u').where(
            Clause(self.user.id_ == self.user_pet.users_id)
        ))
        expected = 'WITH "pets" AS ' + \
            '(SELECT "users_pets"."users_id" FROM "users_pets") ' + \
            'SELECT "u"."name" FROM "users" AS "u" WHERE "u"."id" = "pets"."users_id"'

        # TODO: aliasing in where clause WHERE "u"."id" = "pets"."users_id" AS "master_id"
        self.assertEquals(query, expected)

        self.user.reset_alias()
        self.user_pet.reset_alias()

    def test_insert(self):
        """Tests simple insertions"""
        query = str(self.user.insert(
            (self.user.name, self.user.age),
            (('Nikita', 23),),
        ))
        expected = 'INSERT INTO "users" ("users"."name", "users"."age") ' + \
            'VALUES (\'Nikita\', 23)'

        self.assertEquals(query, expected)

        # TODO: implement INSERT SELECT operations
        query = str(self.user.insert(
            (self.user.name, self.user.age),
            self.user.select(
                self.user.name,
                self.user.age + 3,
            ),
        ))
        expected = 'INSERT INTO "users" ("users"."name", "users"."age") ' + \
            'SELECT "users"."name", "users"."age" + 3 FROM "users"'

        self.assertEquals(query, expected)
