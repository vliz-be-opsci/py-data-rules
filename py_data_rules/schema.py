from .column import Column


class Schema:
    def __init__(self, columns=None):
        self.columns = columns or []
        assert len(self.columns) == len(set(self.get_column_labels()))

    def get_column_labels(self):
        return [c.label for c in self.columns]

    def add_column(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Column):
            column = args[0]
        else:
            column = Column(*args, **kwargs)
        assert column.label not in self.get_column_labels()
        self.columns.append(column)
