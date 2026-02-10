"""https://www.w3.org/TR/xmlschema-2/#built-in-datatypes
"""
import re
from abc import ABC, abstractmethod
from datetime import datetime


class DataType(ABC):
    """Any DataType assumes that no None or "" is passed to its methods.
    This is ensured by the assert_schema rule.
    """

    @staticmethod
    @abstractmethod
    def match(instance: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def repair(instance: str) -> str | None:
        """This method should not be abstract as not all extended data types
        will override it.
        """
        return None


class XSDAnyType(DataType):
    ...


class XSDAnySimpleType(XSDAnyType):
    ...


class XSDString(XSDAnySimpleType):
    def __init__(self, pattern=None):
        self.pattern = pattern or r".*"

    def match(self, instance):
        if re.match(self.pattern, instance):
            return True
        else:
            return False


class XSDInteger(XSDAnySimpleType):
    @staticmethod
    def match(instance):
        if "." in instance:
            return False
        try:
            int(instance)
            return True
        except ValueError:
            return False

    @staticmethod
    def repair(instance):
        try:
            return str(int(float(instance)))
        except ValueError:
            return None


class XSDFloat(XSDAnySimpleType):
    @staticmethod
    def match(instance):
        try:
            float(instance)
            return True
        except ValueError:
            return False

    @classmethod
    def repair(cls, instance: str):
        def _find(string, char):
            return [i for i, c in enumerate(string) if c == char]

        transformation = (
            instance.replace(" ", "").replace("'", "").replace("_", "")
        )
        p = _find(transformation, ".")
        c = _find(transformation, ",")

        if not p and not c:
            pass
        elif p and not c:
            if len(p) == 1:
                pass
            else:
                transformation = transformation.replace(".", "")
        elif not p and c:
            if len(c) == 1:
                transformation = transformation.replace(",", ".")
            else:
                transformation = transformation.replace(",", "")
        else:
            if p[0] > c[-1]:
                transformation = transformation.replace(",", "")
            else:
                transformation = transformation.replace(".", "").replace(
                    ",", "."
                )

        if cls.match(transformation):
            return transformation
        else:
            return None


class XSDDouble(XSDAnySimpleType):
    ...


class XSDDate(XSDAnySimpleType):
    def __init__(self, formats=None):
        self.formats = formats or ["%Y-%m-%d"]  # ISO 8601
        if isinstance(formats, str):
            self.formats = [self.formats]

    def match(self, instance):
        for fmt in self.formats:
            try:
                datetime.strptime(instance, fmt)
                return True
            except ValueError:
                pass
        return False

    def repair(self, instance: str):
        datetime_truncation = instance[0:10]
        if self.match(datetime_truncation):
            return datetime_truncation
        else:
            return None


class XSDDateTime(XSDDate):  # TODO inherit from XSDAnySimpleType
    def __init__(self, formats=None):
        self.formats = formats or ["%Y-%m-%dT%H:%M:%SZ"]  # ISO 8601
        super().__init__(self.formats)


class XSDBoolean(XSDAnySimpleType):
    @staticmethod
    def match(instance):
        if instance in ["true", "false", "1", "0"]:
            return True
        else:
            return False

    @staticmethod
    def repair(instance: str):
        trues = ["t", "true", "y", "yes"]
        falses = ["f", "false", "n", "no"]
        instance_lower = instance.lower()
        if instance_lower in trues:
            return "true"
        elif instance_lower in falses:
            return "false"
        else:
            return None


class XSDAnyURI(XSDAnySimpleType):
    def __init__(self, base_uri=None):
        self.base_uri = base_uri or ""

    @staticmethod
    def match(instance):
        if re.match(r".+:.+", instance):
            return True
        else:
            return False

    def repair(self, instance: str):
        instance = self.base_uri + instance
        if self.match(instance):
            return instance
        else:
            return None
