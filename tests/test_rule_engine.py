import pandas as pd

import py_data_rules.rule_factory as rf
from py_data_rules.column import Column
from py_data_rules.data_type import DataType, XSDDate, XSDFloat, XSDInteger
from py_data_rules.rule_engine import RuleEngine
from py_data_rules.schema import Schema
from py_data_rules.violation import Violation


def read_wobs(path) -> pd.DataFrame:
    return pd.read_csv(path, delimiter=";")


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


def test_report():
    report_path = "./tests/resources/report.csv"
    RuleEngine(data_model, rules).execute(report_path)
    df = pd.read_csv(report_path)
    assert (
        df["diagnosis"][(df["column"] == "time_utc") & (df["row"] == 17)].iloc[
            0
        ]
        == "regex violation"
    )
    assert (
        df["diagnosis"][(df["column"] == "date") & (df["row"] == 8554)].iloc[0]
        == "date violation"
    )
    assert (
        df["diagnosis"][(df["column"] == "date") & (df["row"] == 15)].iloc[0]
        == "datatype mismatch"
    )
    assert (
        df["diagnosis"][
            (df["column"] == "temperature") & (df["row"] == 8615)
        ].iloc[0]
        == "datatype mismatch"
    )
    assert (
        df["diagnosis"][(df["column"] == "humidity") & (df["row"] == 7)].iloc[
            0
        ]
        == "datatype mismatch"
    )
    assert (
        df["diagnosis"][(df["column"] == "pressure") & (df["row"] == 1)].iloc[
            0
        ]
        == "datatype mismatch"
    )
    assert (
        df["diagnosis"][
            (df["column"] == "precipitation") & (df["row"] == 4)
        ].iloc[0]
        == "missing value"
    )
    assert (
        df["diagnosis"][
            (df["column"] == "precipitation") & (df["row"] == 5)
        ].iloc[0]
        == "missing value"
    )
    assert (
        df["diagnosis"][
            (df["column"] == "wind_direction") & (df["row"] == 1)
        ].iloc[0]
        == "datatype mismatch"
    )
    assert (
        df["diagnosis"][
            (df["column"] == "wind_speed") & (df["row"] == 16)
        ].iloc[0]
        == "datatype mismatch"
    )
