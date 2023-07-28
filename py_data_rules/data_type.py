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


class XSDString(DataType):  # TODO: allow to instantiate XSDString with regex,
    # as opposed to using rule_factory.regex
    @staticmethod
    def match(instance):
        assert instance
        return True


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
            return int(instance)
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
        self.formats = formats or ["%Y-%m-%d"]

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
        self.formats = formats or [
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ]  # TODO: verify this
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
    @staticmethod
    def match(instance):
        assert instance
        if re.match(r".+:.+", instance):
            return True
        else:
            return False


if __name__ == "__main__":  # TODO: these should become proper unit tests
    print(XSDFloat.repair("ATextField"))
    print(XSDFloat.repair("8603700"))
    print(XSDFloat.repair("8,603,700"))
    print(XSDFloat.repair("8.603.700"))
    print(XSDFloat.repair("8603700.80"))
    print(XSDFloat.repair("8603700,80"))
    print(XSDFloat.repair("8 603 700.80"))
    print(XSDFloat.repair("8 603 700,80"))
    print(XSDFloat.repair("8'603'700.80"))
    print(XSDFloat.repair("8'603'700,80"))
    print(XSDFloat.repair("8_603_700.80"))
    print(XSDFloat.repair("8_603_700,80"))
    print(XSDFloat.repair("8,603,700.80"))
    print(XSDFloat.repair("8.603.700,80"))
