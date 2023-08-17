import re
from abc import ABC, abstractmethod
from datetime import datetime


class DataType(ABC):  # TODO: this should be interface
    @staticmethod
    @abstractmethod
    def match(instance: str) -> bool:
        assert instance
        return NotImplementedError

    @staticmethod  # TODO: this should be abstract
    def repair(instance: str):
        assert instance
        return None


class XSDString(DataType):
    def __init__(self, pattern=None):
        self.pattern = pattern or r".*"

    def match(self, instance):
        assert instance
        if re.match(self.pattern, instance):
            return True
        else:
            return False


class XSDInteger(DataType):
    @staticmethod
    def match(instance):
        assert instance
        if "." in instance:
            return False
        try:
            int(instance)
            return True
        except ValueError:
            return False

    @staticmethod
    def repair(instance):
        assert instance
        try:
            return str(int(float(instance)))
        except ValueError:
            return None


class XSDFloat(DataType):
    @staticmethod
    def match(instance):
        assert instance
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


class XSDDate(DataType):
    def __init__(self, formats=None):
        self.formats = formats or ["%Y-%m-%d"]  # ISO 8601
        if isinstance(formats, str):
            self.formats = [self.formats]

    def match(self, instance):
        assert instance
        for fmt in self.formats:
            try:
                datetime.strptime(instance, fmt)
                return True
            except ValueError:
                pass
        return False


class XSDDateTime(XSDDate):
    def __init__(self, formats=None):
        self.formats = formats or ["%Y-%m-%dT%H:%M:%SZ"]  # ISO 8601
        super().__init__(self.formats)


class XSDBoolean(DataType):
    @staticmethod
    def match(instance):
        assert instance
        if instance in ["true", "false", "1", "0"]:
            return True
        else:
            return False

    @staticmethod
    def repair(instance: str):
        assert instance
        trues = ["Y", "y", "yes"]
        falses = ["N", "n", "no"]
        if instance in trues:
            return "true"
        elif instance in falses:
            return "false"
        else:
            return None


class XSDAnyURI(DataType):
    def __init__(self, base_uri=None):
        self.base_uri = base_uri or ""

    @staticmethod
    def match(instance):
        assert instance
        if re.match(r".+:.+", instance):
            return True
        else:
            return False

    def repair(self, instance: str):
        assert instance
        instance = self.base_uri + instance
        if self.match(instance):
            return instance
        else:
            return None
