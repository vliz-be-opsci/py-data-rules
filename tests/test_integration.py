import pandas as pd

import py_data_rules.rule_factory as rf
from py_data_rules.column import Column
from py_data_rules.data_type import DataType, XSDDate, XSDFloat, XSDInteger
from py_data_rules.dsv import read_dsv
from py_data_rules.rule_engine import RuleEngine
from py_data_rules.schema import Schema
from py_data_rules.violation import Violation


def read_wobs(path):
    return read_dsv(path, delimiter=";")


class Angle(DataType):
    @staticmethod
    def match(instance):
        assert instance
        try:
            assert (float(instance) >= 0) and (float(instance) < 360)
            return True
        except (ValueError, AssertionError):
            return False


schema = Schema(
    [
        Column("date", XSDDate()),
        Column("time_utc"),
        Column("temperature", XSDFloat()),
        Column("humidity", XSDInteger()),
        Column("pressure", XSDInteger()),
        Column("precipitation", XSDFloat()),
        Column("wind_direction", Angle()),
        Column("wind_speed", XSDFloat()),
    ]
)

data_model = {
    "wmay": {
        "path": "./tests/resources/weather_observations_may.csv",
        "reader": read_wobs,
        "schema": schema,
    },
    "wjun": {
        "path": "./tests/resources/weather_observations_june.csv",
        "reader": read_wobs,
        "schema": schema,
    },
}

time_utc_rule = rf.regex("time_utc", r"^\d{2}:\d{2}:\d{2}$", ["wmay", "wjun"])


def date_rule(data_model):
    violations = []
    df_may = data_model["wmay"]
    df_june = data_model["wjun"]
    for index, row in df_june.iterrows():
        if row["date"] <= df_may["date"].max():
            violations.append(
                Violation(
                    diagnosis="date violation",
                    table="wjun",
                    column="date",
                    row=index + 1,
                    value=row["date"],
                    extended_diagnosis=(
                        f"date must be after {df_may['date'].max()}"
                    ),
                )
            )
    return violations


rules = [time_utc_rule, date_rule]


def test_main():
    report_path = "./tests/resources/report.csv"
    RuleEngine(data_model, rules).execute(report_path)
    df = pd.read_csv(report_path)
    edits = [
        ("time_utc", 17, "regex violation"),
        ("date", 8554, "date violation"),
        ("date", 15, "datatype mismatch"),
        ("temperature", 8615, "datatype mismatch"),
        ("humidity", 7, "datatype mismatch"),
        ("pressure", 1, "datatype mismatch"),
        ("precipitation", 4, "missing value"),
        ("precipitation", 5, "missing value"),
        ("wind_direction", 1, "datatype mismatch"),
        ("wind_speed", 16, "datatype mismatch"),
    ]
    for c, r, d in edits:
        assert (
            df["diagnosis"][(df["column"] == c) & (df["row"] == r)].iloc[0]
            == d
        )


# this block isn't required for pytest, but is useful for
# test-driven development
if __name__ == "__main__":
    test_main()
