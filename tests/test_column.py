from unittest import TestCase

from py_data_rules.column import Column
from py_data_rules.data_type import XSDFloat


class TestColumn(TestCase):
    def test_init(self):
        dt = XSDFloat()
        c = Column("A", data_type=dt, nullable=True, trim="leading")
        self.assertEqual(c.label, "A")
        self.assertEqual(c.data_type, dt)
        self.assertEqual(c.nullable, True)
        self.assertEqual(c.trim, "leading")
