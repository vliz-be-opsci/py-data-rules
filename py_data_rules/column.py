from .data_type import DataType

class Column:
    def __init__(self, label, data_type: DataType, nullable, trim=None):
        self.label = label
        self.data_type = data_type
        self.nullable = nullable
        self.trim = trim
        assert isinstance(self.data_type, DataType), "data_type must be an instance of DataType"
        if self.trim:
            assert trim in ("leading", "trailing", "both") # TODO: enum -> e.g. Trimming.BOTH