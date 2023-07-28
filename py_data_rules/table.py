import pandas as pd


class Table(pd.DataFrame):
    def __init__(self, path, reader, schema, *args, alias=None, **kwargs):
        super().__init__(data=reader(path), *args, **kwargs)
        assert not hasattr(self, "path")
        assert not hasattr(self, "reader")
        assert not hasattr(self, "schema")
        assert not hasattr(self, "alias")
        self.path = path
        self.reader = reader
        self.schema = schema
        self.alias = alias
