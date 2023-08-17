from unittest import TestCase

from py_data_rules.column import Column
from py_data_rules.data_type import XSDFloat
from py_data_rules.schema import Schema


class TestSchema(TestCase):
    def test_add_columns_and_get_labels(self):
        s = Schema()
        c = Column("A")
        s.add_column(c)
        s.add_column("B")
        self.assertEqual(s.get_column_labels(), ["A", "B"])

    def test_add_column(self):
        s = Schema()
        c = Column("A")
        s.add_column(c)
        # try to add the same column twice
        self.assertRaises(AssertionError, s.add_column, c)
        # try to add a new column with existing name but different dtype
        d = Column("A", data_type=XSDFloat())
        self.assertRaises(AssertionError, s.add_column, d)
