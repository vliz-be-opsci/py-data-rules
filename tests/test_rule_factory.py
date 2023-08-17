from unittest import TestCase

import pandas as pd

import py_data_rules.rule_factory as rf
from py_data_rules.column import Column
from py_data_rules.data_type import XSDDate, XSDFloat, XSDInteger
from py_data_rules.rule_engine import RuleEngine
from py_data_rules.schema import Schema


class TestRuleFactory(TestCase):
    def test_rules(self):
        def read_wobs(path) -> pd.DataFrame:
            return pd.read_csv(path, delimiter=";")

        schema = Schema(
            [
                Column("date", XSDDate()),
                Column("time_utc"),
                Column("temperature", XSDFloat()),
                Column("humidity", XSDInteger()),
                Column("pressure", XSDInteger()),
                Column("precipitation", XSDFloat()),
                Column("wind_direction"),
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

        date_rule = rf.x_after_y("date", "date", ["wmay", "wjun"])
        time_utc_rule = rf.regex(
            "time_utc", r"^\d{2}:\d{2}:\d{2}$", ["wmay", "wjun"]
        )
        humidity_rule = rf.membership(
            "humidity", [i for i in range(101)], ["wmay", "wjun"]
        )

        rules = [date_rule, time_utc_rule, humidity_rule]

        report_path = "./tests/resources/report_test_rule_factory.csv"
        RuleEngine(data_model, rules).execute(report_path)
