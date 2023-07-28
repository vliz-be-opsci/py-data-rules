from .table import Table

class DataModel:
    def __init__(self, description: dict):
        for k, v in description.items():
            assert "path" in v.keys(), f'no "path" defined for alias "{k}"'
            assert "reader" in v.keys(), f'no "reader" defined for alias "{k}"'
            assert "schema" in v.keys(), f'no "schema" defined for alias "{k}"'
        self.description: dict = description
        self.tables: dict = {}
        self._generate_tables()


    def _generate_tables(self):
        for k, v in self.description.items():
            self.tables.update({
                k: Table(
                    path=v["path"],
                    reader=v["reader"],
                    schema=v["schema"],
                    alias=k,
                )
            })
    
    def __getitem__(self, alias: str) -> Table:
        return self.tables[alias]

    def keys(self):
        return self.tables.keys()

    def values(self):
        return self.tables.values()

    def items(self):
        return self.tables.items()
