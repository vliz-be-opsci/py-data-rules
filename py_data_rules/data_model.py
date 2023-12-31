from .table import Table


class DataModel:
    def __init__(self, description: dict, na_literal: str = "N/A"):
        required_keys = {"path", "reader", "schema"}
        for alias, descr in description.items():
            missing_keys = required_keys - descr.keys()
            assert not missing_keys, (
                f"missing key(s) {missing_keys} in description for alias "
                f"{alias}"
            )
        self.description: dict = description
        self.na_literal: str = na_literal
        self.null_literal: str = ""
        self.tables: dict = {}
        self._generate_tables()

    def _generate_tables(self):
        for alias, descr in self.description.items():
            self.tables.update({alias: Table(**descr, alias=alias)})

    def __getitem__(self, alias: str) -> Table:
        return self.tables[alias]

    def keys(self):
        return self.tables.keys()

    def values(self):
        return self.tables.values()

    def items(self):
        return self.tables.items()

    def isna(self, value: str) -> bool:
        return value in (self.null_literal, self.na_literal)
