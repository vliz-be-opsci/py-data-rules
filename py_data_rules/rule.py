from typing import Callable
# from abc import ABC, abstractmethod


# class RuleInterface(ABC):
#     @abstractmethod
#     def evaluate(self, data_model: DataModel, violations: List[Violation]) -> None:
#         return NotImplementedError


class Rule:
    def __init__(self, evaluator: Callable, name=None):
        self.evaluator = evaluator
        self.name = name or evaluator.__name__

    # def evaluate(self, data_model: DataModel, violations: List[Violation]) -> None:
    #     violations.extend(self.evaluator(data_model))


# class RuleComposite(RuleInterface):
#     def __init__(self, rules: Iterable[RuleInterface]):
#         self.rules = rules

#     def evaluate(self, data_model: DataModel, violations: List[Violation]) -> None:
#         for r in self.rules:
#             r.evaluate(data_model, violations)

