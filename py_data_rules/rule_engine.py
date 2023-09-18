import csv
import logging
from inspect import getmembers, isfunction
from types import ModuleType
from typing import Callable, Dict, List, Union

from .data_model import DataModel
from .rule import Rule
from .rule_factory import assert_schema
from .violation import Violation

logger = logging.getLogger(__name__)


class RuleEngine:  # TODO: find better name, e.g. QCExecutor, or even better
    def __init__(
        self,
        data_model: Union[DataModel, Dict, ModuleType],
        rules: Union[List[Rule], ModuleType] = None,
        implicit: bool = True,
    ):
        self.violations: List[Violation] = []
        if isinstance(data_model, DataModel):
            self.data_model = data_model
        elif isinstance(data_model, Dict):
            self.data_model = DataModel(data_model)
        elif isinstance(data_model, ModuleType):
            data_model_retrieval_flag = False
            for _, value in getmembers(data_model):
                if isinstance(value, DataModel):
                    self.data_model = value
                    data_model_retrieval_flag = True
                    break
            if not data_model_retrieval_flag:
                raise RuntimeError(f"no DataModel found in {data_model}")
        else:
            raise TypeError(
                "data_model must be a DataModel, Dict or Module,"
                f" not {type(data_model)}"
            )
        self.rules = []
        if not rules:
            pass
        elif isinstance(
            rules, List
        ):  # TODO: should be able to accept a single Rule or Callable as well
            for rule in rules:
                if isinstance(rule, Rule):
                    self.rules.append(rule)
                elif isinstance(rule, Callable):
                    self.rules.append(Rule(rule))
                else:
                    raise TypeError(
                        f"rule must be a Rule or a Callable, not {type(rule)}"
                    )
        elif isinstance(rules, ModuleType):
            for name, value in getmembers(rules, isfunction):
                # if name.endswith("_rule"):
                self.rules.append(Rule(value, name))
        else:
            raise TypeError(
                f"rules must be a List or a Module, not {type(rules)}"
            )
        if implicit:
            self.rules.extend([Rule(assert_schema)])

    def _export_violations(self, report_path):
        # TODO: add json serialization
        with open(report_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "diagnosis",
                    "table",
                    "column",
                    "row",
                    "value",
                    "repair",
                    "extended_diagnosis",
                    "file_path",
                    "data_type",
                    "nullable",
                ]
            )
            for violation in self.violations:
                s = violation.serialize(self.data_model)
                w.writerow(s.values())

    def execute(self, report_path="."):
        for rule in self.rules:
            try:
                self.violations.extend(rule.evaluator(self.data_model))
            except Exception as e:
                logger.error(
                    f"rule evaluation failed for {rule.name}"
                    f" with exception {type(e).__name__}: {e}"
                )
        self._export_violations(report_path=report_path)
        return self.violations
