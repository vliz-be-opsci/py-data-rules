from py_data_rules.data_model import DataModel

my_data_model = DataModel(
    {"my_alias": {"path": ".", "reader": lambda _: None, "schema": None}}
)
