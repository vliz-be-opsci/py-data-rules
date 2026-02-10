import numpy as np
import pandas as pd


def read_dsv(path, delimiter=None) -> pd.DataFrame:
    """Read a delimiter-separated values (DSV) file into a pandas DataFrame."""
    df = (
        pd.read_csv(
            path, delimiter=delimiter, dtype=object, keep_default_na=False
        )
        .astype(str)
        .reset_index(drop=True)  # drop the old index
        .map(lambda _: _.strip())
        .map(lambda _: np.nan if _ == "" else _)
    )
    df = df[~(df == np.nan).all(axis=1)]  # drop empty rows
    return df


def write_dsv(df: pd.DataFrame, path: str) -> None:
    """Write a pandas DataFrame to a delimiter-separated values (DSV) file."""
    df.to_csv(path, index=False)
