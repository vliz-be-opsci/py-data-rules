from .column import Column


class Schema:
    def __init__(self, columns=None):
        self.columns = columns or []
        assert len(self.columns) == len(set(self.get_column_labels()))

    def get_column_labels(self):
        return [c.label for c in self.columns]

    def add_column(self, *args, **kwargs):
        column = Column(*args, **kwargs)
        assert column.label not in self.get_column_labels()
        self.columns.append(column)

    # TODO: make this behave as a dict
    # useful to make this expose itself dictlike as a label -> column thing
    # so one can simply, given a schema
    # s: Schema
    # test if a column-label is in there
    #   "mycolumn" in s
    # loop over columns
    #   for label, col in s.items()
