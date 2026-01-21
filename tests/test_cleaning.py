"""
test_cleaning.py

Tests for cleaning.py:
- numeric columns are imputed (no NaNs remain there)
- productivity_gap is created
- key columns are numeric after coercion
"""

import pandas as pd

from src.social_media_productivity.constants import (
    NUMERIC_COLS_FOR_IMPUTATION,
    COL_GAP,
    COL_PERCEIVED,
    COL_ACTUAL,
)


def test_cleaning_creates_gap_column(df_clean: pd.DataFrame) -> None:
    """Cleaning must create the productivity gap feature."""
    assert COL_GAP in df_clean.columns


def test_cleaning_imputes_numeric_columns(df_clean: pd.DataFrame) -> None:
    """After cleaning, numeric columns used for analysis should have no NaNs."""
    for col in NUMERIC_COLS_FOR_IMPUTATION:
        assert df_clean[col].isna().sum() == 0, f"Expected no NaNs in '{col}' after imputation."


def test_gap_is_difference(df_clean: pd.DataFrame) -> None:
    """
    Gap must equal perceived - actual for all rows (within floating tolerance).
    """
    computed = df_clean[COL_PERCEIVED] - df_clean[COL_ACTUAL]
    # pandas Series comparison with float safety
    assert (df_clean[COL_GAP].round(10) == computed.round(10)).all()
