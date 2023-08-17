from unittest import TestCase

from py_data_rules.data_model import DataModel
from py_data_rules.rule import Rule
from py_data_rules.rule_engine import RuleEngine

from .resources import module_data_model, module_data_model_empty, module_rules


class TestRuleEngine(TestCase):
    def test_init(self):
        dm = DataModel(
            {
                "my_alias": {
                    "path": ".",
                    "reader": lambda _: None,
                    "schema": None,
                }
            }
        )
        RuleEngine(dm)
        RuleEngine(
            {
                "my_alias": {
                    "path": ".",
                    "reader": lambda _: None,
                    "schema": None,
                }
            }
        )
        RuleEngine(module_data_model)
        self.assertRaises(RuntimeError, RuleEngine, module_data_model_empty)
        self.assertRaises(TypeError, RuleEngine, "ATextField")
        RuleEngine(dm, [Rule(lambda _: None)])
        RuleEngine(dm, [lambda _: None])
        RuleEngine(dm, module_rules)
        self.assertRaises(TypeError, RuleEngine, dm, "ATextField")
