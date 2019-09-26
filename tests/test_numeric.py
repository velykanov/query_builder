"""Numeric field test module"""
import unittest

from .. import fields


class TestCase(unittest.TestCase):
    """Tests numeric fields for correct operations execution"""

    def test_decimal_aliasing(self):
        """Tests Decimal aliasing"""
        decimal = fields.Decimal('simple_decimal')
        self.assertEqual(str(decimal), '"simple_decimal"')

        decimal.set_alias('alias')
        self.assertEqual(str(decimal), '"simple_decimal" AS "alias"')

        decimal.set_table_prefix("table")
        self.assertEqual(str(decimal), '"table"."simple_decimal" AS "alias"')

    def test_decimal_operations(self):
        """Tests Decimal operations"""
        decimal = fields.Decimal('decimal')
        self.assertEqual(str(decimal + 2), '"decimal" + 2')
        self.assertEqual(str(decimal + 2.0), '"decimal" + 2.0')
        self.assertEqual(str(decimal - 2), '"decimal" - 2')
        self.assertEqual(str(decimal - 2.0), '"decimal" - 2.0')
        self.assertEqual(str(decimal * 2), '"decimal" * 2')
        self.assertEqual(str(decimal * 2.0), '"decimal" * 2.0')
        self.assertEqual(str(decimal / 2), '"decimal" / 2')
        self.assertEqual(str(decimal / 2.0), '"decimal" / 2.0')
        self.assertEqual(str(decimal % 2), '"decimal" % 2')
        self.assertEqual(str(decimal % 2.0), '"decimal" % 2.0')
        self.assertEqual(str(decimal // 2), 'div("decimal", 2)')
        self.assertEqual(str(decimal // 2.0), 'div("decimal", 2.0)')
        self.assertEqual(str(decimal ** 2), '"decimal" ^ 2')
        self.assertEqual(str(decimal ** 2.0), '"decimal" ^ 2.0')
