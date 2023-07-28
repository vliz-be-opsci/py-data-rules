from .data_model import DataModel
from .violation import Violation
import pandas as pd
from datetime import datetime
from typing import List, Callable
import re
import logging

logger = logging.getLogger(__name__)

def assert_schema(data_model: DataModel) -> List[Violation]:
    violations = []
    for alias, table in data_model.items():
        df_columns = set(table.columns)
        schema_columns = set(table.schema.get_column_labels())
        missing_columns = schema_columns - df_columns
        excess_columns = df_columns - schema_columns
        if missing_columns: logger.warning(f"missing columns in table {alias}: {missing_columns}")
        if excess_columns: logger.warning(f"excess columns in table {alias}: {excess_columns}")
        relevant_columns = [c for c in table.schema.columns if c.label in (schema_columns - missing_columns)]
        for c in relevant_columns:
            for index, value in table[c.label].items():
                if str(value) == "nan" and c.nullable:
                    continue
                if str(value) == "nan" and not c.nullable:
                    violations.append(
                        Violation(
                            diagnosis="missing value",
                            table=table,
                            column=c,
                            row=index + 1,
                            value=value,
                        )
                    )
                    continue
                # TODO: if ...
                #   check trim whitespace ...
                if not c.data_type.match(str(value)):
                    repair = c.data_type.repair(str(value)) or ""
                    violations.append(
                        Violation(
                            diagnosis="datatype mismatch",
                            table=table,
                            column=c,
                            row=index + 1,
                            value=value,
                            repair=repair,
                        )
                    )
                    continue
    return violations


def regex(column, pattern, table_aliases) -> Callable:
    def fn(data_model: DataModel) -> List[Violation]:
        violations = []
        for ta in table_aliases:
            df = data_model[ta]
            for index, row in df.iterrows():
                if not pd.isna(row[column]):
                    if not re.match(pattern, row[column]):
                        violations.append(
                            Violation(
                                diagnosis="regex violation",
                                table=ta,
                                column=column,
                                row=index + 1,
                                value=row[column],
                                extended_diagnosis=f"{column} must match {pattern}",
                            )
                        )
        return violations
    return fn


def membership(column, members, table_aliases: list) -> Callable:
    def fn(data_model: DataModel) -> List[Violation]:
        violations = []
        for ta in table_aliases:
            df = data_model[ta]
            invalid_row_indices = df[~df[column].isin(members)].index.tolist()
            for index in invalid_row_indices:
                violations.append(
                    Violation(
                        diagnosis="membership violation",
                        table=ta,
                        column=column,
                        row=index + 1,
                        value=df.at[index, column],
                        extended_diagnosis=f'{column} must be in {list(members)}',
                    )
                )
        return violations
    return fn


def x_after_y(x: str, y: str, table_aliases: list) -> Callable:
    """ Date X must be NULL or after date Y
    """
    def fn(data_model: DataModel) -> List[Violation]:
        violations = []
        for ta in table_aliases:
            df = data_model[ta]
            for index, row in df.iterrows():
                if not pd.isna(row[x]):
                    if not (
                        datetime.strptime(row[x], "%Y-%m-%d")
                        >= datetime.strptime(row[y], "%Y-%m-%d")
                    ):
                        violations.append(
                            Violation(
                                diagnosis="x after y violation",
                                table=ta,
                                column=x,
                                row=index + 1,
                                value=row[x],
                                extended_diagnosis=f"{x} must be after {y} (y = {row[y]})",
                            )
                        )
        return violations
    return fn


# TODO: cleanup
# def fn_xyz(model: DataModel) -> List[Violation]:
#     pass

# rules: List[Rule] = [Rule(fn_xyz), ...]

# class KnownRules(Enum):
#     XYZ = Rule(fn_xyz)

# def fn_emobon_eval1(model) -> List:
#     pass

# class KnownEMOBONRules(Enum):
#     EVAL1=Rule(fn_emobon_eval1)

# myrules = [KnownRules.XYZ, KnownEMOBONRules.EVAL1, ...]