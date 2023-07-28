class Violation:
    def __init__(
        self,
        diagnosis,
        table,
        column,
        row: int,
        value,
        repair=None,
        extended_diagnosis=None,
    ):
        self.diagnosis = diagnosis
        self.table = table
        self.column = column
        self.row = row
        self.value = value
        self.repair = repair
        self.extended_diagnosis = extended_diagnosis

    def serialize(self, data_model):
        if isinstance(self.table, str):
            self.table = data_model[self.table]

        if isinstance(self.column, str):
            columns = [
                c for c in self.table.schema.columns if c.label == self.column
            ]
            assert len(columns) == 1
            self.column = columns[0]
            # TODO: use dict-like behaviour in schema, would be simplified to:
            # column = self.table.schema[column]

        return {
            "diagnosis": self.diagnosis,
            "table": self.table.alias,
            "column": self.column.label,
            "row": self.row,
            "value": self.value,
            "repair": self.repair,
            "extended_diagnosis": self.extended_diagnosis,
            "file_path": self.table.path,
            "data_type": type(self.column.data_type).__name__,
            "nullable": self.column.nullable,
        }
