from unittest import TestCase

from py_data_rules.data_model import DataModel


class TestDataModel(TestCase):
    def test_accessors(self):
        dm = DataModel(
            {
                "my_alias": {
                    "path": ".",
                    "reader": lambda _: None,
                    "schema": None,
                }
            }
        )
        self.assertEqual(list(dm.keys()), ["my_alias"])
        self.assertEqual(len(dm.values()), 1)
        self.assertEqual(list(dm.values())[0].alias, "my_alias")
        self.assertEqual(
            list(dm.items()), [("my_alias", list(dm.values())[0])]
        )
